<div align="center">

# 🧠 AI Text Summarizer
### Intelligent Summarization · AI Security Testing · Reliability

<p>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Giskard-AI%20Testing-7C3AED?style=for-the-badge" alt="Giskard"/>
  <img src="https://img.shields.io/badge/Groq-LLM%20Integration-F55036?style=for-the-badge" alt="Groq"/>
</p>

**Turn lengthy text into concise, meaningful summaries — and test your AI system for potential vulnerabilities.**

Built with Python, FastAPI, Groq, and Giskard.

</div>

---

## 📌 About the Project

The **AI Text Summarizer** is a backend application that transforms lengthy text into concise summaries using a large language model (LLM).

Alongside summarization, the project integrates **Giskard's AI vulnerability scanning capabilities** to evaluate how the summarization agent behaves under adversarial and challenging inputs.

The goal is to build an AI application that is not only useful but also tested for reliability, safety, and potentially problematic behavior.

### 🎯 Project Goals

- 📝 Generate concise summaries from lengthy text.
- ⚡ Expose summarization functionality through a FastAPI REST API.
- 🤖 Integrate an LLM through Groq and LiteLLM.
- 🛡️ Evaluate AI behavior using Giskard vulnerability scans.
- 📊 Save scan results for inspection and further analysis.
- 🔍 Identify potential weaknesses and improve the summarization workflow.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📝 Text Summarization | Converts lengthy text into concise summaries. |
| 🚀 REST API | Provides an HTTP endpoint using FastAPI. |
| 🧠 LLM Integration | Uses a Groq-hosted model through LiteLLM for configured AI operations. |
| 🛡️ AI Vulnerability Scanning | Tests the summarization agent with adversarial scenarios using Giskard. |
| 📋 Scan Reports | Saves scan results and test suites locally. |
| 🔧 Modular Development | Separates the application backend from the Giskard testing environment. |
| 🔐 Environment Configuration | Uses environment variables to manage API credentials. |

---

## 🏗️ Architecture

```text
                    ┌─────────────────────────┐
                    │       User / Client     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Server     │
                    │       Port: 8000        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Summarization Agent   │
                    │                         │
                    │     LLM Integration     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Summary Response    │
                    └─────────────────────────┘


      AI Security & Reliability Testing
      ──────────────────────────────────

                    ┌─────────────────────────┐
                    │  Giskard Scan Script    │
                    │ run_giskard_scan.py     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Adversarial Testing   │
                    │                         │
                    │  Scenario Generation    │
                    │  Agent Response Checks  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Local Reports       │
                    │                         │
                    │ JSON / XML / Test Suite │
                    └─────────────────────────┘
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| ⚡ FastAPI | Backend REST API framework |
| 🤖 Groq | LLM provider |
| 🔌 LiteLLM | LLM integration for Giskard scanning |
| 🛡️ Giskard | AI vulnerability testing |
| 🌐 Uvicorn | ASGI server |
| 🔑 python-dotenv | Environment variable management |
| 🔗 HTTPX | HTTP client for API communication |

---

## 📂 Project Structure

```text
backend/
│
├── main.py                    # FastAPI application
├── run_giskard_scan.py        # Giskard vulnerability scan
│
├── .env                       # API credentials (not committed)
├── .env.example               # Environment variable template
├── .gitignore                 # Git exclusions
├── requirements.txt            # Application dependencies
│
├── reports/                   # Generated scan reports
│   ├── giskard_scan_result.json
│   ├── giskard_scan.xml
│   └── giskard_scan_suite.json
│
├── venv/                      # Application environment
└── venv-giskard/              # Giskard testing environment
```

> **Note:** Virtual environments and generated reports are excluded from Git by default. The structure above illustrates the local development setup.

---

## 🚀 Getting Started

Follow these instructions to run the project locally on Windows.

### 1️⃣ Prerequisites

Make sure you have:

- Python 3.12
- pip
- A Groq API key
- Git (optional, for version control)

### 2️⃣ Clone the Repository

Replace `<your-repository-url>` with your GitHub repository URL.

```bash
git clone <your-repository-url>
cd backend
```

If you have already downloaded the project, open a terminal in its backend directory instead.

### 3️⃣ Create a Python Virtual Environment

```powershell
py -3.12 -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4️⃣ Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual API key.

**Security reminder:** Never commit your `.env` file or expose your API key in public repositories.

### 6️⃣ Start the FastAPI Server

```powershell
uvicorn main:app --reload --port 8000
```

If the application starts successfully, the API will be available at:

**Base URL:** `http://127.0.0.1:8000`

**Swagger API Documentation:** `http://127.0.0.1:8000/docs`

Keep this terminal running while testing the API.

---

## 📝 Using the Summarization API

### Endpoint

```http
POST /api/summarize
```

### Request Body

```json
{
  "text": "Paste a lengthy article, document, or paragraph here to generate a concise summary."
}
```

### Example Request with Python

```python
import requests

url = "http://127.0.0.1:8000/api/summarize"

payload = {
    "text": """
    Artificial intelligence is transforming many industries.
    Organizations use AI to automate repetitive tasks,
    analyze large datasets, and improve decision-making.
    """
}

response = requests.post(url, json=payload, timeout=60)

response.raise_for_status()

print(response.json())
```

### Expected Response Format

