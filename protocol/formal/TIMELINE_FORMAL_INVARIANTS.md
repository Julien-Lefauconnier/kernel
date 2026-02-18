# TIMELINE_FORMAL_INVARIANTS — Veramem Kernel

## 0. Scope

This document specifies the **formal invariants** of the Veramem Timeline kernel.

It is intentionally:
- **implementation-agnostic** (spec-level),
- **deterministic** (no hidden heuristics),
- **safety-first** (abstention when uncertainty exists).

It complements:
- `TIMELINE_DISTRIBUTED_MODEL.md` (distributed structure + merge model),
- `TIMELINE_TRUST_MODEL.md` (trust, anchors, threat posture),
- kernel tests (conformance / property / adversarial).

---

## 1. Entities and Notation

### 1.1 Entry

An entry is an immutable tuple:

\[
e = (\text{id}, \text{ts}, \text{payload})
\]

- `id` is unique and **deterministic** (derived from canonical encoding of stable components).
- `ts` is **not trusted** (distributed clock model).
- `payload` is opaque at this layer (bytes / canonical message).

### 1.2 Timeline

A timeline is a finite ordered sequence of entries:

\[
T = (e_1, e_2, \dots, e_n)
\]

### 1.3 Hashchain Commitment

Define a head commitment:

\[
H(T_0) = H_0 \quad \text{(genesis constant)}
\]
\[
H(T_k) = \text{hash}(H(T_{k-1}) \Vert \text{hash}(e_k))
\]

The value `H(T_n)` is the timeline head commitment.

### 1.4 Snapshot and Cursor Identity

A snapshot is:

\[
S = (\text{entries}, \text{head}, n)
\]

Identity is represented by the cursor:

\[
\text{cursor}(S) = (\text{head}, n)
\]

**Timestamp is excluded** from snapshot identity to tolerate clock drift.

### 1.5 Delta

Given two snapshots \( S_a, S_b \) derived from timelines \(T_a, T_b\) such that:

- \( n_a \le n_b \)
- the first \(n_a\) entries are identical

then:

\[
\Delta(S_a, S_b) = (e_{a+1}, \dots, e_b)
\]

---

## 2. Core Safety Invariants

### INV-1 — Immutability of Entries
**No entry changes once committed.**

