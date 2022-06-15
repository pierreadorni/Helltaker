""" Helltaker Solver """
import heapq
from typing import NamedTuple, Tuple, Callable, FrozenSet, List, Dict, Optional, Set
from collections import deque
from numpy import array


class PrecondNotMetException(Exception):
    """Exception raised when a precondition is not met"""


class NoSolutionException(Exception):
    """Exception raised when no solution is found"""


Position = Tuple[int, int]
State = NamedTuple(
    "State",
    [
        ("hero", Tuple[int, int]),
        ("key", Optional[Tuple[int, int]]),
        ("lock", Optional[Tuple[int, int]]),
        ("depth", int),
        ("open_traps", Tuple[Tuple[int, int]]),
        ("closed_traps", Tuple[Tuple[int, int]]),
        ("boxes", Tuple[Tuple[int, int]]),
        ("mobs", Tuple[Tuple[int, int]]),
    ],
)
Map = NamedTuple(
    "Map",
    [
        ("walls", FrozenSet[Tuple[int, int]]),
        ("demons", FrozenSet[Tuple[int, int]]),
        ("spikes", FrozenSet[Tuple[int, int]]),
        ("max_depth", int),
    ],
)
Action = NamedTuple(
    "Action",
    [
        ("preconditions", FrozenSet[Callable[[State], bool]]),
        ("effects", List[Callable[[State], State]]),
    ],
)


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


def is_valid(
    map_: Map,
    state: State,
    actions_factories: Dict[str, Callable[[Map], Action]],
    plan: List[str],
) -> bool:
    """Checks if a plan is valid"""
    actions = create_actions(actions_factories, map_)
    for action_name in plan:
        action = actions[action_name]
        for precond in action.preconditions:
            if not precond(state):
                return False
        for effect in action.effects:
            state = effect(state)
    return is_final(state, map_)


def parse_grid(file_dict: dict) -> (Map, State):
    """Parse a grid to a map and a state"""
    grid = file_dict["grid"]
    walls = set()
    demons = set()
    spikes = set()
    boxes = set()
    mobs = set()
    closed_traps = set()
    open_traps = set()
    hero = (-1, -1)
    key = (-1, -1)
    lock = (-1, -1)
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "#":
                walls.add((j, i))
            elif char == "D":
                demons.add((j, i))
            elif char == "H":
                hero = (j, i)
            elif char == "K":
                key = (j, i)
            elif char == "L":
                lock = (j, i)
            elif char == "S":
                spikes.add((j, i))
            elif char == "T":
                closed_traps.add((j, i))
            elif char == "U":
                open_traps.add((j, i))
            elif char == "B":
                boxes.add((j, i))
            elif char == "M":
                mobs.add((j, i))

    return Map(
        walls=frozenset(walls),
        demons=frozenset(demons),
        spikes=frozenset(spikes),
        max_depth=file_dict["max_steps"],
    ), State(
        hero,
        key,
        lock,
        0,
        tuple(open_traps),
        tuple(closed_traps),
        tuple(boxes),
        tuple(mobs),
    )


