from pochurl.domain import GivenElement
from pochurl.importer import csv_to_dicts, dict_to_elements

intermediate_several_items = [
    {"url": "https://example1.py", "name": "name1", "tags": "test"},
    {"url": "https://example2.py", "name": "name2", "tags": "test"},
    {"url": "https://example3.py", "name": "name3", "tags": "python"},
]

intermediate_special_items = [
    {"url": "https://example1.py", "name": "without_tag", "tags": ""},
    {"url": "https://example2.py", "name": "with space", "tags": "with space"},
    {"url": "https://example3.py", "name": "with_several_tags", "tags": "one_tag,two_tag"},
]

intermediate_items_with_error = [
    {"url": "https://example1.py", "name": "name1", "tags": "test"},
    {"url": "not_an_url", "name": "name2", "tags": "test"},
    {"url": "https://example3.py", "name": "name3", "tags": "python"},
]


def test_parse_several_items_intermediate():
    given = """
https://example1.py,name1,test
https://example2.py,name2,test
https://example3.py,name3,python
"""
    assert csv_to_dicts(given) == intermediate_several_items


def test_parse_several_items_final():
    result, rejected = dict_to_elements(intermediate_several_items)
    expected = [
        GivenElement(url="https://example1.py", name="name1", tags={"test"}),
        GivenElement(url="https://example2.py", name="name2", tags={"test"}),
        GivenElement(url="https://example3.py", name="name3", tags={"python"}),
    ]
    assert result == expected
    assert not rejected


def test_parse_special_items_intermediate():
    given = """
"https://example1.py","without_tag",
"https://example2.py","with space", "with space"
"https://example3.py","with_several_tags","one_tag,two_tag"
"""
    assert csv_to_dicts(given) == intermediate_special_items


def test_parse_special_items_final():
    result, rejected = dict_to_elements(intermediate_special_items)
    expected = [
        GivenElement(url="https://example1.py", name="without_tag", tags=set()),
        GivenElement(url="https://example2.py", name="with space", tags={"with space"}),
        GivenElement(url="https://example3.py", name="with_several_tags", tags={"one_tag", "two_tag"}),
    ]
    assert result == expected
    assert not rejected


def test_parse_items_with_error_intermediate():
    given = """
"https://example1.py","name1","test"
"not_an_url","name2", "test"
"https://example3.py","name3", "python"
"""
    assert csv_to_dicts(given) == intermediate_items_with_error


def test_parse_items_with_error_final():
    result, rejected = dict_to_elements(intermediate_items_with_error)
    expected = [
        GivenElement(url="https://example1.py", name="name1", tags={"test"}),
        GivenElement(url="https://example3.py", name="name3", tags={"python"}),
    ]
    assert result == expected
    assert rejected == [intermediate_items_with_error[1]]


def test_parse_zero_item():
    given = "\n"
    intermediate = []
    assert csv_to_dicts(given) == intermediate
    assert dict_to_elements(intermediate) == ([], [])
