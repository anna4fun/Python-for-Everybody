class Solution:
    def checkString(self, s: str) -> bool:
        # find position of first b as first_b
        # if any i > pos_b contains a, return false
        if not s or len(s) == 1:
            return True
        first_b = len(s)
        for i in range(len(s)):
            if s[i] == 'a':
                if i > first_b:
                    return False
            if s[i] == 'b':
                first_b = min(first_b, i)
        return True