import time
from threading import Thread

from requests import request
from requests.models import Response

from .config import POSITIVE_RESPONSE_CODES


class RootModel(Thread):
    """
    The root model for all models defined in LLM Master.
    2025-01-10: renamed from BaseModel to RootModel, and revised the code.
    """

    def __init__(self, api_key: str = '', **kwargs) -> None:
        """
        Arguments in kwargs:
          - model: model name defined by provider
          - prompt: message or request to model
          - additional args: parameters for different model type
            (e.g. max_tokens, temperature, size, quality, etc.)
        2024-09-03: added new argument `api_key`
        2025-01-17: removed self.headers and consolidated self.payload.
        2025-02-12: added _config_headers() method.
        """
        super().__init__()
        self.api_key = api_key
        self.parameters = self._verify_arguments(**kwargs)
        self._config_headers()
        self.payload = {}
        self.response = ''

    def run(self) -> None:
        """
        This method is used for multi-threading.
        Implement run method for each model of sub-class.
        Must set anything to self.response as return value.
        """
        pass

    def _call_rest_api(self, url: str = '') -> any:
        """
        Call common REST API using requests library.
        Returns `requests.models.Response` that contains various data types.
        Handle the returned object in run() method of each sub-class.
        """
        to_return = "Something went wrong. "

        try:
            response = request(method="POST", url=url, **self.payload)

            if response.status_code in POSITIVE_RESPONSE_CODES:
                to_return = response
            else:
                msg = f"{response.status_code} - {response.text}"
                to_return += msg

        except Exception as e:
            to_return += str(e)

        return to_return

    def _fetch_result(
        self,
        url: str = '',
        wait_time: float = 5.0
    ) -> any:
        """
        Common function to fetch result through GET request.
          url: endpoint that must include task_id or other identifier.
          wait_time: time to wait for next GET request.
        """
        headers = self._headers()
        flg = True
        while flg:
            response = request(method="GET", url=url, headers=headers)
            if self._is_task_ongoing(response):
                self._wait(wait_time)
            else:
                flg = False

        return response

    def _is_task_ongoing(self, response: Response) -> bool:
        """
        Check if content generation task has stopped by vendor.
        Implement this method in each sub-class.
        """
        if response:
            pass
        return False

    def _headers(self) -> dict:
        """
        Set headers before using _call_rest_api().
        """
        headers = {}

        auth_header = getattr(self, "auth_header", "Authorization")
        auth_prefix = getattr(self, "auth_prefix", "Bearer ")
        content_type = getattr(self, "content_type", "application/json")
        extra_headers = getattr(self, "extra_headers", None)

        if auth_header:
            headers[auth_header] = f"{auth_prefix}{self.api_key}"

        if content_type:
            headers["Content-Type"] = content_type

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def _config_headers(self) -> None:
        """
        Configure header parameters here before calling _headers().
          - self.auth_header: str
          - self.auth_prefix: str
          - self.content_type: str
          - self.extra_headers: dict or None
        Implement this method in each sub-class if needed.
        No implemenation needed for the following standard case:
        {
            'Authorization': 'Bearer <api_key>',
            'Content-Type': 'application/json'
        }
        """
        pass

    def _body(self) -> dict:
        """
        Make request body for REST API including json and files.
        Implement this method in each sub-class.
        """
        return {}

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Verify arguments before summoning a model in LLMMaster.
        Implement this method in each sub-class.
        """
        return kwargs

    def _wait(self, to_wait: float) -> None:
        time.sleep(to_wait)
