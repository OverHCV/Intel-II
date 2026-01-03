# Diagrams: Fase 2 - Sistema de Proyectos con Chat Conversacional

Professional Mermaid diagrams representing the PLANNED/IDEAL architecture. Discrepancies with actual implementation documented in consolidation.md.

**Style**: Pastel blues/greens, no emojis, formal technical documentation.

---

## 1. Multi-Agent System Architecture

Supervisor pattern coordinating specialized agents for different execution domains.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','lineColor':'#42a5f5','secondaryColor':'#c5e1a5','tertiaryColor':'#fff9c4','fontSize':'14px','fontFamily':'Arial'}}}%%
graph TB
    subgraph "User Layer"
        User[User Chat Interface]
    end

    subgraph "Supervisor Layer"
        Supervisor[Supervisor Agent<br/>Route & Coordinate]
    end

    subgraph "Specialized Agents"
        Planner[Crafts Planner Agent<br/>Task Breakdown & Planning]
        Backend[Backend Agent<br/>N8N Workflow Generation]
    end

    subgraph "Execution Layer"
        N8N[N8N Workflow Engine]
    end

    subgraph "Storage Layer"
        Supabase[(Supabase PostgreSQL<br/>State & Data)]
        Redis[(Redis<br/>Session Cache)]
    end

    User -->|Message| Supervisor
    Supervisor -->|Delegate Planning| Planner
    Supervisor -->|Delegate Backend| Backend

    Planner -->|Store Plan| Supabase
    Backend -->|Generate Workflow| N8N
    Backend -->|Persist Craft| Supabase

    N8N -->|Execution Results| Backend

    Supervisor -->|Save Checkpoint| Supabase
    Supervisor -->|Cache Session| Redis

    Planner -.->|Response| Supervisor
    Backend -.->|Response| Supervisor
    Supervisor -.->|Response| User

    style User fill:#e1f5fe
    style Supervisor fill:#b3e5fc
    style Planner fill:#c5e1a5
    style Backend fill:#c5e1a5
    style N8N fill:#fff9c4
    style Supabase fill:#d1c4e9
    style Redis fill:#d1c4e9
```

---

## 2. Backend Agent State Graph

LangGraph state machine for backend agent workflow execution.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','lineColor':'#42a5f5','fontSize':'13px'}}}%%
stateDiagram-v2
    [*] --> MessageSummarizer: User Input

    MessageSummarizer --> TaskInjector: Summarize Context

    TaskInjector --> Planner: No Active Tasks
    TaskInjector --> TaskEvaluator: Has Active Tasks

    Planner --> TaskBreakdown: Create Plan
    TaskBreakdown --> TaskInjector: Inject Tasks

    TaskEvaluator --> N8NToolExecution: Task Incomplete
    TaskEvaluator --> TestingSteps: Task Complete

    N8NToolExecution --> WorkflowGeneration: Generate Workflow
    WorkflowGeneration --> WorkflowPersister: Save Workflow
    WorkflowPersister --> WorkflowExecution: Execute
    WorkflowExecution --> ObserveExecution: Monitor
    ObserveExecution --> TaskEvaluator: Return Results

    TestingSteps --> TestEvaluation: Run Tests
    TestEvaluation --> TaskEvaluator: Tests Pass
    TestEvaluation --> N8NToolExecution: Tests Fail

    TaskEvaluator --> [*]: All Tasks Complete

    note right of MessageSummarizer
        Summarizes conversation
        context for agent context
    end note

    note right of TaskInjector
        Manages task queue
        and determines next action
    end note

    note right of Planner
        Uses Crafts Planner Agent
        to break down requirements
    end note

    note right of WorkflowPersister
        Persists to craft_storage
        for user visibility
    end note
```

---

## 3. Frontend Component Architecture

