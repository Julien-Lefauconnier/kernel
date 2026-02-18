"""
Identity & Attestation Example (generic).

This example demonstrates:
- zero-trust identity
- device or agent attestation
- cryptographic verification
- append-only identity history
- temporal trust evolution
- independent verification

This scenario is intentionally domain-agnostic.

It can represent:
- AI agent identity
- device integrity
- secure edge infrastructure
- distributed authentication
- digital sovereignty
- long-term trust frameworks
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.api.attestation import (
    create_device_attestation,
    verify_device_attestation,
)
from veramem_kernel.api.crypto import generate_hmac_key


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Step 1: root of trust ---
    timeline = TimelineJournal()

    # Secret known only to the trusted device or agent
    device_secret = generate_hmac_key()

    print("Device secret generated.")

    # --- Step 2: device attestation ---
    attestation = create_device_attestation(
        device_id="generic-device-001",
        firmware_hash=b"firmware-v1",
        signer_key=device_secret,
    )

    # Record attestation in the kernel
    timeline.append_signal(attestation.signal)

    print("Device attested and recorded.")

    print_timeline("Kernel timeline", timeline)

    # --- Step 3: independent verifier ---
    verifier = TimelineJournal()

    for entry in timeline.entries():
        verifier.append_signal(entry.signal)

    print("\nVerifier reconstructed identity history.")

    # --- Step 4: verify trust ---
    is_valid = verify_device_attestation(
        attestation,
        expected_device_id="generic-device-001",
        signer_key=device_secret,
    )

    print("\nVerification result:", is_valid)

    if is_valid:
        print("Zero-trust identity verified.")
    else:
        print("Attestation invalid.")

    # --- Step 5: evolution of trust ---
    # Device firmware update
    attestation_v2 = create_device_attestation(
        device_id="generic-device-001",
        firmware_hash=b"firmware-v2",
        signer_key=device_secret,
    )

    timeline.append_signal(attestation_v2.signal)

    print("\nDevice firmware updated and re-attested.")

    print_timeline("Updated identity history", timeline)

    print("\nProperties demonstrated:")
    print("- No implicit trust")
    print("- Cryptographic identity")
    print("- Historical traceability")
    print("- Independent verification")
    print("- Temporal trust evolution")
    print("- Zero-trust infrastructure")


if __name__ == "__main__":
    main()
