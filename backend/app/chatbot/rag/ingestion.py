from typing import List, Dict,Optional
from datetime import datetime
from langchain_core.documents import Document
from rag.chunking import chunk_text
from rag.vectorstore import load_vector_db

def ingest_documents(
        documents: List[Document],
        extra_metadata : Optional[Dict] = None
    ) -> Dict:

    if not documents:
        return {
            "documents_received" :0,
            "chunks_added" : 0,
            "status" :"no_documents"
        }
    chunks = chunk_text(documents)
    vector_db = load_vector_db()
    vector_db.add_documents(chunks)
    vector_db.persist()

    return {
        "documents_received": len(documents),
        "chunks_added": len(chunks),
        "status": "success"
    }





