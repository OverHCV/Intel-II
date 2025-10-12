# ParLang Language Guide

> **Summary**: Executable language where VERBS are keywords, based on IN/OUT. Designed for human writability and agents to read/execute systematically.

### 🎯 Key Takeaways:

1. **Parameters** - ANY verb can have IN(...) or OUT(...)
2. **Nesting** - Any verb level can have inside another verbs (like JSON)
3. **Named outputs** - reference objects across verbs (`OUT(object)` → `IN(object)`)
4. **Two-file system** - `feature.plan.md` (context/header) + `feature.exec.md` (instructions/body)
5. **Human + Agent friendly** - readable pseudocode that executes like a program

## Philosophy: Computer Architecture 🖥️

This language treats you (agent) as a **computer's ALU (Arithmetic Logic Unit)**.

### System Architecture:

```
1. feature.plan.md = DATA MEMORY (Objectives, Context, Dependencies)
2. feature.exec.md = INSTRUCTION MEMORY (Step-by-step operations to execute)
3. AGENT (YOU) = ALU (Reason and executes instructions, gather data)
4. STATUS_POINTER = INSTRUCTION POINTER (Simple counter: which line/objective is right now)
5. feature.analysis.md = FEEDBACK LOOP (Post-mortem, bugs found, lessons learned)
```

### Iterative Cycle:

1. **User sends initial plan** (feature.plan.md)
2. **Agent reads, improves, and ASKs questions** (feature.plan.md)
3. **User answers, modifies, clarifies**
4. **Iterate until plan is crystal clear** (feature.exec.md also is iterated)
5. **Executes when confirmed** (feature.exec.md is executed)
6. **Bugs happen** (normal!) (Document in feature.analysis.md)
8. **Closed feedback loop** (parlang-guide.md is updated based on the reflection made in feature.analysis.md)

This way you can map what really needs to be done, get clarity with inputs/outputs, and iterate before execution

## File Structure (The 3 Memories)

### 📋 PLANNING.md (Data Memory)

The "what" and "why" - high-level objectives and context

```
CONTEXT { ... }
OBJECTIVES as obj [ ... ]
DEPENDENCIES [ ... ]
ASK blocks for clarification
```

### ⚙️ EXECUTION.md (Instruction Memory)

The "how" - detailed step-by-step operations (auto-generated during execution)

```
IMPLEMENT obj["X"] {
  UNDERSTAND { ... }
  CREATE { ... }
  VALIDATE { ... }
}
```

### 📊 ANALYSIS.md (Feedback Memory)

The "what we learned" - post-mortem after completion to not fail again

```
BUGS_FOUND [ ... ]
PLANNING_GAPS [ ... ]
LESSONS_LEARNED [ ... ]
```

---

## Planning Language Structure

### CONTEXT Block

```
CONTEXT IN(@existing_files) OUT(environment_map) {
  project: [technology stack],
  rules: [@files with guidelines to read],
  current_state: [@key_files_to_understand]
}
```

**Purpose**: Sets your operational environment and constraints.

### OBJECTIVES Block

```
OBJECTIVES as obj OUT(goal_list) [
  "key name a": { 
    why: "[business/technical reason]",
    DoD: "[Definition of Done - when is this complete?]"
  },
  "key name b": { why: "[reason]", DoD: "[criteria]" },
  ...
]
```

**Purpose**: Defines what needs to be accomplished, why, and when it's done.

## Execution Commands (The Instruction Set)

### Taxonomy Verb Hierarchy

Execute in complexity order - simpler operations build into complex ones:

**Level 0: Clarification** (BEFORE anything else)

- `ASK`: Request clarification from user (blocks execution until answered)

**Level 1: Comprehension**

- `READ`: Parse file content, understand structure
- `UNDERSTAND`: Grasp logic, patterns, existing implementations
- `TRACE`: Follow COMPLETE execution flow from start to FINAL DESTINATION (including database/external systems)

**Level 2: Analysis**

- `ANALYZE`: Break down components, identify patterns
- `EXTRACT`: Pull specific logic/data from existing code
- `IDENTIFY`: Find specific elements or patterns
- `AUDIT`: Check shared components, dependencies, integration points
- `SCHEMA_CHECK`: Verify data structure compatibility with database/external systems (CRITICAL for data changes)
- `IMPORT_TRACE`: Trace module resolution paths for nested structures (CRITICAL before creating files)
- `ENVIRONMENT_CHECK`: Verify framework execution context and runtime environment (CRITICAL for framework-specific code)
- `NAMESPACE_CHECK`: Verify identifier uniqueness before creating files/functions/classes (CRITICAL for avoiding collisions)
- `DEPENDENCY_TRACE`: Track what depends on a file/module after creation (CRITICAL for refactoring)
- `POST_CHANGE_VALIDATION`: Verify system coherence after any modification (CRITICAL after any change)

