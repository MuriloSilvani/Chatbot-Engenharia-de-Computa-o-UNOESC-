import requests
from bs4 import BeautifulSoup
import markdownify
import pdfplumber
import re
import os

OUTPUT_FILE = "../backend/ai/base_conhecimento.md"

PAGES = [
    "https://www.unoesc.edu.br/cursos/engenharia-de-computacao",
]

PDF_LINKS = [
    "https://www.unoesc.edu.br/cursos/wp-content/uploads/sites/2/2025/09/PPC-Engenharia-de-Computacao.pdf",
]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def fetch_html(url):
    print(f"🔎 Extraindo página: {url}")
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "footer", "header", "nav"]):
        tag.decompose()

    main = soup.find("main") or soup.body
    text_html = str(main)

    markdown = markdownify.markdownify(text_html, heading_style="ATX")
    markdown = clean_text(markdown)
    return markdown

def fetch_pdf(url):
    resp = requests.get(url, stream=True, verify=False)
    fname = "temp.pdf"
    with open(fname, "wb") as f:
        f.write(resp.content)
    text = ""
    with pdfplumber.open(fname) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    os.remove(fname)
    return text.strip()

def generate_knowledge_base():
    print("🧠 Gerando base de conhecimento...")
    final_md = "# Base de Conhecimento — Engenharia de Computação (UNOESC)\n\n"

    for page in PAGES:
        content = fetch_html(page)
        final_md += f"\n\n---\n## Conteúdo extraído de: {page}\n\n"
        final_md += content

    for pdf in PDF_LINKS:
        txt = fetch_pdf(pdf)
        if txt:
            final_md += f"## Fonte: {pdf}\n\n{txt}\n\n---\n"
        else:
            final_md += f"## Fonte: {pdf}\n\n*(Conteúdo não extraído — revisão manual necessária)*\n\n---\n"

    with open(OUTPUT_FILE, "w") as f:
        f.write(final_md)

    print(f"\n✅ Base de conhecimento gerada em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_knowledge_base()
