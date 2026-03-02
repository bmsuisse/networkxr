---
title: "Cookbook: Classic Generators"
---

# Classic Graph Generators

networkXR includes standard graph generators out-of-the-box, allowing you to quickly create well-known graph topologies for testing algorithms or visualising networks. 

## Basic Generators

```python
import networkxr as nx

# An empty graph with 10 nodes (no edges)
G_empty = nx.empty_graph(10)

# A path graph with 5 nodes in a line
G_path = nx.path_graph(5)

# A cycle graph (ring) with 8 nodes
G_cycle = nx.cycle_graph(8)
```

## Complete Graphs & Stars

Complete graphs connect every node to every other node, while star graphs feature one central hub connected to multiple peripheral nodes.

```python
import networkxr as nx

# Complete graph with 6 nodes (K6)
K_6 = nx.complete_graph(6)
print(f"Nodes: {K_6.number_of_nodes()}, Edges: {K_6.number_of_edges()}")
# Output: Nodes: 6, Edges: 15

# A star graph with a center node and 7 outer nodes
G_star = nx.star_graph(7)
```

## Barbell Graphs

A barbell graph consists of two complete graphs connected by a path. It is often used in community detection and random walk experiments.

```python
import networkxr as nx

# Two K5 graphs connected by a path of length 2
G_barbell = nx.barbell_graph(m1=5, m2=2)

# Verify the number of nodes
# (2 * m1) + m2 = (2 * 5) + 2 = 12 nodes
print(f"Barbell Nodes: {G_barbell.number_of_nodes()}")
```

## Combining Generators with Plotting

You can quickly visualise generated topologies using the built-in [plotting functionality](plotting.md):

```python
import networkxr as nx

# Generate standard shapes
G_cycle = nx.cycle_graph(20)
G_barbell = nx.barbell_graph(10, 3)

# View them interactively
nx.draw(G_cycle, layout="circular", node_color="#10b981", title="C20 Cycle")
nx.draw(G_barbell, node_color="#6366f1", title="Barbell Graph (10, 3)")
```
