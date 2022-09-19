import requests
import http.client as http_client

# consts
PROXY_URL_HTTP = 'http://0.0.0.0:8081'
PROXY_URL_HTTPS = 'https://0.0.0.0:8081'


def scrubber(url=None, headers=None, proxies=None):
    """
    Parsing website, test method of scrubber.

    :param url:
    :param proxies:
    :return:
    """
    if not url:
        url = ''

    if not proxies:
        proxies = {}

    if not headers:
        headers = {}

    response = requests.get(
        url=url,
        headers=headers,
        proxies=proxies
    )

    return response


def main():
    """
    Entry point for testing.

    :return:
    """
    url = 'https://example.org'
    headers = {
        'scrubber-name': 'scrubber_1'
    }
    proxies = {
        "http": PROXY_URL_HTTP,
    }

    result = scrubber(
        url=url,
        headers=headers,
        proxies=proxies
    )

    print(result.text)


if __name__ == '__main__':
    main()
