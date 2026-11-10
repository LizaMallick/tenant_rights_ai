import os
import json
from typing import Optional, List
from pydantic import BaseModel, Field
import pdfplumber
from google import genai
from google.genai import types

class RentalDisputeData(BaseModel):
    landlord_name: Optional[str] = Field(description="Full name of the landlord")
    tenant_name: Optional[str] = Field(description="Full name of the tenant")
    property_address: Optional[str] = Field(description="Full address of the rental property")
    monthly_rent: Optional[float] = Field(description="Agreed monthly rent amount")
    security_deposit: Optional[float] = Field(description="Security deposit paid by tenant")
    notice_period_days: Optional[int] = Field(description="Notice period required in days")
    dispute_category: Optional[str] = Field(
        description="Type of issue: Deposit Refund, Maintenance, Unfair Eviction, etc."
    )
    unlawful_clauses: List[str] = Field(
        default=[],
        description="List of clauses in the lease that seem illegal or unfair to the tenant"
    )
    summary_of_issue: Optional[str] = Field(
        description="Short 2-sentence summary of the main dispute"
    )

def extract_text_from_pdf(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found at: {pdf_path}")
        
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    return extracted_text

def parse_rental_document(raw_text: str) -> RentalDisputeData:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API Key not provided. Please enter it in the sidebar.")
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert legal assistant specializing in Indian rental disputes.
    Extract key tenancy terms and dispute details from the document text below.
    Identify any potential lease terms that seem unfair or violate standard tenant rights.

    --- DOCUMENT TEXT START ---
    {raw_text}
    --- DOCUMENT TEXT END ---
    """
    
    candidate_models = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    last_error = None
    
    for model_id in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RentalDisputeData,
                    temperature=0
                )
            )
            return RentalDisputeData.model_validate_json(response.text)
        except Exception as e:
            last_error = e
            continue
            
    raise RuntimeError(f"All candidate models failed: {last_error}")

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

    print("Processing raw rental text...")
    parsed_data = parse_rental_document(sample_lease_text)
    print("--- VERIFIED STRUCTURED OUTPUT ---")
    print(json.dumps(parsed_data.model_dump(), indent=2))