# 🧠 Maestro

An AI-powered exam prep assistant built for KIIT University students, using LLaMA 3, LangChain, and ChromaDB — powered entirely offline with Retrieval-Augmented Generation (RAG).

## 🚀 Features

- Ask questions from past papers by subject, year, or exam type
- Get repeated questions or generate mock papers from real data
- Fully offline RAG using `Ollama` and `mxbai-embed-large` embeddings
- Filters results based on metadata like semester, marks, etc.

## 📁 Data Structure

All historical papers are stored as structured JSONs in `json_subs/`.  
Each file follows a format with metadata + actual question parts.

## ⚙️ Technologies Used

- 🧠 LLaMA 3 (via Ollama)
- 🧵 LangChain + Prompt Templates
- 📊 ChromaDB for vector search
- 📄 JSON parsing & metadata filtering

## 🧪 Usage

```bash
# Run Ollama model locally (requires ollama installed)
ollama run llama3

# Then run the bot
python main.py
