import os
from dotenv import load_dotenv
#from langchain.vectorstores import Chroma
from langchain_chroma import Chroma
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

load_dotenv()

VECTOR_STORE_DIR = os.getenv("VECTOR_STORE", "./vector_store")

_embeddings = OpenAIEmbeddings()


def load_vector_db() -> Chroma:
    """
    Initialize or load the persistent Chroma vector store.
    """
    return Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=_embeddings,
        collection_name="capstone"
    )
