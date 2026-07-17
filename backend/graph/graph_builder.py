"""
Graph Builder for Project Cortex.

Converts a Project model into a directed graph
using NetworkX.
"""

import networkx as nx

from backend.models.project import Project


class GraphBuilder:
    """
    Builds a directed graph from a Project.
    """

    def build(self, project: Project) -> nx.DiGraph:
        """
        Convert a Project into a directed graph.

        Parameters
        ----------
        project : Project

        Returns
        -------
        nx.DiGraph
        """

        graph = nx.DiGraph()

        # --------------------------
        # Add Nodes
        # --------------------------

        for entity in project.entities:

            graph.add_node(
                entity.id,
                name=entity.name,
                entity_type=entity.entity_type.value,
                status=entity.status,
            )

        # --------------------------
        # Add Edges
        # --------------------------

        for relationship in project.relationships:

            graph.add_edge(
                relationship.source_entity_id,
                relationship.target_entity_id,
                relationship_type=relationship.relationship_type.value,
            )

        return graph
