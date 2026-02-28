---
title: Plotting Graphs
---

# Plotting Graphs

networkXR provides a built-in `draw()` function powered by **Plotly** for interactive graph visualization — with hover tooltips, panning, and zoom out of the box.

!!! info "Optional Dependency"
    Plotly is **not** required by networkXR itself. Install the optional plotting extra when you need it:

    ```bash
    pip install networkxr[plot]
    # or
    uv add networkxr[plot]
    ```

---

## Quick Start

```python
import networkxr as nx

G = nx.barbell_graph(5, 1)
nx.draw(G)
```

This opens an interactive Plotly figure in your browser (or inline in Jupyter).

---

## Choosing a Layout

Two built-in layout algorithms are available — no extra dependencies required.

### Spring Layout (default)

The [Fruchterman-Reingold](https://en.wikipedia.org/wiki/Force-directed_graph_drawing)
force-directed layout spreads nodes apart while pulling connected nodes closer.

```python
G = nx.complete_graph(8)
nx.draw(G, layout="spring")
```

### Circular Layout

Places nodes evenly around a circle — ideal for ring or cycle graphs.

```python
G = nx.cycle_graph(12)
nx.draw(G, layout="circular")
```

### Custom Positions

Pass your own positions as a ``{node: (x, y)}`` dictionary:

```python
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 1)])

pos = {1: (0, 0), 2: (1, 0), 3: (0.5, 0.87)}
nx.draw(G, pos=pos)
```

---

## Customising Appearance

`draw()` accepts many options to fine-tune the visual output:

```python
G = nx.star_graph(6)

fig = nx.draw(
    G,
    node_color="#10b981",      # Emerald green
    node_size=30,
    edge_color="#64748b",
    edge_width=2.0,
    with_labels=True,
    font_size=14,
    title="Star Graph K₆",
    width=900,
    height=600,
    show=False,                # Don't open browser, return Figure
)

# Further customise with the Plotly API
fig.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#1e293b")
fig.show()
```

### Per-Node Colours

Pass a list of CSS colour strings (one per node):

```python
G = nx.path_graph(5)
colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6"]
nx.draw(G, node_color=colors)
```

---

## Working with Layouts Directly

The layout functions are also exposed at the top level for advanced use:

```python
import networkxr as nx

G = nx.barbell_graph(5, 1)

pos = nx.spring_layout(G, seed=42)
# pos = nx.circular_layout(G)

# Use with draw
nx.draw(G, pos=pos, show=False)

# Or with any other plotting library
import plotly.graph_objects as go

fig = go.Figure()
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines"))
fig.show()
```

---

## Comparison to NetworkX

| Feature          | NetworkX (`nx.draw`)         | networkXR (`nx.draw`)       |
| ---------------- | ---------------------------- | --------------------------- |
| Backend          | Matplotlib (static)          | **Plotly (interactive)**    |
| Hover info       | ❌                           | ✅ Node name + degree       |
| Zoom / Pan       | Limited                      | ✅ Built-in                 |
| Jupyter support  | ✅                           | ✅                          |
| HTML export      | ❌                           | ✅ `fig.write_html()`       |
| Dependencies     | matplotlib required          | `networkxr[plot]` optional  |

---

## Full API Reference

::: networkxr.drawing.nx_plotly.draw

::: networkxr.drawing.layout.spring_layout

::: networkxr.drawing.layout.circular_layout
