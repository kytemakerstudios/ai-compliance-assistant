import streamlit as st
from app import ask_agent

st.set_page_config(page_title="RegulaAI")

st.title("🛡️ RegulaAI – Compliance Copilot")

st.warning(
    "⚠️ Demo only. Do NOT input real personal or health data."
)

role = st.selectbox(
    "Select role",
    ["product_manager", "data_scientist", "engineer"]
)

query = st.text_input("Ask a compliance question")

if st.button("Analyze"):
    result = ask_agent(query, role)

    st.write("### Risk Level")
    st.write(result["risk_level"])

    st.write("### Answer")
    st.write(result["answer"])

    st.write("### Reasoning")
    st.write(result["reasoning"])

    st.write("### Guidance")
    st.write(result["role_guidance"])

    st.write("### Sources")
    st.write(result["sources"])
