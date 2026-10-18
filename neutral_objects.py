class NeutralObject:
    """Базовый класс нейтрального объекта на карте."""

    def __init__(self, symbol):
        """
        :param symbol: str, символ отображения предмета на карте
        """
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol

    def apply(self, unit):
        pass

    def __str__(self):
        return f"[{self._symbol}]"


class HealPotion(NeutralObject):
    def __init__(self, heal_value=30):
        super().__init__('+')
        self._heal_value = heal_value

    def apply(self, unit):
        unit.heal(self._heal_value)


class AttackBuff(NeutralObject):
    def __init__(self, bonus_attack=10):
        super().__init__('!')
        self._bonus_attack = bonus_attack

    def apply(self, unit):
        unit.modify_attack(self._bonus_attack)


class ArmorBuff(NeutralObject):
    def __init__(self, bonus_armor=3):
        super().__init__('@')
        self._bonus_armor = bonus_armor

    def apply(self, unit):
        unit.modify_armor(self._bonus_armor)


class RustTrap(NeutralObject):
    def __init__(self, armor_penalty=3):
        super().__init__('%')
        self._armor_penalty = armor_penalty

    def apply(self, unit):
        unit.modify_armor(-self._armor_penalty)

class CurseTotem(NeutralObject):
    def __init__(self, attack_penalty=8):
        super().__init__('?')
        self._attack_penalty = attack_penalty

    def apply(self, unit):
        unit.modify_attack(-self._attack_penalty)

class NeutralObjectFactory:
    """Фабрика для создания нейтральных объектов."""

    _REGISTRY = {
        "HealPotion": HealPotion,
        "RustTrap": RustTrap,
        "AttackBuff": AttackBuff,
        "ArmorBuff": ArmorBuff,
        "CurseTotem": CurseTotem
    }

    @classmethod
    def create(cls, obj_type):
        obj_class = cls._REGISTRY.get(obj_type)
        return obj_class() if obj_class else None