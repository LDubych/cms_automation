import pytest
from getprice import CalcOrderPrice


@pytest.fixture(scope="module")
def order():
    order = CalcOrderPrice('https://site.com')
    yield order


@pytest.mark.parametrize("premium_service", [
    False,
    True
])
def test_price(order, premium_service):
    """
    Testing parameters calculation using the API
    :param order: test order
    :param premium_service:
    :return:
    """
    length = 10
    for delivery_days in range(length + 1):
        delivery_days_in_hours = order.delivery_days_in_hours(delivery_days)
        koef_top_servise = order.get_ratio_top_service(premium_service)
        quantity = 1
        discount_percent = 0
        calc_price_by_api = order.calc_prices_with_all_variables_due_to_delivery_days_by_api(
            quantity,
            delivery_days,
            premium_service,
            discount_percent
        )
        calc_price = order.calc_prices_with_all_variables_due_to_delivery_days(
            delivery_days_in_hours,
            quantity,
            premium_service,
            discount_percent
        )
        deadline = order.delivery_days_to_deadline(delivery_days_in_hours)
        assert len(calc_price_by_api) == len(calc_price)
        i = 0
        while i < len(calc_price_by_api):
            print(f'api parameters: {calc_price_by_api[i]}')
            assert calc_price_by_api[i]['basicPrice'] == calc_price[i]['basic_price'], f'basic_price isn\'t equal, \
                                                                                {calc_price[i]["basic_price"]} '
            assert calc_price_by_api[i]['finalPrice'] == calc_price[i]['final_price'], \
                'final_price isn\'t equal' + calc_price[i]['final_price']
            assert calc_price_by_api[i]['deliveryDay'][:-5] == deadline.strftime("%Y-%m-%d %H:%M:%S")[:-5], \
                'Deadline, isn\'t equal delivery_days'
            assert calc_price_by_api[i]['topService'] == koef_top_servise
            i += 1
