"""CSVIngestor."""

import pandas as pd
from typing import List

from src.QuoteEngine.ingestor_interface import IngestionInterface
from src.QuoteEngine.models.QuoteModel import QuoteModel


class CSVIngestor(IngestionInterface):
    """
    Ingestor for CSV files.

    extracts quotes and authors into QuoteModel instances.
    """

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a CSV file and return a list of QuoteModel instances.

        Args:
            path (str): Path to the CSV file.

        Returns:
            List[QuoteModel]: A list of quotes parsed from the file.

        Raises:
            ValueError: If the file extension is not supported.
            FileNotFoundError: If the file cannot be found.
            pd.errors.ParserError: If there is a parsing error.
            KeyError: If required columns are missing.
        """
        if not cls.can_ingest(path):
            raise ValueError(
                f"Cannot ingest file with unsupported extension: {path}"
            )

        try:
            df = pd.read_csv(path, encoding='utf-8')
            quotes = [
                QuoteModel(row['body'], row['author'])
                for _, row in df.iterrows()
            ]
            return quotes

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {path}") from e

        except pd.errors.ParserError as e:
            raise ValueError(f"Failed to parse CSV file: {path}") from e

        except KeyError as e:
            raise KeyError(f"Missing required columns in CSV file: {e}") from e
