from datetime import datetime, timedelta
from .utils.api import API


class CalcOrderPrice(API):
    def __init__(self, site):
        API.__init__(self)
        self.site = site
        self.current_date = datetime.utcnow()

    def get_ratio_top_service(self, top_service):
        """

        :param top_service: is order has top service
        :type top_service: boolean
        :return:
        """
        if top_service:
            return 1.5
        elif not top_service:
            return 1

    def get_price_due_to_parameters(self, delivery_days, id_type, id_level):
        """
        Get price and parameters that price depends of, for one item
        :param delivery_days:
        :param id_type:
        :param id_level:
        :return: dictionary with parameters: price, delivery_days, id_type, id_level
        """
        request_rez = self.get_prices(self.site)
        for x in request_rez:
            if x['delivery_days'] == delivery_days and x['id_type'] == id_type and x['level'] == id_level:
                return x

    def get_basic_prices(self, delivery_days, id_type, id_level):
        """
        Get price that depends of parameters, for one item
        :param delivery_days:
        :param id_type:
        :param id_level:
        :return:
        """
        price_by_item = None
        request_rez = self.get_prices(self.site)
        for x in request_rez:
            if x['delivery_days'] == delivery_days and x['id_table'] == id_type and x['level'] == id_level:
                price_by_item = x['price']
                break
        return price_by_item

    def get_final_prices(self, discount, top_service, basic_price):
        """
        Calculate final price of order
        :param discount:
        :param top_service:
        :param basic_price:
        :return:
        """
        return round((basic_price * (1 - (discount / 100))) * self.get_ratio_top_service(top_service), 2)

    def get_price_table_due_to_delivery_days(self, delivery_days):
        """
        Get prices, that related to specific count of delivery days, and dependent parameters
        :param delivery_days:
        :return:
        """
        data_due_to_delivery_days = []
        price_table = self.get_prices(self.site)
        for x in price_table:
            if x["delivery_days"] == delivery_days:
                data_due_to_delivery_days.append(x)
        return data_due_to_delivery_days

    def delivery_days_in_hours(self, delivery_days):
        """

        :param delivery_days:
        :return:
        """
        if delivery_days == 0:
            hours = 12
        else:
            hours = delivery_days * 24
        return hours

    def delivery_days_to_deadline(self, delivery_days):
        """

        :param delivery_days:
        :return:
        """
        return self.current_date + timedelta(hours=delivery_days)

    def deadline_to_delivery_days(self, deadline):
        """

        :param deadline:
        :return:
        """
        return int((deadline - self.current_date).total_seconds() / 60 / 60)

    def calc_prices_with_all_variables_due_to_delivery_days_by_api(self,
                                                                   quantity,
                                                                   delivery_days,
                                                                   premium_service,
                                                                   discount_percent,
                                                                   ):
        """
        Get arrays of order parameters that related to specific delivery days calculated by the API
        :param quantity:
        :param delivery_days:
        :param premium_service:
        :param discount_percent:
        :return:
        """
        price_table = self.get_price_table_due_to_delivery_days(delivery_days)
        return [
            self.api_get_order_calculation(
                self.site,
                table_row['id_type'],
                table_row['id_level'],
                quantity,
                delivery_days,
                premium_service,
                discount_percent
            )
            for table_row in price_table
        ]

    def calc_prices_with_all_variables_due_to_delivery_days(self, delivery_days, quantity, premium_service, discount):
        """
        Get arrays of order parameters that related to specific delivery days
        :param delivery_days:
        :param quantity:
        :param premium_service:
        :param discount:
        :return:
        """
        price_table = self.get_price_table_due_to_delivery_days(delivery_days)
        data_due_to_delivery_days = []
        for table_row in price_table:
            basic_price = table_row["price"] * quantity
            final_price = basic_price * (1 - (discount / 100)) * self.get_ratio_top_service(premium_service)
            data_due_to_delivery_days.append({
                'basic_price': basic_price,
                'final_price': final_price
            })
        return data_due_to_delivery_days
