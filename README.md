# AI Engineering Challenge

<img width="959" height="446" alt="image" src="https://github.com/user-attachments/assets/29bc9d5b-a2eb-4446-88b2-5595d0d1f58a" />





🛠 Tech Stack
Language: Python

Frameworks: FastAPI (Backend), Streamlit (Frontend)

AI/ML: Google Gemini API (Vision-Language Processing)

Containerization: Docker



🏗 System Architecture
The application is architected into two main services:

Backend (FastAPI): Handles core logic, document processing, and interactions with the Gemini API.

Frontend (Streamlit): Provides an intuitive interface for users to upload documents and view extracted results in real-time.



⚙️ How to Run Locally
Clone the repository:

git clone https://github.com/raoud43/dga-challenge.git
cd dga-challenge

Set up Environment Variables:
Create a .env file and add your Google Gemini API Key:

GEMINI_API_KEY=your_actual_api_key_here

Run with Docker:
docker-compose up --build
