# Tenant Rights & Rental Dispute Resolver ⚖️🤖

An AI-powered legal audit and deposit recovery engine built to evaluate tenant-landlord disputes under Indian Tenancy Law (Model Tenancy Act & Rent Control Acts).

## 🌟 Key Features
- **Lease Document Analysis:** Parses structured lease metadata (rent, deposit, notice period, clauses) using Gemini AI.
- **RAG-Powered Legal Audit:** Queries a vector database (ChromaDB) to ground legal audits in statutory laws.
- **Deposit Recovery Estimation:** Automatically calculates legally refundable security deposit amounts.
- **Automated Escalation PDF:** Generates formal legal demand notices in downloadable PDF format.

## 🛠️ Tech Stack
- **Framework:** Python, Streamlit
- **LLM & Embeddings:** Google Gemini API, LangChain
- **Vector Store:** ChromaDB
- **PDF Generation:** FPDF / ReportLab

## 🚀 Getting Started

### 1. Prerequisites & Installation
Clone the repository and install dependencies:
```bash
git clone [https://github.com/LizaMallick/tenant_rights_ai.git](https://github.com/LizaMallick/tenant_rights_ai.git)
cd tenant_rights_ai
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
