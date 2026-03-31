class Solution:
    def hIndex1(self, citations: List[int]) -> int:
        if citations is None:
            return 0

        citations.sort()
        n = len(citations)
        for i in range(n):
            # n-i: the number of papers on the right of the ith paper(including)
            # n-i = the number of papers have citations >= the ith paper's citation 
            # n-i = (n-1) - i + 1
            if citations[i] <= n-i:
                next # wrong, should be continue
            else:
                # ith paper have citations > the number of papers on the right
                # so i-1's paper's citation is the max
                # 但 h-index 返回的不是某篇论文的引用数，而是满足条件的“论文篇数”，也就是 n - i。
                return citations[i-1]
        return citations[i]
        # 最大的错误：返回值是“引用数”，而题目要求的是“篇数”