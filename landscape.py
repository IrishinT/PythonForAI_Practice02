class Landscape:
    """Базовый класс ландшафта клетки."""

    def __init__(self, symbol, is_passable=True):
        """
        :param symbol: str, символ на карте
        :param is_passable: bool, проходима ли клетка
        """
        self._symbol = symbol
        self._is_passable = is_passable

    @property
    def symbol(self):
        return self._symbol

    def can_pass(self, unit):
        return self._is_passable

    def on_enter(self, unit):
        pass

    def __str__(self):
        return self._symbol


class Grass(Landscape):
    def __init__(self):
        super().__init__('.', is_passable=True)


class Spikes(Landscape):
    def __init__(self, damage=15):
        super().__init__('*', is_passable=True)
        self._damage = damage

    def on_enter(self, unit):
        unit.take_damage(self._damage)


class Water(Landscape):
    def __init__(self):
        super().__init__('~', is_passable=False)

    def can_pass(self, unit):
        return False


class Mountain(Landscape):
    def __init__(self):
        super().__init__('^', is_passable=False)

    def can_pass(self, unit):
        return False