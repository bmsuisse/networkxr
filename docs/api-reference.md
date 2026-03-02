# API Reference

Auto-generated from the live `networkxr` package. All signatures, type hints, and docstrings are extracted at build time.

## Core Graph Types

### `class Graph`

Undirected graph with self-loops but no parallel edges.

#### `Graph.adj` *(property)*

#### `Graph.degree` *(property)*

#### `Graph.edges` *(property)*

#### `Graph.name` *(property)*

#### `Graph.nodes` *(property)*

#### `Graph.__init__(self, incoming_graph_data: 'Any' = None, **attr: 'Any') -> 'None'`

Initialize self.  See help(type(self)) for accurate signature.

#### `Graph.add_edge(self, u_of_edge: 'Any', v_of_edge: 'Any', **attr: 'Any') -> 'None'`

#### `Graph.add_edges_from(self, ebunch: 'Any', **attr: 'Any') -> 'None'`

#### `Graph.add_node(self, node_for_adding: 'Any', **attr: 'Any') -> 'None'`

#### `Graph.add_nodes_from(self, nodes: 'Any', **attr: 'Any') -> 'None'`

#### `Graph.add_weighted_edges_from(self, ebunch: 'Any', weight: 'str' = 'weight') -> 'None'`

#### `Graph.adjacency(self) -> 'Any'`

#### `Graph.clear(self) -> 'None'`

#### `Graph.clear_edges(self) -> 'None'`

#### `Graph.copy(self) -> 'Graph'`

#### `Graph.get_edge_data(self, u: 'Any', v: 'Any', default: 'Any' = None) -> 'Any'`

#### `Graph.has_edge(self, u: 'Any', v: 'Any') -> 'bool'`

#### `Graph.has_node(self, n: 'Any') -> 'bool'`

#### `Graph.is_directed(self) -> 'bool'`

#### `Graph.is_multigraph(self) -> 'bool'`

#### `Graph.neighbors(self, n: 'Any') -> 'Any'`

#### `Graph.number_of_edges(self) -> 'int'`

#### `Graph.number_of_nodes(self) -> 'int'`

#### `Graph.order(self) -> 'int'`

#### `Graph.remove_edge(self, u: 'Any', v: 'Any') -> 'None'`

#### `Graph.remove_node(self, n: 'Any') -> 'None'`

#### `Graph.remove_nodes_from(self, nodes: 'Any') -> 'None'`

#### `Graph.size(self, weight: 'str | None' = None) -> 'Any'`

#### `Graph.subgraph(self, nodes: 'Any') -> 'Graph'`

#### `Graph.to_undirected(self) -> 'Graph'`

### `class DiGraph`

Directed graph with self-loops but no parallel edges.

#### `DiGraph.adj` *(property)*

#### `DiGraph.degree` *(property)*

#### `DiGraph.edges` *(property)*

#### `DiGraph.name` *(property)*

#### `DiGraph.nodes` *(property)*

#### `DiGraph.__init__(self, incoming_graph_data: 'Any' = None, **attr: 'Any') -> 'None'`

Initialize self.  See help(type(self)) for accurate signature.

#### `DiGraph.add_edge(self, u_of_edge: 'Any', v_of_edge: 'Any', **attr: 'Any') -> 'None'`

#### `DiGraph.add_edges_from(self, ebunch_to_add: 'Any', **attr: 'Any') -> 'None'`

#### `DiGraph.add_node(self, node_for_adding: 'Any', **attr: 'Any') -> 'None'`

#### `DiGraph.add_nodes_from(self, nodes: 'Any', **attr: 'Any') -> 'None'`

#### `DiGraph.add_weighted_edges_from(self, ebunch: 'Any', weight: 'str' = 'weight') -> 'None'`

#### `DiGraph.adjacency(self) -> 'Any'`

#### `DiGraph.clear(self) -> 'None'`

#### `DiGraph.clear_edges(self) -> 'None'`

#### `DiGraph.copy(self) -> 'DiGraph'`

