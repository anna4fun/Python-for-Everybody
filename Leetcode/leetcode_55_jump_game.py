class Solution:
    # 2026/03/20 my own solution, DFS/backtracking
    # severe time out issue
    def canJump(self, nums: List[int]) -> bool:
        if len(nums) == 0:
            return False

        current = 0
        distance = len(nums) - 1 - current # current distance between current index to last index
        current_max_step = nums[current]
        #  if distance == current_max_step: # wrong; it's reach or past the last index
        if distance <= current_max_step:
            return True
        else:
            # for i in range(1, current_max_step): # wrong: missed the last item = current_max_step
            for i in range(1, current_max_step+1):
                if self.canJump(nums[i:]) is True: # wrong: will create a new array every single time
                    return True
            return False

    # 2026/03/21 version 2
        # 主要有四点问题：
        # 1. current_max_step 只初始化一次，后面没跟着 current 更新
        # 2. nums[i] 应该是 nums[current + i]
        # 3. >= len(nums) 应该更合理地写成 >= len(nums) - 1
        # 4. 最本质的是：你在盲目 current += 1，但后面的 current 不一定真的可达
        # 你这题不是在“尝试从每个位置都起跳”，而是要始终维护“最远可达边界”。
    def canJump2(self, nums: List[int]) -> bool:
        if len(nums) == 0:
            return False
        current = 0
        current_max_step = nums[current]
        
        while current < len(nums) - 1:
            if current_max_step >= len(nums) - 1 - current: 
                # current distance between current index to last index
                return True
            else:
                for i in range(1, current_max_step+1):
                    if current + i + nums[i] >= len(nums):
                        return True
                current += 1          
                # missing update current_max_step current_max_step = nums[current]
        return False

    # 2026/03/21 GPT的greedy 答案，看不懂
    def canJump3(self, nums: List[int]) -> bool:
        farthest = 0 # 到目前为止，你最远能够到达的下标

        for i in range(len(nums)):
            if i <= farthest:
                # i比目前能达到的最远下标近，更新farthest
                farthest = max(i+nums[i], farthest)
            else:
                return False
        return True
