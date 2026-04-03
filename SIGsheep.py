# region Do not edit, your solution will be invalidated

from typing import Any, Set, List
from dataclasses import dataclass

import random
import time


@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, value: object) -> bool:
        return self.x == value.x and self.y == value.y

    def __ne__(self, value: object) -> bool:
        return self.x != value.x or self.y != value.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Sheep:
    position: Position
    points: int

    def __lt__(self, other) -> bool:
        return self.points < other.points


@dataclass
class Field:
    length: int
    walls: Set[Position]
    sheep: List[Sheep]
    rivals: List[Position]


def move(field: Field, current_position: Position) -> Position:
    from collections import deque
    
    if not field.sheep:
        moves = get_valid_neighbors(current_position, field)
        return moves[0] if moves else current_position

    dist_map = {current_position: 0}
    parent_map = {current_position: None}
    queue = deque([current_position])
    
    while queue:
        curr = queue.popleft()
        for neighbor in get_valid_neighbors(curr, field):
            if neighbor not in dist_map:
                dist_map[neighbor] = dist_map[curr] + 1
                parent_map[neighbor] = curr
                queue.append(neighbor)

    best_target = None
    max_score = -1e9

    for s in field.sheep:
        if s.position in dist_map:
            my_real_dist = dist_map[s.position]
            
            rival_competitiveness = 999
            for r in field.rivals:
                d = abs(s.position.x - r.x) + abs(s.position.y - r.y)
                rival_competitiveness = min(rival_competitiveness, d)
            
            if my_real_dist < rival_competitiveness:
                score = (s.points * 20) / (my_real_dist + 1)
            elif my_real_dist == rival_competitiveness:
                score = (s.points * 5) / (my_real_dist + 1)
            else:
                score = s.points / (my_real_dist + 100)
            
            for other_s in field.sheep:
                if other_s.position != s.position:
                    # If another sheep is within 3 steps of our target
                    if abs(s.position.x - other_s.position.x) + abs(s.position.y - other_s.position.y) <= 3:
                        score *= 1.2 # Cluster bonus

            if score > max_score:
                max_score = score
                best_target = s.position

    if best_target:
        step = best_target
        while parent_map[step] is not None and parent_map[step] != current_position:
            step = parent_map[step]
        return step

    fallback = get_valid_neighbors(current_position, field)
    return fallback[0] if fallback else current_position


def get_valid_neighbors(current_position: Position, field: Field) -> List[Position]:
    possible_neighbors = [
        Position(current_position.x, current_position.y - 1),
        Position(current_position.x, current_position.y + 1),
        Position(current_position.x + 1, current_position.y),
        Position(current_position.x - 1, current_position.y),
    ]
    valid_neighbors = []
    for neighbor in possible_neighbors:
        is_valid = (
            0 <= neighbor.x < field.length
            and 0 <= neighbor.y < field.length
            and neighbor not in field.walls
        )
        if is_valid:
            valid_neighbors.append(neighbor)
    return valid_neighbors

def show_grid(field: Field, player: Position):
    grid = [[" " for _ in range(field.length)] for _ in range(field.length)]
    for sheep in field.sheep:
        grid[sheep.position.y][sheep.position.x] = str(sheep.points)
    for wall in field.walls:
        grid[wall.y][wall.x] = "X"

    grid[player.y][player.x] = "P"
    print("\033[H\033[J", end="")
    printable_grid_lines = ["".join(row) for row in grid]
    print("\n".join(printable_grid_lines))


