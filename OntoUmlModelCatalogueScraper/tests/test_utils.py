from OntoUmlModelCatalogueScraper.util import recursive_dict_add, recursive_dict_sum

class TestUtils:

    def test_basic_dict_add(self):
        d1 = {"a": 4, "b": 6}
        d2 = {"b": 4, "c": 5}

        result = recursive_dict_add(d1, d2)

        assert result["a"] == 4
        assert result["b"] == 10
        assert result["c"] == 5

    def test_recursive_add(self):
        d1 = {"X": {"a": 1, "b": 3}, "Y": {"a": 4, "b": 8}}
        d2 = {"Z": {"a": 5, "b": 7}, "Y": {"a": 3, "b": 9}}

        result = recursive_dict_add(d1, d2)

        expected_X = {"a": 1, "b": 3}
        assert result["X"] == expected_X
        expected_Y = {"a": 7, "b": 17}
        assert result["Y"] == expected_Y
        expected_Z = {"a": 5, "b": 7}
        assert result["Z"] == expected_Z


    def test_multiple_recursive_add(self):
        d1 = {"X": {"a": 1, "b": 3}, "Y": {"a": 4, "b": 8}}
        d2 = {"Z": {"a": 5, "b": 7}, "Y": {"a": 3, "b": 9}}
        d3 = {"X": {"a": 2, "b": 1}, "Y": {"a": 3, "b": 9}}

        result = recursive_dict_sum(d1, d2, d3)

        expected_X = {"a": 3, "b": 4}
        assert result["X"] == expected_X
        expected_Y = {"a": 10, "b": 26}
        assert result["Y"] == expected_Y
        expected_Z = {"a": 5, "b": 7}
        assert result["Z"] == expected_Z


    def test_different_recursive_levels(self):
        d1 = {"X": 5}
        d2 = {"A": {"X": 7}}

        result = recursive_dict_add(d1, d2)
        result2 = recursive_dict_add(d2, d1)

        expected = {"X": 5, "A": {"X": 7}}
        assert result == expected
        assert result2 == expected