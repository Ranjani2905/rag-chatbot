from qdrant_client import QdrantClient
from qdrant_client.models import CollectionInfo, VectorParams
import os

# Initialize Qdrant client (Change 'localhost' to your server if needed)
qdrant = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "pdf_docs"

# Function to initialize Qdrant collection
def initialize_qdrant():
    existing_collections = [col.name for col in qdrant.get_collections().collections]
    
    if COLLECTION_NAME not in existing_collections:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance="Cosine")  # Vector size should match model output
        )
        print(f"✅ Created Qdrant Collection: {COLLECTION_NAME}")
    else:
        print(f"✅ Qdrant Collection `{COLLECTION_NAME}` already exists!")

initialize_qdrant()
