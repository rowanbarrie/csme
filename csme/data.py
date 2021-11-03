from typing import List

from csme.model import Conversation, State, Transition, Language, ConversationSpace

start = State("Start")
one_greeted = State("One greeted")
both_greeted = State("Both greeted")
name_asked = State("Name asked")
name_answered = State("Name answered")
one_farewelled = State("One farewelled")
end = State("End")

salam_first = Transition(source=start, target=one_greeted, statement="Salam")
salamon_alaikom_first = Transition(source=start, target=one_greeted, statement="Salamon Alaikom")
marhaba_first = Transition(source=start, target=one_greeted, statement="Marhaba")
salam_second = Transition(source=one_greeted, target=both_greeted, statement="Salam")
salamon_alaikom_second = Transition(source=one_greeted, target=both_greeted, statement="Salamon Alaikom")
marhaba_second = Transition(source=one_greeted, target=both_greeted, statement="Marhaba")

masmok = Transition(source=both_greeted, target=name_asked, statement="Masmok?")
esmi = Transition(source=name_asked, target=name_answered, statement="Esmi {name}")

maasalama_first = Transition(source=name_answered, target=one_farewelled, statement="Maasalama")
maasalama_second = Transition(source=one_farewelled, target=end, statement="Maasalama")


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

a = State("A")
b = State("B")
c = State("C")

english = Language("English")
basic_conversation_space = ConversationSpace(
    name="Basic conversation space",
    states=[a, b, c]
)
basic_conversation = Conversation(
    name="Basic conversation",
    language=english,
    conversation_space=basic_conversation_space,
    transitions=[Transition(source=a, target=b, statement="1"),
                 Transition(source=b, target=c, statement="2")]
)

d = State("D")
e = State("E")
f = State("F")

english = Language("English")
string_interpolation_space = ConversationSpace(
    name="String interpolation space",
    states=[d, e, f]
)

string_interpolation_conversation = Conversation(
    name="String interpolation conversation",
    language=english,
    conversation_space=string_interpolation_space,
    transitions=[Transition(source=d, target=e, statement="What is your name?"),
                 Transition(source=e, target=f, statement="My name is {name}")]
)