**Level 3: Synthesis**

- `CREATE`: Build new components, write new code
- `IMPLEMENT`: Execute the full objective
- `INTEGRATE`: Combine new code with existing systems

**Level 4: Evaluation**

- `EVALUATE`: Make architectural decisions
- `VALIDATE`: Check correctness, test functionality (MUST have acceptance criteria)
- `DECISION`: Choose between implementation approaches

**Level 5: Reflection** (AFTER execution)

- `REFLECT`: Document what went wrong, why bugs happened, lessons learned

### Control Flow Constructs

Like a normal proggraming language use flow control and

```
IF (condition) THEN action ELSE alternative
FOR item IN collection { operations }
WHILE (condition) { operations }
```

### Special Operations

- `MODIFY`: Change existing code
- `EXTRACT`: Pull logic from one file to use elsewhere
- `REDIRECT`: Change routing/navigation flow
- `COMPLETED`: Marks task section as finished

---

## Verbs Block structure

ANY verb word can be a block and can be embeed in themselfs if needed. They can

define a procedure or a lineal step of the process. Some examples below.

### ASK Verb (Blocks Execution)

**Purpose**: Clarify ambiguities BEFORE implementing

```
ASK IN(current_context) OUT(user_decision): human {
  question: "Where should AdminOnboardingData be stored?",
  options: [
    "1. Extend OnboardingData interface",
    "2. Create separate admin_onboarding table",
    "3. Store as placeholder in existing table"
  ],
  required_for: obj["admin_data_persistence"],
  blocks_execution: true,
  why: "Implementation depends on storage strategy decision"
}
```

**When to use**: Any time you need user input to make architectural decisions

### TRACE Verb (Level 1 - Deep Analysis)

**Purpose**: Follow COMPLETE execution flow from User perspective to minimal detail (database/backend systems) Top-Down methodology

```
TRACE IN(@useAdminOnboardingFlow.ts, @OnboardingContext.tsx, @onboardingStorage.ts) OUT(completion_flow_map): completion_flow {
  from: "user clicks Complete Setup button",
  through: [
    "handleComplete() in useAdminOnboardingFlow",
    "onboardingContext.completeOnboarding()",
    "onboardingStorage.save()",
    "localStorage.setItem()",
    "supabase.from('onboard').upsert()"
  ],
  to: "state persisted : localStorage + Supabase",
  validates: [
    "completion flag set to true",
    "page reload doesn't reset state",
    "no infinite redirect loops",
    "database save operation succeeds"  // NEW: Always validate external persistence
  ],
  why: "Must understand COMPLETE flow including database to avoid persistence bugs"
}
```

**When to use**: When you need to understand how data flows end-to-end

**CRITICAL**: Always trace to the final destination (database, API, file system), not just application layer

### AUDIT Verb (Level 2 - Dependency Analysis)

**Purpose**: Identify shared components and integration points

```
AUDIT IN(@OnboardingLayout.tsx, @AdminOnboarding.tsx, @UserOnboarding.tsx) OUT(shared_analysis): shared_components {
  identify: [
    "OnboardingLayout - used by both User and Admin flows",
    "QuestionCard - generic, reusable",
    "OnboardingProgress - depends on step configuration"
  ],
  check_each: {
    OnboardingLayout: {
      is_shared: true,
      is_configurable: CHECK,
      hardcoded_assumptions: IDENTIFY,
      needs_changes: ["step labels", "skip button logic"]
    }
  },
  validates: "shared components support all use cases",
  why: "Prevent bugs from hardcoded assumptions in shared code"
}
```

**When to use**: When creating parallel flows that share infrastructure

### SCHEMA_CHECK Verb (Level 2 - Compatibility Validation)

**Purpose**: Verify data structure changes are compatible, eg. the database schema

