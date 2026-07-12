import re


class TextPreprocessor:
    """
    Handles text preprocessing before classification.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean and normalize input text.
        """

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(r"[^\w\s]", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text