import json
import logging
import re

import ollama

logger = logging.getLogger(__name__)


class LLMClassifier:
    """
    Uses Ollama (Qwen3) to classify an academic doubt.

    Responsibility
    ----------------
    Question
        +
    Retrieved Knowledge Chunks
        ↓
    Ollama (Qwen3)
        ↓
    Structured Classification JSON
    """

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------

    def classify(
        self,
        question: str,
        retrieved_chunks: list
    ) -> dict:

        context = self._build_context(
            retrieved_chunks
        )

        prompt = self._build_prompt(
            question,
            context
        )

        result = self._call_model(prompt)

        result = self._validate_response(result)

        return result

    # --------------------------------------------------
    # Build Context
    # --------------------------------------------------

    def _build_context(
        self,
        retrieved_chunks: list
    ) -> str:

        context = []

        for chunk in retrieved_chunks:

            context.append(
                f"""
====================================================

Subject : {chunk["subject"]}

Page : {chunk["page"]}

Content:

{chunk["content"]}

"""
            )

        return "\n".join(context)

    # --------------------------------------------------
    # Prompt Engineering
    # --------------------------------------------------

    def _build_prompt(
        self,
        question: str,
        context: str
    ) -> str:

        return f"""
You are an Academic Doubt Classification Engine.

Your ONLY responsibility is to classify the student's academic doubt.

IMPORTANT RULES

1. DO NOT answer the student's question.

2. Use ONLY the retrieved academic knowledge.

3. DO NOT use outside knowledge.

4. If the information is missing,
choose the closest matching topic.

5. Difficulty must be exactly one of:

Easy
Medium
Hard

6. Confidence must be between 0.0 and 1.0.

7. Return ONLY valid JSON.

8. DO NOT return:

- Markdown
- Code fences
- Explanations
- Thinking
- Reasoning

--------------------------------------------------------

Student Question

{question}

--------------------------------------------------------

Retrieved Academic Knowledge

{context}

--------------------------------------------------------

Return ONLY this JSON format:

{{
    "subject": "",
    "topic": "",
    "subtopic": "",
    "difficulty": "",
    "confidence": 0.95
}}
"""

    # --------------------------------------------------
    # Ollama Call
    # --------------------------------------------------

    def _call_model(
        self,
        prompt: str
    ) -> dict:

        try:

            response = ollama.chat(

                model="qwen3:8b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an academic classifier. "
                            "Return ONLY valid JSON. "
                            "Do not explain. "
                            "Do not think aloud."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

            )

            text = response["message"]["content"]

            print("\n========== OLLAMA RESPONSE ==========\n")
            print(text)
            print("\n=====================================\n")

            # Remove markdown
            text = text.replace("```json", "")
            text = text.replace("```", "")

            # Remove <think>...</think>
            text = re.sub(
                r"<think>.*?</think>",
                "",
                text,
                flags=re.DOTALL,
            )

            text = text.strip()

            # Extract JSON if extra text exists
            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:
                text = text[start:end + 1]

            return json.loads(text)

        except Exception as e:

            print("\n========== OLLAMA ERROR ==========\n")
            print(e)
            print("\n==================================\n")

            logger.exception(e)

            return {}

    # --------------------------------------------------
    # Validate Response
    # --------------------------------------------------

    def _validate_response(
        self,
        result: dict
    ) -> dict:

        default = {

            "subject": "Unknown",

            "topic": "Unknown",

            "subtopic": "Unknown",

            "difficulty": "Unknown",

            "confidence": 0.0

        }

        if not isinstance(result, dict):

            return default

        for key, value in default.items():

            result.setdefault(key, value)

        try:

            result["confidence"] = float(result["confidence"])

        except Exception:

            result["confidence"] = 0.0

        return result


# --------------------------------------------------
# Singleton
# --------------------------------------------------

llm_classifier = LLMClassifier()


# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":

    sample_chunks = [

        {

            "subject": "Big Data",

            "page": 36,

            "content": """
MapReduce is the programming model
used by Hadoop.
Mapper and Reducer are the two
major phases.
"""

        }

    ]

    result = llm_classifier.classify(

        question="What is MapReduce?",

        retrieved_chunks=sample_chunks

    )

    print("\nClassification Result\n")

    print(json.dumps(result, indent=4))