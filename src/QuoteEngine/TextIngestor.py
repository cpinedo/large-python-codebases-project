"""TextIngestor."""

import csv
from typing import List

from src.QuoteEngine.ingestor_interface import IngestionInterface
from src.QuoteEngine.models.QuoteModel import QuoteModel


class TextIngestor(IngestionInterface):
    """
    Ingestor for plain text (.txt) files that contain quotes in the format.

    "quote body" - author
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a TXT file into a list of QuoteModel instances.

        Args:
            path (str): Path to the TXT file.

        Returns:
            List[QuoteModel]: A list of parsed quotes.

        Raises:
            ValueError: If the file cannot be ingested or a
            line is improperly formatted.
            FileNotFoundError: If the TXT file does not exist.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest unsupported file: {path}")

        quotes = []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                for line in file:
                    text = line.strip()
                    if not text:
                        continue
                    try:
                        body, author = text.split(" - ")
                        quotes.append(
                            QuoteModel(body.strip('" '), author.strip())
                        )
                    except ValueError:
                        raise ValueError(
                            f"Invalid line format in TXT file: '{text}'"
                        )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"TXT file not found: {path}") from e

        return quotes
