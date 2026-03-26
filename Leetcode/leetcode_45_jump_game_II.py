class Solution:
    def jump(self, nums: List[int]) -> int:
        current_boundary = 0
        farthest = 0
        jumps = 0

        for i in range(len(nums)-1):
            # 顺着列表iterate, 每次一都检查一下当前位置最远是不是能跳得更远
            farthest = max(farthest, i+nums[i])
            if i == current_boundary:
                # 当我们iterate到boundary时，我们一定需要转移一次
                jumps +=1 
                # 这里省略了一个回头决定是从current_boundary左边哪一个开始跳，只保留了左边这一段所有位置中能跳到的最远距离
                current_boundary = farthest
        return jumps