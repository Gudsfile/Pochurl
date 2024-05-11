import json
import logging
from datetime import datetime
from typing import List

from pydantic import AnyHttpUrl
from tinydb import Query, TinyDB
from tinydb.table import Document

from pochurl.core.storage import Storage, log
from pochurl.domain import GivenElement, SavedElement


logger = logging.getLogger(__name__)


class TinyDbStorage(Storage):
    db = TinyDB("pochurl-tinydb.json")

    @log(logger=logger)
    def read_item(self, element_id: str) -> SavedElement | None:
        previous = self.db.get(doc_id=element_id)
        return SavedElement(id=element_id, **dict(previous)) if previous else None

    @log(logger=logger)
    def read_items(self) -> List[SavedElement]:
        previous = self.db.all()
        return [SavedElement(id=str(p.doc_id), **dict(p)) for p in previous] if previous else []

    @log(logger=logger)
    def read_items_by_name(self, name: str) -> List[SavedElement]:
        condition = Query().name.test(_test_str_contains, name)
        previous = self.db.search(condition)
        return [SavedElement(id=str(p.doc_id), **dict(p)) for p in previous] if previous else []

    @log(logger=logger)
    def read_items_by_url(self, url: AnyHttpUrl) -> List[SavedElement]:
        condition = Query().url.test(_test_str_contains, str(url))
        previous = self.db.search(condition)
        return [SavedElement(id=str(p.doc_id), **dict(p)) for p in previous] if previous else []

    @log(logger=logger)
    def write_item(self, element: GivenElement) -> str:
        element_id = self.db.insert(json.loads(element.json()) | {"timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")})
        return str(element_id)

    @log(logger=logger)
    def rewrite_item(self, element_id: str, element: GivenElement) -> str | None:
        previous = self.read_item(element_id)
        if previous:
            self.db.upsert(Document(json.loads(element.json()), doc_id=int(element_id)))
            return element_id
        logger.warning("no id=%s yet", element_id)
        return None


def _test_str_contains(val, string):
    return string.lower() in val.lower()
