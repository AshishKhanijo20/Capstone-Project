from app.chatbot.rag.loader import load_documents_from_dir
from app.chatbot.rag.chunking import chunk_text
from app.chatbot.rag.vectorstore import load_vector_db

def run_manual_ingestion():
    try:
        print("🔹 Loading documents...")
        docs = load_documents_from_dir("app/chatbot/rag/kb")
        print(f"Loaded {len(docs)} documents")

        print("🔹 Chunking documents...")
        chunks = chunk_text(docs)
        print(f"Created {len(chunks)} chunks")

        # Add metadata (IMPORTANT)
        for chunk in chunks:
            chunk.metadata.update({
                "memory_scope": "permanent",
                "source_type": "knowledge_base"
            })

        print("🔹 Storing in Chroma...")
        vector_db = load_vector_db()
        vector_db.add_documents(chunks)
        #vector_db.persist()

        print("✅ Manual ingestion complete!")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Manual ingestion started")
    run_manual_ingestion()
    print("✅ Manual ingestion finished")
