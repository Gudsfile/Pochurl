from pochurl.domain import SavedElement


def has_desired_tag(element_tags: set[str], desired_tags: set[str]):
    return len(element_tags & desired_tags) > 0


def select_by_tags(elements: list[SavedElement], desired_tags: set[str]):
    return [element for element in elements if has_desired_tag(element.tags, desired_tags)]


class TestTagsFilter:
    desired_tags = {"tag1", "tag2"}

    def test_one_desired_tag(self):
        """For a tag that is one of the desired tags, the result should be true"""
        assert has_desired_tag({"tag1"}, self.desired_tags) is True

    def test_multiple_desired_tags(self):
        """For two tags that are one of the desired tags, the result should be true"""
        assert has_desired_tag({"tag1", "tag2"}, self.desired_tags) is True

    def test_unwanted_tag(self):
        """For a tag that are not one of the desired tags, the result should be false"""
        assert has_desired_tag({"dummy-tag"}, self.desired_tags) is False

    def test_multiple_tags(self):
        """For two tags, one of which is one of the desired tags, the result should be true"""
        assert has_desired_tag({"tag1", "dummy-tag"}, self.desired_tags) is True

    def test_multiple_tags_another_order(self):
        """For two tags, one of which is one of the desired tags, regardless of its position the result should be true"""
        assert has_desired_tag({"dummy-tag", "tag2"}, self.desired_tags) is True

    def test_no_tag(self):
        """For an empty set of tag, the result should be false"""
        assert has_desired_tag(set(), self.desired_tags) is False

    def test_select(self):
        """For several elements with different tags, only those with the desired tags should be kept"""
        elements = [
            SavedElement(id="id1", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name1", tags=["tag1"]),
            SavedElement(id="id2", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name2", tags=["tag1", "tag2"]),
            SavedElement(id="id3", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name3", tags=["dummy-tag"]),
            SavedElement(id="id3", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name3", tags=["tag1", "dummy-tag"]),
            SavedElement(id="id3", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name3", tags=["dummy-tag", "tag2"]),
            SavedElement(id="id3", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name3", tags=[]),
        ]
        selected_elements = select_by_tags(elements, self.desired_tags)

        expected_elements = [
            SavedElement(id="id1", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name1", tags=["tag1"]),
            SavedElement(id="id2", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name2", tags=["tag1", "tag2"]),
            SavedElement(id="id3", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name3", tags=["tag1", "dummy-tag"]),
            SavedElement(id="id3", timestamp="2020-01-01T00:00:00", url="https://example.py", name="name3", tags=["dummy-tag", "tag2"]),
        ]
        assert selected_elements == expected_elements
