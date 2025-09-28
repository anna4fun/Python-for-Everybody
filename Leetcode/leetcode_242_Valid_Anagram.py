"""
Topics
Given two strings s and t, return true if t is an anagram of s, and false otherwise.
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once.

Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false

Constraints:

1 <= s.length, t.length <= 5 * 104
s and t consist of lowercase English letters.

Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?
"""
from typing import Dict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        s_dict = self.generate_dict(s)
        t_dict = self.generate_dict(t)
        if s_dict == t_dict:
            return True
        else:
            return False

    def generate_dict(self, s: str) -> Dict:
        results = {}
        for i in s:
            if i in results:
                results[i] += 1
            else:
                results[i] = 1
        return results

s = Solution()
print(s.isAnagram("anagram", "nagaram"))
print(s.isAnagram("cat", "car"))

