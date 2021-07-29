import logging
from abc import ABC, abstractmethod

import networkx as nx

from csme.model import Conversation, State, Transition


class UserInterface(ABC):

    @abstractmethod
    def receive(self) -> str:
        pass

    @abstractmethod
    def send(self, message: str):
        pass


class Speaker(ABC):

    @abstractmethod
    def talk(self, from_state: State, conversation: Conversation) -> Transition:
        pass

    @abstractmethod
    def listen(self, transition: Transition):
        pass


class SimpleUserSpeaker(Speaker):

    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def talk(self, from_state: State, conversation: Conversation) -> Transition:
        user_input = self.user_interface.receive()
        # TODO: Make a "fuzzy" / regex version also (first of all for "Esmi ____" !)
        # Just expect user input to match transition sentence exactly
        return next(filter(
            lambda t: t.source == from_state and t.sentence == user_input,
            conversation.transitions))

    def listen(self, transition: Transition):
        self.user_interface.send(transition.sentence)
        pass


class SimpleComputerSpeaker(Speaker):

    def talk(self, from_state: State, conversation: Conversation) -> Transition:
        out_transitions = conversation.get_transitions(from_state)
        # Just traverse the first transition in the list...
        # FIXME: Get this line working!!!
        return out_transitions[0]

    def listen(self, transition: Transition):
        # Nothing to do...
        pass


class ConversationEngine:

    def __init__(self, conversation: Conversation, speaker_a: Speaker, speaker_b: Speaker):
        self.conversation = conversation
        self.speaker_a = speaker_a
        self.speaker_b = speaker_b

    def run(self):
        logging.info("Running engine...")
        current_state: State = self.conversation.get_start_state()
        out_transitions = self.conversation.get_transitions(current_state)
        while out_transitions:
            logging.info("Speaker A talking...")
            speaker_a_transition = self.speaker_a.talk(current_state, self.conversation)
            logging.info(f"Speaker A transition = '{speaker_a_transition}'")
            self.speaker_b.listen(speaker_a_transition)
            current_state = speaker_a_transition.target
            # TODO: Handle case where we are at a final state here!
            logging.info("Speaker B talking...")
            speaker_b_transition = self.speaker_b.talk(current_state, self.conversation)
            logging.info(f"Speaker B transition = '{speaker_b_transition}'")
            self.speaker_a.listen(speaker_b_transition)
            current_state = speaker_b_transition.target
            out_transitions = self.conversation.get_transitions(current_state)
