from enum import Enum

MIN_DELIVERY_COST = 400


class Size(Enum):
    """Габариты груза."""
    SMALL = "small"
    BIG = "big"


class KWorkload(Enum):
    """Коэффициент загруженности службы доставки."""
    VERY_HIGH = 1.6
    HIGH = 1.4
    INCREASED = 1.2
    NORMAL = 1.0


class ErrorMessages(Enum):
    FRAGILE_CANNOT_BE_DELIVERED = "Хрупкие грузы нельзя доставлять на расстояние более 30 км"
    INCORRECT_DISTANCE = "Некорректное расстояние для доставки"
    INCORRECT_SIZE = "Некорректные габариты груза"
    INCORRECT_FRAGILE = "Некорректное значение хрупкости груза"
    INCORRECT_K_WORKLOAD = "Некорректное значение коэффициента загруженности службы доставки"
