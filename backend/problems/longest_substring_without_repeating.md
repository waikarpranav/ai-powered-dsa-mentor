# Longest Substring Without Repeating Characters

## Problem Statement
Given a string `s`, find the length of the longest substring without duplicate characters.

## Optimal Approach
**Sliding Window + HashMap** | Time: O(n) | Space: O(min(n, 26)) ≈ O(1) for lowercase letters

Maintain a window `[left, right]` where all characters are unique. Use a `HashMap<Character, Integer>` storing the **last seen index** of each character.

For each character at `right`:
- If it was seen before AND its last index ≥ `left` (i.e., it's inside the current window): jump `left` to `lastSeen[char] + 1` to skip past the duplicate.
- Update `lastSeen[char] = right`.
- Update `maxLen = max(maxLen, right - left + 1)`.

```java
// Java — Optimal (HashMap storing last index)
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> lastSeen = new HashMap<>();
    int maxLen = 0;
    int left = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (lastSeen.containsKey(c) && lastSeen.get(c) >= left) {
            left = lastSeen.get(c) + 1;  // Jump left past the duplicate
        }
        lastSeen.put(c, right);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

```python
# Python — Optimal
def lengthOfLongestSubstring(s):
    last_seen = {}
    max_len = 0
    left = 0
    for right, c in enumerate(s):
        if c in last_seen and last_seen[c] >= left:
            left = last_seen[c] + 1
        last_seen[c] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

**Alternative — HashSet with slow shrink** (also O(n) but two movements per character):
```java
// Also acceptable — HashSet variant
public int lengthOfLongestSubstring(String s) {
    Set<Character> window = new HashSet<>();
    int maxLen = 0, left = 0;
    for (int right = 0; right < s.length(); right++) {
        while (window.contains(s.charAt(right))) {
            window.remove(s.charAt(left++));
        }
        window.add(s.charAt(right));
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

## Suboptimal Approaches
- **Brute Force O(n²) or O(n³)**: Generate all substrings, check each for uniqueness. Very slow.
- **HashSet without index tracking**: Forces you to shrink one character at a time from the left (the while loop variant above). O(n) amortized but makes more operations — acceptable but not optimal.

## Common Edge Cases
- **Empty string** (`""`): return 0. The loop never runs.
- **All unique characters** (`"abcdef"`): the whole string is the answer. `left` never moves.
- **All same character** (`"aaaaaa"`): answer is 1. Every step jumps `left` to `right`.
- **String of length 1**: return 1.
- **Characters like spaces, digits, uppercase**: HashMap handles all ASCII characters correctly; the array trick (`int[128]`) also works.
- **Critical bug**: forgetting the `lastSeen.get(c) >= left` check. Without it, `left` could jump backwards when a character was seen before the current window started. E.g., `"abba"` — when you hit the second `a`, `lastSeen['a'] = 0`, but `left` is already at 2. Without the `>= left` check, you'd wrongly set `left = 1`.

## Key Concepts Tested
- Sliding window pattern: expand right, contract left on violation
- Storing last-seen index (not just presence) for O(1) left-pointer jumps
- The `>= left` boundary check — the most commonly missed detail
- This is the canonical sliding window problem — understanding it deeply helps with Minimum Window Substring and other harder variants

## Verdict Guide
| Approach | Verdict |
|---|---|
| HashMap with index jump O(n)/O(k) | **Optimal** |
| HashSet with while-loop shrink O(n)/O(k) | **Acceptable** |
| HashMap without `>= left` check (buggy on repeated chars) | **Incorrect** |
| Brute force O(n²) | **Suboptimal** |
