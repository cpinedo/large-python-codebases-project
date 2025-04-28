"""Ingestor Interface."""

from abc import ABC, abstractmethod
from typing import List

from src.QuoteEngine.models.QuoteModel import QuoteModel


class IngestionInterface(ABC):
    """
    Abstract base class for file ingestion.

    This class defines the interface that all concrete ingestor classes must implement.
    It provides a common structure for ingesting different types of files and converting
    their contents into QuoteModel objects.

    Attributes:
        allowed_extensions (list): List of file extensions that can be processed by the ingestor.
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path):
        """Determine if the file can or cannot be ingested."""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the provided file into a List of QuoteModel."""
        pass
