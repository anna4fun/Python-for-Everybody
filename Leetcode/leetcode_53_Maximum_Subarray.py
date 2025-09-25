# Given an integer array nums, find the subarray with the largest sum, and return its sum.
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # DP: the overall idea of DP is, keep rolling and update the global maximum
        gmax = nums[0]
        prev_sum = nums[0]

        for n in nums[1:]:
            # at n, we make the judgement of:
            #  do we want to (1)Re-start the subarray from n, or (2)attach n to the subarray
            # (1) if prev_sum + n < n, update head to n; if gmax > n, keep gmax, else gmax = n
            # (2) if prev_sum + n >= n, update tail to n; if new array's sum prev_sum > gmax, update gmax = prev_max, else keep gmax
            # the updates of prev_sum (local max) and gmax (global max) seems disconnected
            prev_sum = max(prev_sum+n, n)
            gmax = max(gmax, prev_sum)
        return(gmax)

    # my own code
    def maxSubArray1(self, nums: List[int]) -> int:
        gmax = nums[0]
        prev_sum = nums[0]
        for n in nums[1:]:
            # at n, we make the judgement of:
            #  do we want to (1)Re-start the subarray from n, or (2)attach n to the subarray
            # (1) if prev_sum + n < gmax, update head to n, gmax = n
            # (2) if prev_sum + n >= gmax, update tail to n, gmax = n+gmax
            if prev_sum + n < gmax:
                prev_sum = n
                gmax = n
            else:
                prev_sum += n
                gmax += n
        return (gmax)


s = Solution()
print(s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))
assert s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]) == 6