```
SCHEMA_CHECK IN(@types/onboarding.ts, @supabase/types, @onboardingStorage.ts) OUT(compatibility_report): {
  
  typescript_interface: {
    name: "OnboardingData",
    fields: ["jobRole", "repetitiveTasks", "selectedTemplate"],
    removed: ["industry", "companySize", "tools"]
  },
  
  database_schema: {
    table: "onboarding",
    required_fields: ["user_id", "job_role", "industry", "company_size", "tools", "selected_template"],
    nullable_fields: ["tenant_id", "templates"]
  },
  
  MISMATCH_DETECTED: {
    missing_in_typescript: [],
    missing_in_database: ["repetitiveTasks"],
    removed_from_typescript: ["industry", "companySize", "tools"],
    CRITICAL: true,
    why: "Save operation will fail - removed fields are required in database"
  },
  
  IF (MISMATCH_DETECTED.CRITICAL) THEN {
    ASK: user {
      question: "Schema mismatch: TypeScript removed fields that database requires. How to handle?",
      options: [
        "1. Database migration (ALTER TABLE - requires schema change)",
        "2. Provide empty defaults for removed fields (backward compatible)",
        "3. Store new fields in separate table"
      ],
      blocks_execution: true,
      required_for: "database persistence",
      why: "Will cause runtime errors on save operation"
    }
  }
}
```

**When to use**: ALWAYS when modifying any data structure that gets persisted

**CRITICAL**: Run BEFORE implementing, not after bug is found

### IMPORT_TRACE Verb (Level 2 - Import Resolution Analysis)

**Purpose**: Trace imports in nested structures BEFORE creating files

```
IMPORT_TRACE IN(@project_structure, execution_point) OUT(import_validation): {
  executing_from: "ui/app.py",
  trying_to_import: ["config", "settings.imports", "funcs.visualizers"],
  python_searches: [
    "1. Same directory (ui/)",
    "2. Parent directories in sys.path",
    "3. PYTHONPATH env variable",
    "4. Site-packages"
  ],
  will_succeed: {
    "config": "NO - not in ui/ or sys.path",
    "settings.imports": "NO - parent not in sys.path"
  },
  solutions: [
    "1. Add: sys.path.append(os.path.dirname(__file__)/../)",
    "2. Add: PYTHONPATH=. streamlit run ui/app.py",
    "3. Create: __init__.py and use relative imports",
    "4. Run from root with adjusted paths"
  ],
  chosen_solution: "Add sys.path manipulation to ui/app.py",
  why: "Prevents ModuleNotFoundError at runtime"
}
```

**When to use**: ALWAYS before creating nested file structures with cross-directory imports

**CRITICAL**: Run BEFORE writing any imports, not after error occurs

### ENVIRONMENT_CHECK Verb (Level 2 - Runtime Context Verification)

**Purpose**: Verify framework execution environment before running code

```
ENVIRONMENT_CHECK IN(@framework, @file_structure) OUT(env_validation): {
  framework: "Streamlit",
  execution_command: "streamlit run ui/app.py",
  checks: {
    working_directory: {
      when_run: "Where is os.getcwd() when command executes?",
      expected: "project_root OR ui/?",
      affects: "Relative path resolution"
    },
    sys_path: {
      contains: ["ui/", "project_root?", "site-packages"],
      missing: "project_root if not included",
      affects: "Import resolution"
    },
    import_resolution: {
      test: "Can ui/app.py import config.py?",
      result: "YES/NO based on sys.path"
    }
  },
  failure_modes: [
    "ModuleNotFoundError if parent not in sys.path",
    "FileNotFoundError if cwd assumptions wrong",
    "Import errors if framework changes context"
  ],
  why: "Framework execution context often differs from normal execution"
}
```

**When to use**: ALWAYS before running framework-specific code (Streamlit, Django, Flask, etc.)

### NAMESPACE_CHECK Verb (Level 2 - Identifier Collision Detection)

**Purpose**: Verify name uniqueness BEFORE creating any file/function/class

```
NAMESPACE_CHECK IN(@project_structure, new_identifier) OUT(collision_report): {
  identifier: "config",
  type: "file/module",
  searching_in: ["project_root/", "ui/", "ui/pages/"],
  
  CHECK: {
    existing_files: grep -r "config.py" .,
    existing_imports: grep -r "from config import" .,
    existing_modules: grep -r "import config" .
  },
  
  found_collisions: [
    "project_root/config.py",
    "Multiple imports from root config.py"
  ],
  
  IF (collisions_found) THEN {
    alternative_names: ["conf.py", "page_config.py", "settings_page.py"],
    chosen: "conf.py",
    why: "Avoids collision with root config.py module"
  },
  
  validates: "No namespace pollution, unique identifier"
}
```

**When to use**: ALWAYS before creating any new file, function, class, or module

**Time cost**: 5 seconds of grep  
**Time saved**: Hours of debugging import errors

### DEPENDENCY_TRACE Verb (Level 2 - Dependent Tracking)

**Purpose**: Track what depends on a module/file AFTER creation

