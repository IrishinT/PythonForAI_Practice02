class Unit:
    """Базовый класс отряда. Задает общие статы и логику перемещения."""

    def __init__(self, symbol, hp, armor, attack, attack_range=1, x=0, y=0):
        """
        :param symbol: str, символ отряда на поле (напр. 'S', 'A')
        :param hp: int, очки здоровья
        :param armor: int, очки брони (снижают урон)
        :param attack: int, сила атаки
        :param attack_range: int, дальность атаки в клетках (по дефолту 1)
        :param x: int, начальная координата по горизонтали
        :param y: int, начальная координата по вертикали
        """
        self._symbol = symbol
        self._hp = hp
        self._armor = armor
        self._attack = attack
        self._attack_range = attack_range
        self._pos_x = x
        self._pos_y = y

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, x):
        self._pos_x = x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, y):
        self._pos_y = y

    @property
    def symbol(self):
        return self._symbol

    @property
    def hp(self):
        return self._hp

    @property
    def armor(self):
        return self._armor

    @property
    def attack(self):
        return self._attack

    @property
    def attack_range(self):
        return self._attack_range

    def move(self, board, new_x, new_y):
        """
        Запрос на перемещение юнита по полю.

        :param board: GameBoard, поле на котором стоит юнит
        :param new_x: int, целевой X
        :param new_y: int, целевой Y
        :return: bool, удалось ли сделать ход
        """
        return board.move_unit(self, new_x, new_y)

    def __str__(self):
        return f"{self._symbol}(hp:{self._hp}, arm:{self._armor}, atk:{self._attack}, rng:{self._attack_range})"
