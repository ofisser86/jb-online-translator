import requests


def check_success(url):
    return 'Fail' if requests.get(url).status_code % 100 == 4 else "Success"
