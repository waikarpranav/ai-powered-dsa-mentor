"""
seed.py — Seeds the problems table from PROBLEM_METADATA on app startup.

Idempotent: will not insert duplicates if run multiple times.
Later, Week 2: extend this to also parse the .md files for problem descriptions.
"""

from sqlalchemy.orm import Session
import models

# Each entry: slug → (title, category, difficulty, description)
PROBLEM_METADATA: dict[str, tuple[str, str, str, str]] = {
    # ── Arrays ──────────────────────────────────────────────────────────────
    "two_sum": (
        "Two Sum", "Arrays", "Easy",
        "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume exactly one solution exists, and you may not use the same element twice.",
    ),
    "best_time_to_buy_stock": (
        "Best Time to Buy and Sell Stock", "Arrays", "Easy",
        "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy and a single day to sell. Return the maximum profit you can achieve. If no profit is possible, return 0.",
    ),
    "maximum_subarray": (
        "Maximum Subarray", "Arrays", "Medium",
        "Given an integer array nums, find the subarray with the largest sum, and return its sum. The subarray must contain at least one element.",
    ),
    "product_except_self": (
        "Product of Array Except Self", "Arrays", "Medium",
        "Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i]. You must solve it in O(n) time without using the division operation.",
    ),
    "container_with_most_water": (
        "Container With Most Water", "Arrays", "Medium",
        "You are given an integer array height of length n. Find two lines that together with the x-axis form a container that contains the most water. Return the maximum amount of water a container can store.",
    ),
    # ── Sliding Window ───────────────────────────────────────────────────────
    "longest_substring_without_repeating": (
        "Longest Substring Without Repeating Characters", "Sliding Window", "Medium",
        "Given a string s, find the length of the longest substring without duplicate characters.",
    ),
    "minimum_window_substring": (
        "Minimum Window Substring", "Sliding Window", "Hard",
        "Given two strings s and t, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If no such window exists, return an empty string.",
    ),
    # ── Two Pointers ─────────────────────────────────────────────────────────
    "three_sum": (
        "3Sum", "Two Pointers", "Medium",
        "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i, j, and k are distinct and nums[i] + nums[j] + nums[k] == 0. The solution set must not contain duplicate triplets.",
    ),
    "trapping_rain_water": (
        "Trapping Rain Water", "Two Pointers", "Hard",
        "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
    ),
    # ── Binary Search ─────────────────────────────────────────────────────────
    "search_rotated_sorted_array": (
        "Search in Rotated Sorted Array", "Binary Search", "Medium",
        "Given a rotated sorted array nums of unique elements and an integer target, return the index of target if it is in nums, or -1 if it is not.",
    ),
    "find_min_rotated_array": (
        "Find Minimum in Rotated Sorted Array", "Binary Search", "Medium",
        "Given the sorted rotated array nums of unique elements, return the minimum element of this array. You must write an algorithm that runs in O(log n) time.",
    ),
    # ── Linked Lists ──────────────────────────────────────────────────────────
    "reverse_linked_list": (
        "Reverse Linked List", "Linked Lists", "Easy",
        "Given the head of a singly linked list, reverse the list, and return the reversed list.",
    ),
    "merge_two_sorted_lists": (
        "Merge Two Sorted Lists", "Linked Lists", "Easy",
        "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.",
    ),
    "detect_cycle": (
        "Linked List Cycle", "Linked Lists", "Easy",
        "Given head, the head of a linked list, determine if the linked list has a cycle in it. Return true if there is a cycle, otherwise return false.",
    ),
    # ── Trees ────────────────────────────────────────────────────────────────
    "inorder_traversal": (
        "Binary Tree Inorder Traversal", "Trees", "Easy",
        "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
    ),
    "max_depth_binary_tree": (
        "Maximum Depth of Binary Tree", "Trees", "Easy",
        "Given the root of a binary tree, return its maximum depth. The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.",
    ),
    "validate_bst": (
        "Validate Binary Search Tree", "Trees", "Medium",
        "Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST has every left node strictly less and every right node strictly greater than the current node, recursively.",
    ),
    "lowest_common_ancestor": (
        "Lowest Common Ancestor of a BST", "Trees", "Medium",
        "Given a binary search tree, find the lowest common ancestor (LCA) node of two given nodes p and q in the BST.",
    ),
    # ── Graphs ────────────────────────────────────────────────────────────────
    "number_of_islands": (
        "Number of Islands", "Graphs", "Medium",
        "Given an m x n 2D binary grid representing a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
    ),
    "clone_graph": (
        "Clone Graph", "Graphs", "Medium",
        "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.",
    ),
    "course_schedule": (
        "Course Schedule", "Graphs", "Medium",
        "There are numCourses courses labeled from 0 to numCourses-1. Given prerequisites pairs, return true if you can finish all courses (i.e., no cycle exists in the dependency graph).",
    ),
    # ── Dynamic Programming ───────────────────────────────────────────────────
    "climbing_stairs": (
        "Climbing Stairs", "Dynamic Programming", "Easy",
        "You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?",
    ),
    "house_robber": (
        "House Robber", "Dynamic Programming", "Medium",
        "You are a robber. You cannot rob two adjacent houses. Given an integer array nums representing the amount of money in each house, return the maximum amount you can rob tonight.",
    ),
    "coin_change": (
        "Coin Change", "Dynamic Programming", "Medium",
        "You are given an integer array coins representing coins of various denominations and an integer amount. Return the fewest number of coins needed to make up that amount, or -1 if it is not possible.",
    ),
    "longest_common_subsequence": (
        "Longest Common Subsequence", "Dynamic Programming", "Medium",
        "Given two strings text1 and text2, return the length of their longest common subsequence. A subsequence is a sequence derived from another string by deleting some characters without changing the order.",
    ),
    # ── Tries ─────────────────────────────────────────────────────────────────
    "implement_trie": (
        "Implement Trie (Prefix Tree)", "Tries", "Medium",
        "Implement a Trie class with insert(word), search(word), and startsWith(prefix) methods.",
    ),
    # ── Heaps ─────────────────────────────────────────────────────────────────
    "kth_largest_element": (
        "Kth Largest Element in an Array", "Heaps", "Medium",
        "Given an integer array nums and an integer k, return the kth largest element in the array. Note that it is the kth largest element in sorted order, not the kth distinct element.",
    ),
}


def seed_problems(db: Session) -> None:
    """
    Insert all problems from PROBLEM_METADATA into the DB.
    Idempotent: skips problems that already exist (checked by slug).
    Called once at app startup.
    """
    inserted = 0
    for slug, (title, category, difficulty, description) in PROBLEM_METADATA.items():
        existing = db.query(models.Problem).filter(models.Problem.slug == slug).first()
        if not existing:
            db.add(models.Problem(
                slug=slug,
                title=title,
                category=category,
                difficulty=difficulty,
                description=description,
            ))
            inserted += 1

    if inserted > 0:
        db.commit()
        print(f"[OK] Seeded {inserted} new problems into the database")
    else:
        print("[OK] Database already seeded -- no new problems to add")
