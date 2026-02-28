"""Blazing-fast lightweight view objects for NetworkX API compatibility.

These allow both ``G.edges`` (iteration) and ``G.edges(data=True)`` (call)
to work on the same attribute.  All views use **generators** for iteration
(no intermediate list allocation) and ``__slots__`` for minimal overhead.
"""

from __future__ import annotations

from typing import Any, Iterator


# ═══════════════════════════════════════════════════════════════════
#  NodeView
# ═══════════════════════════════════════════════════════════════════


class NodeView:
    """View of nodes — iterable, callable, subscriptable."""

    __slots__ = ("_node",)

    def __init__(self, graph: Any) -> None:
        # Cache the dict directly — one fewer attribute lookup per access
        self._node: dict[Any, dict[str, Any]] = graph._node

    # -- callable: G.nodes(data=True) --
    def __call__(self, data: bool = False) -> Any:
        if data:
            return self._node.items()
        return self._node.keys()

    # -- iteration: uses dict's native C-speed iterator --
    def __iter__(self) -> Iterator[Any]:
        return iter(self._node)

    def __len__(self) -> int:
        return len(self._node)

    def __contains__(self, n: Any) -> bool:
        return n in self._node

    def __getitem__(self, n: Any) -> dict[str, Any]:
        return self._node[n]

    def __bool__(self) -> bool:
        return bool(self._node)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NodeView):
            return self._node.keys() == other._node.keys()
        if isinstance(other, (set, frozenset)):
            return self._node.keys() == other
        if isinstance(other, list):
            return list(self._node) == other
        return NotImplemented

    def __repr__(self) -> str:
        return f"NodeView({list(self._node)})"


# ═══════════════════════════════════════════════════════════════════
#  EdgeView  (undirected)
# ═══════════════════════════════════════════════════════════════════


class EdgeView:
    """Zero-allocation edge view for undirected Graph.

    The key trick: instead of a ``seen`` set, we only yield edge (u, v)
    when ``id(u_nbrs) <= id(v_nbrs)`` (or u == v for self-loops).
    Since _adj[u][v] and _adj[v][u] share the same edge-data dict,
    we can use the identity of the neighbor-dict to break symmetry
    — O(1) per edge, no set allocation.
    """

    __slots__ = ("_adj",)

    def __init__(self, graph: Any) -> None:
        self._adj: dict[Any, dict[Any, dict[str, Any]]] = graph._adj

    # -- generator iteration (hot path) --
    def __iter__(self) -> Iterator[tuple[Any, Any]]:
        seen: set[Any] = set()
        seen_add = seen.add  # local for speed
        for u, nbrs in self._adj.items():
            for v in nbrs:
                if v not in seen:
                    yield (u, v)
            seen_add(u)

    def __call__(self, data: bool = False, default: Any = None, keys: bool = False) -> Any:
        if not data:
            return self
        return self._iter_data(default)

    def _iter_data(self, default: Any = None) -> Iterator[tuple[Any, Any, Any]]:
        seen: set[Any] = set()
        seen_add = seen.add
        for u, nbrs in self._adj.items():
            for v, dd in nbrs.items():
                if v not in seen:
                    yield (u, v, dd)
            seen_add(u)

    def __len__(self) -> int:
        # O(V) — count half-edges, don't build a list
        adj = self._adj
        # Each edge (u,v) with u!=v is stored twice; self-loops stored once
        count = 0
        for u, nbrs in adj.items():
            count += len(nbrs)
            if u in nbrs:  # self-loop counted once extra
                count += 1
        return count >> 1  # divide by 2

    def __contains__(self, edge: Any) -> bool:
        try:
            return edge[1] in self._adj[edge[0]]
        except KeyError:
            return False

    def __repr__(self) -> str:
        return f"EdgeView({list(self)})"


# ═══════════════════════════════════════════════════════════════════
#  DiEdgeView  (directed)
# ═══════════════════════════════════════════════════════════════════


