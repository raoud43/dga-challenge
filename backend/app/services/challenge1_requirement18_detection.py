import os
from openai import OpenAI
from app.core.config import settings

class ChallengeAService:
    def __init__(self):
        # Initializing the DeepSeek API client via central core configuration
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )

    def analyze_documents(self, doc_alpha_text: str, doc_beta_text: str) -> str:
        """
        Analyzes and compares two large documents to detect which one satisfies Requirement 18
        based on the 'Shared Locus of Decision' philosophy.
        """
        
        # 1.  System Prompt
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
            "strictly as a raw JSON object matching the schema below. Do NOT wrap it in markdown code blocks like ```json or add any conversational text.\n\n"
            "Required JSON Schema:\n"
            "{\n"
            "  \"evidence_pack_alpha\": {\n"
            "    \"verdict\": \"satisfies\" or \"does_not_satisfy\",\n"
            "    \"reason\": \"A detailed, precise engineering justification explaining who holds the deciding authority, quoting or referencing specific evidence from the text.\"\n"
            "  },\n"
            "  \"evidence_pack_beta\": {\n"
            "    \"verdict\": \"satisfies\" or \"does_not_satisfy\",\n"
            "    \"reason\": \"A detailed, precise engineering justification explaining who holds the deciding authority, quoting or referencing specific evidence from the text.\"\n"
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
            # 3. Requesting deep analysis from DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1, # Lowest temperature to enforce strict factuality and remove hallucinations
                response_format={"type": "json_object"} # Forces the engine to return a valid JSON object
            )
            
            # Returning the raw JSON string
            return response.choices[0].message.content

        except Exception as e:
            # Handling API or network connection errors gracefully for cloud runtime
            return {
                "error": "Failed to analyze documents via DeepSeek API",
                "details": str(e)
            }