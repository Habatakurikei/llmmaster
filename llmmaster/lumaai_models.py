from requests.models import Response

from .config import LUMAAI_BASE_EP
from .config import LUMAAI_ITI_EP
from .config import LUMAAI_ITV_EP
from .config import LUMAAI_RESULT_EP
from .config import LUMAAI_STATUS_IN_PROGRESS
from .config import LUMAAI_TTI_EP
from .config import LUMAAI_TTV_EP
from .config import LUMAAI_VTV_EP
from .config import WAIT_FOR_LUMAI_RESULT
from .root_model import RootModel


class LumaAIBase(RootModel):
    """
    Base model for Luma AI API wrapper.
    Luma AI provides:
      1. Text-To-Image (lumaai_tti)
      2. Image-To-Image (lumaai_iti)
      3. Text-To-Video (lumaai_ttv)
      4. Image-To-Video (lumaai_itv)
      5. Video-To-Video (lumaai_vtv)
    Only online images and videos are acceptable for input.
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in LumaAIBase"
            raise Exception(msg) from e

    def _call_llm(self, url: str) -> any:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=LUMAAI_BASE_EP+url)
        if isinstance(response, Response):
            fetch_url = LUMAAI_BASE_EP + LUMAAI_RESULT_EP.format(
                id=response.json().get("id")
            )
            response = self._fetch_result(
                url=fetch_url,
                wait_time=WAIT_FOR_LUMAI_RESULT
            )
        return response.json() if isinstance(response, Response) else response

    def _config_headers(self) -> None:
        self.extra_headers = {"Accept": "application/json"}

    def _body(self) -> dict:
        return {
            "prompt": self.parameters["prompt"],
            "model": self.parameters["model"]
        }

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.json().get("state") in LUMAAI_STATUS_IN_PROGRESS


class LumaAITextToImage(LumaAIBase):
    """
    Text-To-Image
    """

    def run(self) -> any:
        self.response = self._call_llm(LUMAAI_TTI_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - aspect_ratio: str
        """
        body = super()._body()

        if "aspect_ratio" in self.parameters:
            body["aspect_ratio"] = self.parameters["aspect_ratio"]

        return body


class LumaAIImageToImage(LumaAIBase):
    """
    Image-To-Image
    """

    def run(self) -> any:
        self.response = self._call_llm(LUMAAI_ITI_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - image_ref: list of dict
          - style_ref: list of dict
          - character_ref: list of dict
          - modify_image_ref: list of dict
        """
        body = super()._body()

        if "image_ref" in self.parameters:
            body["image_ref"] = self.parameters["image_ref"]

        if "style_ref" in self.parameters:
            body["style_ref"] = self.parameters["style_ref"]

        if "character_ref" in self.parameters:
            body["character_ref"] = self.parameters["character_ref"]

        if "modify_image_ref" in self.parameters:
            body["modify_image_ref"] = self.parameters["modify_image_ref"]

        return body


class LumaAITextToVideo(LumaAIBase):
    """
    Text-To-Video
    """

    def run(self) -> any:
        self.response = self._call_llm(LUMAAI_TTV_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - aspect_ratio: str
          - loop: bool
          - resolution: str, 720p
          - duration: str, 5s/9s
        """
        body = super()._body()

        if "aspect_ratio" in self.parameters:
            body["aspect_ratio"] = self.parameters["aspect_ratio"]

        if "loop" in self.parameters:
            body["loop"] = self.parameters["loop"]

        if "resolution" in self.parameters:
            body["resolution"] = self.parameters["resolution"]

        if "duration" in self.parameters:
            body["duration"] = self.parameters["duration"]

        return body


class LumaAIImageToVideo(LumaAIBase):
    """
    Image-To-Video
    """

    def run(self) -> any:
        self.response = self._call_llm(LUMAAI_ITV_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - aspect_ratio: str
          - loop: bool
          - keyframes: dict of frame0 and frame1
        """
        body = super()._body()

        if "aspect_ratio" in self.parameters:
            body["aspect_ratio"] = self.parameters["aspect_ratio"]

        if "loop" in self.parameters:
            body["loop"] = self.parameters["loop"]

        if "keyframes" in self.parameters:
            body["keyframes"] = self.parameters["keyframes"]

        return body


class LumaAIVideoToVideo(LumaAIBase):
    """
    Video-To-Video
    Extension (forward/backward) and Interpolation
    """

    def run(self) -> any:
        self.response = self._call_llm(LUMAAI_VTV_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - aspect_ratio: str
          - loop: bool
          - resolution: str, 720p
          - duration: str, 5s/9s
          - keyframes: dict of frame0 and frame1
        """
        body = super()._body()

        if "aspect_ratio" in self.parameters:
            body["aspect_ratio"] = self.parameters["aspect_ratio"]

        if "loop" in self.parameters:
            body["loop"] = self.parameters["loop"]

        if "resolution" in self.parameters:
            body["resolution"] = self.parameters["resolution"]

        if "duration" in self.parameters:
            body["duration"] = self.parameters["duration"]

        if "keyframes" in self.parameters:
            body["keyframes"] = self.parameters["keyframes"]

        return body
