"""
Overall Analysis Component
Comprehensive comparison of SVM and ANN performance with and without PCA
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from ui.pages.pca.experiments import render_experiment_history, save_pca_experiment


def render_overall_analysis():
    """
    Render overall analysis comparing SVM and ANN with PCA
    Shows summary table, radar chart, and insights
    """
    st.markdown("### 📊 Overall Analysis & Conclusions")
    st.markdown("Comprehensive comparison of all models and PCA impact")

    # Save current experiment if both models are trained
    if (
        st.session_state.pca.get("pca_applied")
        and (
            st.session_state.pca.get("svm_pca_trained")
            or st.session_state.pca.get("ann_pca_trained")
        )
    ):
        # Auto-save experiment on first render
        if not st.session_state.pca.get("current_experiment_saved"):
            save_pca_experiment()
            st.session_state.pca["current_experiment_saved"] = True

    # Check if PCA has been applied
    if not st.session_state.pca.get("pca_applied"):
        st.warning("⚠️ Please apply PCA transformation first")
        return

    # Check which models have been trained on PCA
    has_svm_original = st.session_state.svm.get("best_model") is not None
    has_svm_pca = st.session_state.pca.get("svm_pca_trained", False)
    has_ann_original = st.session_state.ann.get("best_model") is not None
    has_ann_pca = st.session_state.pca.get("ann_pca_trained", False)

    if not (has_svm_original or has_ann_original):
        st.info("📝 No models available. Please save best models from SVM/ANN tabs first.")
        return

    # Render summary table
    _render_summary_table(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)

    st.divider()

    # Render radar chart if both models have PCA comparison
    if (has_svm_original and has_svm_pca) or (has_ann_original and has_ann_pca):
        _render_radar_chart(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)

    st.divider()

    # Render insights
    _render_insights(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)

    st.divider()

    # Export options
    _render_export_options(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)


def _render_summary_table(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Render summary comparison table"""
    st.markdown("#### 📋 Summary Comparison Table")

    table_data = []

    # SVM rows
    if has_svm_original:
        svm_original_metrics = st.session_state.svm.get("best_metrics", {})
        svm_original_acc = svm_original_metrics.get(
            "Accuracy", svm_original_metrics.get("CV Accuracy", 0)
        )
        svm_original_time = st.session_state.svm.get("best_params", {}).get("training_time", 0)

        table_data.append({
            "Model": "SVM",
            "Type": "Original",
            "Accuracy": f"{svm_original_acc:.4f}",
            "Training Time (s)": f"{svm_original_time:.2f}",
            "Dimensions": st.session_state.pca.get("X_scaled", np.array([])).shape[1] 
                if len(st.session_state.pca.get("X_scaled", [])) > 0 else "N/A",
        })

        if has_svm_pca:
            svm_pca_metrics = st.session_state.pca.get("svm_pca_metrics", {})
            svm_pca_acc = svm_pca_metrics.get("Accuracy", 0)
            svm_pca_time = st.session_state.pca.get("svm_pca_training_time", 0)
            delta_acc = svm_pca_acc - svm_original_acc
            delta_time = svm_pca_time - svm_original_time

            table_data.append({
                "Model": "SVM",
                "Type": "PCA",
                "Accuracy": f"{svm_pca_acc:.4f}",
                "Training Time (s)": f"{svm_pca_time:.2f}",
                "Dimensions": st.session_state.pca.get("n_components_used", "N/A"),
            })

            table_data.append({
                "Model": "SVM",
                "Type": "Δ Change",
                "Accuracy": f"{delta_acc:+.4f} ({delta_acc*100:+.2f}%)",
                "Training Time (s)": f"{delta_time:+.2f}s",
                "Dimensions": "-",
            })

    # ANN rows
    if has_ann_original:
        ann_original_metrics = st.session_state.ann.get("best_metrics", {})
        ann_original_acc = ann_original_metrics.get(
            "Accuracy", ann_original_metrics.get("CV Accuracy", 0)
        )
        ann_original_time = st.session_state.ann.get("best_params", {}).get("training_time", 0)

        table_data.append({
            "Model": "ANN",
            "Type": "Original",
            "Accuracy": f"{ann_original_acc:.4f}",
            "Training Time (s)": f"{ann_original_time:.2f}",
            "Dimensions": st.session_state.pca.get("X_scaled", np.array([])).shape[1] 
                if len(st.session_state.pca.get("X_scaled", [])) > 0 else "N/A",
        })

        if has_ann_pca:
            ann_pca_metrics = st.session_state.pca.get("ann_pca_metrics", {})
            ann_pca_acc = ann_pca_metrics.get("Accuracy", 0)
            ann_pca_time = st.session_state.pca.get("ann_pca_training_time", 0)
            delta_acc = ann_pca_acc - ann_original_acc
            delta_time = ann_pca_time - ann_original_time

            table_data.append({
                "Model": "ANN",
                "Type": "PCA",
                "Accuracy": f"{ann_pca_acc:.4f}",
                "Training Time (s)": f"{ann_pca_time:.2f}",
                "Dimensions": st.session_state.pca.get("n_components_used", "N/A"),
            })

            table_data.append({
                "Model": "ANN",
                "Type": "Δ Change",
                "Accuracy": f"{delta_acc:+.4f} ({delta_acc*100:+.2f}%)",
                "Training Time (s)": f"{delta_time:+.2f}s",
                "Dimensions": "-",
            })

    # Display table
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # PCA variance info
    if st.session_state.pca.get("explained_variance_ratio") is not None:
        cumulative_var = st.session_state.pca["cumulative_variance"][-1]
        n_components = st.session_state.pca.get("n_components_used", 0)
        
        st.caption(
            f"💡 **PCA Info:** Using **{n_components}** components, "
            f"retaining **{cumulative_var*100:.2f}%** of total variance."
        )