```
DEPENDENCY_TRACE IN(@created_file) OUT(dependent_list): {
  file: "ui/pages/config.py",
  search_imports: [
    "from ui.pages.config import",
    "from ui.pages import config",
    "import ui.pages.config"
  ],
  
  found_dependents: [
    "ui/pages/__init__.py:3 → from .config import config_page"
  ],
  
  IF (file_renamed_to: "conf.py") THEN {
    UPDATE_DEPENDENTS: [
      "ui/pages/__init__.py:3 → from .conf import config_page"
    ],
    validates: "All imports still resolve after rename"
  },
  
  why: "Prevent broken imports during refactoring"
}
```

**When to use**: ALWAYS after creating files that will be imported, ALWAYS before renaming/moving files

### POST_CHANGE_VALIDATION Verb (Level 2 - System Coherence Check)

**Purpose**: Verify system still works after ANY modification

```
POST_CHANGE_VALIDATION IN(@modified_files) OUT(validation_result): {
  changes: ["Renamed ui/pages/config.py → conf.py"],
  
  checks: [
    {
      type: "imports_resolve",
      action: "Trace all imports of renamed module",
      result: "PASS/FAIL"
    },
    {
      type: "execution_test",
      action: "Run entry point (streamlit run ui/app.py)",
      result: "PASS/FAIL"
    }
  ],
  
  IF (ANY check FAILS) THEN {
    ROLLBACK or FIX_IMMEDIATELY,
    document: "What broke and why"
  },
  
  why: "Catch cascading failures immediately"
}
```

**When to use**: ALWAYS after ANY file rename, move, deletion, or major refactoring

**Rule**: Never end a change session without validation

### FRAMEWORK_CHECKS Verb (Level 4 - Technology-Specific Validation)

**Purpose**: Validate framework-specific requirements

```
STREAMLIT_CHECKS IN(@ui/, @app.py) OUT(validation_report): {
  import_resolution: {
    check: IMPORT_TRACE(ui/app.py → config),
    validates: "No ModuleNotFoundError"
  },
  execution_context: {
    check: ENVIRONMENT_CHECK(streamlit, ui/),
    validates: "Paths resolve correctly"
  },
  session_state: {
    check: "State persists across reruns",
    validates: "No state loss on interaction"
  }
}

REACT_CHECKS IN(@components/) OUT(validation_report): {
  conditional_rendering: {
    check: "Components need key props",
    validates: "No hook order violations"
  },
  hooks: {
    check: "Consistent import style",
    validates: "No reconciliation issues"
  }
}
```

**When to use**: ALWAYS for framework-specific implementations

## VERB Block Structure

**Remember**: ANY verb can have IN/OUT, and ANY verb can be a parent or nested element!

```
IMPLEMENT obj["objective_name"] IN(@file1.tsx, @file2.ts) OUT(@newFile.tsx, @modified.ts) = {

  ASK IN(current_context) OUT(user_decision): user {
    question: "Which approach?",
    options: [...],
    blocks_execution: true
  }

  UNDERSTAND IN(@existing_files) OUT(understanding_map): {
    
    READ IN(@file.ts) OUT(extracted_patterns): {
      extract: "specific logic",
      why: "need this pattern"
    }
    
    TRACE IN(@file1.ts, @file2.ts) OUT(flow_diagram): {
      from: "entry point",
      through: ["step1", "step2"],
      to: "final state"
    }
  }

  ANALYZE: {
    
    AUDIT IN(@shared_components) OUT(component_audit): {
      identify: components_used_by_multiple_flows,
      check: configuration_needs
    }
    
    IDENTIFY IN(extracted_patterns) OUT(reusable_parts): {
      find: "what can be reused",
      extract: "specific functions/logic"
    }
  }

  EVALUATE IN(analysis_result): {
    DECISION: "option A" OR "option B",
    IF (condition) THEN action ELSE alternative
  }

  CREATE IN(decisions, reusable_parts) OUT(@ComponentName.tsx, @hookName.ts): {
    component_name: {
      why: "reason",
      props: [...],
      logic: {...}
    }
  }

  INTEGRATE IN(@ComponentName.tsx, @existing_system.tsx) OUT(integrated_system): {
    WITH: existing_systems,
    ENSURE: state_persistence,
    TRIGGER: necessary_events
  }

  VALIDATE IN(integrated_system) OUT(validation_report): {
    
    ACCEPTANCE_CRITERIA: [
      "User can complete action",
      "State persists after reload",
      "No infinite loops",
      "Correct UI displayed"
    ]

    TEST_SCENARIOS IN(integrated_system) OUT(test_results): [
      {
        name: "Happy path",
        steps: ["action1", "action2"],
        expected: ["result1", "result2"]
      }
    ]

    REACT_CHECKS IN(@components) OUT(framework_validation): {
      conditional_rendering: needs_keys?,
      hooks: consistent_imports?
    }
  }

  COMPLETED: obj["objective_name"]

} OUT(
  created_files: [...],
  modified_files: [...]
)
```