def use_default_field():
    # Example grid. The competition grid will be different
    return Field(
        length=50,
        walls={
            Position(x=38, y=23),
            Position(x=42, y=39),
            Position(x=7, y=26),
            Position(x=18, y=26),
            Position(x=22, y=26),
            Position(x=29, y=41),
            Position(x=40, y=41),
            Position(x=9, y=17),
            Position(x=9, y=26),
            Position(x=24, y=8),
            Position(x=41, y=24),
            Position(x=9, y=35),
            Position(x=18, y=10),
            Position(x=21, y=9),
            Position(x=26, y=23),
            Position(x=13, y=26),
            Position(x=24, y=26),
            Position(x=30, y=39),
            Position(x=43, y=39),
            Position(x=11, y=44),
            Position(x=40, y=34),
            Position(x=47, y=27),
            Position(x=40, y=43),
            Position(x=28, y=23),
            Position(x=22, y=37),
            Position(x=31, y=40),
            Position(x=9, y=19),
            Position(x=41, y=26),
            Position(x=32, y=23),
            Position(x=1, y=26),
            Position(x=31, y=15),
            Position(x=11, y=46),
            Position(x=34, y=23),
            Position(x=40, y=36),
            Position(x=30, y=13),
            Position(x=9, y=12),
            Position(x=3, y=26),
            Position(x=14, y=26),
            Position(x=43, y=7),
            Position(x=40, y=45),
            Position(x=9, y=21),
            Position(x=41, y=28),
            Position(x=42, y=27),
            Position(x=27, y=38),
            Position(x=19, y=34),
            Position(x=16, y=26),
            Position(x=31, y=8),
            Position(x=45, y=7),
            Position(x=46, y=27),
            Position(x=25, y=38),
            Position(x=9, y=42),
            Position(x=11, y=48),
            Position(x=12, y=13),
            Position(x=17, y=9),
            Position(x=20, y=26),
            Position(x=29, y=38),
            Position(x=20, y=35),
            Position(x=40, y=38),
            Position(x=9, y=14),
            Position(x=40, y=47),
            Position(x=41, y=21),
            Position(x=32, y=18),
            Position(x=41, y=30),
            Position(x=43, y=27),
            Position(x=35, y=23),
            Position(x=41, y=39),
            Position(x=27, y=40),
            Position(x=31, y=1),
            Position(x=20, y=10),
            Position(x=45, y=9),
            Position(x=31, y=10),
            Position(x=25, y=40),
            Position(x=31, y=19),
            Position(x=40, y=31),
            Position(x=37, y=23),
            Position(x=40, y=40),
            Position(x=21, y=36),
            Position(x=9, y=16),
            Position(x=41, y=14),
            Position(x=43, y=11),
            Position(x=44, y=10),
            Position(x=23, y=42),
            Position(x=41, y=23),
            Position(x=30, y=20),
            Position(x=45, y=39),
            Position(x=10, y=26),
            Position(x=31, y=3),
            Position(x=9, y=37),
            Position(x=31, y=12),
            Position(x=22, y=9),
            Position(x=11, y=43),
            Position(x=12, y=8),
            Position(x=49, y=27),
            Position(x=14, y=14),
            Position(x=40, y=33),
            Position(x=12, y=26),
            Position(x=23, y=26),
            Position(x=40, y=42),
            Position(x=43, y=13),
            Position(x=13, y=9),
            Position(x=41, y=25),
            Position(x=30, y=22),
            Position(x=25, y=26),
            Position(x=31, y=5),
            Position(x=9, y=39),
            Position(x=31, y=14),
            Position(x=11, y=45),
            Position(x=31, y=23),
            Position(x=48, y=39),
            Position(x=40, y=35),
            Position(x=20, y=32),
            Position(x=21, y=31),
            Position(x=40, y=44),
            Position(x=41, y=9),
            Position(x=42, y=8),
            Position(x=10, y=12),
            Position(x=33, y=23),
            Position(x=9, y=23),
            Position(x=16, y=16),
            Position(x=19, y=33),
            Position(x=2, y=26),
            Position(x=40, y=10),
            Position(x=31, y=7),
            Position(x=9, y=41),
            Position(x=31, y=16),
            Position(x=11, y=47),
            Position(x=14, y=9),
            Position(x=6, y=26),
            Position(x=24, y=41),
            Position(x=26, y=38),
            Position(x=40, y=37),
            Position(x=4, y=26),
            Position(x=45, y=27),
            Position(x=41, y=20),
            Position(x=11, y=13),
            Position(x=16, y=9),
            Position(x=8, y=26),
            Position(x=9, y=25),
            Position(x=19, y=26),
            Position(x=28, y=38),
            Position(x=22, y=43),
            Position(x=39, y=13),
            Position(x=40, y=12),
            Position(x=31, y=9),
            Position(x=11, y=49),
            Position(x=21, y=26),
            Position(x=26, y=40),
            Position(x=19, y=10),
            Position(x=10, y=7),
            Position(x=42, y=12),
            Position(x=27, y=23),
            Position(x=9, y=18),
            Position(x=31, y=2),
            Position(x=9, y=36),
            Position(x=15, y=15),
            Position(x=40, y=14),
            Position(x=31, y=11),
            Position(x=48, y=27),
            Position(x=29, y=23),
            Position(x=46, y=39),
            Position(x=44, y=39),
            Position(x=40, y=32),
            Position(x=42, y=14),
            Position(x=9, y=11),
            Position(x=11, y=8),
            Position(x=30, y=21),
            Position(x=9, y=20),
            Position(x=0, y=26),
            Position(x=11, y=26),
            Position(x=41, y=27),
            Position(x=31, y=4),
            Position(x=9, y=38),
            Position(x=23, y=9),
            Position(x=15, y=26),
            Position(x=24, y=38),
            Position(x=9, y=13),
            Position(x=40, y=46),
            Position(x=17, y=26),
            Position(x=30, y=23),
            Position(x=47, y=39),
            Position(x=9, y=22),
            Position(x=23, y=39),
            Position(x=32, y=17),
            Position(x=13, y=13),
            Position(x=41, y=29),
            Position(x=31, y=6),
            Position(x=9, y=40),
            Position(x=45, y=8),
            Position(x=36, y=23),
            Position(x=9, y=6),
            Position(x=40, y=39),
            Position(x=9, y=15),
            Position(x=5, y=26),
            Position(x=21, y=44),
            Position(x=9, y=24),
            Position(x=41, y=22),
            Position(x=40, y=11),
            Position(x=44, y=27),
        },
        sheep=[
            Sheep(position=Position(x=12, y=0), points=4),
            Sheep(position=Position(x=23, y=0), points=8),
            Sheep(position=Position(x=45, y=0), points=7),
            Sheep(position=Position(x=7, y=1), points=3),
            Sheep(position=Position(x=34, y=1), points=3),
            Sheep(position=Position(x=0, y=2), points=4),
            Sheep(position=Position(x=15, y=2), points=5),
            Sheep(position=Position(x=8, y=3), points=9),
            Sheep(position=Position(x=30, y=3), points=6),
            Sheep(position=Position(x=45, y=3), points=7),
            Sheep(position=Position(x=23, y=4), points=3),
            Sheep(position=Position(x=15, y=5), points=4),
            Sheep(position=Position(x=35, y=5), points=4),
            Sheep(position=Position(x=13, y=6), points=6),
            Sheep(position=Position(x=29, y=6), points=5),
            Sheep(position=Position(x=8, y=7), points=5),
            Sheep(position=Position(x=20, y=8), points=7),
            Sheep(position=Position(x=23, y=8), points=9),
            Sheep(position=Position(x=44, y=8), points=2),
            Sheep(position=Position(x=35, y=9), points=4),
            Sheep(position=Position(x=42, y=10), points=3),
            Sheep(position=Position(x=0, y=11), points=4),
            Sheep(position=Position(x=7, y=11), points=3),
            Sheep(position=Position(x=27, y=11), points=6),
            Sheep(position=Position(x=15, y=12), points=5),
            Sheep(position=Position(x=31, y=13), points=5),
            Sheep(position=Position(x=41, y=13), points=9),
            Sheep(position=Position(x=13, y=14), points=6),
            Sheep(position=Position(x=37, y=15), points=4),
            Sheep(position=Position(x=8, y=16), points=9),
            Sheep(position=Position(x=11, y=17), points=2),
            Sheep(position=Position(x=31, y=17), points=6),
            Sheep(position=Position(x=43, y=17), points=6),
            Sheep(position=Position(x=16, y=18), points=2),
            Sheep(position=Position(x=31, y=18), points=8),
            Sheep(position=Position(x=37, y=18), points=8),
            Sheep(position=Position(x=42, y=19), points=3),
            Sheep(position=Position(x=7, y=21), points=3),
            Sheep(position=Position(x=31, y=21), points=3),
            Sheep(position=Position(x=16, y=23), points=2),
            Sheep(position=Position(x=8, y=24), points=3),
            Sheep(position=Position(x=17, y=24), points=8),
            Sheep(position=Position(x=28, y=24), points=3),
            Sheep(position=Position(x=43, y=24), points=2),
            Sheep(position=Position(x=42, y=26), points=5),
            Sheep(position=Position(x=44, y=26), points=5),
            Sheep(position=Position(x=9, y=27), points=4),
            Sheep(position=Position(x=28, y=27), points=3),
            Sheep(position=Position(x=18, y=28), points=8),
            Sheep(position=Position(x=42, y=28), points=9),
            Sheep(position=Position(x=14, y=30), points=4),
            Sheep(position=Position(x=30, y=30), points=5),
            Sheep(position=Position(x=38, y=30), points=2),
            Sheep(position=Position(x=23, y=32), points=4),
            Sheep(position=Position(x=5, y=33), points=4),
            Sheep(position=Position(x=14, y=33), points=9),
            Sheep(position=Position(x=41, y=33), points=7),
            Sheep(position=Position(x=42, y=33), points=3),
            Sheep(position=Position(x=21, y=34), points=8),
            Sheep(position=Position(x=27, y=35), points=4),
            Sheep(position=Position(x=6, y=36), points=4),
            Sheep(position=Position(x=42, y=36), points=3),
            Sheep(position=Position(x=38, y=38), points=3),
            Sheep(position=Position(x=25, y=39), points=9),
            Sheep(position=Position(x=5, y=40), points=5),
            Sheep(position=Position(x=13, y=40), points=2),
            Sheep(position=Position(x=44, y=40), points=5),
            Sheep(position=Position(x=46, y=47), points=7),
            Sheep(position=Position(x=12, y=48), points=2),
            Sheep(position=Position(x=22, y=48), points=1),
            Sheep(position=Position(x=4, y=49), points=8),
            Sheep(position=Position(x=22, y=49), points=5),
            Sheep(position=Position(x=49, y=49), points=4),
        ],
        rivals=[Position(x=22, y=25)],
    )

if __name__ == "__main__":
    # Example: Load field from a file
    # with open("map_file.txt", "r") as f:
    #     field = field_from_string(f.read())

    field = use_default_field()

    current_position = field.rivals[0]
    while len(field.sheep) > 0:
        current_position = move(field, current_position)
        field.sheep = [
            sheep for sheep in field.sheep if current_position != sheep.position
        ]
        show_grid(field, current_position)
        time.sleep(0.5)

# endregion