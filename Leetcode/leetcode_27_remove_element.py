class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            if nums[right] == val:
                right -= 1
                continue
            if nums[left] == val:
                temp = nums[left]
                nums[left] = nums[right]
                nums[right] = temp
                right -= 1
            left += 1
        
        return right+1

# essentially: right is the index if the last element of the "effective" list, so the final effective list is of length right+1