**Key principles**:

- **Every VERB can have IN/OUT** - not just top-level blocks
- **Nested composition** - verbs inside verbs, infinitely
- **Named outputs** - reference results later (flow_diagram, analysis_result, etc.)
- **Flexible structure** - Human-readable
- **Chain outputs to inputs** - Clear OUT from one verb becomes IN for next

## Key Execution Rules

### 0. The Three Layers Rule ⚠️ CRITICAL

**ALWAYS trace and validate THREE layers for BOTH data flow AND execution context**:

#### Data Flow (original):
1. **Application Layer** (Component → Hook → Context)
2. **Persistence Layer** (Storage Service → Database/API)
3. **External Systems** (Supabase, REST APIs, File System)

Example INCOMPLETE (❌): `Component → Hook → Context 🛑`  
Example COMPLETE (✅): `Component → Hook → Context → Storage → Database ✅`

#### Execution Context (NEW - equally critical):
1. **Code Layer** (What imports you write)
2. **Framework Layer** (How framework resolves imports - Streamlit, Django, Flask context)
3. **Runtime Layer** (Where Python actually finds modules - sys.path, cwd, PYTHONPATH)

Example INCOMPLETE (❌): `Write imports 🛑 STOPPED` (assumes it works)  
Example COMPLETE (✅): `Write imports → IMPORT_TRACE → ENVIRONMENT_CHECK → TEST ✅`

**NEVER stop at layer 1 or 2. ALWAYS reach layer 3 for BOTH flows.**

### 1. Follow Dependency Order

- Execute simpler operations before complex ones
- Complete all operations in a section before moving to next
- Respect DEPENDENCIES block sequence requirements

### 2. File References

- `@filename.ext` = Read this file for context
- `IN(...)` = Input files you need to work with
- `OUT(...)` = Files you will create or modify
- `...` in OUT means "other files/functions may be modified as needed" but is better to always concretize them

### 3. Why-Driven Development

- Every operation includes `why:` - this is the business/technical reason, the rationale behind
- Use the "why" to guide implementation decisions
- If unclear, prioritize the "why" over specific implementation details
- Always know what makes the objective to end (DoD) so is NOT an infinite of subtasks

### 3.5. Data Structure Change Protocol

**When changing ANY data structure that gets persisted**:

```
PROTOCOL: {
  STEP 1: SCHEMA_CHECK {
    compare: typescript_types vs database_schema,
    identify: removed_fields, added_fields, type_changes
  }
  
  STEP 2: ASK (if mismatch) {
    question: "How to handle schema mismatch?",
    options: [migration, defaults, separate_storage],
    blocks_execution: true
  }
  
  STEP 3: TRACE {
    from: "UI action",
    through: ["component", "hook", "context", "storage", "DATABASE"],
    to: "data persisted in external system",
    validates: "save operation succeeds with new structure"
  }
  
  STEP 4: VALIDATE {
    test: "actual database save operation",
    not_just: "TypeScript compilation"
  }
}
```

**Why this matters**: TypeScript types ≠ Database schema. Runtime errors happen at persistence layer.

### 4. Modular Architecture

- Separate logic from UI (state, components, ...)
- Create reusable, focused components
- Follow existing project patterns and conventions

### 5. Status Tracking (Instruction Pointer)

**Keep it SIMPLE** - like a program counter in a CPU:

```
STATUS_POINTER = obj["objective_name"]: VERB: operation
```

**Examples**:

```
STATUS_POINTER = obj["role_based_onboarding"]: CREATE: getUserRole.ts
```

Or could be like:

```
STATUS_POINTER = obj["admin_credentials_setup"]: VALIDATE: acceptance_criteria
STATUS_POINTER = "COMPLETED: ALL OBJECTIVES"
```

**Purpose**:

- Simple counter: which instruction/objective are we on?
- If interrupted, you know exactly where to resume
- All previous objectives must be COMPLETED before moving forward

**Don't overcomplicate it** - complex state goes in other objects/sections, not in the pointer

## Example Usage Patterns

### Simple Task with IN/OUT

```
CREATE IN(@types.ts, @existing_pattern.ts) OUT(@ComponentName.tsx): ComponentName {
  why: "User needs X functionality",
  props: ["prop1", "prop2"],
  logic: {
    state: "useState()",
    effects: "useEffect(() => {...})"
  },
  validation: "Required behavior"
}
```

### Complex Integration Chain

