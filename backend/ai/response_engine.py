from ai.gemini_client import client
import os

BASE_PATH = "./ai/base_conhecimento.md"

def load_knowledge():
    return open(BASE_PATH).read()

def ask_gemini(question, context):
    knowledge = load_knowledge()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Você é um agente especializado em responder perguntas sobre o curso de Engenharia de Computação
        SOMENTE usando as informações da base de conhecimento.

        BASE DE CONHECIMENTO:
        {knowledge}

        HISTORICO DE PERGUNTAS E RESPOSTAS:
        {context}

        Pergunta do usuário:
        {question}

        Responda de forma objetiva, clara e sem inventar informações.
        """
    )

    return response.text
