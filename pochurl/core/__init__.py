import sys

STORAGE = 'FIRESTORE'

match STORAGE:
    case 'FIRESTORE':
        from pochurl.core.storage_firestore import read_item_by_url, read_items_by_name, read_items, write_item
    case 'TINYDB':
        from pochurl.core.storage_tinydb import read_item_by_url, read_items_by_name, read_items, write_item
    case _:
        print(f'storage {STORAGE} not impletemend yet')
        sys.exit(1)
