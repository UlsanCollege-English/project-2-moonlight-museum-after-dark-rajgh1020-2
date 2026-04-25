"""Extra edge case tests for Project 2: Moonlight Museum After Dark."""

from __future__ import annotations

import pytest

from src.project import (
    ArchiveUndoStack,
    Artifact,
    ArtifactBST,
    ExhibitRoute,
    RestorationQueue,
    RestorationRequest,
    count_artifacts_by_category,
    linear_search_by_name,
    sort_artifacts_by_age,
    unique_rooms,
)


def make_artifacts() -> list[Artifact]:
    return [
        Artifact(40, "Cursed Mirror",  "mirror",  220, "North Hall"),
        Artifact(20, "Clockwork Bird", "machine",  80, "Workshop"),
        Artifact(60, "Whispering Map", "paper",   140, "Archive"),
        Artifact(10, "Glowing Key",    "metal",    35, "Vault"),
        Artifact(30, "Moon Dial",      "device",  120, "North Hall"),
        Artifact(50, "Silver Mask",    "costume", 160, "Gallery"),
        Artifact(70, "Lantern Jar",    "glass",    60, "Gallery"),
        Artifact(25, "Ink Compass",    "device",  120, "Archive"),
    ]


# ---------------------------------------------------------------------------
# BST edge cases
# ---------------------------------------------------------------------------

def test_bst_single_node_all_traversals() -> None:
    bst = ArtifactBST()
    bst.insert(Artifact(1, "Only One", "metal", 10, "Vault"))
    assert bst.inorder_ids() == [1]
    assert bst.preorder_ids() == [1]
    assert bst.postorder_ids() == [1]


def test_bst_insert_returns_true_for_new_artifact() -> None:
    bst = ArtifactBST()
    assert bst.insert(Artifact(1, "Glowing Key", "metal", 35, "Vault")) is True


def test_bst_insert_duplicate_does_not_overwrite() -> None:
    bst = ArtifactBST()
    original = Artifact(10, "Glowing Key", "metal", 35, "Vault")
    bst.insert(original)
    bst.insert(Artifact(10, "Imposter", "fake", 1, "Nowhere"))
    assert bst.search_by_id(10).name == "Glowing Key"


def test_bst_insert_many_duplicates_all_return_false() -> None:
    bst = ArtifactBST()
    bst.insert(Artifact(5, "A", "x", 1, "room"))
    for _ in range(5):
        assert bst.insert(Artifact(5, "A", "x", 1, "room")) is False


def test_bst_left_skewed_inorder() -> None:
    bst = ArtifactBST()
    for i in [5, 4, 3, 2, 1]:
        bst.insert(Artifact(i, f"item{i}", "x", i, "room"))
    assert bst.inorder_ids() == [1, 2, 3, 4, 5]


def test_bst_right_skewed_inorder() -> None:
    bst = ArtifactBST()
    for i in [1, 2, 3, 4, 5]:
        bst.insert(Artifact(i, f"item{i}", "x", i, "room"))
    assert bst.inorder_ids() == [1, 2, 3, 4, 5]


def test_bst_search_left_subtree() -> None:
    bst = ArtifactBST()
    for a in make_artifacts():
        bst.insert(a)
    found = bst.search_by_id(10)
    assert found is not None
    assert found.name == "Glowing Key"


def test_bst_search_right_subtree() -> None:
    bst = ArtifactBST()
    for a in make_artifacts():
        bst.insert(a)
    found = bst.search_by_id(70)
    assert found is not None
    assert found.name == "Lantern Jar"


def test_bst_search_root() -> None:
    bst = ArtifactBST()
    for a in make_artifacts():
        bst.insert(a)
    found = bst.search_by_id(40)
    assert found is not None
    assert found.name == "Cursed Mirror"


def test_bst_inorder_always_sorted() -> None:
    import random
    ids = list(range(1, 21))
    random.shuffle(ids)
    bst = ArtifactBST()
    for i in ids:
        bst.insert(Artifact(i, f"item{i}", "x", i, "room"))
    assert bst.inorder_ids() == sorted(ids)


