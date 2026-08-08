"""
loader.py

Loads PDF files and extracts text.
"""

from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:

    def __init__(self):
        pass

    def load_pdf(self, file_path: str):

        """
        Reads a PDF and returns
        LangChain Document objects.
        """

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        return documents

    def get_text(self, file_path: str):

        """
        Reads the PDF and returns
        all text as one string.
        """

        documents = self.load_pdf(file_path)

        full_text = ""

        for document in documents:

            full_text += document.page_content

            full_text += "\n"

        return full_text