```
EXTRACT IN(@existing_file.ts) OUT(reusable_logic): {
  logic: "function calculateTotal() {...}",
  why: "Need this in multiple places"
}

CREATE IN(reusable_logic, @types.ts) OUT(@new_component.tsx): {
  component: "NewComponent",
  uses: reusable_logic
}

INTEGRATE IN(@new_component.tsx, @target_system.tsx) OUT(integrated_app): {
  mount_point: "Dashboard",
  ensure: "preserves_existing_functionality"
}

VALIDATE IN(integrated_app) OUT(test_report): {
  check: "integration_works",
  check: "no_breaking_changes"
}
```

### Conditional Logic with Named Results

```
EVALUATE IN(@current_code.tsx) OUT(decision): {
  DECISION: "create new component" OR "modify existing",

  IF (better_to_create_new) THEN {
    CREATE IN(decision) OUT(@NewComponent.tsx): {...}
  } ELSE {
    MODIFY IN(@ExistingComponent.tsx) OUT(@ExistingComponent.tsx): {...}
  }
}
```

### Chained Verb Composition

```
READ IN(@auth.ts) OUT(auth_pattern) {
  extract: "user.app_metadata.role"
}

TRACE IN(auth_pattern, @OnboardingRouter.tsx) OUT(flow_map) {
  from: "login",
  to: "correct onboarding"
}

AUDIT IN(flow_map, @shared_components) OUT(issues) {
  check: "hardcoded assumptions"
}

FIX IN(issues) OUT(@OnboardingLayout.tsx, @types.ts) {
  add: "steps prop to OnboardingLayout",
  create: "ADMIN_ONBOARDING_STEPS constant"
}
```

## Execution Mindset

- **Be literal**: Execute exactly what's specified
- **Follow hierarchy**: Complete lower-level operations to finish higher-level ones
- **Respect constraints**: Honor architectural principles and existing patterns in repo
- **Think modularly**: Each operation should have clear inputs and outputs
- **Validate continuously**: Check each step so you can keep working
- **Trace completely**: ALWAYS follow data to its final destination (database/API/file system)
- **Question assumptions**: "Does TypeScript type match database schema?"
- **Test externally**: Runtime database operations, not just compilation

## The Iterative Process (How It All Works)

### Phase 1: Planning (User + Agent Collab)

```
1. User writes initial last.plan.md
   ├─ CONTEXT, OBJECTIVES, DEPENDENCIES
   └─ High-level "what" and "why"

2. Agent reads and ASKs questions
   ├─ Identifies ambiguities
   ├─ Asks for clarifications
   └─ Proposes improvements

3. User answers in same file
   ├─ Clarifies decisions
   ├─ Adds missing context
   └─ Refines objectives

4. Iterate until crystal clear ✅
   └─ Both agree plan is executable
```

### Phase 2: Execution (Agent = ALU)

```
1. Agent executes operations sequentially
   ├─ Follows STATUS_POINTER (instruction counter)
   ├─ Moves through UNDERSTAND → CREATE → VALIDATE
   └─ Updates STATUS_POINTER as progress is made

2. Creates files, integrates systems
   └─ Outputs get documented in OUT() sections

3. Bugs may happen (normal!)
   └─ Fix them, document in analysis.md
```

### Phase 3: Reflection (Closed Feedback Loop)

```
1. Document in analysis.md
   ├─ What bugs were found?
   ├─ Why did they happen?
   ├─ What was missing from plan?
   └─ What to add next time?

2. Update parlang-guide.md if needed
   └─ Add new verbs, patterns, checks

3. Next implementation improves
   └─ Closed feedback loop ✅
```

---

## Real Examples: What We've Learned

### ✅ What SUCCEEDED in Third Implementation (User Onboarding 3-Step - Oct 11, 2025):

**Initial Success**:

- Component/Hook/Context layers: Perfect
- TypeScript compilation: Zero errors
- UI/UX implementation: Works correctly
- Template pre-fill: Works as expected

**BUT**: Found critical bug during user testing

**❌ What FAILED**:

```
BUG: Database save operation failed with 400 Bad Request
ERROR: "PGRST116: JSON object requested, multiple (or no) rows returned"
ROOT CAUSE: OnboardingData type changed (removed industry/companySize/tools) 
            but onboardingStorage.ts still tried to save removed fields
IMPACT: User couldn't complete onboarding
```

**Why it happened**:

```
TRACE stopped here:
  Component → Hook → Context → Storage Service 🛑 STOPPED

Should have traced to:
  Component → Hook → Context → Storage Service → DATABASE ✅
                                                    ↑
                                    Would have caught schema mismatch!
```

**What was MISSING from plan**:

