from app.core.preprocess import TextPreprocessor
from app.core.embeddings import embedding_model
from app.core.vector_store import VectorStore
from app.core.llm_classifier import llm_classifier

from app.config import TOP_K


# --------------------------------------------------
# Load Vector Database Once
# --------------------------------------------------

vector_store = VectorStore()
vector_store.load()


class AcademicClassifier:
    """
    Main orchestration pipeline for
    Academic Doubt Classification.

    Pipeline:

    Question
        ↓
    Preprocessing
        ↓
    Embedding
        ↓
    Semantic Search (FAISS)
        ↓
    LLM Classification
        ↓
    API Response
    """

    @staticmethod
    def classify(question: str):

        # --------------------------------------------------
        # Step 1 : Preserve Original Question
        # --------------------------------------------------

        original_question = question

        # --------------------------------------------------
        # Step 2 : Preprocess Question
        # --------------------------------------------------

        cleaned_question = TextPreprocessor.clean(
            original_question
        )

        # --------------------------------------------------
        # Step 3 : Generate Embedding
        # --------------------------------------------------

        question_embedding = embedding_model.generate(
            cleaned_question
        )

        # --------------------------------------------------
        # Step 4 : Semantic Search
        # --------------------------------------------------

        search_results = vector_store.search(

            query_embedding=question_embedding,

            top_k=TOP_K

        )

        # --------------------------------------------------
        # Step 5 : LLM Classification
        # --------------------------------------------------

        classification = llm_classifier.classify(

            question=original_question,

            retrieved_chunks=search_results

        )

        # --------------------------------------------------
        # Debug Information
        # --------------------------------------------------

        print("\n" + "=" * 80)
        print("Academic Doubt Classification Pipeline")
        print("=" * 80)

        print(f"Original Question : {original_question}")
        print(f"Processed Question: {cleaned_question}")
        print(f"Embedding Shape   : {question_embedding.shape}")

        print("\nTop Retrieved Knowledge Chunks")
        print("-" * 80)

        for index, result in enumerate(search_results, start=1):

            print(f"\nResult #{index}")

            print(f"Subject      : {result['subject']}")
            print(f"Page         : {result['page']}")
            print(f"Distance     : {result['distance']:.4f}")

            preview = result["content"][:200].replace("\n", " ")

            print(f"Preview      : {preview}...")

        print("\nLLM Classification")
        print("-" * 80)

        print(f"Subject       : {classification['subject']}")
        print(f"Topic         : {classification['topic']}")
        print(f"Subtopic      : {classification['subtopic']}")
        print(f"Difficulty    : {classification['difficulty']}")
        print(f"Confidence    : {classification['confidence']:.2f}")

        print("=" * 80)

        # --------------------------------------------------
        # Prepare References
        # --------------------------------------------------

        references = []

        for result in search_results:

            references.append({

                "page": result["page"],

                "distance": round(
                    result["distance"],
                    4
                )

            })

        # --------------------------------------------------
        # Final Response
        # --------------------------------------------------

        return {

            "question": original_question,

            "classification": classification,

            "references": references

        }