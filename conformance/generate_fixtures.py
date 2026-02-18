# conformance/generate_fixtures.py
"""
Veramem Kernel — Conformance Fixture Generator (V1)

⚠️ Standard-quality rules (MUST):
- Regenerate fixtures whenever the wire format changes (TLV schema/tags, domain bytes, version tags),
  canonical encoding changes, cryptographic primitives change, or ordering/merge rules change.
- This generator MUST be deterministic: same inputs => same bytes.
- Fixtures MUST be treated as protocol golden vectors (do not edit by hand).

Recommended CI guard:
    python conformance/generate_fixtures.py
    git diff --exit-code conformance/fixtures/

This file intentionally uses a fixed conformance key and fixed test vectors.
The key is NOT secret. It is a public test vector key.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Callable, Dict, Any, Tuple
import json
import os
import sys
import time

from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.common.ed25519_signer import Ed25519Signer
from veramem_kernel.common.device_attestation import DeviceAttestation
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_delta import TimelineDelta
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_merge import TimelineMerge, TimelineMergeResult
from veramem_kernel.journals.timeline.timeline_reconcile import TimelineReconcileDecision

from conformance.utils import build_entry

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ============================================================
# Global configuration (public test vectors)
# ============================================================

GENERATOR_VERSION = "v1"
FIXTURE_SET = "veramem-kernel-conformance"
WIRE_VERSION = 1  # semantic marker for docs/logs (wire tags are inside encoders)

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Public conformance key (NOT SECRET). 32 bytes minimum enforced.
CONFORMANCE_KEY = b"veramem-conformance-key".ljust(32, b"!")
SIGNER = HmacSigner(key=CONFORMANCE_KEY)

# Public deterministic challenge
ATTESTATION_CHALLENGE = b"conformance-challenge"

# Deterministic entry ranges used across fixtures
BASE_RANGE = range(0, 5)      # 5 entries
DELTA_TOTAL_RANGE = range(0, 10)  # 10 entries total
LEFT_SUFFIX_RANGE = range(5, 8)   # 3 entries
RIGHT_SUFFIX_RANGE = range(105, 108)  # 3 entries (force disjoint IDs)


# ============================================================
# IO helpers
# ============================================================

def _mkdir_clean(dirpath: Path) -> None:
    dirpath.mkdir(parents=True, exist_ok=True)


def _write_bytes(path: Path, data: bytes) -> None:
    # Always overwrite; fixtures are deterministic.
    path.write_bytes(data)


def _write_json(path: Path, obj: Dict[str, Any]) -> None:
    # Stable JSON output: sorted keys, LF, utf-8, deterministic formatting.
    path.write_text(
        json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _sha256_hex(b: bytes) -> str:
    return sha256(b).hexdigest()


def _file_sha256_hex(path: Path) -> str:
    return _sha256_hex(path.read_bytes())


def _banner() -> None:
    print(f"{FIXTURE_SET} fixture generator ({GENERATOR_VERSION})")
    print(f"- wire_version_hint: {WIRE_VERSION}")
    print(f"- conformance_key_sha256: {_sha256_hex(CONFORMANCE_KEY)}")
    print(f"- fixtures_dir: {FIXTURES_DIR}")
    print("")


# ============================================================
# Fixture generation
# ============================================================

@dataclass(frozen=True)
class FixtureSpec:
    name: str
    gen: Callable[[], Tuple[bytes, Dict[str, Any]]]
    bin_filename: str
    json_filename: str


def _entries(rng) -> list:
    # build_entry is assumed deterministic
    return [build_entry(i) for i in rng]


def generate_attestation() -> Tuple[bytes, Dict[str, Any]]:
    snap = TimelineSnapshot.build(_entries(BASE_RANGE))
    commitment = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=commitment, signer=SIGNER)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=SIGNER,
        challenge=ATTESTATION_CHALLENGE,
    )

    raw = att.to_bytes()

    info = {
        "fixture": "attestation_v1",
        "challenge_sha256": _sha256_hex(ATTESTATION_CHALLENGE),
        "commitment_hex": commitment.commitment,
        "signed_commitment_algo": signed.signature.algo,
        "attestation_algo": att.response.algo,
        "binary_sha256": _sha256_hex(raw),
        # Traceability: tie fixture to the generator and key hash
        "generator": {
            "fixture_set": FIXTURE_SET,
            "generator_version": GENERATOR_VERSION,
            "wire_version_hint": WIRE_VERSION,
            "conformance_key_sha256": _sha256_hex(CONFORMANCE_KEY),
        },
    }
    return raw, info


def generate_attestation_ed25519() -> Tuple[bytes, Dict[str, Any]]:
    """
    Deterministic Ed25519 attestation fixture.

    This fixture provides asymmetric crypto test vectors for
    interoperability and long-term cryptographic agility.
    """

    # Deterministic seed (public, NOT secret)
    seed_material = b"veramem-ed25519-conformance-seed-0001"
    seed = sha256(seed_material).digest()
    signer = Ed25519Signer.from_seed(seed)

    challenge = b"conformance-challenge-ed25519"

    snap = TimelineSnapshot.build(_entries(BASE_RANGE))
    commitment = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(
        commitment=commitment,
        signer=signer,
    )

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = att.to_bytes()

    info = {
        "fixture": "attestation_ed25519_v1",
        "challenge_sha256": _sha256_hex(challenge),
        "commitment_hex": commitment.commitment,
        "signed_commitment_algo": signed.signature.algo,
        "attestation_algo": att.response.algo,
        "binary_sha256": _sha256_hex(raw),
        "generator": {
            "fixture_set": FIXTURE_SET,
            "generator_version": GENERATOR_VERSION,
            "wire_version_hint": WIRE_VERSION,
            "seed_sha256": _sha256_hex(seed),
        },
    }

    return raw, info



def generate_timeline_delta() -> Tuple[bytes, Dict[str, Any]]:
    entries = _entries(DELTA_TOTAL_RANGE)
    snap1 = TimelineSnapshot.build(entries[:5])
    snap2 = TimelineSnapshot.build(entries)

    delta = TimelineDelta.from_snapshots(snap1, snap2)
    raw = delta.to_bytes()

    info = {
        "fixture": "timeline_delta_v1",
        "description": "Timeline delta between snapshot1 (first 5) and snapshot2 (first 10).",
        "entries_added": 5,
        "base_total_entries": 5,
        "target_total_entries": 10,
        "binary_sha256": _sha256_hex(raw),
        "generator": {
            "fixture_set": FIXTURE_SET,
            "generator_version": GENERATOR_VERSION,
            "wire_version_hint": WIRE_VERSION,
        },
    }
    return raw, info


def generate_timeline_fork() -> Tuple[bytes, Dict[str, Any]]:
    base_entries = _entries(BASE_RANGE)
    local = TimelineSnapshot.build(base_entries + _entries(LEFT_SUFFIX_RANGE))
    remote = TimelineSnapshot.build(base_entries + _entries(RIGHT_SUFFIX_RANGE))

    fork = TimelineFork.detect(local, remote)
    raw = fork.to_bytes()

    info = {
        "fixture": "timeline_fork_v1",
        "kind": fork.kind.value,
        "common_prefix_len": fork.common_prefix_len,
        "left_total_entries": fork.left_total_entries,
        "right_total_entries": fork.right_total_entries,
        "binary_sha256": _sha256_hex(raw),
        "generator": {
            "fixture_set": FIXTURE_SET,
            "generator_version": GENERATOR_VERSION,
            "wire_version_hint": WIRE_VERSION,
        },
    }
    return raw, info


def generate_timeline_merge() -> Tuple[bytes, Dict[str, Any]]:
    base_entries = _entries(BASE_RANGE)
    local = TimelineSnapshot.build(base_entries + _entries(LEFT_SUFFIX_RANGE))
    remote = TimelineSnapshot.build(base_entries + _entries(RIGHT_SUFFIX_RANGE))

    fork = TimelineFork.detect(local, remote)
    res: TimelineMergeResult = TimelineMerge.try_merge(fork=fork, local=local, remote=remote)
    raw = res.to_bytes()

    info = {
        "fixture": "timeline_merge_v1",
        "kind": res.kind.value,
        "reason": res.reason,
        "merged_total_entries": len(res.merged.entries) if res.merged else None,
        "binary_sha256": _sha256_hex(raw),
        "generator": {
            "fixture_set": FIXTURE_SET,
            "generator_version": GENERATOR_VERSION,
            "wire_version_hint": WIRE_VERSION,
        },
    }
    return raw, info


def generate_timeline_reconcile() -> Tuple[bytes, Dict[str, Any]]:
    base_entries = _entries(BASE_RANGE)
    local = TimelineSnapshot.build(base_entries + _entries(LEFT_SUFFIX_RANGE))
    remote = TimelineSnapshot.build(base_entries + _entries(RIGHT_SUFFIX_RANGE))

    fork = TimelineFork.detect(local, remote)
    decision = TimelineReconcileDecision.from_fork_keep_both(fork)
    raw = decision.to_bytes()

    info = {
        "fixture": "timeline_reconcile_v1",
        "decision": decision.kind.value,
        "common_prefix_len": decision.common_prefix_len,
        "binary_sha256": _sha256_hex(raw),
        "generator": {
            "fixture_set": FIXTURE_SET,
            "generator_version": GENERATOR_VERSION,
            "wire_version_hint": WIRE_VERSION,
        },
    }
    return raw, info


# ============================================================
# Fixture registry & verification
# ============================================================

FIXTURES: Tuple[FixtureSpec, ...] = (
    FixtureSpec(
        name="attestation_v1",
        gen=generate_attestation,
        bin_filename="attestation_v1.bin",
        json_filename="attestation_v1.json",
    ),
    FixtureSpec(
        name="attestation_ed25519_v1",
        gen=generate_attestation_ed25519,
        bin_filename="attestation_ed25519_v1.bin",
        json_filename="attestation_ed25519_v1.json",
    ),
    FixtureSpec(
        name="timeline_delta_v1",
        gen=generate_timeline_delta,
        bin_filename="timeline_delta_v1.bin",
        json_filename="timeline_delta_v1.json",
    ),
    FixtureSpec(
        name="timeline_fork_v1",
        gen=generate_timeline_fork,
        bin_filename="timeline_fork_v1.bin",
        json_filename="timeline_fork_v1.json",
    ),
    FixtureSpec(
        name="timeline_merge_v1",
        gen=generate_timeline_merge,
        bin_filename="timeline_merge_v1.bin",
        json_filename="timeline_merge_v1.json",
    ),
    FixtureSpec(
        name="timeline_reconcile_v1",
        gen=generate_timeline_reconcile,
        bin_filename="timeline_reconcile_v1.bin",
        json_filename="timeline_reconcile_v1.json",
    ),
)


def _self_check() -> None:
    # Hard invariants for standard-quality generation.
    if len(CONFORMANCE_KEY) < 32:
        raise SystemExit("CONFORMANCE_KEY must be >= 32 bytes")
    if ATTESTATION_CHALLENGE == b"":
        raise SystemExit("ATTESTATION_CHALLENGE must not be empty")
    _mkdir_clean(FIXTURES_DIR)


def _regenerate_all() -> Dict[str, str]:
    """
    Generate all fixtures and write bin+json.
    Returns a manifest mapping fixture name -> binary sha256.
    """
    manifest: Dict[str, str] = {}
    for spec in FIXTURES:
        raw, info = spec.gen()

        bin_path = FIXTURES_DIR / spec.bin_filename
        json_path = FIXTURES_DIR / spec.json_filename

        _write_bytes(bin_path, raw)
        _write_json(json_path, info)

        # Record in manifest
        manifest[spec.name] = _sha256_hex(raw)

    return manifest


def _write_manifest(manifest: Dict[str, str]) -> None:
    """
    Write an overall manifest to support third-party audit and CI pinning.
    """
    out = {
        "fixture_set": FIXTURE_SET,
        "generator_version": GENERATOR_VERSION,
        "wire_version_hint": WIRE_VERSION,
        "conformance_key_sha256": _sha256_hex(CONFORMANCE_KEY),
        "generated_at_unix": int(time.time()),
        "fixtures": manifest,
    }
    _write_json(FIXTURES_DIR / "manifest_v1.json", out)


def main() -> int:
    _self_check()
    _banner()

    manifest = _regenerate_all()
    _write_manifest(manifest)

    # Print summary (useful for CI logs)
    print("Generated fixtures:")
    for name, digest in sorted(manifest.items()):
        print(f"- {name}: sha256={digest}")
    print(f"- manifest_v1.json: sha256={_file_sha256_hex(FIXTURES_DIR / 'manifest_v1.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