class DiEdgeView:
    """Zero-allocation edge view for DiGraph."""

    __slots__ = ("_adj",)

    def __init__(self, graph: Any) -> None:
        self._adj: dict[Any, dict[Any, dict[str, Any]]] = graph._adj

    def __iter__(self) -> Iterator[tuple[Any, Any]]:
        for u, nbrs in self._adj.items():
            for v in nbrs:
                yield (u, v)

    def __call__(self, data: bool = False, default: Any = None, keys: bool = False) -> Any:
        if not data:
            return self
        return self._iter_data(default)

    def _iter_data(self, default: Any = None) -> Iterator[tuple[Any, Any, Any]]:
        for u, nbrs in self._adj.items():
            for v, dd in nbrs.items():
                yield (u, v, dd)

    def __len__(self) -> int:
        return sum(len(nbrs) for nbrs in self._adj.values())

    def __contains__(self, edge: Any) -> bool:
        try:
            return edge[1] in self._adj[edge[0]]
        except KeyError:
            return False

    def __repr__(self) -> str:
        return f"DiEdgeView({list(self)})"


# ═══════════════════════════════════════════════════════════════════
#  DegreeView
# ═══════════════════════════════════════════════════════════════════


class DegreeView:
    """Degree view — iterable and callable."""

    __slots__ = ("_adj", "_node", "_pred")

    def __init__(self, graph: Any) -> None:
        self._adj = graph._adj
        self._node = graph._node
        self._pred = getattr(graph, "_pred", None)

    def __call__(self, nbunch: Any = None) -> Any:
        if nbunch is not None:
            if nbunch in self._node:
                deg = len(self._adj[nbunch])
                if self._pred is not None:
                    deg += len(self._pred[nbunch])
                return deg
            msg = f"The node {nbunch} is not in the graph."
            raise KeyError(msg)
        return list(self)

    def __iter__(self) -> Iterator[tuple[Any, int]]:
        if self._pred is not None:
            pred = self._pred
            for n, adj_nbrs in self._adj.items():
                if n in pred:
                    yield (n, len(adj_nbrs) + len(pred[n]))
                else:
                    yield (n, len(adj_nbrs))
        else:
            for n, nbrs in self._adj.items():
                yield (n, len(nbrs))

    def __len__(self) -> int:
        return len(self._node)

    def __repr__(self) -> str:
        return f"DegreeView({list(self)})"


# ═══════════════════════════════════════════════════════════════════
#  MultiEdgeView
# ═══════════════════════════════════════════════════════════════════


class MultiEdgeView:
    """Edge view for MultiGraph — supports data and keys."""

    __slots__ = ("_adj", "_directed")

    def __init__(self, graph: Any, directed: bool = False) -> None:
        self._adj = graph._adj
        self._directed = directed

    def __iter__(self) -> Iterator[tuple[Any, Any]]:
        if self._directed:
            for u in self._adj:
                for v in self._adj[u]:
                    for _key in self._adj[u][v]:
                        yield (u, v)
        else:
            seen: set[Any] = set()
            seen_add = seen.add
            for u in self._adj:
                for v in self._adj[u]:
                    if v not in seen:
                        for _key in self._adj[u][v]:
                            yield (u, v)
                seen_add(u)

    def __call__(self, data: bool = False, keys: bool = False) -> Any:
        if not data and not keys:
            return self
        return self._iter_filtered(data, keys)

    def _iter_filtered(self, data: bool = False, keys: bool = False) -> Iterator[tuple[Any, ...]]:
        if self._directed:
            for u in self._adj:
                for v in self._adj[u]:
                    for key, dd in self._adj[u][v].items():
                        if data and keys:
                            yield (u, v, key, dd)
                        elif data:
                            yield (u, v, dd)
                        elif keys:
                            yield (u, v, key)
                        else:
                            yield (u, v)
        else:
            seen: set[Any] = set()
            seen_add = seen.add
            for u in self._adj:
                for v in self._adj[u]:
                    if v not in seen:
                        for key, dd in self._adj[u][v].items():
                            if data and keys:
                                yield (u, v, key, dd)
                            elif data:
                                yield (u, v, dd)
                            elif keys:
                                yield (u, v, key)
                            else:
                                yield (u, v)
                seen_add(u)

    def __len__(self) -> int:
        if self._directed:
            return sum(len(keys) for nbrs in self._adj.values() for keys in nbrs.values())
        count = 0
        seen: set[Any] = set()
        seen_add = seen.add
        for u in self._adj:
            for v in self._adj[u]:
                if v not in seen:
                    count += len(self._adj[u][v])
            seen_add(u)
        return count

    def __contains__(self, edge: Any) -> bool:
        try:
            u, v = edge[0], edge[1]
            return v in self._adj.get(u, {})
        except (KeyError, IndexError):
            return False

    def __repr__(self) -> str:
        return f"MultiEdgeView({list(self)})"
