# Streamlit Cloud Deployment Guide

## ✅ Fixed Issues (2025-10-12)

### 1. **FileNotFoundError - Data Path Issue** ✅ FIXED
**Problem**: Relative paths `"data/bank.csv"` don't work on Streamlit Cloud

**Solution**: Updated `settings/config.py` to use absolute paths:
```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CONF = {
    Keys.DATASET_PATH_FULL: str(DATA_DIR / "bank-full.csv"),
    Keys.DATASET_PATH_SMALL: str(DATA_DIR / "bank.csv"),
}
```

### 2. **Cache Directory Path Issue** ✅ FIXED
**Problem**: `.cache/` relative path might not work on cloud

**Solution**: Updated `ui/pages/pca/experiments.py` to use absolute paths:
```python
CACHE_DIR = Path(__file__).resolve().parent.parent.parent.parent / ".cache"
CACHE_FILE = CACHE_DIR / "pca_experiments.json"
```

### 3. **Confusion Matrix Display Error** ✅ FIXED
**Problem**: `plot_confusion_matrix()` got unexpected `figsize` argument

**Solution**: Updated `pca/components/model_comparison.py`:
- Pass `y_true` and `y_pred` instead of pre-computed matrix
- Removed unsupported `figsize` parameter

---

## 📋 Deployment Checklist

### Required Files in Repository:
- ✅ `app.py` (main entry point)
- ✅ `data/bank.csv` and `data/bank-full.csv` (datasets)
- ✅ All Python files in `settings/`, `ui/`, `funcs/`
- ✅ `requirements.txt` or `pyproject.toml` (dependencies)

### Streamlit Cloud Settings:
```
Main file path: .jorge/partials/second/app.py
Python version: 3.12
Branch: main
```

### Environment Requirements:
```
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.11.0
plotly>=5.17.0  # Optional, for 3D plots
```

---

## 🚀 Deployment Steps

### Option 1: Deploy from Main Branch (Recommended)
1. **Push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Fix: Streamlit Cloud path issues (data files + cache)"
   git push origin main
   ```

2. **On Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository
   - Main file path: `.jorge/partials/second/app.py`
   - Branch: `main`
   - Click "Deploy"

### Option 2: Test Locally First
```bash
cd .jorge/partials/second
streamlit run app.py
```

If it works locally with the new paths, it should work on cloud!

---

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure all dependencies are in `requirements.txt`

### Issue: "Data file not found"
**Check**: 
1. `data/` folder is committed to git
2. CSV files are in the repository (not gitignored)
3. File names match exactly: `bank.csv` and `bank-full.csv`

### Issue: Cache directory errors
**Fix**: The code now creates `.cache/` automatically with:
```python
CACHE_DIR.mkdir(exist_ok=True, parents=True)
```

### Issue: Import errors
**Check**: All modules can be found with:
```python
import sys
print(sys.path)
```

---

## 📊 Expected Behavior

### On First Load:
1. ✅ Data loads from `data/bank.csv`
2. ✅ Config tab shows dataset info
3. ✅ SVM/ANN/PCA tabs are accessible
4. ✅ No file path errors

### During Usage:
1. ✅ Train models in SVM/ANN tabs
2. ✅ Save best models
3. ✅ Navigate to PCA tab
4. ✅ Apply PCA transformation
5. ✅ Compare models BEFORE/AFTER
6. ✅ Export results to CSV

### File System:
- `.cache/` directory auto-created
- Experiment history saved correctly
- No permission errors

---

## ✅ Verification Tests

Run these after deployment:

### Test 1: Data Loading
```python
# Should work without errors
from settings.config import CONF, Keys
import pandas as pd

df = pd.read_csv(CONF[Keys.DATASET_PATH_SMALL], delimiter=';')
print(f"Loaded {len(df)} rows")  # Should show ~4500
```

### Test 2: Path Resolution
```python
from pathlib import Path
from settings.config import DATA_DIR

print(f"Data directory: {DATA_DIR}")
print(f"Exists: {DATA_DIR.exists()}")
print(f"Files: {list(DATA_DIR.glob('*.csv'))}")
```

### Test 3: Cache Creation
```python
from ui.pages.pca.experiments import CACHE_DIR

CACHE_DIR.mkdir(exist_ok=True, parents=True)
print(f"Cache directory: {CACHE_DIR}")
print(f"Exists: {CACHE_DIR.exists()}")
```

---

## 🎉 Success Indicators

✅ App loads without errors
✅ Dataset statistics show in Config section
✅ All tabs are accessible
✅ No "FileNotFoundError" messages
✅ Models can be trained
✅ PCA comparison works
✅ Confusion matrices display correctly
✅ Export CSV works

---

## 📝 Notes

- **Absolute paths**: All file paths now use `Path(__file__).resolve()` for portability
- **Cross-platform**: Works on Windows, Linux, Mac, and Streamlit Cloud
- **Auto-creation**: Directories created automatically if missing
- **No hardcoded paths**: Everything relative to file locations

---

**Last Updated**: October 12, 2025
**Status**: ✅ Ready for Deployment
**Tested**: Local ✅ | Cloud ⏳ (awaiting your test)

