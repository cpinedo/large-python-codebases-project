from typing import List
import subprocess
import os
import random

from src.QuoteEngine.ingestor_interface import IngestionInterface
from src.QuoteEngine.models.QuoteModel import QuoteModel


class PDFIngestor(IngestionInterface):
    """
    Ingestor for PDF files using the external `pdftotext` utility.
    Converts PDF to text and parses quotes.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a PDF file into a list of QuoteModel instances.

        Each line is expected to follow the format:
            "quote body" - author

        Args:
            path (str): Path to the PDF file.

        Returns:
            List[QuoteModel]: A list of parsed quotes.

        Raises:
            ValueError: If the file cannot be ingested or a line is improperly formatted.
            RuntimeError: If `pdftotext` fails.
            FileNotFoundError: If the PDF file is not found.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest unsupported file: {path}")

        try:
            os.makedirs('./tmp', exist_ok=True)
            tmp = f'./tmp/{random.randint(0, 1_000_000)}.txt'

            result = subprocess.call(['pdftotext', '-layout', path, tmp])
            if result != 0 or not os.path.exists(tmp):
                raise RuntimeError(f"pdftotext failed or did not create output file: {tmp}")

            quotes = []
            with open(tmp, 'r', encoding='utf-8') as file_ref:
                for line in file_ref:
                    line = line.strip()
                    if line:
                        try:
                            body, author = line.split(' - ')
                            quotes.append(QuoteModel(body.strip('" '), author.strip()))
                        except ValueError:
                            raise ValueError(f"Invalid line format in PDF text: '{line}'")

            return quotes

        except FileNotFoundError as e:
            raise FileNotFoundError(f"PDF file not found: {path}") from e

        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
