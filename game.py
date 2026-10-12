from board import GameBoard
from base import Base
from controllers import BaseController, UnitController
from landscape import Water, Mountain, Spikes
from neutral_objects import HealPotion, RustTrap


class Game:
    """Главный класс игровой сессии."""

    def __init__(self, cols=8, rows=8):
        self.board = GameBoard(cols=cols, rows=rows, max_units=5)
        self.base = Base(x=0, y=0, hp=300, max_units=3, symbol='#')
        self.board.add_object(self.base, self.base.x, self.base.y)

        # Контроллеры
        self.base_ctrl = BaseController(self.base, self.board)
        self.unit_ctrl = UnitController(self.board)

        self._setup_map()

    def _setup_map(self):
        """Генерация препятствий и предметов на карте."""
        # Препятствия
        self.board.set_landscape(Water(), 3, 2)
        self.board.set_landscape(Water(), 4, 2)
        self.board.set_landscape(Mountain(), 3, 3)
        self.board.set_landscape(Mountain(), 4, 3)
        self.board.set_landscape(Spikes(), 2, 1)

        # Нейтральные объекты
        self.board.add_object(HealPotion(), 1, 3)
        self.board.add_object(RustTrap(), 2, 4)

    def start(self):
        """Основной цикл игры."""
        print("Добро пожаловать в пошаговую стратегию!")

        while True:
            self.board.display()
            print(self.base_ctrl.get_status())
            print("1 - Управление базой (нанять отряд)")
            print("2 - Управление юнитом (выбрать и отдать приказ)")
            print("0 - Выход из игры")

            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self._menu_base()
            elif choice == "2":
                self._menu_unit()
            elif choice == "0":
                print("Игра завершена.")
                break
            else:
                print("Неизвестная команда.")

    def _menu_base(self):
        """Подменю базы."""
        print("\n--- Найм в гарнизон ---")
        for key, (name, _) in self.base_ctrl.RECRUIT_LIST.items():
            print(f"{key} - {name}")
        print("0 - Отмена")

        sub_choice = input("Кого нанять: ").strip()
        if sub_choice == "0":
            return

        unit = self.base_ctrl.hire_unit(sub_choice)
        if unit:
            print(f"Отряд [{unit.symbol}] успешно нанят и выставлен на поле.")
        else:
            print("Не удалось создать отряд (лимит исчерпан или все клетки заняты).")

    def _menu_unit(self):
        """Подменю управления юнитом."""
        try:
            x = int(input("Введите координату X юнита: "))
            y = int(input("Введите координату Y юнита: "))
        except ValueError:
            print("Координаты должны быть числами.")
            return

        unit = self.unit_ctrl.select_unit(x, y)
        if not unit:
            print("В этой клетке нет подконтрольного юнита.")
            return

        print(f"\nВыбран: {unit}")
        print("1 - Переместить")
        print("2 - Атаковать цель")
        print("0 - Снять выбор")

        action = input("Приказ: ").strip()
        if action == "1":
            try:
                tx = int(input("Куда идти (целевой X): "))
                ty = int(input("Куда идти (целевой Y): "))
                if self.unit_ctrl.move_selected(tx, ty):
                    print("Отряд успешно перемещен.")
                else:
                    print("Невозможно выполнить ход (препятствие, занято или за границами).")
            except ValueError:
                print("Координаты должны быть числами.")

        elif action == "2":
            try:
                tx = int(input("Цель для атаки (X): "))
                ty = int(input("Цель для атаки (Y): "))
                if self.unit_ctrl.attack_target(tx, ty):
                    print("Атака успешно совершена!")
                else:
                    print("Не удалось атаковать (цель вне зоны досягаемости или пустая клетка).")
            except ValueError:
                print("Координаты должны быть числами.")


if __name__ == "__main__":
    game = Game()
    game.start()