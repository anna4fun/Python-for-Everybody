class Solution:

    # 2026/03/20 my own version
    # 最大错误：你想在“下跌时卖出”，但真正结算时却用了“下跌后的当天价格”，而不是“下跌前的峰值价格”。
    def maxProfit1(self, prices: List[int]) -> int:
        if not prices:
            return 0

        max_profit = 0
        buy_price = None 
        sell_price = None
        temp_min_price = None
        temp_max_price = None

        for i in range(len(prices)):
            if not temp_min_price:
                temp_min_price = prices[i]
            else:
                if not buy_price:
                    # assumption: no buy_price, then no sell_price
                    buy_price = min(temp_min_price, prices[i])
                    temp_max_price = buy_price
                else:
                    # if buy_price, then decide to sell. if sell, reset buy and sell price to None
                    if prices[i] > temp_max_price:
                        temp_max_price = prices[i]
                    else:
                        if prices[i] > buy_price:
                            max_profit += prices[i] - buy_price
                            temp_min_price, buy_price, sell_price = None, None, None

    # correted version
    def maxProfit1_corrected(self, prices: List[int]) -> int:
        if not prices:
            return 0

        max_profit = 0
        buy_price = None
        temp_max_price = None

        for price in prices:
            if buy_price is None:
                buy_price = price
                temp_max_price = price
            else:
                if price >= temp_max_price:
                    temp_max_price = price
                else:
                    max_profit += temp_max_price - buy_price
                    buy_price = price
                    temp_max_price = price

        if buy_price is not None:
            max_profit += temp_max_price - buy_price

        return max_profit

    
    # 2026/03/20 GPT Greedy solution
    def maxProfit2(self, prices: List[int]) -> int:
        if not prices:
            return 0
        max_profit = 0

        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                max_profit += prices[i] - prices[i-1]
        return max_profit
