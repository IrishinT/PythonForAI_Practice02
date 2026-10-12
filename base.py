class Base:
    """
    Класс базы.
    Отвечает за производство отрядов и учет живой силы.
    """

    def __init__(self, x, y, hp=500, max_units=3, symbol='#'):
        """
        :param x: int, координата X на карте
        :param y: int, координата Y на карте
        :param hp: int, прочность базы
        :param max_units: int, максимальное число живых юнитов базы
        :param symbol: str, отображение на карте
        """
        self._x = x
        self._y = y
        self._hp = hp
        self._max_hp = hp
        self._max_units = max_units
        self._symbol = symbol
        self._units = []  # Список живых юнитов базы

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def symbol(self):
        return self._symbol

    @property
    def hp(self):
        return self._hp

    @property
    def current_units_count(self):
        return len(self._units)

    @property
    def max_units(self):
        return self._max_units

    def _find_spawn_point(self, board, max_radius=2):
        """
        Поиск свободной клетки вокруг базы по расширяющимся кругам.

        :param board: игровое поле
        :param max_radius: максимальный радиус поиска
        :return: (spawn_x, spawn_y) или None, если места нет
        """
        for r in range(1, max_radius + 1):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    # Проверка только внешнего периметра круга r
                    if max(abs(dx), abs(dy)) != r:
                        continue

                    target_x = self._x + dx
                    target_y = self._y + dy

                    # Проверка внутри ли поля, свободна ли клетка и проходим ли ландшафт
                    if board.is_valid_coord(target_x, target_y):
                        if board.is_cell_empty(target_x, target_y) and board.can_unit_stand(target_x, target_y):
                            return target_x, target_y

        return None

    def create_unit(self, unit_class, board):
        """
        Создание юнита указанного класса.

        :param unit_class: класс (например, Swordsman, Bowman)
        :param board: GameBoard, поле для размещения
        :return: Unit или None (в случае неудачи)
        """
        if len(self._units) >= self._max_units:
            return None

        # Поиск места для спавна
        spawn_pos = self._find_spawn_point(board)
        if spawn_pos is None:
            return None

        spawn_x, spawn_y = spawn_pos

        # Создать юнит и привязка к нему базы
        new_unit = unit_class(x=spawn_x, y=spawn_y)
        new_unit.base = self

        # Регистрация юнита на доске и внутри базы
        if board.add_unit(new_unit, spawn_x, spawn_y):
            self._units.append(new_unit)
            return new_unit

        return None

    def notify_unit_death(self, unit):
        """
        Реакция на уничтожение юнита: удаление из списка и освобождение слота.
        """
        if unit in self._units:
            self._units.remove(unit)

    def take_damage(self, damage):
        """Получение урона базой."""
        self._hp = max(0, self._hp - damage)
        return self._hp

    def __str__(self):
        return f"База {self._symbol} [HP:{self._hp}/{self._max_hp}, Войска:{len(self._units)}/{self._max_units}]"