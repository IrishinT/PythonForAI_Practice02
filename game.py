import random

from gamestate import GameState
from board import GameBoard
from base import Base
from controllers import BaseController, UnitController
from landscape import Grass, Water, Mountain, Spikes
from neutral_objects import HealPotion, RustTrap
from landscape import LandscapeFactory
from neutral_objects import NeutralObjectFactory
from units import UnitFactory


class Game:
    """Главный класс игровой сессии."""

    def __init__(self, cols=8, rows=8):
        self.board = GameBoard(cols=cols, rows=rows, max_units=10)
        self.base = Base(x=0, y=0, hp=300, max_units=3, symbol='#')
        self.board.add_object(self.base, self.base.x, self.base.y)

        # Контроллеры
        self.base_ctrl = BaseController(self.base, self.board)
        self.unit_ctrl = UnitController(self.board)
        self.turn = 1

        self._setup_map()

    def _setup_map(self):
        """Генерация препятствий и предметов на карте."""
        water_count = random.randint(3, 6)
        mountain_count = random.randint(3, 5)
        spikes_count = random.randint(2, 4)
        potions_count = random.randint(2, 4)
        traps_count = random.randint(2, 4)

        def get_rand_coords():
            while True:
                x = random.randint(0, self.board.cols - 1)
                y = random.randint(0, self.board.rows - 1)

                # Не ставим объекты на саму базу (0, 0) и соседние клетки
                if x + y <= 1:
                    continue
                return x, y

        for _ in range(water_count):
            x, y = get_rand_coords()
            self.board.set_landscape(Water(), x, y)

        for _ in range(mountain_count):
            x, y = get_rand_coords()
            self.board.set_landscape(Mountain(), x, y)

        for _ in range(spikes_count):
            x, y = get_rand_coords()
            self.board.set_landscape(Spikes(), x, y)

        for _ in range(potions_count):
            for _ in range(10):  # Лимит попыток, чтобы избежать зависаний
                x, y = get_rand_coords()
                if self.board.is_cell_empty(x, y):
                    self.board.add_object(HealPotion(), x, y)
                    break

        for _ in range(traps_count):
            for _ in range(10):
                x, y = get_rand_coords()
                if self.board.is_cell_empty(x, y):
                    self.board.add_object(RustTrap(), x, y)
                    break

    def start(self):
        """Основной цикл игры."""
        print("Добро пожаловать в игру!")

        while True:
            self.board.display()
            print(self.base_ctrl.get_status())
            print(f"Текущий ход: {self.turn}")
            print("\nМеню:")
            print("1 - Управление базой (найм отрядов)")
            print("2 - Управление юнитами")
            print("3 - Сохранить игру в JSON")
            print("4 - Загрузить игру из JSON")
            print("0 - Выход из игры")

            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self._menu_base()
            elif choice == "2":
                self._menu_unit()
            elif choice == "3":
                self.save_game()
            elif choice == "4":
                self.load_game()
            elif choice == "0":
                print("Игра завершена.")
                break
            else:
                print("Неизвестная команда.")

    def _menu_base(self):
        print("\n### Найм на базу ###")
        for symbol, (name, _) in self.base_ctrl.RECRUIT_LIST.items():
            print(f"{symbol} - {name}")
        print("Q - Отмена")

        sub_choice = input("Введите символ отряда для найма: ").strip().upper()
        if sub_choice == "Q":
            return

        unit = self.base_ctrl.hire_unit(sub_choice)
        if unit:
            print(f"{unit.name} [{unit.symbol}] успешно нанят и выставлен на поле.")
        else:
            print("Не удалось создать отряд (неверный символ, лимит исчерпан или нет места).")

    def _menu_unit(self):
        my_units = self.base._units

        if not my_units:
            print("Нет отрядов на поле.")
            return

        print("\n### Отряды ###")
        for i, unit in enumerate(my_units, start=1):
            print(f"{i}. {unit.name} [{unit.symbol}] на ({unit.pos_x}, {unit.pos_y}) | HP: {unit.hp} | Урон: {unit.attack}")
        print("0. Назад")

        choice = input("Выберите номер отряда: ").strip()
        if choice == "0" or not choice.isdigit():
            return

        idx = int(choice) - 1
        if 0 <= idx < len(my_units):
            self._control_unit_wasd(my_units[idx])
        else:
            print("Неверный номер.")

    def _control_unit_wasd(self, unit):
        while True:
            self.board.display()
            print(f"Отряд: {unit.name} [{unit.symbol}] | HP: {unit.hp} | Броня: {unit.armor} | Урон: {unit.attack} | Радиус: {unit.attack_range}")
            print("Действия: W/A/S/D - Перемещение | F - Атака | Q - Назад")

            cmd = input("Ввод: ").strip().lower()
            if cmd == 'q':
                break

            tx, ty = unit.pos_x, unit.pos_y

            if cmd in ['w', 'a', 's', 'd']:
                if cmd == 'w':
                    ty -= 1
                elif cmd == 's':
                    ty += 1
                elif cmd == 'a':
                    tx -= 1
                elif cmd == 'd':
                    tx += 1

                if self.board.move_unit(unit, tx, ty):
                    print("Успешно.")
                else:
                    print("Недопустимый ход.")

            elif cmd == 'f':
                # Поиск всех доступных целей в радиусе поражения
                targets = []
                for row in range(self.board.rows):
                    for col in range(self.board.cols):
                        target = self.board.get_entity(col, row)

                        # Проверяем, что это не мы сами, и что объект можно ударить
                        if target and target != unit and hasattr(target, 'take_damage'):

                            dist = max(abs(unit.pos_x - target.pos_x), abs(unit.pos_y - target.pos_y))
                            if dist <= unit.attack_range:
                                targets.append(target)

                if not targets:
                    print("Нет целей в радиусе поражения.")
                    continue

                print("\n### Доступные цели ###")
                for i, t in enumerate(targets, start=1):
                    print(f"{i}. {t.name} [{t.symbol}] на ({t.pos_x}, {t.pos_y}) | HP: {t.hp}")

                print("0. Отмена")

                atk_choice = input("Выберите цель: ").strip()
                if atk_choice == "0" or not atk_choice.isdigit():
                    continue

                idx = int(atk_choice) - 1
                if 0 <= idx < len(targets):
                    target = targets[idx]

                    if unit.attack_target(target):
                        print(f"Урон нанесен. HP цели: {target.hp}")

                        if target.hp <= 0:
                            print("Цель уничтожена.")
                            if target.__class__.__name__ == 'Base':
                                print("База разрушена. Конец игры.")
                                exit(0)
                            else:
                                self.board.remove_unit(target.pos_x, target.pos_y)
                                if getattr(target, 'base', None):
                                    target.base.notify_unit_death(target)
                    else:
                        print("Не удалось атаковать.")

    def save_game(self, filepath="savegame.json"):
        state = GameState(save_name="Быстрое сохранение", turn=self.turn, base_hp=self.base.hp)
        state.board_size = (self.board.cols, self.board.rows)

        landscapes_data = []
        objects_data = []

        # Собираем ландшафт и нейтральные объекты за один проход по карте
        for y in range(self.board.rows):
            for x in range(self.board.cols):
                land = self.board.get_landscape(x, y)
                if not isinstance(land, Grass):
                    landscapes_data.append({"type": land.__class__.__name__, "x": x, "y": y})

                entity = self.board.get_entity(x, y)
                if hasattr(entity, 'apply'):
                    objects_data.append({"type": entity.__class__.__name__, "x": x, "y": y})

        state.landscapes = landscapes_data
        state.objects = objects_data

        # Собираем юнитов базы
        state.units = [
            {"type": u.__class__.__name__, "x": u.pos_x, "y": u.pos_y, "hp": u.hp}
            for u in self.base._units
        ]

        state.save_to_json(filepath)
        print(f"Игра успешно сохранена в {filepath}")

    def load_game(self, filepath="savegame.json"):
        try:
            state = GameState()
            state.load_from_json(filepath)
        except FileNotFoundError:
            print(f"Файл {filepath} не найден.")
            return

        # Очистка карты
        for y in range(self.board.rows):
            for x in range(self.board.cols):
                self.board.set_landscape(Grass(), x, y)
                self.board.remove_unit(x, y)

        # Восстановление ландшафта через фабрику
        for item in state.landscapes:
            land = LandscapeFactory.create(item["type"])
            self.board.set_landscape(land, item["x"], item["y"])

        # Восстановление предметов через фабрику
        for item in state.objects:
            obj = NeutralObjectFactory.create(item["type"])
            if obj:
                self.board.add_object(obj, item["x"], item["y"])

        # Восстановление базы
        self.base._hp = state.base_hp
        self.base._units.clear()
        self.board.add_object(self.base, self.base.x, self.base.y)

        # Восстановление юнитов через фабрику
        for data in state.units:
            unit = UnitFactory.create(
                unit_type=data["type"],
                x=data["x"],
                y=data["y"],
                hp=data["hp"],
                base=self.base
            )
            if unit:
                self.board.add_unit(unit, unit.pos_x, unit.pos_y)
                self.base._units.append(unit)

        self.turn = state.turn
        print(f"Игра загружена (Ход: {self.turn}, HP базы: {self.base.hp})")


if __name__ == "__main__":
    game = Game()
    game.start()