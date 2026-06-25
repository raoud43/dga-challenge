import os
import sys

# حساب المسار الرئيسي للمشروع (المجلد الأب للفرونت إند والباكيند) وحقنه في بايثون
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

    
import json
import requests
# بقية الاستدعاءات...
# الآن بقية الـ Imports الخاصة بكِ ستعمل بأمان تّام
import streamlit as st
# ... بقية الاستيرادات الكود الخاص بكِ

# تحديد رابط الـ Backend بشكل ديناميكي (محلياً أو سحابياً عبر دوكر)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# إعدادات الشاشة الأساسية
st.set_page_config(page_title="AI Engineering Challenge Dashboard", layout="wide")

# ... (هنا نترك كود الـ CSS والاستايل المكتوب في رسالتكِ كما هو دون تغيير) ...

st.markdown("<h1 class='main-title'>AI Engineering Challenge Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

tab_challenge_a, tab_challenge_b = st.tabs([
    "🎯 Challenge A — Requirement-18 Detection", 
    "📊 Challenge B — Requirements Extraction (VLM + LLM)"
])

# =========================================================================
# 🎯 التحدي الأول الحقيقي عبر الـ API
# =========================================================================
with tab_challenge_a:
    st.markdown("<h2 class='challenge-header'>🎯 Challenge A: Requirement-18 Detection</h2>", unsafe_allow_html=True)
    
    st.markdown("### 📤 Upload the documents")
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        file_alpha = st.file_uploader("(Evidence Pack Alpha)", type=["docx"], key="upload_alpha")
    with col_up2:
        file_beta = st.file_uploader("(Evidence Pack Beta)", type=["docx"], key="upload_beta")
    
    if st.button("🚀 Run Compliance Audit", key="btn_run_a"):
        if file_alpha and file_beta:
            with st.spinner("جاري الاستخراج والتحليل عبر الـ API الخلفي..."):
                try:
                    # 1. استخراج النصوص محلياً في الواجهة لتوفير حجم نقل البيانات
                    from backend.app.utils.docx_parser import extract_text_and_tables_from_docx
                    
                    doc_alpha_text = extract_text_and_tables_from_docx(file_alpha.getvalue())
                    doc_beta_text = extract_text_and_tables_from_docx(file_beta.getvalue())
                    
                    # 2. إرسال البيانات عبر الـ HTTP POST إلى الـ FastAPI Backend
                    payload = {
                        "doc_alpha_text": doc_alpha_text,
                        "doc_beta_text": doc_beta_text
                    }
                    response = requests.post(f"{BACKEND_URL}/api/challenge-a", json=payload)
                    
                    if response.status_code == 200:
                        # تحويل النص المستلم إلى قاموس بايثون والتعامل معه ديناميكياً
                        backend_output = response.json()
                        if isinstance(backend_output, str):
                            backend_output = json.loads(backend_output)
                        
                        # ... (هنا نترك كود الرسم والتظليل البصري للأعمدة col_res1 و col_res2 كما كتبتيه تماماً) ...
                        st.success("🎯 اكتمل التحليل المتقاطع بنجاح!")
                        st.code(response.json(), language="json")
                    else:
                        st.error(f"❌ خطأ في الاتصال بالخادم: {response.text}")
                except Exception as e:
                    st.error(f"🚨 فشل النظام في معالجة الملفات: {str(e)}")
        else:
            st.warning("⚠️ الرجاء رفع الملفين معاً لبدء عملية المقارنة.")

# =========================================================================
# 📊 التحدي الثاني الحقيقي عبر الـ VLM API
# =========================================================================
with tab_challenge_b:
    st.markdown("<h2 class='challenge-header'>📊 Challenge B: Requirements Extraction (VLM + LLM)</h2>", unsafe_allow_html=True)
    
    st.markdown("### 📤 رفع وثائق المتطلبات البصرية")
    file_challenge_b = st.file_uploader("ارفع ملف PDF الخاص بالدليل الحكومي", type=["pdf"], key="upload_vlm")
    
    if st.button("🔍 تحليل واستخراج المتطلبات عبر الـ VLM", key="btn_run_b"):
        if file_challenge_b:
            with st.spinner("جاري إرسال الملف وتحليله بصرياً عبر نموذج DeepSeek VLM السحابي..."):
                try:
                    # إرسال ملف الـ PDF كـ Multipart Form Data إلى الـ Backend
                    files = {"file": (file_challenge_b.name, file_challenge_b.getvalue(), "application/pdf")}
                    response = requests.post(f"{BACKEND_URL}/api/challenge-b", files=files)
                    
                    if response.status_code == 200:
                        extracted_data = response.json()
                        st.success("🎯 تم الاستخراج البصري وتحقيق البنية الهيكلية بنجاح!")
                        
                        # عرض البيانات الحقيقية في جدول مبهر ومنظم
                        st.subheader("📋 مصفوفة المتطلبات المستخرجة من المستند")
                        
                        requirements_list = extracted_data.get("requirements", [])
                        
                        # بناء جدول Streamlit تفاعلي حقيقي يعرض الـ 8 حقول المستخرجة بذكاء
                        st.dataframe(requirements_list, use_container_width=True)
                        
                        # إضافة زر لتحميل ملف الـ JSON النهائي لتعزيز جودة التسليم (Maximum Criterion)
                        json_string = json.dumps(extracted_data, ensure_ascii=False, indent=4)
                        st.download_button(
                            label="📥 تحميل مصفوفة المتطلبات كملف JSON مهيكل",
                            data=json_string,
                            file_name="digital_experience_requirements.json",
                            mime="application/json"
                        )
                    else:
                        st.error(f"❌ فشل السيرفر في معالجة الصور: {response.text}")
                except Exception as e:
                    st.error(f"🚨 خطأ أثناء معالجة خط إنتاج الـ VLM: {str(e)}")
        else:
            st.warning("⚠️ الرجاء رفع مستند PDF للبدء.")