```
❌ No SCHEMA_CHECK comparing TypeScript types vs database schema
❌ No ASK about migration strategy when removing fields
❌ No TRACE to database layer
❌ No validation of actual save operation
✅ Only validated TypeScript compilation (not enough!)
```

**The Fix**:

```typescript
// Provide empty defaults for backward compatibility
const record = {
  industry: "",        // Deprecated but required by database
  company_size: "",    // Deprecated but required by database
  tools: [],          // Deprecated but required by database
}
```

**Time to fix**: 2 minutes (once root cause identified)

**Key Learning**:

- **TypeScript types ≠ Database schema**
- **Always trace to final destination (database/API)**
- **Always validate actual persistence operations**
- **For data structure changes: SCHEMA_CHECK is mandatory**

---

### ❌ What FAILED in First Implementation (Admin Onboarding - Oct 10, 2025):

```
UNDERSTAND IN(@useOnboardingFlow.ts): {
  READ: @file_example.ts
}
```

**Problem**: Only READ, didn't TRACE the complete flow

**Result**: Missed that completion needs OnboardingContext integration

### ✅ What SHOULD Have Been:

```
UNDERSTAND: {
  READ: @useOnboardingFlow.ts
  TRACE: completion_flow {
    from: "handleComplete() call",
    through: [
      "onboardingContext.completeOnboarding()",
      "onboardingStorage.save()",
      "localStorage + Supabase"
    ],
    to: "completed state persisted",
    validates: "no redirect loops"
  }
}
```

### ❌ What FAILED: No Shared Components Audit

```
CREATE IN(@OnboardingLayout.tsx): AdminOnboarding {
  uses: OnboardingLayout
}
```

**Problem**: Didn't check if OnboardingLayout was configurable

**Result**: Hardcoded step labels showed wrong text for admin

### ✅ What SHOULD Have Been:

```
ANALYZE: {
  
  AUDIT IN(@OnboardingLayout.tsx) OUT(layout_audit_error): {
    OnboardingLayout: {
      is_shared: true,
      check: "step labels configurable?",
      result: "❌ HARDCODED - needs prop"
    }
  }
}

FIX IN(layout_audit_error) OUT(@OnboardingLayout.tsx, @types.ts): {
  MODIFY IN(@OnboardingLayout.tsx) OUT(@OnboardingLayout.tsx): {
    add: "optional steps prop"
  },
  CREATE IN(@types.ts) OUT(@types.ts): {
    add: "ADMIN_ONBOARDING_STEPS constant"
  }
}

CREATE IN(@OnboardingLayout.tsx, @types.ts) OUT(@AdminOnboarding.tsx): {
  component: "AdminOnboarding",
  passes: "ADMIN_ONBOARDING_STEPS to layout"
}
```

---

## Error Handling & Communication

### When Data Structures Change:

```
SCHEMA_CHECK: {
  compare: typescript_interface vs database_schema,
  IF (mismatch) THEN {
    ASK: user {
      question: "Schema mismatch detected. How to handle?",
      options: ["migration", "defaults", "separate_storage"],
      blocks_execution: true,
      why: "Will cause runtime save errors"
    }
  }
}
```

**Critical for**: Any change to persisted data structures

### When Things Are Unclear:

```
ASK: user {
  question: "Specific question about X",
  why: "I need this to proceed with Y",
  blocks_execution: true
}
```

**Don't assume** - always ASK when unclear (last option search by yourself)

### When File Not Found:

```
ERROR: {
  missing: "@InviteUsersModal.tsx",
  searched_in: "src/components/onboarding/",
  action: "Searching codebase...",
  found: "src/components/companies/analytics/InviteUsersModal.tsx"
}
```

**Don't fail** - search/grep and report actual location

### When Constraint Conflict:

```
CONFLICT: {
  constraint: "Files must be < 300 lines",
  current: "AdminOnboarding.tsx would be 350 lines",
  resolution: "Split into AdminOnboarding + AdminOnboardingLogic"
}
```

**Don't violate** - explain conflict and propose solution

---

## Remember: You Are The ALU

Each instruction is a function call with specific parameters and expected outputs

- **number.plan.md = DATA** you operate on
- **number.exec.md = INSTRUCTIONS** you execute
- **You = ALU** that processes everything
- **STATUS_POINTER = Program Counter** (simple!)
- **analysis.md = Feedback** for improvement
```
VERB IN(input1, input2, @file.ts) OUT(result1, @newfile.ts) {
  operations: [...],
  validations: [...],
  why: "reason"
}
```


**You process**:

- Clear inputs (IN) - what data/files you need
- Operations (body) - what to do
- Expected outputs (OUT) - what you produce
- Validation criteria (ACCEPTANCE_CRITERIA) - how to verify

