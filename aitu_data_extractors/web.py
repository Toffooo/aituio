import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Web:
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36",
    }

    def requests_retry_session(
        self,
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get(self, url: str, **kwargs) -> requests.Response:
        headers = self.headers
        if "headers" in kwargs:
            headers = kwargs["headers"]
        with requests.Session() as session:
            session.headers.update(headers)
            response = self.requests_retry_session(session=session).get(url=url)
        return response

    def post(self, url: str, **kwargs) -> requests.Response:
        headers = self.headers
        if "headers" in kwargs:
            headers = kwargs["headers"]
        with requests.Session() as session:
            data = kwargs.get("data") if kwargs.get("data") is not None else {}
            session.headers.update(headers)
            response = self.requests_retry_session(session=session).post(url, data=data)
