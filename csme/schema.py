from typing import List

from pydantic import BaseModel


class TransitionBase(BaseModel):
    source: str
    target: str
    statement: str


class ConversationSpaceBase(BaseModel):
    name: str
    states: List[str]


class ConversationBase(BaseModel):
    name: str
    language: str
    conversation_space: str
    transitions: List[TransitionBase]


class ConversationSetBase(BaseModel):
    conversation_space: ConversationSpaceBase
    conversations: List[ConversationBase]
