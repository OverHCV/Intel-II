"""
Dataset Tab 2: Class Distribution
Visualizes malware family distribution and allows class selection
"""

import plotly.graph_objects as go
import streamlit as st


def render(dataset_info):
    """Render class distribution visualizations with selection interface"""
    st.subheader("Class Distribution & Selection")

    if not dataset_info["samples"]:
        st.warning("No data found")
        return

    # Get all classes
    all_classes = sorted(dataset_info["samples"].keys())

    # Initialize session state for selected classes
    if "selected_classes" not in st.session_state:
        st.session_state.selected_classes = all_classes.copy()  # Select all by default

    # Class selection interface
    st.markdown("### Select Classes to Include")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("Select All", width="stretch"):
            st.session_state.selected_classes = all_classes.copy()
            st.rerun()

    with col2:
        if st.button("Deselect All", width="stretch"):
            st.session_state.selected_classes = []
            st.rerun()

    with col3:
        # Quick filter for large/small classes
        threshold = st.number_input(
            "Min samples per class",
            min_value=0,
            max_value=1000,
            value=0,
            help="Filter classes with fewer samples than this threshold",
        )

        if threshold > 0:
            filtered_classes = [
                cls
                for cls in all_classes
                if dataset_info["samples"].get(cls, 0) >= threshold
            ]
            if st.button(f"Select classes with ≥{threshold} samples", width="stretch"):
                st.session_state.selected_classes = filtered_classes
                st.rerun()

    # Multi-select for individual class selection
    selected = st.multiselect(
        "Selected Classes (you can search by typing)",
        options=all_classes,
        default=st.session_state.selected_classes,
        key="class_selector",
        help="Select which malware families to include in your dataset",
    )

    # Update session state
    st.session_state.selected_classes = selected

    # Show selection summary
    if selected:
        total_samples = sum(dataset_info["samples"].get(c, 0) for c in selected)

        # Get split info
        use_cross_validation = st.session_state.get("use_cross_validation", False)

        if use_cross_validation:
            n_folds = st.session_state.get("n_folds", 5)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Selected Classes", len(selected))
            with col2:
                st.metric("Total Samples", f"{total_samples:,}")
            with col3:
                st.metric("K-Folds", n_folds)
        else:
            from utils.dataset_utils import calculate_split_percentages

            train_pct = st.session_state.get("train_split", 70)
            val_of_remaining = st.session_state.get("val_split", 50)
            train_final, val_final, test_final = calculate_split_percentages(
                train_pct, val_of_remaining
            )

            train_samples = int(total_samples * train_final / 100)
            val_samples = int(total_samples * val_final / 100)
            test_samples = int(total_samples * test_final / 100)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Selected Classes", len(selected))
            with col2:
                st.metric("Total Samples", f"{total_samples:,}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"Train ({train_final:.1f}%)", f"{train_samples:,}")
            with col2:
                st.metric(f"Val ({val_final:.1f}%)", f"{val_samples:,}")
            with col3:
                st.metric(f"Test ({test_final:.1f}%)", f"{test_samples:,}")
    else:
        st.warning("⚠️ No classes selected! Please select at least one class.")

    st.divider()

    # Visualization of distribution
    st.markdown("### Distribution Visualization")

    # Use selected classes for visualization
    display_classes = selected if selected else all_classes
    sample_counts = [dataset_info["samples"].get(c, 0) for c in display_classes]

    # Get split configuration from session state
    use_cross_validation = st.session_state.get("use_cross_validation", False)

    if use_cross_validation:
        # Cross-Validation: Show total samples per class
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                name="Total Samples (used in CV)",
                x=display_classes,
                y=sample_counts,
                marker_color="#98c127",
                text=sample_counts,
                textposition="outside",
            )
        )

        n_folds = st.session_state.get("n_folds", 5)
        title_text = f"Samples per Malware Family - {n_folds}-Fold Cross-Validation"
    else:
        # Fixed split: Show Train/Val/Test breakdown
        from utils.dataset_utils import calculate_split_percentages

        train_pct = st.session_state.get("train_split", 70)
        val_of_remaining = st.session_state.get("val_split", 50)
        train_final, val_final, test_final = calculate_split_percentages(
            train_pct, val_of_remaining
        )

        # Calculate samples per class for each split
        train_counts = [
            int(dataset_info["samples"].get(c, 0) * train_final / 100)
            for c in display_classes
        ]
        val_counts = [
            int(dataset_info["samples"].get(c, 0) * val_final / 100)
            for c in display_classes
        ]
        test_counts = [
            int(dataset_info["samples"].get(c, 0) * test_final / 100)
            for c in display_classes
        ]

        # Grouped bar chart with train/val/test
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name=f"Train ({train_final:.1f}%)",
                x=display_classes,
                y=train_counts,
                marker_color="#98c127",
                text=train_counts,
                textposition="outside",
            )
        )

        fig.add_trace(
            go.Bar(
                name=f"Validation ({val_final:.1f}%)",
                x=display_classes,
                y=val_counts,
                marker_color="#8fd7d7",
                text=val_counts,
                textposition="outside",
            )
        )

        fig.add_trace(
            go.Bar(
                name=f"Test ({test_final:.1f}%)",
                x=display_classes,
                y=test_counts,
                marker_color="#ffb255",
                text=test_counts,
                textposition="outside",
            )
        )

        title_text = "Samples per Malware Family - Train/Val/Test Split"

    fig.update_layout(
        title=title_text,
        xaxis_title="Malware Family",
        yaxis_title="Number of Samples",
        barmode="stack",
        height=500,
        xaxis={"tickangle": -45},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fafafa"),
        showlegend=True,
    )

    st.plotly_chart(fig, width="stretch")

    # Show imbalance status (depends on selected strategy)
    if selected and len(selected) > 1:
        selected_counts = [dataset_info["samples"].get(c, 0) for c in selected]
        original_ratio = max(selected_counts) / max(min(selected_counts), 1)
        imbalance_strategy = st.session_state.get(
            "imbalance_strategy", "Auto Class Weights (Recommended)"
        )

        if imbalance_strategy == "No Adjustment":
            if original_ratio > 10:
                st.error(
                    f"⚠️ **Severe Imbalance:** {original_ratio:.1f}:1 — No mitigation selected!"
                )
            elif original_ratio > 3:
                st.warning(
                    f"⚠️ **Moderate Imbalance:** {original_ratio:.1f}:1 — Consider using class weights"
                )
        else:
            st.success(
                f"✅ **Imbalance Handled:** Original {original_ratio:.1f}:1 → Strategy: _{imbalance_strategy}_"
            )

    # Effective Distribution After Balancing
    render_effective_distribution(display_classes, sample_counts)

    # Top and bottom classes (from selected)
    if selected:
        col1, col2 = st.columns(2)

        selected_items = [(c, dataset_info["samples"].get(c, 0)) for c in selected]

        with col1:
            st.markdown("**Most Common Selected Classes**")
            top_5 = sorted(selected_items, key=lambda x: x[1], reverse=True)[:5]
            for cls, count in top_5:
                st.text(f"{cls}: {count:,} samples")

        with col2:
            st.markdown("**Least Common Selected Classes**")
            bottom_5 = sorted(selected_items, key=lambda x: x[1])[:5]
            for cls, count in bottom_5:
                st.text(f"{cls}: {count:,} samples")