def state_to_string(_map: Map, state: State) -> str:
    """Print the state"""
    grid = [
        [" " for _ in range(max(wall[1] for wall in _map.walls) + 1)]
        for _ in range(max(wall[0] for wall in _map.walls) + 1)
    ]
    for i, j in _map.walls:
        grid[i][j] = "#"
    for i, j in _map.spikes:
        grid[i][j] = "S"
    for i, j in _map.demons:
        grid[i][j] = "D"
    for i, j in state.open_traps:
        grid[i][j] = "U"
    for i, j in state.closed_traps:
        grid[i][j] = "T"
    for i, j in state.boxes:
        grid[i][j] = "B"
    for i, j in state.mobs:
        grid[i][j] = "M"
    i, j = state.hero
    grid[i][j] = "H"
    if state.key != (-1, -1):
        grid[state.key[0]][state.key[1]] = "K"
    if state.lock != (-1, -1):
        grid[state.key[0]][state.key[1]] = "L"

    return "\n".join(["".join(line) for line in array(grid).transpose()])


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

    def move_top(state: State) -> State:
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
        effects=[
            move_top,
            check_for_key,
            check_for_spike,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_top_factory(_map: Map, direction: Callable[[Position], Position]) -> Action:
    """Create an action that pushes the box the given direction"""

    def push_top(state: State) -> State:
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
        effects=[
            push_top,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_bottom_factory(_map: Map) -> Action:
    """Create an action that pushes the box on bottom of the hero"""

    def push_bottom(state: State) -> State:
        """Push the box on bottom of the hero"""
        boxes = [
            b for b in state.boxes if not b == (state.hero[0], state.hero[1] + 1)
        ] + [(state.hero[0], state.hero[1] + 2)]
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
                lambda s: (s.hero[0], s.hero[1] + 1) in s.boxes,
                lambda s: (s.hero[0], s.hero[1] + 2) not in _map.walls,
                lambda s: (s.hero[0], s.hero[1] + 2) not in _map.demons,
                lambda s: (s.hero[0], s.hero[1] + 2) not in s.mobs,
                lambda s: (s.hero[0], s.hero[1] + 2) not in s.boxes,
                lambda s: (s.hero[0], s.hero[1] + 2) != s.lock,
            ]
        ),
        effects=[
            push_bottom,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_left_factory(_map: Map) -> Action:
    """Create an action that pushes the box on left of the hero"""

    def push_left(state: State) -> State:
        """Push the box on left of the hero"""
        boxes = [
            b for b in state.boxes if not b == (state.hero[0] - 1, state.hero[1])
        ] + [(state.hero[0] - 2, state.hero[1])]
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
                lambda s: (s.hero[0] - 1, s.hero[1]) in s.boxes,
                lambda s: (s.hero[0] - 2, s.hero[1]) not in _map.walls,
                lambda s: (s.hero[0] - 2, s.hero[1]) not in _map.demons,
                lambda s: (s.hero[0] - 2, s.hero[1]) not in s.mobs,
                lambda s: (s.hero[0] - 2, s.hero[1]) not in s.boxes,
                lambda s: (s.hero[0] - 2, s.hero[1]) != s.lock,
            ]
        ),
        effects=[
            push_left,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_right_factory(_map: Map) -> Action:
    """Create an action that pushes the box on right of the hero"""

    def push_right(state: State) -> State:
        """Push the box on right of the hero"""
        boxes = [
            b for b in state.boxes if not b == (state.hero[0] + 1, state.hero[1])
        ] + [(state.hero[0] + 2, state.hero[1])]
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
                lambda s: (s.hero[0] + 1, s.hero[1]) in s.boxes,
                lambda s: (s.hero[0] + 2, s.hero[1]) not in _map.walls,
                lambda s: (s.hero[0] + 2, s.hero[1]) not in _map.demons,
                lambda s: (s.hero[0] + 2, s.hero[1]) not in s.mobs,
                lambda s: (s.hero[0] + 2, s.hero[1]) not in s.boxes,
                lambda s: (s.hero[0] + 2, s.hero[1]) != s.lock,
            ]
        ),
        effects=[
            push_right,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
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


def wait_top_factory(_map: Map) -> Action:
    """Create an action that does nothing by pushing the box on top of the hero"""

    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: (top(s.hero) in s.boxes and top(top(s.hero)) in s.boxes)
                or (top(s.hero) in s.boxes and top(top(s.hero)) in _map.walls)
            ]
        ),
        effects=[
            wait,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def wait_bottom_factory(_map: Map) -> Action:
    """Create an action that does nothing by pushing the box on bottom of the hero"""
    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: (
                    bottom(s.hero) in s.boxes and bottom(bottom(s.hero)) in s.boxes
                )
                or (bottom(s.hero) in s.boxes and bottom(bottom(s.hero)) in _map.walls)
            ]
        ),
        effects=[
            wait,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def wait_left_factory(_map: Map) -> Action:
    """Create an action that does nothing by pushing the box on left of the hero"""
    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: (left(s.hero) in s.boxes and left(left(s.hero)) in s.boxes)
                or (left(s.hero) in s.boxes and left(left(s.hero)) in _map.walls)
            ]
        ),
        effects=[
            wait,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def wait_right_factory(_map: Map) -> Action:
    """Create an action that does nothing by pushing the box on right of the hero"""

    check_for_kills = check_for_kills_factory(_map)

    return Action(
        preconditions=frozenset(
            [
                lambda s: (right(s.hero) in s.boxes and right(right(s.hero)) in s.boxes)
                or (right(s.hero) in s.boxes and right(right(s.hero)) in _map.walls)
            ]
        ),
        effects=[
            wait,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_mob_top_factory(_map: Map) -> Action:
    """Creates an Action that pushes a mob top"""

    def push_mob_top(state: State) -> State:
        """Push the mob top"""
        mobs = [
            m for m in state.mobs if not m == (state.hero[0], state.hero[1] - 1)
        ] + [(state.hero[0], state.hero[1] - 2)]
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
                lambda s: top(s.hero) in s.mobs,
            ],
        ),
        effects=[
            push_mob_top,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_mob_bottom_factory(_map: Map) -> Action:
    """Creates an Action that pushes a mob bottom"""

    def push_mob_bottom(state: State) -> State:
        """Push the mob bottom"""
        mobs = [
            m for m in state.mobs if not m == (state.hero[0], state.hero[1] + 1)
        ] + [(state.hero[0], state.hero[1] + 2)]
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
                lambda s: bottom(s.hero) in s.mobs,
            ],
        ),
        effects=[
            push_mob_bottom,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_mob_left_factory(_map: Map) -> Action:
    """Creates an Action that pushes a mob left"""

    def push_mob_left(state: State) -> State:
        """Push the mob left"""
        mobs = [
            m for m in state.mobs if not m == (state.hero[0] - 1, state.hero[1])
        ] + [(state.hero[0] - 2, state.hero[1])]
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
                lambda s: left(s.hero) in s.mobs,
            ],
        ),
        effects=[
            push_mob_left,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def push_mob_right_factory(_map: Map) -> Action:
    """Creates an Action that pushes a mob right"""

    def push_mob_right(state: State) -> State:
        """Push the mob right"""
        mobs = [
            m for m in state.mobs if not m == (state.hero[0] + 1, state.hero[1])
        ] + [(state.hero[0] + 2, state.hero[1])]
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
                lambda s: right(s.hero) in s.mobs,
            ],
        ),
        effects=[
            push_mob_right,
            switch_traps,
            check_for_trap,
            check_for_kills,
        ],
    )


