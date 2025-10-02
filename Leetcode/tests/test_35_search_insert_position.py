import pytest
from leetcode_35_Search_Insert_Position import Solution

@pytest.fixture(scope="module")
def s():
    return Solution() # have to return, otherwise s would be NoneType

@pytest.mark.parametrize(
    "nums, target, expected",
    [
        ([1,3,5,6], 5, 2), # target exists in the list, list length is an even number
        ([1,3,5,7,9], 1, 0), # target exists in the list, list length is an even number
        ([5], 5, 0), # target exists in the list, list length is 1
        ([], 30, 0), # target doesn't exist in the list, the list is empty
        ([1,2,3,4], 7, 4), # target doesn't exist in the list, list length is an even number, target is larger than the max
        ([1,2,3,4], -1, 0), # target doesn't exist in the list, list length is an even number, target is smaller than the min
        ([1,2,3,5], 4, 3), # target doesn't exist in the list, list length is an even number, target is within the range
        ([1,2,3,4,5], 7, 5), # target doesn't exist in the list, list length is an odd number, target is larger than the max
        ([1,2,3,4,7], -1, 0), # target doesn't exist in the list, list length is an odd number, target is smaller than the min
        ([1,2,3,5,9], 6, 4), # target doesn't exist in the list, list length is an odd number, target is within the range

    ],
    ids = [
        "found_5",
        "found_1",
        "single_found",
        "single_not_found_insert",
        "even_insert_last_element",
        "even_insert_first_element",
        "even_insert_middle",
        "odd_insert_last_element",
        "odd_insert_first_element",
        "odd_insert_middle",
    ]
    )

def test_search_insert_position(s, nums, target, expected):
    assert s.searchInsert(nums, target) == expected