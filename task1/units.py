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

class MeleeUnit(Unit):
    def __init__(self, symbol, hp, armor, attack, attack_range=1, x=0, y=0):
        super().__init__(symbol, hp, armor, attack, attack_range, x, y)

class Swordsman(MeleeUnit):
    def __init__(self, x=0, y=0):
        super().__init__('S', hp=100, armor=6, attack=25, attack_range=1, x=x, y=y)

class Spearman(MeleeUnit):
    def __init__(self, x=0, y=0):
        super().__init__('P', hp=90, armor=4, attack=18, attack_range=2, x=x, y=y)


# Дистанционный бой (радиус 3-4)
class RangedUnit(Unit):
    def __init__(self, symbol, hp, armor, attack, attack_range, x=0, y=0):
        super().__init__(symbol, hp, armor, attack, attack_range, x, y)

class Bowman(RangedUnit):
    def __init__(self, x=0, y=0):
        super().__init__('B', hp=60, armor=2, attack=15, attack_range=4, x=x, y=y)

class Crossbowman(RangedUnit):
    def __init__(self, x=0, y=0):
        super().__init__('C', hp=70, armor=4, attack=28, attack_range=3, x=x, y=y)


class MageUnit(Unit):
    def __init__(self, symbol, hp, armor, attack, attack_range=999, x=0, y=0):
        super().__init__(symbol, hp, armor, attack, attack_range, x, y)

class AttackMage(MageUnit):
    def __init__(self, x=0, y=0):
        super().__init__('M', hp=50, armor=1, attack=30, attack_range=9**10, x=x, y=y)

class HealerMage(MageUnit):
    def __init__(self, x=0, y=0):
        super().__init__('H', hp=60, armor=2, attack=-25, attack_range=9**10, x=x, y=y)