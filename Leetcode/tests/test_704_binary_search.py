import pytest
from leetcode_704_Binary_Search import Solution

@pytest.fixture(scope="module")
def s():
    return Solution()

@pytest.mark.parametrize(
    "nums,target,expected", # the structure of what each example test case should contain in which sequence
    [
        ([-1,0,3,5,9,12], 9, 4),     # example 1
        ([-1,0,3,5,9,12], 2, -1),    # example 2
        ([5], 5, 0),                 # single element found
        ([5], 3, -1),                # single element not found
        ([1,2,3], 1, 0),             # first element
        ([1,2,3], 3, 2),             # last element
        ([], 1, -1),                 # empty array
        ([1,3,5,7,9], 6, -1),        # gap target
        ([1,3,5,7,9], 8, -1),        # gap target 2
    ],
    ids=[
        "found_9",
        "not_found_2",
        "single_found",
        "single_not_found",
        "first_element",
        "last_element",
        "empty",
        "gap",
        "gap"

    ],
)
def test_search_parametrized(s, nums, target, expected):
    assert s.search(nums, target) == expected


# click the triangle on the left of `def test_search_parametrized` and here are the results on the terminal
"""
============================= test session starts ==============================
collecting ... collected 9 items

tests/test_704_binary_search.py::test_search_parametrized[found_9] PASSED [ 11%]
tests/test_704_binary_search.py::test_search_parametrized[not_found_2] PASSED [ 22%]
tests/test_704_binary_search.py::test_search_parametrized[single_found] PASSED [ 33%]
tests/test_704_binary_search.py::test_search_parametrized[single_not_found] PASSED [ 44%]
tests/test_704_binary_search.py::test_search_parametrized[first_element] PASSED [ 55%]
tests/test_704_binary_search.py::test_search_parametrized[last_element] PASSED [ 66%]
tests/test_704_binary_search.py::test_search_parametrized[empty] PASSED  [ 77%]
tests/test_704_binary_search.py::test_search_parametrized[gap0] PASSED   [ 88%]
tests/test_704_binary_search.py::test_search_parametrized[gap1] PASSED   [100%]

============================== 9 passed in 0.01s ===============================

Process finished with exit code 0
"""