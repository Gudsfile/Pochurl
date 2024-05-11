from unittest.mock import MagicMock

import pytest
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient

from pochurl.core import get_db
from pochurl.domain import SavedElement
from pochurl.main import app


client = TestClient(app)
mock_db = MagicMock()

empty = []
one_element = [
    SavedElement(id='id', name='name', url='http://example.py', timestamp='2020-01-01T00:00:00')
]
many_elements = [
    SavedElement(id='id1', name='name1', url='http://example1.py', timestamp='2020-01-01T01:01:01'),
    SavedElement(id='id2', name='name1', url='http://example1.py', timestamp='2021-01-01T01:01:01'),
]
expected_from_one_element = list(map(lambda x: x.model_dump(mode='json'), one_element))
expected_from_many_elements = list(map(lambda x: x.model_dump(mode='json'), many_elements))


def test_get_item_no_result():
    """
    For an empty storage, /api/element/{id} should return None
    """
    mock_db.read_item = MagicMock(return_value=None)
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/api/element/dummy-id')
    assert response.status_code == 200
    assert response.json() is None

def test_get_item_one_result():
    """
    For a non empty storage, /api/element/{id} should return the url concerned
    """
    mock_db.read_item = MagicMock(return_value=one_element[0])
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/api/element/dummy-id')
    assert response.status_code == 200
    assert response.json() == expected_from_one_element[0]

def test_get_item_multiple_results():
    """
    /api/element/{id} should raise an error if many element are returned
    """
    mock_db.read_item = MagicMock(return_value=many_elements)
    app.dependency_overrides[get_db] = lambda: mock_db
    with pytest.raises(ResponseValidationError) as err:
        client.get('/api/element/dummy-id')

def test_get_items_by_url_no_result():
    """
    For an empty storage, /api/elements/url/ should return an empty list
    """
    mock_db.read_items_by_url = MagicMock(return_value=empty)
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/api/elements/url/', params={'url': 'http://dummy.param'})
    assert response.status_code == 200
    assert response.json() == []

def test_get_items_by_url_one_result():
    """
    For a non empty storage, /api/elements/url/ should return the url concerned
    """
    mock_db.read_items_by_url = MagicMock(return_value=one_element)
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/api/elements/url/', params={'url': 'http://dummy.param'})
    assert response.status_code == 200
    assert response.json() == expected_from_one_element

def test_get_items_by_url_multiple_results():
    """
    For a non empty storage, /api/elements/url/ should return all the url concerned
    """
    mock_db.read_items_by_url = MagicMock(return_value=many_elements)
    app.dependency_overrides[get_db] = lambda: mock_db
    response = client.get('/api/elements/url/', params={'url': 'http://dummy.param'})
    assert response.status_code == 200
    assert response.json() == expected_from_many_elements
