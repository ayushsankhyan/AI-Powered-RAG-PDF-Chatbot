import os
import streamlit as st

from utils.pdf_loader import load_pdf
from utils.vector_store import create_vector_store
from utils.chatbot import ask_question


# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------
# SESSION STATE
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.title("🤖 RAG PDF Chatbot")

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password"
)

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown("""
### About

This chatbot uses:

- LangChain
- FAISS
- Sentence Transformers
- Groq Llama 3
- Streamlit

Upload one or more PDFs and ask questions.
""")

# --------------------------------
# MAIN PAGE
# --------------------------------
st.title("🤖 RAG PDF Chatbot")

st.markdown("""
Upload one or more PDFs and ask questions about their contents.
""")

# --------------------------------
# MULTI PDF UPLOAD
# --------------------------------
uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs(
        "data",
        exist_ok=True
    )

    all_documents = []

    with st.spinner(
        "Processing PDFs..."
    ):

        for uploaded_file in uploaded_files:

            pdf_path = os.path.join(
                "data",
                uploaded_file.name
            )

            with open(
                pdf_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.read()
                )

            documents = load_pdf(
                pdf_path
            )

            all_documents.extend(
                documents
            )

        vector_store = create_vector_store(
            all_documents
        )

    st.success(
        f"✅ {len(uploaded_files)} PDF(s) Uploaded Successfully"
    )

    st.success(
        "✅ Vector Database Created"
    )

    total_pages = len(
        all_documents
    )

    word_count = sum(
        len(
            doc.page_content.split()
        )
        for doc in all_documents
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📄 Pages",
            total_pages
        )

    with col2:
        st.metric(
            "📝 Words",
            word_count
        )

    with col3:
        st.metric(
            "📚 PDFs",
            len(uploaded_files)
        )

    st.subheader(
        "📂 Uploaded Documents"
    )

    for pdf in uploaded_files:

        st.write(
            f"• {pdf.name}"
        )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    question = st.chat_input(
        "Ask something about the uploaded PDFs..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):
            st.write(
                question
            )

        with st.spinner(
            "Generating Answer..."
        ):

            docs = vector_store.similarity_search(
                question,
                k=10
            )

            context = "\n".join(
                [
                    doc.page_content
                    for doc in docs
                ]
            )

            sources = []

            for doc in docs:

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                sources.append(
                    f"{os.path.basename(source)} (Page {page})"
                )

            sources = list(
                set(sources)
            )

            answer = ask_question(
                api_key,
                context,
                question
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message(
            "assistant"
        ):

            st.write(
                answer
            )

            st.markdown(
                "### 📌 Sources"
            )

            for source in sources:

                st.write(
                    f"• {source}"
                )

    chat_text = ""

    for msg in st.session_state.messages:

        role = msg["role"].upper()

        chat_text += f"{role}\n"
        chat_text += f"{msg['content']}\n\n"

    st.download_button(
        "📥 Download Chat",
        chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )