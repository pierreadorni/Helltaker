""" Helltaker Solver """
import heapq
from typing import List, Dict, Callable, Tuple
from collections import deque
from state_space_search.types import State, Map, Position, Action
from state_space_search.actions import (
    move_factory,
    push_factory,
    push_mob_factory,
    wait_factory,
    open_lock_factory,
    top,
    left,
    bottom,
    right,
)
from state_space_search.utils import is_final, is_valid, create_actions


class PrecondNotMetException(Exception):
    """Exception raised when a precondition is not met"""


class NoSolutionException(Exception):
    """Exception raised when no solution is found"""


def standardize_depth(state: State) -> State:
    """Standardizes depth to a value of 0 for storing in visited states set during search"""
    return State(
        hero=state.hero,
        key=state.key,
        lock=state.lock,
        depth=0,
        open_traps=state.open_traps,
        closed_traps=state.closed_traps,
        boxes=state.boxes,
        mobs=state.mobs,
    )


helltaker_actions_factories = {
    "move": move_factory,
    "push": push_factory,
    "push_mob": push_mob_factory,
    "wait": wait_factory,
    "open_lock": open_lock_factory,
}

helltaker_directions = {"top": top, "bottom": bottom, "left": left, "right": right}


def execute(state: State, action: Action) -> State:
    """Execute an action on a state, returns the new state"""
    for precondition in action.preconditions:
        if not precondition(state):
            raise PrecondNotMetException("Precondition not met")

    for effect in action.effects:
        state = effect(state)

    return state


def rebuild_path(
    previous_dict: Dict[State, Tuple[State, str]], final_state: State
) -> List[str]:
    """Rebuild the path from a dictionary of previous states"""
    path = [final_state]
    actions = []
    while final_state in previous_dict:
        actions.append(previous_dict[final_state][1])
        final_state = previous_dict[final_state][0]
        path.append(final_state)
    return actions[::-1]


def solve(
    state: State,
    map_: Map,
    actions_factories: Dict[
        str, Callable[[Map, Callable[[Position], Position]], Action]
    ],
    directions: Dict[str, Callable[[Position], Position]] = helltaker_directions,
) -> List[str]:
    """Solve the puzzle using a breadth first search"""
    actions = create_actions(actions_factories, map_, directions)
    queue = deque([state])
    visited = set()
    previous_dict = {}
    current_state = state
    while queue:
        current_state = queue.popleft()
        if is_final(current_state, map_):
            break
        for name, action in actions.items():
            try:
                new_state = execute(current_state, action)
                std_new_state = standardize_depth(new_state)
            except PrecondNotMetException:
                continue
            if std_new_state not in visited and new_state.depth <= map_.max_depth:
                previous_dict[new_state] = (current_state, name)
                queue.append(new_state)
                visited.add(std_new_state)
    if not is_final(current_state, map_):
        raise NoSolutionException(f"No solution found in {map_.max_depth} actions.")

    return rebuild_path(previous_dict, current_state)


def basic_manhattan_distance(map_: Map, state: State) -> int:
    """Compute the basic Manhattan distance between the hero and the closest Demon"""
    demons = map_.demons
    hero = state.hero
    distances = [abs(demon[0] - hero[0]) + abs(demon[1] - hero[1]) for demon in demons]
    return min(distances) + state.depth - 5 * (state.key == (-1, -1))


def solve_a_star(
    state: State,
    map_: Map,
    actions_factories: Dict[str, Callable[[Map], Callable]],
    directions: Dict[str, Callable[[Position], Position]] = helltaker_directions,
    heuristic: Callable[[Map, State], int] = basic_manhattan_distance,
) -> List[str]:
    """Solve the puzzle using an A* search algorithm"""
    actions = create_actions(actions_factories, map_, directions)
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap, (heuristic(map_, state), state))
    visited = set()
    previous_dict = {}
    current_state = state
    while heap:
        _, current_state = heapq.heappop(heap)
        if is_final(current_state, map_) and current_state.depth <= map_.max_depth:
            break
        for name, action in actions.items():
            try:
                new_state = execute(current_state, action)
                std_new_state = standardize_depth(new_state)
            except PrecondNotMetException:
                continue
            if std_new_state not in visited and new_state.depth <= map_.max_depth:
                previous_dict[new_state] = (current_state, name)
                visited.add(std_new_state)
                heapq.heappush(heap, (heuristic(map_, new_state), new_state))
    if not is_final(current_state, map_):
        raise NoSolutionException(f"No solution found in {map_.max_depth} actions.")

    return rebuild_path(previous_dict, current_state)
