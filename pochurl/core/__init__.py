import logging
import sys
from typing import Literal

from pochurl.core.storage import Storage


logger = logging.getLogger(__name__)


def get_db(storage: Literal['firestore', 'tinydb']) -> Storage:
    match storage:
        case 'firestore':
            from pochurl.core.storage_firestore import FireStoreStorage
            return FireStoreStorage()
        case 'tinydb':
            from pochurl.core.storage_tinydb import TinyDbStorage
            return TinyDbStorage()
        case _:
            logger.error('storage %s not impletemend yet', storage)
