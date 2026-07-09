# Minimum Window Substring

## Problem Statement
Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such window exists, return `""`.

## Optimal Approach
**Sliding Window + Two Frequency Maps** | Time: O(|s| + |t|) | Space: O(|s| + |t|)

**Setup**:
- `need`: frequency map of characters required from `t`.
- `have`: frequency map of characters currently in the window.
- `formed`: number of distinct characters in `t` whose required count is satisfied in the current window.
- `required`: total number of distinct characters in `t` that need to be satisfied.

**Expand** `right` until the window is valid (formed == required). Then **shrink** `left` to find the minimum valid window. Record the minimum each time the window is valid.

```java
// Java — Optimal
public String minWindow(String s, String t) {
    if (s.isEmpty() || t.isEmpty()) return "";

    Map<Character, Integer> need = new HashMap<>();
    for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);

    int required = need.size();   // distinct chars in t that need to be matched
    int formed = 0;               // distinct chars currently satisfied in window
    Map<Character, Integer> have = new HashMap<>();

    int left = 0;
    int minLen = Integer.MAX_VALUE;
    int resLeft = 0, resRight = 0;

    for (int right = 0; right < s.length(); right++) {
        // Expand: add s[right] to window
        char c = s.charAt(right);
        have.merge(c, 1, Integer::sum);
        if (need.containsKey(c) && have.get(c).equals(need.get(c))) {
            formed++;
        }

        // Shrink: move left while window is valid
        while (formed == required) {
            // Record minimum
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                resLeft = left;
                resRight = right;
            }
            // Remove s[left] from window
            char lc = s.charAt(left++);
            have.merge(lc, -1, Integer::sum);
            if (need.containsKey(lc) && have.get(lc) < need.get(lc)) {
                formed--;
            }
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(resLeft, resRight + 1);
}
```

```python
# Python — Optimal
from collections import Counter
def minWindow(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    required = len(need)
    have = {}
    formed = 0
    left = 0
    min_len = float('inf')
    res = (0, 0)

    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                res = (left, right)
            lc = s[left]
            have[lc] -= 1
            if lc in need and have[lc] < need[lc]:
                formed -= 1
            left += 1
    return s[res[0]:res[1] + 1] if min_len != float('inf') else ""
```

## Suboptimal Approaches
- **Brute Force O(n²)**: Generate all substrings, check each against `t`. Very slow.
- **Sliding window without `formed` counter**: Check validity by comparing entire maps at each step — O(26) per step instead of O(1). Still O(n) overall but unnecessarily slow.

## Common Edge Cases
- **`t` longer than `s`**: Impossible to satisfy — return `""`. The loop will never set `formed == required`.
- **`t` contains duplicates** (e.g., `t = "aa"`): Both 'a's must appear in the window. `need['a'] = 2` and `have['a']` must reach 2. The `formed` counter handles this correctly via `.equals()` comparison.
- **`s == t`**: The entire `s` is the answer.
- **No valid window**: Return `""`. `minLen == Integer.MAX_VALUE` catches this.
- **Single character `t`**: Find the first occurrence in `s`.
- **Using `==` instead of `.equals()` for Integer comparison in Java**: A classic Java bug. `Integer` objects are cached for values -128 to 127, so `==` works accidentally for small counts but fails for larger ones. Always use `.equals()` or unbox with `.intValue()`.

## Key Concepts Tested
- Sliding window with two-pointer
- `formed` / `required` pattern to track window validity in O(1) per step
- Frequency map with duplicate support (not just a set)
- This is a Hard problem — the `formed` counter optimization is what separates O(n) from O(26n)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Sliding window with formed/required O(n)/O(k) | **Optimal** |
| Sliding window with full map comparison per step | **Acceptable** |
| Brute force O(n²) | **Suboptimal** |
| Using `==` on Integer objects (Java) — incorrect for large counts | **Incorrect** |
