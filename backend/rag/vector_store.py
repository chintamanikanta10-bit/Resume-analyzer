"""
vector_store.py

Creates and manages the Chroma Vector Database.
"""

from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma

from config import (
    EMBEDDING_MODEL,
    VECTOR_DB_PATH
)


class VectorStoreService:
    """
    Handles storing and loading document embeddings.
    """

    def __init__(self, user_id: int | None = None):
        self.user_id = user_id
        self.embedding_model = EMBEDDING_MODEL
        self.persist_directory = str(VECTOR_DB_PATH / str(user_id or "shared"))
        self.vector_db = None

    # --------------------------------------------------------

    def create_vector_store(self, chunks: List[Document]):

        """
        Creates a new Chroma vector database.
        """

        self.vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory
        )

        return self.vector_db

    # --------------------------------------------------------

    def load_vector_store(self):

        """
        Loads an existing Chroma database.
        """

        self.vector_db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

        return self.vector_db

    # --------------------------------------------------------

    def get_vector_store(self):

        """
        Returns the vector database instance.
        """

        if self.vector_db is None:

            self.load_vector_store()

        return self.vector_db

    # --------------------------------------------------------

    def total_documents(self):

        """
        Returns number of stored chunks.
        """

        db = self.get_vector_store()

        return db._collection.count()