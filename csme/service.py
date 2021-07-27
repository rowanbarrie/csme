import logging

import networkx as nx
from pydot import Dot, Node, Edge

from csme.model import Conversation, State


def _slugify(string: str):
    return "".join(x for x in string if x.isalnum())


def render(conversation: Conversation) -> str:
    logging.info("Rendering conversation...")

    digraph = Dot()
    for state in conversation.conversation_space.states:
        digraph.add_node(Node(state.name))
    for transition in conversation.transitions:
        digraph.add_edge(Edge(transition.source.name, transition.target.name, label=transition.sentence))

    output_filepath = f"build/{_slugify(conversation.name)}.png"
    digraph.write_png(output_filepath)
    return output_filepath


def render_no_states(conversation: Conversation) -> str:
    logging.info("Rendering conversation without states...")

    graph = nx.MultiDiGraph()
    for state in conversation.conversation_space.states:
        graph.add_node(state.name)
    for transition in conversation.transitions:
        graph.add_edge(transition.source.name, transition.target.name, sentence=transition.sentence)

    # TODO: Explain "simple graph" here!
    simple_graph = nx.DiGraph(graph)
    line_graph = nx.line_graph(simple_graph)

    # Map associating Networkx line graph node -> pydot node
    node_map = {}

    digraph = Dot()

    for node in line_graph.nodes:
        # TODO: Comment all of these!
        parallel_edges = graph.subgraph([node[0], node[1]]).edges(data=True)
        concatenated_parallel_sentences = ' / '.join(list(map(lambda edge: edge[2]["sentence"], parallel_edges)))
        merged_edge_name = "{}_{}".format(node[0], node[1])
        node_map[node] = merged_edge_name
        digraph.add_node(Node(merged_edge_name, label=concatenated_parallel_sentences))

    for edge in line_graph.edges:
        digraph.add_edge(Edge(node_map[edge[0]], node_map[edge[1]]))

    output_filepath = f"build/{_slugify(conversation.name)}_no_states.png"
    digraph.write_png(output_filepath)
    return output_filepath
