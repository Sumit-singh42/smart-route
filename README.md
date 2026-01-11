# SmartRoute AI Proxy 🚀

**SmartRoute** is an intelligent AI proxy that optimizes LLM usage by routing queries to the most cost-effective or capable model based on complexity. It features a semantic caching layer to deliver instant responses for recurring queries and a real-time dashboard to monitor usage.

## ✨ Features

-   **🧠 Smart Routing**: Automatically routes simple queries (e.g., "What is 2+2?") to faster/cheaper models (Groq/Llama-3) and complex queries (e.g., coding tasks) to capable models (GPT-4/Claude-3).
-   **⚡ Semantic Caching**: Uses **Qdrant** (Local Mode) to cache responses. Similar queries are served instantly without hitting an LLM provider.
-   **🛠️ Mock Mode**: Fully simulated mode for development. Test the entire flow without API keys or costs.
-   **📊 Analytics Dashboard**: React-based UI to visualize request distribution, latency, and simulated costs.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, Redis (Optional), Qdrant (Local Vector DB)
-   **Frontend**: React, Vite, TailwindCSS, Recharts

## 🚀 Getting Started

Runs completely locally! No Docker required.

### Prerequisites
-   **Python** 3.8+
-   **Node.js** 18+

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*Server runs at `http://localhost:8000`*

### 2. Frontend Setup

Open a new terminal:
```bash
cd frontend
npm install

# Start the dashboard
npm run dev -- --host
```
*Dashboard runs at `http://localhost:5173`*

## ⚙️ Configuration

The project uses a `.env` file in the `backend/` directory.

**Default Configuration (Mock Mode):**
```ini
USE_MOCK_LLM=True
```
*This simulates all LLM responses. Great for testing.*

**To use Real APIs:**
1.  Open `backend/.env`
2.  Set `USE_MOCK_LLM=False`
3.  Add your API keys (OPENAI_API_KEY, GROQ_API_KEY, etc.)
4.  Restart the backend.

## ✅ Verification

We include scripts to verify functionality:

1.  **Check Connectivity**:
    ```bash
    python verify_setup.py
    ```
    *Sends test queries to the backend.*

2.  **Verify Routing**:
    ```bash
    python verify_real_keys.py
    ```
    *Bypasses cache to test actual routing logic.*
