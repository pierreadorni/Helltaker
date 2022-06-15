from typing import Dict, List, Callable
from numpy import array
from state_space_search.types import Map, State, Action, Position


def create_actions(
    actions_factories: Dict[
        str, Callable[[Map, Callable[[Position], Position]], Action]
    ],
    _map: Map,
    directions: Dict[str, Callable[[Position], Position]],
) -> Dict[str, Action]:
    """Create actions from actions factories"""
    return {
        name + "_" + dirname: factory(_map, direction)
        for name, factory in actions_factories.items()
        for dirname, direction in directions.items()
    }


def is_final(state: State, map_: Map) -> bool:
    """Check if a state is a final state"""
    for demon in map_.demons:
        if abs(demon[0] - state.hero[0]) + abs(demon[1] - state.hero[1]) == 1:
            return True
    return False


def is_valid(
    map_: Map,
    state: State,
    actions_factories: Dict[
        str, Callable[[Map, Callable[[Position], Position]], Action]
    ],
    directions: Dict[str, Callable[[Position], Position]],
    plan: List[str],
) -> bool:
    """Checks if a plan is valid"""
    actions = create_actions(actions_factories, map_, directions)
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
