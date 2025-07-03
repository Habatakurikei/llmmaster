from requests.models import Response

from .config import SKYBOX_BASE_EP
from .config import SKYBOX_EXPORT_EP
from .config import SKYBOX_EXPORT_RESULT_EP
from .config import SKYBOX_GENERATION_EP
from .config import SKYBOX_GENERATION_RESULT_EP
from .config import SKYBOX_STATUS_IN_PROGRESS
from .config import WAIT_FOR_SKYBOX_RESULT
from .config import X_API_KEY
from .root_model import RootModel


class SkyboxBase(RootModel):
    """
    Base model for Skybox API wrapper.
    Skybox provides:
      1. text_to_panorama (skybox_ttp)
      2. panorama_to_image/video (skybox_ptiv)
    Note: officially panorama_to_image/video is called export.
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in SkyboxBase"
            raise Exception(msg) from e

    def _call_llm(self, request_url: str = '', result_url: str = '') -> any:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=request_url)
        if isinstance(response, Response):
            response = self._fetch_result(
                url=result_url.format(id=response.json().get("id")),
                wait_time=WAIT_FOR_SKYBOX_RESULT
            )
        return response.json() if isinstance(response, Response) else response

    def _config_headers(self) -> None:
        self.auth_header = X_API_KEY
        self.auth_prefix = ''


class SkyboxTextToPanorama(SkyboxBase):
    """
    Text-To-Panorama
    """

    def run(self):
        self.response = self._call_llm(
            request_url=f"{SKYBOX_BASE_EP}{SKYBOX_GENERATION_EP}",
            result_url=f"{SKYBOX_BASE_EP}{SKYBOX_GENERATION_RESULT_EP}"
        )

    def _body(self):
        """
        Specific parameters:
          - skybox_style_id (required): int
          - negative_text: str
          - enhance_prompt: bool
          - seed: int
          - remix_imagine_id: int
          - control_image: binary/base64/url
          - control_model: str
          - webhook_url: str
        Note: prompt must be less than 2000 characters.
        """
        body = {
            "prompt": self.parameters["prompt"],
            "skybox_style_id": self.parameters["skybox_style_id"]
        }

        if "negative_text" in self.parameters:
            body["negative_text"] = self.parameters["negative_text"]

        if "enhance_prompt" in self.parameters:
            body["enhance_prompt"] = self.parameters["enhance_prompt"]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "remix_imagine_id" in self.parameters:
            body["remix_imagine_id"] = self.parameters["remix_imagine_id"]

        if "control_image" in self.parameters:
            body["control_image"] = self.parameters["control_image"]

        if "control_model" in self.parameters:
            body["control_model"] = self.parameters["control_model"]

        if "webhook_url" in self.parameters:
            body["webhook_url"] = self.parameters["webhook_url"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - skybox_style_id
        """
        parameters = kwargs

        if "skybox_style_id" not in kwargs:
            msg = "parameter `skybox_style_id` is required"
            raise ValueError(msg)

        return parameters

    def _is_task_ongoing(self, response: Response) -> bool:
        response_json = response.json()
        return response_json["request"]["status"] in SKYBOX_STATUS_IN_PROGRESS


class SkyboxPanoramaToImageVideo(SkyboxBase):
    """
    Panorama-To-Image/Video (export)
    """

    def run(self):
        self.response = self._call_llm(
            request_url=f"{SKYBOX_BASE_EP}{SKYBOX_EXPORT_EP}",
            result_url=f"{SKYBOX_BASE_EP}{SKYBOX_EXPORT_RESULT_EP}"
        )

    def _body(self):
        """
        Specific parameters:
          - skybox_id (required): str
          - type_id (required): int
            1: jpg, 2: png, 3: cube map,
            4: HDRI HDR, 5: HDRI EXR, 6: depth map,
            7: mp4 landscape, 8: mp4 portrait, 9: mp4 square
          - webhook_url: str
        """
        body = {
            "skybox_id": self.parameters["skybox_id"],
            "type_id": self.parameters["type_id"]
        }

        if "webhook_url" in self.parameters:
            body["webhook_url"] = self.parameters["webhook_url"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - skybox_id
          - type_id
        """
        parameters = kwargs

        if "skybox_id" not in kwargs:
            msg = "parameter `skybox_id` is required"
            raise ValueError(msg)

        if "type_id" not in kwargs:
            msg = "parameter `type_id` is required"
            raise ValueError(msg)

        return parameters

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.json().get("status") in SKYBOX_STATUS_IN_PROGRESS
