import logging

import networkx as nx
from pydot import Dot, Node, Edge

from config import settings
from csme.engine import ConversationEngine, SimpleComputerPeer, Peer
from csme.model import Conversation


def run_engine(conversation: Conversation, user_peer: Peer):
    logging.info("Running CSME service...")
    # TODO: Configure a pipeline of filters and print out all them instead of relying on (brittle) settings object!
    logging.info("case_ignore_filter_enabled: %s", settings.case_ignore_filter_enabled)

    engine = ConversationEngine(conversation=conversation,
                                peer_a=SimpleComputerPeer(name="Computer"),
                                peer_b=user_peer)
    engine.run()


def _slugify(string: str) -> str:
    return "".join(x for x in string if x.isalnum())


def render(conversation: Conversation) -> str:
    """
    Generates the conversation state diagram.

    :param conversation: The conversation to generate
    :return: Output filename
    """
    logging.info("Rendering conversation...")

    output_filepath = f"build/{_slugify(conversation.name)}.png"
    conversation.as_dot_digraph().write_png(output_filepath)
    return output_filepath


def render_no_states(conversation: Conversation) -> str:
    """
    Generates the conversation state diagram without any states.

    In more technical terms converts the conversation graph first into a 'simple graph', from which a 'line graph' is
    then generated. This yields a graph connecting all of the statements that can be made in the conversation, but with
    parallel statements (e.g. "Hello", "Hi") missing.

    The parallel statements are then recovered and merged by iterating over each edge in the generated line graph.

    Simple graph: https://en.wikipedia.org/wiki/Directed_graph#Types_of_directed_graphs
    Line graph: https://en.wikipedia.org/wiki/Line_graph

    :param conversation: The conversation to generate
    :return: Output filename
    """
    logging.info("Rendering conversation without states...")

    simple_graph = nx.DiGraph(conversation.get_graph())
    line_graph = nx.line_graph(simple_graph)

    # Map associating Networkx line graph node -> pydot node
    node_map = {}

    digraph = Dot()

    logging.info(f"Conversation={conversation}")
    for node in line_graph.nodes:
        parallel_edges = conversation.get_graph().subgraph([node[0], node[1]]).edges(data=True)
        concatenated_parallel_statements = ' / '.join(list(map(lambda edge: edge[2]["statement"], parallel_edges)))
        merged_edge_name = "{}_{}".format(node[0], node[1])
        node_map[node] = merged_edge_name
        digraph.add_node(Node(merged_edge_name, label=concatenated_parallel_statements))

    for edge in line_graph.edges:
        digraph.add_edge(Edge(node_map[edge[0]], node_map[edge[1]]))

    output_filepath = f"build/{_slugify(conversation.name)}_no_states.png"
    digraph.write_png(output_filepath)
    return output_filepath
