from units import Swordsman, Spearman, Bowman, Crossbowman, AttackMage, HealerMage


class BaseController:
    """Контроллер для управления базой игрока."""

    RECRUIT_LIST = {
        "1": ("Мечник", Swordsman),
        "2": ("Копейщик", Spearman),
        "3": ("Лучник", Bowman),
        "4": ("Арбалетчик", Crossbowman),
        "5": ("Боевой маг", AttackMage),
        "6": ("Лекарь", HealerMage),
    }

    def __init__(self, base, board):
        self._base = base
        self._board = board

    def get_status(self):
        """Возвращает текущую информацию о базе."""
        return (f"База [{self._base.symbol}] | HP: {self._base.hp} | "
                f"Отряды: {self._base.current_units_count}/{self._base.max_units}")

    def hire_unit(self, unit_choice_key):
        """
        Наем отряда по ключу из RECRUIT_LIST.
        Возвращает созданный Unit или None при неудаче.
        """
        if unit_choice_key not in self.RECRUIT_LIST:
            return None

        _, unit_class = self.RECRUIT_LIST[unit_choice_key]
        return self._base.create_unit(unit_class, self._board)


class UnitController:
    """Контроллер для управления юнитами на поле."""

    def __init__(self, board):
        self._board = board
        self._selected_unit = None

    @property
    def selected_unit(self):
        return self._selected_unit

    def select_unit(self, x, y):
        """Выбрать юнит по координатам клетки."""
        entity = self._board.get_entity(x, y)

        if entity is not None and hasattr(entity, 'move'):
            self._selected_unit = entity
            return self._selected_unit
        self._selected_unit = None
        return None

    def deselect(self):
        """Снять выделение с текущего юнита."""
        self._selected_unit = None

    def move_selected(self, target_x, target_y):
        """Переместить выбранного юнита в указанную клетку."""
        if self._selected_unit is None:
            return False
        return self._selected_unit.move(self._board, target_x, target_y)

    def attack_target(self, target_x, target_y):
        """Атаковать цель на клетке (target_x, target_y)."""
        if self._selected_unit is None:
            return False

        target = self._board.get_entity(target_x, target_y)
        if target is None:
            return False

        success = self._selected_unit.attack_target(target)
        if success:
            # Если цель погибла (HP <= 0), убрать её с доски
            if hasattr(target, 'hp') and target.hp <= 0:
                self._board.remove_unit(target_x, target_y)
        return success