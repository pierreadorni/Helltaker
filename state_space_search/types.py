from typing import NamedTuple, Tuple, Optional, FrozenSet, Callable, List

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
