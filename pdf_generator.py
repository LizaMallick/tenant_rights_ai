import tempfile
from fpdf import FPDF

class LegalNoticePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, 'FORMAL LEGAL DEMAND NOTICE', border=0, ln=1, align='C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 6, '(Issued under Section 11 & Section 21 of the Model Tenancy Act)', border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_legal_notice_pdf(landlord_name: str, tenant_name: str, property_address: str, deposit_amount: float) -> str:
    pdf = LegalNoticePDF()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 11)
    
    notice_text = f"""
BY REGISTERED POST / EMAIL

TO:
{landlord_name}
Landlord / Property Owner
Re: {property_address}

FROM:
{tenant_name}
Former Tenant

SUBJECT: LEGAL DEMAND NOTICE FOR IMMEDIATE REFUND OF SECURITY DEPOSIT (RS. {deposit_amount:,.2f})

Sir/Madam,

Under instructions from my client, {tenant_name}, I hereby serve you with this formal Legal Demand Notice:

1. My client entered into a rental agreement with you for the premises located at {property_address}.

2. My client has fully complied with all terms of the tenancy, including serving the requisite notice period and handing over vacant possession of the premises.

3. As per statutory provisions under Section 11 and Section 21 of the Model Tenancy Act, deductions for routine wear-and-tear or repainting are unlawful, and security deposit retention is strictly regulated.

4. You have wrongfully withheld the security deposit of Rs. {deposit_amount:,.2f} without statutory justification.

TAKE NOTICE that you are hereby called upon to refund the full principal amount of Rs. {deposit_amount:,.2f} along with interest at 9% p.a. within FIFTEEN (15) DAYS of receipt of this notice.

Failure to comply will compel my client to initiate appropriate legal proceedings before the Rent Authority / Consumer Disputes Redressal Commission at your sole risk and costs.

Dated this day.

Sincerely,
Advocate / Authorized Representative
(For {tenant_name})
"""
    
    pdf.multi_cell(0, 7, notice_text)
    
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name