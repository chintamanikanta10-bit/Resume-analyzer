"""
retriever.py

Retrieves the most relevant chunks
from ChromaDB.
"""

from config import TOP_K_RESULTS

from rag.vector_store import VectorStoreService


class RetrieverService:

    def __init__(self):
        self.vector_store = VectorStoreService()

    # --------------------------------------------------------

    def retrieve(self, query: str, user_id: int | None = None):

        """
        Returns the most relevant
        document chunks.
        """

        store = VectorStoreService(user_id=user_id)
        db = store.get_vector_store()

        results = db.similarity_search(

            query=query,

            k=TOP_K_RESULTS

        )

        return results

    # --------------------------------------------------------

    def retrieve_with_score(self, query: str, user_id: int | None = None):

        """
        Returns documents with similarity score.
        """

        store = VectorStoreService(user_id=user_id)
        db = store.get_vector_store()

        results = db.similarity_search_with_score(

            query=query,

            k=TOP_K_RESULTS

        )

        return results

    # --------------------------------------------------------

    def print_results(self, query: str):

        """
        Prints retrieved chunks.
        """

        results = self.retrieve(query)

        print("=" * 60)

        print("Retrieved Chunks")

        print("=" * 60)

        for index, document in enumerate(results):

            print(f"\nChunk {index+1}")

            print("-" * 40)

            print(document.page_content[:400])