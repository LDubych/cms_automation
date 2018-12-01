import requests
import pytest


@pytest.mark.prod
@pytest.mark.parametrize(
    'site_url, expected_yandex_id', [
        ('https://checked_site.com',	'12345678'),
        ('https://site',	'yandex_id')

    ])
def test_yandex_id_matching(site_url, expected_yandex_id):
    """
    Checking matching expected yandex_id with actual
    :param site_url: site that will be checked
    :param expected_yandex_id: expected yandex_id for this site
    :type site_url: string
    :type expected_yandex_id: int
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': '123456token',
    }
    data = {"section": "site_var", "field": "yandex_id"}

    response = requests.post(f'{site_url}/api/get_yandex_id_from_site', headers=headers, json=data).json()
    print(f' - {site_url} yandex id: expected = {expected_yandex_id}, actual  = {response["result"]}')
    assert response['result'] == expected_yandex_id, "Mismatch"


