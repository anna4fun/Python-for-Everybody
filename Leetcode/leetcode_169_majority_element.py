class Solution:
    # 2026/03/18 my own version, O(n) time and space complexity
    def majorityElement1(self, nums: List[int]) -> int:
        stats = {}
        for i in range(len(nums)):
            if nums[i] in stats:
                stats[nums[i]] += 1
            else:
                stats[nums[i]] = 1

        
        max_cur = -1
        majority_element = -1
        for key, values in stats.items():
            if values > max_cur:
                majority_element = key
                max_cur = values
        return majority_element

    # 2026/03/18 GPT solution,  let each new number cancel or contribute to the current candidate, 
    # majority elements means: the winning candidates must have > n//2 votes ** key assumption **
    # this key assumption means there's no such case as [1,1,1,2,2,2,3] which has no candidate that have > n//2 votes
    def majorityElement2(self, nums: List[int]) -> int:
        candidate = None
        count = 0

        for n in nums:
            if count == 0:
                candidate = n
                count += 1
            else:
                if n == candidate:
                    count += 1
                else:
                    count -= 1
        return candidate