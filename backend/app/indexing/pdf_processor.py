"""
PDF Processor

Reads academic PDF documents and converts them into
structured knowledge chunks for indexing.

Responsibilities
----------------
1. Read PDF files.
2. Extract text page-by-page.
3. Split text into semantic chunks.
4. Attach metadata to every chunk.

This module does NOT:
- generate embeddings
- build the vector database
- perform retrieval
"""

from pathlib import Path

import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class PDFProcessor:
    """
    Processes PDF documents into structured
    knowledge chunks.
    """

    def __init__(self):
        """
        Initialize the text splitter using
        application configuration.
        """

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=CHUNK_SIZE,

            chunk_overlap=CHUNK_OVERLAP,

            separators=[

                "\n\n",

                "\n",

                ". ",

                " ",

                ""

            ]

        )

    # ======================================================
    # Public Method
    # ======================================================

    def process(
        self,
        pdf_path: str | Path
    ) -> list[dict]:
        """
        Process a PDF into structured chunks.

        Parameters
        ----------
        pdf_path : str | Path

        Returns
        -------
        list[dict]
            List of knowledge chunks.
        """

        pdf_path = Path(pdf_path)

        subject = pdf_path.stem.replace("_", " ")

        source = pdf_path.name

        knowledge_chunks = []

        with fitz.open(pdf_path) as document:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                page_text = page.get_text().strip()

                if not page_text:
                    continue

                chunks = self.text_splitter.split_text(
                    page_text
                )

                for chunk in chunks:

                    chunk = chunk.strip()

                    # Skip empty or tiny chunks
                    if len(chunk) < 30:
                        continue

                    knowledge_chunks.append({

                        "subject": subject,

                        "source": source,

                        "page": page_number,

                        "text": chunk,

                        "text_length": len(chunk)

                    })

        return knowledge_chunks


# ======================================================
# Module Test
# ======================================================

if __name__ == "__main__":

    processor = PDFProcessor()

    chunks = processor.process(

        "app/data/pdfs/Big Data.pdf"

    )

    print("=" * 60)

    print(f"Total Chunks : {len(chunks)}")

    print("=" * 60)

    if chunks:

        from pprint import pprint

        pprint(chunks[0])