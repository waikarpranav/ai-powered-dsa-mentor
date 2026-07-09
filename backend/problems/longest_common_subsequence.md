# Longest Common Subsequence (LCS)

## Problem Statement
Given two strings `text1` and `text2`, return the length of their **longest common subsequence**. A subsequence is formed by deleting some characters without changing order. If no common subsequence exists, return 0.

**Example**: `text1 = "abcde"`, `text2 = "ace"` → LCS = "ace" → length 3.

## Optimal Approach
**2D Bottom-Up DP** | Time: O(m × n) | Space: O(m × n)

`dp[i][j]` = length of LCS of `text1[0..i-1]` and `text2[0..j-1]`.

**Recurrence**:
- If `text1[i-1] == text2[j-1]`: characters match → `dp[i][j] = dp[i-1][j-1] + 1`
- Else: take the best from skipping one character from either string → `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

**Base case**: `dp[0][j] = dp[i][0] = 0` (empty string has LCS of 0 with anything).

```java
// Java — Bottom-Up DP (Optimal)
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}
```

```python
# Python — Bottom-Up DP
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

**Space-Optimized O(n) space** — use only two rows:
```java
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[] prev = new int[n + 1], curr = new int[n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i-1) == text2.charAt(j-1)) curr[j] = prev[j-1] + 1;
            else curr[j] = Math.max(prev[j], curr[j-1]);
        }
        int[] temp = prev; prev = curr; curr = temp;
    }
    return prev[n];
}
```

## Common Mistakes
- **Confusing with Longest Common Substring**: Substring requires contiguous characters. LCS allows non-contiguous. They have different recurrences.
  - LCS match: `dp[i][j] = dp[i-1][j-1] + 1`
  - Substring match: `dp[i][j] = dp[i-1][j-1] + 1` ← same, BUT
  - LCS no-match: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` ← carry forward
  - Substring no-match: `dp[i][j] = 0` ← reset (no carry)

## Common Edge Cases
- **One or both strings empty**: `dp[0][j] = dp[i][0] = 0`. Returns 0 correctly.
- **No common characters**: All `dp[i][j]` computed via max — returns 0.
- **Identical strings**: LCS = entire string. `dp[m][n] = m = n`.
- **One string is a subsequence of the other**: LCS = shorter string length.

## Key Concepts Tested
- 2D DP — the most common interview DP after 1D
- The "match or skip" recurrence structure
- LCS vs Longest Common Substring (different recurrence on no-match)
- Space optimization: 2D → 1D (two rows)
- LCS is a building block for: diff algorithms, edit distance, shortest common supersequence

## Verdict Guide
| Approach | Verdict |
|---|---|
| 2D DP O(mn)/O(mn) | **Optimal** |
| Space-optimized 2-row DP O(mn)/O(n) | **Optimal** |
| Memoized recursion O(mn)/O(mn) | **Acceptable** |
| Confused with Longest Common Substring (wrong no-match case) | **Incorrect** |
| Plain recursion without memo O(2^(m+n)) | **Suboptimal** |
