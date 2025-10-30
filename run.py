import sys
import heapq

COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_EXITS = [2, 4, 6, 8]
HALLWAY_FREE_POS = [0,1,3,5,7,9,10]

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

def check_clear_path(hallway_state, start, end) -> bool:
    """
    Метод-проверка, свободен ли путь

    Args:
        hallway: текущее состояние коридора
        start: точка старта
        end: точка конца
    
    Returns:
        True - если путь свободен
        False - если путь не свободен
    """
    if start < end:
        rng = range(start+1, end+1)
    else:
        rng = range(end, start)
    return all(hallway_state[i] == '.' for i in rng)

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

def generate_moves(state, depth):
    """
    Метод генерации ходов
    
    Args:
        state: Текущее состояние комнат и коридора
        depth: Глубина комнат

    Returns:
        Возвращает все возможные ходы из текущего состояния
    """
    hallway_state, rooms_state = state
    moves = []

    for current_pos, current_obj in enumerate(hallway_state):
        if current_obj == '.':
            continue
        target_room_index = ord(current_obj) - ord('A')
        target_room = rooms_state[target_room_index]
        room_pos = ROOM_EXITS[target_room_index]
        if all(room_obj == '.' or room_obj == current_obj for room_obj in target_room):
            if check_clear_path(hallway_state, current_pos, room_pos):
                depth_pos = depth - 1
                while target_room[depth_pos] != '.':
                    depth_pos -= 1
                steps = abs(room_pos - current_pos) + depth_pos + 1
                energy = steps * COST[current_obj]
                new_hallway_state = list(hallway_state)
                new_hallway_state[current_pos] = '.'
                new_rooms_state = [list(room) for room in rooms_state]
                new_rooms_state[target_room_index][depth_pos] = current_obj
                moves.append(((tuple(new_hallway_state), tuple(tuple(room) for room in new_rooms_state)), energy))

    for room_index, room in enumerate(rooms_state):
        room_pos = ROOM_EXITS[room_index]
        for depth_pos, current_obj in enumerate(room):
            if current_obj == '.':
                continue
            if current_obj == chr(ord('A')+room_index) and all(room_obj == current_obj for room_obj in room[depth_pos:]):
                break
            if any(room_obj != '.' for room_obj in room[:depth_pos]):
                break
            for current_pos in HALLWAY_FREE_POS:
                if check_clear_path(hallway_state, room_pos, current_pos):
                    steps = abs(room_pos - current_pos) + depth_pos + 1
                    energy = steps * COST[current_obj]
                    new_hallway_state = list(hallway_state)
                    new_hallway_state[current_pos] = current_obj
                    new_rooms_state = [list(room) for room in rooms_state]
                    new_rooms_state[room_index][depth_pos] = '.'
                    moves.append(((tuple(new_hallway_state), tuple(tuple(room) for room in new_rooms_state)), energy))
            break
    return moves

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
        for new_state, cost in generate_moves(current_state, depth):
            heapq.heappush(heap, (energy+cost, new_state))
    return -1


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()