import copy

class GameBoard:
    def __init__(self, cols, rows, max_units):
        """
        :param cols: int, ширина поля (число колонок)
        :param rows: int, высота поля (число строк)
        :param max_units: int, лимит отрядов на карте
        """
        self.__cols = cols
        self.__rows = rows
        self.__max_units = max_units
        self.__current_units = 0
        # Сетка: строки (y) на столбцы (x)
        self.__matrix = [[None] * cols for _ in range(rows)]

    @property
    def cols(self):
        return self.__cols

    @property
    def rows(self):
        return self.__rows

    @property
    def max_units(self):
        return self.__max_units

    @property
    def current_units(self):
        return self.__current_units

    def get_unit(self, x, y):
        """Получить юнита по клетке (x, y). Если мимо поля — вернет None."""
        if 0 <= x < self.__cols and 0 <= y < self.__rows:
            return self.__matrix[y][x]
        return None

    def add_unit(self, unit, x, y):
        """
        Ставит юнита на клетку (x, y).
        Проверяет лимит поля и свободность клетки.
        """
        if self.__current_units >= self.__max_units:
            print(f"Ошибка: достигнут лимит армии ({self.__max_units}).")
            return False

        if not (0 <= x < self.__cols and 0 <= y < self.__rows):
            print(f"Ошибка: координаты ({x}, {y}) вне карты.")
            return False

        if self.__matrix[y][x] is not None:
            print(f"Ошибка: клетка ({x}, {y}) уже кем-то занята.")
            return False

        self.__matrix[y][x] = unit
        unit.pos_x = x
        unit.pos_y = y
        self.__current_units += 1
        return True

    def remove_unit(self, x, y):
        """Снимает юнита с клетки (x, y) и возвращает его."""
        if not (0 <= x < self.__cols and 0 <= y < self.__rows):
            return None

        unit = self.__matrix[y][x]
        if unit is None:
            return None

        self.__matrix[y][x] = None
        self.__current_units -= 1
        return unit

    def move_unit(self, unit, to_x, to_y):
        """Перемещает юнита на новые координаты."""
        if not (0 <= to_x < self.__cols and 0 <= to_y < self.__rows):
            print(f"Ход ({to_x}, {to_y}) невозможен: за пределами карты.")
            return False

        if self.__matrix[to_y][to_x] is not None:
            print(f"Ход ({to_x}, {to_y}) невозможен: клетка занята.")
            return False

        # Освобождаем старую позицию и занимаем новую
        self.__matrix[unit.pos_y][unit.pos_x] = None
        self.__matrix[to_y][to_x] = unit
        unit.pos_x = to_x
        unit.pos_y = to_y
        return True

    def clone(self):
        """
        Создает полную независимую копию поля и всех юнитов на нем (по ТЗ).
        """
        return copy.deepcopy(self)

    def display(self):
        """Вывод карты в терминал."""
        print(f"\nКарта {self.__cols}x{self.__rows} | Отрядов: {self.__current_units}/{self.__max_units}")
        for row in self.__matrix:
            row_str = ""
            for cell in row:
                if cell is None:
                    row_str += " . "
                else:
                    row_str += f"[{cell.symbol}]"
            print(row_str)
        print()