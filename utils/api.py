import requests
from datetime import datetime


class API(object):
    URL_ROOT = 'https://site.com'
    LOGIN = 'user_login'
    PASSWORD = '123456'

    def __init__(self):
        self._session = requests.Session()
        url_login = '{0}/login'.format(API.URL_ROOT)
        data = {
            'email': API.LOGIN,
            'pwd': API.PASSWORD
        }
        self._session.post(url_login, data=data)

    def __del__(self):
        self._session.close()

    def get_prices(self, site):
        """

        :param site: site that will be tested
        :return: dictionary of basic order price by one item and depended parameters
        """
        data = {
            "price_on_date": datetime.utcnow().strftime("%Y-%m-%d")
        }
        headers = {
            "contentType": "application/json",
            "X-Auth-Token": "123456token"
        }
        request_rez = requests.post(url=f'https://{site}/api/prices', json=data, headers=headers).json()
        return request_rez['result']

    def api_get_order_calculation(self, site, id_type, id_level, quantity, delivery_day, premium_service,
                                  discount_percent):
        """

        :param site: site that will be tested
        :param id_type: type of order
        :param id_level: order level
        :param quantity:
        :param delivery_day:
        :param premium_service:
        :param discount_percent:
        :return: json with calculated order price and depended parameters
        """
        data = {
            'idType': id_type,
            'idLevel': id_level,
            'quantity': quantity,
            'delivery_day': delivery_day,
            'topService': premium_service,
            'discountPercent': discount_percent
        }
        headers = {
            "contentType": "application/json",
            "X-Auth-Token": "123456token"
        }
        request_rez = requests.put(url=site + '/api/original_order/price/calculation', json=data, headers=headers)
        return request_rez.json()

    def api_additional_order_price_calculation(self,
                                               id_type,
                                               id_level,
                                               quantity,
                                               delivery_days,
                                               discount_percent,
                                               id_order):
        """

        :param id_type: type of the additional order
        :param id_level: the additional order level
        :param quantity: quantity in the additional order
        :param delivery_days: delivery_days in the additional order
        :param discount_percent: discount_percent in the additional order
        :param id_order: id of test order
        :return: json with calculated price and depended parameters of additional order
        """
        data = {
            'idType': id_type,
            'idLevel': id_level,
            'quantity': quantity,
            'delivery_days': delivery_days,
            'discountPercent': discount_percent
        }
        headers = {
            "contentType": "application/json"
        }
        return self._session.put(
            url='{0}/api/orders/{1}/additional_order/calculation'.format(API.URL_ROOT, id_order), json=data,
            headers=headers).json()

    def api_create_additional_order(self,
                                    id_type,
                                    id_level,
                                    quantity,
                                    delivery_days,
                                    discount_percent,
                                    id_order):
        """

        :param id_type: type of the additional order
        :param id_level: the additional order level
        :param quantity: quantity in the additional order
        :param delivery_days: delivery_days in the additional order
        :param discount_percent: discount_percent in the additional order
        :param id_order: id of test order
        :return:
        """
        data = {
            'idType': id_type,
            'idLevel': id_level,
            'quantity': quantity,
            'delivery_days': delivery_days,
            'discountPercent': discount_percent
        }
        headers = {
            "contentType": "application/json"
        }
        return self._session.post(
            url='{0}/api/orders/{1}/additional_order/create'.format(API.URL_ROOT, id_order), json=data,
            headers=headers).json()

    def api_get_additional_order(self, id_order):
        """

        :param id_order: test order
        :return: json with order parameters
        """
        additional_orders = [
            self._session.get('{0}/api/orders/{1}/additional_orders'.format(API.URL_ROOT, id_order)).json()]
        for additional_order in additional_orders:
            if additional_order["id"] == id_order:
                return additional_order

    def get_order(self, id_order):
        """

        :param id_order:
        :return:
        """
        return self._session.get('{0}/api/order/{1}'.format(API.URL_ROOT, id_order)).json()


class Order(API):
    def __init__(self, id_order):
        API.__init__(self)
        request_rez = self.get_order(id_order)
        self.id_order = id_order
        self.basic_order_price = request_rez['basicPrice']
        self.date_created = request_rez['dateCreated']
        self.discount_percent = request_rez['discountPercent']
        self.premium_service = request_rez['topService']
        self.final_order_price = request_rez['finalPrice']
        self.id = request_rez['id']
        self.id_level = request_rez['idLevel']
        self.id_order_status = request_rez['idOrderStatus']
        self.id_type = request_rez['idType']
        self.has_additional_order = request_rez['hasAdditionalOrder']
        self.quantity = request_rez['quantity']
        self.payment_date = request_rez['paymentDate']
        self.payment_status = request_rez['paymentStatus']
