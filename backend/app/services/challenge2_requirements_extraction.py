import os
import sys
import base64
import io
import json
import requests
from app.core.schemas import RequirementsEnvelope
from app.utils.pdf_processor import convert_pdf_to_images

class ChallengeBService:
    def __init__(self):
        # التوكن المجاني الخاص بكِ من حساب Hugging Face
        self.hf_token = os.getenv("HF_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        # 1. الرابط السحابي المباشر لنموذج DeepSeek VLM النقي
        self.deepseek_vlm_url = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-OCR-2"
        
        # 2. الرابط السحابي للنموذج النصي الاستدلالي من ديب سيك
        self.deepseek_chat_url = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

    def _prepare_image_for_vlm(self, image) -> str:
        """تحويل كائن الصورة في الذاكرة إلى نص مشفر Base64 لإرساله لـ DeepSeek VLM"""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    async def extract_requirements(self, pdf_bytes: bytes) -> RequirementsEnvelope:
        """
        خط إنتاج معتمد على عائلة DeepSeek السحابية فقط (بدون أي بيانات افتراضية)
        """
        # 1. تفكيك المستند إلى صور في الذاكرة
        images = convert_pdf_to_images(pdf_bytes, dpi=150)
        
        print("⏳ المرحلة 1: القراءة البصرية الحصرية عبر DeepSeek-OCR-2 VLM...")
        base64_image = self._prepare_image_for_vlm(images[0])
        
        vlm_payload = {
            "inputs": f"قم بقراءة وتحليل هذه الصورة واستخراج كافة النصوص والجداول المكتوبة فيها باللغة العربية بدقة شديدة ودون تحريف:\n[Image: data:image/jpeg;base64,{base64_image}]",
            "parameters": {"max_new_tokens": 1024}
        }
        
        # استدعاء الـ VLM (إذا فشل سيرتفع الخطأ فوراً للواجهة)
        vlm_resp = requests.post(self.deepseek_vlm_url, headers=self.headers, json=vlm_payload)
        vlm_resp.raise_for_status()
        vlm_result = vlm_resp.json()
        extracted_text = vlm_result[0].get("generated_text", "") if isinstance(vlm_result, list) else str(vlm_result)

        # ----------------------------------------------------
        # المرحلة الثانية: الهيكلة والمنطق الصارم عبر DeepSeek Chat
        # ----------------------------------------------------
        print("⏳ المرحلة 2: صياغة قالب الـ JSON النهائي عبر عائلة DeepSeek...")
        
        system_prompt = (
            "أنت مهندس ومطابق أنظمة خبير في هيئة الحكومة الرقمية بالمملكة العربية السعودية. "
            "قم بفحص النص واستخراج متطلبات كتيب المنظور الرابع. "
            "يجب أن تعيد المخرج النهائي بصيغة كائن JSON يحتوي على حقل أساسي باسم 'requirements' يضم قائمة الكائنات، وبدون أي مقدمات:"
        )
        
        deepseek_payload = {
            "inputs": f"<｜System｜>{system_prompt}<｜User｜>إليك النص المفرغ بصرياً:\n{extracted_text}\nقم بتوليد الـ JSON المطلوب الآن:",
            "parameters": {"max_new_tokens": 1500}
        }
        
        # استدعاء ديب سيك شات للهيكلة
        ds_resp = requests.post(self.deepseek_chat_url, headers=self.headers, json=deepseek_payload)
        ds_resp.raise_for_status()
        ds_result = ds_resp.json()
        
        raw_json = ds_result[0].get("generated_text", "{}") if isinstance(ds_result, list) else str(ds_result)
        
        # تنظيف النص لانتزاع الـ JSON الصافي بين الأقواس
        if "{" in raw_json and "}" in raw_json:
            start_idx = raw_json.find("{")
            end_idx = raw_json.rfind("}") + 1
            raw_json = raw_json[start_idx:end_idx]
            
        # التحقق الحجمي والمطابقة مع الـ Schema وعرضها فوراً
        validated_envelope = RequirementsEnvelope.parse_raw(raw_json)
        return validated_envelope