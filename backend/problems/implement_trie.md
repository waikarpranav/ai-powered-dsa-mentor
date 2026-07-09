# Implement Trie (Prefix Tree)

## Problem Statement
Implement a Trie class with three operations:
- `insert(word)` — Inserts a string into the trie.
- `search(word)` — Returns `true` if the word is in the trie (exact match).
- `startsWith(prefix)` — Returns `true` if any word in the trie has the given prefix.

## Optimal Approach
**Array-based TrieNode** | Time: O(L) per operation | Space: O(26 × L × N)

Each `TrieNode` has an array of 26 children (one per lowercase letter) and an `isEnd` flag marking end of a word.

```java
// Java — Optimal Implementation
class Trie {
    private TrieNode root;

    public Trie() {
        root = new TrieNode();
    }

    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) {
                curr.children[idx] = new TrieNode();
            }
            curr = curr.children[idx];
        }
        curr.isEnd = true;   // Mark end of word
    }

    public boolean search(String word) {
        TrieNode node = traverse(word);
        return node != null && node.isEnd;  // Must reach end AND be marked
    }

    public boolean startsWith(String prefix) {
        return traverse(prefix) != null;    // Just need to reach the end of prefix
    }

    private TrieNode traverse(String s) {
        TrieNode curr = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return null;
            curr = curr.children[idx];
        }
        return curr;
    }
}

class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEnd = false;
}
```

```python
# Python — Optimal Implementation
class TrieNode:
    def __init__(self):
        self.children = {}    # Dict is fine for Python (no fixed 26-array needed)
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word):
        node = self._traverse(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._traverse(prefix) is not None

    def _traverse(self, s):
        curr = self.root
        for c in s:
            if c not in curr.children:
                return None
            curr = curr.children[c]
        return curr
```

## Common Edge Cases
- **`search` vs `startsWith` distinction**: `search("app")` returns `false` if only `"apple"` was inserted — the node for `p` exists but `isEnd = false`. `startsWith("app")` returns `true` because the prefix exists.
- **Inserting a prefix of an existing word**: e.g., insert "apple" then insert "app". Both words coexist — `app`'s node has `isEnd = true`, `apple`'s last `e` also has `isEnd = true`.
- **`search` for a word whose prefix exists but word doesn't**: Must check `isEnd`, not just that traversal completes.
- **Empty string**: `insert("")` → sets `root.isEnd = true`. `search("")` → `root.isEnd = true`. Rarely tested but good to know.

## Why a Trie vs a HashSet?
- HashSet: O(1) exact search, but O(L × N) space and NO prefix support
- Trie: O(L) exact search, O(L × N) space, and O(L) prefix search
- Use Trie when you need prefix queries. Use HashSet when you only need exact lookups.

## Key Concepts Tested
- TrieNode structure: array of 26 children + isEnd flag
- `c - 'a'` trick to map character to array index (Java)
- `search` requires `isEnd = true`; `startsWith` only requires successful traversal
- Refactoring: extract common traversal logic into a helper (shows clean code thinking)
- Space complexity: O(26 × average_word_length × number_of_words)

## Verdict Guide
| Approach | Verdict |
|---|---|
| Array[26] based TrieNode O(L)/O(26LN) | **Optimal** |
| HashMap based TrieNode O(L)/O(LN) | **Optimal** (slightly more space-efficient for sparse alphabets) |
| No `isEnd` flag (search and startsWith behave identically) | **Incorrect** |
| HashSet for search + no prefix support | **Incorrect** (doesn't implement Trie) |
