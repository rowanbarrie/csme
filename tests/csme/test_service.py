from csme import data
from csme.service import render, render_no_states


def test_render():
    render(data.arabic_conversation_1)


def test_render_no_states():
    render_no_states(data.arabic_conversation_1)
