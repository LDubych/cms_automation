import pytest
import random
from getprice import CalcOrderPrice
from .utils.api import Order
from .utils.additional_order import AdditionalOrder


@pytest.fixture(scope="module", params=["112351"])
def original_order(request):
    """
    Get order parameters by order id by API
    :param request: value from attribute "params"- order id ,
    :return: original_order object
    """
    original_order = Order(request.param)
    yield original_order


@pytest.fixture(scope="module")
def additional_order():
    """
    :return: additional_order object
    """
    additional_order = AdditionalOrder()
    yield additional_order


def test_order_price_calculation(original_order, additional_order):
    """
    Checking the price calculation for original_order and additional_order with the same parameters
    :param original_order:
    :param additional_order:
    :return:
    """
    additional_order = additional_order.get_calculation(
        original_order.id_type,
        original_order.id_level,
        original_order.quantity,
        original_order.delivery_days,
        original_order.discount_percent,
        original_order.id_order
    )
    assert original_order.basic_order_price == additional_order.basic_order_price, \
        f'original_order.basic_order_price({original_order.basic_order_price}),' \
        f' additional_order.basic_order_price({additional_order.basic_order_price}) isn\'t equal'

    assert original_order.discount_percent == additional_order.discount_percent, \
        f'original_order original_order.discount_percent({original_order.discount_percent}), ' \
        f'additional_order.discount_percent ({additional_order.discount_percent}) isn\'t equal'

    assert original_order.final_order_price == additional_order.final_order_price, \
        f'original_order.final_order_price({original_order.final_order_price}),' \
        f' additional_order.final_order_price({additional_order.final_order_price}) isn\'t equal'

    assert original_order.id_level == additional_order.id_level, \
        f'original_order.id_level({original_order.id_level}), ' \
        f'additional_order.id_level({additional_order.id_level}) isn\'t equal'

    assert original_order.id_type == additional_order.id_type, \
        f'original_order.id_type({original_order.id_type}), ' \
        f'additional_order.id_type({additional_order.id_type}) isn\'t equal'

    assert original_order.quantity == additional_order.quantity, \
        f'original_order.quantity({original_order.quantity}), ' \
        f'additional_order.quantity({additional_order.quantity}) isn\'t equal'

    assert original_order.delivery_days == additional_order.delivery_days, \
        f'original_order.delivery_days({original_order.delivery_days}), ' \
        f'additional_order.delivery_days({additional_order.delivery_days}) isn\'t equal'

    assert additional_order.final_order_surcharge == 0, f'additional_order.final_order_surcharge\
                                                            ({additional_order.final_order_surcharge}) !=0'
    assert additional_order.basic_order_surcharge == 0, f'additional_order.final_order_surcharge\
                                                            ({additional_order.basic_order_surcharge}) !=0'


@pytest.mark.parametrize(
    'id_type, id_level', [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (3, 5)
    ])
def test_additional_order_calculation_with_valid_parameters(
        additional_order,
        id_type,
        id_level
):
    """
    Checking the price calculation for different valid parameters

    :param additional_order: pytest fixture
    :param id_type: type of order
    :param id_level: level of order
    :return:
    """
    delivery_days_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    quantity = random.randint(1, 100)
    discount_percent = random.randint(0, 20)
    order_calculation = CalcOrderPrice('testedSite.com')
    for delivery_days in delivery_days_array:
        additional_order = additional_order.get_calculation(
            id_type,
            id_level,
            quantity,
            delivery_days,
            discount_percent,
            original_order.id_order
        )

        """ Calculate the price (expected price) """
        basic_price = order_calculation.get_basic_prices(delivery_days, id_type, id_level) * quantity
        final_price = order_calculation.get_final_prices(discount_percent, original_order.premium_service > 1,
                                                         basic_price)

        """ Comparison of expected value and value that was calculated by API """
        assert round(basic_price, 2) == additional_order.basic_order_price
        assert round(basic_price - original_order.basic_order_price, 2) == additional_order.basic_order_surcharge
        assert round(discount_percent, 2) == additional_order.discount_percent
        assert round(final_price, 2) == additional_order.final_order_price
        assert round(final_price - original_order.final_order_price, 2) == additional_order.final_order_surcharge
