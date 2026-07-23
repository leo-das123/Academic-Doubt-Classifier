"""
Text Preprocessing

Provides utilities for cleaning and normalizing
student questions before semantic embedding and
retrieval.

This module intentionally performs only lightweight
normalization to preserve the semantic meaning of
the original question.
"""

import re


class TextPreprocessor:
    """
    Handles text preprocessing for academic questions.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean and normalize an input question.

        Steps:
        1. Convert to lowercase.
        2. Remove punctuation.
        3. Normalize whitespace.

        Parameters
        ----------
        text : str
            Raw student question.

        Returns
        -------
        str
            Cleaned question.
        """

        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation while preserving letters,
        # numbers, and whitespace.
        text = re.sub(r"[^\w\s]", "", text)

        # Normalize multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()