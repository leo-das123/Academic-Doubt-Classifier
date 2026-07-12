import fitz
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class PDFProcessor:
    """
    Reads a PDF and converts it into structured knowledge chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=CHUNK_SIZE,

            chunk_overlap=CHUNK_OVERLAP

        )

    # ------------------------------------
    # Public Method
    # ------------------------------------

    def process(self, pdf_path: str):

        pdf_path = Path(pdf_path)

        subject = pdf_path.stem.replace("_", " ")
        source_file = pdf_path.name

        document = fitz.open(pdf_path)

        knowledge_chunks = []

        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text()

            if not page_text.strip():
                continue

            page_chunks = self.text_splitter.split_text(page_text)

            for index, chunk in enumerate(page_chunks, start=1):

                knowledge_chunks.append({

                    "chunk_id": f"{subject}_{page_number}_{index}",

                    "subject": subject,

                    "source_file": source_file,

                    "page": page_number,

                    "content": chunk,

                    "content_length": len(chunk)

                })

        document.close()

        return knowledge_chunks


if __name__ == "__main__":

    processor = PDFProcessor()

    chunks = processor.process("app/data/pdfs/Big Data.pdf")

    print(f"Total Chunks : {len(chunks)}")

    print("-" * 60)

    print(chunks[100])