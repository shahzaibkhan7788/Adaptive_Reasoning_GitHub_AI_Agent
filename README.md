# 🧠 Adaptive Reasoning Agent - GitHub AI Assistant

An intelligent GitHub repository assistant powered by **Mistral AI** that adapts its reasoning depth based on network conditions. Features voice I/O, persistent chat sessions, and a ChatGPT-like interface.

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.42+-red.svg)
![Mistral AI](https://img.shields.io/badge/Mistral-AI-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features

### 🎯 Core Capabilities
- **GitHub Repository Analysis**: Clone and analyze any public GitHub repository
- **Adaptive Reasoning**: Automatically adjusts AI reasoning depth based on network latency
  - **FAST Mode** (>200ms): Quick single-pass responses
  - **STANDARD Mode** (100-200ms): Chain-of-thought reasoning
  - **DEEP Mode** (<100ms): Tree-of-thoughts analysis
- **RAG Pipeline**: Dual implementation with LangChain and custom NumPy-based retrieval
- **Multi-Repository Support**: Switch between multiple repositories seamlessly

### 🎤 Voice & Interaction
- **Voice Input**: Speak your questions (integrated microphone button), add another featuesr
- **Voice Output**: Optional text-to-speech responses
- **Real-time Streaming**: Token-by-token response rendering
- **ChatGPT-like UI**: Clean, modern interface with voice popover

### 💾 Data Management
- **User Authentication**: Session-based user management
- **Persistent Chats**: Chat history saved per user and repository
- **Context Refresh**: Update repository context on demand

### 🛠️ Integrated Tools
- **Web Search**: Real-time information via DuckDuckGo
- **PDF Generation**: Create reports and summaries
- **DateTime Awareness**: Time-aware responses
- **Code Analysis**: Deep understanding of repository structure

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit UI                       │
│  (Chat Interface + Voice + Auth + History)          │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌───────▼────────┐
│  Adaptive      │   │  RAG Pipeline  │
│  Reasoning     │   │  (Dual Mode)   │
│  Engine        │   │                │
│                │   │ • LangChain    │
│ • Fast Mode    │   │ • Custom       │
│ • Standard     │◄──┤   (NumPy)      │
│ • Deep         │   │                │
└───────┬────────┘   └───────┬────────┘
        │                    │
        │            ┌───────▼────────┐
        │            │  Vector Store  │
        │            │                │
        │            │ • Qdrant       │
        └────────────┤ • In-Memory    │
                     └────────────────┘
                             │
                     ┌───────▼────────┐
                     │  Mistral API   │
                     │                │
                     │ • mistral-tiny │
                     │ • mistral-embed│
                     └────────────────┘
```

---

## 🤖 Models & APIs

### Mistral AI
- **LLM Model**: `mistral-tiny`
  - Used for: Chat completions, reasoning, tool usage
  - Supports: Streaming responses
  
- **Embedding Model**: `mistral-embed`
  - Dimensions: 1024
  - Used for: Document vectorization and similarity search

### Voice Services
- **Speech-to-Text**: Google Web Speech API (via SpeechRecognition)
- **Text-to-Speech**: Google TTS (via gTTS)

---

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- Mistral API key ([Get one here](https://console.mistral.ai/))
- Git installed on your system

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd module2_github_agent
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```
   
   Or use the provided batch file (Windows):
   ```bash
   run.bat
   ```

6. **Access the app**
   
   Open your browser to: `http://localhost:8501`

---

## 🚀 Usage

### Getting Started

1. **Login**
   - Enter any username to create a session
   - Your chat history will be saved under this username

2. **Add a Repository**
   - Paste a GitHub repository URL in the sidebar
   - Click "Ingest Repository"
   - Wait for the cloning and indexing process

3. **Start Chatting**
   - Type your question in the chat input
   - Or click the 🎙️ microphone icon for voice input
   - Watch the AI respond in real-time with streaming

4. **Switch Repositories**
   - Select different repositories from the sidebar
   - Your chat history is preserved per repository

5. **Voice Settings**
   - Toggle "🔊 Enable Voice Response" in the sidebar
   - When enabled, responses are spoken aloud

### Example Queries

```
"Explain the main architectural patterns in this repository"

"What are the security vulnerabilities in this code?"

"Generate a PDF summary of the key components"

"Search the web for best practices related to this implementation"

"What files were modified in the last commit?"
```

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit |
| **LLM** | Mistral AI (mistral-tiny, mistral-embed) |
| **Vector DB** | Qdrant (in-memory) |
| **Document Processing** | LangChain, PDFPlumber |
| **Version Control** | GitPython |
| **Voice** | SpeechRecognition, gTTS |
| **Search** | DuckDuckGo Search |
| **PDF Generation** | ReportLab |
| **Math** | NumPy (cosine similarity) |

---

## 📁 Project Structure

```
module2_github_agent/
├── app.py                    # Main Streamlit application
├── auth.py                   # User authentication
├── reasoning_core.py         # Adaptive reasoning engine
├── network.py               # Network latency sensor
├── prompt_templates.py      # Reasoning prompts
├── tools.py                 # Tool definitions
├── ingestion.py             # GitHub repo ingestion
├── db.py                    # Qdrant vector database
├── rag.py                   # LangChain RAG pipeline
├── native_rag.py           # Custom RAG implementation
├── chat_manager.py          # Chat persistence
├── kv_store.py             # Metadata storage
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── run.bat                 # Windows runner
└── chats/                  # Chat history storage
    └── {username}/
        └── {repo}.json
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MISTRAL_API_KEY` | Your Mistral API key | ✅ Yes |

### Performance Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Chunk Size | 500 chars | Text chunking for RAG |
| Top-K Results | 3 | Similarity search results |
| Latency Threshold (Fast) | >200ms | Network trigger for fast mode |
| Latency Threshold (Standard) | 100-200ms | Network trigger for standard mode |
| Embedding Dimensions | 1024 | Mistral embed vector size |

---

## 🎯 Adaptive Reasoning Modes

### FAST Mode (Network Latency > 200ms)
- **Strategy**: Direct single-pass response
- **Use Case**: Poor network conditions, quick answers
- **Prompt**: Minimal context, focused query

### STANDARD Mode (100-200ms)
- **Strategy**: Chain-of-thought reasoning
- **Use Case**: Normal conditions, balanced quality
- **Prompt**: Step-by-step analysis with tool awareness

### DEEP Mode (< 100ms)
- **Strategy**: Tree-of-thoughts analysis
- **Use Case**: Excellent network, complex queries
- **Prompt**: Multi-path reasoning with reflections

---

## 🔧 Available Tools

1. **Web Search**
   - Powered by DuckDuckGo
   - Real-time web information retrieval
   - Useful for current events and trends

2. **PDF Generation**
   - Create formatted documents
   - Export summaries and reports
   - Uses ReportLab library

3. **DateTime**
   - Current date/time context
   - Time-aware responses
   - Timestamp references

4. **GitHub RAG**
   - Repository-specific queries
   - Code analysis and search
   - Context-aware responses

---

## 🎨 UI Features

### ChatGPT-like Interface
- **Clean Design**: Modern, intuitive layout
- **Voice Integration**: Microphone button in chat area
- **Streaming**: Real-time response rendering
- **History Navigation**: Easy repository switching

### Voice Workflow
1. Click 🎙️ microphone icon (bottom-right)
2. Popover opens with recorder
3. Speak your question
4. Transcription appears
5. Query is submitted automatically
6. Response (optionally) spoken aloud

---

## 📊 Performance

- **Embedding Generation**: ~1-2 seconds per document
- **Query Response**: 2-5 seconds (streaming starts immediately)
- **Repository Ingestion**: Depends on size (typically 30-120 seconds)
- **Network Latency Check**: ~100ms

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Mistral AI** for the powerful LLM and embedding models
- **Streamlit** for the fantastic web framework
- **LangChain** for document processing utilities
- **Qdrant** for vector database capabilities

---

## 📞 Contact & Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation in `docs/`

---

## 🚧 Roadmap

- [ ] Multi-LLM support (OpenAI, Anthropic)
- [ ] Code execution sandbox
- [ ] Collaborative features
- [ ] Docker deployment
- [ ] Real-time git pull integration
- [ ] Advanced tool calling system
- [ ] Custom embedding models

---

**Built with ❤️ for AI Hackathon**
