import requests
import pytest


@pytest.fixture(scope="module")
def session():
    """
    Establish a site session
    :return:
    """
    session = requests.Session()
    data = {
        'email': 'email@gmail.com',
        'password': '123'
    }
    url = "https://grading_site/login"
    session.post(url, data=data)
    return session


def test_401():
    """
    Checking possibility of using api without session
    :return:
    """
    data = {
        'idType ': 1,
        'data': 1,
        'asActive': True
    }
    url = 'https://site.com/api/parameters'
    response = requests.post(url=url, data=data)
    print(' Status code = ', response.status_code)
    assert response.status_code == 401, "Work with out session"


def test_4400_wrong_content_type(session):
    """
    Checking possibility of using api with wrong content type header
    :param session: pytest fixture
    :return:
    """
    data = {
        'idType': 1,
        'data': 'random data in format {":key:int": :value:float}',
        'asActive': True
    }
    url = 'https://site.com/api/parameters'
    response = session.post(url=url, data=data).json()
    print(' Status code = ', response['status'])
    print(' Status code = ', response)
    assert response['status'] == 4400, "Work with wrong content type"


def test_4400_required_param_id_type_negative(session):
    """
    Checking response from api after sending request without required parameter idType
    :param session:
    :return:
    """
    data = {
        'idType': '',
        'data': 'random data in format {":key:int": :value:float}',
        'asActive': True
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://site.com/api/parameters'
    response = session.post(url=url, json=data, headers=headers).json()
    print(' Status code = ', response['status'])
    print(' Status code = ', response)
    assert response['status'] == 4400, "Work without idType"


def test_4400_required_param_data(session):
    """
    hecking response from api after sending request without required parameter data
    :param session:
    :return:
    """
    data = {
        'idType': 2,
        'data': '',
        'asActive': True
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://site.com/api/parameters'
    response = session.post(url=url, json=data, headers=headers).json()
    print(' Status code = ', response['status'])
    print(' Status code = ', response)
    assert response['status'] == 4400, "Work without param Data"


def test_4400_required_param_asActive(session):
    """
    Checking response from api after sending request without required parameter asActivee
    :param session:
    :return:
    """
    data = {
        'idType': 2,
        'data': 'random data in format {":key:int": :value:float}',
        'asActive': ''
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://site.com/api/parameters'
    response = session.post(url=url, json=data, headers=headers).json()
    print(' Status code = ', response['status'])
    print(' Status code = ', response)
    assert response['status'] == 4400, "Work without param asActive"


def test_4400_required_param_id_type_invalid(session):
    """
    Checking response from api after sending request with invalid parameter idType
    :param session:
    :return:
    """
    data = {
        'idType': "hng",
        'data': 'random data in format {":key:int": :value:float}',
        'asActive': True
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://site.com/api/parameters'
    response = session.post(url=url, json=data, headers=headers).json()
    # print(' Status code = ', response.status_code)
    print(' Status code = ', response['status'])
    print(' Status code = ', response)
    assert response['status'] == 4400, "Work with invalid parameter idType"


@pytest.mark.skip
def test_2200_positive(session):
    """
    Checking response from api after sending valid parameters
    :param session:
    :return:
    """
    data = {
        'idType': 1,
        'data': 'random data in format {":key:int": :value:float}',
        'asActive': True
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://site.com/api/parameters'
    response = session.post(url=url, json=data, headers=headers).json()
    print(' Status code = ', response['status'])
    print(' Status code = ', response)
    assert response['status'] == 2200, "Doesn't work with positive values"
