from abc import ABC, abstractmethod
from typing import List

from pydantic import AnyHttpUrl

from pochurl.domain import GivenElement, SavedElement


class Storage(ABC):

    @abstractmethod
    def read_item(self, id: str) -> SavedElement | None:
        pass
    
    @abstractmethod
    def read_items(self) -> List[SavedElement]:
        pass
    
    @abstractmethod
    def read_items_by_name(self, name: str) -> List[SavedElement]:
        pass
    
    @abstractmethod
    def read_items_by_url(self, url: AnyHttpUrl) -> List[SavedElement]:
        pass
    
    @abstractmethod
    def write_item(self, element: GivenElement) -> str:
        pass
    
    @abstractmethod
    def rewrite_item(self, id: str, element: GivenElement) -> str | None:
        pass
