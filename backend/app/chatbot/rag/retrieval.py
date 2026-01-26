from typing import Optional, List

from langchain_core.documents import Document
from langchain_core.tools import tool

from app.chatbot.rag.vectorstore import load_vector_db


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

def retrive_context(
        query: str,
        ticket_id: Optional[str] = None,
        k: int = 4
) -> str:
    vector_db = load_vector_db()
    if ticket_id:
        filters = {
            "$or" : [
                {"memory_scope" : "temporary"},
                {"ticket_id": ticket_id}

            ]
        }
    else:
        filters = {"memory_scope" : "permanent"}


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


    