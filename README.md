# AI Engineering Challenge

<img width="959" height="446" alt="image" src="https://github.com/user-attachments/assets/29bc9d5b-a2eb-4446-88b2-5595d0d1f58a" />



[cite_start]A robust, AI-powered system designed to automate both **Requirement-18 Detection** (Challenge A) and **Requirements Extraction** (Challenge B) based on the DGA Fourth-Perspective framework[cite: 4, 18, 40].

## 🚀 Overview
This application addresses the two independent tasks defined in the DGA Engineering Challenge:
* [cite_start]**Challenge A (Requirement-18 Detection):** An AI system that analyzes candidate documents to determine if they satisfy "Requirement 18" regarding co-creation methodology, providing both a verdict and a reasoning-based justification[cite: 18, 21, 31].
* [cite_start]**Challenge B (Requirements Extraction):** A robust pipeline that processes complex government guides (in varied layouts) and extracts all 22 requirements into a standardized, valid JSON format[cite: 40, 48].

## 🏗 System Architecture
The application follows a modular design to ensure scalability and reproducibility:
* [cite_start]**Backend (FastAPI):** Orchestrates the AI logic, processes PDF/Docx files, and interacts with the Google Gemini API to perform reasoning and extraction[cite: 71].
* [cite_start]**Frontend (Streamlit):** An intuitive user interface allowing users to upload evidence packs or government guides and receive instant, structured results.
* [cite_start]**Containerization:** Fully Dockerized to ensure consistent behavior across different environments.

## 🛠 Tech Stack
* **Language:** Python 
* **Frameworks:** FastAPI, Streamlit
* **AI/ML:** Google Gemini API (VLM)
* **Infrastructure:** Docker, Docker Compose

## ⚙️ How to Run Locally

### 1. Prerequisites
Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### 2. Setup
Clone the repository:
```bash
git clone [https://github.com/raoud43/dga-challenge.git](https://github.com/raoud43/dga-challenge.git)
cd dga-challenge

### 3. Environment Variables
To interact with the Google Gemini API, you must provide your own API key. Create a .env file in the project root:

```bash
GEMINI_API_KEY=your_actual_api_key_here

Note: You can obtain your key from Google AI Studio.

### 4. Launch Application

Run the entire system using Docker Compose:
```bash
docker-compose up --build

Once the services are running, the Frontend will be accessible via your browser (usually http://localhost:8501).

📝 Troubleshooting
API Key Issues: Ensure your GEMINI_API_KEY is valid and has the necessary permissions in Google AI Studio.

Docker Errors: If the services fail to start, ensure no other applications are using ports 8000 (Backend) or 8501 (Frontend).

Service Communication: The Frontend relies on the Backend URL. If you modify the service names, ensure the configuration in the docker-compose.yml remains consistent.
