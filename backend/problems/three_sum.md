# 3Sum

## Problem Statement
Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that `i`, `j`, `k` are distinct indices and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

## Optimal Approach
**Sort + Two Pointers** | Time: O(n²) | Space: O(1) excluding output

**Steps:**
1. Sort the array — this enables two-pointer and easy duplicate skipping.
2. Iterate `i` from 0 to `n-3`:
   - **Early exit**: if `nums[i] > 0`, break — a sorted array with positive first element can't sum to 0.
   - **Skip outer duplicates**: if `i > 0 && nums[i] == nums[i-1]`, continue.
   - Run two-pointer: `left = i+1`, `right = n-1`.
3. While `left < right`:
   - `sum = nums[i] + nums[left] + nums[right]`
   - If sum == 0: record triplet, skip duplicates on both sides, move both pointers.
   - If sum < 0: `left++` (need larger value).
   - If sum > 0: `right--` (need smaller value).

```java
// Java — Optimal
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (nums[i] > 0) break;
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

```python
# Python — Optimal
def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result
```

## Suboptimal Approaches
- **Brute Force O(n³)**: Three nested loops + a set to deduplicate. Correct but very slow.
- **Hash Set O(n²)**: For each pair `(i,j)`, look up `-(nums[i]+nums[j])` in a set. Same asymptotic complexity as two-pointer but harder deduplication logic and more space.

## Common Edge Cases
- **Fewer than 3 elements** → return empty list.
- **All zeros** (e.g., `[0,0,0,0]`) → return `[[0,0,0]]` exactly once. The duplicate-skipping logic must handle this.
- **All positive or all negative** → no triplets, return empty.
- **Duplicate elements** → three separate deduplication points: outer loop (`i`), left pointer, right pointer. Missing any one causes duplicate triplets.
- **Array like `[-4,-1,-1,0,1,2]`** → tests both the outer and inner duplicate skipping.

## Key Concepts Tested
- Sorting as a preprocessing step to enable two-pointer
- Deduplication logic (three separate places)
- Two-pointer technique on a sorted array
- Early exit optimization (`nums[i] > 0`)
- This problem specifically tests whether candidates can handle duplicates — that's the hard part, not the algorithm itself

## Verdict Guide
| Approach | Verdict |
|---|---|
| Sort + two pointers O(n²) with correct deduplication | **Optimal** |
| Sort + two pointers with missing/wrong deduplication | **Acceptable** (correct algorithm, has bugs) |
| Hash set O(n²) with correct deduplication | **Acceptable** |
| Brute force O(n³) | **Suboptimal** |
| Any approach producing duplicate triplets | **Incorrect** |
