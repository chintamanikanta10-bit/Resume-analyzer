"""
embeddings.py

Creates embeddings for document chunks and user queries.
"""

from typing import List

from langchain_core.documents import Document

from config import get_embedding_model


class EmbeddingService:
    """
    Handles embedding generation.
    """

    def __init__(self):
        pass

    @property
    def embedding_model(self):
        return get_embedding_model()

    # ----------------------------------------------------

    def embed_documents(self, chunks: List[Document]):

        """
        Generate embeddings for document chunks.
        """

        texts = []

        for chunk in chunks:
            texts.append(chunk.page_content)

        embeddings = self.embedding_model.embed_documents(texts)

        return embeddings

    # ----------------------------------------------------

    def embed_query(self, query: str):

        """
        Generate embedding for user query.
        """

        embedding = self.embedding_model.embed_query(query)

        return embedding

    # ----------------------------------------------------

    def get_text_list(self, chunks: List[Document]):

        """
        Returns only text from LangChain documents.
        """

        return [chunk.page_content for chunk in chunks]