# Kth Largest Element in an Array

## Problem Statement
Given an integer array `nums` and an integer `k`, return the **kth largest element** in the array. Note: this is the kth largest in **sorted order**, not the kth distinct element.

**Example**: `nums = [3,2,1,5,6,4], k = 2` → `5` (2nd largest).

## Optimal Approach 1
**Min-Heap of size K** | Time: O(n log k) | Space: O(k)

Maintain a min-heap of size `k`. For each element:
- Add it to the heap.
- If heap size > k, remove the smallest (the heap root).

At the end, the root of the min-heap is the kth largest.

**Why min-heap?** The top of the min-heap is the smallest among the k largest elements, which is exactly the kth largest.

```java
// Java — Min-Heap O(n log k)/O(k)
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();  // min-heap by default
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll();   // Remove smallest — keep only k largest
        }
    }
    return minHeap.peek();   // Root = kth largest
}
```

```python
# Python — Min-Heap using heapq
import heapq
def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

## Optimal Approach 2 (Average Case)
**QuickSelect** | Time: O(n) average, O(n²) worst case | Space: O(1)

A partition-based algorithm similar to QuickSort. Pick a pivot, partition the array:
- If pivot lands at index `n-k` (from left), it IS the kth largest.
- If pivot index > `n-k`, search left half.
- If pivot index < `n-k`, search right half.

```java
// Java — QuickSelect
public int findKthLargest(int[] nums, int k) {
    return quickSelect(nums, 0, nums.length - 1, nums.length - k);
}
private int quickSelect(int[] nums, int left, int right, int kSmallest) {
    int pivot = nums[right];
    int p = left;
    for (int i = left; i < right; i++) {
        if (nums[i] <= pivot) swap(nums, i, p++);
    }
    swap(nums, p, right);
    if (p == kSmallest) return nums[p];
    return p > kSmallest ? quickSelect(nums, left, p-1, kSmallest)
                         : quickSelect(nums, p+1, right, kSmallest);
}
private void swap(int[] nums, int i, int j) {
    int tmp = nums[i]; nums[i] = nums[j]; nums[j] = tmp;
}
```

## Suboptimal Approaches
- **Sort then index**: `Arrays.sort(nums); return nums[n-k];` → O(n log n) / O(1). Simple, works, but not optimal.
- **Max-heap of all n elements, poll k times**: O(n + k log n). Acceptable but wastes space with all n elements.

## Common Edge Cases
- **k = 1**: Returns the maximum. Works correctly for both approaches.
- **k = n**: Returns the minimum. Works correctly.
- **Duplicate values** (e.g., `[3,3,3,3], k=2`): Returns `3`. Both approaches handle duplicates correctly.
- **Single element** (`k = 1`): Returns that element.
- **QuickSelect worst case O(n²)**: Occurs when the pivot is always the smallest or largest (e.g., sorted array). Randomizing pivot selection (swap random element with `right` before partitioning) fixes this to O(n) expected.

## Key Concepts Tested
- Min-heap of size k pattern (appears in: top-k frequent elements, k closest points, etc.)
- Why min-heap for k-largest (counterintuitive but logical once understood)
- QuickSelect — average O(n) beats sorting
- `PriorityQueue` is a min-heap by default in Java. For max-heap: `new PriorityQueue<>(Collections.reverseOrder())`
- Python's `heapq` is a min-heap. For max-heap: push negative values.

## Verdict Guide
| Approach | Verdict |
|---|---|
| Min-heap of size k O(n log k)/O(k) | **Optimal** |
| QuickSelect O(n) avg / O(n²) worst / O(1) space | **Optimal** (better avg complexity, good for interviews) |
| Sort then index O(n log n)/O(1) | **Acceptable** |
| Max-heap of all n, poll k times O(n + k log n)/O(n) | **Acceptable** |
| Wrong heap type (max-heap of size k) | **Incorrect** |
