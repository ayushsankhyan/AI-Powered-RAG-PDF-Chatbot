import os
import streamlit as st

from utils.pdf_loader import load_pdf
from utils.vector_store import create_vector_store
from utils.chatbot import ask_question


# ====================================
# PAGE CONFIG
# ====================================
st.set_page_config(
    page_title="AI-Powered RAG PDF Chatbot | Ayush Sankhyan",
    page_icon="🤖",
    layout="wide"
)

# ====================================
# CUSTOM CSS
# ====================================
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg,#1e293b,#0f172a);
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    background: #111827;
    border: 1px solid #374151;
    text-align: center;
}

.feature-card {
    padding: 18px;
    border-radius: 12px;
    background: #111827;
    border: 1px solid #374151;
    text-align: center;
    margin-bottom: 10px;
}

.footer {
    text-align:center;
    padding:20px;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# ====================================
# SESSION STATE
# ====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ====================================
# SIDEBAR
# ====================================
st.sidebar.title("🤖 AI PDF Chatbot")

st.sidebar.info(
    """
🔑 **Groq API Key Required**

1. Visit:
https://console.groq.com

2. Create a free account

3. Generate an API key

4. Paste it below

Without an API key, question answering will not work.
"""
)

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password"
)

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("""
### 🚀 Tech Stack

- LangChain
- FAISS
- Sentence Transformers
- Groq Llama 3
- Streamlit

### Features

✅ Multi PDF Upload  
✅ Semantic Search  
✅ Source Citations  
✅ Chat Export  
✅ Vector Retrieval
""")

# ====================================
# HERO SECTION
# ====================================
st.markdown("""
<div class="hero">
<h1>🤖 AI Powered RAG PDF Chatbot</h1>

Upload multiple PDFs and chat with them using
<b>LangChain</b>, <b>FAISS</b>, and <b>Groq Llama 3</b>.

Ask questions, compare documents, summarize reports,
and retrieve information instantly.
</div>
""", unsafe_allow_html=True)

# ====================================
# API WARNING
# ====================================
if not api_key:
    st.warning(
        "⚠️ Enter your Groq API Key from the sidebar before asking questions."
    )

# ====================================
# FEATURE CARDS
# ====================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    📄<br><br>
    <b>Multi PDF Upload</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    🔍<br><br>
    <b>Semantic Search</b>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    🧠<br><br>
    <b>Groq Llama 3</b>
    </div>
    """, unsafe_allow_html=True)

# ====================================
# PDF UPLOAD
# ====================================
uploaded_files = st.file_uploader(
    "📂 Upload PDF Files",
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

    total_pages = len(
        all_documents
    )

    word_count = sum(
        len(doc.page_content.split())
        for doc in all_documents
    )

    chat_count = len(
        st.session_state.messages
    )

    # ====================================
    # DASHBOARD METRICS
    # ====================================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📚 PDFs",
        len(uploaded_files)
    )

    c2.metric(
        "📄 Pages",
        total_pages
    )

    c3.metric(
        "📝 Words",
        word_count
    )

    c4.metric(
        "💬 Messages",
        chat_count
    )

    st.markdown("---")

    st.subheader("📂 Uploaded Documents")

    for pdf in uploaded_files:
        st.write(f"• {pdf.name}")

    st.markdown("---")

    # ====================================
    # CHAT HISTORY
    # ====================================
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):
            st.write(
                message["content"]
            )

    # ====================================
    # CHAT INPUT
    # ====================================
    question = st.chat_input(
        "Ask something about the uploaded PDFs..."
    )

    if question:

        if not api_key:
            st.error(
                "Please enter your Groq API Key first."
            )
            st.stop()

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

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

            st.write(answer)

            st.markdown(
                "### 📌 Sources"
            )

            for source in sources:
                st.write(
                    f"• {source}"
                )

    # ====================================
    # DOWNLOAD CHAT
    # ====================================
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

# ====================================
# FOOTER
# ====================================
st.markdown("---")

st.markdown("""
<div class="footer">

Built with ❤️ using LangChain • FAISS • Groq • Streamlit

<br><br>

Created by <b>Ayush Sankhyan</b>
<br><br>

GitHub: github.com/ayushsankhyan

</div>
""", unsafe_allow_html=True)