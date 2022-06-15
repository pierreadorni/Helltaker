from state_space_search.types import Action, State, Map, Position
from typing import Tuple, Callable


def left(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Returns the position to the left of the given position"""
    return pos[0] - 1, pos[1]


def right(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Returns the position to the right of the given position"""
    return pos[0] + 1, pos[1]


def top(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Returns the top position of the given position"""
    return pos[0], pos[1] - 1


def bottom(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Returns the bottom position of the given position"""
    return pos[0], pos[1] + 1


def check_for_key(state: State) -> State:
    """Check if the hero has the key"""
    if state.key == state.hero:
        return State(
            hero=state.hero,
            key=(-1, -1),
            lock=state.lock,
            depth=state.depth,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )
    return state


def check_for_spike_factory(_map: Map) -> Callable[[State], State]:
    """
    Create a function that checks if the hero is on a spike and if so, adds one to depth
    """

    def check_for_spike(state: State, _map: Map) -> State:
        """Check if the hero is on a spike"""
        if state.hero in _map.spikes:
            return State(
                hero=state.hero,
                key=state.key,
                lock=state.lock,
                depth=state.depth + 1,
                open_traps=state.open_traps,
                closed_traps=state.closed_traps,
                boxes=state.boxes,
                mobs=state.mobs,
            )
        return state

    return lambda s: check_for_spike(s, _map)


def check_for_kills_factory(_map):
    """Create a function that checks if a mob is killed on the given state"""

    def check_for_kills(state: State, _map: Map) -> State:
        """Check if a mob is killed"""
        mobs = list(state.mobs)
        for mob in state.mobs:
            if (
                mob in _map.walls
                or mob in state.boxes
                or mob in state.open_traps
                or mob in _map.spikes
                or state.mobs.count(mob) > 1
            ) and mob in mobs:
                mobs.remove(mob)

        return State(
            hero=state.hero,
            key=state.key,
            lock=state.lock,
            depth=state.depth,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=tuple(mobs),
        )

    return lambda s: check_for_kills(s, _map)


def switch_traps(state: State) -> State:
    """Switch the traps"""
    return State(
        hero=state.hero,
        key=state.key,
        lock=state.lock,
        depth=state.depth,
        open_traps=state.closed_traps,
        closed_traps=state.open_traps,
        boxes=state.boxes,
        mobs=state.mobs,
    )


def check_for_trap(state: State) -> State:
    """Check if the hero is on an open trap, if so, add one to depth"""
    if state.hero in state.open_traps:
        return State(
            hero=state.hero,
            key=state.key,
            lock=state.lock,
            depth=state.depth + 1,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )
    return state


def move_factory(_map: Map, direction: Callable[[Position], Position]) -> Action:
    """Create an action that moves the hero one step in the given direction"""

    def move(state: State) -> State:
        """Move the hero one step in the given direction"""
        return State(
            hero=direction(state.hero),
            key=state.key,
            lock=state.lock,
            depth=state.depth + 1,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )

    check_for_spike = check_for_spike_factory(_map)
    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: direction(s.hero) not in _map.walls,
                lambda s: direction(s.hero) not in s.boxes,
                lambda s: direction(s.hero) not in s.mobs,
                lambda s: direction(s.hero) != s.lock,
            ]
        ),
        effects=(
            move,
            check_for_key,
            check_for_spike,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ),
    )


def push_factory(_map: Map, direction: Callable[[Position], Position]) -> Action:
    """Create an action that pushes the box the given direction"""

    def push(state: State) -> State:
        """Push the box the given direction"""
        boxes = [b for b in state.boxes if not b == direction(state.hero)] + [
            direction(direction(state.hero))
        ]
        return State(
            hero=state.hero,
            key=state.key,
            lock=state.lock,
            depth=state.depth + 1,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=tuple(boxes),
            mobs=state.mobs,
        )

    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: direction(s.hero) in s.boxes,
                lambda s: direction(direction(s.hero)) not in _map.walls,
                lambda s: direction(direction(s.hero)) not in _map.demons,
                lambda s: direction(direction(s.hero)) not in s.mobs,
                lambda s: direction(direction(s.hero)) not in s.boxes,
                lambda s: direction(direction(s.hero)) != s.lock,
            ]
        ),
        effects=(
            push,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ),
    )


def wait(state: State) -> State:
    """Do nothing"""
    return State(
        hero=state.hero,
        key=state.key,
        lock=state.lock,
        depth=state.depth + 1,
        open_traps=state.open_traps,
        closed_traps=state.closed_traps,
        boxes=state.boxes,
        mobs=state.mobs,
    )


def wait_factory(_map: Map, direction: Callable[[Position], Position]) -> Action:
    """Create actions that do nothing by pushing a stuck box around the hero"""

    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: (
                    direction(s.hero) in s.boxes
                    and direction(direction(s.hero)) in s.boxes
                )
                or (
                    direction(s.hero) in s.boxes
                    and direction(direction(s.hero)) in _map.walls
                )
                or (
                    direction(s.hero) in s.boxes
                    and direction(direction(s.hero)) == s.lock
                )
            ]
        ),
        effects=(
            wait,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ),
    )


def push_mob_factory(_map: Map, direction: Callable[[Position], Position]) -> Action:
    """Creates an Action that pushes a mob the given direction"""

    def push_mob(state: State) -> State:
        """Push the mob a given direction"""
        mobs = [m for m in state.mobs if not m == direction(state.hero)] + [
            direction(direction(state.hero))
        ]
        return State(
            hero=state.hero,
            key=state.key,
            lock=state.lock,
            depth=state.depth + 1,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=tuple(mobs),
        )

    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: direction(s.hero) in s.mobs,
            ],
        ),
        effects=(
            push_mob,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ),
    )


def open_lock_factory(_map: Map, direction: Callable[[Position], Position]) -> Action:
    """Creates an Action that opens a lock next to the hero"""

    def open_lock(state: State) -> State:
        """Open the lock"""
        return State(
            hero=direction(state.hero),
            key=state.key,
            lock=(-1, -1),
            depth=state.depth + 1,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )

    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: s.lock == direction(s.hero),
                lambda s: s.key == (-1, -1),
            ],
        ),
        effects=[
            open_lock,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )
