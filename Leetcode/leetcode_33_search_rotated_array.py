from typing import List
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            middle = (left + right) // 2
            if target == nums[middle]:
                return middle

            if nums[left] <= nums[middle]:
                # meaning the left part is sorted
                if nums[left] <= target < nums[middle]:
                    right = middle - 1
                else:
                    # go to the other part
                    left = middle + 1

            else:
                # meaning the right part is sorted
                if nums[middle] < target <= nums[right]:
                    left = middle + 1
                else:
                    # go to the other part
                    right = middle - 1
        return -1