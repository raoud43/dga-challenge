import os
import json
from google import genai
from google.genai import types
from app.core.config import settings

class ChallengeAService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def analyze_documents(self, doc_alpha_text: str, doc_beta_text: str) -> str:
        """
        Analyzes and compares two large documents to detect which one satisfies Requirement 18
        based on the 'Shared Locus of Decision' philosophy and extracts visual/location parameters.
        """
        
        # 1. System Prompt المحدث ليتطابق مع متطلبات الواجهة الرسومية (Streamlit)
        system_prompt = (
            "You are an expert AI auditor and compliance consultant assessing evidence packs "
            "against the DGA Digital-Experience Maturity Index (2025) - Fourth Perspective (Tools & Technologies).\n\n"
            "Your strict task is to analyze two text dumps extracted from candidate Word documents (Alpha and Beta) "
            "and determine which one satisfies Requirement 18, and which one does not.\n\n"
            "Requirement 18 Definition:\n"
            "Does the platform encourage a collaborative environment that allows for the shared verification of "
            "hypotheses, broadly participatory planning, and sharing of results (Co-creation Methodology) "
            "to ensure transparency, enhance trust, and engage users from diverse categories or backgrounds?\n\n"
            "THE CORE DISCRIMINATION RULE (Watch out for the trap):\n"
            "- Both documents look identical on the surface. They share the same personas, same journey maps, "
            "and both extensively use terms like 'co-creation', 'workshops', and 'user journey'.\n"
            "- The document that DOES NOT SATISFY (does_not_satisfy): Conducts rigorous user research and usability testing "
            "where users are interviewed or observed, BUT the internal project team retains full, exclusive decision-making authority "
            "and planning power (the users have no actual vote or share in the ultimate direction).\n"
            "- The document that SATISFIES (satisfies): Demonstrates a genuine co-creation environment where stakeholders and users "
            "hold a part of the decision itself (Shared Locus of Decision) in planning, verifying hypotheses, and co-shaping the results.\n\n"
            "You must perform deep reasoning over the texts, find the subtle differentiator, and output your answer "
            "strictly as a raw valid JSON object matching the schema below. Do NOT wrap it in markdown code blocks like ```json or add any conversational text.\n\n"
            "Required JSON Schema (Strictly follow these exact keys for Frontend alignment):\n"
            "{\n"
            "  \"evidence_pack_alpha\": {\n"
            "    \"verdict\": \"satisfies\" or \"does_not_satisfy\",\n"
            "    \"page_number\": \"Specify the exact page number found in text, e.g., 'Page 12' (or 'Unknown' if not explicit)\",\n"
            "    \"location_context\": \"Specify the context section or table name, e.g., 'Section 3.2: Governance'\",\n"
            "    \"text_content\": \"Extract the EXACT verbatim textual quotation or key sentence from the text that triggered this judgment. Do not summarize.\"\n"
            "  },\n"
            "  \"evidence_pack_beta\": {\n"
            "    \"verdict\": \"satisfies\" or \"does_not_satisfy\",\n"
            "    \"page_number\": \"Specify the exact page number found in text, e.g., 'Page 27' (or 'Unknown' if not explicit)\",\n"
            "    \"location_context\": \"Specify the context section or table name, e.g., 'Table 4: Decision Matrix'\",\n"
            "    \"text_content\": \"Extract the EXACT verbatim textual quotation or key sentence from the text that triggered this judgment. Do not summarize.\"\n"
            "  }\n"
            "}"
        )

        # 2. Feeding the document context into the user prompt
        user_content = (
            f"Analyze the following text extractions from both evidence packs and discover the true differentiator:\n\n"
            f"=== START OF EVIDENCE PACK ALPHA ===\n{doc_alpha_text[:40000]}\n=== END OF EVIDENCE PACK ALPHA ===\n\n"
            f"=== START OF EVIDENCE PACK BETA ===\n{doc_beta_text[:40000]}\n=== END OF EVIDENCE PACK BETA ===\n"
        )

        try:
            # 3. Requesting analysis using Google GenAI SDK
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.1,
                    # إجبار النموذج على إرجاع JSON نظيف وهيكلي مطابق تماماً للمطلوب
                    response_mime_type="application/json"
                )
            )
            
            # إرجاع النص المولد وهو الـ JSON النظيف الحقيقي
            return response.text

        except Exception as e:
            return json.dumps({
                "error": "Failed to analyze documents via Gemini Native API",
                "details": str(e)
            }, ensure_ascii=False)