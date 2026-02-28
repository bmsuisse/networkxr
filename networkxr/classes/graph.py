"""Pure Python Graph — undirected, single-edge, NetworkX-compatible API.

Optimised for speed:
- ``__slots__`` on hot classes
- EAFP (try/except) instead of LBYL (if … in …) in hot paths
- Direct ``dict`` operations bypassing factory indirection
- Minimal attribute lookups via local-variable caching
"""

from __future__ import annotations

from typing import Any

from networkxr.classes.views import DegreeView, EdgeView, NodeView


class Graph:
    """Undirected graph with self-loops but no parallel edges."""

    __slots__ = ("graph", "_node", "_adj")

    # Factories for subclass customisation
    node_attr_dict_factory = dict
    adjlist_inner_dict_factory = dict
    edge_attr_dict_factory = dict
    graph_attr_dict_factory = dict

    def __init__(self, incoming_graph_data: Any = None, **attr: Any) -> None:
        self.graph: dict[str, Any] = {}
        self.graph.update(attr)
        self._node: dict[Any, dict[str, Any]] = {}
        self._adj: dict[Any, dict[Any, dict[str, Any]]] = {}
        if incoming_graph_data is not None:
            self._ingest(incoming_graph_data)

    # ── internal ────────────────────────────────────────────────

    def _ingest(self, data: Any) -> None:
        if isinstance(data, Graph):
            for n, dd in data.nodes(data=True):
                self.add_node(n, **dd)
            for u, v, dd in data.edges(data=True):
                self.add_edge(u, v, **dd)
            self.graph.update(data.graph)
        elif hasattr(data, "nodes") and hasattr(data, "edges"):
            for n, dd in data.nodes(data=True):
                self.add_node(n, **dd)
            for e in data.edges(data=True):
                if len(e) == 3:
                    self.add_edge(e[0], e[1], **e[2])
                elif len(e) == 2:
                    self.add_edge(e[0], e[1])
            if hasattr(data, "graph") and isinstance(data.graph, dict):
                self.graph.update(data.graph)
        elif isinstance(data, dict):
            first_val = next(iter(data.values()), None)
            if isinstance(first_val, dict):
                for u in data:
                    self.add_node(u)
                for u, nbrs in data.items():
                    for v, edata in nbrs.items():
                        if isinstance(edata, dict):
                            first_inner = next(iter(edata.values()), None) if edata else None
                            if isinstance(first_inner, dict):
                                merged: dict[str, Any] = {}
                                for _key, attr_dict in edata.items():
                                    merged.update(attr_dict)
                                self.add_edge(u, v, **merged)
                            else:
                                self.add_edge(u, v, **edata)
                        else:
                            self.add_edge(u, v)
            elif isinstance(first_val, list):
                for u, nbrs in data.items():
                    self.add_node(u)
                    for v in nbrs:
                        self.add_edge(u, v)
            else:
                msg = "Input is not a known data type for conversion"
                raise TypeError(msg)
        elif hasattr(data, "__iter__"):
            for item in data:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    u, v = item[0], item[1]
                    dd = item[2] if len(item) >= 3 and isinstance(item[2], dict) else {}
                    self.add_edge(u, v, **dd)
                else:
                    from networkxr.exception import NetworkXError

                    msg = "Input is not a valid edge list"
                    raise NetworkXError(msg)

    # ── properties ──────────────────────────────────────────────

    @property
    def adj(self) -> dict[Any, dict[Any, dict[str, Any]]]:
        return self._adj

    @property
    def name(self) -> str:
        return self.graph.get("name", "")

    @name.setter
    def name(self, val: str) -> None:
        self.graph["name"] = val

    # ── node ops  (EAFP hot path) ──────────────────────────────

    def add_node(self, node_for_adding: Any, **attr: Any) -> None:
        _node = self._node
        try:
            _node[node_for_adding].update(attr)
        except KeyError:
            _node[node_for_adding] = attr.copy() if attr else {}
            self._adj[node_for_adding] = {}

    def add_nodes_from(self, nodes: Any, **attr: Any) -> None:
        _node = self._node
        _adj = self._adj
        for item in nodes:
            if isinstance(item, tuple) and len(item) == 2:
                n, dd = item
                ndict = {**attr, **(dd if isinstance(dd, dict) else {})}
                try:
                    _node[n].update(ndict)
                except KeyError:
                    _node[n] = ndict
                    _adj[n] = {}
            else:
                try:
                    _node[item].update(attr)
                except KeyError:
                    _node[item] = attr.copy() if attr else {}
                    _adj[item] = {}

    def remove_node(self, n: Any) -> None:
        _adj = self._adj
        try:
            nbrs = _adj[n]
        except KeyError:
            msg = f"The node {n} is not in the graph."
            raise KeyError(msg) from None
        for nbr in nbrs:
            _adj[nbr].pop(n, None)
        del _adj[n]
        del self._node[n]

    def remove_nodes_from(self, nodes: Any) -> None:
        _adj = self._adj
        for n in nodes:
            try:
                nbrs = _adj[n]
            except KeyError:
                continue
            for nbr in nbrs:
                _adj[nbr].pop(n, None)
            del _adj[n]
            del self._node[n]

    # ── edge ops (EAFP hot path — the most critical) ──────────

    def add_edge(self, u_of_edge: Any, v_of_edge: Any, **attr: Any) -> None:
        u, v = u_of_edge, v_of_edge
        _node = self._node
        _adj = self._adj
        # Ensure both nodes exist (EAFP)
        if u not in _node:
            _node[u] = {}
            _adj[u] = {}
        if v not in _node:
            _node[v] = {}
            _adj[v] = {}
        # Add/update edge
        adj_u = _adj[u]
        try:
            adj_u[v].update(attr)
        except KeyError:
            dd = dict(attr)
            adj_u[v] = dd
            _adj[v][u] = dd  # share the same dict (undirected)

    def add_edges_from(self, ebunch: Any, **attr: Any) -> None:
        _node = self._node
        _adj = self._adj
        for e in ebunch:
            ne = len(e)
            if ne >= 3 and isinstance(e[2], dict):
                u, v = e[0], e[1]
                eattr = {**attr, **e[2]}
            elif ne >= 2:
                u, v = e[0], e[1]
                eattr = attr
            else:
                continue
            if u not in _node:
                _node[u] = {}
                _adj[u] = {}
            if v not in _node:
                _node[v] = {}
                _adj[v] = {}
            adj_u = _adj[u]
            try:
                adj_u[v].update(eattr)
            except KeyError:
                dd = dict(eattr)
                adj_u[v] = dd
                _adj[v][u] = dd

    def add_weighted_edges_from(self, ebunch: Any, weight: str = "weight") -> None:
        _node = self._node
        _adj = self._adj
        for e in ebunch:
            u, v, w = e[0], e[1], e[2]
            if u not in _node:
                _node[u] = {}
                _adj[u] = {}
            if v not in _node:
                _node[v] = {}
                _adj[v] = {}
            adj_u = _adj[u]
            try:
                adj_u[v][weight] = w
            except KeyError:
                dd = {weight: w}
                adj_u[v] = dd
                _adj[v][u] = dd

    def remove_edge(self, u: Any, v: Any) -> None:
        try:
            del self._adj[u][v]
        except KeyError:
            msg = f"Edge {u}-{v} is not in the graph."
            raise KeyError(msg) from None
        if u != v:
            del self._adj[v][u]

    # ── queries ─────────────────────────────────────────────────

    def has_node(self, n: Any) -> bool:
        return n in self._node

    def has_edge(self, u: Any, v: Any) -> bool:
        try:
            return v in self._adj[u]
        except KeyError:
            return False

    def neighbors(self, n: Any) -> Any:
        try:
            return iter(self._adj[n])
        except KeyError:
            msg = f"The node {n} is not in the graph."
            raise KeyError(msg) from None

    def get_edge_data(self, u: Any, v: Any, default: Any = None) -> Any:
        try:
            return self._adj[u][v]
        except KeyError:
            return default

    # ── views ───────────────────────────────────────────────────

    @property
    def nodes(self) -> NodeView:
        return NodeView(self)

    @property
    def edges(self) -> EdgeView:
        return EdgeView(self)

    @property
    def degree(self) -> DegreeView:
        return DegreeView(self)

    def adjacency(self) -> Any:
        return iter(self._adj.items())

    # ── info ────────────────────────────────────────────────────

    def number_of_nodes(self) -> int:
        return len(self._node)

    def number_of_edges(self) -> int:
        return len(self.edges)

    def order(self) -> int:
        return len(self._node)

    def size(self, weight: str | None = None) -> Any:
        if weight is not None:
            return sum(dd.get(weight, 1) for _u, _v, dd in self.edges(data=True))
        return self.number_of_edges()

    def is_multigraph(self) -> bool:
        return False

    def is_directed(self) -> bool:
        return False

    def copy(self) -> Graph:
        G = self.__class__()
        G.graph.update(self.graph)
        g_node = G._node
        g_adj = G._adj
        for n, dd in self._node.items():
            g_node[n] = dd.copy()
            g_adj[n] = {}
        for u, nbrs in self._adj.items():
            for v, dd in nbrs.items():
                if v not in g_adj[u]:
                    new_dd = dd.copy()
                    g_adj[u][v] = new_dd
                    g_adj[v][u] = new_dd
        return G

    def clear(self) -> None:
        self._node.clear()
        self._adj.clear()
        self.graph.clear()

    def clear_edges(self) -> None:
        for nbrs in self._adj.values():
            nbrs.clear()

    def subgraph(self, nodes: Any) -> Graph:
        node_set = set(nodes)
        G = self.__class__()
        G.graph = self.graph
        g_node = G._node
        g_adj = G._adj
        for n in node_set:
            if n in self._node:
                g_node[n] = self._node[n]
                g_adj[n] = {}
        for u in node_set:
            if u in self._adj:
                for v, dd in self._adj[u].items():
                    if v in node_set:
                        g_adj[u][v] = dd
        return G

    def to_undirected(self) -> Graph:
        return self.copy()

    # ── dunder ──────────────────────────────────────────────────

    def __contains__(self, n: Any) -> bool:
        return n in self._node

    def __len__(self) -> int:
        return len(self._node)

    def __iter__(self) -> Any:
        return iter(self._node)

    def __getitem__(self, n: Any) -> dict[Any, dict[str, Any]]:
        try:
            return self._adj[n]
        except KeyError:
            msg = f"The node {n} is not in the graph."
            raise KeyError(msg) from None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nodes={len(self._node)}, edges={len(self.edges)})"
