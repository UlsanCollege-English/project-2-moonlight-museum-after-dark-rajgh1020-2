"""Project 2 starter code: Moonlight Museum After Dark.

Students should implement all required behavior in this file.
Use stdlib only.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass(frozen=True)
class Artifact:
    """A museum artifact stored in the archive BST."""

    artifact_id: int
    name: str
    category: str
    age: int
    room: str


@dataclass(frozen=True)
class RestorationRequest:
    """A request to inspect or repair an artifact."""

    artifact_id: int
    description: str


class TreeNode:
    """A node for the artifact BST."""

    def __init__(
        self,
        artifact: Artifact,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.artifact = artifact
        self.left = left
        self.right = right


class ArtifactBST:
    """Binary search tree keyed by artifact_id."""

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, artifact: Artifact) -> bool:
        """Insert an artifact.

        Return True if the artifact was inserted.
        Return False if an artifact with the same ID already exists.
        """
        if self.root is None:
            self.root = TreeNode(artifact)
            return True
        return self._insert(self.root, artifact)

    def _insert(self, node: TreeNode, artifact: Artifact) -> bool:
        if artifact.artifact_id == node.artifact.artifact_id:
            return False
        if artifact.artifact_id < node.artifact.artifact_id:
            if node.left is None:
                node.left = TreeNode(artifact)
                return True
            return self._insert(node.left, artifact)
        else:
            if node.right is None:
                node.right = TreeNode(artifact)
                return True
            return self._insert(node.right, artifact)

    def search_by_id(self, artifact_id: int) -> Artifact | None:
        """Return the matching artifact, or None if it does not exist."""
        return self._search(self.root, artifact_id)

    def _search(self, node: TreeNode | None, artifact_id: int) -> Artifact | None:
        if node is None:
            return None
        if artifact_id == node.artifact.artifact_id:
            return node.artifact
        if artifact_id < node.artifact.artifact_id:
            return self._search(node.left, artifact_id)
        return self._search(node.right, artifact_id)

    def inorder_ids(self) -> list[int]:
        """Return a list of artifact IDs using inorder traversal."""
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.artifact.artifact_id)
        self._inorder(node.right, result)

    def preorder_ids(self) -> list[int]:
        """Return a list of artifact IDs using preorder traversal."""
        result: list[int] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        result.append(node.artifact.artifact_id)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def postorder_ids(self) -> list[int]:
        """Return a list of artifact IDs using postorder traversal."""
        result: list[int] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.artifact.artifact_id)


class RestorationQueue:
    """FIFO queue of restoration requests."""

    def __init__(self) -> None:
        self._items: Deque[RestorationRequest] = deque()

    def add_request(self, request: RestorationRequest) -> None:
        """Add a request to the back of the queue."""
        self._items.append(request)

    def process_next_request(self) -> RestorationRequest | None:
        """Remove and return the next request, or None if the queue is empty."""
        if not self._items:
            return None
        return self._items.popleft()

    def peek_next_request(self) -> RestorationRequest | None:
        """Return the next request without removing it, or None if empty."""
        if not self._items:
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue has no requests."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of queued requests."""
        return len(self._items)


class ArchiveUndoStack:
    """LIFO stack of recent archive actions."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push_action(self, action: str) -> None:
        """Push an action onto the stack."""
        self._items.append(action)

    def undo_last_action(self) -> str | None:
        """Remove and return the most recent action, or None if empty."""
        if not self._items:
            return None
        return self._items.pop()

    def peek_last_action(self) -> str | None:
        """Return the most recent action without removing it, or None if empty."""
        if not self._items:
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no actions."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of stored actions."""
        return len(self._items)


class ExhibitNode:
    """A node in the singly linked exhibit route."""

    def __init__(self, stop_name: str, next_node: ExhibitNode | None = None) -> None:
        self.stop_name = stop_name
        self.next = next_node


class ExhibitRoute:
    """Singly linked list of exhibit stops."""

    def __init__(self) -> None:
        self.head: ExhibitNode | None = None

    def add_stop(self, stop_name: str) -> None:
        """Add a stop to the end of the route."""
        new_node = ExhibitNode(stop_name)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def remove_stop(self, stop_name: str) -> bool:
        """Remove the first matching stop.

        Return True if a stop was removed.
        Return False if the stop does not exist.
        """
        if self.head is None:
            return False
        if self.head.stop_name == stop_name:
            self.head = self.head.next
            return True
        current = self.head
        while current.next is not None:
            if current.next.stop_name == stop_name:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def list_stops(self) -> list[str]:
        """Return the route as a list of stop names in order."""
        stops = []
        current = self.head
        while current is not None:
            stops.append(current.stop_name)
            current = current.next
        return stops

    def count_stops(self) -> int:
        """Return the number of stops in the route."""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count


def count_artifacts_by_category(artifacts: list[Artifact]) -> dict[str, int]:
    """Return a dictionary counting artifacts in each category."""
    counts: dict[str, int] = {}
    for artifact in artifacts:
        counts[artifact.category] = counts.get(artifact.category, 0) + 1
    return counts


