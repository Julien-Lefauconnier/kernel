# Timeline Lifecycle

```mermaid
sequenceDiagram
participant A as Device A
participant B as Device B

A->>A: Append new entry
A->>A: Update commitment

A->>B: Send snapshot cursor

alt B behind
    B->>A: Request delta
    A->>B: Send delta
    B->>B: Validate and apply
else Divergence
    A->>B: Fork detected
    B->>A: Exchange fork proof
    A->>B: Merge or abstain
end
```

---

## Description

The timeline lifecycle includes:

1. Append-only memory.
2. Commitment updates.
3. Snapshot exchange.
4. Delta synchronization.
5. Fork detection.
6. Safe merge or abstention.

---

## Safety Principle

The system prefers:

> Refusal over unsafe convergence.