def render_effective_distribution(display_classes, sample_counts):
    """Render effective distribution with Train/Val/Test split (matching first chart format)"""
    st.divider()
    st.markdown("### Effective Distribution (After Balancing)")

    imbalance_strategy = st.session_state.get(
        "imbalance_strategy", "Auto Class Weights (Recommended)"
    )

    if imbalance_strategy == "No Adjustment":
        st.info("ℹ️ No balancing applied — see original distribution above")
        return

    if not sample_counts or not display_classes:
        return

    max_samples = max(sample_counts) if sample_counts else 1

    # Calculate effective counts based on strategy
    if "Auto Class Weights" in imbalance_strategy:
        effective_counts = [max_samples] * len(display_classes)
        explanation = "All classes contribute **equally** to training loss"

    elif imbalance_strategy == "Selective Augmentation (H2)":
        threshold = st.session_state.get("minority_threshold", 200)
        multiplier = st.session_state.get("aug_multiplier", 2.0)
        effective_counts = [
            int(count * multiplier) if count < threshold else count
            for count in sample_counts
        ]
        explanation = f"Minority classes (<{threshold} samples) get **{multiplier}x** augmentation"

    elif imbalance_strategy == "Manual Class Weights":
        weights = st.session_state.get("class_weights", {})
        effective_counts = [
            int(sample_counts[i] * weights.get(c, 1.0))
            for i, c in enumerate(display_classes)
        ]
        explanation = "Effective contribution = samples × weight"

    elif imbalance_strategy == "Oversampling (SMOTE)":
        smote_ratio = st.session_state.get("smote_ratio", 0.5)
        target = int(max_samples * smote_ratio)
        effective_counts = [max(count, target) for count in sample_counts]
        explanation = f"SMOTE targets {smote_ratio * 100:.0f}% of majority class"

    elif imbalance_strategy == "Undersampling":
        min_samples = min(sample_counts) if sample_counts else 1
        effective_counts = [min_samples] * len(display_classes)
        explanation = "All classes reduced to smallest class size"

    else:
        effective_counts = sample_counts
        explanation = ""

    st.info(explanation)

    # Build chart with Train/Val/Test split (same format as first chart)
    use_cross_validation = st.session_state.get("use_cross_validation", False)

    fig = go.Figure()

    if use_cross_validation:
        # Cross-validation: single bar per class
        n_folds = st.session_state.get("n_folds", 5)
        fig.add_trace(
            go.Bar(
                name="Effective Samples (CV)",
                x=display_classes,
                y=effective_counts,
                marker_color="#98c127",
                text=effective_counts,
                textposition="outside",
            )
        )
        title_text = f"Effective Distribution - {n_folds}-Fold CV"
    else:
        # Fixed split: Train/Val/Test breakdown
        from utils.dataset_utils import calculate_split_percentages

        train_pct = st.session_state.get("train_split", 70)
        val_of_remaining = st.session_state.get("val_split", 50)
        train_final, val_final, test_final = calculate_split_percentages(
            train_pct, val_of_remaining
        )

        train_eff = [int(c * train_final / 100) for c in effective_counts]
        val_eff = [int(c * val_final / 100) for c in effective_counts]
        test_eff = [int(c * test_final / 100) for c in effective_counts]

        fig.add_trace(
            go.Bar(
                name=f"Train ({train_final:.1f}%)",
                x=display_classes,
                y=train_eff,
                marker_color="#98c127",
                text=train_eff,
                textposition="outside",
            )
        )

        fig.add_trace(
            go.Bar(
                name=f"Validation ({val_final:.1f}%)",
                x=display_classes,
                y=val_eff,
                marker_color="#8fd7d7",
                text=val_eff,
                textposition="outside",
            )
        )

        fig.add_trace(
            go.Bar(
                name=f"Test ({test_final:.1f}%)",
                x=display_classes,
                y=test_eff,
                marker_color="#ffb255",
                text=test_eff,
                textposition="outside",
            )
        )

        title_text = "Effective Distribution - Train/Val/Test Split"

    fig.update_layout(
        title=title_text,
        xaxis_title="Malware Family",
        yaxis_title="Effective Samples",
        barmode="stack",
        height=500,
        xaxis={"tickangle": -45},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#fafafa"),
        showlegend=True,
    )

    st.plotly_chart(fig, width="stretch")

    # Show improvement metrics
    if effective_counts and sample_counts:
        original_ratio = max(sample_counts) / max(min(sample_counts), 1)
        effective_ratio = max(effective_counts) / max(min(effective_counts), 1)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Ratio", f"{original_ratio:.1f}:1")
        with col2:
            st.metric("Effective Ratio", f"{effective_ratio:.1f}:1")
        with col3:
            improvement = ((original_ratio - effective_ratio) / original_ratio) * 100
            st.metric("Imbalance Reduction", f"{improvement:.0f}%")
