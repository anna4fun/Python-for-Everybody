"""
Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
Explanation:
There is no string in strs that can be rearranged to form "bat".
The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]
"""
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        results = [None]*len(strs)
        dict_vocab = []
        clock = -1
        results_dd = []
        for i in range(len(strs)):
            # print(i)
            words = self.generate_dict(strs[i]) # a dictionary/hash of tokens and frequency of the input string
            if words not in dict_vocab:
                clock += 1
                dict_vocab.append(words)
                results[i] = clock
                results_dd.append([strs[i]])
            else:
                for j in range(len(dict_vocab)):
                    if dict_vocab[j] == words:
                        results[i] = j
                        results_dd[j].extend([strs[i]]) # in-place
        return results_dd

    def generate_dict(self, s: str) -> Dict:
        results = {}
        for i in s:
            if i in results:
                results[i] += 1
            else:
                results[i] = 1
        return results

s = Solution()
strs = ["eat","tea","tan","ate","nat","bat"]
print(s.groupAnagrams(strs))
print(s.groupAnagrams([" "])) # [[' ']]
# dict_vocab = [{'e': 1, 'a': 1, 't': 1}, {'t': 1, 'a': 1, 'n': 1}, {'b': 1, 'a': 1, 't': 1}]
# result  = [0, 0, 1, 0, 1, 2] # for strs[i] of the string, results[i] tells you which one of the dict_vocab it belongs to
# results_dd is just organizing results so that [0, 0, 1, 0, 1, 2] -> [[0,0,0],[1,1],[2]] and put the corresponding string to repalce the digits

