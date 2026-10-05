from abc import ABC, abstractmethod


class Unit(ABC):
    """
    Абстрактный базовый класс юнита.
    Все отряды на поле боя обязаны наследоваться от него.
    """

    def __init__(self, name: str, hp: int, armor: int, attack: int, speed: int = 1, x: int = 0, y: int = 0):
        self._name = name
        self._max_hp = hp
        self._hp = hp
        self._armor = armor
        self._attack = attack
        self._speed = speed

        # Координаты на игровом поле
        self._pos_x = x
        self._pos_y = y

    # Свойства для координат
    @property
    def pos_x(self) -> int:
        return self._pos_x

    @pos_x.setter
    def pos_x(self, x: int):
        self._pos_x = x

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @pos_y.setter
    def pos_y(self, y: int):
        self._pos_y = y

    # Свойства для характеристик
    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @property
    def armor(self) -> int:
        return self._armor

    @property
    def attack_power(self) -> int:
        return self._attack

    @property
    def speed(self) -> int:
        return self._speed

    # Базовые методы жизнедеятельности юнита
    def take_damage(self, damage: int) -> int:
        """
        Получение урона с учетом брони.
        Возвращает фактически нанесенный урон.
        """
        actual_damage = max(1, damage - self._armor)
        self._hp = max(0, self._hp - actual_damage)
        return actual_damage

    @abstractmethod
    def move(self, board, target_x: int, target_y: int) -> bool:
        """
        Перемещение юнита по игровому полю.
        Логику реализуем при интеграции с GameBoard.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Текстовое представление для вывода на карту/в консоль."""
        pass



class GameBoard:
    def __init__(self, cols, rows, max_units):
        self.__cols = cols
        self.__rows = rows
        self.__matrix = [[None] * cols for _ in range(rows)]
        self.__current_units = 0
        self.__max_units = max_units

    @property
    def current_units(self):
        return self.__current_units

    @current_units.getter
    def current_units(self):
        return self.__current_units


    def get_unit(self, x, y):
        return self.__matrix[x][y]

    def