#### `DiGraph.get_edge_data(self, u: 'Any', v: 'Any', default: 'Any' = None) -> 'Any'`

#### `DiGraph.has_edge(self, u: 'Any', v: 'Any') -> 'bool'`

#### `DiGraph.has_node(self, n: 'Any') -> 'bool'`

#### `DiGraph.in_degree(self, nbunch: 'Any' = None) -> 'Any'`

#### `DiGraph.is_directed(self) -> 'bool'`

#### `DiGraph.is_multigraph(self) -> 'bool'`

#### `DiGraph.neighbors(self, n: 'Any') -> 'Any'`

#### `DiGraph.number_of_edges(self) -> 'int'`

#### `DiGraph.number_of_nodes(self) -> 'int'`

#### `DiGraph.order(self) -> 'int'`

#### `DiGraph.out_degree(self, nbunch: 'Any' = None) -> 'Any'`

#### `DiGraph.predecessors(self, n: 'Any') -> 'Any'`

#### `DiGraph.remove_edge(self, u: 'Any', v: 'Any') -> 'None'`

#### `DiGraph.remove_node(self, n: 'Any') -> 'None'`

#### `DiGraph.remove_nodes_from(self, nodes: 'Any') -> 'None'`

#### `DiGraph.reverse(self, copy: 'bool' = True) -> 'DiGraph'`

#### `DiGraph.size(self, weight: 'str | None' = None) -> 'Any'`

#### `DiGraph.subgraph(self, nodes: 'Any') -> 'DiGraph'`

#### `DiGraph.successors(self, n: 'Any') -> 'Any'`

#### `DiGraph.to_undirected(self) -> 'Graph'`

### `class MultiGraph`

Undirected multigraph allowing parallel edges.

#### `MultiGraph.adj` *(property)*

#### `MultiGraph.edges` *(property)*

#### `MultiGraph.name` *(property)*

#### `MultiGraph.nodes` *(property)*

#### `MultiGraph.__init__(self, incoming_graph_data: 'Any' = None, **attr: 'Any') -> 'None'`

Initialize self.  See help(type(self)) for accurate signature.

#### `MultiGraph.add_edge(self, u: 'Any', v: 'Any', key: 'Any' = None, **attr: 'Any') -> 'Any'`

#### `MultiGraph.add_edges_from(self, ebunch: 'Any', **attr: 'Any') -> 'None'`

#### `MultiGraph.add_node(self, n: 'Any', **attr: 'Any') -> 'None'`

#### `MultiGraph.add_nodes_from(self, nodes: 'Any', **attr: 'Any') -> 'None'`

#### `MultiGraph.add_weighted_edges_from(self, ebunch: 'Any', weight: 'str' = 'weight') -> 'None'`

#### `MultiGraph.clear(self) -> 'None'`

#### `MultiGraph.copy(self) -> 'MultiGraph'`

#### `MultiGraph.degree(self, nbunch: 'Any' = None) -> 'Any'`

#### `MultiGraph.get_edge_data(self, u: 'Any', v: 'Any', key: 'Any' = None, default: 'Any' = None) -> 'Any'`

#### `MultiGraph.has_edge(self, u: 'Any', v: 'Any', key: 'Any' = None) -> 'bool'`

#### `MultiGraph.has_node(self, n: 'Any') -> 'bool'`

#### `MultiGraph.is_directed(self) -> 'bool'`

#### `MultiGraph.is_multigraph(self) -> 'bool'`

#### `MultiGraph.neighbors(self, n: 'Any') -> 'list[Any]'`

#### `MultiGraph.number_of_edges(self) -> 'int'`

#### `MultiGraph.number_of_nodes(self) -> 'int'`

#### `MultiGraph.remove_edge(self, u: 'Any', v: 'Any', key: 'Any' = None) -> 'None'`

#### `MultiGraph.remove_node(self, n: 'Any') -> 'None'`

#### `MultiGraph.subgraph(self, nodes: 'Any') -> 'MultiGraph'`

#### `MultiGraph.to_undirected(self) -> 'MultiGraph'`

