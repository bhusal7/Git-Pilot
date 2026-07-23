# 🤖 GitHub AI Repository Analyzer

> **Agentic AI + RAG + LangChain Powered Repository Intelligence System**

Analyze any public GitHub repository using multiple AI agents, Retrieval-Augmented Generation (RAG), and LLM reasoning to understand architecture, technologies, documentation, code quality, and improvement opportunities.

---

## 📸 Preview

<img width="100%" alt="GitHub AI Repository Analyzer" src="assets/demo.png">

> *(Replace with your own project screenshot or GIF.)*

---

# 🚀 Features

✅ Analyze any **public GitHub repository**

✅ Automatically clones repository

✅ Loads source code & documentation

✅ Builds a **RAG Knowledge Base**

✅ Semantic search across repository

✅ AI-powered repository understanding

✅ Multi-Agent workflow

- 🔍 Search Agent
- 📂 Repository Agent
- 🧠 Analysis Agent
- 📝 Report Generator
- 🧐 Critic Agent

✅ Generates detailed Markdown report

✅ Modern Streamlit Hacker UI

✅ Interactive progress tracking

---

# 🧠 AI Workflow

```
GitHub URL
      │
      ▼
Clone Repository
      │
      ▼
Load Files
      │
      ▼
Split Documents
      │
      ▼
Generate Embeddings
      │
      ▼
Store into ChromaDB
      │
      ▼
Retriever (RAG)
      │
      ▼
Search Agent
      │
      ▼
Repository Agent
      │
      ▼
Analysis Agent
      │
      ▼
Critic Agent
      │
      ▼
Final Report
```

---

# 🏗 Project Structure

```
GitHub-AI-Repository-Analyzer/

│
├── app.py
├── pipeline.py
├── agents.py
├── tools.py
├── rag.py
├── loader.py
├── splitter.py
├── embeddings.py
├── vectorstore.py
├── prompts.py
├── utils.py
│
├── reports/
│
├── chroma_db/
│
├── cloned_repo/
│
├── requirements.txt
│
├── .env
│
└── README.md
```

---

# ⚙️ Tech Stack

## AI

- LangChain
- LangGraph (Optional)
- Groq LLM
- HuggingFace Embeddings
- RAG
- Multi-Agent AI

---

## Vector Database

- ChromaDB

---

## Frontend

- Streamlit

---

## Backend

- Python

---

## Other Libraries

- GitPython
- RecursiveCharacterTextSplitter
- Markdown
- dotenv

---

# 🧩 Architecture

```
                  User
                    │
                    ▼
             Streamlit Interface
                    │
                    ▼
             Repository Pipeline
                    │
     ┌──────────────┼──────────────┐
     │              │              │
     ▼              ▼              ▼
 Clone Repo    Build RAG      Search Docs
     │              │              │
     └──────────────┼──────────────┘
                    ▼
              AI Agent System
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Search Agent Repository Agent Critic Agent
      │             │             │
      └─────────────┼─────────────┘
                    ▼
             Final Repository Report
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/github-ai-repository-analyzer.git

cd github-ai-repository-analyzer
```

---

Create virtual environment

```bash
python -m venv .venv
```

Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key

HF_TOKEN=your_huggingface_token

TAVILY_API_KEY=your_tavily_api_key
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 💡 How It Works

1. Enter a public GitHub repository URL.

2. Ask any question about the repository.

Examples:

```
Explain architecture

Summarize project

Review code quality

Find improvements

Explain folder structure

How does authentication work?

Suggest production improvements
```

3. Click **Analyze Repository**

The application will

- Clone repository
- Load files
- Build embeddings
- Create vector database
- Search repository
- Run AI agents
- Generate report

---

# 📋 Example Output

```
Repository Overview

Architecture Analysis

Technology Stack

Folder Structure

Important Components

Dependencies

Design Patterns

Strengths

Weaknesses

Potential Bugs

Performance Suggestions

Security Suggestions

Best Practices

Final Critic Review
```

---

# 📊 AI Agents

## 🔎 Search Agent

Searches repository documentation and retrieves relevant information using RAG.

---

## 📂 Repository Agent

Analyzes

- folders
- files
- architecture
- technologies

---

## 🧠 Analysis Agent

Provides deep reasoning over repository structure.

---

## 📝 Report Agent

Generates structured Markdown documentation.

---

## 🧐 Critic Agent

Reviews AI output and improves report quality.

---

# 🌟 User Interface

The Streamlit application includes

- Modern Glassmorphism UI
- Gradient Theme
- Interactive Progress Bar
- Expandable AI Outputs
- Markdown Rendering
- Repository Report Viewer
- Error Handling

---

# 📚 Built Using

- LangChain
- Groq
- HuggingFace Embeddings
- ChromaDB
- Streamlit
- Python
- GitPython
- RAG
- Multi-Agent AI

---

# 🎯 Future Improvements

- GitHub Authentication
- Private Repository Support
- Commit History Analysis
- Pull Request Review
- Issue Analysis
- Dependency Vulnerability Scan
- Code Quality Metrics
- Repository Diagram Generation
- PDF Report Export
- Docker Deployment
- LangGraph Workflow
- Multi-LLM Support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork repository

2. Create feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push branch

```bash
git push origin feature/new-feature
```

5. Open Pull Request

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

# 👨‍💻 Author

**Bashudev Bhusal**

AI Engineer | Machine Learning | Generative AI | Agentic AI

GitHub:
https://github.com/bhusal7


---

# 📄 License

This project is licensed under the MIT License.

---

## ❤️ Built with

**LangChain • RAG • Agentic AI • Groq • ChromaDB • Streamlit • Python**