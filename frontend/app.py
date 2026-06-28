import os
import sys
import json
import requests
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from config import settings

st.set_page_config(page_title="AI Engineering Challenge Dashboard", layout="wide")


if 'res_a' not in st.session_state: st.session_state.res_a = None
if 'res_b1' not in st.session_state: st.session_state.res_b1 = None
if 'res_b2' not in st.session_state: st.session_state.res_b2 = None


# Custom CSS 
st.markdown("""
    <style>
    .main-title { font-family: sans-serif; color: #2E86C1; text-align: center; }
    .challenge-header { font-family: sans-serif; color: #1B4F72; border-bottom: 2px solid #2E86C1; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>AI Engineering Challenge Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

tab_a, tab_b = st.tabs(["🎯 Challenge A — Requirement-18 Detection", "📊 Challenge B — Requirements Extraction (VLM + LLM)"])

# =========================================================================
# Challenge A
# =========================================================================
with tab_a:
    st.markdown("<h2 class='challenge-header'>🎯  Requirement-18 Detection</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: file_alpha = st.file_uploader("Evidence Pack Alpha", type=["docx"], key="alpha")
    with col2: file_beta = st.file_uploader("Evidence Pack Beta", type=["docx"], key="beta")
    
    if st.button("🚀 Run Compliance Audit", key="run_a"):
        if file_alpha and file_beta:
            with st.spinner("🚀 Analyzing documents with Gemini (this may take a minute)..."):
                try:
                    files = {
                        'file_alpha': (file_alpha.name, file_alpha.getvalue(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                        'file_beta': (file_beta.name, file_beta.getvalue(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    }
                    backend_url = settings.BACKEND_URL.rstrip('/') 
                    full_url = f"{backend_url}/api/challenge-a"


                    response = requests.post(full_url, files=files, timeout=300)
                    
                    if response.status_code == 200:
                        st.session_state.res_a = response.json()
                        st.rerun() 
                    else:
                        st.error(f"❌ Server Error ({response.status_code}): {response.text}")
                except requests.exceptions.ReadTimeout:
                    st.error("⏰ Error: The request timed out. The server is still processing, please try again later.")
                except Exception as e:
                    st.error(f"🚨 Pipeline Error: {str(e)}")
        else:
            st.warning("⚠️ Please upload both documents.")

    if st.session_state.res_a:
        st.success("🎯 Compliance audit complete!")
        st.json(st.session_state.res_a)
        st.download_button("📥 Download JSON Results", 
                           data=json.dumps(st.session_state.res_a, indent=4, ensure_ascii=False),
                           file_name="challenge_a_results.json", mime="application/json")

# =========================================================================
# Challenge B 
# =========================================================================
with tab_b:
    st.markdown("<h2 class='challenge-header'>📊 Requirements Extraction (VLM + LLM)</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)

    
    def get_axis_style(axis_number):
        colors = {1: "#FFF9C4", 2: "#E3F2FD", 3: "#FFEBEE", 4: "#E8F5E9", 5: "#FCE4EC"}
        borders = {1: "#FBC02D", 2: "#1976D2", 3: "#D32F2F", 4: "#388E3C", 5: "#C2185B"}
        color = colors.get(axis_number, "#F5F5F5")
        border = borders.get(axis_number, "#9E9E9E")
        return color, border

    def process_and_display(file, col, state_key, title):
        with col:
            st.subheader(title)
            uploaded_file = st.file_uploader(f"Upload {title}", type=["pdf"], key=f"uploader_{state_key}")
            if st.button(f"🔍 Analyze {title}", key=f"btn_{state_key}"):
                if uploaded_file:
                    with st.spinner("Analyzing..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        backend_url = settings.BACKEND_URL.rstrip('/')
                        full_url = f"{backend_url}/api/challenge-b"

                        response = requests.post(full_url, files=files)
                        if response.status_code == 200:
                            st.session_state[state_key] = response.json()
                        else:
                            st.error(f"Server Error: {response.text}")

            if state_key in st.session_state and st.session_state[state_key]:
                data = st.session_state[state_key]
                
                
                st.download_button(
                    label=f"📥 Download {title} JSON",
                    data=json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8'),
                    file_name=f"{state_key}_results.json",
                    mime="application/json"
                )

               
                for req in data.get("requirements", []):
                    axis_num = req.get('axis_number', 0)
                    bg_color, border_color = get_axis_style(axis_num)
                    
                    
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                        <h4 style="margin-top:0;">{req.get('requirement_number')}. {req.get('axis_name')}</h4>
                        <p><b>التعريف:</b> {req.get('requirement_definition')}</p>
                        <p><b>السؤال:</b> {req.get('question')}</p>
                        <p><b>أمثلة الأدلة:</b> {', '.join(str(e) for e in req.get('evidence_examples', []))}</p>
                        <p><b>صيغة الدليل:</b> {req.get('evidence_format')}</p>
                        <p><b>مؤشر الشمولية:</b> {req.get('counts_toward_inclusivity_index')}</p>
                        <small>صفحة المستند: {req.get('document_page_number')}</small>
                    </div>
                    """, unsafe_allow_html=True)

    process_and_display(None, col_a, 'res_b1', "Guide 1")
    process_and_display(None, col_b, 'res_b2', "Guide 2")