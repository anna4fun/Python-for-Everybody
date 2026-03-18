class Solution:
    # 2026/03/18 I work this out myself, O(n) O(1) complexity
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        write = 1
        counter = 0 # duplicate counter
        
        for read in range(1, len(nums)):
            if nums[read] == nums[read-1]:
                counter += 1
                if counter == 1:
                    nums[write] = nums[read]
                    write += 1
            else:
                counter = 0
                nums[write] = nums[read]
                write += 1

        return write