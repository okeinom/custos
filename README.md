# custos
Custos is a lightweight, policy-driven helper library for applying explicit, auditable guardrails to common data transformations at ingestion time.
=======
## Custos

Custos is a lightweight, policy-driven helper library for applying explicit, auditable guardrails to common data transformations at ingestion time.

Custos helps data engineers make routine transformations—such as JSON flattening, schema normalization, PII handling, and row-level quality checks—consistent, visible, and safe, without replacing existing tools or platforms.

Custos is Latin for “guardian.”

### Why Custos exists

In many data pipelines, the same transformation logic is repeatedly rewritten:

- flattening nested JSON

- renaming columns

- casting types

- masking or dropping PII

- filtering invalid rows

These transformations are often:

- implicit

- scattered across scripts

- hard to audit

- easy to change accidentally

Custos makes these decisions explicit by defining them once, as policy, and applying them consistently.

### What Custos is (and is not)
✅ Custos is

- A helper library, not a platform

- Policy-driven and explicit

- Designed for ingestion-time transformations

- Focused on correctness and auditability

- Easy to add — and easy to remove

❌ Custos is not

- A replacement for dbt, Spark, or SQL

- A data modeling tool

- An orchestration framework

- An auto-fixing or inference engine

- A governance or compliance platform

Custos deliberately avoids “magic.”
If data is changed, dropped, or rejected, it is logged and reported.

### Core features

- Controlled JSON flattening (with depth and array handling)

- Column renaming and schema normalization

- Type casting with explicit failure modes

- PII masking, hashing, or dropping

- Row-level data quality enforcement

- Structured audit reports for every run

### Design principles

- Explicit over clever

- Fail loudly or drop safely — never guess

- Policy as code

- Guardrails, not enforcement

- Low friction for developers

Custos is designed to complement existing pipelines, not redefine them.

### Quick example

```python
from custos import PolicyTransformer

transformer = PolicyTransformer(
    policy="policy.yml",
    mode="drop"   # strict | drop | dry_run
)

df_out, report = transformer.apply(df_in)
```

A single policy file controls what happens.
A structured report explains exactly what changed and why.

### When to use Custos

- In ingestion or staging pipelines

- When transforming semi-structured data

- When enforcing basic correctness early

- When you want repeatable, auditable transformations

### When not to use Custos

- For warehouse modeling (use dbt)

- For cross-table validation

- For complex business logic

- For inference-based data repair

### Status

Custos is currently early-stage and intentionally small.
The API is designed to be stable, predictable, and easy to reason about.
