from board import GameBoard
from units import Swordsman, Crossbowman, HealerMage


def main():
    print("Создание поля 4x4 с лимитом в 2 юнита")
    board = GameBoard(cols=4, rows=4, max_units=2)

    sword = Swordsman()
    xbow = Crossbowman()
    healer = HealerMage()

    print("\nРазмещение отрядов на поле")
    board.add_unit(sword, 0, 0)
    board.add_unit(xbow, 1, 1)

    print("\nПроверка лимита (попытка добавить третий отряд):")
    board.add_unit(healer, 2, 2)
    board.display()

    print("Перемещение мечника с (0, 0) на (0, 1):")
    sword.move(board, 0, 1)
    board.display()

    print("Клонирование поля и проверка независимости копии:")
    board_copy = board.clone()

    print("Ход мечника на исходном поле на клетку (0, 2)...")
    sword.move(board, 0, 2)

    print("Исходное поле:")
    board.display()

    print("Склонированное поле (мечник остался на прежней позиции):")
    board_copy.display()

    print("Удаление арбалетчика:")
    removed = board.remove_unit(1, 1)
    print(f"Снят с поля: {removed}")
    board.display()

    print("Добавление лекаря на освободившееся место:")
    board.add_unit(healer, 3, 3)
    board.display()


if __name__ == "__main__":
    main()