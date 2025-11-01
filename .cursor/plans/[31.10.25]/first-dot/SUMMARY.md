# Architecture Plan Summary - Student Performance Analysis

## 🎯 Core Vision

Build a **modular, reusable ML application** where:
- ✅ Clean layer separation (Data | Logic | Versioning | UI)
- ✅ 70%+ code reuse across tabs (template + content slots)
- ✅ Proper experiment version control (not just .cache)
- ✅ Timeline-based progress tracking
- ✅ Cross-domain validation (Math → Portuguese)

---

## 📊 Key Enhancements vs. Previous Implementation

### 1. Dataset Review Tab (NEW)
**Why**: Understand and prepare data BEFORE training
- Balance classes (SMOTE, Random Over/Under)
- Visualize class distributions (before/after)
- Engineer target variable (G3 → categorical)
- Remove leakage features (G1, G2)
- Create dataset snapshots

### 2. Versioning Layer (NEW)
**Why**: Track progress systematically, not ad-hoc
- Experiment store (JSON metadata + pickle models)
- Timeline manager (chronological ordering, filtering)
- Comparison engine (multi-experiment analysis)
- Version ID generator (sortable, unique)

### 3. Timeline Visualization (NEW)
**Why**: See how metrics evolved over time
- Matplotlib line charts (metric evolution)
- Experiment markers (clickable points)
- Comparison views (side-by-side)
- Best model highlighting

### 4. Cross-Dataset Strategy (NEW)
**Why**: Test real-world generalization
- Train: Math dataset (395 students)
- Test: Portuguese dataset (649 students)
- Compare: Train vs test metrics
- Reflect: What generalizes, what doesn't

### 5. State Management (ENHANCED)
**Why**: Predictable, centralized state handling
- Session state (rerun-safe)
- Local state (widget-level)
- Persistent state (survives restarts)
- Cross-page data sharing

---

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────┐
│           UI LAYER                      │
│  - Pages (extend template)              │
│  - Patterns (reusable components)       │
│  - State Manager (centralized)          │
└─────────────┬───────────────────────────┘
              │ calls
┌─────────────▼───────────────────────────┐
│      VERSIONING LAYER                   │
│  - Experiment Store                     │
│  - Timeline Manager                     │
│  - Comparison Engine                    │
└─────────────┬───────────────────────────┘
              │ saves/loads
┌─────────────▼───────────────────────────┐
│         LOGIC LAYER                     │
│  - Decision Trees                       │
│  - Clustering (Hierarchical, K-means)   │
│  - Analysis & Evaluation                │
└─────────────┬───────────────────────────┘
              │ uses
┌─────────────▼───────────────────────────┐
│          DATA LAYER                     │
│  - Loader (Math/Portuguese)             │
│  - Validator (cross-dataset checks)     │
│  - Transformer (preprocessing)          │
│  - Balancer (SMOTE, etc.)               │
└─────────────────────────────────────────┘
```

---

## 📁 File Structure

```
.jorge/partials/third/
├── data/
│   ├── loader.py              # Load Math/Portuguese datasets
│   ├── validator.py           # Cross-dataset validation
│   ├── transformer.py         # Preprocessing, target engineering
│   └── balancer.py            # SMOTE, random sampling
│
├── logic/
│   ├── decision_tree.py       # CART, rule extraction
│   ├── clustering.py          # Hierarchical + K-means
│   ├── analysis.py            # Rule ranking, optimal k
│   └── evaluation.py          # J4 criterion, metrics
│
├── versioning/
│   ├── experiment_store.py    # Persist/retrieve experiments
│   ├── timeline_manager.py    # Chronological history
│   ├── comparison_engine.py   # Multi-experiment comparison
│   └── version_id_gen.py      # Unique ID generation
│
├── ui/
│   ├── patterns/
│   │   ├── layouts.py         # TwoColumn, Tabs, Grid
│   │   ├── controls.py        # Sliders, Selects, Buttons
│   │   └── displays.py        # MetricCard, Table, PlotContainer
│   │
│   ├── pages/
│   │   ├── template.py        # Abstract PageTemplate
│   │   ├── dataset_review.py  # 🆕 Data exploration & balancing
│   │   ├── decision_tree.py   # Extends template
│   │   ├── hierarchical.py    # Extends template
│   │   ├── kmeans.py          # Extends template
│   │   └── history.py         # 🆕 Timeline & comparison
│   │
│   ├── orchestrator.py        # Wire layers together
│   ├── state_manager.py       # 🆕 Centralized state
│   └── app.py                 # Main entry point
│
├── notebooks/
│   └── deliverable.ipynb      # Final submission
│
└── experiments/               # 🆕 Structured versioning (not .cache)
    ├── decision_tree/
    ├── hierarchical/
    └── kmeans/
