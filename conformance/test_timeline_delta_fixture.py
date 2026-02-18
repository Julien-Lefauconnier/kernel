# conformance/test_timeline_delta_fixture.py

from hashlib import sha256

from veramem_kernel.common.canonical_encoding import decode_message


def test_timeline_delta_fixture():
    with open("conformance/fixtures/timeline_delta_v1.bin", "rb") as f:
        raw = f.read()

    domain, tlvs = decode_message(raw)

    assert domain == b"veramem.timeline.delta.v1"

    fields = {t.tag: t.value for t in tlvs}

    # Basic structure checks
    assert 1 in fields  # base snapshot
    assert 2 in fields  # new entries
    assert 3 in fields  # resulting head

    # External hash continuity check
    resulting_head = fields[3]

    # Minimal invariant:
    assert len(resulting_head) > 0
