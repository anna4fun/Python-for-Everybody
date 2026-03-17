from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        if len(nums1) != m + n:
            raise ValueError("length don't match")
        if n == 0:
            return nums1
        if m == 0:
            for i in range(n):
                nums1[i] = nums2[i]
            return nums1

        p1 = m - 1
        p2 = n - 1
        p3 = m + n - 1
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p3] = nums1[p1]
                p1 -= 1
                p3 -= 1
            elif nums1[p1] < nums2[p2]:
                nums1[p3] = nums2[p2]
                p2 -= 1
                p3 -= 1
            else:
                nums1[p3] = nums1[p1]
                nums1[p3 - 1] = nums2[p2]
                p1 -= 1
                p2 -= 1
                p3 -= 2

        # when p1 = 0 but p2 >= 0, move rest of L2 to L1
        while p2 >= 0:
            nums1[p3] = nums2[p2]
            p2 -= 1
            p3 -= 1

        return nums1