"""
704. Binary Search
Easy

Given an array of integers nums which is sorted in ascending order, and an integer target,
write a function to search target in nums.
If the target exists, then return its index. Otherwise, return -1.
You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
Example 2:

Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1


Constraints:

1 <= nums.length <= 104
-104 < nums[i], target < 104
All the integers in nums are unique.
nums is sorted in ascending order.
"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        # have the "=" here because nums might only contain 1 item, such that left = right = 0
        while left <= right:
            if  target < nums[left] or target > nums[right]:
                return -1
            middle_index = round((right + left)/2) # + for if the list moves right
            if nums[middle_index] == target:
                return middle_index
            elif nums[middle_index] > target:
                # meaning the target is on the left/small side of nums
                right = middle_index - 1
            else:
                left = middle_index + 1
        # if till the end (aka left > right) it still doesn't return anything, means the target doesn't exist in nums
        return -1

    # my first intuitive solution
    def search_test(self, nums: List[int], target: int) -> int:
        len_num = len(nums)
        if target > nums[len_num-1] | target < nums[0]:
            return -1
        # if len_num is odd, start_index would be the middle one, else, start_index would be the mid-right one
        start_index = round(len_num/2)
        if nums[start_index] == target:
            return start_index
        elif nums[start_index] > target:
            # meaning the target is on the left/small side of nums[start_index]
            nums = nums[0:start_index-1]
        else:
            nums = nums[start_index+1:]
        # Biggest problem: how to iterate to the next nums? and the nums length changed, how do I return the global index?
        # you create a new sliced list that loses the original indices. That’s why you’re stuck — you no longer know the “global index” in the original nums.



s = Solution()
assert s.search([-1,0,3,5,9,12], 9) == 4
assert s.search([-1,0,3,5,9,12], 2) == -1

