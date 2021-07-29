import logging

import networkx as nx
from pydot import Dot, Node, Edge

from csme.engine import ConversationEngine, SimpleComputerSpeaker, SimpleUserSpeaker, UserInterface
from csme.model import Conversation


def run_engine(conversation: Conversation, user_interface: UserInterface):
    logging.info("Running CSME service...")

    # TODO: Use configuration for args here!
    engine = ConversationEngine(conversation,
                                SimpleComputerSpeaker(),
                                SimpleUserSpeaker(user_interface))
    engine.run()


def _slugify(string: str) -> str:
    return "".join(x for x in string if x.isalnum())


def render(conversation: Conversation) -> str:
    logging.info("Rendering conversation...")

    output_filepath = f"build/{_slugify(conversation.name)}.png"
    conversation.as_dot_digraph().write_png(output_filepath)
    return output_filepath


# FIXME: Not working at the moment!
def render_no_states(conversation: Conversation) -> str:
    logging.info("Rendering conversation without states...")

    # TODO: Explain "simple graph" here!
    simple_graph = nx.DiGraph(conversation.get_graph())
    line_graph = nx.line_graph(simple_graph)

    # Map associating Networkx line graph node -> pydot node
    node_map = {}

    digraph = Dot()

    logging.info(f"Conversation={conversation}")
    for node in line_graph.nodes:
        logging.info(f"node={node}")
        # TODO: Comment all of these!
        parallel_edges = conversation.get_graph().subgraph([node[0], node[1]]).edges(data=True)
        concatenated_parallel_sentences = ' / '.join(list(map(lambda edge: edge[2]["sentence"], parallel_edges)))
        merged_edge_name = "{}_{}".format(node[0], node[1])
        node_map[node] = merged_edge_name
        digraph.add_node(Node(merged_edge_name, label=concatenated_parallel_sentences))

    for edge in line_graph.edges:
        digraph.add_edge(Edge(node_map[edge[0]], node_map[edge[1]]))

    output_filepath = f"build/{_slugify(conversation.name)}_no_states.png"
    digraph.write_png(output_filepath)
    return output_filepath
