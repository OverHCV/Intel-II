# Execution: Interactive Streamlit UI for Bank Marketing ML Analysis

## STATUS_POINTER {
  current: "obj['working_prototype']: COMPLETE → Moving to obj['svm_interactive_tab']",
  progress: "✅ All critical bugs fixed, UX improvements applied"
}

## CRITICAL_FIX: Import Resolution Error

**Bug**: `ModuleNotFoundError: No module named 'config'`

**Root Cause**: Streamlit runs ui/app.py but project root not in sys.path

**Solution Applied**:
```python
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

**Lesson**: Should have used IMPORT_TRACE and ENVIRONMENT_CHECK BEFORE creating files

**Updated parlang-guide.md** with:
- New verb: IMPORT_TRACE (Level 2 - trace module resolution)
- New verb: ENVIRONMENT_CHECK (Level 2 - verify runtime context)  
- New failure pattern: Framework Context Blindness
- Updated Three Layers Rule to include execution context
- Added to Golden Rules: Never create nested structures without IMPORT_TRACE

**Analysis documented in**: `.cursor/plans/[11.10.25]/1/.analysis.md`

---

## CRITICAL_FIX 2: Namespace Collision

**Bug #2**: File `ui/pages/config.py` already renamed to `conf.py`, imports already updated correctly

**Root Cause**: Namespace collision with root `config.py` - user renamed file but I didn't proactively check for collisions

**Lesson**: Should have used NAMESPACE_CHECK BEFORE creating file to avoid collision from start

**Updated parlang-guide.md** with:
- New verb: NAMESPACE_CHECK (Level 2 - detect identifier collisions)
- New verb: DEPENDENCY_TRACE (Level 2 - track what depends on a module)
- New verb: POST_CHANGE_VALIDATION (Level 2 - verify system coherence after changes)
- New failure pattern: Namespace Collision & Incomplete Refactoring
- Added to Golden Rules: Never create files without NAMESPACE_CHECK

**Analysis documented in**: `.cursor/plans/[11.10.25]/1/.analysis.md`

**Current state**: Imports are correct (using `.conf`), ready to test app

## IMPLEMENT obj["ui_architecture"] IN(@config.py, @settings/, @funcs/) OUT(@ui/, folder_structure) {

  UNDERSTAND IN(@config.py, @settings/imports.py) OUT(current_structure) {
    current_files: [
      "config.py - CONF dict with Keys",
      "settings/feats.py - BankFeatures, BankTarget",
      "settings/options.py - SVMKernel, ANNActivation, ANNSolver",
      "settings/imports.py - All imports",
      "funcs/evaluator.py - k-fold CV"
    ],
    streamlit_status: "INSTALLED (user confirmed)",
    need_to_create: [
      "ui/ folder with React-like component structure",
      "funcs/visualizers.py for plotting",
      "ui/utils/data_loader.py for preprocessing"
    ]
  }

  CREATE IN(current_structure) OUT(@ui/, @funcs/visualizers.py) {
    
    folders: [
      "ui/",
      "ui/components/",
      "ui/pages/",
      "ui/utils/"
    ],
    
    files: [
      "ui/app.py",
      "ui/components/__init__.py",
      "ui/components/tabs.py",
      "ui/components/panels.py", 
      "ui/components/sliders.py",
      "ui/components/metrics.py",
      "ui/pages/__init__.py",
      "ui/pages/config.py",
      "ui/pages/svm.py",
      "ui/pages/ann.py",
      "ui/pages/pca.py",
      "ui/utils/__init__.py",
      "ui/utils/data_loader.py",
      "ui/utils/state_manager.py",
      "funcs/visualizers.py"
    ],
    
    why: "Modular React-like structure for maintainability"
  }

  COMPLETED: obj["ui_architecture"]
}

## IMPLEMENT obj["data_loader"] IN(@config.py, @data/bank.csv) OUT(@ui/utils/data_loader.py) {

  CREATE IN(@config.py, @settings/imports.py) OUT(@ui/utils/data_loader.py) {
    
    function: "load_and_preprocess_data",
    params: {
      use_full_dataset: "bool (from UI toggle)",
      use_categorical: "bool (start with False, add selector later)",
      random_state: "from CONF[Keys.RANDOM_STATE]"
    },
    returns: {
      X_scaled: "StandardScaler transformed features",
      y: "encoded labels",
      feature_names: "list of feature names",
      dataset_info: "dict with shape, classes, etc"
    },
    why: "Centralized preprocessing for all tabs"
  }

  VALIDATE IN(@ui/utils/data_loader.py) OUT(validation_result) {
    test: "Load both datasets, verify shapes",
    check: "Scaling applied correctly",
    check: "Labels encoded properly"
  }

  COMPLETED: obj["data_loader"]
}

## IMPLEMENT obj["visualization_functions"] IN(@settings/imports.py) OUT(@funcs/visualizers.py) {

  CREATE IN(@settings/imports.py) OUT(@funcs/visualizers.py) {
    
    functions: [
      {
        name: "plot_confusion_matrix",
        params: "y_true, y_pred, labels",
        returns: "matplotlib Figure",
        why: "Reusable confusion matrix for all models"
      },
      {
        name: "plot_metrics_bars",
        params: "metrics_dict",
        returns: "matplotlib Figure",
        why: "Bar chart for accuracy, precision, recall, F1"
      },
      {
        name: "plot_pca_variance",
        params: "pca_object",
        returns: "matplotlib Figure",
        why: "Show explained variance by components"
      },
      {
        name: "plot_learning_curve",
        params: "train_scores, val_scores, param_range",
        returns: "matplotlib Figure",
        why: "Visualize how model improves with hyperparams"
      }
    ],
    
    style: "Use config.CONF for figure sizes and colors",
    why: "Keep visualizations consistent across tabs"
  }

  COMPLETED: obj["visualization_functions"]
}

## IMPLEMENT obj["base_layout"] IN(@ui/) OUT(@ui/app.py, @ui/components/) {

  CREATE IN(@config.py) OUT(@ui/components/tabs.py) {
    component: "TabNavigator",
    props: {
      tabs: "['Config', 'SVM', 'ANN', 'PCA']",
      icons: "optional emoji icons"
    },
    behavior: "st.tabs() wrapper with consistent styling",
    why: "Reusable tab component like React"
  }

  CREATE IN() OUT(@ui/components/panels.py) {
    component: "TwoColumnLayout",
    props: {
      left_content: "function or component",
      right_content: "function or component",
      ratio: "[2, 1] default"
    },
    behavior: "st.columns() wrapper with consistent spacing",
    why: "Reusable two-panel layout"
  }

  CREATE IN() OUT(@ui/components/sliders.py) {
    components: [
      "NumericSlider - for C, gamma values",
      "DiscreteSlider - for n_folds (1-10)",
      "Selector - for kernel, activation choices"
    ],
    why: "Consistent UI controls across tabs"
  }

  CREATE IN() OUT(@ui/components/metrics.py) {
    component: "MetricCard",
    props: {
      label: "string",
      value: "number",
      delta: "optional improvement",
      icon: "optional emoji"
    },
    behavior: "st.metric() wrapper with custom styling",
    why: "Consistent metric display"
  }

  CREATE IN(@ui/components/) OUT(@ui/app.py) {
    
    structure: {
      imports: "config, components, pages",
      sidebar: "st.sidebar with app info",
      tabs: "Config, SVM, ANN, PCA",
      state_init: "Initialize session_state",
      layout: "Call page functions based on tab"
    },
    
    why: "Main entry point that orchestrates everything"
  }

  VALIDATE IN(@ui/app.py) OUT(validation_result) {
    test: "streamlit run ui/app.py",
    check: "App loads without errors",
    check: "Tabs render correctly",
    check: "Session state initializes"
  }

  COMPLETED: obj["base_layout"]
}

## IMPLEMENT obj["working_prototype"] IN(@ui/app.py, @ui/pages/) OUT(@ui/pages/config.py, working_demo) {

  CREATE IN(@ui/utils/data_loader.py, @ui/components/) OUT(@ui/pages/config.py) {
    
    content: {
      title: "⚙️ Configuration",
      dataset_toggle: "Small (4.5K) vs Full (45K)",
      features_selector: "Numerical only vs All features (for later)",
      cv_strategy: {
        mode: "Train/Test vs K-Fold",
        n_folds_slider: "1-10 if K-Fold selected"
      },
      preview: "Show dataset shape, feature count, class distribution"
    },
    
    behavior: "Updates st.session_state['config']",
    why: "User controls for global settings"
  }

  VALIDATE IN(@ui/pages/config.py, @ui/app.py) OUT(prototype_result) {
    
    ACCEPTANCE_CRITERIA: [
      "App runs: streamlit run ui/app.py",
      "Config tab shows dataset info",
      "Toggle switches dataset (see shape change)",
      "CV strategy changes via UI",
      "K-folds slider appears when K-Fold selected"
    ],
    
    TEST_SCENARIOS: [
      {
        action: "Toggle dataset small → full",
        expected: "Shape changes from (4521, X) → (45211, X)"
      },
      {
        action: "Change CV strategy to K-Fold",
        expected: "Slider for folds appears (1-10)"
      }
    ]
  }

  COMPLETED: obj["working_prototype"]
}

## IMPLEMENT obj["svm_interactive_tab"] IN(@ui/pages/, @funcs/) OUT(@ui/pages/svm.py) {

  CREATE IN(@ui/components/, @funcs/visualizers.py, @config.py) OUT(@ui/pages/svm.py) {
    
    layout: {
      title: "🔍 Support Vector Machine (SVM)",
      two_columns: {
        left: [
          "Confusion Matrix (live)",
          "Metrics bar chart (Acc, Prec, Rec, F1)",
          "Training time display"
        ],
        right: [
          "Kernel selector (linear, poly, rbf, sigmoid)",
          "C slider (log scale 0.01-100)",
          "Gamma selector (scale, auto, 0.001-1)",
          "Degree slider (if poly kernel, 2-5)",
          "Train button",
          "Metric cards (current results)"
        ]
      }
    },
    
    behavior: {
      on_param_change: "Update UI only",
      on_train_click: {
        get_data: "from data_loader",
        get_cv_config: "from session_state['config']",
        train_model: "SVC with selected params",
        evaluate: "train/test split OR k-fold CV",
        plot_results: "confusion matrix + metrics",
        store_state: "Save model + results for PCA comparison"
      }
    },
    
    why: "Task 1 - Interactive SVM exploration"
  }

  VALIDATE IN(@ui/pages/svm.py) OUT(svm_validation) {
    
    ACCEPTANCE_CRITERIA: [
      "Kernel selector changes options (gamma hidden for linear)",
      "C slider responds (log scale)",
      "Train button triggers model training",
      "Confusion matrix updates after train",
      "Metrics display: accuracy, precision, recall, F1",
      "Results stored in session_state for PCA tab"
    ],
    
    TEST_SCENARIOS: [
      {
        params: "Linear kernel, C=1.0",
        expected: "Fast training (~1s), accuracy displayed"
      },
      {
        params: "RBF kernel, C=10, gamma=0.1, K-Fold CV (k=5)",
        expected: "Slower training (~5-10s), robust metrics"
      }
    ]
  }

  COMPLETED: obj["svm_interactive_tab"]
}

## IMPLEMENT obj["ann_interactive_tab"] IN(@ui/pages/, @funcs/) OUT(@ui/pages/ann.py) {

  CREATE IN(@ui/components/, @funcs/visualizers.py, @config.py) OUT(@ui/pages/ann.py) {
    
    layout: {
      title: "🧠 Artificial Neural Network (ANN)",
      two_columns: {
        left: [
          "Confusion Matrix",
          "Metrics bar chart",
          "Training history (loss/accuracy curves if available)"
        ],
        right: [
          "Architecture selector (from CONF)",
          "Activation selector (relu, tanh, logistic)",
          "Solver selector (adam, sgd, lbfgs)",
          "Max iterations slider",
          "Train button",
          "Metric cards"
        ]
      }
    },
    
    behavior: {
      on_train_click: {
        get_data: "from data_loader",
        get_cv_config: "from session_state['config']",
        train_model: "MLPClassifier with selected params",
        evaluate: "train/test OR k-fold CV",
        plot_results: "confusion matrix + metrics",
        store_state: "Save model + results for PCA"
      }
    },
    
    why: "Task 2 - Interactive ANN exploration"
  }

  COMPLETED: obj["ann_interactive_tab"]
}

## IMPLEMENT obj["pca_interactive_tab"] IN(@ui/pages/, @funcs/) OUT(@ui/pages/pca.py) {

  CREATE IN(@ui/components/, @funcs/visualizers.py) OUT(@ui/pages/pca.py) {
    
    layout: {
      title: "📊 PCA Analysis & Comparison",
      sections: [
        {
          name: "PCA Configuration",
          content: "n_components slider (2-20)"
        },
        {
          name: "Variance Explained",
          content: "Plot showing cumulative variance by component"
        },
        {
          name: "SVM Comparison",
          content: "Side-by-side: Original vs PCA metrics"
        },
        {
          name: "ANN Comparison",
          content: "Side-by-side: Original vs PCA metrics"
        },
        {
          name: "Conclusion",
          content: "Text area for analysis/insights"
        }
      ]
    },
    
    behavior: {
      on_apply_pca: {
        get_data: "from data_loader",
        apply_pca: "PCA(n_components)",
        get_best_svm: "from session_state",
        get_best_ann: "from session_state",
        retrain_svm: "on PCA-transformed data",
        retrain_ann: "on PCA-transformed data",
        compare: "Show before/after metrics",
        plot_variance: "Explained variance chart"
      }
    },
    
    why: "Task 3 - PCA impact analysis"
  }

  VALIDATE IN(@ui/pages/pca.py) OUT(pca_validation) {
    
    ACCEPTANCE_CRITERIA: [
      "n_components slider updates PCA",
      "Variance plot shows cumulative variance",
      "Retrieves best SVM/ANN from previous tabs",
      "Retrains models on PCA data",
      "Shows clear before/after comparison",
      "Allows user to add conclusions"
    ]
  }

  COMPLETED: obj["pca_interactive_tab"]
}

## EXECUTION_ORDER {
  
  STEP 1: obj["ui_architecture"] - Create folder structure ✓
  STEP 2: obj["visualization_functions"] - Create plotting utilities ✓
  STEP 3: obj["data_loader"] - Create data preprocessing ✓
  STEP 4: obj["base_layout"] - Create components + main app ✓
  STEP 5: obj["working_prototype"] - Build Config tab + validate ✓
  STEP 6: obj["svm_interactive_tab"] - Build SVM tab ✓
  STEP 7: obj["ann_interactive_tab"] - Build ANN tab ✓
  STEP 8: obj["pca_interactive_tab"] - Build PCA tab ✓
  
}

## NEXT_ACTION {
  action: "CREATE folder structure and start with components",
  why: "Foundation for all other work"
}