def unique_rooms(artifacts: list[Artifact]) -> set[str]:
    """Return a set of all rooms used by the given artifacts."""
    return {artifact.room for artifact in artifacts}


def sort_artifacts_by_age(
    artifacts: list[Artifact],
    descending: bool = False,
) -> list[Artifact]:
    """Return a new list of artifacts sorted by age.

    If descending is False, sort from youngest to oldest.
    If descending is True, sort from oldest to youngest.
    """
    return sorted(artifacts, key=lambda a: a.age, reverse=descending)


def linear_search_by_name(
    artifacts: list[Artifact],
    name: str,
) -> Artifact | None:
    """Return the first artifact with an exact matching name, or None."""
    for artifact in artifacts:
        if artifact.name == name:
            return artifact
    return None


def demo_museum_night() -> None:
    """Run a small integration demo showing the system working together."""
    print("=== Moonlight Museum After Dark ===\n")

    artifacts = [
        Artifact(5,  "Cursed Mirror",      "Cursed",       400, "Hall of Shadows"),
        Artifact(3,  "Clockwork Bird",     "Mechanical",   120, "Gear Room"),
        Artifact(7,  "Whispering Map",     "Enchanted",    250, "Map Vault"),
        Artifact(1,  "Glowing Key",        "Enchanted",     80, "Key Chamber"),
        Artifact(9,  "Phantom Lantern",    "Cursed",       310, "Hall of Shadows"),
        Artifact(4,  "Ivory Compass",      "Navigational", 190, "Map Vault"),
        Artifact(6,  "Bronze Sundial",     "Mechanical",   500, "Gear Room"),
        Artifact(2,  "Silk Star Chart",    "Navigational",  60, "Map Vault"),
        Artifact(8,  "Frozen Hourglass",   "Cursed",       730, "Time Tower"),
    ]

    # --- BST ---
    bst = ArtifactBST()
    for a in artifacts:
        bst.insert(a)

    print("Inorder IDs (sorted):", bst.inorder_ids())
    print("Preorder IDs:        ", bst.preorder_ids())
    print("Postorder IDs:       ", bst.postorder_ids())

    found = bst.search_by_id(7)
    print(f"\nSearch ID 7:  {found.name if found else 'Not found'}")
    print(f"Search ID 99: {bst.search_by_id(99)}")
    print(f"Duplicate insert ID 5: {bst.insert(Artifact(5, 'Fake', 'Cursed', 1, 'Nowhere'))}")

    # --- Restoration queue (FIFO) ---
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(8, "Clean frost damage"))
    queue.add_request(RestorationRequest(1, "Polish surface"))
    queue.add_request(RestorationRequest(3, "Oil gears"))

    print(f"\nQueue size: {queue.size()}")
    print(f"Peek:       {queue.peek_next_request().description}")
    print(f"Processed:  {queue.process_next_request().description}")
    print(f"Processed:  {queue.process_next_request().description}")
    print(f"Queue size after processing: {queue.size()}")

    # --- Undo stack (LIFO) ---
    stack = ArchiveUndoStack()
    stack.push_action("Inserted Cursed Mirror")
    stack.push_action("Inserted Clockwork Bird")
    stack.push_action("Moved Phantom Lantern to storage")

    print(f"\nStack size: {stack.size()}")
    print(f"Peek: {stack.peek_last_action()}")
    print(f"Undo: {stack.undo_last_action()}")
    print(f"Undo: {stack.undo_last_action()}")
    print(f"Stack size after undo: {stack.size()}")

    # --- Exhibit route ---
    route = ExhibitRoute()
    for stop in ["Entrance", "Key Chamber", "Gear Room", "Map Vault", "Hall of Shadows", "Time Tower"]:
        route.add_stop(stop)

    print(f"\nFull route:              {route.list_stops()}")
    print(f"Stop count:              {route.count_stops()}")
    route.remove_stop("Gear Room")
    print(f"After removing Gear Room: {route.list_stops()}")

    # --- Reports ---
    print(f"\nCategory counts: {count_artifacts_by_category(artifacts)}")
    print(f"Unique rooms:    {unique_rooms(artifacts)}")

    sorted_asc = sort_artifacts_by_age(artifacts)
    sorted_desc = sort_artifacts_by_age(artifacts, descending=True)
    print(f"\nYoungest: {sorted_asc[0].name} ({sorted_asc[0].age} yrs)")
    print(f"Oldest:   {sorted_desc[0].name} ({sorted_desc[0].age} yrs)")

    found_by_name = linear_search_by_name(artifacts, "Ivory Compass")
    print(f"\nSearch 'Ivory Compass': {found_by_name.name if found_by_name else 'Not found'}")
    print(f"Search 'Dragon Skull':  {linear_search_by_name(artifacts, 'Dragon Skull')}")

    print("\n=== Demo complete ===")


if __name__ == "__main__":
    demo_museum_night()