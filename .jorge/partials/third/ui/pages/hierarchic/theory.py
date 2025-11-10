"""
Theory content for Hierarchical Clustering page.

Single Responsibility: Render educational content explaining hierarchical clustering.
"""

import streamlit as st


def render_theory_section():
    """
    Render theory expander with educational content about Hierarchical Clustering.
    
    Returns:
        None (renders directly to Streamlit)
    """
    with st.expander("📚 THEORY: Hierarchical Clustering & Dendrograms", expanded=False):
        st.markdown("""
        ### What is Hierarchical Clustering?
        
        **Agglomerative (bottom-up)**: Starts with each student as a separate cluster,
        then iteratively merges the closest pairs until all students belong to one cluster.
        
        ### Why Hierarchical Clustering?
        
        - **Dendrogram visualization**: Shows the tree of merges → understand relationships
        - **No need to specify K upfront**: Can cut the tree at any height
        - **Reveals structure**: See natural groupings at different granularities
        - **Interpretable**: Each merge decision is based on similarity
        
        ### Linkage Methods
        
        How to measure distance between clusters:
        
        - **Ward**: Minimize within-cluster variance (best for balanced, spherical clusters)
        - **Complete**: Maximum distance between any two points (compact clusters)
        - **Average**: Mean distance between all pairs (balanced approach)
        - **Single**: Minimum distance between closest points (can create chains)
        
        ### The Dendrogram
        
        ```
        Height = distance at which clusters merge
        ├── High cut → few large clusters (general patterns)
        └── Low cut → many small clusters (specific subgroups)
        ```
        
        ### J4 Metric (Optimal K)
        
        **Silhouette Score**: Measures how similar each point is to its own cluster
        compared to other clusters. Range: [-1, 1]
        
        - **1.0**: Perfect clustering
        - **0.0**: Overlapping clusters
        - **-1.0**: Wrong assignments
        
        **J4**: Average silhouette score across all samples. Higher = better clustering.
        
        ### Use Case for Students
        
        Discover natural student groups based on behavior, demographics, and performance:
        - "High achievers with low social activity"
        - "Struggling students with high failures"
        - "Average performers with strong family support"
        
        These insights can guide targeted interventions!
        """)