React component hierarchy for project workspace interface.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','lineColor':'#42a5f5','fontSize':'14px'}}}%%
graph TD
    subgraph "Page Level"
        Projects[Projects Page<br/>Main Container]
    end

    subgraph "Section Components"
        Header[ProjectHeader<br/>Title & Status]
        CraftSection[AlterCraftSection<br/>Planning & Building Mode]
        ProjectSection[AlterProjectSection<br/>Testing & Deployment]
    end

    subgraph "Checklist Components"
        ChecklistSection[ChecklistSection<br/>Task Category Container]
        ChecklistItem[ChecklistItem<br/>Individual Task]
        LoadingDots[LoadingDots<br/>Progress Indicator]
    end

    subgraph "Visualization Components"
        Diagram[Planning Diagram<br/>React Flow Graph]
        DiagramControls[Zoom/Pan Controls<br/>Interaction Layer]
    end

    subgraph "Execution Components"
        ExecutionFeedback[ExecutionFeedback<br/>Real-time Status]
        CredentialButtons[CredentialButtons<br/>Configuration UI]
        PublishButton[PublishButton<br/>Finalization Action]
    end

    Projects --> Header
    Projects --> CraftSection
    Projects --> ProjectSection

    CraftSection --> ChecklistSection
    CraftSection --> Diagram

    ChecklistSection --> ChecklistItem
    ChecklistItem --> LoadingDots

    Diagram --> DiagramControls

    ProjectSection --> ExecutionFeedback
    ProjectSection --> CredentialButtons
    ProjectSection --> PublishButton

    style Projects fill:#b3e5fc
    style Header fill:#c5e1a5
    style CraftSection fill:#c5e1a5
    style ProjectSection fill:#c5e1a5
    style ChecklistSection fill:#e3f2fd
    style ChecklistItem fill:#e3f2fd
    style Diagram fill:#fff9c4
    style ExecutionFeedback fill:#d1c4e9
```

---

## 4. Data Flow: From User Request to Workflow Execution

End-to-end sequence showing how a user request becomes an executed workflow.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','lineColor':'#42a5f5','fontSize':'13px'}}}%%
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant S as Supervisor
    participant P as Planner Agent
    participant B as Backend Agent
    participant N as N8N Engine
    participant D as Database

    U->>F: "Create workflow to send emails"
    F->>S: Chat message + project context

    S->>S: Load conversation checkpoint
    S->>P: Delegate: Create plan

    P->>P: Analyze requirements
    P->>P: Break down into tasks
    P->>D: Store plan structure
    P-->>S: Return: Plan with 3 tasks

    S->>B: Delegate: Execute Task 1

    B->>B: Identify N8N nodes needed
    B->>B: Generate workflow JSON
    B->>D: Persist craft (workflow definition)
    B->>N: Execute workflow

    N->>N: Run nodes sequentially
    N-->>B: Execution results + logs

    B->>B: Evaluate: Task 1 complete
    B->>D: Update task status
    B-->>S: Return: Task 1 success

    S->>D: Save checkpoint (state)
    S-->>F: Stream: Task 1 complete
    F-->>U: Update UI: Checklist item ✓

    Note over S,B: Repeat for Tasks 2-3

    S->>B: Delegate: Run tests
    B->>N: Test workflow execution
    N-->>B: All tests passed
    B-->>S: Return: Tests passed

    S->>D: Mark project as complete
    S-->>F: Stream: Project ready
    F-->>U: Enable "Publish" button
```

---

## 5. Craft Storage Schema

