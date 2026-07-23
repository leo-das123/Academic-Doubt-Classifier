"""
Knowledge Base Builder

Builds the complete semantic knowledge base
used by the Academic Doubt Classifier.

Pipeline
--------
Academic PDFs
        ↓
PDF Processing
        ↓
Knowledge Chunks
        ↓
Embedding Generation
        ↓
FAISS Index Creation
        ↓
Save Vector Database

Run

python -m app.indexing.build_index
"""

from pathlib import Path
import logging

from app.config import (
    PDF_DIRECTORY,
    VECTOR_DB_PATH
)

from app.indexing.pdf_processor import PDFProcessor
from app.core.embeddings import EmbeddingService
from app.core.vector_store import VectorStore

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger(__name__)


class IndexBuilder:
    """
    Offline Knowledge Base Builder.
    """

    def __init__(self):

        self.pdf_directory = Path(PDF_DIRECTORY)

        self.processor = PDFProcessor()

        self.vector_store = VectorStore()

    # =====================================================
    # Public Method
    # =====================================================

    def build(self):

        logger.info("=" * 70)
        logger.info("Building Academic Knowledge Base")
        logger.info("=" * 70)

        pdf_files = self._load_pdfs()

        chunks = self._process_pdfs(pdf_files)

        embeddings = self._generate_embeddings(chunks)

        self._build_vector_database(
            embeddings,
            chunks
        )

        self._print_summary(
            pdf_files,
            chunks,
            embeddings
        )

        logger.info("\nKnowledge Base Ready Successfully.\n")

    # =====================================================
    # Load PDFs
    # =====================================================

    def _load_pdfs(self):

        if not self.pdf_directory.exists():

            raise FileNotFoundError(

                f"PDF directory not found: {self.pdf_directory}"

            )

        pdf_files = sorted(

            self.pdf_directory.glob("*.pdf")

        )

        if not pdf_files:

            raise FileNotFoundError(

                "No PDF files found."

            )

        logger.info(

            "Found %d PDF(s).\n",

            len(pdf_files)

        )

        return pdf_files

    # =====================================================
    # Process PDFs
    # =====================================================

    def _process_pdfs(

        self,

        pdf_files

    ):

        all_chunks = []

        chunk_id = 0

        for pdf in pdf_files:

            logger.info("-" * 70)

            logger.info(

                "Processing %s",

                pdf.name

            )

            chunks = self.processor.process(pdf)

            for chunk in chunks:

                chunk["id"] = chunk_id

                chunk_id += 1

            logger.info(

                "Chunks Created : %d",

                len(chunks)

            )

            all_chunks.extend(chunks)

        logger.info("-" * 70)

        logger.info(

            "Total Chunks : %d\n",

            len(all_chunks)

        )

        return all_chunks

    # =====================================================
    # Generate Embeddings
    # =====================================================

    def _generate_embeddings(

        self,

        chunks

    ):

        logger.info("=" * 70)

        logger.info("Generating Embeddings")

        logger.info("=" * 70)

        texts = [

            chunk["text"]

            for chunk in chunks

        ]

        embeddings = EmbeddingService.generate_batch(

            texts

        )

        logger.info(

            "Generated %d embeddings.\n",

            len(embeddings)

        )

        return embeddings

    # =====================================================
    # Build Vector Database
    # =====================================================

    def _build_vector_database(

        self,

        embeddings,

        metadata

    ):

        logger.info("=" * 70)

        logger.info("Building FAISS Index")

        logger.info("=" * 70)

        self.vector_store.create_index(

            embeddings,

            metadata

        )

        self.vector_store.save()

        logger.info(

            "Vector database saved to:\n%s\n",

            VECTOR_DB_PATH

        )

    # =====================================================
    # Summary
    # =====================================================

    def _print_summary(

        self,

        pdf_files,

        chunks,

        embeddings

    ):

        subjects = sorted({

            chunk["subject"]

            for chunk in chunks

        })

        logger.info("=" * 70)

        logger.info("Knowledge Base Summary")

        logger.info("=" * 70)

        logger.info(

            "PDFs Indexed       : %d",

            len(pdf_files)

        )

        logger.info(

            "Subjects           : %d",

            len(subjects)

        )

        logger.info(

            "Knowledge Chunks   : %d",

            len(chunks)

        )

        logger.info(

            "Embeddings         : %d",

            len(embeddings)

        )

        if len(embeddings):

            logger.info(

                "Vector Dimension   : %d",

                len(embeddings[0])

            )

        logger.info(

            "Vector Database    : %s",

            VECTOR_DB_PATH

        )

        logger.info(

            "Subjects Indexed   : %s",

            ", ".join(subjects)

        )

        logger.info("=" * 70)


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    builder = IndexBuilder()

    builder.build()