Formally:
If an entry id exists at position \(k\) in timeline \(T\), then any valid extension timeline \(T'\) sharing prefix length \(k\) must satisfy:

\[
e_k(T) = e_k(T')
\]

Corollary: No in-place mutation, no overwrite, no edit.

---

### INV-2 — Append-Only Growth (Monotonicity)
A valid state transition can only extend the timeline:

\[
T \preceq T' \iff \exists m \ge 0 : T' = (e_1,\dots,e_n,e_{n+1},\dots,e_{n+m})
\]

No rollback is valid at the kernel level.

---

### INV-3 — Uniqueness of Entry IDs
Entry identifiers are globally unique within a timeline.

\[
\forall i \neq j,\ \text{id}(e_i) \neq \text{id}(e_j)
\]

Additionally, merge must refuse any operation producing an id collision.

---

### INV-4 — Hashchain Integrity
Commitments must correspond exactly to the ordered entries.

For all prefixes:

\[
H(T_k) = \text{hash}(H(T_{k-1}) \Vert \text{hash}(e_k))
\]

Any mismatch => corruption or adversarial tampering => invalid state.

---

### INV-5 — Snapshot Consistency
A snapshot is valid only if:

- `n` equals the number of entries carried,
- `head` equals the hashchain commitment of those entries.

\[
|S.entries| = S.n
\]
\[
S.head = H(S.entries)
\]

---

## 3. Fork Invariants

### 3.1 Fork Definition

Two timelines \(T^A, T^B\) are forked iff:

\[
\exists k \le \min(|T^A|,|T^B|) : e_k^A \neq e_k^B
\]

Let \(p\) be the maximal common prefix length. Then:

\[
T^A = (P, A_s), \quad T^B = (P, B_s)
\]

where:
- \(P\) is the common prefix,
- \(A_s, B_s\) are divergent suffixes.

---

### INV-6 — Fork Prefix Preservation
Any operation involving forked states must preserve the maximal common prefix:

No valid merge can rewrite \(P\).

---

### INV-7 — Fork Class Safety
A fork must be classified into exactly one of:

1. **Mergeable**: safe deterministic merge exists.
2. **Stable Divergence**: no safe merge exists, but each side is internally consistent.
3. **Malicious Fork**: integrity violations, replay/mutation evidence, or contradictions.

No operation may convert a Stable Divergence into convergence without new evidence.

---

## 4. Merge Invariants (Conditional Convergence)

### 4.1 Merge Goal
Merge is defined only for timelines that share a common prefix.

If merge is allowed, it returns a timeline \(T^M\) such that:

- It contains all entries from both suffixes (no loss),
- Order is deterministic,
- Hashchain is correct,
- Append-only is respected.

---

### INV-8 — Non-Destructive Merge
If merge succeeds:

\[
\{e \in T^A\} \cup \{e \in T^B\} \subseteq \{e \in T^M\}
\]

No entry from either input is dropped.

---

### INV-9 — Deterministic Merge Ordering
When merge is permitted, the ordering of merged suffix entries must be deterministic.

Canonical ordering key:

1. `timestamp` (as provided, but not trusted for identity)
2. `entry_id`

Formally, for suffix set \(U\), merge output suffix equals:

\[
\text{sort}(U,\ (\text{ts},\text{id}))
\]

If ordering cannot be made deterministic (ties not resolvable), merge must **refuse**.

---

### INV-10 — Merge Refusal on Ambiguity
Merge must be rejected if any of the following holds:

- entry id collision,
- inability to establish deterministic order,
- append-only violation,
- integrity violation (hash mismatch, malformed entry),
- temporal inconsistency rule violation (policy-defined),
- any conflicting structural commitment.

Refusal is a valid safe outcome.

---

## 5. Delta and Sync Invariants

### INV-11 — Delta Validity (Base Match)
A delta is valid only if the base snapshot matches the receiver snapshot cursor.

\[
\text{cursor}(S_{base}) = \text{cursor}(S_{receiver})
\]

Otherwise: reject delta (prevents replay against wrong base).

---

### INV-12 — Delta Integrity
Applying a delta must produce the target cursor.

Let applying delta yield snapshot \(S'\). Then:

\[
\text{cursor}(S') = \text{cursor}(S_{target})
\]

If not: invalid delta.

---

### INV-13 — Idempotence of Sync
Applying the same valid delta multiple times must not change state after first application.

If `apply(S, Δ)` succeeds:

\[
apply(apply(S,\Delta),\Delta) = apply(S,\Delta)
\]

If duplicates exist, they must be detected (e.g., by entry_id) and refused or ignored deterministically.

---

### INV-14 — Commutativity Under Safe Conditions
If two deltas are independent and mergeable under policy, applying them in any order yields the same final cursor.

\[
apply(apply(S,\Delta_1),\Delta_2) = apply(apply(S,\Delta_2),\Delta_1)
\]

If this cannot be guaranteed (dependency ambiguity), merge must refuse (abstention).

---

## 6. Determinism Invariants (Kernel-Level)

### INV-15 — Pure Deterministic Operations
All kernel operations that transform timeline state must be:

- pure (no side effects),
- deterministic given identical inputs.

For any kernel function \(f\):

\[
x = y \implies f(x) = f(y)
\]

---

### INV-16 — Canonical Encoding Stability
All cryptographic commitments, signatures, and identifiers must be derived only from canonical encodings.

If two encodings represent the same semantic structure, they must be byte-identical (or be rejected as non-canonical).

---

## 7. Stability and Abstention (ARVIS Principle)

### INV-17 — Safety over Liveness
If the system cannot prove a safe transformation, it must refuse.

This is a correctness condition, not an error.

---

### INV-18 — Eventual Stability (Not Forced Convergence)
A network is stable if:

\[
\forall (A,B),\ sync(A,B) \text{ produces no change}
\]

If safe convergence exists, the system may reach eventual consistency.
If safe convergence does not exist, the system must remain stable under divergence.

---

## 8. Trust-Related Kernel Invariants (Minimal)

This file does not define the full trust model (see `TIMELINE_TRUST_MODEL.md`),
but formalizes the minimum structural property:

### INV-19 — Signed Head Consistency (when signatures are used)
If a signed commitment exists, it must sign the **canonical representation** of the head cursor and/or head commitment.

Any mismatch => invalid signature.

---

## 9. Summary: What is “Correct” Timeline State?

A timeline state is considered **kernel-correct** iff:

1. It satisfies INV-1..INV-5 (structural integrity + append-only + hashchain),
2. Any forks are recognized and handled according to INV-6..INV-7,
3. Any merge/sync obeys INV-8..INV-14,
4. Determinism holds (INV-15..INV-16),
5. Abstention is allowed and treated as correct (INV-17..INV-18),
6. Optional signature rules hold when activated (INV-19).

---

## 10. Non-Goals

This specification does not define:
- semantic meaning of payload,
- higher-level resolution heuristics,
- probabilistic trust graphs,
- quorum overlays,
- governance or policy layer.

Those are explicitly layered above the kernel.
