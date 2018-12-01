import pytest
import random
from datetime import datetime
import requests

order_type = [1, 2, 3, 4, 5]
level = [1, 2, 3]
order_format = {1: "Format 1",
                2: "Format 2",
                3: "Format 3"
                }
summary = f"Test topic {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} Mei at oportere laboramus, \
            cu qui consul pertinacia disputando. Est eu suas dictas."
details = "Delicata temporibus reformidans ius ad, utroque recteque ei est."
quantity = random.randint(1, 60)
top_koef = [0, 1]
discount = "0"
deadline = [120, 144, 168, 192, 216, 240]
cur_date = datetime.utcnow().strftime("%Y-%m-%d")
site_name = "https://example.com"


@pytest.fixture(scope="module")
def session_user(email, password):
    """
    Establishing a site session; authorization.

    :param email: user email
    :param password: user password
    :type email: string
    :type password: string
    :return:
    """
    data_login = {'email': email, 'password': password}
    session = requests.Session()
    req = session.post(f'{site_name}/check_login', data=data_login, verify=False)
    print("\n status code = ", req.text)
    assert req.text == '0', "Problem with checking authorization"
    return session


@pytest.mark.skip
@pytest.mark.parametrize('id_type, id_level, id_format',
                         [(1, 1, 1),
                          (2, 2, 2),
                          (3, 3, 3),
                          (4, 1, 2),
                          (5, 2, 3)])
def test_create_order_positive(session_user, id_type, id_level, id_format):
    """
    Creating original_order on site with positive parameters by url with different values of 'type', 'format', 'level'.

    :param session_user: pytest fixture
    :param id_type: type of product
    :param id_level: product level
    :param id_format: product format
    :type id_type: int
    :type id_level: int
    :type id_format: int
    :return:
    """
    files = {'file[]': ('test.txt', open('test.txt', 'rb'), 'application/vnd.oasis.opendocument.text')}
    data = {
        'type': order_type[id_type - 1],
        'format': order_format[id_format],
        'level': level[id_level - 1],
        'summary': summary,
        'details': details,
        'quantity': quantity,
        'top': top_koef[random.randint(0, 1)],
        'day_submit': cur_date,
        'deadline': deadline[random.randint(0, 11)],
        'discount': discount
    }
    print(data)
    url = f'{site_name}/ordering'
    req = session_user.post(url=url, data=data, files=files)
    print("\n status code = ", req.status_code)
    json_data = req.json()
    print(json_data)
    assert req.status_code == 202, "Problem with ordering"


@pytest.mark.skip
@pytest.mark.parametrize('id_type', [6])
def test_create_order_negative_id_type(session_user, id_type):
    """
    Checking possibility of creating original_order with invalid value of parameter 'type'.

    :param session_user: pytest fixture
    :param id_type: type of product
    :type id_type: int
    :return:
    """
    files = {'file[]': ('test.txt', open('test.txt', 'rb'), 'application/vnd.oasis.opendocument.text')}
    data = {
        'type': order_type[id_type - 1],
        'format': order_format[random.randint(0, 2)],
        'level': level[random.randint(0, 2)],
        'summary': summary,
        'details': details,
        'quantity': quantity,
        'top': top_koef[random.randint(0, 1)],
        'day_submit': cur_date,
        'deadline': deadline[random.randint(0, 5)],
        'discount': discount,
    }
    print(data)
    url = f'{site_name}/ordering'
    req = session_user.post(url=url, data=data, files=files)
    print("\n status code = ", req.status_code)
    json_data = req.json()
    print(json_data)
    assert req.status_code == 404, "Creating original_order with wrong data"
