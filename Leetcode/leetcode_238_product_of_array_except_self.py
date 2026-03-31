class Solution:
    def productExceptSelf1(self, nums: List[int]) -> List[int]:
        count_zero = 0
        total_product = 1
        for num in nums:
            if num != 0:
                total_product *= num
            else:
                count_zero +=1

        if count_zero > 1:
            for i in range(len(nums)):
                nums[i] = 0
        elif count_zero == 1:
            for i in range(len(nums)):
                if nums[i] != 0:
                    nums[i] = 0
                else:
                    nums[i] = total_product
        else:
            for i in range(len(nums)):
                nums[i] = round(total_product/nums[i])
                # 违反了题目说不能用除法
                # 而且精度不对，应该用 total_product // nums[i]
        return nums

    def productExceptSelf2(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answers = [1] * n
        left_product = 1

        # from left to right, answers[i] is the product of all numbers left of i
        for i in range(n):
            answers[i] = left_product
            left_product *= answers[i] # wrong: left_product *= nums[i]
            # answers用来存left product, left_product本身需要用nums来算
        
        right_product = nums[-1] # wrong: right_product起始是1，而不是nums最后一个数
        # 因为nums最后一个数右边没有数字了，所以要乘1
        for i in range(n-1, 0, -1): # wrong: range(n-1, -1, -1)写-1才能到0
            answers[i] *= right_product
            right_product *= nums[i]
        
        return answers
