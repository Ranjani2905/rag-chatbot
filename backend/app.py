from fastapi import FastAPI, UploadFile, File
from qdrant_client.models import Filter
from sentence_transformers import SentenceTransformer
from db import qdrant, COLLECTION_NAME
import fitz

app = FastAPI()
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF, processes it, and stores embeddings in Qdrant."""
    pdf_text = ""
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    
    for page in doc:
        pdf_text += page.get_text()

    chunks = pdf_text.split("\n")  
    points = []
    
    for idx, chunk in enumerate(chunks):
        vector = model.encode(chunk).tolist()
        points.append({"id": idx, "vector": vector, "payload": {"text": chunk}})

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return {"message": "PDF uploaded and processed"}

@app.get("/ask/")
async def ask(question: str):
    """Retrieves the most relevant text chunk from the stored PDFs."""
    query_vector = model.encode(question).tolist()
    search_results = qdrant.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=3)

    answers = [hit.payload["text"] for hit in search_results]
    return {"answers": answers}
