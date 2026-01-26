from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_text(
    documents: List[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 100
) -> List[Document]:
   

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    return splitter.split_documents(documents)

