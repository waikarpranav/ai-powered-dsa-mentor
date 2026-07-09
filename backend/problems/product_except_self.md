# Product of Array Except Self

## Problem Statement
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`. Must run in O(n) time. **Division is NOT allowed.**

## Optimal Approach
**Prefix × Suffix Pass** | Time: O(n) | Space: O(1) (output array doesn't count)

**Key Insight**: `answer[i] = (product of everything to the LEFT of i) × (product of everything to the RIGHT of i)`

**Two-pass strategy**:
1. **Left pass**: For each position `i`, store the product of all elements to its left.
2. **Right pass**: Multiply in the product of all elements to the right (tracked as a running variable).

```java
// Java — Optimal
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];

    // Left pass: result[i] = product of nums[0..i-1]
    result[0] = 1;
    for (int i = 1; i < n; i++) {
        result[i] = result[i - 1] * nums[i - 1];
    }

    // Right pass: multiply in product of nums[i+1..n-1]
    int rightProduct = 1;
    for (int i = n - 1; i >= 0; i--) {
        result[i] *= rightProduct;
        rightProduct *= nums[i];
    }

    return result;
}
```

```python
# Python — Optimal
def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n

    # Left pass
    for i in range(1, n):
        result[i] = result[i - 1] * nums[i - 1]

    # Right pass
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]

    return result
```

**Trace through `[1, 2, 3, 4]`**:
- After left pass:  `[1, 1, 2, 6]`
- Right pass (i=3): result[3] = 6×1 = 6,  right = 4
- Right pass (i=2): result[2] = 2×4 = 8,  right = 12
- Right pass (i=1): result[1] = 1×12 = 12, right = 24
- Right pass (i=0): result[0] = 1×24 = 24, right = 24
- Final: `[24, 12, 8, 6]` ✓

## Suboptimal Approaches
- **Brute Force O(n²)**: For each `i`, loop through all other elements and multiply. Correct but too slow.
- **Division approach**: Compute total product, divide by `nums[i]`. Disallowed by the problem AND breaks on zeros.
- **Two separate O(n) arrays for prefix and suffix**: Correct and O(n) time but uses O(n) extra space. The optimal solution reduces this to O(1) extra by computing suffix on-the-fly.

## Common Edge Cases
- **Array contains a zero**: The element at the zero's position gets the product of all others; everything else gets 0. The prefix/suffix approach handles this correctly without division.
- **Array contains two or more zeros**: All results are 0.
- **Negative numbers**: No special handling needed — multiplication works correctly.
- **Array of length 2** (e.g., `[3, 7]`): result = `[7, 3]`. Works correctly.
- **All ones** (e.g., `[1,1,1]`): result = `[1,1,1]`. Works correctly.
- **Integer overflow**: If all numbers are large, products may overflow `int`. In practice, assume values are within safe range unless told otherwise.

## Key Concepts Tested
- Prefix product technique — same pattern used in many range query problems
- Recognizing that "left product × right product" decomposes the problem
- Optimizing space by using the output array itself as the prefix store
- Why division is specifically forbidden (fails on zeros)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Prefix/suffix O(n)/O(1) extra space | **Optimal** |
| Prefix/suffix with two separate O(n) arrays | **Acceptable** |
| Division-based approach | **Incorrect** (disallowed + fails on zero) |
| Brute force O(n²) | **Suboptimal** |
