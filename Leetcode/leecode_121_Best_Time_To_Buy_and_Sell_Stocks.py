from typing import List

class Solution:
    # intuition, this one works for small lists, but timeout when list is huge
    def maxProfit1(self, prices: List[int]) -> int:
        # starting from left to right
        max_p = 0
        for sell_day in list(range(len(prices)-1, 0, -1)):
            # print(sell_day)
            buy_day = 0
            while buy_day < sell_day:
                delta = prices[sell_day] - prices[buy_day]
                if delta > max_p:
                    max_p = delta
                buy_day += 1
        return(max_p)

    # DP
    def maxProfit(self, prices: List[int]) -> int:
        # overall idea: keep rolling, update the global maximum profit and minimum price
        if len(prices) < 2:
            return 0
        min_buy_price = prices[0]
        max_profit = 0
        for p in prices[1:]:
            if p < min_buy_price:
                min_buy_price = p
            else:
                max_profit = max(max_profit, p-min_buy_price)
        return max_profit

s = Solution()
print(s.maxProfit([7,1,5,3,6,4]))
print(s.maxProfit([7,6,4,3,1]))

