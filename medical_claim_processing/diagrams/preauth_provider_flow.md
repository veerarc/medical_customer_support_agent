# Medical Pre-authorization Workflow

```mermaid
graph TB
    subgraph "Front Desk Process"
        A[Patient Visit] --> B[Front Desk Agent]
        B --> C[Collect Demographics]
        B --> D[Scan Insurance Card]
        C --> E[Create/Update EMR]
        D --> E
    end

    subgraph "Clinical Processing"
        E --> F[Diagnosis Billing Agent]
        F --> G[Extract Clinical Concepts]
        G --> H[Generate Codes]
        H --> I[Cost Estimation]
        I --> J[Clinical Justification]
    end

    subgraph "Insurance Verification"
        J --> K[Insurance Desk Agent]
        K --> L[Verify Coverage]
        L --> M[Validate Network Status]
        M --> N[Check Authorization Requirements]
    end

    subgraph "Pre-authorization Submission"
        N --> O[Pre-auth Form Generator]
        O --> P[Compile Data]
        P --> Q[Format Request]
        Q --> R[Submit to Insurer]
        R --> S((Approval Status))
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style K fill:#bbf,stroke:#333,stroke-width:2px
    style O fill:#bbf,stroke:#333,stroke-width:2px
    style S fill:#bfb,stroke:#333,stroke-width:2px

    classDef process fill:#f9f9f9,stroke:#333,stroke-width:1px
    class C,D,E,G,H,I,J,L,M,N,P,Q,R process
```

## Diagram Components

### 1. Front Desk Process
- Initial patient contact
- Demographics collection
- Insurance verification
- EMR creation/update

### 2. Clinical Processing
- Clinical data extraction
- Medical coding (ICD-10, CPT, DRG)
- Cost estimation
- Treatment justification

### 3. Insurance Verification
- Coverage validation
- Network status check
- Authorization requirements

### 4. Pre-authorization Submission
- Data compilation
- Request formatting
- Submission to insurer
- Status tracking

## Color Legend
- 🟣 Purple Boxes: AI Agents
- ⬜ White Boxes: Process Steps
- 🟢 Green Circle: Final Status

This diagram illustrates the automated workflow using CrewAI agents for medical pre-authorization processing, from patient registration to final submission.
