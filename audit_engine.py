import os
import json
from main import parse_rental_document
from rag_database import retrieve_relevant_laws
from google import genai

def audit_rental_dispute(sample_text: str):
    print("Step 1: Extracting structured data from lease agreement...")
    dispute_data = parse_rental_document(sample_text)
    data_dict = dispute_data.model_dump()
    
    print("\nStep 2: Retrieving relevant statutory laws from ChromaDB...")
    query = f"{data_dict.get('dispute_category', '')} {' '.join(data_dict.get('unlawful_clauses', []))}"
    relevant_laws = retrieve_relevant_laws(query, k=2)
    
    laws_context = "\n\n".join([
        f"Source: {doc.metadata['source']}\nContent: {doc.page_content}"
        for doc in relevant_laws
    ])
    
    print("\nStep 3: Running Legal Cross-Examination Audit Engine...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API Key not provided. Please enter it in the sidebar.")
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a senior Indian Legal Auditor specializing in Tenancy Rights.
    Evaluate the following tenant-landlord dispute by cross-examining the extracted lease details 
    against the retrieved statutory laws.

    --- EXTRACTED LEASE FACTS ---
    {json.dumps(data_dict, indent=2)}

    --- APPLICABLE STATUTORY LAWS ---
    {laws_context}

    --- AUDIT INSTRUCTIONS ---
    Provide a comprehensive dispute audit with the following sections:
    1. LEGAL VIOLATIONS DETECTED: Identify specific clauses or landlord actions that violate statutory laws.
    2. FINANCIAL RECOVERY ESTIMATE: Calculate the exact deposit amount legally refundable to the tenant based on the 2-month deposit limit and unlawful deduction rules.
    3. RECOMMENDED ESCALATION PATH: Recommend specific step-by-step actions (e.g., Formal Legal Notice, Rent Authority Complaint, Consumer Forum).
    """
    
    candidate_models = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    last_error = None
    content_text = ""
    
    for model_id in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            content_text = response.text
            break
        except Exception as e:
            last_error = e
            continue
            
    if not content_text:
        raise RuntimeError(f"All candidate models failed: {last_error}")
        
    return content_text, dispute_data

if __name__ == "__main__":
    sample_lease_text = """
    LEAVE AND LICENSE AGREEMENT
    This Agreement is made on 10th January 2024 between Mr. Vikram Singh (Licensor/Landlord)
    and Ms. Priya Sharma (Licensee/Tenant).
    Property Location: Flat 301, Blue Ridge Towers, Hinjewadi, Pune.
    Monthly Rent: Rs 28,000.
    Security Deposit: Rs 1,68,000 (Equivalent to 6 months rent).
    Notice Period: 30 days.

    TERMS & CONDITIONS:
    1. Landlord reserves the right to deduct 100% of the security deposit for painting 
       and routine wear-and-tear regardless of tenure.
    2. Landlord may enter the premises without prior notification at any time.

    TENANT DISPUTE NOTES:
    Tenant served 30 days notice via email and vacated property. Landlord is refusing to refund 
    the Rs 1,68,000 security deposit citing wall repainting costs and unannounced property inspection fees.
    """
    
    audit_report, _ = audit_rental_dispute(sample_lease_text)
    print("\n" + "="*50)
    print("           FINAL LEGAL AUDIT REPORT           ")
    print("="*50 + "\n")
    print(audit_report)