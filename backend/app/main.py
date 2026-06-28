import os
import sys
import json  
from app.core.config import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.schemas import RequirementsEnvelope
from app.services.challenge2_requirements_extraction import ChallengeBService
from app.services.challenge1_requirement18_detection import ChallengeAService

app = FastAPI(title="AI Engineering Challenge API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


challenge_a_service = ChallengeAService()
challenge_b_service = ChallengeBService()

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Welcome"}

# ==========================================
# 🎯  Requirement-18 Detection
# ==========================================
@app.post("/api/challenge-a")
async def process_challenge_a(
    file_alpha: UploadFile = File(...),
    file_beta: UploadFile = File(...)
):
    """
    Endpoint for Challenge A: Processes two Word documents and returns 
    the compliance audit as a JSON object.
    """
    # 1. Basic Existence Validation
    if not file_alpha or not file_beta:
        raise HTTPException(status_code=400, detail="Both Alpha and Beta evidence packs are required.")

    try:
        # 2. Read file contents into memory
        alpha_bytes = await file_alpha.read()
        beta_bytes = await file_beta.read()
        
        # 3. Content Validation
        if len(alpha_bytes) == 0 or len(beta_bytes) == 0:
            raise HTTPException(status_code=400, detail="One of the uploaded files is empty.")

        # 4. Invoke the service
        raw_json_response = challenge_a_service.analyze_documents(alpha_bytes, beta_bytes)
        
        # 5. Parse and return
        return json.loads(raw_json_response)
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI output as valid JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during processing: {str(e)}")
# ==========================================
# 📊  Requirements Extraction
# ==========================================
@app.post("/api/challenge-b", response_model=RequirementsEnvelope)
async def process_challenge_b(file: UploadFile = File(...)):
    """
    Endpoint for Challenge B: Receives a PDF evidence pack, 
    analyzes it via DeepSeek VLM, and returns the 22 extracted requirements.
    """
    # 1. Format Validation
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only PDF files are accepted for Challenge B."
        )
    
    try:
        # 2. Read file contents
        pdf_bytes = await file.read()
        
        # 3. Check for empty file
        if len(pdf_bytes) == 0:
            raise HTTPException(status_code=400, detail="The uploaded PDF file is empty.")

        # 4. Invoke the service
        # Assuming extract_requirements is an async method
        result = await challenge_b_service.extract_requirements(pdf_bytes)
        return result

    except Exception as e:
        # 5. Error handling
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process Challenge B requirements: {str(e)}"
        )