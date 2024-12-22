import pytest

from calculate_delivery_cost import calculate_delivery_cost
from constants import Size, KWorkload, ErrorMessages, MIN_DELIVERY_COST


@pytest.mark.parametrize('size, is_fragile, k_workload',
                         [(Size.BIG, False, KWorkload.VERY_HIGH.value)])
@pytest.mark.parametrize('distance, expected',
                         [
                             (31, 800),
                             (30, 640),
                             (10, 480),
                             (2, 400),
                             (0, 400)
                         ])
def test_delivery_cost_by_distance(distance, size, is_fragile, k_workload, expected):
    """Проверка расчета стоимости доставки на разные расстояния."""
    result = calculate_delivery_cost(distance=distance,
                                     size=size,
                                     is_fragile=is_fragile,
                                     k_workload=k_workload)
    assert result == expected, f"\nНеверная стоимость доставки: {result}\nОжидалась: {expected}"


@pytest.mark.parametrize('distance, is_fragile, k_workload',
                         [(20, True, KWorkload.VERY_HIGH.value)])
@pytest.mark.parametrize('size, expected',
                         [
                             (Size.SMALL, 960),
                             (Size.BIG, 1120)
                         ])
def test_delivery_cost_by_size(distance, size, is_fragile, k_workload, expected):
    """Проверка расчета стоимости доставки грузов с разными габаритами."""
    result = calculate_delivery_cost(distance=distance,
                                     size=size,
                                     is_fragile=is_fragile,
                                     k_workload=k_workload)
    assert result == expected, f"\nНеверная стоимость доставки: {result}\nОжидалась: {expected}"


@pytest.mark.parametrize('distance, size, k_workload',
                         [(20, Size.BIG, KWorkload.HIGH.value)])
@pytest.mark.parametrize('is_fragile, expected',
                         [
                             (True, 980),
                             (False, 560)
                         ])
def test_delivery_cost_by_fragility(distance, size, is_fragile, k_workload, expected):
    """Проверка расчета стоимости доставки хрупких и нехрупких грузов."""
    result = calculate_delivery_cost(distance=distance,
                                     size=size,
                                     is_fragile=is_fragile,
                                     k_workload=k_workload)
    assert result == expected, f"\nНеверная стоимость доставки: {result}\nОжидалась: {expected}"


@pytest.mark.parametrize('distance, size, is_fragile',
                         [(1, Size.BIG, True)])
@pytest.mark.parametrize('k_workload, expected',
                         [(KWorkload.NORMAL.value, 550),
                          (KWorkload.INCREASED.value, 660),
                          (KWorkload.HIGH.value, 770),
                          (KWorkload.VERY_HIGH.value, 880)])
def test_delivery_cost_by_workload_coefficient(distance, size, is_fragile, k_workload, expected):
    """Проверка расчета стоимости доставки грузов при разных коэффициентах загруженности курьерской службы."""
    result = calculate_delivery_cost(distance=distance,
                                     size=size,
                                     is_fragile=is_fragile,
                                     k_workload=k_workload)
    assert result == expected, f"\nНеверная стоимость доставки: {result}\nОжидалась: {expected}"


def test_min_delivery_cost():
    """Проверка, что при расчете доставки возвращается минимальная стоимость, если сумма меньше минимальной."""
    distance = 1.5
    size = Size.SMALL
    is_fragile = False
    k_workload = KWorkload.NORMAL.value
    result = calculate_delivery_cost(distance=distance,
                                     size=size,
                                     is_fragile=is_fragile,
                                     k_workload=k_workload)
    assert result == MIN_DELIVERY_COST, f"\nНеверная стоимость доставки: {result}\nОжидалась: {MIN_DELIVERY_COST}"


def test_fragile_cannot_be_delivered():
    """Проверка запрета доставки хрупких грузов на расстояния более 30 км."""
    distance = 31
    size = Size.SMALL
    is_fragile = True
    k_workload = KWorkload.NORMAL.value
    expected_msg = ErrorMessages.FRAGILE_CANNOT_BE_DELIVERED.value
    with pytest.raises(ValueError, match=expected_msg):
        calculate_delivery_cost(distance=distance,
                                size=size,
                                is_fragile=is_fragile,
                                k_workload=k_workload)


@pytest.mark.parametrize('distance, size, is_fragile, k_workload, expected_msg',
                         [('unknown', Size.BIG, False, KWorkload.NORMAL.value, ErrorMessages.INCORRECT_DISTANCE.value),
                          (-5, Size.BIG, False, KWorkload.NORMAL.value, ErrorMessages.INCORRECT_DISTANCE.value),
                          (None, Size.BIG, False, KWorkload.NORMAL.value, ErrorMessages.INCORRECT_DISTANCE.value),
                          (10, 'unknown', False, KWorkload.NORMAL.value, ErrorMessages.INCORRECT_SIZE.value),
                          (10, Size.BIG, 'unknown', KWorkload.NORMAL.value, ErrorMessages.INCORRECT_FRAGILE.value),
                          (10, Size.BIG, False, 'unknown', ErrorMessages.INCORRECT_K_WORKLOAD.value)
                          ])
def test_delivery_cost_not_calculated_with_invalid_params(distance, size, is_fragile, k_workload, expected_msg):
    """Проверка невозможности расчета стоимости доставки при некорректных параметрах груза."""
    with pytest.raises(ValueError, match=str(expected_msg)):
        calculate_delivery_cost(distance=distance,
                                size=size,
                                is_fragile=is_fragile,
                                k_workload=k_workload)


def test_delivery_cost_not_calculated_missing_distance():
    """Проверка невозможности расчета стоимости доставки при отсутствии расстояния."""
    size = Size.SMALL
    is_fragile = True
    k_workload = KWorkload.NORMAL.value
    expected_msg = ErrorMessages.INCORRECT_DISTANCE.value
    with pytest.raises(ValueError, match=expected_msg):
        calculate_delivery_cost(size=size,
                                is_fragile=is_fragile,
                                k_workload=k_workload)


def test_delivery_cost_not_calculated_missing_size():
    """Проверка невозможности расчета стоимости доставки при отсутствии габаритов."""
    distance = 10
    is_fragile = True
    k_workload = KWorkload.NORMAL.value
    expected_msg = ErrorMessages.INCORRECT_SIZE.value
    with pytest.raises(ValueError, match=expected_msg):
        calculate_delivery_cost(distance=distance,
                                is_fragile=is_fragile,
                                k_workload=k_workload)


def test_delivery_cost_not_calculated_missing_is_fragile():
    """Проверка невозможности расчета стоимости доставки при отсутствии сведений о хрупкости груза."""
    distance = 10
    size = Size.SMALL
    k_workload = KWorkload.NORMAL.value
    expected_msg = ErrorMessages.INCORRECT_FRAGILE.value
    with pytest.raises(ValueError, match=expected_msg):
        calculate_delivery_cost(distance=distance,
                                size=size,
                                k_workload=k_workload)


def test_delivery_cost_not_calculated_missing_k_workload():
    """Проверка невозможности расчета стоимости доставки при отсутствии сведений о загруженности службы доставки."""
    distance = 10
    size = Size.SMALL
    is_fragile = True
    expected_msg = ErrorMessages.INCORRECT_K_WORKLOAD.value
    with pytest.raises(ValueError, match=expected_msg):
        calculate_delivery_cost(distance=distance,
                                size=size,
                                is_fragile=is_fragile)
