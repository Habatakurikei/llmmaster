from requests.models import Response

from .config import RUNWAY_BASE_EP
from .config import RUNWAY_ITV_EP
from .config import RUNWAY_RESULT_EP
from .config import RUNWAY_STATUS_IN_PROGRESS
from .config import RUNWAY_VERSION
from .config import WAIT_FOR_RUNWAY_RESULT
from .root_model import RootModel


class RunwayBase(RootModel):
    """
    Base model for Runway API wrapper.
    Runway provides:
      1. Image-To-Video model (runway_itv)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in RunwayBase"
            raise Exception(msg) from e

    def _call_llm(self, url: str = '') -> any:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=url)
        if isinstance(response, Response):
            response = self._fetch_result(
                url=(
                    RUNWAY_BASE_EP +
                    RUNWAY_RESULT_EP.format(id=response.json().get("id"))
                ),
                wait_time=WAIT_FOR_RUNWAY_RESULT
            )
        return response.json() if isinstance(response, Response) else response

    def _config_headers(self) -> None:
        self.extra_headers = {"X-Runway-Version": RUNWAY_VERSION}

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.json().get("status") in RUNWAY_STATUS_IN_PROGRESS

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - x_runway_version
        """
        parameters = kwargs

        if "x_runway_version" not in kwargs:
            parameters["x_runway_version"] = RUNWAY_VERSION

        return parameters


class RunwayImageToVideo(RunwayBase):
    """
    Image-To-Video
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{RUNWAY_BASE_EP}{RUNWAY_ITV_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - promptImage (required): str or list of dict
          - model (required): str
          - promptText: str
          - seed: int
          - watermark: bool
          - duration: int (5 or 10)
          - ratio: str
        """
        body = {
            "model": self.parameters["model"],
            "promptImage": self.parameters["promptImage"]
        }

        if "prompt" in self.parameters:
            body["promptText"] = self.parameters["prompt"]
        elif "promptText" in self.parameters:
            body["promptText"] = self.parameters["promptText"]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "watermark" in self.parameters:
            body["watermark"] = self.parameters["watermark"]

        if "duration" in self.parameters:
            body["duration"] = self.parameters["duration"]

        if "ratio" in self.parameters:
            body["ratio"] = self.parameters["ratio"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - promptImage
        """
        parameters = super()._verify_arguments(**kwargs)

        if "promptImage" not in kwargs:
            msg = "parameter `promptImage` is required"
            raise ValueError(msg)

        return parameters
