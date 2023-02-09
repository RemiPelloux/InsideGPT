import streamlit as st
from utils import (
    parse_docx,
    parse_pdf,
    parse_txt,
    parse_vtt,
    search_docs,
    embed_docs,
    text_to_docs,
    get_answer,
    get_sources,
    wrap_text_in_html,
)
from openai.error import OpenAIError




def clear_submit():
    st.session_state["submit"] = False


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


st.set_page_config(page_title="InsideGPT ", page_icon="📖", layout="wide")
st.header("📖InsideGPT ")

with st.sidebar:
    st.markdown("# A propos")
    st.markdown(
        "📖InsideGPT permet de poser des questions sur vos "
        "documents et d'obtenir des réponses précises avec des citations instantanées. "
        ""
    )
    st.markdown(
        "Cet outil est en cours de développement. "
        " "
        ""
    )
    st.markdown("---")
    st.markdown(
        "## Comment utiliser\n"
        "1. Entrez votre [OpenAI API key](https://platform.openai.com/account/api-keys) ci-dessous 🔑\n"
        "2. Téléchargez un fichier pdf, docx ou txt 📄\n"
        "3. Posez une question sur le document upload💬\n"
    )
    api_key_input = st.text_input(
        "Cle OpenAI API",
        type="password",
        placeholder="Collez votre clé OpenAI API ici (sk-...)",
        help="Vous pouvez obtenir votre clé API à partir de https://platform.openai.com/account/api-keys.",
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )

    if api_key_input:
        set_openai_api_key(api_key_input)

    st.markdown("---")
    st.markdown("Mod par [RemiPelloux](https://github.com/RemiPelloux)")

uploaded_file = st.file_uploader(
    "Téléchargez un fichier pdf, docx, vtt, txt",
    type=["pdf", "docx", "txt", "vtt"],
    help="Vous pouvez télécharger un fichier pdf,docx ,vtt ou txt.",
    on_change=clear_submit,
)

index = None
doc = None
if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        doc = parse_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        doc = parse_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        doc = parse_txt(uploaded_file)
    elif uploaded_file.name.endswith(".vtt"):
        doc = parse_vtt(uploaded_file)
    else:
        raise ValueError("Le fichier doit être un pdf, docx, txt ou vtt.")
    text = text_to_docs(doc)
    try:
        with st.spinner("Indexation du document... ⏳"):
            index = embed_docs(text)
        st.session_state["api_key_configured"] = True
    except OpenAIError as e:
        st.error(e._message)

query = st.text_area("Poser votre question ..", on_change=clear_submit)
with st.expander("Options"):
    show_all_chunks = st.checkbox("Montrer tous les morceaux de réponse")
    show_full_doc = st.checkbox("Afficher le contenu analysé du document")

if show_full_doc and doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_text_in_html(doc)}</p>", unsafe_allow_html=True)

button = st.button("Envoi")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Configurez votre clé OpenAI API !")
    elif not index:
        st.error("Veuillez télécharger un document !")
    elif not query:
        st.error("Veuillez poser une question ?")
    else:
        st.session_state["submit"] = True
        # Output Columns
        answer_col, sources_col = st.columns(2)
        sources = search_docs(index, query)

        try:
            answer = get_answer(sources, query)
            if not show_all_chunks:
                # Get the sources for the answer
                sources = get_sources(answer, sources)

            with answer_col:
                st.markdown("#### Réponse")
                st.markdown(answer["output_text"].split("SOURCES: ")[0])

            with sources_col:
                st.markdown("#### Sources")
                for source in sources:
                    st.markdown(source.page_content)
                    st.markdown(source.metadata["source"])
                    st.markdown("---")

        except OpenAIError as e:
            st.error(e._message)
