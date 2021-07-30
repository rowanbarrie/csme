from typing import List


# Could combine/replace this with pycountry language
import pydot
from networkx import MultiDiGraph
# from pydot import Dot, Node, Edge


class Language:
    def __init__(self, name: str):
        self.name = name


# class State(Node):
class State:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"State({self.name})"


class Transition:
    def __init__(self, source: State, target: State, statement: str):
        self.source = source
        self.target = target
        self.statement = statement

    def __repr__(self):
        return f"Transition({self.source}, {self.target}, {self.statement})"


class ConversationSpace:
    def __init__(self, name: str, states: List[State]):
        self.name = name
        self.states = states

    def __repr__(self):
        return f"ConversationSpace({self.name}, {self.states})"


class Conversation:

    def __init__(self, name: str, language: Language, conversation_space: ConversationSpace, transitions: List[Transition]):
        super(Conversation, self).__init__()
        self.name = name
        self.language = language
        self.conversation_space = conversation_space
        self.transitions = transitions

        self.graph = MultiDiGraph()
        for state in self.conversation_space.states:
            self.graph.add_node(state.name)
        for transition in self.transitions:
            self.graph.add_edge(transition.source.name, transition.target.name, statement=transition.statement)

    def get_graph(self) -> MultiDiGraph:
        return self.graph

    def get_state(self, state_name: str) -> State:
        return next(filter(lambda s: s.name == state_name, self.conversation_space.states))

    # TODO: Could just track the start state ourselves...
    def get_start_state(self) -> State:
        state_name = [n for n, d in self.graph.in_degree if d == 0][0]
        return self.get_state(state_name)

    def get_transition(self, from_state: State, statement: str) -> Transition:
        return next(filter(lambda t: t.source == from_state and t.statement == statement, self.transitions))

    def get_out_transitions(self, from_state: State) -> List[Transition]:
        nx_edges = self.graph.edges(from_state.name, data=True)
        statements = list(map(lambda nx_edge: nx_edge[2]["statement"], list(nx_edges)))
        transitions = list(map(lambda s: self.get_transition(from_state=from_state, statement=s), statements))
        return transitions

    def as_dot_digraph(self) -> pydot.Dot:
        graph = pydot.Dot()
        for state in self.conversation_space.states:
            graph.add_node(pydot.Node(state.name))
        for transition in self.transitions:
            graph.add_edge(pydot.Edge(transition.source.name, transition.target.name, label=transition.statement))
        return graph

    def __repr__(self):
        return f"Conversation({self.conversation_space}, {self.transitions})"
