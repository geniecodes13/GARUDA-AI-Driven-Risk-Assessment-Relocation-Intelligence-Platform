# GARUDA Architecture Overview

```mermaid
flowchart LR
    A[Select habitation / district / block] --> B[Validation layer]
    B --> C[Hazard engine]
    B --> D[Vulnerability engine]
    C --> E[Risk engine]
    D --> E
    E --> F[Priority engine]
    F --> G[Safe-site discovery]
    G --> H[Capacity engine]
    H --> I[Relocation optimizer]
    I --> J[What-if simulator]
    J --> K[Explainability layer]
    K --> L[Officer review & approval]
    L --> M[Resource-aware decision cockpit]
    M --> N[AI assistant query interface]
```

## Prototype notes

- The MVP uses synthetic, demonstration-grade geospatial data to represent Uttarakhand pilot conditions.
- The calculation pipeline remains deterministic and explainable; no numerical decisions are delegated to an LLM.
- Resource checks are integrated into the same decision flow so that relocation feasibility depends on both safety and availability.
