import requests


# site = 'https://site.com'
# data_login = {'email': "user_email", 'password': '123'}


def create_an_order(site, data_login, id_type, id_level, quantity, delivery_day, premium_service, discount_percent,
                    checkout, item_name, details):
    """

    :param site:
    :param data_login:
    :param id_type:
    :param id_level:
    :param quantity:
    :param delivery_day:
    :param premium_service:
    :param discount_percent:
    :param checkout:
    :param item_name:
    :param details:
    :return:
    """
    data_create_an_order = {
        'idType': id_type,
        'idLevel': id_level,
        'quantity': quantity,
        'deliveryDay': delivery_day,
        'topService': premium_service,
        'discountPercent': discount_percent,
        "checkout": checkout,
        "itemName": item_name,
        "details": details,
    }

    with requests.Session() as s:
        s.get(site)
        req_login = s.post('{0}/login_url'.format(site), data=data_login, verify=False)
        if int(req_login.text) == 0:
            req_create_an_order = s.post('{0}/create_an_order'.format(site), data=data_create_an_order, verify=False)
            return req_create_an_order.text
        return {"status_code": req_login.text, "message": "Invalid authentication data"}