def _render_radar_chart(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Render radar chart comparing metrics"""
    st.markdown("#### 🎯 Multi-Metric Radar Comparison")

    # Collect data for radar chart
    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
    
    # Prepare data
    data_dict = {}

    if has_svm_original:
        svm_original_metrics = st.session_state.svm.get("best_metrics", {})
        data_dict["SVM Original"] = [
            svm_original_metrics.get("Accuracy", svm_original_metrics.get("CV Accuracy", 0)),
            svm_original_metrics.get("Precision", svm_original_metrics.get("CV Precision", 0)),
            svm_original_metrics.get("Recall", svm_original_metrics.get("CV Recall", 0)),
            svm_original_metrics.get("F1-Score", svm_original_metrics.get("CV F1-Score", 0)),
        ]

    if has_svm_pca:
        svm_pca_metrics = st.session_state.pca.get("svm_pca_metrics", {})
        data_dict["SVM PCA"] = [
            svm_pca_metrics.get("Accuracy", 0),
            svm_pca_metrics.get("Precision", 0),
            svm_pca_metrics.get("Recall", 0),
            svm_pca_metrics.get("F1-Score", 0),
        ]

    if has_ann_original:
        ann_original_metrics = st.session_state.ann.get("best_metrics", {})
        data_dict["ANN Original"] = [
            ann_original_metrics.get("Accuracy", ann_original_metrics.get("CV Accuracy", 0)),
            ann_original_metrics.get("Precision", ann_original_metrics.get("CV Precision", 0)),
            ann_original_metrics.get("Recall", ann_original_metrics.get("CV Recall", 0)),
            ann_original_metrics.get("F1-Score", ann_original_metrics.get("CV F1-Score", 0)),
        ]

    if has_ann_pca:
        ann_pca_metrics = st.session_state.pca.get("ann_pca_metrics", {})
        data_dict["ANN PCA"] = [
            ann_pca_metrics.get("Accuracy", 0),
            ann_pca_metrics.get("Precision", 0),
            ann_pca_metrics.get("Recall", 0),
            ann_pca_metrics.get("F1-Score", 0),
        ]

    # Plot radar chart
    _plot_radar_chart(metrics_names, data_dict)


def _plot_radar_chart(categories, data_dict):
    """
    Plot radar chart
    
    Args:
        categories: List of metric names
        data_dict: Dictionary mapping model names to metric values
    """
    # Number of variables
    num_vars = len(categories)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

    # Colors for different models
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Plot each model
    for idx, (model_name, values) in enumerate(data_dict.items()):
        values += values[:1]  # Complete the circle
        ax.plot(angles, values, 'o-', linewidth=2, label=model_name, color=colors[idx % len(colors)])
        ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])

    # Fix axis to go in the right order
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=11)

    # Set y-axis limits
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], size=9)

    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)

    # Title
    ax.set_title("Model Performance Comparison", size=13, fontweight='bold', pad=20)

    plt.tight_layout()
    st.pyplot(fig)

    st.caption(
        "💡 **Radar Chart:** Larger area = better overall performance. "
        "Compare shapes to see which model excels at different metrics."
    )


def _render_insights(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Generate and render insights based on results"""
    st.markdown("#### 💡 Automated Insights & Recommendations")

    insights = []

    # PCA variance insight
    if st.session_state.pca.get("explained_variance_ratio") is not None:
        cumulative_var = st.session_state.pca["cumulative_variance"][-1]
        n_components = st.session_state.pca.get("n_components_used", 0)
        original_dims = st.session_state.pca.get("X_scaled", np.array([])).shape[1]
        
        dim_reduction = ((original_dims - n_components) / original_dims) * 100 if original_dims > 0 else 0
        
        insights.append(
            f"📉 **Dimensionality Reduction:** Reduced from **{original_dims}** to **{n_components}** "
            f"features ({dim_reduction:.1f}% reduction), retaining **{cumulative_var*100:.2f}%** of variance."
        )

    # SVM insights
    if has_svm_original and has_svm_pca:
        svm_original_acc = st.session_state.svm["best_metrics"].get(
            "Accuracy", st.session_state.svm["best_metrics"].get("CV Accuracy", 0)
        )
        svm_pca_acc = st.session_state.pca["svm_pca_metrics"]["Accuracy"]
        delta_acc = svm_pca_acc - svm_original_acc

        svm_original_time = st.session_state.svm["best_params"].get("training_time", 0)
        svm_pca_time = st.session_state.pca["svm_pca_training_time"]
        
        if delta_acc > 0.01:
            insights.append(
                f"✅ **SVM Improved:** PCA **improved** SVM accuracy by **{delta_acc*100:.2f}%** "
                f"(from {svm_original_acc:.4f} to {svm_pca_acc:.4f}). "
                f"Dimensionality reduction helped eliminate noise and improved generalization."
            )
        elif delta_acc < -0.01:
            insights.append(
                f"⚠️ **SVM Degraded:** PCA **reduced** SVM accuracy by **{abs(delta_acc)*100:.2f}%** "
                f"(from {svm_original_acc:.4f} to {svm_pca_acc:.4f}). "
                f"Some discriminative features may have been lost in transformation."
            )
        else:
            insights.append(
                f"➡️ **SVM Unchanged:** PCA had **minimal impact** on SVM accuracy "
                f"(Δ{delta_acc*100:.2f}%). Performance remained consistent."
            )

        # Training time insight
        if svm_pca_time < svm_original_time:
            time_reduction = ((svm_original_time - svm_pca_time) / svm_original_time) * 100
            insights.append(
                f"⚡ **SVM Training Speed:** PCA **reduced** training time by **{time_reduction:.1f}%** "
                f"({svm_original_time:.2f}s → {svm_pca_time:.2f}s). Fewer dimensions = faster training!"
            )

    # ANN insights
    if has_ann_original and has_ann_pca:
        ann_original_acc = st.session_state.ann["best_metrics"].get(
            "Accuracy", st.session_state.ann["best_metrics"].get("CV Accuracy", 0)
        )
        ann_pca_acc = st.session_state.pca["ann_pca_metrics"]["Accuracy"]
        delta_acc = ann_pca_acc - ann_original_acc

        ann_original_time = st.session_state.ann["best_params"].get("training_time", 0)
        ann_pca_time = st.session_state.pca["ann_pca_training_time"]
        
        if delta_acc > 0.01:
            insights.append(
                f"✅ **ANN Improved:** PCA **improved** ANN accuracy by **{delta_acc*100:.2f}%** "
                f"(from {ann_original_acc:.4f} to {ann_pca_acc:.4f}). "
                f"Reduced overfitting risk with fewer parameters."
            )
        elif delta_acc < -0.01:
            insights.append(
                f"⚠️ **ANN Degraded:** PCA **reduced** ANN accuracy by **{abs(delta_acc)*100:.2f}%** "
                f"(from {ann_original_acc:.4f} to {ann_pca_acc:.4f}). "
                f"Neural networks may benefit from raw features in this dataset."
            )
        else:
            insights.append(
                f"➡️ **ANN Unchanged:** PCA had **minimal impact** on ANN accuracy "
                f"(Δ{delta_acc*100:.2f}%). Performance remained stable."
            )

        # Training time insight
        if ann_pca_time < ann_original_time:
            time_reduction = ((ann_original_time - ann_pca_time) / ann_original_time) * 100
            insights.append(
                f"⚡ **ANN Training Speed:** PCA **reduced** training time by **{time_reduction:.1f}%** "
                f"({ann_original_time:.2f}s → {ann_pca_time:.2f}s)."
            )

    # Best model recommendation
    best_model, best_acc = _get_best_model(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)
    if best_model:
        insights.append(
            f"🏆 **Best Model:** **{best_model}** achieved the highest accuracy of **{best_acc:.4f}**."
        )

    # Display insights
    for insight in insights:
        st.markdown(insight)

    st.divider()

    # Final recommendation
    st.markdown("#### 🎯 Final Recommendation for YOUR Dataset")
    _render_final_recommendation(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)


def _get_best_model(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Determine the best performing model"""
    best_model = None
    best_acc = 0

    if has_svm_original:
        acc = st.session_state.svm["best_metrics"].get(
            "Accuracy", st.session_state.svm["best_metrics"].get("CV Accuracy", 0)
        )
        if acc > best_acc:
            best_acc = acc
            best_model = "SVM (Original)"

    if has_svm_pca:
        acc = st.session_state.pca["svm_pca_metrics"]["Accuracy"]
        if acc > best_acc:
            best_acc = acc
            best_model = "SVM (PCA)"

    if has_ann_original:
        acc = st.session_state.ann["best_metrics"].get(
            "Accuracy", st.session_state.ann["best_metrics"].get("CV Accuracy", 0)
        )
        if acc > best_acc:
            best_acc = acc
            best_model = "ANN (Original)"

    if has_ann_pca:
        acc = st.session_state.pca["ann_pca_metrics"]["Accuracy"]
        if acc > best_acc:
            best_acc = acc
            best_model = "ANN (PCA)"

    return best_model, best_acc


def _render_final_recommendation(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Render final recommendation"""
    
    # Determine if PCA helps
    pca_helps_svm = False
    pca_helps_ann = False

    if has_svm_original and has_svm_pca:
        svm_original_acc = st.session_state.svm["best_metrics"].get(
            "Accuracy", st.session_state.svm["best_metrics"].get("CV Accuracy", 0)
        )
        svm_pca_acc = st.session_state.pca["svm_pca_metrics"]["Accuracy"]
        pca_helps_svm = svm_pca_acc > svm_original_acc

    if has_ann_original and has_ann_pca:
        ann_original_acc = st.session_state.ann["best_metrics"].get(
            "Accuracy", st.session_state.ann["best_metrics"].get("CV Accuracy", 0)
        )
        ann_pca_acc = st.session_state.pca["ann_pca_metrics"]["Accuracy"]
        pca_helps_ann = ann_pca_acc > ann_original_acc

    # Generate recommendation
    if pca_helps_svm and pca_helps_ann:
        st.success(
            "✅ **USE PCA!** PCA improved performance for **both** SVM and ANN on your dataset. "
            "Benefits: Faster training, reduced overfitting, better generalization."
        )
    elif pca_helps_svm or pca_helps_ann:
        model_name = "SVM" if pca_helps_svm else "ANN"
        st.info(
            f"⚖️ **CONDITIONAL USE:** PCA helped **{model_name}** but not the other model. "
            f"Use PCA specifically for {model_name} deployment."
        )
    else:
        st.warning(
            "❌ **AVOID PCA:** PCA did not improve (or degraded) performance on your dataset. "
            "Your features are already informative. Stick with original feature space."
        )


def _render_export_options(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Render export options for results"""
    st.markdown("#### 💾 Export Results")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Export to CSV", width="stretch"):
            csv = _generate_csv(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="pca_comparison_results.csv",
                mime="text/csv",
            )

    with col2:
        if st.button("📄 Generate Report", width="stretch"):
            st.info("📝 Report generation feature coming soon!")

    # Show experiment history
    render_experiment_history()


def _generate_csv(has_svm_original, has_svm_pca, has_ann_original, has_ann_pca):
    """Generate CSV export of results"""
    data = []

    # SVM data
    if has_svm_original:
        svm_metrics = st.session_state.svm["best_metrics"]
        data.append({
            "Model": "SVM",
            "Type": "Original",
            "Accuracy": svm_metrics.get("Accuracy", svm_metrics.get("CV Accuracy", 0)),
            "Precision": svm_metrics.get("Precision", svm_metrics.get("CV Precision", 0)),
            "Recall": svm_metrics.get("Recall", svm_metrics.get("CV Recall", 0)),
            "F1-Score": svm_metrics.get("F1-Score", svm_metrics.get("CV F1-Score", 0)),
        })

    if has_svm_pca:
        svm_pca_metrics = st.session_state.pca["svm_pca_metrics"]
        data.append({
            "Model": "SVM",
            "Type": "PCA",
            "Accuracy": svm_pca_metrics["Accuracy"],
            "Precision": svm_pca_metrics["Precision"],
            "Recall": svm_pca_metrics["Recall"],
            "F1-Score": svm_pca_metrics["F1-Score"],
        })

    # ANN data
    if has_ann_original:
        ann_metrics = st.session_state.ann["best_metrics"]
        data.append({
            "Model": "ANN",
            "Type": "Original",
            "Accuracy": ann_metrics.get("Accuracy", ann_metrics.get("CV Accuracy", 0)),
            "Precision": ann_metrics.get("Precision", ann_metrics.get("CV Precision", 0)),
            "Recall": ann_metrics.get("Recall", ann_metrics.get("CV Recall", 0)),
            "F1-Score": ann_metrics.get("F1-Score", ann_metrics.get("CV F1-Score", 0)),
        })

    if has_ann_pca:
        ann_pca_metrics = st.session_state.pca["ann_pca_metrics"]
        data.append({
            "Model": "ANN",
            "Type": "PCA",
            "Accuracy": ann_pca_metrics["Accuracy"],
            "Precision": ann_pca_metrics["Precision"],
            "Recall": ann_pca_metrics["Recall"],
            "F1-Score": ann_pca_metrics["F1-Score"],
        })

    df = pd.DataFrame(data)
    return df.to_csv(index=False)

