import os
import json
import time
from app.core.config import settings
from google import genai
from google.genai import types
from app.core.schemas import RequirementsEnvelope
from app.utils.pdf_processor import convert_pdf_to_images

class ChallengeBService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)


    async def extract_requirements(self, pdf_bytes: bytes) -> RequirementsEnvelope:
        
        images = convert_pdf_to_images(pdf_bytes)
        
        
        contents = [img for img in images]
        
        system_instruction = (
            "أنت خبير في هيئة الحكومة الرقمية. مهمتك استخراج 22 متطلباً من المستند المرفق.\n"
            "يجب أن يتطابق المخرج مع هيكل JSON المطلوب:\n"
            "الحقول: requirement_number, document_page_number, axis_number, axis_name, question, "
            "requirement_definition, evidence_examples (list), evidence_format, counts_toward_inclusivity_index (bool).\n"
            "تأكد من توزيع المتطلبات حسب المحاور (1: 1-4، 2: 5-9، 3: 10-14، 4: 15-18، 5: 19-22).\n"
            "المخرج يجب أن يكون JSON صافي فقط."
        )

        model_options = ["gemini-2.0-flash", "gemini-flash-latest", "gemini-2.5-flash"]
        max_retries = 2
        
        for model in model_options:
            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=model, 
                        contents=[system_instruction] + contents,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            
                            temperature=0.1, 
                        ),
                    )
                    
                    data = json.loads(response.text)
                    return RequirementsEnvelope(requirements=data) if isinstance(data, list) else RequirementsEnvelope.model_validate(data)
                
                except Exception as e:
                    error_msg = str(e)
                    # إذا كان الخطأ بسبب الضغط (503/429)، انتظر قليلاً وأعد المحاولة
                    if "503" in error_msg or "429" in error_msg:
                        time.sleep(2 * (attempt + 1))
                        continue
                    else:
                  
                        break
        
     
        raise Exception("فشلت عملية استخراج البيانات بعد عدة محاولات بسبب ضغط الخوادم.")
