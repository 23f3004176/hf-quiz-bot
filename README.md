---
title: Hf Quiz Bot
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---

# 🤖 HF Quiz Bot

An intelligent, AI-powered quiz solver bot built with FastAPI and deployed on Hugging Face Spaces. This bot leverages Google's Gemini 2.0 Flash Lite model and Playwright for web scraping to automatically analyze and solve various types of quiz questions.

## ✨ Features

- **Multi-Type Quiz Support**: Handles various quiz formats including:
  - Simple instruction-based questions
  - Data analysis tasks (CSV, Excel, PDF files)
  - API sourcing challenges
  - Visualization tasks
  - Web scraping questions

- **Intelligent Agent System**: Uses `smolagents` CodeAgent for dynamic problem-solving
- **Headless Browser Support**: Playwright integration for JavaScript-rendered content
- **Automatic Retry Logic**: Built-in retry mechanism for API resilience
- **Background Processing**: Non-blocking quiz solving with FastAPI background tasks

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI |
| **AI Model** | Gemini 2.0 Flash Lite (via LiteLLM) |
| **Agent Framework** | smolagents (CodeAgent) |
| **Web Scraping** | Playwright (Chromium) |
| **Data Processing** | Pandas, NumPy, scikit-learn |
| **Deployment** | Docker, Hugging Face Spaces |

## 📋 Requirements

- Python 3.10+
- Docker (for containerized deployment)
- Gemini API Key
- Hugging Face account (for Spaces deployment)

## 🚀 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hf-quiz-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   playwright install-deps
   ```

5. **Set environment variables**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   export STUDENT_EMAIL="your-email@example.com"
   export STUDENT_SECRET="your-secret-key"
   ```

6. **Run the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 7860
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t hf-quiz-bot .
   ```

2. **Run the container**
   ```bash
   docker run -p 7860:7860 \
     -e GEMINI_API_KEY="your-gemini-api-key" \
     -e STUDENT_EMAIL="your-email@example.com" \
     -e STUDENT_SECRET="your-secret-key" \
     hf-quiz-bot
   ```

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI model access | ✅ Yes |
| `STUDENT_EMAIL` | Email address for quiz submissions | ✅ Yes |
| `STUDENT_SECRET` | Secret key for authentication | ✅ Yes |

## 📡 API Reference

### POST `/run`

Starts the quiz-solving process for a given URL.

**Request Body:**
```json
{
  "email": "your-email@example.com",
  "secret": "your-secret-key",
  "url": "https://quiz-url.example.com/quiz/1"
}
```

**Response:**
```json
{
  "message": "Universal Agent started",
  "status": "ok"
}
```

**Status Codes:**
- `200`: Quiz solving started successfully
- `403`: Invalid secret key

## 🏗️ Project Structure

```
hf-quiz-bot/
├── main.py           # FastAPI application and agent logic
├── tools.py          # Playwright web scraping tool
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker configuration
└── README.md         # Project documentation
```

## 🧠 How It Works

1. **Request Received**: The bot receives a quiz URL via the `/run` endpoint
2. **Page Analysis**: Playwright visits the page and extracts content
3. **Task Classification**: The AI agent determines the quiz type
4. **Problem Solving**: The agent executes the appropriate strategy:
   - Extracts answers from JSON blocks
   - Downloads and analyzes data files
   - Fetches data from APIs
   - Performs calculations or visualizations
5. **Submission**: The answer is submitted to the quiz platform
6. **Chain Handling**: If a new URL is returned, the process continues

## 🚢 Hugging Face Spaces Deployment

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select **Docker** as the SDK
3. Upload the repository files
4. Add the following secrets in Space Settings:
   - `GEMINI_API_KEY`
   - `STUDENT_EMAIL`
   - `STUDENT_SECRET`
5. The Space will automatically build and deploy

## 📦 Dependencies

Key libraries used in this project:

- **fastapi** - Modern web framework for building APIs
- **uvicorn** - Lightning-fast ASGI server
- **smolagents** - Lightweight agent framework
- **litellm** - Unified API for LLM providers
- **playwright** - Browser automation library
- **pandas** - Data manipulation and analysis
- **beautifulsoup4** - HTML parsing
- **scikit-learn** - Machine learning utilities

## ⚠️ Important Notes

- Ensure your `STUDENT_SECRET` is kept confidential
- The bot runs in background tasks to avoid request timeouts
- Rate limiting may apply based on the Gemini API quota
- Playwright requires Chromium to be installed

## 📄 License

This project is open source. Feel free to use and modify as needed.

## 🔗 Links

- [Hugging Face Spaces Configuration Reference](https://huggingface.co/docs/hub/spaces-config-reference)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [smolagents Documentation](https://huggingface.co/docs/smolagents)
- [Playwright Python Documentation](https://playwright.dev/python/)

---

<p align="center">
  Made with ❤️ for automated quiz solving
</p>
