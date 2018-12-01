import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

build_version = '123456_1100'
data_version = '123456-v2.1.0'


def get_cms_build_version(site):
    """

    :param site: site that will be checked
    :return: True if expected build version == actual build version, else - False
    """
    cms_url = '/cms_url'
    cms_user = 'user_login'
    cms_pwd = 'user_password'
    data_login = {'login': cms_user, 'password': cms_pwd}
    with requests.Session() as s:
        req_login = s.post('{0}/{1}'.format(site, cms_url), data=data_login, verify=False)
        cms_req = s.get('{0}/cms_page_with_vars'.format(site), verify=False)

        soup = BeautifulSoup(str(cms_req.text.encode('utf-8')), "html.parser")
        cms_build_version = soup.find_all('div', {"id": "id_build_version_cell"})[0].text
        if build_version != cms_build_version:
            return False
        return True


def get_data_version(site):
    """

    :param site: site that will be checked
    :return: True if expected data version == actual data version, else - False
    """
    with requests.Session() as s:
        res = s.get('{0}'.format(site), verify=False)
        soup = BeautifulSoup(str(res.text.encode('utf-8')), "html.parser")
        site_data_version = [item["data-version"] for item in soup.find_all() if "data-version" in item.attrs][0]
        if data_version != site_data_version:
            return False
        return True


def get_constant_value(site, const_name, const_value):
    """

    :param site: site that will be checked
    :param const_name: constant that will be checked
    :param const_value: expected value of constant
    :return: True if expected const_value == actual const_value, else - False
    """
    cms_url = '/cms_url'
    cms_user = 'user_login'
    cms_pwd = 'user_password'
    data_login = {'login': cms_user, 'password': cms_pwd}

    with requests.Session() as s:
        req_login = s.post('{0}/{1}'.format(site, cms_url), data=data_login, verify=False)
        cms_req = s.get('{0}/cms_page_with_consts'.format(site), verify=False)

        soup = BeautifulSoup(str(cms_req.text.encode('utf-8')), "html.parser")
        cms_const_value = soup.find("span", text=const_name).parent.find_next_siblings('css_selector')[0].text
        if const_value != cms_const_value.strip():
            return False
        return True


site = 'https://site.com'
print(get_cms_build_version(site))
print(get_data_version(site))
print(get_constant_value(site, "const_name", "const_value"))
