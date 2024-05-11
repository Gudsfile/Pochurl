from pochurl.domain import GivenElement


def csv_to_dicts(csv_content: str) -> list:
    columns = ["url", "name", "tags"]
    return [
        dict(((k, {v.strip()}) if k == "tags" else (k, v.strip()) for k, v in zip(columns, line.split(",")))) for line in csv_content.split("\n") if line != ""
    ]


def dict_to_elements(dict_content: dict) -> list[GivenElement]:
    return []
