from csme.service import Conversation


def test_service():
    test_conversation = Conversation('TestConversation')
    assert test_conversation.state == 'start'
    # test_conversation.talk()
    test_conversation.machine.dispatch('talk')
    assert test_conversation.state == 'end'


