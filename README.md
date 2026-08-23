# 📚 DocuMint

**Intelligent Document Q&A System powered by RAG (Retrieval-Augmented Generation)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-red)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local-purple)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📖 Overview

**DocuMint** is a powerful, fully local Retrieval-Augmented Generation (RAG) system that allows you to chat with your documents. Upload PDFs and ask questions in natural language – DocuMint will find relevant information and generate accurate answers using local LLMs.

### ✨ Key Features

- **🔒 100% Local & Private** – Your data never leaves your computer
- **💬 Natural Language Q&A** – Ask questions about your documents
- **📄 Multi-Format Support** – Upload PDF and TXT files
- **🧠 Multiple LLM Options** – Choose between phi3:mini, tinyllama, and more
- **🎨 Dark/Light Mode** – Automatic theme detection
- **📊 Real-time Processing** – Instant document ingestion and querying
- **💾 Persistent Storage** – ChromaDB vector database for efficient retrieval
- **🔄 Easy Management** – Clear chat, reset database, upload documents

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Ollama installed locally
- 8GB+ RAM recommended

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/boughanmiyoussef/DocuMint.git
cd DocuMint
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### 5. Pull Required Models

```bash
ollama pull nomic-embed-text

# LLM models (choose one or more)
ollama pull phi3:mini      # 2.2GB - Good balance
ollama pull tinyllama      # 637MB - Fastest
```

#### 6. Start Ollama

```bash
ollama serve &
```

#### 7. Populate Database

Add your PDFs to the `data/` folder, then run:

```bash
python populate_database.py
```

#### 8. Run DocuMint

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
DocuMint/
├── app.py                      # Streamlit web interface
├── query_data.py              # CLI query interface
├── populate_database.py       # Database builder
├── get_embedding_function.py  # Embedding configuration
├── test_rag.py               # Unit tests
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── data/                     # Uploaded documents
│   └── your_documents.pdf
├── chroma/                   # Vector database
│   └── chroma.sqlite3
└── venv/                     # Virtual environment
```

---

## 🎯 Usage Guide

### Web Interface

1. **Upload Documents**
   - Click "Add Document" in the sidebar
   - Select PDF or TXT files
   - Wait for processing confirmation

2. **Ask Questions**
   - Type your question in the chat input
   - Press Enter or click Send
   - Get instant answers with source references

3. **Manage Conversation**
   - Clear chat history from sidebar
   - Reset database if needed

4. **Switch Models**
   - Select from available LLM models
   - phi3:mini (default) – Good balance
   - tinyllama – Fastest responses

### Command Line Interface

```bash
# Query documents
python query_data.py "What is this document about?"

# Specify model
python query_data.py "Summarize the key points" --model phi3:mini

# Build database
python populate_database.py

# Reset database
python populate_database.py --reset
```

---

## 🧠 Supported Models

| Model | Size | Quality | Speed | Best For |
|-------|------|---------|-------|----------|
| **phi3:mini** | 2.2 GB | ⭐⭐⭐⭐ | Fast | Daily use |
| **tinyllama** | 637 MB | ⭐⭐ | Fastest | Quick queries |

### Add More Models

```bash
ollama pull <model_name>
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Framework** | LangChain 0.2.16 |
| **Vector Database** | ChromaDB 0.4.24 |
| **LLM** | Ollama (phi3:mini, tinyllama, mistral) |
| **Embeddings** | nomic-embed-text |
| **Web Interface** | Streamlit 1.37.0 |
| **Document Processing** | PyPDF, pdfplumber |
| **Language** | Python 3.10+ |

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Ollama API endpoint | `http://localhost:11434` |

### Database Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| `chunk_size` | 800 | Document chunk size |
| `chunk_overlap` | 80 | Overlap between chunks |
| `k` | 5 | Number of retrieved chunks |

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Query Latency** | 2-5 seconds (phi3:mini) |
| **Document Processing** | ~1 page/second |
| **Database Size** | ~5-10 MB per 100 pages |
| **Memory Usage** | ~2-4 GB (phi3:mini) |

---

## 🔒 Privacy & Security

- ✅ **100% Local Processing** – No external API calls
- ✅ **Data Privacy** – Documents never leave your machine
- ✅ **No Tracking** – No telemetry or analytics
- ✅ **Offline Capable** – Works without internet

---

## 🐛 Troubleshooting

### Common Issues

#### Ollama Connection Refused

```bash
# Start Ollama
ollama serve &

# Check status
curl http://localhost:11434/api/tags
```

#### Database Not Found

```bash
# Rebuild database
python populate_database.py
```

#### Out of Memory

```bash
# Use smaller model
ollama pull tinyllama
# Select tinyllama in the UI
```

#### Import Errors

```bash
# Clean install
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📝 Development

### Running Tests

```bash
pytest test_rag.py -v
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) – RAG framework
- [Ollama](https://ollama.ai/) – Local LLM runner
- [Streamlit](https://streamlit.io/) – Web interface
- [ChromaDB](https://www.trychroma.com/) – Vector database

---

## 📞 Contact

**Youssef Boughanmi**

- 📧 yussefboughanmy@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/youssef-boughanmi-4990222a0)
- 🐙 [GitHub](https://github.com/boughanmiyoussef)
- 🌐 [Portfolio](https://boughanmiyoussef.github.io)

---

## ⭐ Star Us

If you find DocuMint useful, please give it a star on GitHub!

---

**Built with ❤️ by Youssef Boughanmi**