from csme import data
from csme.engine import UserInterface
from csme.service import render, render_no_states, run_engine


class FakeUserInterface(UserInterface):
    def receive(self) -> str:
        # Send second transition in the test conversation...
        message = "2"
        print(f"FakeUserInterface sending '{message}'")
        return message

    def send(self, message: str):
        print(f"FakeUserInterface received '{message}'")


def test_run_engine():
    run_engine(data.test_conversation_1, FakeUserInterface())


def test_render():
    render(data.arabic_conversation_1)


def test_render_no_states():
    render_no_states(data.arabic_conversation_1)
