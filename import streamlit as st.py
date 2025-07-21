import streamlit as st
import openai
import fitz  # PyMuPDF

# Sicherer Zugriff auf den API-Schlüssel
openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

st.title("📄 PDF Analyzer mit GPT-3.5")

pdf_file = st.file_uploader("📤 Lade ein PDF hoch", type=["pdf"])

if pdf_file:
    raw_text = extract_text_from_pdf(pdf_file)
    st.text_area("📄 Ausgelesener Text (Vorschau)", raw_text[:2000], height=300)

    if st.button("🔍 Mit GPT analysieren"):
        with st.spinner("GPT denkt nach..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "user",
                        "content": f"Fasse diesen PDF-Text zusammen:\n\n{raw_text}"
                    }]
                )
                antwort = response['choices'][0]['message']['content']
                st.subheader("🧠 GPT-Antwort:")
                st.write(antwort)
            except Exception as e:
                st.error(f"Fehler bei der Anfrage: {e}")
