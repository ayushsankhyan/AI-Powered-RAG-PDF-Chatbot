# 🤖 AI-Powered RAG PDF Chatbot

An advanced Retrieval Augmented Generation (RAG) application that allows users to upload multiple PDF documents and interact with them using natural language.

Built using LangChain, FAISS Vector Database, Sentence Transformers, Groq Llama 3, and Streamlit.

---

## 🌐 Live Demo

**Try the Application:**
[https://ai-powered-rag-pdf-chatbot-fesbska7gdduc2ebns6dlk.streamlit.app/]

---

## 📌 Overview

This project enables users to upload one or more PDF documents and ask questions about their contents. The application uses semantic search and vector embeddings to retrieve relevant information before generating context-aware responses using Groq Llama 3.

Unlike traditional keyword search, this chatbot understands the meaning of queries and retrieves the most relevant content from uploaded documents.

---

## ✨ Features

### 📄 Multi-PDF Upload

Upload and analyze multiple PDF documents simultaneously.

### 🔍 Semantic Search

Retrieve information based on meaning rather than exact keywords.

### 🧠 Groq Llama 3 Integration

Generate intelligent answers using a state-of-the-art Large Language Model.

### 📚 FAISS Vector Database

Store and retrieve document embeddings efficiently.

### 💬 Interactive Chat Interface

Ask questions naturally and receive contextual answers.

### 📌 Source Citations

View the document and page references used to generate answers.

### 📥 Download Chat History

Export conversations for future reference.

### 🎨 Premium Streamlit Dashboard

Modern UI with metrics, document tracking, and interactive components.

---

## 🏗️ System Architecture

PDF Upload
↓
PDF Text Extraction
↓
Document Chunking
↓
Sentence Transformer Embeddings
↓
FAISS Vector Database
↓
Semantic Retrieval
↓
Groq Llama 3
↓
Answer Generation

---

## 🛠️ Tech Stack

### Programming Language

* Python

### AI & Machine Learning

* LangChain
* Sentence Transformers
* Groq Llama 3

### Vector Database

* FAISS

### Frontend

* Streamlit

### Document Processing

* PyPDF

---

## 📂 Project Structure

AI-Powered-RAG-PDF-Chatbot

├── app.py

├── requirements.txt

├── README.md

├── .gitignore

├── data/

└── utils/

    ├── chatbot.py

    ├── pdf_loader.py

    └── vector_store.py

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/ayushsankhyan/AI-Powered-RAG-PDF-Chatbot.git
```

Move into the project directory:

```bash
cd AI-Powered-RAG-PDF-Chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 💡 Example Use Cases

* Research Paper Analysis
* Resume Screening
* Job Description Comparison
* Academic Question Answering
* Business Document Analysis
* Technical Documentation Search
* Report Summarization

---

## 📈 Future Enhancements

* PDF Preview Panel
* Voice-Based Question Answering
* Multi-Session Chat History
* OCR Support for Scanned PDFs
* Cloud Vector Database Integration
* Resume Analyzer Mode

---

## 👨‍💻 Author

Ayush Sankhyan

BE CSE (Hons) Artificial Intelligence & Machine Learning

Chandigarh University

---

## ⭐ If you found this project useful, consider starring the repository.
