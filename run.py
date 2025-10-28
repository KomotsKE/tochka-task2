import sys
import heapq

COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_X = [3, 5, 7, 9]
HALLWAY_X = [1,2,4,6,8,10,11] 

def prepare_data(lines: list[str], depth : int) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    """
    Подготовка данных для алгоритма

    Args:
        lines: список строк, представляющих лабиринт
        depth: глубина лабиринта

    Returns:
        кортеж ячеек коридора и кортеж ячеек комнат
    """
    hallway = tuple(lines[1][1:-1])
    rooms = [] 
    room_start_line = 2 # линия с которой начинаются комнаты
    for i in range(room_start_line, room_start_line+depth):
        row = [char for char in lines[i] if char in "ABCD"]
        rooms.append(row)
    rooms = tuple(zip(*rooms))
    return hallway, rooms

def generate_goal_state(depth: int) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    """
    Генерация выигрышного состояния

    Args:
        depth: глубина лабиринта

    Returns: 
        кортеж выигрышных ячеек коридора и кортеж ячеек комнат
    """
    goal_hallway = (".",) * 11
    rooms_count = 4
    goal_rooms = tuple(
        tuple(chr(ord("A")+i) for _ in range(depth)) 
        for i in range(rooms_count)
        )
    return goal_hallway, goal_rooms

def generate_move(state):
    pass

def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    depth = len(lines[2:-1])
    state = prepare_data(lines, depth)
    goal_state = generate_goal_state(depth)
    heap = [(0, state)]
    visited = {}
    while heap:
        energy, current_state = heapq.heappop(heap)
        if current_state in visited and energy >= visited[current_state]:
            continue
        visited[current_state] = energy
        if current_state == goal_state:
            return energy
        for move, cost in generate_move(state): # type: ignore
            heapq.heappush(heap, (cost, (energy+cost, move)))



    
    return 0


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    print(tuple(tuple(chr(ord("A")+i) for _ in range(2)) for i in range(5)))
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()