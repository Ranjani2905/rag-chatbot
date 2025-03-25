import fitz  # PyMuPDF for PDF text extraction
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from db import qdrant, COLLECTION_NAME

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text_chunks = [page.get_text("text") for page in doc]  # Extract text per page
    return text_chunks

def store_embeddings(pdf_path):
    """Processes the PDF, generates embeddings, and stores them in Qdrant."""
    chunks = extract_text_from_pdf(pdf_path)
    points = []
    
    for idx, chunk in enumerate(chunks):
        vector = model.encode(chunk).tolist()
        points.append(PointStruct(id=idx, vector=vector, payload={"text": chunk}))

    # Insert vectors into Qdrant
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ PDF `{pdf_path}` processed and stored in Qdrant.")

if __name__ == "__main__":
    store_embeddings("E:/Skillmine internship/rag-chatbot/pdfs/Ch 8 Childhood mental and developmental disorders.pdf")  # Test with a sample PDF
