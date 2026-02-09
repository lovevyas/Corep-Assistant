
# COREP Own Funds Reporting Assistant (Prototype)

## Overview

This project is a small prototype that explores how a Large Language Model (LLM) can assist with COREP Own Funds (Template C 01.00) regulatory reporting.

The purpose of this project is to learn and demonstrate:
- how regulatory concepts map to COREP template fields,
- how natural-language scenarios can be converted into structured outputs,
- and how validation and auditability can be kept separate from AI reasoning.

This is not a production system.
It is a learning-focused prototype with a deliberately limited scope.

---

## Problem Background

COREP reporting requires analysts to:
- read regulatory text,
- interpret how it applies to a bank’s situation,
- and populate specific COREP rows correctly.

This process is mostly manual and can be error-prone.

This prototype explores whether an LLM can assist analysts by:
- extracting values from plain-language scenarios,
- mapping them to COREP rows,
- and explaining how each value was derived.

---

## Scope of the Prototype

### In Scope
- COREP C 01.00 – Own Funds
- Rows:
  - Row 010 — Common Equity Tier 1 (CET1)
  - Row 020 — Additional Tier 1 (AT1)
  - Row 040 — Tier 2 Capital
  - Row 030 — Total Own Funds
- Natural-language questions and scenarios
- Basic validation and audit trail
- Local UI for interaction

### Out of Scope
- Other COREP templates
- Capital eligibility rules and deductions
- Regulatory buffers and ratios
- Full PRA taxonomy coverage
- Data storage or authentication

---

## How the System Works

User Question + Scenario  
↓  
Rule Retrieval (rules.txt)  
↓  
LLM extracts structured values  
↓  
COREP schema limits allowed fields  
↓  
Validation checks consistency  
↓  
Audit trail explains results  

Each step is kept separate so that AI handles interpretation, while validation remains deterministic.

---

## Key Design Choices

- Structured Output: The LLM outputs only schema-defined COREP fields.
- No Guessing: Missing values are returned as "MISSING".
- Simple Validation: Total Own Funds = CET1 + AT1 + Tier 2 (when present).

---

## Example Usage

### Example 1: Complete Own Funds Data

Question:
What should be reported for own funds?

Scenario:
Bank has CET1 of 100, AT1 of 40, and Tier 2 capital of 20.

Output:
- Row 010 → 100
- Row 020 → 40
- Row 040 → 20
- Row 030 → 160

---

### Example 2: Missing Data

Scenario:
Bank has CET1 of 100 and AT1 of 40.

Output:
- Row 010 → 100
- Row 020 → 40
- Row 040 → MISSING
- Row 030 → MISSING

---

## Testing Approach

The prototype was tested using complete, missing, and contradictory data scenarios.
The goal was to ensure the system does not crash, does not guess values, and always explains outputs.

---

## Known Limitations

- Missing values are not inferred as zero
- Validation rules are simplified
- Only one COREP template is supported

---

## Why This Project

This project helped me understand how regulatory rules map to structured templates, where LLMs are useful, and where they should not be trusted.

The focus was on learning and correct design, not completeness.

---

## How to Run

pip install -r requirements.txt  
streamlit run src/app.py  

---

## Final Notes

This prototype is intended as a learning and demonstration project and shows careful use of LLMs in a regulated-style workflow.
