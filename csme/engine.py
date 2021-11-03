import logging
import re
from abc import ABC, abstractmethod

from fuzzywuzzy import fuzz

from config import settings
from csme.model import Conversation, State, Transition


class Peer(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def speak(self, conversation: Conversation, from_state: State) -> str:
        pass

    @abstractmethod
    def listen(self, message: str):
        pass


# TODO: Maybe this should actually be called 'Conversation' and renaming the initial 'Conversation' to 'ConversationStateMachine' ?
class ConversationContext:
    current_state: State
    current_speaker: Peer
    current_listener: Peer


class SimpleComputerPeer(Peer):

    def speak(self, conversation: Conversation, from_state: State) -> str:
        valid_transitions = conversation.get_out_transitions(from_state)
        # Just select the first valid transition...
        # TODO: Add different selection strategy implementations here (e.g. seeded random) ?
        return valid_transitions[0].statement

    def listen(self, message: str):
        # Nothing to do...
        pass


class TransitionMatcher(ABC):

    @abstractmethod
    def matches(self, message: str, transition: Transition) -> bool:
        pass


class SimpleTransitionMatcher(TransitionMatcher):

    def matches(self, message: str, transition: Transition) -> bool:
        # TODO: Consider adding a pipeline of "processors" (filters? matchers) here, e.g. comprehending different aspects of
        #  speech

        # TODO: The below code is UGLY - in serious need of a refactor!

        # TODO: Can we add some typing to this?
        regex_map = {}
        statement_placeholders = re.findall("{.*?}", transition.statement)
        # statement_placeholder_names = list(map(
        #     lambda p: statement_variable.replace("{", "").replace("}", ""), statement_placeholders))
        for statement_variable in statement_placeholders:
            statement_variable_name = statement_variable.replace("{", "").replace("}", "")
            regex_map[statement_variable] = f"(?P<{statement_variable_name}>.*)"

        search_pattern = transition.statement

        for key, value in regex_map.items():
            logging.debug("key: %s, value: %s", key, value)
            search_pattern = re.sub(key, value, search_pattern)

        logging.debug("search_pattern: %s", search_pattern)

        match = re.search(search_pattern, message)
        if match:
            groups = match.groups()

            if len(groups) == len(statement_placeholders):
                logging.debug("Match! (%s)", len(groups))
                logging.debug("Groups: (%s)", str(groups))
                if len(groups) >= 1:
                    logging.info("Name: %s", match.group("name"))
                return True
            else:
                logging.info("No match!", len(groups))
                return False
        else:
            # TODO: What here?
            pass

        # # TODO: Do something with match.groups
        #
        # if settings.case_ignore_filter_enabled:
        #     expected = transition.statement.lower()
        #     inbound = message.lower()
        # else:
        #     expected = transition.statement
        #     inbound = message
        #
        # return inbound == expected


class ConversationEngine:
    # TODO: Matcher should be set in configuration!
    # TODO: Could be different for each peer?
    matcher = SimpleTransitionMatcher()

    def __init__(self, conversation: Conversation, peer_a: Peer, peer_b: Peer):
        self.conversation = conversation
        self.context = ConversationContext()
        self.peer_a = peer_a
        self.peer_b = peer_b
        self.context.current_state = self.conversation.get_start_state()
        self.context.current_speaker = self.peer_a
        self.context.current_listener = self.peer_b

    def _toggle_roles(self):
        self.context.current_speaker, self.context.current_listener = \
            self.context.current_listener, self.context.current_speaker

    def run(self):
        logging.info("Running engine...")
        while valid_transitions := self.conversation.get_out_transitions(self.context.current_state):
            logging.debug("%s talking...", self.context.current_speaker.name)
            speaker_message = self.context.current_speaker.speak(self.conversation, self.context.current_state)
            logging.debug("%s message = '%s'", self.context.current_speaker.name, speaker_message)

            matching_transitions = list(filter(lambda t: self.matcher.matches(message=speaker_message, transition=t),
                                               valid_transitions))
            if len(matching_transitions) == 1:
                speaker_transition = matching_transitions[0]
            elif len(matching_transitions) > 1:
                logging.warning("Multiple matching transitions! Taking first...")
                speaker_transition = matching_transitions[0]
            else:
                logging.info("Invalid statement, try again")
                continue

            logging.debug("%s transition = '%s'", self.context.current_speaker.name, speaker_transition)
            self.context.current_listener.listen(speaker_message)
            self.context.current_state = speaker_transition.target
            self._toggle_roles()
