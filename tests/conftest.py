# tests/conftest.py

import pytest
from veramem_kernel.journals.knowledge.knowledge_journal import reset_knowledge_journal


@pytest.fixture(autouse=True)
def reset_knowledge_journal_between_tests():
    reset_knowledge_journal()
    yield
    reset_knowledge_journal()
