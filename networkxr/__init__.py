"""networkxr — drop-in replacement for NetworkX (Rust-accelerated)."""

from __future__ import annotations

# Core graph types (pure Python for now, Rust backend later)
from networkxr.classes.digraph import DiGraph
from networkxr.classes.graph import Graph

# Pure Python multi-graph types
from networkxr.multigraph import MultiDiGraph, MultiGraph

# Rust-accelerated integer graph
from networkxr.intgraph import IntGraph

# Convert functions
from networkxr.convert import (
    from_dict_of_dicts,
    from_dict_of_lists,
    to_dict_of_dicts,
    to_dict_of_lists,
    to_edgelist,
    to_networkx_graph,
)

# Exceptions
from networkxr.exception import (
    AmbiguousSolution,
    ExceededMaxIterations,
    HasACycle,
    NetworkXAlgorithmError,
    NetworkXError,
    NetworkXException,
    NetworkXNoCycle,
    NetworkXNoPath,
    NetworkXPointlessConcept,
    NetworkXUnbounded,
    NetworkXUnfeasible,
    NodeNotFound,
    PowerIterationFailedConvergence,
)

# Generators
from networkxr.generators.classic import (
    barbell_graph,
    complete_graph,
    cycle_graph,
    empty_graph,
    path_graph,
    star_graph,
)
from networkxr.generators.fake import (
    fake_org_chart,
    fake_social_network,
    fake_transaction_network,
)

# Isomorphism
from networkxr.isomorphism import is_isomorphic

# Relabel
from networkxr.relabel import convert_node_labels_to_integers, relabel_nodes

# Removed functions (raise helpful deprecation messages)
from networkxr.removed import random_tree

# Drawing (optional — requires plotly)
from networkxr.drawing import draw
from networkxr.drawing.layout import circular_layout, spring_layout

# Utils
from networkxr.utils.misc import edges_equal, flatten, graphs_equal, nodes_equal, pairwise

__version__ = "0.1.5"

__all__ = [
    "DiGraph",
    "Graph",
    "IntGraph",
    "MultiDiGraph",
    "MultiGraph",
    "AmbiguousSolution",
    "ExceededMaxIterations",
    "HasACycle",
    "NetworkXAlgorithmError",
    "NetworkXError",
    "NetworkXException",
    "NetworkXNoCycle",
    "NetworkXNoPath",
    "NetworkXPointlessConcept",
    "NetworkXUnbounded",
    "NetworkXUnfeasible",
    "NodeNotFound",
    "PowerIterationFailedConvergence",
    "barbell_graph",
    "circular_layout",
    "complete_graph",
    "convert_node_labels_to_integers",
    "cycle_graph",
    "draw",
    "edges_equal",
    "empty_graph",
    "fake_org_chart",
    "fake_social_network",
    "fake_transaction_network",
    "flatten",
    "from_dict_of_dicts",
    "from_dict_of_lists",
    "graphs_equal",
    "is_isomorphic",
    "nodes_equal",
    "pairwise",
    "path_graph",
    "random_tree",
    "relabel_nodes",
    "spring_layout",
    "star_graph",
    "to_dict_of_dicts",
    "to_dict_of_lists",
    "to_edgelist",
    "to_networkx_graph",
]
