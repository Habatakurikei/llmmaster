from requests import request
from requests.models import Response

from .config import FAL_BASE_EP
from .config import FAL_STATUS_IN_PROGRESS
from .config import FLUX1_FAL_ITI_EP
from .config import FLUX1_FAL_TTI_EP
from .config import WAIT_FOR_FLUX1_FAL_RESULT
from .root_model import RootModel


class Flux1FalBase(RootModel):
    """
    Base class for Flux1Fal models
      1. Text-To-Image model (flux1_fal_tti)
      2. Image-To-Image model (flux1_fal_iti)
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in Flux1FalBase"
            raise Exception(msg) from e

    def _call_llm(self, url: str) -> any:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=url)
        if isinstance(response, Response):
            response = self._fetch_result(
                url=response.json().get("status_url"),
                wait_time=WAIT_FOR_FLUX1_FAL_RESULT
            )
            if isinstance(response, Response):
                response = request(
                    "GET",
                    headers=self._headers(),
                    url=response.json().get("response_url")
                )
        return response.json() if isinstance(response, Response) else response

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.json().get("status") in FAL_STATUS_IN_PROGRESS

    def _config_headers(self) -> None:
        self.auth_prefix = "Key "


class Flux1FalTextToImage(Flux1FalBase):
    """
    Text-To-Image
      - dev
      - schnell
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=f"{FAL_BASE_EP}{FLUX1_FAL_TTI_EP}/{self.parameters['model']}"
        )

    def _body(self) -> dict:
        """
        Specific parameters:
          - image_size: str or dict
            - str: square_hd, square, portrait_4_3, portrait_16_9,
              landscape_4_3, landscape_16_9
            - dict: width, height
          - num_inference_steps: int
          - seed: int
          - guidance_scale: float
          - sync_mode: bool
          - num_images: int
          - enable_safety_checker: bool
        Note: sync_mode is fixed True
        """
        body = {"prompt": self.parameters["prompt"], "sync_mode": True}

        if "image_size" in self.parameters:
            body["image_size"] = self.parameters["image_size"]

        if "num_inference_steps" in self.parameters:
            body["num_inference_steps"] = self.parameters[
                "num_inference_steps"
            ]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "guidance_scale" in self.parameters:
            body["guidance_scale"] = self.parameters["guidance_scale"]

        if "num_images" in self.parameters:
            body["num_images"] = self.parameters["num_images"]

        if "enable_safety_checker" in self.parameters:
            body["enable_safety_checker"] = self.parameters[
                "enable_safety_checker"
            ]

        return body


class Flux1FalImageToImage(Flux1FalBase):
    """
    Image-To-Image
      - dev/image-to-image
      - dev/redux
      - schnell/redux
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=f"{FAL_BASE_EP}{FLUX1_FAL_ITI_EP}/{self.parameters['model']}"
        )

    def _body(self) -> dict:
        """
        Specific parameters:
          - image_url (required): str of URL or base64 encoded image
          - strength: float
          - num_inference_steps: int
          - seed: int
          - guidance_scale: float
          - sync_mode: bool
          - num_images: int
          - enable_safety_checker: bool
        Only for Redux:
          - image_size: str
        Note:
          - prompt is required only for dev/image-to-image
          - sync_mode is fixed True
        """
        body = {"sync_mode": True}

        if "prompt" in self.parameters:
            body["prompt"] = self.parameters["prompt"]

        if "image_url" in self.parameters:
            body["image_url"] = self.parameters["image_url"]

        if "strength" in self.parameters:
            body["strength"] = self.parameters["strength"]

        if "image_size" in self.parameters:
            body["image_size"] = self.parameters["image_size"]

        if "num_inference_steps" in self.parameters:
            body["num_inference_steps"] = self.parameters[
                "num_inference_steps"
            ]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "guidance_scale" in self.parameters:
            body["guidance_scale"] = self.parameters["guidance_scale"]

        if "num_images" in self.parameters:
            body["num_images"] = self.parameters["num_images"]

        if "enable_safety_checker" in self.parameters:
            body["enable_safety_checker"] = self.parameters[
                "enable_safety_checker"
            ]

        return body