The API returns a JSON response containing a `summary` field.

```json
{
  "summary": "Artificial intelligence helps organizations automate tasks, analyze data, and improve decision-making."
}
```

> The example response illustrates the expected format. Actual wording depends on the input and the summarization implementation.

---

## 🛡️ AI Vulnerability Testing with Giskard

This project uses Giskard to evaluate the summarization agent with automatically generated adversarial test scenarios.

### Why Test an AI Summarizer?

AI summarizers may produce outputs that:

- Repeat stereotypes or biased statements.
- Distort the original meaning.
- Handle sensitive subjects inappropriately.
- Follow misleading or adversarial instructions.
- Produce inconsistent results for challenging inputs.

Security and quality testing helps reveal these behaviors before an application is deployed.

### 1️⃣ Create a Separate Testing Environment

Open a new PowerShell terminal in the backend folder:

```powershell
py -3.12 -m venv venv-giskard
```

Activate the environment:

```powershell
.\venv-giskard\Scripts\Activate.ps1
```

### 2️⃣ Install Giskard Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install "giskard[scan,litellm]" httpx python-dotenv
```

### 3️⃣ Configure the LLM Provider

Make sure your `.env` file contains:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

The scan script uses LiteLLM with the configured model:

```python
LiteLLMGenerator(
    model="groq/openai/gpt-oss-120b"
)
```

Ensure the model is available to your Groq account and your API key has sufficient quota.

### 4️⃣ Start the Summarizer API

In a separate terminal, start the FastAPI server:

```powershell
uvicorn main:app --reload --port 8000
```

The API must be running before the scan begins.

### 5️⃣ Execute the Scan

In the terminal with `venv-giskard` activated, run:

```powershell
python run_giskard_scan.py
```

The script configures the summarization target, generates adversarial scenarios, evaluates responses, and saves the scan artifacts locally.

### 6️⃣ Review the Results

Look for the following files in the `reports/` directory:

| File | Purpose |
|---|---|
| `giskard_scan_result.json` | Detailed scan results |
| `giskard_scan.xml` | XML-format test report |
| `giskard_scan_suite.json` | Generated test suite |

The exact files generated depend on the scan script and whether the scan completes successfully.

### Understanding Scan Results

- **Passed:** The scenario passed the relevant checks.
- **Failed:** A check identified behavior that did not meet its expected criteria.
- **Errored:** A check could not complete, for example because of an API rate limit or another execution problem.
- **Skipped:** The scenario was not executed.

**Important:** An errored scenario is not automatically a confirmed vulnerability. Investigate failures separately from execution errors.

> **Giskard Hub:** Local scan reports are not automatically uploaded to the Giskard Hub website. Viewing results in Hub requires the appropriate access and a supported integration workflow.

---

## ⚠️ Troubleshooting

### Problem: Groq API returns HTTP 429

**Possible cause:** The account has exceeded its request or token-processing limit.

**What to try:**
- Wait for the applicable rate limit to reset.
- Reduce the number of scenarios.
- Run tests sequentially rather than concurrently.
- Avoid unnecessary repeated scan runs.
- Check the current limits for your Groq account.

### Problem: Giskard generates zero scenarios

**Possible cause:** The scan configuration, target interface, or scenario-generation process may not be working as expected.

**What to try:**
- Confirm the target is configured correctly.
- Verify the model provider and API key.
- Review the scan logs.
- Check the installed Giskard version and compatible API.

### Problem: The API cannot be reached

**Possible cause:** The FastAPI server is not running or the endpoint is unavailable.

**What to try:**

```powershell
uvicorn main:app --reload --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

### Problem: Python cannot import Giskard

Activate the correct environment before running the scan:

```powershell
.\venv-giskard\Scripts\Activate.ps1
```

Then verify the installation:

```powershell
python -m pip show giskard
```

---

## 🔐 Security Best Practices

- Never expose API keys in source code.
- Keep `.env` excluded from version control.
- Do not commit virtual environments.
- Avoid uploading confidential text to external LLM services.
- Review generated summaries before using them in high-impact applications.
- Investigate failed security checks and rerun tests that errored.
- Keep dependencies updated and review security advisories.

---

## 🔮 Future Improvements

Potential next steps for the project include:

- 📊 Add a dashboard for visualizing scan results.
- 🔄 Integrate automated security testing into CI/CD.
- 🧪 Expand testing across summarization quality and robustness.
- 📈 Track results across multiple scan runs.
- 🛡️ Address identified vulnerabilities and retest.
- ☁️ Explore Giskard Hub integration when access is available.

These are planned improvements, not necessarily implemented features.

---

## 📚 Resources

- [Giskard Documentation](https://docs.giskard.ai/)
- [Giskard Hub Documentation](https://docs.giskard.ai/hub/ui)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [LiteLLM Documentation](https://docs.litellm.ai/)

---

## 👨‍💻 Project Summary

This project combines AI-powered text summarization with automated vulnerability testing.

It demonstrates how a Python backend can expose an AI capability through a REST API while using adversarial testing to investigate potential safety, reliability, and quality issues.

**The objective is simple: build useful AI systems, test their weaknesses, and improve them before deployment.**

<div align="center">

### ⭐ If you find this project useful, consider giving it a star!

**Built with Python · FastAPI · Groq · Giskard**

</div>
