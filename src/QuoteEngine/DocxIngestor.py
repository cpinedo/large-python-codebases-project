"""DOCXIngestor."""
import docx
from typing import List

from src.QuoteEngine.ingestor_interface import IngestionInterface
from src.QuoteEngine.models.QuoteModel import QuoteModel


class DocxIngestor(IngestionInterface):
    """Ingestor for .docx files that extracts quotes into QuoteModel instances."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a DOCX file and return a list of QuoteModel instances.

        Each paragraph is expected to follow the format:
            "quote body" - author

        Args:
            path (str): Path to the DOCX file.

        Returns:
            List[QuoteModel]: A list of quotes parsed from the file.

        Raises:
            ValueError: If the file format is unsupported or line format
                is invalid.
            FileNotFoundError: If the file does not exist.
            Exception: For general read or parsing issues.
        """
        if not cls.can_ingest(path):
            raise ValueError(
                f"Cannot ingest file with unsupported extension: {path}"
            )

        quotes = []
        try:
            doc = docx.Document(path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to load DOCX file: {path}") from e

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                try:
                    body, author = text.split(" - ")
                    quote = QuoteModel(body.strip('" '), author.strip())
                    quotes.append(quote)
                except ValueError:
                    raise ValueError(
                        f"Invalid line format in DOCX file: '{text}'"
                    )

        return quotes