**Like a program**:

- `number.plan.md` = Header file (declarations, interface, why)
- `number.exec.md` = Implementation file (actual code)
- Last number = latest version

**Be precise, methodical, and systematic** 🎯

---

## Common Failure Patterns (Learn from these!)

### FAILURE PATTERN #1: Stopping Trace Too Early

```
❌ WRONG:
TRACE: Component → Hook → Context 🛑
Result: Missed database persistence issues

✅ CORRECT:
TRACE: Component → Hook → Context → Storage → DATABASE ✅
Result: Caught schema mismatch before runtime
```

### FAILURE PATTERN #2: Trusting Types Alone

```
❌ WRONG:
"TypeScript compiles = everything works"
Result: Runtime database errors

✅ CORRECT:
"TypeScript compiles AND database operation tested = works"
Result: Validated actual persistence
```

### FAILURE PATTERN #3: No Schema Compatibility Check

```
❌ WRONG:
Change OnboardingData interface → implement → deploy
Result: Save operation fails (removed fields still required by DB)

✅ CORRECT:
Change interface → SCHEMA_CHECK → ASK about migration → implement with compatibility layer
Result: Backward compatible, saves successfully
```

### FAILURE PATTERN #4: Assuming Shared Components Are Configurable

```
❌ WRONG:
"This component exists, I'll just reuse it"
Result: Hardcoded assumptions break new use case

✅ CORRECT:
AUDIT: "Is this component configurable for my use case?"
Result: Made component accept configuration props
```

### FAILURE PATTERN #5: No End-to-End Validation

```
❌ WRONG:
VALIDATE: ["Component renders", "State updates"]
Result: Persistence failures not caught

✅ CORRECT:
VALIDATE: ["Component renders", "State updates", "Database save succeeds"]
Result: Full flow validated
```

### FAILURE PATTERN #6: Framework Context Blindness

```
❌ WRONG:
Create nested structure → write imports → assume works
Result: ModuleNotFoundError because framework execution context differs

✅ CORRECT:
IMPORT_TRACE → ENVIRONMENT_CHECK → CREATE → TEST_EXECUTION → verify
Result: Import paths validated before writing code

Example (Streamlit):
  ❌ "Created ui/app.py with 'from config import CONF' → should work"
  ✅ "IMPORT_TRACE shows ui/app.py can't reach config.py → add sys.path fix → test → works"
```

**Why it matters**: Frameworks change execution context  
**Time saved**: 30 seconds of checks prevents hours of debugging

### FAILURE PATTERN #7: Namespace Collision & Incomplete Refactoring

```
❌ WRONG:
Create ui/pages/config.py → realizes conflict → rename to conf.py → move on
Result: ui/pages/__init__.py still imports from .config → ModuleNotFoundError

✅ CORRECT:
NAMESPACE_CHECK → detect collision BEFORE creating → choose unique name from start
Result: No collision, no refactoring needed

Alternative (if rename needed):
NAMESPACE_CHECK → detect collision → DEPENDENCY_TRACE → update all imports → POST_CHANGE_VALIDATION
Result: Complete refactoring, all imports updated
```

**Why it happens**:
1. Create file without checking if name exists elsewhere
2. Rename to fix collision but don't trace dependents
3. Don't validate system still works after change
4. Context blindness: focus on file creation, ignore broader system

**Abstract pattern** (not language-specific):
- **Namespace pollution**: Same identifier at multiple levels
- **Incomplete refactoring**: Change one thing, forget to update dependents
- **No coherence check**: Make change → don't verify → breaks cascade

**Should prevent by**:
1. `NAMESPACE_CHECK` BEFORE creating any identifier (file/function/class)
2. `DEPENDENCY_TRACE` AFTER creating file that will be imported
3. `POST_CHANGE_VALIDATION` AFTER any rename/move/delete operation
4. `SYSTEMATIC_SEARCH`: "Does this name exist? What imports it?"

**Time cost of checks**: 10 seconds (grep existing names)  
**Time cost of bug**: 15+ minutes (identify, trace, fix, test)  
**Ratio**: Spending 10s saves 90x time

---

**Golden Rules**:
1. NEVER stop at Layer 1 or 2. ALWAYS validate Layer 3 (for BOTH data AND execution)
2. NEVER create nested structures without IMPORT_TRACE first
3. NEVER run framework code without ENVIRONMENT_CHECK first
4. NEVER create files/functions/classes without NAMESPACE_CHECK first
5. NEVER rename/move/delete without DEPENDENCY_TRACE + POST_CHANGE_VALIDATION

**Be precise, methodical, and systematic** 🎯