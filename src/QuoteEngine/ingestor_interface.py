from abc import ABC, abstractmethod
from typing import List

from src.QuoteEngine.models.QuoteModel import QuoteModel


class IngestionInterface(ABC):

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path):
        """Determines if the file can or cannot be ingested"""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parses the provided file into a List of QuoteModel"""
        pass
