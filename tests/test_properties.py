import networkxr as nx
from hypothesis import given
import hypothesis.strategies as st


# Strategies to generate complex but valid graph nodes
node_strategy = st.one_of(
    st.integers(),
    st.text(min_size=1, max_size=10),
)


@given(st.lists(node_strategy, unique=True, max_size=100))
def test_property_add_nodes(nodes):
    """
    Property: Adding a node means `has_node` is True and it appears in `G.nodes`.
    """
    G = nx.Graph()
    for n in nodes:
        G.add_node(n)

    # Invariants
    assert len(G) == len(nodes)
    for n in nodes:
        assert G.has_node(n)
        assert n in G
        assert n in G.nodes

    # The list of nodes should exactly match the inserted unique nodes (order might differ)
    assert set(G.nodes) == set(nodes)


@given(st.lists(node_strategy, unique=True, min_size=1, max_size=50))
def test_property_remove_nodes(nodes):
    """
    Property: Removing a node means `has_node` is False and its edges disappear.
    """
    G = nx.Graph()
    G.add_nodes_from(nodes)

    # Add a central hub node connected to everyone
    hub = "HUB_NODE"
    edge_list = [(hub, n) for n in nodes]
    G.add_edges_from(edge_list)

    assert G.number_of_edges() == len(nodes)

    # Remove half the nodes
    to_remove = nodes[: len(nodes) // 2]
    G.remove_nodes_from(to_remove)

    # Invariants
    # Use sets to determine correct remaining counts, since 'hub' might already be in nodes
    hub = "HUB_NODE"
    remaining_nodes = (set(nodes) - set(to_remove)) | {hub}

    assert len(G) == len(remaining_nodes)
    for n in remaining_nodes:
        if n != hub:
            assert G.has_node(n)
            assert G.has_edge(hub, n)
        if n != hub:
            assert G.has_edge(hub, n)

    assert G.number_of_edges() == len(nodes) - len(to_remove)


@given(st.lists(st.tuples(node_strategy, node_strategy), max_size=100))
def test_property_add_edges_undirected(edges):
    """
    Property: Adding undirected (u, v) implies has_edge(u, v) and has_edge(v, u).
    """
    G = nx.Graph()
    G.add_edges_from(edges)

    # Invariants
    for u, v in edges:
        assert G.has_node(u)
        assert G.has_node(v)
        assert G.has_edge(u, v)
        assert G.has_edge(v, u)

    # Edge count should be <= len(edges) because of duplicates or (u,v)/(v,u) pairs
    assert G.number_of_edges() <= len(edges)


@given(st.lists(st.tuples(node_strategy, node_strategy), max_size=100))
def test_property_add_edges_directed(edges):
    """
    Property: Adding directed (u, v) implies has_edge(u, v). (v,u) is NOT implied.
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Invariants
    for u, v in edges:
        assert G.has_node(u)
        assert G.has_node(v)
        assert G.has_edge(u, v)

    # We know that for each unique pair (u, v) in edges, the edge exists.
    # However, if u and v are tuples (v1, v2) they can be misparsed if len is 2/3
    # G.number_of_edges() will <= len(edges)
    assert G.number_of_edges() <= len(set(edges))


@given(st.lists(node_strategy, unique=True, max_size=100))
def test_property_clear_graph(nodes):
    """
    Property: Clearing a graph leaves 0 nodes and 0 edges.
    """
    G = nx.Graph()
    G.add_nodes_from(nodes)
    if len(nodes) > 1:
        G.add_edges_from(zip(nodes[:-1], nodes[1:]))

    assert len(G) == len(set(nodes))

    G.clear()

    assert len(G) == 0
    assert G.number_of_edges() == 0
    assert list(G.nodes) == []
    assert list(G.edges) == []


@given(st.lists(st.tuples(st.integers(), st.integers()), max_size=30))
def test_property_dict_conversion(edges):
    """
    Property: G -> dict -> G returns an identical graph.
    """
    # Test Undirected
    G1 = nx.Graph()
    G1.add_edges_from(edges)
    d1 = nx.to_dict_of_dicts(G1)
    G1_rebuilt = nx.from_dict_of_dicts(d1, create_using=nx.Graph)

    assert nx.is_isomorphic(G1, G1_rebuilt)
    assert set(G1.nodes) == set(G1_rebuilt.nodes)
    assert G1.number_of_edges() == G1_rebuilt.number_of_edges()

    # Test Directed
    G2 = nx.DiGraph()
    G2.add_edges_from(edges)
    d2 = nx.to_dict_of_dicts(G2)
    G2_rebuilt = nx.from_dict_of_dicts(d2, create_using=nx.DiGraph)

    assert nx.is_isomorphic(G2, G2_rebuilt)
    assert set(G2.nodes) == set(G2_rebuilt.nodes)
    assert G2.number_of_edges() == G2_rebuilt.number_of_edges()
