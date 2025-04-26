from typing import List
from src.QuoteEngine.CSVIngestor import CSVIngestor
from src.QuoteEngine.DocxIngestor import DocxIngestor
from src.QuoteEngine.ingestor_interface import IngestionInterface
from src.QuoteEngine.models.QuoteModel import QuoteModel
from src.QuoteEngine.PDFIngestor import PDFIngestor
from src.QuoteEngine.TextIngestor import TextIngestor


class Ingestor(IngestionInterface):
    """
    A generic Ingestor that selects the appropriate ingestor (CSV, DOCX, PDF, or TXT)
    based on the file extension and returns a list of QuoteModel instances.
    """

    importers = [DocxIngestor, CSVIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a file into a list of QuoteModel instances, based on its format (CSV, DOCX, PDF, or TXT).

        Args:
            path (str): The file path to the file to be ingested.

        Returns:
            List[QuoteModel]: A list of parsed quotes.

        Raises:
            ValueError: If no valid ingestor is found for the file.
        """
        for importer in cls.importers:
            if importer.can_ingest(path):
                return importer.parse(path)

        raise ValueError(f"No ingestor available for the file format: {path}")