Database structure for persisting agent-generated workflows and components.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','fontSize':'14px'}}}%%
erDiagram
    PROJECTS ||--o{ CRAFTS : contains
    PROJECTS ||--o{ PROJECT_CREDENTIALS : requires
    PROJECT_CREDENTIALS }o--|| CREDENTIAL_RULES : follows
    CRAFTS ||--o{ CRAFT_EXECUTIONS : produces

    PROJECTS {
        uuid id PK
        text name
        text description
        enum status
        timestamp created_at
        timestamp updated_at
    }

    CRAFTS {
        uuid id PK
        uuid project_id FK
        text name
        text description
        enum craft_type
        jsonb workflow_definition
        enum status
        timestamp created_at
        timestamp updated_at
    }

    CRAFT_EXECUTIONS {
        uuid id PK
        uuid craft_id FK
        jsonb execution_data
        enum status
        text error_message
        timestamp started_at
        timestamp completed_at
    }

    PROJECT_CREDENTIALS {
        uuid id PK
        uuid project_id FK
        uuid credential_rule_id FK
        text credential_name
        boolean is_configured
    }

    CREDENTIAL_RULES {
        uuid id PK
        text name
        text description
        jsonb schema
        enum provider
    }
```

---

## 6. Deployment Architecture

Infrastructure components and their interactions.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','lineColor':'#42a5f5','fontSize':'14px'}}}%%
graph LR
    subgraph "Client Layer"
        Browser[Web Browser<br/>React SPA]
    end

    subgraph "CDN Layer"
        Vercel[Vercel CDN<br/>Static Assets]
    end

    subgraph "API Layer"
        FastAPI[FastAPI Server<br/>agents-api]
    end

    subgraph "Agent Layer"
        Agents[LangGraph Agents<br/>Python Runtime]
    end

    subgraph "Execution Layer"
        N8NDocker[N8N Container<br/>Docker]
        E2BCloud[E2B Sandbox<br/>Cloud]
    end

    subgraph "Data Layer"
        SupabaseDB[(Supabase<br/>PostgreSQL)]
        RedisCache[(Redis<br/>Cache)]
    end

    subgraph "Monitoring Layer"
        ClickHouse[(ClickHouse<br/>Telemetry)]
        OpenTel[OpenTelemetry<br/>Collector]
    end

    Browser --> Vercel
    Browser --> FastAPI

    FastAPI --> Agents

    Agents --> N8NDocker
    Agents --> E2BCloud
    Agents --> SupabaseDB
    Agents --> RedisCache

    FastAPI --> OpenTel
    Agents --> OpenTel
    N8NDocker --> OpenTel

    OpenTel --> ClickHouse

    style Browser fill:#e1f5fe
    style Vercel fill:#b3e5fc
    style FastAPI fill:#c5e1a5
    style Agents fill:#c5e1a5
    style N8NDocker fill:#fff9c4
    style E2BCloud fill:#fff9c4
    style SupabaseDB fill:#d1c4e9
    style RedisCache fill:#d1c4e9
    style ClickHouse fill:#ffccbc
    style OpenTel fill:#ffccbc
```

---

## 7. Development Timeline (Gantt)

Timeline showing the progression of major development efforts across the 21-day period.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e3f2fd','primaryTextColor':'#1565c0','primaryBorderColor':'#1976d2','fontSize':'13px'}}}%%
gantt
    title Fase 2: Multi-Agent System Development (Sep 14 - Oct 4, 2025)
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Architecture
    Plan Visibility Tooling           :done, arch1, 2025-09-14, 1d
    Frontend Agent POC                :done, arch2, 2025-09-17, 3d
    Task Manager Integration          :done, arch3, 2025-09-25, 3d
    Agent Separation Refactor         :done, arch4, 2025-09-28, 3d

    section Backend Development
    N8N Tools Enhancement             :done, be1, 2025-09-29, 2d
    Testing Steps Fix                 :done, be2, 2025-09-29, 1d
    Workflow Persistence              :done, be3, 2025-10-01, 2d
    Credentials Schema                :done, be4, 2025-10-03, 2d

    section Frontend Development
    Todo Components                   :done, fe1, 2025-09-14, 1d
    Planning Checklist                :done, fe2, 2025-09-14, 1d
    Planning Diagram                  :done, fe3, 2025-09-14, 2d
    Building Steps UI                 :done, fe4, 2025-09-19, 1d
    Loading States                    :done, fe5, 2025-09-19, 1d
    Planning Mode Refactor            :done, fe6, 2025-09-20, 1d
    Credentials Buttons               :done, fe7, 2025-09-23, 1d
    Testing Mode                      :done, fe8, 2025-09-23, 1d
    Execution Feedback                :done, fe9, 2025-09-25, 1d
    Publish Workflow                  :done, fe10, 2025-09-25, 1d
    Frontend Checklist                :done, fe11, 2025-09-27, 1d

    section Integration & Testing
    E2B Sandbox Integration           :done, test1, 2025-09-30, 2d
    Performance Testing               :done, test2, 2025-10-02, 2d
    Bug Fixes & Polish                :done, test3, 2025-10-03, 2d
```

---

## 8. Workflow Success Rates

Visualización de tasas de éxito de workflows por complejidad.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'xyChart': { 'plotColorPalette': '#4caf50, #f44336' }}}}%%
xychart-beta
    title "Tasa de Éxito de Workflows por Complejidad"
    x-axis "Complejidad" ["Simple", "Medio", "Complejo"]
    y-axis "Cantidad" 0 --> 160
    bar [153, 133, 38]
    bar [3, 9, 6]
```

---

## Diagram Usage Notes

1. **Architecture Diagram (1)**: Use in Part A to introduce overall system design
2. **State Graph (2)**: Use in Part B to explain backend agent implementation
3. **Component Hierarchy (3)**: Use in Part B for frontend architecture explanation
4. **Data Flow (4)**: Use in Part A or B to show user journey through system
5. **Schema (5)**: Use in Part B for data modeling explanation
6. **Deployment (6)**: May reference but likely defer to Fase 4 (deployment phase)
7. **Gantt Timeline (7)**: Use in Part A to show development progression over 21 days
8. **Workflow Success Rates (8)**: Use in Part C for validation metrics

**Rendering**: Export to PNG via Mermaid Live Editor or similar tool. Place screenshots in `.docs/project/images/10-04/`.

**Image Naming Convention**:
- `multi-agent-architecture.png`
- `backend-state-graph.png`
- `frontend-component-hierarchy.png`
- `data-flow-sequence.png`
- `craft-storage-schema.png`
- `deployment-architecture.png`
- `development-timeline-gantt.png`
- `workflow-success-chart.png`