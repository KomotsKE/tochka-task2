import sys

def prepare_data(lines: list[str]):
    """
    Подготовка данных для алгоритма

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        

    """
    hallway = list(lines[1][1:-1])
    depth = len(lines[2:-1])
    rooms = [] 
    room_start = 2 # линия с которой начинаются комнаты
    for i in range(room_start, room_start+depth):
        row = [char for char in lines[i] if char in "ABCD"]
        rooms.append(row)
    rooms = list(zip(*rooms))
    return hallway, rooms

def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    # TODO: Реализация алгоритма
    return 0


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    print(prepare_data(lines))
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()