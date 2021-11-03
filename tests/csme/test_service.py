from typing import List

from csme import data
from csme.engine import Peer
from csme.service import render, render_no_states, run_engine
from csme.model import Conversation, State


class FakeUserPeer(Peer):

    def __init__(self, statement_list: List[str]):
        super().__init__("fakeUserPeer")
        self.statement_list = statement_list

    def speak(self, conversation: Conversation, from_state: State) -> str:
        statement = self.statement_list.pop()
        print(f"{self.name} sending '{statement}'")
        return statement

    def listen(self, message: str):
        print(f"FakeUserInterface received '{message}'")


def test_run_engine():
    # Send second transition in the conversation...
    run_engine(data.basic_conversation, FakeUserPeer(["2"]))


def test_run_engine_string_interpolation():
    run_engine(data.string_interpolation_conversation, FakeUserPeer(["My name is Rowan"]))


def test_render():
    render(data.arabic_conversation_1)


def test_render_no_states():
    render_no_states(data.arabic_conversation_1)
