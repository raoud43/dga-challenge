import os
import json
from app.utils.docx_parser import extract_text_and_tables_from_docx
from app.services.challenge1_requirement18_detection import ChallengeAService

def run_production_challenge_a_test():
    print("🚀 Starting Challenge A Verification Test with Absolute Paths...\n")
    
    # 1. Using your exact workspace paths
    alpha_path = "/workspaces/dga-challenge/backend/evidence pack alpha.docx"
    beta_path = "/workspaces/dga-challenge/backend/evidence pack beta.docx"
    
    # Check if files exist to prevent system crash
    if not os.path.exists(alpha_path) or not os.path.exists(beta_path):
        print("❌ Error: Verification failed. One or both files do not exist at the specified paths!")
        print(f"Alpha exists: {os.path.exists(alpha_path)}")
        print(f"Beta exists: {os.path.exists(beta_path)}")
        return

    print("📖 Step 1: Reading raw binary bytes from workspace...")
    with open(alpha_path, "rb") as f:
        alpha_bytes = f.read()
        
    with open(beta_path, "rb") as f:
        beta_bytes = f.read()

    print("🧹 Step 2: Extracting text and parsing tables into Markdown rows...")
    extracted_alpha_text = extract_text_and_tables_from_docx(alpha_bytes)
    extracted_beta_text = extract_text_and_tables_from_docx(beta_bytes)

    print("🧠 Step 3: Invoking gemini-2.5-flash LLM for causal reasoning over Requirement 18...")
    auditor = ChallengeAService()
    
    try:
        raw_json_result = auditor.analyze_documents(extracted_alpha_text, extracted_beta_text)
        
        print("\n" + "="*20 + " EVALUATION OUTPUT " + "="*20)
        # Pretty print the JSON so it's easy for you to inspect
        parsed_json = json.loads(raw_json_result)
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
        print("=" * 59)
        
        print("\n🎉 Test executed successfully!")
        
    except Exception as e:
        print(f"\n❌ An error occurred during AI analysis: {str(e)}")

if __name__ == "__main__":
    run_production_challenge_a_test()