# Streamlit Import Resolution & Module Structure

## The Problem

Streamlit runs files in a specific execution context that differs from normal Python. When running `streamlit run folder/app.py`, module imports may fail even if files exist.

## Root Cause

**Framework Context Blindness**: Assuming Python import rules work the same way under Streamlit as they do in normal Python execution.

### Three Layers of Import Resolution

1. **Code Layer**: What imports you write
2. **Framework Layer**: How Streamlit resolves them
3. **Runtime Layer**: Where Python finds modules (sys.path)

## Common Error

```python
# In ui/app.py
from config import CONF  # ❌ ModuleNotFoundError
```

**Why it fails**:
- Streamlit sets working directory to where app.py is located
- Python looks in `ui/` directory for `config` module
- `config.py` is at project root
- Result: ModuleNotFoundError

## Solutions

### Solution 1: sys.path Manipulation (Recommended)

```python
# ui/app.py - ADD THIS BEFORE ANY LOCAL IMPORTS
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now imports work
import streamlit as st
from config import CONF
from ui.pages import svm_page
```

**✅ Order matters**: sys.path manipulation MUST come BEFORE local imports

### Solution 2: Relative Imports + __init__.py

```python
# Structure:
# project/
#   __init__.py        # Make it a package
#   ui/
#     __init__.py
#     app.py
#   config.py

# In ui/app.py
from ..config import CONF  # Relative import
```

**⚠️ Limitation**: Requires running from parent directory

### Solution 3: PYTHONPATH Environment Variable

```bash
# PowerShell
$env:PYTHONPATH = "C:\path\to\project"
streamlit run ui/app.py

# Bash
PYTHONPATH=/path/to/project streamlit run ui/app.py
```

**⚠️ Not portable**: Different for each developer

## Best Practice Checklist

Before creating nested Streamlit structures:

1. **IMPORT_TRACE**: Map out where Python will search for modules
2. **ENVIRONMENT_CHECK**: Verify Streamlit's execution context
3. **TEST_EXECUTION**: Run actual command, wait for output
4. **VALIDATE**: Confirm no ModuleNotFoundError before moving on

## Pattern to Follow

```python
# ALWAYS at top of Streamlit entry point
import sys
from pathlib import Path

# Resolve paths FIRST
project_root = Path(__file__).parent.parent  # or however many .parent needed
sys.path.insert(0, str(project_root))

# THEN do framework imports
import streamlit as st

# FINALLY do local imports
from your_module import your_function
```

## Common Mistake

```python
# ❌ WRONG ORDER
import streamlit as st
from settings.config import CONF  # Tries to import

# Add project root (TOO LATE!)
sys.path.insert(0, str(project_root))
```

The imports execute BEFORE sys.path is modified!

## Key Takeaway

**Streamlit execution context ≠ Normal Python execution**

Always verify import resolution for framework-specific execution. Don't assume "files exist" means "imports will work".