```

---

## 🔄 Reusability Pattern

**CONSTANT (Reused 70%+):**
- Layout structure (TwoColumn, Tabs)
- Interaction flow (button → train → display)
- State management patterns
- Data pipeline (load → validate → transform)
- Experiment tracking (save → load → compare)

**VARIABLE (Swapped per tab):**
- Parameter widgets (specific to algorithm)
- Visualizations (tree plot vs dendrogram vs scatter)
- Metrics displayed (classification vs clustering)
- Logic functions called (decision_tree vs clustering)

**Result**: Adding Task 4 requires ~100 LOC (logic + content only)

---

## 🚀 Implementation Phases

1. **Contracts** - Define all interfaces
2. **Data Layer** - Load, validate, transform, balance
3. **Logic Layer** - Implement algorithms
4. **Versioning Layer** - Experiment tracking
5. **UI Patterns** - Reusable components + template
6. **Dataset Review Tab** - Data exploration
7. **Algorithm Tabs** - Decision Tree, Hierarchical, K-means
8. **History Tab** - Timeline & comparison
9. **Cross-Dataset Validation** - Math → Portuguese
10. **Notebook Export** - Generate deliverable

---

## ✅ Validation Criteria

- [ ] Logic layer: No UI imports, no file I/O
- [ ] Data layer: No algorithms, no display code
- [ ] Versioning layer: No UI, no algorithms
- [ ] UI layer: No algorithm implementation
- [ ] Each layer independently testable
- [ ] PageTemplate reused by all 5 pages
- [ ] Dataset Review tab: Balance classes + visualize
- [ ] Experiment timeline: Matplotlib chart showing metric evolution
- [ ] Comparison tool: Side-by-side experiment comparison
- [ ] Cross-dataset validation: Train Math, test Portuguese
- [ ] State management: Session state + persistent storage
- [ ] Adding task 4 would require <100 new LOC
- [ ] All files < 300 LOC
- [ ] Jupyter notebook exports cleanly

---

## 🎓 Cross-Domain Philosophy

> **"Leap of Faith" Validation**
> 
> Train on Math (395 samples) → Test on Portuguese (649 samples)
> 
> **Questions to Answer:**
> - Do patterns learned from Math students generalize to Portuguese students?
> - Which student characteristics are universal vs subject-specific?
> - How does class distribution mismatch affect performance?
> - What can we learn about model robustness?

---

## 🧠 State Management Strategy

**Session State** (rerun-safe)
- Trained models
- Current experiment results
- Dataset versions
- User configurations

**Local State** (widget-level)
- Form inputs
- Temporary selections
- UI-only values

**Persistent State** (survives restarts)
- Experiment history
- Best models
- User preferences
- Timeline data

---

## 📈 Timeline Visualization Features

**Experiment Table:**
- Sortable by all columns
- Filterable by date range, metrics
- Highlight best experiment
- Actions: load, compare, delete

**Timeline Chart:**
- X-axis: Timestamp (chronological)
- Y-axis: Metric value
- Lines: One per metric (Accuracy, F1, etc.)
- Markers: Clickable experiment points

**Comparison View:**
- Select up to 5 experiments
- Parameter diff table
- Metric comparison bars
- Improvement percentages

---

## 🔧 Tech Stack

- **UI Framework**: Streamlit (proven, fast prototyping)
- **ML Libraries**: scikit-learn, imbalanced-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Data**: Pandas, NumPy
- **Storage**: JSON (metadata) + Pickle (models)

---

## 📝 Next Steps

1. Review plan and execution structure
2. Start with Phase 1: Define contracts
3. Implement phases sequentially
4. Test each layer independently
5. Integrate layers progressively
6. Export to Jupyter notebook
7. Prepare oral presentation

**Current Status**: ✅ Architecture defined, ready for execution
**Next Action**: Start `A1.exec.md` Phase 1

