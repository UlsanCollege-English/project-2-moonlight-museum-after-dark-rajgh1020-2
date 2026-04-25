[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tfm_-hwX)
# Project 2: Moonlight Museum After Dark

## Team information
- Team name: Solo submission
- Members: Raj
- Repository name: project2-moonlight-museum

---

## Project summary
This project builds a museum management system for organizing strange artifacts during a secret late-night exhibition. It uses five different data structures — a BST, queue, stack, singly linked list, and utility functions — each chosen to match a specific real-world need in the museum. Artifacts can be inserted and searched by ID, restoration requests are processed in order, archive mistakes can be undone, and a guided exhibit route can be built and modified. A demo function ties all parts together to show the system working end to end.

---

## Feature checklist
Mark each item when it is working.

### Core structures
- [x] `Artifact` class/record
- [x] `ArtifactBST`
- [x] `RestorationQueue`
- [x] `ArchiveUndoStack`
- [x] `ExhibitRoute` singly linked list

### BST features
- [x] insert artifact
- [x] search by ID
- [x] preorder traversal
- [x] inorder traversal
- [x] postorder traversal
- [x] duplicate IDs ignored

### Queue features
- [x] add request
- [x] process next request
- [x] peek next request
- [x] empty check
- [x] size

### Stack features
- [x] push action
- [x] undo last action
- [x] peek last action
- [x] empty check
- [x] size

### Linked list features
- [x] add stop to end
- [x] remove first matching stop
- [x] list stops in order
- [x] count stops

### Utility/report features
- [x] category counts
- [x] unique rooms
- [x] sort by age
- [x] linear search by name

### Integration
- [x] `demo_museum_night()`
- [x] at least 8 artifacts in demo
- [x] demo shows system parts working together

---

## Design note (150-250 words)
The core of the system is the `ArtifactBST`, which stores artifacts keyed by `artifact_id`. A BST is the right choice here because artifact IDs are unique integers, which means every insert naturally goes left or right with no ambiguity. Searching is O(h) rather than O(n), which is a meaningful improvement over a plain list as the archive grows. Duplicate IDs are silently ignored and return `False` to keep the archive clean without crashing.

Restoration requests use a `RestorationQueue` backed by `collections.deque`. A queue enforces FIFO order, which mirrors how real repair workflows operate — the request that came in first should be handled first. `deque` makes both enqueue and dequeue O(1), which a plain list cannot guarantee for front removals.

The `ArchiveUndoStack` uses a Python list, which is the natural fit for LIFO behavior. Every `append` is a push and every `pop` is an undo — both O(1). This maps directly to the idea of reversing the most recent mistake first.

The `ExhibitRoute` is a singly linked list because a guided tour is inherently sequential. Stops are visited in order, new stops are added to the end, and any stop along the route can be removed by name. A linked list handles these operations cleanly without shifting elements like a list would on mid-removal.

Utility functions are kept as standalone functions rather than methods because they operate on plain lists of artifacts and don't depend on any internal state.

---

## Complexity reasoning

- `ArtifactBST.insert`: O(h) where h is the tree height, because each recursive call moves one level down following the BST property until an empty slot is found.
- `ArtifactBST.search_by_id`: O(h) where h is the tree height, because the search follows exactly one root-to-leaf path based on ID comparisons.
- `ArtifactBST.inorder_ids`: O(n) where n is the number of nodes, because every node is visited exactly once during the traversal.
- `RestorationQueue.process_next_request`: O(1) because `deque.popleft()` removes from the front in constant time.
- `ArchiveUndoStack.undo_last_action`: O(1) because `list.pop()` removes from the end in constant time.
- `ExhibitRoute.remove_stop`: O(n) where n is the number of stops, because in the worst case the target stop is at the end and the whole list must be traversed to find it.
- `sort_artifacts_by_age`: O(n log n) because it uses Python's built-in `sorted()`, which uses Timsort.
- `linear_search_by_name`: O(n) where n is the number of artifacts, because in the worst case the target name is at the end or missing and every artifact is checked.

---

## Edge-case checklist

### BST
- [x] insert into empty tree — handled by checking `self.root is None` first and creating the root node directly
- [x] search for missing ID — recursive search returns `None` when it reaches a null node
- [x] empty traversals — all three traversal helpers return immediately when `node is None`, so an empty tree returns `[]`
- [x] duplicate ID — compared in `_insert` before going left or right; returns `False` without modifying the tree

### Queue
- [x] process empty queue — `process_next_request` checks `if not self._items` and returns `None`
- [x] peek empty queue — `peek_next_request` checks `if not self._items` and returns `None`

### Stack
- [x] undo empty stack — `undo_last_action` checks `if not self._items` and returns `None`
- [x] peek empty stack — `peek_last_action` checks `if not self._items` and returns `None`

### Exhibit route linked list
- [x] empty route — `list_stops` and `count_stops` both return `[]` / `0` when `self.head is None`
- [x] remove missing stop — walk reaches the end without a match and returns `False`
- [x] remove first stop — handled as a special case by reassigning `self.head = self.head.next`
- [x] remove middle stop — trailing pointer skips the target node by linking `current.next = current.next.next`
- [x] remove last stop — same trailing pointer logic; last node's `next` is `None` after removal
- [x] one-stop route — covered by the head special case; after removal `self.head` is `None`

### Reports
- [x] empty artifact list — all four functions return `{}`, `set()`, `[]`, or `None` respectively on empty input
- [x] repeated categories — `count_artifacts_by_category` uses `dict.get(..., 0) + 1` to accumulate counts correctly
- [x] repeated rooms — `unique_rooms` uses a set comprehension so duplicates are automatically collapsed
- [x] missing artifact name — `linear_search_by_name` returns `None` after checking every artifact without a match
- [x] same-age artifacts — `sort_artifacts_by_age` uses `sorted()` which is stable, so equal-age artifacts keep their relative input order

---

## Demo plan / how to run

Install dependencies (none beyond stdlib) and run tests:

```bash
pytest -q
```

Run just the demo to see all parts of the system working together:

```bash
python -c "from src.project import demo_museum_night; demo_museum_night()"
```

Run extra edge case tests if present:

```bash
pytest tests/test_project_extra.py -v
```

Run everything with verbose output:

```bash
pytest tests/ -v
```

---

## Assistance & sources
This section is required.

- AI used? Y
- What it helped with: Debugging a failing test where the demo printed `"Peek:"` but the test checked for `"Next restoration request:"`. Also helped structure the edge case test file and check that all required test categories from the brief were covered.
- Non-course sources used: Python standard library documentation
- Links: https://docs.python.org/3/library/heapq.html, https://docs.python.org/3/library/collections.html#collections.deque