# Kernel — Contract of Responsibility

> **Status**: Canonical — must be read before contributing
>
> This document defines the **explicit contract** between the **Kernel** and any consuming application (e.g. Veramem).
>
> The Kernel is intentionally strict. Any ambiguity here must be resolved in favor of **immutability, declarativity, and temporal correctness**.

---

## 1. What the Kernel **IS**

The Kernel is a **minimal cognitive substrate** whose role is to **record**, **structure**, and **expose** immutable signals over time.

It provides:

* 📜 **Append-only journals**
* 🧱 **Immutable domain primitives**
* ⏱ **Strict temporal invariants**
* 🧭 **Declarative representations of events and states**

The Kernel is:

* Deterministic
* Side-effect free
* Application-agnostic

It can be embedded, imported, or vendored by higher-level systems.

---

## 2. What the Kernel **IS NOT**

The Kernel deliberately does **not**:

* ❌ Execute actions
* ❌ Make decisions
* ❌ Enforce policies
* ❌ Resolve conflicts
* ❌ Apply business rules
* ❌ Maintain mutable runtime state

In particular:

> **The Kernel never decides what should happen.**
> It only records **what happened**, **what was observed**, or **what was declared**.

Any logic that answers *"should we"*, *"can we"*, or *"what now"* belongs **outside** the Kernel.

---

## 3. Core Invariants (Non‑Negotiable)

All Kernel code MUST respect the following invariants.

### 3.1 Immutability

* All domain objects are immutable after construction
* No in-place mutation
* No setters
* No internal state transitions

If a value changes over time, it is represented by **multiple entries**, not mutation.

---

### 3.2 Append‑Only Semantics

* Journals only grow
* Past entries are never rewritten or deleted
* Corrections are represented as **new entries**

---

### 3.3 Temporal Strictness

* Every entry **must** be time-bound
* `created_at` (or equivalent) is mandatory
* Time is monotonic within a journal context

The Kernel does **not** infer time — it records it.

---

### 3.4 Declarativity

Kernel structures describe **facts**, not **intentions**.

Allowed:

* “Action X was proposed”
* “Decision Y was validated”
* “Constraint Z was observed”

Forbidden:

* “Execute X”
* “Apply policy Y”
* “Resolve conflict Z”

---

## 4. Responsibility Split

This table defines **who owns what**.

| Concern                     | Kernel | Application |
| --------------------------- | ------ | ----------- |
| Timeline entries            | ✅      | ❌           |
| Journals                    | ✅      | ❌           |
| Action proposal recording   | ✅      | ❌           |
| Action resolution recording | ✅      | ❌           |
| Control state               | ❌      | ✅           |
| Policy enforcement          | ❌      | ✅           |
| Action execution            | ❌      | ✅           |
| Decision making             | ❌      | ✅           |
| UI / API mapping            | ❌      | ✅           |

If a feature touches **both columns**, it is almost certainly misdesigned.

---

## 5. Timeline Model Contract

### 5.1 TimelineEntry

A `TimelineEntry` represents a **single immutable fact**.

Guaranteed properties:

* Immutable
* Time-bound
* Declarative
* Serializable

It may reference:

* `action_id` (what action is concerned)
* `place_id` (contextual scope)
* `origin_ref` (traceability)

But it never:

* Executes the action
* Validates permissions
* Applies policies

---

### 5.2 Specialized Entries

Specializations (e.g. `ActionResolutionTimelineEntry`) are:

* Still immutable
* Still declarative
* Still append-only

They **add information**, never behavior.

Example:

> “Action A was VALIDATED”
> not
> “Action A should now execute”

---

## 6. Tests as Contract Enforcers

Kernel tests are **contract tests**, not implementation tests.

They MUST:

* Enforce immutability
* Reject hidden side-effects
* Fail if decision logic appears
* Fail if temporal invariants are bypassed

If a test requires mocking execution or policy:

> ❌ The test does not belong in the Kernel

---

## 7. Versioning & Evolution

The Kernel evolves **slowly and conservatively**.

Rules:

* Breaking changes require a major version bump
* New fields must be additive and optional
* Removal of fields is strongly discouraged

Applications adapt to the Kernel — **never the opposite**.

---

## 8. Guiding Principle (TL;DR)

> **The Kernel remembers.**
> **The Application decides.**

If you hesitate about where code belongs:

* If it *records*: Kernel
* If it *thinks*: Application
* If it *acts*: Application

---

*End of contract.*
