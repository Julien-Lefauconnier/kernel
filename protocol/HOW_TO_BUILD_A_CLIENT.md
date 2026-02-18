# How to Build a Veramem Client

## 1. Purpose

This guide explains how to implement a minimal Veramem-compatible client.

---

## 2. Minimal Requirements

A client must implement:

1. Canonical encoding.
2. Timeline structure.
3. Commitment computation.
4. Delta synchronization.
5. Attestation verification.

---

## 3. Step-by-Step Implementation

### Step 1 — Canonical Encoding

Implement TLV deterministic encoding.

Follow:

* strict ordering,
* domain separation.

---

### Step 2 — Timeline

Implement:

* append-only entries,
* immutable storage.

---

### Step 3 — Commitment

Compute hashchain.

---

### Step 4 — Delta

Support:

* forward-only sync,
* replay protection.

---

### Step 5 — Fork Detection

Detect prefix divergence.

---

### Step 6 — Merge

Implement safe deterministic merge.

---

### Step 7 — Attestation

Implement challenge-response verification.

---

## 4. Validation

Run the conformance suite.

---

## 5. Security Requirements

The client must:

* refuse unsafe operations,
* verify all commitments,
* abstain under uncertainty.

---

## 6. Reference Languages

Recommended:

* Rust,
* Go,
* WebAssembly.

---

## 7. Conclusion

A minimal client can be implemented in a few thousand lines.

The focus must remain on determinism and safety.