# ---------------------------------------------------------------------------
# RestorationQueue edge cases
# ---------------------------------------------------------------------------

def test_queue_peek_does_not_shrink_queue() -> None:
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(1, "Fix A"))
    queue.peek_next_request()
    queue.peek_next_request()
    assert queue.size() == 1


def test_queue_fifo_strict_order() -> None:
    queue = RestorationQueue()
    for i in range(10):
        queue.add_request(RestorationRequest(i, f"task {i}"))
    for i in range(10):
        assert queue.process_next_request().artifact_id == i


def test_queue_is_empty_after_all_processed() -> None:
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(1, "Fix A"))
    queue.add_request(RestorationRequest(2, "Fix B"))
    queue.process_next_request()
    queue.process_next_request()
    assert queue.is_empty() is True
    assert queue.size() == 0


def test_queue_process_returns_none_on_empty_repeatedly() -> None:
    queue = RestorationQueue()
    assert queue.process_next_request() is None
    assert queue.process_next_request() is None


def test_queue_peek_returns_none_on_empty_repeatedly() -> None:
    queue = RestorationQueue()
    assert queue.peek_next_request() is None
    assert queue.peek_next_request() is None


def test_queue_size_tracks_correctly() -> None:
    queue = RestorationQueue()
    for i in range(5):
        queue.add_request(RestorationRequest(i, f"task {i}"))
        assert queue.size() == i + 1
    for i in range(4, -1, -1):
        queue.process_next_request()
        assert queue.size() == i


# ---------------------------------------------------------------------------
# ArchiveUndoStack edge cases
# ---------------------------------------------------------------------------

def test_stack_lifo_strict_order() -> None:
    stack = ArchiveUndoStack()
    for i in range(10):
        stack.push_action(f"action {i}")
    for i in range(9, -1, -1):
        assert stack.undo_last_action() == f"action {i}"


def test_stack_peek_does_not_shrink_stack() -> None:
    stack = ArchiveUndoStack()
    stack.push_action("do something")
    stack.peek_last_action()
    stack.peek_last_action()
    assert stack.size() == 1


def test_stack_is_empty_after_all_undone() -> None:
    stack = ArchiveUndoStack()
    stack.push_action("A")
    stack.push_action("B")
    stack.undo_last_action()
    stack.undo_last_action()
    assert stack.is_empty() is True
    assert stack.size() == 0


def test_stack_undo_returns_none_repeatedly_on_empty() -> None:
    stack = ArchiveUndoStack()
    assert stack.undo_last_action() is None
    assert stack.undo_last_action() is None


def test_stack_peek_returns_none_repeatedly_on_empty() -> None:
    stack = ArchiveUndoStack()
    assert stack.peek_last_action() is None
    assert stack.peek_last_action() is None


def test_stack_size_tracks_correctly() -> None:
    stack = ArchiveUndoStack()
    for i in range(5):
        stack.push_action(f"action {i}")
        assert stack.size() == i + 1
    for i in range(4, -1, -1):
        stack.undo_last_action()
        assert stack.size() == i


# ---------------------------------------------------------------------------
# ExhibitRoute edge cases
# ---------------------------------------------------------------------------

def test_route_count_empty() -> None:
    route = ExhibitRoute()
    assert route.count_stops() == 0


def test_route_remove_nonexistent_from_single_stop() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    assert route.remove_stop("Exit") is False
    assert route.list_stops() == ["Entrance"]


def test_route_remove_only_stop_makes_empty() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    assert route.remove_stop("Entrance") is True
    assert route.list_stops() == []
    assert route.count_stops() == 0


def test_route_add_duplicate_stop_names() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Entrance")
    assert route.count_stops() == 2
    assert route.list_stops() == ["Entrance", "Entrance"]


def test_route_remove_first_of_duplicate_stops() -> None:
    route = ExhibitRoute()
    route.add_stop("A")
    route.add_stop("B")
    route.add_stop("A")
    route.remove_stop("A")
    assert route.list_stops() == ["B", "A"]