def open_lock_top_factory(_map: Map) -> Action:
    """Creates an Action that opens a lock at the top of the hero"""

    def open_lock(state: State) -> State:
        """Open the lock"""
        return State(
            hero=state.hero,
            key=state.key,
            lock=(-1, -1),
            depth=state.depth,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )

    return Action(
        preconditions=frozenset(
            [
                lambda s: s.lock == top(s.hero),
                lambda s: s.key == (-1, -1),
            ],
        ),
        effects=[
            open_lock,
        ],
    )


def open_lock_bottom_factory(_map: Map) -> Action:
    """Creates an Action that opens a lock at the bottom of the hero"""

    def open_lock(state: State) -> State:
        """Open the lock"""
        return State(
            hero=state.hero,
            key=state.key,
            lock=(-1, -1),
            depth=state.depth,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )

    return Action(
        preconditions=frozenset(
            [
                lambda s: s.lock == bottom(s.hero),
                lambda s: s.key == (-1, -1),
            ],
        ),
        effects=[
            open_lock,
        ],
    )


def open_lock_left_factory(_map: Map) -> Action:
    """Creates an Action that opens a lock at the left of the hero"""

    def open_lock(state: State) -> State:
        """Open the lock"""
        return State(
            hero=state.hero,
            key=state.key,
            lock=(-1, -1),
            depth=state.depth,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )

    return Action(
        preconditions=frozenset(
            [
                lambda s: s.lock == left(s.hero),
                lambda s: s.key == (-1, -1),
            ],
        ),
        effects=[
            open_lock,
        ],
    )


def open_lock_right_factory(_map: Map) -> Action:
    """Creates an Action that opens a lock at the right of the hero"""

    def open_lock(state: State) -> State:
        """Open the lock"""
        return State(
            hero=state.hero,
            key=state.key,
            lock=(-1, -1),
            depth=state.depth,
            open_traps=state.open_traps,
            closed_traps=state.closed_traps,
            boxes=state.boxes,
            mobs=state.mobs,
        )

    return Action(
        preconditions=frozenset(
            [
                lambda s: s.lock == right(s.hero),
                lambda s: s.key == (-1, -1),
            ],
        ),
        effects=[
            open_lock,
        ],
    )


helltaker_actions_factories = {
    "move_top": move_top_factory,
    "move_bottom": move_bottom_factory,
    "move_left": move_left_factory,
    "move_right": move_right_factory,
    "push_top": push_top_factory,
    "push_bottom": push_bottom_factory,
    "push_left": push_left_factory,
    "push_right": push_right_factory,
    "push_mob_top": push_mob_top_factory,
    "push_mob_bottom": push_mob_bottom_factory,
    "push_mob_left": push_mob_left_factory,
    "push_mob_right": push_mob_right_factory,
    "wait_top": wait_top_factory,
    "wait_bottom": wait_bottom_factory,
    "wait_left": wait_left_factory,
    "wait_right": wait_right_factory,
    "open_lock_top": open_lock_top_factory,
    "open_lock_bottom": open_lock_bottom_factory,
    "open_lock_left": open_lock_left_factory,
    "open_lock_right": open_lock_right_factory,
}


def create_actions(
    actions_factories: Dict[str, Callable[[Map], Callable]],
    _map: Map,
    directions: Dict[str, Callable[[Tuple[int, int]], Tuple[int, int]]],
) -> Dict[str, Action]:
    """Create actions from actions factories"""
    return {
        name + "_" + dirname: factory(_map, direction)
        for name, factory in actions_factories.items()
        for dirname, direction in directions.items()
    }


def execute(state: State, action: Action) -> State:
    """Execute an action on a state, returns the new state"""
    for precondition in action.preconditions:
        if not precondition(state):
            raise PrecondNotMetException("Precondition not met")

    for effect in action.effects:
        state = effect(state)

    return state


def is_final(state: State, map_: Map) -> bool:
    """Check if a state is a final state"""
    for demon in map_.demons:
        if abs(demon[0] - state.hero[0]) + abs(demon[1] - state.hero[1]) == 1:
            return True
    return False


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
    state: State, map_: Map, actions_factories: Dict[str, Callable[[Map], Callable]]
) -> List[str]:
    """Solve the puzzle using a breadth first search"""
    actions = create_actions(actions_factories, map_)
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
    heuristic: Callable[[Map, State], int] = basic_manhattan_distance,
) -> List[str]:
    """Solve the puzzle using an A* search algorithm"""
    actions = create_actions(actions_factories, map_)
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
