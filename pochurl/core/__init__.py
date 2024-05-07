import sys

STORAGE = 'FIRESTORE'

match STORAGE:
    case 'FIRESTORE':
        from pochurl.core.storage_firestore import read_item, read_items, read_items_by_name, read_items_by_url, rewrite_item, write_item
    case 'TINYDB':
        from pochurl.core.storage_tinydb import read_item, read_items, read_items_by_name, read_items_by_url, rewrite_item, write_item
    case _:
        print(f'storage {STORAGE} not impletemend yet')
        sys.exit(1)
