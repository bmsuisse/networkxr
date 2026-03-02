# networkXR

> [!CAUTION]
> 🚧 **Under Heavy Construction** 🚧
>
> This project is in early development. APIs may change without notice. Not yet ready for production use.

## Goal

**networkXR** is a Rust-backed, drop-in replacement for [NetworkX](https://networkx.org/) — the popular Python library for graph creation, manipulation, and analysis.

By leveraging [PyO3](https://pyo3.rs/) and Rust's performance characteristics, networkXR aims to provide a **fully compatible NetworkX API** with significantly improved speed for compute-intensive graph operations, while remaining a seamless swap for existing Python codebases.

### Why networkXR?

- 🚀 **Blazing Fast**: Core graphs (`Graph`, `DiGraph`) use Rust `IndexMap` internally for high-performance processing.
- 🤝 **Drop-in Replaceable**: Change your `import networkx as nx` to `import networkxr as nx`. That's it.
- 🎨 **Batteries Included**: Comes with generators (including fake data), converters, isomorphism checks, and a rich Plotly-native visualization engine.

## Installation

```bash
pip install networkxr

# With interactive plotting support (optional)
pip install networkxr[plot]
```

## Quick Start

```python
# Just swap the import — everything else stays the same
import networkxr as nx

G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
G.add_node(5, role="isolated")

print(G.number_of_nodes())   # 5
print(G.number_of_edges())   # 5
print(list(G.neighbors(1)))  # [2, 3, 4]
```

## Plotting & Visualization

networkXR natively supports **Plotly** for interactive, publication-ready graph visualization out-of-the-box (no matplotlib required!).

```python
import networkxr as nx

# Create a beautiful graph topology
G = nx.barbell_graph(5, 1)

# Draw it with custom styling
fig = nx.draw(
    G, 
    node_color="#6366f1", 
    edge_color="#cbd5e1", 
    title="Barbell Graph Visualization", 
    show=False
)
fig.write_html("my_graph.html")
```

> **Note:** Plotting requires `plotly` — install with `pip install networkxr[plot]`.

## Rich Data Generation

Need a realistic graph for testing? networkXR includes Faker-powered network generation:

```python
import networkxr as nx

# Create a realistic social network graph with user attributes
G = nx.fake_social_network(n=50, p=0.1, seed=42)

for u, data in list(G.nodes(data=True))[:2]:
    print(f"{data['name']} ({data['email']}) works at {data['company']}")
```

## Documentation

For full API reference, examples, and cookbooks, check out our [documentation website](https://bmsuisse.github.io/networkXR/).
