import csv

from pochurl.domain import GivenElement


def csv_to_dicts(csv_content: str) -> list:
    return list(csv.DictReader(csv_content.strip().split("\n"), skipinitialspace=True, fieldnames=["url", "name", "tags"]))


def dict_to_elements(dict_content: dict) -> list[GivenElement]:
    return []
