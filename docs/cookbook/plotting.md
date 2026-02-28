---
title: "Cookbook: Plotting Graphs"
---

# Plotting Graphs with Plotly

networkXR ships with a zero-dependency core, but when you need visualization
it natively supports **Plotly** for interactive, publication-quality graph plots.

!!! tip "Install the plotting extra"
    ```bash
    pip install networkxr[plot]
    ```

---

## 1 — Basic Plot

```python
import networkxr as nx

G = nx.barbell_graph(5, 1)
nx.draw(G)
```

This opens an interactive Plotly figure with hover tooltips showing each
node's name and degree.

---

## 2 — Social Network

Build a small social network and visualize it with custom styling:

```python
import networkxr as nx

G = nx.Graph()

# Add people
people = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"]
G.add_nodes_from(people)

# Add friendships
G.add_edges_from([
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Dave"),
    ("Carol", "Dave"),
    ("Carol", "Eve"),
    ("Dave", "Frank"),
    ("Eve", "Frank"),
    ("Alice", "Eve"),
])

nx.draw(
    G,
    node_color="#8b5cf6",
    node_size=28,
    edge_color="#a78bfa",
    edge_width=1.5,
    font_size=13,
    title="Friend Network",
)
```

---

## 3 — Circular Layout

Ring and cycle graphs look best on a circle:

```python
import networkxr as nx

G = nx.cycle_graph(12)

nx.draw(G, layout="circular", node_color="#06b6d4", title="Cycle C₁₂")
```

---

## 4 — Per-Node Colours

Colour each node individually — useful for community detection or
categorical data:

```python
import networkxr as nx

G = nx.star_graph(6)

# Hub gets a different colour from the leaves
colors = ["#ef4444"] + ["#3b82f6"] * 6

nx.draw(
    G,
    node_color=colors,
    node_size=30,
    title="Star Graph — Hub vs Leaves",
)
```

---

## 5 — Export to HTML

Save a fully interactive graph as a standalone HTML file:

```python
import networkxr as nx

G = nx.complete_graph(8)

fig = nx.draw(G, show=False, title="K₈ — Complete Graph")
fig.write_html("graph_k8.html")
```

Open `graph_k8.html` in any browser — no server required.

---

## 6 — Custom Positions

Supply your own `{node: (x, y)}` dictionary for full control:

```python
import networkxr as nx

G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])

pos = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}

nx.draw(G, pos=pos, node_color="#10b981", title="Square with Diagonal")
```

---

## 7 — Dark-Theme Dashboard

Customise the Plotly figure after calling `draw()`:

```python
import networkxr as nx

G = nx.barbell_graph(5, 1)

fig = nx.draw(
    G,
    show=False,
    node_color="#a78bfa",
    edge_color="#475569",
    font_color="#e2e8f0",
    title="Dark Dashboard",
)

fig.update_layout(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    title_font_color="#f1f5f9",
)
fig.show()
```

---

## 8 — Using Layouts Directly

The layout functions are first-class citizens — use them with any
plotting library:

```python
import networkxr as nx

G = nx.complete_graph(10)

# Compute positions once
pos = nx.spring_layout(G, seed=7)

# Option A: use with nx.draw
nx.draw(G, pos=pos, show=False)

# Option B: feed into raw Plotly
import plotly.graph_objects as go

fig = go.Figure()
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    fig.add_trace(
        go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line={"color": "#94a3b8", "width": 0.5},
            hoverinfo="none",
            showlegend=False,
        )
    )

node_x = [pos[n][0] for n in G.nodes()]
node_y = [pos[n][1] for n in G.nodes()]
fig.add_trace(
    go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        marker={"size": 12, "color": "#6366f1"},
        text=[str(n) for n in G.nodes()],
        hoverinfo="text",
    )
)
fig.update_layout(showlegend=False)
fig.show()
```
