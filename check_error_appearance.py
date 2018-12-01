import requests
import urllib3

urllib3.disable_warnings()

# site = 'https://site.com'
# error_text = 'Error loading prices'


def is_an_error_message_appears_on_page(site, error_text, page):
    """

    :param site: site that will be checked
    :param error_text: expected error massage
    :param page: site's page that will be checked
    :return: True if error message appears, else - False
    """
    with requests.Session() as s:
        res = s.get('{0}/{1}'.format(site, page), verify=False)
        if res.text.find(error_text) != -1:
            return True
        return False


"""
Error loading prices
Please reload the page
"""
