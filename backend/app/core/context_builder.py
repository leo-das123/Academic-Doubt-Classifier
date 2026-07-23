"""
Context Builder

Builds a structured prompt for the LLM using
retrieved knowledge chunks.

Responsibilities
----------------
1. Combine retrieved chunks.
2. Respect maximum context length.
3. Build a consistent prompt.
4. Preserve source information.

This module does NOT perform retrieval,
classification, or confidence scoring.
"""

from app.config import MAX_CONTEXT_CHARACTERS


class ContextBuilder:
    """
    Builds the context passed to the LLM.
    """

    @staticmethod
    def build(chunks):
        """
        Build a formatted context string from retrieved chunks.

        Parameters
        ----------
        chunks : list
            Retrieved chunks from the retriever.

        Returns
        -------
        str
            Context string for the LLM.
        """

        if not chunks:
            return ""

        context_parts = []

        current_length = 0

        for index, chunk in enumerate(chunks, start=1):

            text = chunk["text"].strip()

            section = (
                f"[Chunk {index}]\n"
                f"Source : {chunk['source']}\n"
                f"Page   : {chunk['page']}\n"
                f"Content:\n"
                f"{text}\n"
            )

            if current_length + len(section) > MAX_CONTEXT_CHARACTERS:
                break

            context_parts.append(section)

            current_length += len(section)

        return "\n".join(context_parts)

    # ======================================================
    # Prompt Builder
    # ======================================================

    @staticmethod
    def build_prompt(question, context):
        """
        Build the final prompt for the LLM.

        Parameters
        ----------
        question : str
            Student question.

        context : str
            Retrieved academic context.

        Returns
        -------
        str
            Complete LLM prompt.
        """

        return f"""
You are an academic classification assistant.

Your task is ONLY to classify the student's question.

Use ONLY the provided academic context.

If the context is insufficient, classify conservatively.

Return ONLY valid JSON.

Context
-------
{context}

Student Question
----------------
{question}

Return JSON in exactly this format:

{{
    "subject": "...",
    "topic": "...",
    "subtopic": "...",
    "difficulty": "Easy | Medium | Hard"
}}
""".strip()


# ======================================================
# Module Test
# ======================================================

if __name__ == "__main__":

    print("=" * 60)
    print("ContextBuilder Module Ready")
    print("=" * 60)