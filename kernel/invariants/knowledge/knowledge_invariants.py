# kernel/invariants/knowledge/knowledge_invariants.py

"""
KNOWLEDGE KERNEL INVARIANTS (NORMATIVE)

These invariants define the HARD guarantees of the Knowledge kernel.

The kernel:
- does NOT interpret knowledge
- does NOT infer truth
- does NOT evaluate correctness
- does NOT relate events semantically

It ONLY enforces structural and declarative validity.
"""

from kernel.journals.knowledge.knowledge_event import KnowledgeEvent


def assert_has_timestamp(event: KnowledgeEvent) -> None:
    """
    Invariant: every knowledge event must be time-bound.
    """
    if event.created_at is None:
        raise ValueError("KnowledgeEvent must have a created_at timestamp")


def assert_has_source(event: KnowledgeEvent) -> None:
    """
    Invariant: every knowledge event must declare a source.
    The source is opaque and never interpreted by the kernel.
    """
    if not event.source:
        raise ValueError("KnowledgeEvent must declare a non-empty source")


def assert_has_knowledge_type(event: KnowledgeEvent) -> None:
    """
    Invariant: every knowledge event must declare a knowledge type.
    The kernel does not interpret this value.
    """
    if not event.knowledge_type:
        raise ValueError("KnowledgeEvent must declare a non-empty knowledge_type")
