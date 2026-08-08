"""
splitter.py

Splits documents into smaller chunks
before generating embeddings.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


class DocumentSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_documents(self, documents):

        """
        Splits LangChain Document objects
        into smaller chunks.
        """

        chunks = self.splitter.split_documents(documents)

        return chunks

    def split_text(self, text: str):

        """
        Splits raw text into chunks.
        """

        chunks = self.splitter.split_text(text)

        return chunks

    def print_chunk_info(self, chunks):

        """
        Utility function for debugging.
        """

        print("=" * 60)

        print(f"Total Chunks : {len(chunks)}")

        print("=" * 60)

        for i, chunk in enumerate(chunks):

            print(f"\nChunk {i+1}")

            print("-" * 40)

            if hasattr(chunk, "page_content"):
                print(chunk.page_content[:300])
            else:
                print(chunk[:300])