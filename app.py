import streamlit as st
import tempfile
import os
from main import extract_text_from_pdf
from audit_engine import audit_rental_dispute
from pdf_generator import generate_legal_notice_pdf

st.set_page_config(
    page_title="Tenant Rights & Rental Dispute Resolver",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Tenant Rights & Rental Dispute Resolver")
st.subheader("AI-Powered Legal Audit & Deposit Recovery Engine (Indian Tenancy Law)")
st.write("---")

# Sidebar
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", value=os.environ.get("GEMINI_API_KEY", ""), type="password")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

# Fast Testing Toggle
use_mock = st.sidebar.checkbox("⚡ Fast Testing Mode (Skip AI Quotas)", value=False)

uploaded_file = st.sidebar.file_uploader("Upload Lease Agreement (PDF)", type=["pdf"])

st.markdown("### Enter Dispute Text or Upload Agreement")
sample_default_text = """LEAVE AND LICENSE AGREEMENT
This Agreement is made on 10th January 2024 between Mr. Vikram Singh (Landlord) and Ms. Priya Sharma (Tenant).
Property Location: Flat 301, Blue Ridge Towers, Hinjewadi, Pune.
Monthly Rent: Rs 28,000.
Security Deposit: Rs 1,68,000 (Equivalent to 6 months rent).
Notice Period: 30 days.

TERMS & CONDITIONS:
1. Landlord reserves the right to deduct 100% of the security deposit for painting and routine wear-and-tear regardless of tenure.
2. Landlord may enter the premises without prior notification at any time.

TENANT DISPUTE NOTES:
Tenant served 30 days notice via email and vacated property. Landlord is refusing to refund the Rs 1,68,000 security deposit citing wall repainting costs and unannounced property inspection fees."""

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    raw_text = extract_text_from_pdf(tmp_path)
    os.remove(tmp_path)
    st.success("PDF uploaded and parsed successfully!")
else:
    raw_text = st.text_area("Dispute Agreement & Notes", value=sample_default_text, height=220)

if st.button("🔍 Run Legal Audit", type="primary"):
    with st.spinner("Analyzing contract, retrieving statutory laws, and running audit..."):
        try:
            if use_mock:
                # Instant response for quick layout and PDF testing
                report = """## 📊 LEGAL AUDIT REPORT: TENANCY DISPUTE EVALUATION

### 1. LEGAL VIOLATIONS DETECTED
1. **Contravention of Security Deposit Cap (Section 11, Model Tenancy Act):** Landlord collected ₹1,68,000 (6 months rent) exceeding statutory limit of 2 months rent.
2. **Unlawful Deductions for Wear & Tear (Section 21, Model Tenancy Act):** Deductions for repainting/routine wear are illegal.

### 2. FINANCIAL RECOVERY ESTIMATE
* **Monthly Rent:** ₹28,000.00
* **Total Security Deposit Paid:** ₹1,68,000.00
* **TOTAL LEGALLY REFUNDABLE AMOUNT:** ₹1,68,000.00

### 3. RECOMMENDED ESCALATION PATH
* **Step 1:** Serve Formal Legal Demand Notice (15 days notice).
* **Step 2:** File Complaint with Rent Authority / Consumer Forum."""
                
                class MockData:
                    landlord_name = "Vikram Singh"
                    tenant_name = "Priya Sharma"
                    property_address = "Flat 301, Blue Ridge Towers, Hinjewadi, Pune"
                    security_deposit = 168000.0
                
                extracted_data = MockData()
            else:
                report, extracted_data = audit_rental_dispute(raw_text)
            
            st.markdown("## 📊 Legal Audit & Escalation Report")
            st.markdown(report)
            
            pdf_file_path = generate_legal_notice_pdf(
                landlord_name=getattr(extracted_data, 'landlord_name', 'Landlord') or "Landlord",
                tenant_name=getattr(extracted_data, 'tenant_name', 'Tenant') or "Tenant",
                property_address=getattr(extracted_data, 'property_address', 'Property Address') or "Rental Property",
                deposit_amount=getattr(extracted_data, 'security_deposit', 0.0) or 0.0
            )
            
            with open(pdf_file_path, "rb") as file:
                st.download_button(
                    label="📄 Download Official Legal Demand Notice (PDF)",
                    data=file,
                    file_name="Formal_Legal_Demand_Notice.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error during legal audit execution: {str(e)}")