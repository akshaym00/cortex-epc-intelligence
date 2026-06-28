"""
Reasoning Engine for Project Cortex.

Provides graph-based reasoning capabilities over the
Living Project Model.
"""

import networkx as nx

from backend.graph.graph_utils import GraphUtils


class ReasoningEngine:
    """
    Performs reasoning using the Living Project Graph.
    """

    def get_downstream_entities(
        self,
        graph: nx.DiGraph,
        entity_id: str,
    ) -> list[str]:
        """
        Return every downstream entity affected by
        the supplied entity.
        """

        return GraphUtils.find_downstream_entities(
            graph,
            entity_id,
        )