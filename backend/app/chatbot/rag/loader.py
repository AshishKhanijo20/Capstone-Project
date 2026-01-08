from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def load_document(file_path: str) -> List[Document]:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {ext}")

    if ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")

    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)

    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(file_path)

    docs = loader.load()

    for doc in docs:
        doc.metadata.update({
            "source": path.name,
            "path": str(path),
            "file_type": ext,
        })

    return docs


def load_documents_from_dir(directory: str) -> List[Document]:
    all_docs: List[Document] = []

    for file in Path(directory).rglob("*"):
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                docs = load_document(str(file))
                all_docs.extend(docs)
            except Exception as e:
                print(f"[RAG Loader] Failed to load {file}: {e}")

    return all_docs




