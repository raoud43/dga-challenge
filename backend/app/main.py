import os
import sys

# الخطة البديلة المطلقة: حساب المسار الفعلي لمجلد backend وحقنه في النظام فوراً
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # هذا يعطيكِ مسار backend/
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# الآن الاستيراد المباشر النظيف والآمن بنسبة 100%
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# الاستيراد المباشر بدون نقاط وبدون اسم حزم معقدة
from app.core.schemas import RequirementsEnvelope
from app.services.challenge2_requirements_extraction import ChallengeBService
from app.services.challenge1_requirement18_detection import ChallengeAService

app = FastAPI(title="AI Engineering Challenge API", version="1.0.0")

# تفعيل الـ CORS لربط الشاشات سحابياً ومحلياً بنجاح
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تهيئة كائنات الخدمات مرة واحدة عند إقلاع السيرفر (Singleton-like pattern للسرعة والأداء)
challenge_a_service = ChallengeAService()
challenge_b_service = ChallengeBService()

# قالب بيانات مدخلات التحدي الأول (يستقبل النصوص المستخرجة)
class ChallengeARequest(BaseModel):
    doc_alpha_text: str
    doc_beta_text: str

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "مرحباً بك في نظام هندسة الذكاء الاصطناعي الموحد"}


# ==========================================
# 🎯 التحدي الأول: Requirement-18 Detection
# ==========================================
@app.post("/api/challenge-a")
async def process_challenge_a(data: ChallengeARequest):
    """
    نقطة النهاية للتحدي الأول: تستقبل النصوص المستخرجة للمستندين،
    وتمررها لنموذج LLM لإصدار قرار المطابقة وسبب الحكم.
    """
    try:
        # استدعاء الخدمة الحقيقية للتحدي الأول
        raw_json_response = challenge_a_service.analyze_documents(
            data.doc_alpha_text, 
            data.doc_beta_text
        )
        return raw_json_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل معالجة التحدي الأول: {str(e)}")


# ==========================================
# 📊 التحدي الثاني: Requirements Extraction
# ==========================================
@app.post("/api/challenge-b", response_model=RequirementsEnvelope)
async def process_challenge_b(file: UploadFile = File(...)):
    """
    نقطة النهاية للتحدي الثاني: تستقبل ملف الـ PDF،
    وتحلله عبر DeepSeek VLM، لتعيد مصفوفة الـ 22 متطلباً.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="خطأ: يجب رفع ملف بصيغة PDF فقط.")
    
    try:
        pdf_bytes = await file.read()
        result = await challenge_b_service.extract_requirements(pdf_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل معالجة التحدي الثاني: {str(e)}")