class Solution:
    # 2020/02/17 version
    def removeDuplicates(self, nums: [int]) -> int:
        l = 0
        r = 1
        
        while r < len(nums):
            if nums[l] == nums[r]:
                nums.pop(r)
                
            else:
                l += 1
                r += 1
        return(len(nums))
    
    # 2026/03/18 version from myself O(n^2)
    def removeDuplicates2(self, nums: List[int]) -> int:
        # starting position of each unique element
        start_post = []
        i = 0
        while i <= len(nums)-1:
            if nums[i] not in start_post:
                start_post.append(nums[i])
            i += 1

        total_unique_items = len(start_post)
        for i in range(total_unique_items):
            nums[i] = start_post[i]
        return total_unique_items

    # 2026/03/18 new version after seeing the best solution, O(n) Time and O(1) Space complexity
    def removeDuplicates3(self, nums: List[int]) -> int:
        if not nums:
            return 0   
        l = 0 # l stands for the last item's index in the (current) all unique item list 
        r = 1 # r stands for the item we compare with nums[l] at this round
        while r <= len(nums)-1:
            if nums[l] == nums[r]:
                r += 1
                continue
            else:      
                if r - l > 1: # meaning there's duplicates in between l and r
                    l += 1
                    nums[l] = nums[r]
                    r += 1
                else:
                    l += 1
                    r += 1
        return l+1

    def removeDuplicates4(self, nums: List[int]) -> int:
        if not nums:
            return 0   
        write = 0
        for read in range(1,len(nums)):
            if nums[read] != nums[write]:
                write += 1
                nums[write] = nums[read]
        return write+1
        
def test_functions():
    test = Solution()
    assert test.removeDuplicates([1,1,2]) == 2
    assert test.removeDuplicates([0,0,1,1,1,2,2,3,3,4]) == 5
    assert test.removeDuplicates([0]) == 1
    assert test.removeDuplicates2([1,1,2]) == 2
    assert test.removeDuplicates2([0,0,1,1,1,2,2,3,3,4]) == 5
    assert test.removeDuplicates2([0]) == 1