from constants import Size, KWorkload, ErrorMessages, MIN_DELIVERY_COST


def validate_inputs(distance, size, is_fragile, k_workload):
    """Проверка входных параметров для расчета стоимости доставки."""
    if distance is None or not isinstance(distance, (int, float)) or distance < 0:
        raise ValueError(ErrorMessages.INCORRECT_DISTANCE.value)

    if size not in [item for item in Size]:
        raise ValueError(ErrorMessages.INCORRECT_SIZE.value)

    if is_fragile not in (True, False):
        raise ValueError(ErrorMessages.INCORRECT_FRAGILE.value)

    if k_workload not in [item.value for item in KWorkload]:
        raise ValueError(ErrorMessages.INCORRECT_K_WORKLOAD.value)

    if is_fragile and distance > 30:
        raise ValueError(ErrorMessages.FRAGILE_CANNOT_BE_DELIVERED.value)


def calculate_delivery_cost(distance=None, size=None, is_fragile=None, k_workload=None):
    """Расчет стоимости доставки груза."""
    validate_inputs(distance, size, is_fragile, k_workload)

    delivery_cost = 0

    if distance > 30:
        delivery_cost += 300
    elif distance > 10:
        delivery_cost += 200
    elif distance > 2:
        delivery_cost += 100
    else:
        delivery_cost += 50

    if size == Size.BIG:
        delivery_cost += 200
    else:
        delivery_cost += 100

    if is_fragile:
        delivery_cost += 300

    delivery_cost *= k_workload

    if delivery_cost < MIN_DELIVERY_COST:
        return MIN_DELIVERY_COST

    return round(delivery_cost)
