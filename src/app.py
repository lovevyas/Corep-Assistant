import streamlit as st

from retriever import RuleRetriever
from llm import generate_structured_output
from schema import COREP_SCHEMA
from validator import validate
from audit import build_audit_log

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="COREP Regulatory Assistant",
    layout="wide"
)

st.title("🧠 COREP Regulatory Reporting Assistant")
st.caption("LLM-assisted prototype for PRA COREP Own Funds reporting")

# ---------- INIT RETRIEVER ----------
@st.cache_resource
def load_retriever():
    return RuleRetriever("../data/rules.txt")

retriever = load_retriever()

# ---------- INPUT SECTION ----------
st.subheader("🔍 Input")

question = st.text_area(
    "COREP Question",
    value="What should be reported for own funds?",
    height=80
)

scenario = st.text_area(
    "Reporting Scenario",
    value="Bank has CET1 of 100 and AT1 of 40",
    height=80
)

run = st.button("Run COREP Assistant")

# ---------- PROCESS ----------
if run:
    with st.spinner("Running regulatory analysis..."):
        rules = retriever.retrieve(question)
        result = generate_structured_output(
            question,
            scenario,
            rules,
            COREP_SCHEMA
        )
        errors = validate(result["fields"])
        audit_log = build_audit_log(result["fields"])

    st.success("Analysis complete")

    # ---------- OUTPUT ----------
    st.subheader("📄 COREP Template Output")

    for field in result["fields"]:
        with st.container():
            st.markdown(f"### Field {field['field_id']}")
            st.write("**Value:**", field["value"])
            st.write("**Justification:**", field["justification"])
            st.divider()

    # ---------- VALIDATION ----------
    st.subheader("✅ Validation Results")
    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("No validation errors detected")

    # ---------- AUDIT TRAIL ----------
    st.subheader("🧾 Audit Trail")
    for entry in audit_log:
        st.write(
            f"**Field {entry['field']}** → {entry['justification']}"
        )

    # ---------- RETRIEVED RULES ----------
    with st.expander("📚 Retrieved Regulatory Text"):
        for r in rules:
            st.write("-", r)
