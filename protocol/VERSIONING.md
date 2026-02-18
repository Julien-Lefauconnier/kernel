# Veramem Protocol Versioning

## 1. Purpose

This document defines the versioning strategy of the Veramem protocol.

It ensures long-term compatibility and stable evolution.

---

## 2. Versioning Principles

Veramem follows:

* explicit versioning,
* backward compatibility,
* deterministic upgrades.

---

## 3. Protocol Versions

Each canonical message includes:

* a domain version,
* a wire format version.

Example:

```
veramem.timeline.entry.v1
```

---

## 4. Backward Compatibility

Stable versions MUST remain valid indefinitely.

New implementations MUST support previous stable formats.

---

## 5. Breaking Changes

A breaking change requires:

* new domain version,
* new conformance vectors,
* migration strategy.

---

## 6. Non-Breaking Changes

Allowed:

* optional fields,
* new algorithms,
* additional profiles.

---

## 7. Deprecation

Deprecated features:

* remain readable,
* must not break historical data.

---

## 8. Migration

Implementations should support:

* parallel formats,
* incremental upgrade.

---

## 9. Long-Term Stability

The protocol is designed for:

* decades of operation,
* archival resilience.

---

## 10. Conclusion

Versioning ensures safe and predictable evolution.
