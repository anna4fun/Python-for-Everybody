class Solution:
    # 2026/03/19 my own version, time takes = 14 mins, time complexity O(n), space complexity O(k)
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) < k:
            k = k%len(nums)
            
        num_shifts = nums[-k:] # this is where the space complexity come from
        for i in range(len(nums)-k-1, -1, -1): # reverse order
            nums[i+k] = nums[i]
        for i in range(k):
            nums[i] = num_shifts[i]

    # 2026/03/19 GPT best version, time complexity O(2n) = O(n), space complexity O(1)
    # idea: 先整个 list 倒过来（延中心反转），造成左右两边顺序颠倒，再分别把两边顺序摆正
    def rotate2(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k %= n
        self.reverse(nums, start = 0, end = n-1) # remember to use self.
        self.reverse(nums, start = 0, end = k-1)
        self.reverse(nums, start = k, end = n-1)

    def reverse(self, nums, start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
