"""
35. Search Insert Position
Solved
Easy

Given a sorted array of distinct integers and a target value, return the index if the target is found.
If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [1,3,5,6], target = 5
Output: 2

Example 2:
Input: nums = [1,3,5,6,7], target = 2
Output: 1
(in while loop)
[1,3] left = 0, right = 1, middle = 0
nums[middle] = nums[0] = 1 < target, left = middle+1 = 1 = right
(in while loop)
[3] left = 1, right = 1, middle = 1
nums[middle] = nums[1] = 3 > target, right = middle-1 = 0 = left -1
(out of while loop)
return middle


Example 3:
Input: nums = [1,3,5,6], target = 7
Output: 4

Constraints:

1 <= nums.length <= 104
-104 <= nums[i] <= 104
nums contains distinct values sorted in ascending order.
-104 <= target <= 104
"""
from typing import List

class Solution():
    def searchInsert(self, nums: List[int], target: int) -> int:
        # if nums is empty, just insert the target
        if len(nums) == 0:
            return 0

        left = 0
        right = len(nums) - 1

        while left <= right:
            # use floor division to stabelize the middle to be middle left(small side) when length is even (left = 0, right = 5)
            middle = (left+right)//2
            if nums[middle] == target:
                return middle
            elif nums[middle] > target:
                right = middle-1
            else:
                left = middle+1

        # if at the end target didn't match with anybody in the nums
        # left = right + 1, meaning left = lengh + 1, left is the lower bound of target
        return left

    def searchInsert_bmo(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            middle = round((left+right)/2) # it should be the middle(odd) and middle right(even) except for len(nums) = 2, round(1/2) = 0(the left)
            # round() can sometimes push you right instead of left, especially with even-length arrays.
            if nums[middle] == target:
                return middle
            elif nums[middle] > target:
                # target is the left of middle, update right
                right = middle-1
            else:
                left = middle+1

        # if at the end target didn't match with anybody in the nums
        # right = left - 1
        return middle

# the BMO (build my own) version failed 4 out of 10 tests
# single not found insert: UnboundLocalError: local variable 'middle' referenced before assignment
# round() can sometimes push you right instead of left, especially with even-length arrays.
# even insert last elements: AssertionError # [1,2,3,4], 7 -> returns 3 (expected 4)
"""
[1,2,3,4], target = 7: 
left = 0, right = 3 (in while loop) middle = 2 -> nums[middle] = nums[2] = 3 < 7 -> left = middle+1 = 3
left = 3, right = 3 (in while loop) middle = 3 -> nums[middle] = nums[3] = 4 < 7 -> left = middle+1 = 4
left = 4, right = 3 (out of while loop) left means the lower bound of what we are looking for (target) should return 4 (left)
"""
# odd insert last element: AssertionError # [1,2,3,4,5], 7 -> returns 4 (expected 5)
"""
[1,2,3,4,5], target = 7
left = 0, right = 4 (in while loop) middle = 2 -> nums[middle] = nums[2] = 3 < 7 -> left = middle+1 = 3
left = 3, right = 4 (in while loop) middle = 4 -> nums[middle] = nums[4] = 5 < 7 -> left = middle+1 = 5
left = 5, right = 4 (out of while loop) should return 5 (left)
"""
# odd insert middle: AssertionError # [1,2,3,5,9], 6 -> returns 3 (expect 4)
"""
[1,2,3,5,9], target = 6
left = 0, right = 4 (in while loop) middle = 2 -> nums[middle] = nums[2] = 3 < 6 -> left = middle+1 = 3
left = 3, right = 4 (in while loop) middle = 4 -> nums[middle] = nums[4] = 9 > 6 -> right = middle-1 = 3
left = 3, right = 3 (in while loop) middle = 3 -> nums[middle] = nums[3] = 5 < 6 -> left = middle+1 = 4
left = 4, right = 3 (out of while loop) nums[4] = 9 nums[3] = 5, should returns 4 (left)
"""
"""
We maintain:

left = the smallest index where target could possibly be inserted (lower bound).
right = the largest index where target could possibly be inserted (upper bound).

🔹 When the loop ends

The loop stops when left > right.
At that exact point:
All indices < left hold values strictly less than target.
All indices > right hold values strictly greater than target.

And since right < left, there’s no gap left:
👉 left is exactly the position where target belongs.
"""




