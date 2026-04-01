from logging import raiseExceptions
from typing import List


class Solution:
    def canCompleteCircuit1(self, gas: List[int], cost: List[int]) -> int:
        # gas: for each station, how much gas can buy.
        # cost: for each station, how much gas takes to the next station
        # key: as long as the total gas can buy up-to the current station > total gas consume for the rest stations, success
        if len(gas) != len(cost):
            raiseExceptions

        n = len(gas)
        
        # delta[i] means: if I start from station i (no prev gas), how much gas I have in the next station
        delta = [gas[i]-cost[i] for i in range(n)]
        # sum(delta) < 0 means total gas available are not enough for the total cost of trip
        if sum(delta) < 0:
            return -1
        
        # for starting i: find the i that makes every cummulative sum >= 0, if cummulative sum for station i = 0, verify gas[i+1] > 0
        # a success starting i should have delta[i] > 0
        for starting in range(n):
            if delta[starting] < 0:
                continue
            cum_sum = 0
            travel_index = list(range(starting, n)) + list(range(0, starting))
            for i in travel_index:
                cum_sum += delta[i]
                if (cum_sum == 0 and cost[i+1] == 0) or cum_sum < 0:
                    break
            else:
                return starting

    def canCompleteCircuit2(self, gas: List[int], cost: List[int]) -> int:
        tank = 0
        start = 0
        total = 0
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            tank += diff
            if tank < 0:
                start = i+1 
                tank = 0
        return -1 if total < 0 else start

         
# test
def main():
    s = Solution()
    gas = [1,2,3,4,5]
    cost = [3,4,5,1,2]
    print(s.canCompleteCircuit1(gas, cost))

    gas = [2,3,4] 
    cost = [3,4,3]
    print(s.canCompleteCircuit1(gas, cost))

    gas = [2,5,4,5,0] 
    cost = [2,4,2,7,0]
    print(s.canCompleteCircuit1(gas, cost))

    gas = [2,5,4,5,1] 
    cost = [2,4,2,7,1]
    print(s.canCompleteCircuit1(gas, cost))

    gas = [3,1,1]
    cost = [1,2,3]
    print(s.canCompleteCircuit1(gas, cost))

if __name__ == "__main__":
    main()

