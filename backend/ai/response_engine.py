from ai.gemini_client import client
import os

BASE_PATH = "./ai/base_conhecimento.md"

def load_knowledge():
    return open(BASE_PATH).read()

def ask_gemini(question):
    context = load_knowledge()
    return context
