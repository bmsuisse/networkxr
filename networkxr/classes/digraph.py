"""Pure Python DiGraph — directed, single-edge, NetworkX-compatible API.

Optimised with __slots__, EAFP hot paths, and shared edge dicts.
"""

from __future__ import annotations

from typing import Any

from networkxr.classes.graph import Graph
from networkxr.classes.views import DegreeView, DiEdgeView, NodeView


class DiGraph(Graph):
    """Directed graph with self-loops but no parallel edges."""

    __slots__ = ("_pred",)

    def __init__(self, incoming_graph_data: Any = None, **attr: Any) -> None:
        self.graph: dict[str, Any] = {}
        self.graph.update(attr)
        self._node: dict[Any, dict[str, Any]] = {}
        self._adj: dict[Any, dict[Any, dict[str, Any]]] = {}
        self._pred: dict[Any, dict[Any, dict[str, Any]]] = {}
        if incoming_graph_data is not None:
            self._ingest(incoming_graph_data)

    # ── internal ────────────────────────────────────────────────

    def _ingest(self, data: Any) -> None:
        if isinstance(data, (DiGraph, Graph)):
            for n, dd in data.nodes(data=True):
                self.add_node(n, **dd)
            for u, v, dd in data.edges(data=True):
                self.add_edge(u, v, **dd)
            self.graph.update(data.graph)
        elif isinstance(data, dict):
            first_val = next(iter(data.values()), None)
            if isinstance(first_val, dict):
                for u, nbrs in data.items():
                    self.add_node(u)
                    for v, edata in nbrs.items():
                        self.add_node(v)
                        if isinstance(edata, dict):
                            self.add_edge(u, v, **edata)
                        else:
                            self.add_edge(u, v)
            elif isinstance(first_val, list):
                for u, nbrs in data.items():
                    self.add_node(u)
                    for v in nbrs:
                        self.add_edge(u, v)
        elif hasattr(data, "__iter__"):
            for item in data:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    u, v = item[0], item[1]
                    dd = item[2] if len(item) >= 3 and isinstance(item[2], dict) else {}
                    self.add_edge(u, v, **dd)

    # ── node ops (EAFP) ────────────────────────────────────────

    def add_node(self, node_for_adding: Any, **attr: Any) -> None:
        _node = self._node
        try:
            _node[node_for_adding].update(attr)
        except KeyError:
            _node[node_for_adding] = attr.copy() if attr else {}
            self._adj[node_for_adding] = {}
            self._pred[node_for_adding] = {}

    def remove_node(self, n: Any) -> None:
        _adj = self._adj
        _pred = self._pred
        try:
            succs = _adj[n]
        except KeyError:
            msg = f"The node {n} is not in the graph."
            raise KeyError(msg) from None
        for succ in succs:
            _pred[succ].pop(n, None)
        for pred in list(_pred[n]):
            _adj[pred].pop(n, None)
        del _adj[n]
        del _pred[n]
        del self._node[n]

    def remove_nodes_from(self, nodes: Any) -> None:
        _adj = self._adj
        _pred = self._pred
        for n in nodes:
            try:
                succs = _adj[n]
            except KeyError:
                continue
            for succ in succs:
                _pred[succ].pop(n, None)
            for pred in list(_pred[n]):
                _adj[pred].pop(n, None)
            del _adj[n]
            del _pred[n]
            del self._node[n]

    # ── edge ops (EAFP hot path) ────────────────────────────────

    def add_edge(self, u_of_edge: Any, v_of_edge: Any, **attr: Any) -> None:
        u, v = u_of_edge, v_of_edge
        _node = self._node
        _adj = self._adj
        _pred = self._pred
        if u not in _node:
            _node[u] = {}
            _adj[u] = {}
            _pred[u] = {}
        if v not in _node:
            _node[v] = {}
            _adj[v] = {}
            _pred[v] = {}
        adj_u = _adj[u]
        try:
            adj_u[v].update(attr)
        except KeyError:
            dd = dict(attr)
            adj_u[v] = dd
            _pred[v][u] = dd

    def add_edges_from(self, ebunch_to_add: Any, **attr: Any) -> None:
        _node = self._node
        _adj = self._adj
        _pred = self._pred
        for e in ebunch_to_add:
            ne = len(e)
            if ne == 3:
                u, v, dd = e
                # Update attributes with kwargs overrides
                dd = dict(dd)
                dd.update(attr)
            elif ne == 2:
                u, v = e
                dd = dict(attr)
            else:
                msg = f"Edge tuple {e} must be a 2-tuple or 3-tuple."
                raise ValueError(msg)
            
            if u not in _node:
                _node[u] = {}
                _adj[u] = {}
                _pred[u] = {}
            if v not in _node:
                _node[v] = {}
                _adj[v] = {}
                _pred[v] = {}
            adj_u = _adj[u]
            try:
                adj_u[v].update(dd)
            except KeyError:
                dd_copy = dd.copy()
                adj_u[v] = dd_copy
                _pred[v][u] = dd_copy


    def remove_edge(self, u: Any, v: Any) -> None:
        try:
            del self._adj[u][v]
            del self._pred[v][u]
        except KeyError:
            msg = f"Edge {u}-{v} is not in the graph."
            raise KeyError(msg) from None

    # ── queries ─────────────────────────────────────────────────

    def has_edge(self, u: Any, v: Any) -> bool:
        try:
            return v in self._adj[u]
        except KeyError:
            return False

    def successors(self, n: Any) -> Any:
        try:
            return iter(self._adj[n])
        except KeyError:
            msg = f"The node {n} is not in the graph."
            raise KeyError(msg) from None

    def predecessors(self, n: Any) -> Any:
        try:
            return iter(self._pred[n])
        except KeyError:
            msg = f"The node {n} is not in the graph."
            raise KeyError(msg) from None

    def neighbors(self, n: Any) -> Any:
        return self.successors(n)

    # ── views ───────────────────────────────────────────────────

    @property
    def nodes(self) -> NodeView:
        return NodeView(self)

    @property
    def edges(self) -> DiEdgeView:
        return DiEdgeView(self)

    @property
    def degree(self) -> DegreeView:  # type: ignore[override]
        return DegreeView(self)

    def in_degree(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                return len(self._pred[nbunch])
            msg = f"The node {nbunch} is not in the graph."
            raise KeyError(msg)
        return [(n, len(self._pred[n])) for n in self._node]

    def out_degree(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                return len(self._adj[nbunch])
            msg = f"The node {nbunch} is not in the graph."
            raise KeyError(msg)
        return [(n, len(self._adj[n])) for n in self._node]

    # ── info ────────────────────────────────────────────────────

    def number_of_edges(self) -> int:
        return sum(len(nbrs) for nbrs in self._adj.values())

    def is_directed(self) -> bool:
        return True

    def copy(self) -> DiGraph:
        G = self.__class__()
        G.graph.update(self.graph)
        g_node = G._node
        g_adj = G._adj
        g_pred = G._pred
        for n, dd in self._node.items():
            g_node[n] = dd.copy()
            g_adj[n] = {}
            g_pred[n] = {}
        for u, nbrs in self._adj.items():
            for v, dd in nbrs.items():
                new_dd = dd.copy()
                g_adj[u][v] = new_dd
                g_pred[v][u] = new_dd
        return G

    def clear(self) -> None:
        self._node.clear()
        self._adj.clear()
        self._pred.clear()
        self.graph.clear()

    def clear_edges(self) -> None:
        for nbrs in self._adj.values():
            nbrs.clear()
        for nbrs in self._pred.values():
            nbrs.clear()

    def reverse(self, copy: bool = True) -> DiGraph:
        G = self.__class__()
        G.graph.update(self.graph)
        for n, dd in self._node.items():
            G.add_node(n, **dd)
        for u, nbrs in self._adj.items():
            for v, dd in nbrs.items():
                G.add_edge(v, u, **dd)
        if not copy:
            self._adj, self._pred = self._pred, self._adj
            return self
        return G

    def to_undirected(self) -> Graph:
        G = Graph()
        G.graph.update(self.graph)
        for n, dd in self._node.items():
            G.add_node(n, **dd)
        for u, nbrs in self._adj.items():
            for v, dd in nbrs.items():
                G.add_edge(u, v, **dd)
        return G

    def subgraph(self, nodes: Any) -> DiGraph:
        node_set = set(nodes)
        G = self.__class__()
        G.graph = self.graph
        g_node = G._node
        g_adj = G._adj
        g_pred = G._pred
        for n in node_set:
            if n in self._node:
                g_node[n] = self._node[n]
                g_adj[n] = {}
                g_pred[n] = {}
        for u in node_set:
            if u in self._adj:
                for v, dd in self._adj[u].items():
                    if v in node_set:
                        g_adj[u][v] = dd
                        g_pred[v][u] = dd
        return G
