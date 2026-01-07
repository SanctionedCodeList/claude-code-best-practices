# Testable Code Examples

Skills contain code examples that demonstrate APIs and patterns. Without validation, these examples can drift from reality—referencing methods that were renamed, classes that don't exist, or syntax that's invalid.

## The Problem

Code examples in skills are typically **illustrative**, not **executable**:
- They reference files that don't exist (`Document("contract.docx")`)
- They assume previous state (`doc.replace(...)` without showing the import)
- They have no assertions

This creates **API drift risk**. We've seen bugs where documented methods didn't exist on the actual class.

## Solution: pytest-markdown-docs

Use [pytest-markdown-docs](https://github.com/modal-labs/pytest-markdown-docs) to run Python code blocks from markdown files as tests.

### Setup

1. Install the package:
   ```bash
   pip install pytest-markdown-docs
   ```

2. Create `conftest.py` adjacent to your skill markdown files:
   ```python
   import pytest

   def pytest_markdown_docs_globals():
       """Provide globals available to all markdown code blocks."""
       from my_library import Document
       from my_library.errors import TextNotFoundError

       return {
           "Document": Document,
           "TextNotFoundError": TextNotFoundError,
       }

   @pytest.fixture
   def sample_doc(tmp_path):
       """Create a sample document for testing."""
       from my_library import Document
       doc = Document()
       doc.add_paragraph("Sample content")
       path = tmp_path / "sample.docx"
       doc.save(path)
       return str(path)
   ```

3. Run tests:
   ```bash
   pytest --markdown-docs skills/
   ```

### Markers

Use fence info markers to control test behavior:

| Marker | Description |
|--------|-------------|
| `fixture:name` | Inject pytest fixture as variable |
| `notest` | Skip this block entirely |
| `continuation` | Share namespace with previous block |

#### Testable Block (with fixture)

````markdown
```python fixture:sample_doc
from my_library import Document

doc = Document(sample_doc)  # sample_doc injected from fixture
doc.replace("old", "new")
```
````

#### Non-testable Block

Use `notest` for:
- Anti-pattern examples showing what NOT to do
- Method signatures or API reference
- Examples using external services
- Examples with non-existent APIs (future work)

````markdown
```python notest
# This shows what NOT to do
para.text = para.text.replace("old", "new")  # DESTROYS FORMATTING
```
````

### Fixture Design

Create fixtures that provide documents with content matching your examples:

```python
@pytest.fixture
def contract_doc(tmp_path):
    """Create a contract document with common terms."""
    from docx import Document  # Use raw python-docx for creation

    doc = Document()
    doc.add_paragraph("Payment is due within 30 days.")
    doc.add_paragraph("The Contractor agrees to...")

    path = tmp_path / "contract.docx"
    doc.save(str(path))
    return str(path)
```

**Key insight:** Use the underlying library (python-docx) for fixture creation, not your high-level wrapper. This tests your wrapper's actual behavior.

### When to Use Each Marker

| Content Type | Marker |
|--------------|--------|
| Working code example | `fixture:name` |
| Anti-pattern/what not to do | `notest` |
| Method signature docs | `notest` |
| Pseudocode/partial examples | `notest` |
| Future/planned API | `notest` |
| External service examples | `notest` |

### Benefits

1. **Catches API drift** - Tests fail when documented methods don't exist
2. **Validates syntax** - Typos and unclosed brackets caught
3. **Ensures imports work** - Module/class names verified
4. **Tests real behavior** - Examples actually run against your library

### Integration with CI

Add to your test suite:

```toml
# pyproject.toml
[project.optional-dependencies]
dev = [
    "pytest-markdown-docs>=0.9.0",
]
```

```yaml
# .github/workflows/test.yml
- name: Test documentation examples
  run: pytest --markdown-docs skills/ --no-cov
```

### Gradual Adoption

For existing skills with many code blocks:

1. Start by adding `notest` to all blocks
2. Convert high-value examples to use fixtures
3. Focus on "golden path" examples users will copy
4. Leave reference/signature blocks as `notest`

You don't need 100% executable coverage. Focus on examples that:
- Users will copy verbatim
- Demonstrate core API methods
- Have failed before due to API changes

### Example: Before and After

**Before (untested):**
````markdown
```python
from my_library import Document

doc = Document("contract.docx")
doc.replace("30 days", "45 days")
```
````

**After (tested with fixture):**
````markdown
```python fixture:contract_doc
from my_library import Document

doc = Document(contract_doc)
doc.replace("30 days", "45 days", track=True)
```
````

The fixture creates a temporary file with "30 days" content, the test runs against it, and pytest cleans up automatically.
