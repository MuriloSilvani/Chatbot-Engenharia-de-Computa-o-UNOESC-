import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:4000")

st.set_page_config(page_title="Chatbot – Engenharia de Computação (UNOESC)", page_icon="🤖")

st.title("🤖 Chatbot – Engenharia de Computação (UNOESC)")
st.write("Digite sua pergunta sobre o curso:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

with st.form("chat_form"):
    question = st.text_input("Pergunta", placeholder="Digite sua pergunta...")
    submitted = st.form_submit_button("Enviar")

if submitted:
    if question.strip() == "":
        st.warning("Digite alguma pergunta!")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })
        st.chat_message("user").markdown(question)

        with st.spinner("Carregando resposta..."):
            try:
                response = requests.post(
                    BACKEND_URL + "/ask",
                    json={"question": question}
                )
                answer = response.json().get("answer", "Erro ao gerar resposta.")
            except Exception as e:
                answer = f"Erro ao conectar ao backend: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
        st.chat_message("assistant").markdown(answer)

        st.rerun()
