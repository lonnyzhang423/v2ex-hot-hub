import contextlib

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from util import logger

HOT_URL = "https://www.v2ex.com/api/topics/hot.json"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

RETRIES = Retry(total=3,
                backoff_factor=1,
                status_forcelist=[k for k in range(400, 600)])


@contextlib.contextmanager
def request_session():
    s = requests.session()
    try:
        s.headers.update(HEADERS)
        s.mount("http://", HTTPAdapter(max_retries=RETRIES))
        s.mount("https://", HTTPAdapter(max_retries=RETRIES))
        yield s
    finally:
        s.close()


class V2ex:

    def get_hot_topic(self):
        items = []
        resp = None
        try:
            with request_session() as s:
                resp = s.get(HOT_URL)
                items.extend(resp.json())
        except:
            logger.exception('get hot topic failed')
        return (items, resp)


if __name__ == "__main__":
    v2ex = V2ex()
    topics, resp = v2ex.get_hot_topic()
    logger.info('%s', topics[0])
