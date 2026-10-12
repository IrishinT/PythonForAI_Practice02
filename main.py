from board import GameBoard
from base import Base
from units import Swordsman, Bowman
from landscape import Water, Mountain, Spikes
from neutral_objects import HealPotion, RustTrap


def main():
    print("Инициализация поля 8x8 с общим лимитом в 5 юнитов:")
    board = GameBoard(cols=8, rows=8, max_units=5)

    # Генерация небольшого ландшафта на карте
    # Водоем
    board.set_landscape(Water(), 3, 2)
    board.set_landscape(Water(), 4, 2)
    # Горный хребет
    board.set_landscape(Mountain(), 3, 3)
    board.set_landscape(Mountain(), 4, 3)
    # Полоса шипов
    board.set_landscape(Spikes(), 1, 1)

    print("Размещение базы на позиции (0, 0) с лимитом найма в 2 юнита:")
    base = Base(x=0, y=0, hp=300, max_units=2, symbol='#')
    board.add_object(base, base.x, base.y)

    print("Размещение нейтральных объектов:")
    # Зелье лечения на (1, 2) и кислотная ловушка на (1, 3)
    board.add_object(HealPotion(heal_value=30), 1, 2)
    board.add_object(RustTrap(armor_penalty=2), 1, 3)

    board.display()

    print("Создание отрядов через базу:")
    sword = base.create_unit(Swordsman, board)
    bow = base.create_unit(Bowman, board)
    print(f"Создан отряд ближнего боя: {sword}")
    print(f"Создан отряд стрелков: {bow}")

    print("\nПопытка найма сверх лимита базы (лимит 2 отряда):")
    extra_unit = base.create_unit(Swordsman, board)
    print(f"Результат попытки создания: {extra_unit}")
    board.display()

    print("Проверка непроходимости ландшафта (попытка шага мечника в воду на (3, 2)):")
    # Перемещаем мечника ближе к воде
    sword.move(board, 2, 2)
    step_into_water = sword.move(board, 3, 2)
    print(f"Успешность хода в воду: {step_into_water}")

    print("\nПроверка влияния ландшафта (лучник наступает на шипы на клетке (1, 1)):")
    print(f"Здоровье лучника до шага на шипы: {bow.hp} HP")
    bow.move(board, 1, 1)
    print(f"Здоровье лучника после шага на шипы: {bow.hp} HP")
    board.display()

    print("Взаимодействие с нейтральными объектами через перегрузку оператора '+'):")
    print(f"Состояние лучника до подбора предметов: {bow}")

    # Лучник идет на (1, 2), где лежит зелье лечения '+'
    print("Лучник подбирает зелье лечения на (1, 2)...")
    bow.move(board, 1, 2)
    print(f"Состояние лучника после зелья: {bow}")

    # Лучник идет на (1, 3), где лежит кислота '%'
    print("Лучник наступает в кислоту на (1, 3)...")
    bow.move(board, 1, 3)
    print(f"Состояние лучника после кислоты: {bow}")
    board.display()

    print("Проверка гибели юнита и реакции базы:")
    print(f"Отрядов на базе до гибели бойца: {base.current_units_count}/{base.max_units}")
    print("Нанесение смертельного урона лучнику...")
    bow.take_damage(200)
    # Убираем мертвого юнита с поля
    board.remove_unit(bow.pos_x, bow.pos_y)

    print(f"Отрядов на базе после гибели бойца: {base.current_units_count}/{base.max_units}")

    print("\nПовторная попытка найма на освободившееся место в базе:")
    new_sword = base.create_unit(Swordsman, board)
    print(f"Результат найма: {new_sword}")
    board.display()


if __name__ == "__main__":
    main()