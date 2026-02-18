# Fork and Merge Model

```mermaid
flowchart TD

Start[Shared Prefix]

Start --> A1[Branch A]
Start --> B1[Branch B]

A1 --> A2
B1 --> B2

A2 --> MergeCheck{Safe deterministic merge?}

MergeCheck -->|Yes| Merged[Deterministic Merge]
MergeCheck -->|No| Stable[Stable Divergence]
```

---

## Key Principle

Convergence is conditional.

The system:

* merges only when safe,
* preserves divergence otherwise.

---

## Benefits

* Byzantine resilience.
* Long-term stability.
* No destructive resolution.
