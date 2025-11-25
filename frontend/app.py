import streamlit as st
import requests

st.set_page_config(page_title="Chatbot Engenharia UNOESC", page_icon="🤖")

st.title("🤖 Chatbot – Engenharia de Computação (UNOESC)")
st.write("Digite sua pergunta sobre o curso:")

question = st.text_input("Pergunta")

if st.button("Enviar"):
    if question.strip() == "":
        st.warning("Digite alguma pergunta!")
    else:
        response = requests.post(
            "http://localhost:5000/ask",
            json={"question": question}
        )
        answer = response.json()["answer"]
        st.chat_message("assistant").markdown(answer)
