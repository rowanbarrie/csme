from typing import List

from csme import schema, model


# TODO: Is this really unmarshalling? Or just conversion?
# TODO:  Also is there a better way to do this?


def unmarshal_language(language_schema: str) -> model.Language:
    return model.Language(language_schema)


def unmarshal_state(state_schema: str) -> model.State:
    return model.State(state_schema)


def unmarshal_transition(transition_schema: schema.TransitionBase, states: List[model.State]) -> model.Transition:
    # Consider creating a state lookup instead of filtering twice?
    source = next(filter(lambda s: s.name == transition_schema.source, states))
    target = next(filter(lambda s: s.name == transition_schema.target, states))
    return model.Transition(source=source, target=target, sentence=transition_schema.sentence)


def unmarshal_conversation_space(conversation_space_schema: schema.ConversationSpaceBase) -> model.ConversationSpace:
    states = list(map(lambda s: unmarshal_state(s), conversation_space_schema.states))
    return model.ConversationSpace(name=conversation_space_schema.name,
                                   states=states)


def unmarshal_conversation(conversation_schema: schema.ConversationBase,
                           conversation_space: model.ConversationSpace) -> model.Conversation:
    language = unmarshal_language(conversation_schema.language)
    transitions = list(map(lambda t: unmarshal_transition(t, conversation_space.states),
                           conversation_schema.transitions))
    return model.Conversation(name=conversation_schema.name,
                              language=language,
                              conversation_space=conversation_space,
                              transitions=transitions)


def unmarshal_conversation_set(conversation_set: schema.ConversationSetBase) -> List[model.Conversation]:
    conversation_space = unmarshal_conversation_space(conversation_set.conversation_space)
    return list(map(lambda s: unmarshal_conversation(s, conversation_space), conversation_set.conversations))