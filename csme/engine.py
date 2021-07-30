import logging
from abc import ABC, abstractmethod

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

        if settings.case_ignore_filter_enabled:
            expected = transition.statement.lower()
            inbound = message.lower()
        else:
            expected = transition.statement
            inbound = message

        return inbound == expected


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
            logging.info("%s talking...", self.context.current_speaker.name)
            speaker_message = self.context.current_speaker.speak(self.conversation, self.context.current_state)
            logging.info("%s message = '%s'", self.context.current_speaker.name, speaker_message)
            speaker_transition = next(
                filter(lambda t: self.matcher.matches(message=speaker_message, transition=t), valid_transitions)
            )
            logging.info("%s transition = '%s'", self.context.current_speaker.name, speaker_transition)
            self.context.current_listener.listen(speaker_message)
            self.context.current_state = speaker_transition.target
            self._toggle_roles()