### `class MultiDiGraph`

Directed multigraph allowing parallel edges.

#### `MultiDiGraph.adj` *(property)*

#### `MultiDiGraph.edges` *(property)*

#### `MultiDiGraph.name` *(property)*

#### `MultiDiGraph.nodes` *(property)*

#### `MultiDiGraph.__init__(self, incoming_graph_data: 'Any' = None, **attr: 'Any') -> 'None'`

Initialize self.  See help(type(self)) for accurate signature.

#### `MultiDiGraph.add_edge(self, u: 'Any', v: 'Any', key: 'Any' = None, **attr: 'Any') -> 'Any'`

#### `MultiDiGraph.add_edges_from(self, ebunch: 'Any', **attr: 'Any') -> 'None'`

#### `MultiDiGraph.add_node(self, n: 'Any', **attr: 'Any') -> 'None'`

#### `MultiDiGraph.add_nodes_from(self, nodes: 'Any', **attr: 'Any') -> 'None'`

#### `MultiDiGraph.add_weighted_edges_from(self, ebunch: 'Any', weight: 'str' = 'weight') -> 'None'`

#### `MultiDiGraph.clear(self) -> 'None'`

#### `MultiDiGraph.copy(self) -> 'MultiDiGraph'`

#### `MultiDiGraph.degree(self, nbunch: 'Any' = None) -> 'Any'`

#### `MultiDiGraph.get_edge_data(self, u: 'Any', v: 'Any', key: 'Any' = None, default: 'Any' = None) -> 'Any'`

#### `MultiDiGraph.has_edge(self, u: 'Any', v: 'Any', key: 'Any' = None) -> 'bool'`

#### `MultiDiGraph.has_node(self, n: 'Any') -> 'bool'`

#### `MultiDiGraph.in_degree(self, nbunch: 'Any' = None) -> 'Any'`

#### `MultiDiGraph.is_directed(self) -> 'bool'`

#### `MultiDiGraph.is_multigraph(self) -> 'bool'`

#### `MultiDiGraph.neighbors(self, n: 'Any') -> 'list[Any]'`

#### `MultiDiGraph.number_of_edges(self) -> 'int'`

#### `MultiDiGraph.number_of_nodes(self) -> 'int'`

#### `MultiDiGraph.out_degree(self, nbunch: 'Any' = None) -> 'Any'`

#### `MultiDiGraph.predecessors(self, n: 'Any') -> 'list[Any]'`

#### `MultiDiGraph.remove_edge(self, u: 'Any', v: 'Any', key: 'Any' = None) -> 'None'`

#### `MultiDiGraph.remove_node(self, n: 'Any') -> 'None'`

#### `MultiDiGraph.reverse(self, copy: 'bool' = True) -> 'MultiDiGraph'`

#### `MultiDiGraph.successors(self, n: 'Any') -> 'list[Any]'`

#### `MultiDiGraph.to_undirected(self) -> 'MultiGraph'`

## Graph Generators

### `complete_graph(n: 'int', create_using: 'Any' = None) -> 'Any'`

Return the complete graph K_n.

### `cycle_graph(n: 'int', create_using: 'Any' = None) -> 'Any'`

Return the cycle graph C_n of n cyclically connected nodes.

### `path_graph(n: 'int', create_using: 'Any' = None) -> 'Any'`

Return the path graph P_n of n nodes linearly connected.

### `star_graph(n: 'int', create_using: 'Any' = None) -> 'Any'`

Return the star graph with n+1 nodes: center 0 connected to 1..n.

### `barbell_graph(m1: 'int', m2: 'int', create_using: 'Any' = None) -> 'Any'`

Return the barbell graph: two complete graphs connected by a path.

### `empty_graph(n: 'int' = 0, create_using: 'Any' = None) -> 'Any'`

Return the empty graph with n nodes and zero edges.

## Conversion Functions

### `to_dict_of_dicts(G: 'Any', nodelist: 'list[Any] | None' = None, edge_data: 'Any' = None) -> 'dict[Any, dict[Any, Any]]'`

