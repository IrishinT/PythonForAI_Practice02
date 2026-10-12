import copy
from landscape import Grass, Water, Mountain, Spikes

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
        self.__landscape_matrix = [[Grass() for _ in range(cols)] for _ in range(rows)]


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

    def is_valid_coord(self, x, y):
        return 0 <= x < self.__cols and 0 <= y < self.__rows

    def is_cell_empty(self, x, y):
        if not self.is_valid_coord(x, y):
            return False

        return self.__matrix[y][x] is None

    def can_unit_stand(self, x, y, unit=None):
        if not self.is_valid_coord(x, y):
            return False

        landscape = self.__landscape_matrix[y][x]
        return landscape.can_pass(unit)

    def set_landscape(self, landscape_obj, x, y):
        if self.is_valid_coord(x, y):
            self.__landscape_matrix[y][x] = landscape_obj
            return True

        return False

    def get_landscape(self, x, y):
        if self.is_valid_coord(x, y):
            return self.__landscape_matrix[y][x]

        return None

    def get_entity(self, x, y):

        if self.is_valid_coord(x, y):
            return self.__matrix[y][x]

        return None

    def add_unit(self, unit, x, y):
        if self.__current_units >= self.__max_units:
            return False

        if not self.is_valid_coord(x, y):
            return False

        if not self.is_cell_empty(x, y) or not self.can_unit_stand(x, y, unit):
            return False

        self.__matrix[y][x] = unit
        unit.pos_x = x
        unit.pos_y = y
        self.__current_units += 1

        self.__landscape_matrix[y][x].on_enter(unit)
        return True

    def add_object(self, obj, x, y):
        if not self.is_valid_coord(x, y) or not self.is_cell_empty(x, y):
            return False

        self.__matrix[y][x] = obj
        return True

    def remove_unit(self, x, y):
        if not self.is_valid_coord(x, y):
            return None

        unit = self.__matrix[y][x]
        if unit is None:
            return None

        self.__matrix[y][x] = None
        self.__current_units -= 1
        return unit

    def get_unit(self, x, y):
        """Получить юнита по клетке (x, y). Если мимо поля — вернет None."""
        if 0 <= x < self.__cols and 0 <= y < self.__rows:
            return self.__matrix[y][x]
        return None

    def move_unit(self, unit, to_x, to_y):
        """
        Перемещение юнита.
        """
        if not self.is_valid_coord(to_x, to_y):
            return False

        if not self.can_unit_stand(to_x, to_y, unit):
            return False

        target_cell = self.__matrix[to_y][to_x]

        if target_cell is not None:
            if hasattr(target_cell, 'apply'):
                # подобрать предмет
                unit << target_cell
                self.__matrix[to_y][to_x] = None
            else:
                return False

        # Перемещение
        self.__matrix[unit.pos_y][unit.pos_x] = None
        self.__matrix[to_y][to_x] = unit
        unit.pos_x = to_x
        unit.pos_y = to_y

        self.__landscape_matrix[to_y][to_x].on_enter(unit)
        return True

    def clone(self):
        """
        Создает полную независимую копию поля и всех юнитов на нем (по ТЗ).
        """
        return copy.deepcopy(self)

    def display(self):
        """Вывод карты в терминал."""
        print(f"\nКарта {self.__cols}x{self.__rows} | Отрядов: {self.__current_units}/{self.__max_units}\n")

        # Номера столбцов (координата X)
        x_indices = "   " + "".join([f" {x:2}" for x in range(self.__cols)])
        print(x_indices)

        # Верхняя рамка
        border = "   +" + "---" * self.__cols + "-+"
        print(border)

        for y in range(self.__rows):
            # Номер строки (координата Y) слева
            row_str = f"{y:2} |"
            for x in range(self.__cols):
                entity = self.__matrix[y][x]
                landscape = self.__landscape_matrix[y][x]

                # Если есть юнит/база/предмет — его символ, иначе ландшафт
                symbol = entity.symbol if entity is not None else landscape.symbol
                row_str += f"  {symbol}"
            row_str += " |"
            print(row_str)

        # Нижняя рамка
        print(border)
        print()