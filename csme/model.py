from typing import List


# Could combine/replace this with pycountry language
class Language:
    def __init__(self, name: str):
        self.name = name


class State:
    def __init__(self, name: str):
        self.name = name

    # @classmethod
    # def from_names(cls, names: List[str]):
    #     return list(map(lambda name: cls(name), names))


class Transition:
    def __init__(self, source: State, target: State, sentence: str):
        self.source = source
        self.target = target
        self.sentence = sentence

    # @classmethod
    # def from_sentences(cls, sentences: List[str]):
    #     return list(map(lambda sentence: cls(sentence), sentences))


class ConversationSpace:
    def __init__(self, name: str, states: List[State]):
        self.name = name
        self.states = states


class Conversation:
    def __init__(self, name: str, language: Language, conversation_space: ConversationSpace, transitions: List[Transition]):
        self.name = name
        self.language = language
        self.conversation_space = conversation_space
        self.transitions = transitions
