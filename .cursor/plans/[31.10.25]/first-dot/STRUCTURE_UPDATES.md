# Structure Updates - November 1, 2025

## Folder Renaming

| Old Name | New Name | Reason |
|----------|----------|--------|
| `/logic` | `/core` | Better describes business logic layer |
| `/experiments` | `/sandbox` | Clearer purpose for temporary/experimental data |

## File Organization

### Data Files
- Moved to: `/data/source/`
  - `student-mat.csv`
  - `student-por.csv`

### Tests
- Moved to: `/.tests/`
  - `test_data_layer.py`

## Updated Architecture

```
.jorge/partials/third/
├── data/
│   ├── source/              # CSV files
│   ├── loader.py            # ✅ Updated paths
│   ├── validator.py
│   ├── transformer.py
│   ├── preprocessor.py
│   └── balancer.py
│
├── core/                    # ML algorithms (was /logic)
│   └── (Phase 1)
│
├── versioning/              # Experiment tracking
│   └── (Phase 4)
│
├── ui/                      # Streamlit UI
│   ├── patterns/
│   ├── pages/
│   └── (Phase 5)
│
├── sandbox/                 # Experiments (was /experiments)
│   ├── decision_tree/
│   ├── hierarchical/
│   ├── kmeans/
│   └── snapshots/
│
├── .tests/                  # Test files
│   └── test_data_layer.py
│
├── notebooks/
│   └── deliverable.ipynb
│
├── app.py                   # ✅ Streamlit entry point
└── README.md
```

## Code Changes Made

### 1. loader.py
```python
# OLD:
DATA_DIR = Path(__file__).parent.parent / "data"
output_dir = DATA_DIR.parent / "experiments" / "snapshots"

# NEW:
DATA_DIR = Path(__file__).parent / "source"
output_dir = DATA_DIR.parent.parent / "sandbox" / "snapshots"
```

### 2. app.py
- Created from scratch
- Streamlit entry point
- Welcome page with navigation

## Implementation Checklist

- [x] Create `/core` folder
- [x] Create `/sandbox` folder structure
- [x] Update `loader.py` paths
- [x] Create `app.py` entry point
- [x] Create folder structure for sandbox experiments
- [ ] Update plan documents (Phase 1 onwards)
- [ ] Update execution log

## Next Phase Requirements

When implementing Phase 1 (Core Layer):
- All files go in `/core/` (not `/logic/`)
- Experiments save to `/sandbox/` (not `/experiments/`)
- Follow same patterns as data layer

## Running the Application

```bash
# Test data layer
python3 .tests/test_data_layer.py

# Run Streamlit app
streamlit run app.py
```

---

**Status**: Structure updated and ready for Phase 1 implementation


