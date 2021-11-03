import typer

from csme import service, schema
from csme.data import arabic_conversation_1
from csme.serialize import unmarshal_conversation_set
from csme.engine import Peer
from csme.model import Conversation, State

help = """
Conversational State Machine Engine.

A language learning CLI tool for visualising and traversing a conversation in multiple languages.
"""

app = typer.Typer(help=help)


class CliUserPeer(Peer):
    prompt: str = ""

    def __init__(self, name: str):
        super().__init__(name)

    def speak(self, conversation: Conversation, from_state: State) -> str:
        return typer.prompt(self.prompt)

    def listen(self, message: str):
        styled_message = typer.style(message, fg=typer.colors.BRIGHT_GREEN, bold=True)
        typer.echo(styled_message)


@app.command()
def run(conversation_json_filename: str):
    """
    Traverse the conversation interactively with the user
    """
    conversation_set_schema = schema.ConversationSetBase.parse_file(conversation_json_filename)
    conversation_set = unmarshal_conversation_set(conversation_set_schema)

    # TODO: Ask user to pick a conversation if there are multiple in the file
    conversation = conversation_set[0]

    service.run_engine(conversation, CliUserPeer("User"))


@app.command()
def render(conversation_json_filename: str):
    """
    Render the input conversation, with states, to PNG
    """
    conversation_set_schema = schema.ConversationSetBase.parse_file(conversation_json_filename)
    conversation_set = unmarshal_conversation_set(conversation_set_schema)

    for conversation in conversation_set:
        output_filepath = service.render(conversation)
        typer.echo(f"Output filepath: {output_filepath}")


@app.command()
def render_no_states(conversation_json_filename: str):
    """
    Render the input conversation, excluding states, to PNG
    """
    conversation_set_schema = schema.ConversationSetBase.parse_file(conversation_json_filename)
    conversation_set = unmarshal_conversation_set(conversation_set_schema)

    for conversation in conversation_set:
        output_filepath = service.render_no_states(conversation)
        typer.echo(f"Output filepath: {output_filepath}")


@app.command()
def example_json():
    """
    Print an example conversation set JSON object
    """
    # TODO: Introduce names and descriptions, i.e. to use names as references (snake case)

    # TODO: Generify and move this functionality into serialize.py

    # TODO: Then move data.py into tests/csme !

    # TODO: Add dot-file support - one file should constitute a ConversationSet, i.e.
    # TODO:  have top-level states (ConversationSpace) and multiple subgraphs (Conversations)

    state_names = list(map(lambda s: s.name, arabic_conversation_1.conversation_space.states))

    transitions = list(map(lambda t: schema.TransitionBase(source=t.source.name,
                                                           target=t.target.name,
                                                           statement=t.statement),
                           arabic_conversation_1.transitions))

    conversation_space = schema.ConversationSpaceBase(name=arabic_conversation_1.conversation_space.name,
                                                      states=state_names)
    conversation = schema.ConversationBase(name=arabic_conversation_1.name,
                                           language="Arabic",
                                           conversation_space=arabic_conversation_1.conversation_space.name,
                                           transitions=transitions)
    conversation_set = schema.ConversationSetBase(conversation_space=conversation_space,
                                                  conversations=[conversation])
    typer.echo(conversation_set.json())
