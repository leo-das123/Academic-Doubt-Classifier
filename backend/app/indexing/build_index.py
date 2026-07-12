from pathlib import Path

from app.indexing.pdf_processor import PDFProcessor
from app.core.embeddings import embedding_model
from app.core.vector_store import VectorStore


class IndexBuilder:
    """
    Builds the complete Academic Knowledge Base.

    Pipeline

    Academic PDFs
            │
            ▼
      PDF Processing
            │
            ▼
         Chunking
            │
            ▼
      Metadata Creation
            │
            ▼
     Embedding Generation
            │
            ▼
       FAISS Index Build
            │
            ▼
      Save Vector Database
    """

    def __init__(self):

        self.pdf_folder = Path("app/data/pdfs")

        self.pdf_processor = PDFProcessor()

        self.vector_store = VectorStore()

    # ==================================================
    # Public Method
    # ==================================================

    def build(self):

        pdf_files = self._load_pdfs()

        knowledge_chunks = self._process_pdfs(pdf_files)

        embeddings = self._generate_embeddings(
            knowledge_chunks
        )

        self._build_vector_database(
            embeddings,
            knowledge_chunks
        )

        self._print_summary(
            pdf_files,
            knowledge_chunks,
            embeddings
        )

        return knowledge_chunks, embeddings

    # ==================================================
    # Load PDFs
    # ==================================================

    def _load_pdfs(self):

        pdf_files = sorted(
            self.pdf_folder.glob("*.pdf")
        )

        print("\n" + "=" * 70)
        print("Loading Academic PDFs...")
        print("=" * 70)

        print(f"Found {len(pdf_files)} PDF(s)\n")

        return pdf_files

    # ==================================================
    # Process PDFs
    # ==================================================

    def _process_pdfs(self, pdf_files):

        all_chunks = []

        chunk_id = 0

        for pdf in pdf_files:

            subject = pdf.stem.replace("_", " ")

            print("-" * 70)
            print(f"Processing PDF : {pdf.name}")
            print(f"Subject        : {subject}")
            print("-" * 70)

            chunks = self.pdf_processor.process(pdf)

            for chunk in chunks:

                chunk["id"] = chunk_id

                chunk["subject"] = subject

                chunk["source_file"] = pdf.name

                chunk["chunk_length"] = len(
                    chunk["content"]
                )

                chunk_id += 1

            print(f"Chunks Created : {len(chunks)}\n")

            all_chunks.extend(chunks)

        return all_chunks

    # ==================================================
    # Generate Embeddings
    # ==================================================

    def _generate_embeddings(
        self,
        knowledge_chunks
    ):

        print("=" * 70)
        print("Generating Embeddings...")
        print("=" * 70)

        embeddings = []

        total = len(knowledge_chunks)

        for index, chunk in enumerate(
            knowledge_chunks,
            start=1
        ):

            embedding = embedding_model.generate(
                chunk["content"]
            )

            embeddings.append(embedding)

            if index % 100 == 0 or index == total:

                print(
                    f"Processed {index}/{total} chunks"
                )

        print("\nEmbedding Generation Completed.\n")

        return embeddings

    # ==================================================
    # Build Vector Database
    # ==================================================

    def _build_vector_database(
        self,
        embeddings,
        metadata
    ):

        print("=" * 70)
        print("Building Vector Database...")
        print("=" * 70)

        self.vector_store.create_index(

            embeddings=embeddings,

            metadata=metadata

        )

        self.vector_store.save()

        print("Vector Database Saved Successfully.\n")

    # ==================================================
    # Print Summary
    # ==================================================

    def _print_summary(
        self,
        pdf_files,
        knowledge_chunks,
        embeddings
    ):

        subjects = sorted({

            chunk["subject"]

            for chunk in knowledge_chunks

        })

        print("=" * 70)
        print("Knowledge Base Summary")
        print("=" * 70)

        print(f"PDFs Indexed        : {len(pdf_files)}")
        print(f"Subjects            : {len(subjects)}")
        print(f"Chunks Created      : {len(knowledge_chunks)}")
        print(f"Embeddings Created  : {len(embeddings)}")

        if embeddings:

            print(
                f"Vector Dimension    : {len(embeddings[0])}"
            )

        print(
            f"Knowledge Subjects  : {', '.join(subjects)}"
        )

        print("=" * 70)

        print("\nKnowledge Base Ready Successfully.\n")


# ==================================================
# Testing
# ==================================================

if __name__ == "__main__":

    builder = IndexBuilder()

    builder.build()