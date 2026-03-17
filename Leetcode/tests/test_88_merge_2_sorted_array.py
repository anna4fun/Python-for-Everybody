import pytest
from leetcode_88_merge_2_sorted_arrays import Solution

@pytest.fixture(scope="module")
def s():
    return Solution() # have to return, otherwise s would be NoneType


@pytest.mark.parametrize(
    "nums1, m, nums2, n, expected",  # the structure of what each example test case should contain in which sequence
    [
        ([1,2,3, 0, 0, 0, 0], 3, [2,3,5,6], 4, [1,2,2,3, 3,5,6]),  # example 1
        ([1, 2, 3, 0, 0, 0, 0, 0], 3, [4, 5, 6, 7, 8], 5, [1, 2, 3, 4, 5, 6, 7, 8] ), # nums2 all bigger than nums1
        ([10, 12, 13, 0, 0, 0, 0, 0], 3, [4, 5, 6, 7, 8], 5, [4, 5, 6, 7, 8, 10, 12, 13])  # nums1 all bigger than nums2

    ],
    ids=[
        "mix",
        "nums2 all bigger than nums1 failure",
        "nums1 all bigger than nums2 failure",

    ],
)

# s is a fixture function, but you’re calling it like a global variable. 
# In pytest, you must request the fixture by adding it to the test’s parameters. 
# Otherwise s is the fixture definition object, which has no .merge.
def test_match(s, nums1, m, nums2, n, expected):
    s.merge(nums1 = nums1, m= m, nums2=nums2, n=n)
    assert nums1 == expected  # add assertion here

# 重点总结
# 1. in-place change, 需要从后往前写，要3个pointer, P1,P2, P3 point to the current right-most position to be compared and filled for L1, L2, L3.
# 2. 想清楚极端结束条件，即如果nums1都比nums2大或者小会怎么样