""" Helltaker Solver """
from typing import NamedTuple, Tuple, Callable, FrozenSet, List, Dict


class PrecondNotMetException(Exception):
    """ Exception raised when a precondition is not met """
    pass

class NoSolutionException(Exception):
    """ Exception raised when no solution is found """
    pass

State = NamedTuple("State", [('hero', Tuple[int, int])])
Map = NamedTuple("Map", [('walls', FrozenSet[Tuple[int,int]]), ("demons", FrozenSet[Tuple[int,int]]), ('max_depth', int)])
Action = NamedTuple("Action", [
    ('preconditions', FrozenSet[Callable[[State], bool]]),
    ('effects', List[Callable[[State], State]]),
])


def parse_grid(file_dict: dict) -> (Map, State):
    """ Parse a grid to a map and a state """
    grid = file_dict['grid']
    walls = set()
    demons = set()
    hero = None
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "#":
                walls.add((j, i))
            elif char == "D":
                demons.add((j, i))
            elif char == "H":
                hero = (j, i)

    return Map(walls=frozenset(walls), demons=frozenset(demons), max_depth=file_dict['max_steps']), State(hero)


def move_top_factory(_map: Map) -> Action:
    """ Create an action that moves the hero one step up """
    def move_top(state: State) -> State:
        """ Move the hero one step up """
        return State(hero=(state.hero[0], state.hero[1] - 1))

    return Action(
        preconditions=frozenset([
            lambda s: (s.hero[0], s.hero[1] - 1) not in _map.walls,
        ]),
        effects=[move_top],
    )


def move_bottom_factory(_map: Map) -> Action:
    """ Create an action that moves the hero one step down """
    def move_bottom(state: State) -> State:
        """ Move the hero one step down """
        return State(hero=(state.hero[0], state.hero[1] + 1))

    return Action(
        preconditions=frozenset([
            lambda s: (s.hero[0], s.hero[1] + 1) not in _map.walls,
        ]),
        effects=[move_bottom],
    )


def move_left_factory(_map: Map) -> Action:
    """ Create an action that moves the hero one step left """
    def move_left(state: State) -> State:
        """ Move the hero one step left """
        return State(hero=(state.hero[0] - 1, state.hero[1]))

    return Action(
        preconditions=frozenset([
            lambda s: (s.hero[0] - 1, s.hero[1]) not in _map.walls,
        ]),
        effects=[move_left],
    )


def move_right_factory(_map: Map) -> Action:
    """ Create an action that moves the hero one step right """
    def move_right(state: State) -> State:
        """ Move the hero one step right """
        return State(hero=(state.hero[0] + 1, state.hero[1]))

    return Action(
        preconditions=frozenset([
            lambda s: (s.hero[0] + 1, s.hero[1]) not in _map.walls,
        ]),
        effects=[move_right],
    )


actions_factories = {
    "move_top": move_top_factory,
    "move_bottom": move_bottom_factory,
    "move_left": move_left_factory,
    "move_right": move_right_factory,
}


def create_actions(actions_factories: Dict[str, Callable[[Map], Callable]], _map: Map) -> Dict[str, Action]:
    """ Create actions from actions factories """
    return {
        name: factory(_map) for name, factory in actions_factories.items()
    }


def execute(state: State, action: Action) -> State:
    """ Execute an action on a state, returns the new state """
    for precondition in action.preconditions:
        if not precondition(state):
            raise PrecondNotMetException("Precondition not met")

    for effect in action.effects:
        state = effect(state)

    return state


def is_final(state: State, map_: Map) -> bool:
    """ Check if a state is a final state """
    for demon in map_.demons:
        if abs(demon[0]-state.hero[0]) + abs(demon[1]-state.hero[1]) == 1:
            return True


def rebuild_path(previous_dict: Dict[State, Tuple[State, str]], final_state: State) -> List[str]:
    """ Rebuild the path from a dictionary of previous states """
    path = [final_state]
    actions = []
    while final_state in previous_dict:
        actions.append(previous_dict[final_state][1])
        final_state = previous_dict[final_state][0]
        path.append(final_state)
    return actions[::-1]


def solve(state: State, map_: Map, actions_factories: Dict[str, Callable[[Map], Callable]]) -> List[str]:
    """ Solve the puzzle """
    actions = create_actions(actions_factories, map_)
    queue = [(state, 0)]
    visited = set()
    previous_dict = {}
    current_state = state
    while queue and queue[0][1] <= map_.max_depth:
        current_state, current_depth = queue.pop(0)
        visited.add(current_state)
        if is_final(current_state, map_):
            break
        for name, action in actions.items():
            try:
                new_state = execute(current_state, action)
            except PrecondNotMetException:
                continue
            if new_state not in visited:
                previous_dict[new_state] = (current_state, name)
                queue.append((new_state, current_depth + 1))
    if not is_final(current_state, map_):
        raise NoSolutionException(f"No solution found in {map_.max_depth} actions.")

    return rebuild_path(previous_dict, current_state)
