import csv
import logging

from pydantic import ValidationError

from pochurl.domain import GivenElement

logger = logging.getLogger(__name__)


def csv_to_dicts(csv_content: str) -> list:
    return list(csv.DictReader(csv_content.strip().split("\n"), skipinitialspace=True, fieldnames=["url", "name", "tags"]))


def dict_to_elements(dict_content: dict) -> (list[GivenElement], list[dict]):
    elements = []
    errors = []
    for element in dict_content:
        try:
            element["tags"] = element["tags"].split(",") if element["tags"] else []
            elements.append(GivenElement(**element))
        except ValidationError as err:
            logger.warning(err)
            logger.warning("element does not conform the model : %s", element)
            errors.append(element)
    return elements, errors