Return adjacency representation of graph as a dict of dicts.

### `from_dict_of_dicts(d: 'dict[Any, dict[Any, Any]]', create_using: 'Any' = None, multigraph_input: 'bool' = False) -> 'Any'`

Return a graph from a dict of dicts.

### `to_dict_of_lists(G: 'Any', nodelist: 'list[Any] | None' = None) -> 'dict[Any, list[Any]]'`

Return adjacency representation of graph as a dict of lists.

### `from_dict_of_lists(d: 'dict[Any, list[Any]]', create_using: 'Any' = None) -> 'Any'`

Return a graph from a dict of lists.

### `to_edgelist(G: 'Any', nodelist: 'list[Any] | None' = None) -> 'list[tuple[Any, ...]]'`

Return a list of edges in the graph.

### `to_networkx_graph(data: 'Any', create_using: 'Any' = None, multigraph_input: 'bool' = False) -> 'Any'`

Convert various data formats to a NetworkX graph.

## Relabeling

### `relabel_nodes(G: 'Any', mapping: 'Mapping[Any, Any] | Callable[[Any], Any]', copy: 'bool' = True) -> 'Any'`

Relabel the nodes of the graph G.

### `convert_node_labels_to_integers(G: 'Any', first_label: 'int' = 0, ordering: 'str' = 'default', label_attribute: 'str | None' = None) -> 'Any'`

Return a copy of G with node labels replaced by integers.

## Isomorphism

### `is_isomorphic(G1: 'Any', G2: 'Any') -> 'bool'`

Check if two graphs are isomorphic.

Uses a simple degree-sequence + VF2-like backtracking approach
for small graphs. This is not as sophisticated as NetworkX's full
VF2 implementation but works correctly for the test cases.

## Exceptions

networkXR provides the full NetworkX exception hierarchy for compatibility.

### `class NetworkXException`

Base class for exceptions in NetworkX.

### `class NetworkXError`

Exception for a serious error in NetworkX.

### `class NetworkXAlgorithmError`

Exception for unexpected termination of algorithms.

### `class NetworkXNoPath`

Exception for algorithms that should return a path when running
on graphs where such a path does not exist.

### `class NetworkXNoCycle`

Exception for algorithms that should return a cycle when running
on graphs where such a cycle does not exist.

### `class NetworkXUnfeasible`

Exception raised by algorithms trying to solve a problem
instance that has no feasible solution.

### `class NetworkXUnbounded`

Exception raised by algorithms trying to solve a maximization
or minimization problem instance that is unbounded.

### `class NetworkXPointlessConcept`

Raised when a null graph is drawn w/o a layout algorithm.

### `class NodeNotFound`

Exception raised if requested node is not present in the graph.

### `class HasACycle`

Raised if a graph has a cycle when an algorithm expects it not to.

### `class AmbiguousSolution`

Raised if more than one valid solution exists for an intermediary step
of an algorithm.

### `class ExceededMaxIterations`

Raised if a loop exceeds the maximum number of iterations.

### `class PowerIterationFailedConvergence`

Raised when power iteration fails to converge within max iterations.

#### `PowerIterationFailedConvergence.__init__(self, num_iterations: int, *args: object) -> None`

Initialize self.  See help(type(self)) for accurate signature.

## Utilities

### `nodes_equal(nodes1: 'Any', nodes2: 'Any') -> 'bool'`

Check if two node sequences are equal (unordered).

### `edges_equal(edges1: 'Any', edges2: 'Any', *, directed: 'bool' = False) -> 'bool'`

Check if two edge sequences are equal (unordered).

For undirected graphs, (u,v) == (v,u).

### `graphs_equal(g1: 'Any', g2: 'Any') -> 'bool'`

Check if two graphs are structurally equal.

### `flatten(obj: 'Any', result: 'list[Any] | None' = None) -> 'Any'`

Return flattened version of (possibly nested) iterable.

### `pairwise(iterable: 'Any') -> 'Any'`

s -> (s0,s1), (s1,s2), (s2, s3), ...

