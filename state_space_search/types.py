from typing import NamedTuple, Tuple, Optional, FrozenSet, Callable, List

Position = Tuple[int, int]
State = NamedTuple(
    "State",
    [
        ("hero", Position),
        ("key", Position),
        ("lock", Position),
        ("depth", int),
        ("open_traps", Tuple[Position]),
        ("closed_traps", Tuple[Position]),
        ("boxes", Tuple[Position]),
        ("mobs", Tuple[Position]),
    ],
)
Map = NamedTuple(
    "Map",
    [
        ("walls", FrozenSet[Position]),
        ("demons", FrozenSet[Position]),
        ("spikes", FrozenSet[Position]),
        ("max_depth", int),
    ],
)
Action = NamedTuple(
    "Action",
    [
        ("preconditions", FrozenSet[Callable[[State], bool]]),
        ("effects", Tuple[Callable[[State], State], ...]),
    ],
)
