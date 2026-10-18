# Задача 4 - вариант 6
# Напишите класс, доступ к атрибутам (переменным) которого
# осуществляется с помощью декоратора @property. Класс и информация о нем
# может сохраняться на диск в виде json-файла, а также должны иметь метод
# загрузки данных из файла.


import json
import os


class GameState:
    """
    Класс снимка состояния игры.
    Доступ к атрибутам осуществляется через @property с валидацией.
    """

    def __init__(self, save_name: str = "Autosave", turn: int = 1, base_hp: int = 300):
        self._save_name = None
        self._turn = None
        self._base_hp = None
        self._board_size = (8, 8)
        self._units = []
        self._landscapes = []
        self._objects = []

        self.save_name = save_name
        self.turn = turn
        self.base_hp = base_hp

    @property
    def save_name(self) -> str:
        return self._save_name

    @save_name.setter
    def save_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя сохранения должно быть непустой строкой.")
        self._save_name = value.strip()

    @property
    def turn(self) -> int:
        return self._turn

    @turn.setter
    def turn(self, value: int):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Номер хода должен быть целым числом больше 0.")
        self._turn = value

    @property
    def base_hp(self) -> int:
        return self._base_hp

    @base_hp.setter
    def base_hp(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("HP базы не может быть отрицательным числом.")
        self._base_hp = value

    @property
    def board_size(self) -> tuple:
        return self._board_size

    @board_size.setter
    def board_size(self, value: tuple):
        self._board_size = tuple(value)

    @property
    def units(self) -> list:
        return self._units

    @units.setter
    def units(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Список юнитов должен быть списком.")
        self._units = value

    @property
    def landscapes(self) -> list:
        return self._landscapes

    @landscapes.setter
    def landscapes(self, value: list):
        self._landscapes = value

    @property
    def objects(self) -> list:
        return self._objects

    @objects.setter
    def objects(self, value: list):
        self._objects = value

    def to_dict(self) -> dict:
        return {
            "class_name": self.__class__.__name__,
            "save_name": self.save_name,
            "turn": self.turn,
            "base_hp": self.base_hp,
            "board_size": list(self.board_size),
            "units": self.units,
            "landscapes": self.landscapes,
            "objects": self.objects
        }

    def save_to_json(self, filepath: str = "savegame.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def load_from_json(self, filepath: str = "savegame.json"):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл {filepath} не найден.")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.save_name = data.get("save_name", self.save_name)
        self.turn = data.get("turn", self.turn)
        self.base_hp = data.get("base_hp", self.base_hp)
        self.board_size = tuple(data.get("board_size", self.board_size))
        self.units = data.get("units", [])
        self.landscapes = data.get("landscapes", [])
        self.objects = data.get("objects", [])