def test_route_remove_all_stops_one_by_one() -> None:
    route = ExhibitRoute()
    stops = ["Entrance", "Gallery", "Vault", "Exit"]
    for s in stops:
        route.add_stop(s)
    for s in stops:
        route.remove_stop(s)
    assert route.list_stops() == []
    assert route.count_stops() == 0


def test_route_list_stops_does_not_mutate_route() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Gallery")
    result = route.list_stops()
    result.append("Fake Stop")
    assert route.count_stops() == 2


# ---------------------------------------------------------------------------
# Utility / report edge cases
# ---------------------------------------------------------------------------

def test_category_counts_single_artifact() -> None:
    artifacts = [Artifact(1, "Glowing Key", "metal", 35, "Vault")]
    assert count_artifacts_by_category(artifacts) == {"metal": 1}


def test_category_counts_all_same_category() -> None:
    artifacts = [
        Artifact(1, "A", "cursed", 10, "Room 1"),
        Artifact(2, "B", "cursed", 20, "Room 2"),
        Artifact(3, "C", "cursed", 30, "Room 3"),
    ]
    assert count_artifacts_by_category(artifacts) == {"cursed": 3}


def test_unique_rooms_single_artifact() -> None:
    artifacts = [Artifact(1, "Glowing Key", "metal", 35, "Vault")]
    assert unique_rooms(artifacts) == {"Vault"}


def test_unique_rooms_all_same_room() -> None:
    artifacts = [
        Artifact(1, "A", "x", 10, "Gallery"),
        Artifact(2, "B", "x", 20, "Gallery"),
        Artifact(3, "C", "x", 30, "Gallery"),
    ]
    assert unique_rooms(artifacts) == {"Gallery"}


def test_sort_by_age_single_artifact() -> None:
    artifacts = [Artifact(1, "Glowing Key", "metal", 35, "Vault")]
    assert sort_artifacts_by_age(artifacts) == artifacts


def test_sort_by_age_already_sorted_ascending() -> None:
    artifacts = [
        Artifact(1, "A", "x", 10, "room"),
        Artifact(2, "B", "x", 20, "room"),
        Artifact(3, "C", "x", 30, "room"),
    ]
    assert sort_artifacts_by_age(artifacts) == artifacts


def test_sort_by_age_does_not_mutate_input() -> None:
    artifacts = make_artifacts()
    original_order = [a.artifact_id for a in artifacts]
    sort_artifacts_by_age(artifacts)
    assert [a.artifact_id for a in artifacts] == original_order


def test_sort_by_age_same_age_returns_all() -> None:
    artifacts = [
        Artifact(1, "A", "x", 50, "room"),
        Artifact(2, "B", "x", 50, "room"),
        Artifact(3, "C", "x", 50, "room"),
    ]
    result = sort_artifacts_by_age(artifacts)
    assert len(result) == 3
    assert all(a.age == 50 for a in result)


def test_linear_search_returns_first_match() -> None:
    artifacts = [
        Artifact(1, "Twin Mask", "costume", 100, "Gallery"),
        Artifact(2, "Twin Mask", "costume", 200, "Vault"),
    ]
    found = linear_search_by_name(artifacts, "Twin Mask")
    assert found.artifact_id == 1


def test_linear_search_case_sensitive() -> None:
    artifacts = make_artifacts()
    assert linear_search_by_name(artifacts, "glowing key") is None
    assert linear_search_by_name(artifacts, "GLOWING KEY") is None


def test_linear_search_single_artifact_match() -> None:
    artifacts = [Artifact(1, "Glowing Key", "metal", 35, "Vault")]
    found = linear_search_by_name(artifacts, "Glowing Key")
    assert found is not None
    assert found.artifact_id == 1


def test_linear_search_single_artifact_no_match() -> None:
    artifacts = [Artifact(1, "Glowing Key", "metal", 35, "Vault")]
    assert linear_search_by_name(artifacts, "Cursed Mirror") is None