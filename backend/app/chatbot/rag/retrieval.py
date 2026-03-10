from typing import Optional, List

from langchain_core.documents import Document
from langchain_core.tools import tool

from app.chatbot.rag.vectorstore import load_vector_db


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def infer_doc_type(query: str) -> str:
    incident_keywords = [
        "error", "failed", "stuck", "status", "heartbeat",
        "reprocess", "not working", "issue", "investigate"
    ]

    q = query.lower()
    if any(word in q for word in incident_keywords):
        return "incident"

    return "foundation"

def retrive_context(
        query: str,
        ticket_id: Optional[str] = None,
        k: int = 4
) -> str:
    vector_db = load_vector_db()
    doc_type = infer_doc_type(query)

    if ticket_id:
        filters = {
        "$and": [
            {
                "$or": [
                    {"memory_scope": "temporary"},
                    {"ticket_id": ticket_id}
                ]
            },
            {"doc_type": doc_type}
        ]
    }
    else:
        filters = {
        "$and": [
            {"memory_scope": "permanent"},
            {"doc_type": doc_type}
        ]
    }
        
    docs = vector_db.similarity_search(
        query=query,
        k=k,
        filter=filters
    )

    if not docs:
        return None

    return format_docs(docs)

@tool
def rag_search(
    query: str,
    ticket_id: Optional[str] = None
) -> str:
    """
    Search internal enterprise knowledge base for relevant information.
    Use this tool when the user asks about policies, documentation,
    or past resolutions.
    """
    return retrive_context(query=query, ticket_id=ticket_id)


    