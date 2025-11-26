import requests
from bs4 import BeautifulSoup
import markdownify
import pdfplumber
import re
import os

OUTPUT_FILE = "../backend/ai/base_conhecimento.md"

PAGES = [
    "https://www.unoesc.edu.br/cursos/engenharia-de-computacao",
    "https://www.unoesc.edu.br/sobre-a-unoesc/reitoria/",
    "https://www.unoesc.edu.br/atendimento-ao-estudante/bolsas-de-estudo/"
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
    return clean_text(markdown)

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
    return clean_text(text)

def fetch_ementario():
    print("📘 Buscando ementário das disciplinas...")

    subjects_url = "https://www.unoesc.edu.br/cursos/wp-json/wst/v1/subjects?course_id=4788"
    ementario_url_template = "https://www.unoesc.edu.br/cursos/wp-json/wst/v1/ementario?course_id=4788&subject_id={}&campus_id=600"

    try:
        resp = requests.get(subjects_url, verify=False, timeout=10)
        data = resp.json()
    except Exception as e:
        print("❌ Erro ao obter disciplinas:", e)
        return ""

    if not data.get("status", False):
        print("❌ Resposta inválida da API de subjects.")
        return ""

    subjects = data["data"]["subjects"]

    final_text = "## 📚 Ementário das Disciplinas\n\n"

    for subj in subjects:
        sid = subj["id"]
        title = subj["title"]
        credits = subj.get("credits")
        hours = subj.get("hours")
        fase = subj.get("codigoFase")

        print(f"🔎 Extraindo ementário: {title}")

        try:
            url = ementario_url_template.format(sid)
            r = requests.get(url, verify=False, timeout=10)
            ement = r.json()

            description = ement.get("data", {}).get("description", "Ementário não encontrado")
            description = clean_text(description)

        except Exception as e:
            description = f"Erro ao extrair ementário: {e}"

        final_text += f"""
### 📘 {title}

- Créditos: {credits}
- Carga horária: {hours}h
- Fase: {fase}

**Ementário:**  
{description}

---
"""

    return final_text


def fetch_professores():
    print("👨‍🏫 Buscando lista de professores...")

    url = "https://www.unoesc.edu.br/cursos/wp-json/wst/v1/teachers?course_id=4788&campus_id=600"

    try:
        resp = requests.get(url, verify=False, timeout=10)
        data = resp.json()
    except Exception as e:
        print("❌ Erro ao obter professores:", e)
        return ""

    if not data.get("status", False):
        print("❌ Resposta inválida da API de professores.")
        return ""

    professores = data["data"]

    final_text = "## 👨‍🏫 Professores do Curso\n\n"

    for prof in professores:
        name = prof.get("name", "Nome não informado")
        lattes = prof.get("lattes", "Sem link Lattes")
        pid = prof.get("id")

        final_text += f"""
### 👤 {name}
- ID: {pid}
- Lattes: {lattes}

---
"""

    return final_text

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

    ementario_md = fetch_ementario()
    final_md += "\n\n---\n## Ementário Completo\n\n"
    final_md += ementario_md

    professores_md = fetch_professores()
    final_md += "\n\n---\n## Professores\n\n"
    final_md += professores_md

    with open(OUTPUT_FILE, "w") as f:
        f.write(final_md)

    print(f"\n✅ Base de conhecimento gerada em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_knowledge_base()
