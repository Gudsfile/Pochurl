import logging
import sys
from typing import Literal

from pochurl.core.storage import Storage
from pochurl.core.storage_firestore import FireStoreStorage
from pochurl.core.storage_tinydb import TinyDbStorage


logger = logging.getLogger(__name__)


def get_db(storage: Literal['firestore', 'tinydb']) -> Storage:
    match storage:
        case 'firestore':
            return FireStoreStorage()
        case 'tinydb':
            return TinyDbStorage()
        case _:
            logger.error('storage %s not impletemend yet', storage)
