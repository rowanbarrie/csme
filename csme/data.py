from typing import List

from csme.model import Conversation, State, Transition, Language, ConversationSpace

start = State("Start")
one_greeted = State("One greeted")
both_greeted = State("Both greeted")
name_asked = State("Name asked")
name_answered = State("Name answered")
one_farewelled = State("One farewelled")
end = State("End")

salam_first = Transition(source=start, target=one_greeted, sentence="Salam")
salamon_alaikom_first = Transition(source=start, target=one_greeted, sentence="Salamon Alaikom")
marhaba_first = Transition(source=start, target=one_greeted, sentence="Marhaba")
salam_second = Transition(source=one_greeted, target=both_greeted, sentence="Salam")
salamon_alaikom_second = Transition(source=one_greeted, target=both_greeted, sentence="Salamon Alaikom")
marhaba_second = Transition(source=one_greeted, target=both_greeted, sentence="Marhaba")

masmok = Transition(source=both_greeted, target=name_asked, sentence="Masmok?")
esmi = Transition(source=name_asked, target=name_answered, sentence="Esmi ____")

maasalama_first = Transition(source=name_answered, target=one_farewelled, sentence="Maasalama")
maasalama_second = Transition(source=one_farewelled, target=end, sentence="Maasalama")


arabic = Language("Arabic")
conversation_space_1 = ConversationSpace(
    name="Conversation Space 1",
    states=[
        start, one_greeted, both_greeted, name_asked, name_answered, one_farewelled, end
    ]
)

arabic_conversation_1 = Conversation(
    name="Arabic Conversation 1",
    language=arabic,
    conversation_space=conversation_space_1,
    transitions=[
        salam_first,
        salamon_alaikom_first,
        marhaba_first,
        salam_second,
        salamon_alaikom_second,
        marhaba_second,
        masmok,
        esmi,
        maasalama_first,
        maasalama_second
    ]
)
