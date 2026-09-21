from __future__ import annotations

import logging
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parents[1]))

logger = logging.getLogger("bankassist.app")

from agents.bankassist.async_utils import run_sync  # noqa: E402
from agents.bankassist.prompts import DEFAULT_QUESTION  # noqa: E402
from agents.bankassist.service import ask_bankassist  # noqa: E402

st.set_page_config(page_title="BankAssist", page_icon="🏦", layout="wide")
st.title("BankAssist")
st.caption("Asistente grounded para analistas autorizados de cobranza de Banco ACME")

with st.sidebar:
    st.subheader("Controles de confianza")
    st.success("Políticas: ACTIVE + COLLECTIONS")
    st.info("La evaluación usa hechos estructurados y reglas deterministas.")
    st.warning("La respuesta es generada por IA y debe verificarse. La aprobación es humana.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Pregunta sobre elegibilidad de cobranza")
if st.button("Ejecutar caso de negocio", type="primary"):
    question = DEFAULT_QUESTION

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando Genie y la política vigente…"):
            try:
                result = run_sync(ask_bankassist(question))
            except Exception as exc:
                logger.exception("BankAssist query failed")
                st.error(f"No fue posible completar la consulta: {exc}")
            else:
                st.markdown(result.answer)
                st.caption(f"Latencia: {result.latency_seconds:.2f}s")
                with st.expander("Evaluación determinista"):
                    st.json(result.assessments)
                with st.expander("Evidencia y trazabilidad"):
                    st.json(result.evidence)
                st.session_state.messages.append(
                    {"role": "assistant", "content": result.answer}
                )
