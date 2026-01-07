# Data Models for AI Systems

This reference covers best practices for designing data models and structured output schemas that AI agents will read or write.

## Table of Contents

- [Structured vs Prose Fields](#structured-vs-prose-fields)
- [Structured Output Best Practices](#structured-output-best-practices)

## Structured vs Prose Fields

When designing data models that AI agents will read or write, avoid over-structuring. AI agents don't need the same rigid schemas that traditional software does.

**Use structured fields for:**
- Identity/lookup fields (IDs, names, types) - needed for joins and queries
- Numeric values used in calculations - need to be parseable
- Enums with small, fixed option sets - genuinely constrained choices

**Use prose fields for:**
- Analysis, reasoning, or assessment content
- Data with high variability across instances
- Information that will be read by AI agents (they parse prose just fine)

```python
# Over-structured (bad for AI systems)
class CompanyProfile(BaseModel):
    revenue_low: float
    revenue_mid: float
    revenue_high: float
    revenue_currency: str
    revenue_source: str
    revenue_confidence: str
    market_cap: float
    market_cap_source: str
    # ... 20 more fields

# Right-sized (good for AI systems)
class CompanyProfile(BaseModel):
    company_id: str           # Structured: needed for lookups
    legal_name: str           # Structured: needed for display
    company_type: Literal[...] # Structured: small fixed set
    financial_profile: str    # Prose: high variability, AI-readable
    risk_assessment: str      # Prose: analysis content
```

**Key insight:** If an AI agent is the consumer, it can extract what it needs from prose. Strict structuring just constrains the producer without benefiting the consumer.

## Structured Output Best Practices

When skills instruct LLMs to produce structured output (JSON schemas, Pydantic models), follow these guidelines to avoid degrading reasoning quality.

### Field Count Limit

Keep schemas under **30 fields** for reasoning-heavy tasks. Research shows performance degrades significantly above this threshold:

| Complexity | Fields | Success Rate |
|------------|--------|--------------|
| Easy | <30 | 75-96% |
| Medium | 30-100 | 52-79% |
| Hard | 100+ | Major failures |

### Schema Ordering

Put analysis/reasoning fields **before** conclusion fields. LLMs process schemas sequentially—if the answer field comes first, it short-circuits chain-of-thought reasoning.

```python
# Good: reasoning before conclusions
class AnalysisOutput(BaseModel):
    analysis: str           # Reasoning first
    evidence: str
    conclusion: str         # Conclusion last
    confidence: str

# Bad: conclusion before reasoning
class AnalysisOutput(BaseModel):
    conclusion: str         # Forces premature conclusion
    confidence: str
    analysis: str
```

### Prefer Simple Fields for Prose

When a field will contain paragraph-length analysis, use a single open-ended field rather than breaking it into constrained sub-elements:

```python
# Good: single field for free-form analysis
analysis: str = Field(..., description="Detailed analysis of the evidence")

# Bad: artificially constrained structure
analysis_introduction: str
analysis_point_1: str
analysis_point_2: str
analysis_conclusion: str
```

Breaking prose into multiple fields unnecessarily constrains the LLM and degrades output quality without adding value.

### Nesting Depth

Keep nesting to **3 levels or less**. Deep nesting (>5 levels) causes significant failures even in frontier models.

**Note:** These thresholds are based on 2024-2025 research and may loosen as models improve. When in doubt, simpler schemas produce better reasoning.
