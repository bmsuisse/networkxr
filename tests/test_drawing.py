"""Tests for networkxr.drawing."""

from __future__ import annotations

import pytest

import networkxr as nx
from networkxr.drawing.layout import circular_layout, spring_layout

plotly = pytest.importorskip("plotly")


# ── Layout tests ────────────────────────────────────────────────────


class TestSpringLayout:
    def test_empty_graph(self) -> None:
        G = nx.Graph()
        pos = spring_layout(G)
        assert pos == {}

    def test_single_node(self) -> None:
        G = nx.Graph()
        G.add_node(1)
        pos = spring_layout(G)
        assert 1 in pos

    def test_returns_positions_for_all_nodes(self) -> None:
        G = nx.path_graph(5)
        pos = spring_layout(G)
        assert len(pos) == 5
        for node in G.nodes():
            assert node in pos
            x, y = pos[node]
            assert isinstance(x, float)
            assert isinstance(y, float)

    def test_seed_reproducibility(self) -> None:
        G = nx.complete_graph(6)
        pos1 = spring_layout(G, seed=42)
        pos2 = spring_layout(G, seed=42)
        for node in G.nodes():
            assert pos1[node] == pos2[node]


class TestCircularLayout:
    def test_empty_graph(self) -> None:
        G = nx.Graph()
        pos = circular_layout(G)
        assert pos == {}

    def test_single_node(self) -> None:
        G = nx.Graph()
        G.add_node("a")
        pos = circular_layout(G)
        assert "a" in pos

    def test_nodes_on_circle(self) -> None:
        import math

        G = nx.path_graph(4)
        pos = circular_layout(G, scale=1.0)
        for _, (x, y) in pos.items():
            r = math.sqrt(x * x + y * y)
            assert abs(r - 1.0) < 1e-6


# ── Draw tests ──────────────────────────────────────────────────────


class TestDraw:
    def test_returns_plotly_figure(self) -> None:
        import plotly.graph_objects as go

        G = nx.barbell_graph(3, 1)
        fig = nx.draw(G, show=False)
        assert isinstance(fig, go.Figure)

    def test_with_pos(self) -> None:
        import plotly.graph_objects as go

        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3)])
        pos = {1: (0.0, 0.0), 2: (1.0, 0.0), 3: (0.5, 1.0)}
        fig = nx.draw(G, pos=pos, show=False)
        assert isinstance(fig, go.Figure)

    def test_circular_layout_option(self) -> None:
        import plotly.graph_objects as go

        G = nx.cycle_graph(6)
        fig = nx.draw(G, layout="circular", show=False)
        assert isinstance(fig, go.Figure)

    def test_without_labels(self) -> None:
        import plotly.graph_objects as go

        G = nx.path_graph(3)
        fig = nx.draw(G, with_labels=False, show=False)
        assert isinstance(fig, go.Figure)

    def test_custom_colors(self) -> None:
        import plotly.graph_objects as go

        G = nx.path_graph(3)
        colors = ["#ff0000", "#00ff00", "#0000ff"]
        fig = nx.draw(G, node_color=colors, show=False)
        assert isinstance(fig, go.Figure)

    def test_digraph(self) -> None:
        import plotly.graph_objects as go

        D = nx.DiGraph()
        D.add_edges_from([("a", "b"), ("b", "c"), ("c", "a")])
        fig = nx.draw(D, show=False)
        assert isinstance(fig, go.Figure)
