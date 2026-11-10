import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

# 1. Initialize Gemini Embeddings with the updated model name
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ.get("GEMINI_API_KEY")
)

# 2. Key Tenancy Laws & Regulations Dataset
LEGAL_RULES_DATASET = [
    {
        "source": "Model Tenancy Act - Section 11",
        "content": "Security deposit for residential premises shall not exceed a maximum of two months' rent. Any security deposit collected beyond two months' rent must be refunded to the tenant upon vacation."
    },
    {
        "source": "Model Tenancy Act - Section 15",
        "content": "A landlord or property manager cannot enter the rented premises without giving at least 24 hours prior written or digital notice to the tenant stating the reason for entry."
    },
    {
        "source": "Model Tenancy Act - Section 21",
        "content": "Landlords are responsible for structural repairs and general maintenance. Deductions for routine wear and tear or repainting are unlawful unless explicit structural damage caused by tenant negligence is proven."
    },
    {
        "source": "Rent Control Act - Essential Services",
        "content": "No landlord shall withhold or cut off any essential supply or service (water, electricity, elevator access) to the tenant during a dispute or tenancy."
    }
]

# 3. Function to Initialize and Store Data in ChromaDB
def build_vector_db():
    print("Indexing Tenancy Laws into local ChromaDB...")
    documents = [
        Document(page_content=item["content"], metadata={"source": item["source"]})
        for item in LEGAL_RULES_DATASET
    ]
    
    # Store documents on local disk under ./chroma_db
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("Knowledge base created successfully!")
    return vector_db

# 4. Function to Retrieve Relevant Laws
def retrieve_relevant_laws(query: str, k: int = 2):
    vector_db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    results = vector_db.similarity_search(query, k=k)
    return results

if __name__ == "__main__":
    # Build database
    build_vector_db()
    
    # Test retrieval
    test_query = "Can landlord retain deposit for repainting and routine wear and tear?"
    print(f"\nTesting Query: '{test_query}'")
    matched_docs = retrieve_relevant_laws(test_query)
    
    print("\n--- MATCHED STATUTORY LAWS FROM CHROMADB ---")
    for doc in matched_docs:
        print(f"\nSource: {doc.metadata['source']}")
        print(f"Content: {doc.page_content}")