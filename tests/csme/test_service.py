from csme import data
from csme.engine import Peer
from csme.service import render, render_no_states, run_engine
from csme.model import Conversation, State


class FakeUserPeer(Peer):
    def speak(self, conversation: Conversation, from_state: State) -> str:
        # Send second transition in the test conversation...
        message = "2"
        print(f"FakeUserInterface sending '{message}'")
        return message

    def listen(self, message: str):
        print(f"FakeUserInterface received '{message}'")


def test_run_engine():
    run_engine(data.test_conversation_1, FakeUserPeer("fakeUser"))


def test_render():
    render(data.arabic_conversation_1)


def test_render_no_states():
    render_no_states(data.arabic_conversation_1)
