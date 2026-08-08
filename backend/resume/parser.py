"""
parser.py

Extracts text from uploaded resume PDFs.
"""

from langchain_community.document_loaders import PyPDFLoader


class ResumeParser:
    """
    Extracts text from a resume PDF.
    """

    def extract_text(self, pdf_path: str) -> str:

        loader = PyPDFLoader(pdf_path)

        pages = loader.load()

        resume_text = ""

        for page in pages:

            resume_text += page.page_content

            resume_text += "\n"

        return resume_text