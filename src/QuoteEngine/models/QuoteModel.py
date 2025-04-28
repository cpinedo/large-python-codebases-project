"""QuoteModel."""


class QuoteModel:
    """A class that represents a quote with a body and an author."""

    def __init__(self, body: str, author: str):
        """
        Initialize a new quote with the given body and author.

        Args:
            body (str): The content of the quote.
            author (str): The author of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self) -> str:
        """
        Return a string representation of the quote.

        Returns:
            str: The quote formatted as '"quote" - author'.
        """
        return f'"{self.body}" - {self.author}'
