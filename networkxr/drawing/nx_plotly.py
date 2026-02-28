"""Plotly-based graph drawing for networkxr.

This module provides a ``draw()`` function that renders a networkxr graph as an
interactive Plotly figure.  **Plotly is not a hard dependency** of networkxr — it
is only imported when ``draw()`` is called, and a helpful ``ImportError`` is
raised if it is missing.

Install the optional plotting extra::

    pip install networkxr[plot]
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Hashable, Sequence

from networkxr.drawing.layout import spring_layout

if TYPE_CHECKING:
    import plotly.graph_objects as go  # type: ignore[import-untyped]


def _ensure_plotly() -> Any:
    """Return the ``plotly.graph_objects`` module or raise a clear error."""
    try:
        import plotly.graph_objects as go  # type: ignore[import-untyped]

        return go
    except ImportError:
        raise ImportError(
            "Plotly is required for drawing graphs.\n"
            "Install it with:\n"
            "  pip install networkxr[plot]\n"
            "  # or\n"
            "  pip install plotly"
        ) from None


def draw(
    G: Any,
    *,
    pos: dict[Hashable, tuple[float, float]] | None = None,
    with_labels: bool = True,
    node_color: str | Sequence[str] = "#6366f1",
    node_size: int = 20,
    edge_color: str = "#94a3b8",
    edge_width: float = 1.0,
    font_size: int = 12,
    font_color: str = "#1e293b",
    title: str | None = None,
    width: int = 800,
    height: int = 600,
    show: bool = True,
    layout: str = "spring",
    layout_seed: int | None = 42,
) -> go.Figure:
    """Draw a networkxr graph interactively with Plotly.

    This function produces an interactive Plotly figure similar to
    ``networkx.draw()``, but rendered via Plotly for rich hover-tooltips,
    zooming, and panning.

    Parameters
    ----------
    G : Graph | DiGraph | MultiGraph
        Any networkxr graph object.
    pos : dict, optional
        Pre-computed node positions as ``{node: (x, y)}``.  If *None*, a
        layout is computed automatically (see *layout*).
    with_labels : bool
        If *True*, draw node labels on the figure.
    node_color : str | Sequence[str]
        CSS colour string or a list of colours (one per node).
    node_size : int
        Marker size in pixels.
    edge_color : str
        CSS colour string for edges.
    edge_width : float
        Line width for edges.
    font_size : int
        Font size for node labels.
    font_color : str
        Font colour for node labels.
    title : str, optional
        Figure title.
    width : int
        Figure width in pixels.
    height : int
        Figure height in pixels.
    show : bool
        If *True*, call ``fig.show()`` before returning.
    layout : str
        Layout algorithm when *pos* is not provided.
        ``"spring"`` (default) — Fruchterman-Reingold force-directed layout.
        ``"circular"`` — nodes arranged on a circle.
    layout_seed : int, optional
        Random seed passed to the layout algorithm for reproducibility.

    Returns
    -------
    plotly.graph_objects.Figure
        The Plotly figure object (can be further customised).

    Raises
    ------
    ImportError
        If Plotly is not installed.

    Examples
    --------
    >>> import networkxr as nx
    >>> G = nx.barbell_graph(5, 1)
    >>> fig = nx.draw(G, show=False)  # returns a Plotly Figure
    """
    go = _ensure_plotly()

    # ── Compute layout ──────────────────────────────────────────────
    if pos is None:
        if layout == "circular":
            from networkxr.drawing.layout import circular_layout

            pos = circular_layout(G)
        else:
            pos = spring_layout(G, seed=layout_seed)

    nodes = list(G.nodes())

    # ── Edge traces ─────────────────────────────────────────────────
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []

    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line={"width": edge_width, "color": edge_color},
        hoverinfo="none",
    )

    # ── Node trace ──────────────────────────────────────────────────
    node_x = [pos[n][0] for n in nodes]
    node_y = [pos[n][1] for n in nodes]

    # Build hover text with degree info (graceful fallback)
    hover_text: list[str] = []
    for n in nodes:
        try:
            hover_text.append(f"{n} (degree {G.degree(n)})")
        except (KeyError, TypeError):
            hover_text.append(str(n))

    # Handle per-node colours
    marker_color: str | list[str]
    if isinstance(node_color, str):
        marker_color = node_color
    else:
        marker_color = list(node_color)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text" if with_labels else "markers",
        text=[str(n) for n in nodes] if with_labels else None,
        textposition="top center",
        textfont={"size": font_size, "color": font_color},
        hovertext=hover_text,
        hoverinfo="text",
        marker={
            "size": node_size,
            "color": marker_color,
            "line": {"width": 1.5, "color": "#ffffff"},
        },
    )

    # ── Assemble figure ─────────────────────────────────────────────
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            showlegend=False,
            hovermode="closest",
            width=width,
            height=height,
            xaxis={
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
            plot_bgcolor="#fafafa",
        ),
    )

    if show:
        fig.show()

    return fig
