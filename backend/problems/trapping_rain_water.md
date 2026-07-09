# Trapping Rain Water

## Problem Statement
Given `n` non-negative integers representing an elevation map where each bar has width 1, compute how much water can be trapped after it rains.

Water trapped at position `i` = `min(maxLeft[i], maxRight[i]) - height[i]`

## Optimal Approach
**Two Pointers** | Time: O(n) | Space: O(1)

Instead of precomputing prefix/suffix max arrays, use two pointers and a running max on each side.

**Key insight**: The water at position `i` is determined by `min(maxLeft, maxRight)`. If `maxLeft < maxRight`, we already know the water at `left` is `maxLeft - height[left]` regardless of what's to the right (because maxRight is already larger). So process the smaller side.

```java
// Java — Optimal (Two Pointers)
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int maxLeft = 0, maxRight = 0;
    int water = 0;
    while (left < right) {
        if (height[left] <= height[right]) {
            if (height[left] >= maxLeft) {
                maxLeft = height[left];      // New max — no water here
            } else {
                water += maxLeft - height[left];  // Trapped water
            }
            left++;
        } else {
            if (height[right] >= maxRight) {
                maxRight = height[right];
            } else {
                water += maxRight - height[right];
            }
            right--;
        }
    }
    return water;
}
```

```python
# Python — Optimal (Two Pointers)
def trap(height):
    left, right = 0, len(height) - 1
    max_left = max_right = water = 0
    while left < right:
        if height[left] <= height[right]:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                water += max_right - height[right]
            right -= 1
    return water
```

## Alternative Approach (Prefix/Suffix Arrays)
**Time: O(n) | Space: O(n)** — Easier to understand, acceptable in interviews.

```java
public int trap(int[] height) {
    int n = height.length;
    int[] maxLeft  = new int[n];
    int[] maxRight = new int[n];
    maxLeft[0] = height[0];
    for (int i = 1; i < n; i++) maxLeft[i] = Math.max(maxLeft[i-1], height[i]);
    maxRight[n-1] = height[n-1];
    for (int i = n-2; i >= 0; i--) maxRight[i] = Math.max(maxRight[i+1], height[i]);
    int water = 0;
    for (int i = 0; i < n; i++) water += Math.min(maxLeft[i], maxRight[i]) - height[i];
    return water;
}
```

## Suboptimal Approaches
- **Brute Force O(n²)**: For each bar, scan left and right to find max heights. Then compute water for that bar. Very slow.
- **Stack-based approach**: O(n) time and space. Processes horizontal layers of water. Correct but harder to explain — only use if you already know it well.

## Common Edge Cases
- **Empty array or length < 3**: No water can be trapped — return 0. Arrays of length 0, 1, or 2 have no "middle" to trap water.
- **Monotonically increasing** (e.g., `[1,2,3,4]`): No water trapped — `0`.
- **Monotonically decreasing** (e.g., `[4,3,2,1]`): No water trapped — `0`.
- **Single valley** (e.g., `[3,0,3]`): 3 units of water.
- **Multiple valleys** (e.g., `[0,1,0,2,1,0,1,3,2,1,2,1]`): 6 units. The classic example.

## Common Mistakes
- Confusing this with **Container With Most Water** — that picks two bars to maximize area; this fills all gaps between all bars.
- In the stack approach: forgetting to handle the case where `height[i] == height[stack.peek()]`.
- In the prefix/suffix approach: initializing `maxLeft[0] = 0` instead of `height[0]`.

## Key Concepts Tested
- Two-pointer greedy (advance the smaller side)
- Understanding that water at each bar = min(maxLeft, maxRight) - height
- Space optimization from O(n) prefix/suffix arrays to O(1) two-pointer

## Verdict Guide
| Approach | Verdict |
|---|---|
| Two pointers O(n)/O(1) | **Optimal** |
| Prefix/suffix arrays O(n)/O(n) | **Acceptable** |
| Stack-based O(n)/O(n) | **Acceptable** |
| Brute force O(n²) | **Suboptimal** |
