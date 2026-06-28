import json
from pydantic import BaseModel, Field
from app.core.config import settings
from google import genai
from google.genai import types
from app.utils.docx_parser import extract_text_and_tables_from_docx

# 1. تعريف هياكل البيانات لضمان المخرج (Schema)
class AnalysisResult(BaseModel):
    verdict: str = Field(description="Must be 'satisfies' or 'does_not_satisfy'")
    reason: str = Field(description="Explain the authority locus (who decides).")
    critical_quote: str = Field(description="The exact sentence from the text proving your verdict.")
    analysis_logic: str = Field(description="Why this specific quote proves shared decision-making rather than just feedback.")

class ChallengeAOutput(BaseModel):
    evidence_pack_alpha: AnalysisResult
    evidence_pack_beta: AnalysisResult

class ChallengeAService:
    def __init__(self):
       self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def analyze_documents(self, alpha_file_bytes: bytes, beta_file_bytes: bytes) -> str:
        doc_alpha_text = extract_text_and_tables_from_docx(alpha_file_bytes)
        doc_beta_text = extract_text_and_tables_from_docx(beta_file_bytes)
        
        system_prompt = (
            "You are an expert AI auditor evaluating two documents against the DGA Digital-Experience Maturity Index (2025) - Requirement 18.\n\n"
            "Requirement 18 Definition:\n"
            "Does the platform encourage a genuine Co-creation Methodology where users/stakeholders hold a Shared Locus of Decision in planning and verifying hypotheses?\n\n"
            "THE CORE DISCRIMINATION RULE:\n"
            "- SATISFIES: The document demonstrates that users/stakeholders have actual decision-making power in the project's direction.\n"
            "- DOES_NOT_SATISFY: The document shows 'rigorous research' (interviews/workshops) but the internal team retains full, exclusive decision-making authority.\n\n"
            "IMPORTANT INSTRUCTIONS:\n"
            "1. Evaluate each document independently. Do not assume one must satisfy and the other not. Both could satisfy, or both could fail.\n"
            "2. If the documents are identical, analyze them as two separate entities and provide the same or different results based on their content.\n"
            "3. You must justify your verdict in the 'reason' field by explicitly naming who holds the deciding authority (the locus of decision).\n"
            "4. Output strictly as a valid JSON object matching the provided schema."
        )

        
        user_content = (
            f"=== EVIDENCE PACK ALPHA ===\n{doc_alpha_text[:70000]}\n\n"
            f"=== EVIDENCE PACK BETA ===\n{doc_beta_text[:70000]}\n"
        )

        try:
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=ChallengeAOutput,
                )
            )
            return response.text
        except Exception as e:
           
            return json.dumps({"error": "Failed to analyze", "details": str(e)}, ensure_ascii=False)