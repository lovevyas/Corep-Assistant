from retriever import RuleRetriever
from llm import generate_structured_output
from schema import COREP_SCHEMA
from validator import validate
from audit import build_audit_log

retriever = RuleRetriever("../data/rules.txt")

question = input("Enter COREP question: ")
scenario = input("Describe scenario: ")

rules = retriever.retrieve(question)
result = generate_structured_output(question, scenario, rules, COREP_SCHEMA)

errors = validate(result["fields"])
audit = build_audit_log(result["fields"])

print("\n--- COREP OUTPUT ---")
print(result)

print("\n--- VALIDATION ERRORS ---")
print(errors)

print("\n--- AUDIT LOG ---")
print(audit)
