import os

from requests.models import Response

from .config import REQUEST_ACCEPTED
from .config import STABLE_DIFFUSION_3D_EP
from .config import STABLE_DIFFUSION_BASE_EP
from .config import STABLE_DIFFUSION_ITI_EP
from .config import STABLE_DIFFUSION_ITV_RESULT_EP
from .config import STABLE_DIFFUSION_ITV_START_EP
from .config import STABLE_DIFFUSION_RESULT_EP
from .config import STABLE_DIFFUSION_TTI_EP
from .config import WAIT_FOR_STABLE_DIFFUSION_ITI_RESULT
from .config import WAIT_FOR_STABLE_DIFFUSION_ITV_RESULT
from .multipart_formdata_model import MultipartFormdataModel


class StableDiffusionTextToImage(MultipartFormdataModel):
    """
    Text-to-Image
    Flagship model of Stable Diffusion
    LLMMaster no longer supports Stable Diffusion 3
    model: ultra, core
    output_format: 'png', 'jpeg', 'webp'
    aspect_ratio: '1:1', '16:9', '21:9', '2:3', '3:2',
        '4:5', '5:4', '9:16', '9:21'
    style_preset: 'anime', '3d-model', 'analog-film', 'cinematic',
        'comic-book', 'digital-art', 'enhance', 'fantasy-art', 'isometric',
        'line-art', 'low-poly', 'modeling-compound', 'neon-punk', 'origami',
        'photographic', 'pixel-art', 'tile-texture'
    """

    def run(self) -> None:
        url = (
            f"{STABLE_DIFFUSION_BASE_EP}{STABLE_DIFFUSION_TTI_EP}/"
            f"{self.parameters['model']}"
        )
        response = self._call_llm(url=url)
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _config_headers(self) -> None:
        self.extra_headers = {"Accept": "application/json"}

    def _body(self) -> dict:
        """
        Specific parameters:
          - prompt (required): str
          - aspect_ratio: str
          - negative_prompt: str
          - seed: int
          - style_preset: str
          - output_format: str
        """
        body = {"prompt": self.parameters["prompt"]}

        if "aspect_ratio" in self.parameters:
            body["aspect_ratio"] = self.parameters["aspect_ratio"]

        if "negative_prompt" in self.parameters:
            body["negative_prompt"] = self.parameters["negative_prompt"]

        if "seed" in self.parameters:
            body["seed"] = str(self.parameters["seed"])

        if "style_preset" in self.parameters:
            body["style_preset"] = self.parameters["style_preset"]

        if "output_format" in self.parameters:
            body["output_format"] = self.parameters["output_format"]

        return body


class StableDiffusionImageToImage(MultipartFormdataModel):
    """
    Image-to-Image
    Modes:
      - upscale/conservative
      - upscale/creative
      - upscale/fast
      - edit/erase
      - edit/inpaint
      - edit/outpaint
      - edit/search-and-replace
      - edit/search-and-recolor
      - edit/remove-background
      - edit/replace-background-and-relight
    """

    def run(self) -> None:
        url = (
            f"{STABLE_DIFFUSION_BASE_EP}{STABLE_DIFFUSION_ITI_EP}/"
            f"{self.parameters['mode']}"
        )
        response = self._call_llm(url=url)
        if (
            self.parameters["mode"] == "upscale/creative" or
            self.parameters["mode"] == "edit/replace-background-and-relight"
        ):
            if not isinstance(response, Response):
                raise ValueError("task request failed, not a valid response")
            response = self._fetch_result(
                url=(
                    STABLE_DIFFUSION_BASE_EP +
                    STABLE_DIFFUSION_RESULT_EP.format(
                        id=response.json().get("id")
                    )
                ),
                wait_time=WAIT_FOR_STABLE_DIFFUSION_ITI_RESULT
            )
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _config_headers(self) -> None:
        self.extra_headers = {"Accept": "application/json"}

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.status_code == REQUEST_ACCEPTED

    def _body(self) -> dict:
        """
        Specific parameters:
          - prompt: str
          - search_prompt (required): str, search prompt
          - creativity: float, creativity value
          - negative_prompt: str, negative prompt
          - select_prompt: str, select prompt
          - seed: int, seed value
          - output_format: str, output format
          - mask: str, path to mask file
          - grow_mask: int, grow mask value
          - left: int, left value
          - right: int, right value
          - up: int, up value
          - down: int, down value
          - style_preset: str
        Special parameters for Replace Background and Relight:
          - background_reference: str/binary image
          - background_prompt: str
          - foreground_prompt: str
          - preserve_original_subject: float
          - original_background_depth: float
          - keep_original_background: bool
          - light_source_direction: str, above/below/left/right
          - light_reference: str/binary image
          - light_source_strength: float
        Notes for edit/replace-background-and-relight:
          1. For commonization, `image` is used instead of `subject_image`.
          2. Use either `background_reference` or `background_prompt`.
          3. Use either `light_reference` or `light_source_direction`.
        """
        image_key = (
            "subject_image"
            if self.parameters["mode"] == "edit/replace-background-and-relight"
            else "image"
        )
        body = {
            image_key: (
                os.path.split(self.parameters["image"])[1],
                open(self.parameters["image"], "rb"),
                "application/json"
            )
        }

        if "prompt" in self.parameters:
            body["prompt"] = self.parameters["prompt"]

        if "search_prompt" in self.parameters:
            body["search_prompt"] = self.parameters["search_prompt"]

        if "creativity" in self.parameters:
            body["creativity"] = str(self.parameters["creativity"])

        if "negative_prompt" in self.parameters:
            body["negative_prompt"] = self.parameters["negative_prompt"]

        if "select_prompt" in self.parameters:
            body["select_prompt"] = self.parameters["select_prompt"]

        if "seed" in self.parameters:
            body["seed"] = str(self.parameters["seed"])

        if "output_format" in self.parameters:
            body["output_format"] = self.parameters["output_format"]

        if "mask" in self.parameters:
            body["mask"] = (
                os.path.split(self.parameters["mask"])[1],
                open(self.parameters["mask"], "rb"),
                "application/json"
            )

        if "grow_mask" in self.parameters:
            body["grow_mask"] = str(self.parameters["grow_mask"])

        if "left" in self.parameters:
            body["left"] = str(self.parameters["left"])

        if "right" in self.parameters:
            body["right"] = str(self.parameters["right"])

        if "up" in self.parameters:
            body["up"] = str(self.parameters["up"])

        if "down" in self.parameters:
            body["down"] = str(self.parameters["down"])

        if "style_preset" in self.parameters:
            body["style_preset"] = self.parameters["style_preset"]

        if "background_reference" in self.parameters:
            body["background_reference"] = (
                os.path.split(self.parameters["background_reference"])[1],
                open(self.parameters["background_reference"], "rb"),
                "application/json"
            )

        if "background_prompt" in self.parameters:
            body["background_prompt"] = self.parameters["background_prompt"]

        if "foreground_prompt" in self.parameters:
            body["foreground_prompt"] = self.parameters["foreground_prompt"]

        if "preserve_original_subject" in self.parameters:
            body["preserve_original_subject"] = str(
                self.parameters["preserve_original_subject"]
            )

        if "original_background_depth" in self.parameters:
            body["original_background_depth"] = str(
                self.parameters["original_background_depth"]
            )

        if 'keep_original_background' in self.parameters:
            body["keep_original_background"] = str(
                self.parameters["keep_original_background"]
            ).lower()

        if 'light_source_direction' in self.parameters:
            body["light_source_direction"] = self.parameters[
                "light_source_direction"
            ]

        if 'light_reference' in self.parameters:
            body['light_reference'] = (
                os.path.split(self.parameters["light_reference"])[1],
                open(self.parameters["light_reference"], "rb"),
                "application/json"
            )

        if 'light_source_strength' in self.parameters:
            body["light_source_strength"] = str(
                self.parameters["light_source_strength"]
            )

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - image
          - mode
        """
        parameters = kwargs

        if "image" not in kwargs or not os.path.isfile(kwargs["image"]):
            msg = "parameter `image` is not given or not a valid file"
            raise ValueError(msg)

        if "mode" not in kwargs:
            msg = "parameter `mode` is not given"
            raise ValueError(msg)

        return parameters


class StableDiffusionImageToVideo(MultipartFormdataModel):
    """
    Image-to-Video
    """

    def run(self) -> None:
        response = self._call_llm(
            url=STABLE_DIFFUSION_BASE_EP+STABLE_DIFFUSION_ITV_START_EP
        )
        if isinstance(response, Response):
            response = self._fetch_result(
                url=(
                    STABLE_DIFFUSION_BASE_EP +
                    STABLE_DIFFUSION_ITV_RESULT_EP.format(
                        id=response.json().get("id")
                    )
                ),
                wait_time=WAIT_FOR_STABLE_DIFFUSION_ITV_RESULT
            )
        self.response = response

    def _config_headers(self) -> None:
        self.extra_headers = {"Accept": "video/*"}

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.status_code == REQUEST_ACCEPTED

    def _body(self) -> dict:
        """
        Specific parameters:
          - image (required): local image path
            - format: jpg or png
            - resolution: 1024x576, 576x1024, 768x768
          - seed: int
          - cfg_scale: int
          - motion_bucket_id: int
        """
        body = {
            "image": (
                os.path.split(self.parameters["image"])[1],
                open(self.parameters["image"], "rb"),
                "application/json"
            )
        }

        if "seed" in self.parameters:
            body["seed"] = str(self.parameters["seed"])

        if "cfg_scale" in self.parameters:
            body["cfg_scale"] = str(self.parameters["cfg_scale"])

        if "motion_bucket_id" in self.parameters:
            body["motion_bucket_id"] = str(self.parameters["motion_bucket_id"])

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - image
        """
        parameters = kwargs

        if "image" not in kwargs or not os.path.isfile(kwargs["image"]):
            msg = "parameter `image` is not given or not a valid file"
            raise ValueError(msg)

        return parameters


class StableDiffusionImageTo3D(MultipartFormdataModel):
    """
    Image-to-3D
    Modes:
      - stable-fast-3d
      - stable-point-aware-3d
    """

    def run(self) -> None:
        url = (
            f"{STABLE_DIFFUSION_BASE_EP}{STABLE_DIFFUSION_3D_EP}/"
            f"{self.parameters['mode']}"
        )
        self.response = self._call_llm(url=url)

    def _config_headers(self) -> None:
        self.extra_headers = {"Accept": "image/*"}

    def _body(self) -> dict:
        """
        Specific parameters:
          - texture_resolution: str, 512/1024/2048
          - foreground_ratio: float
          - remesh: quad/triangle
        Additional parameters for Stable Fast 3D:
          - vertex_count: int, between -1 and 20000
        Additional parameters for Stable Point Aware 3D:
          - target_type: str, face/vertex
          - target_count: int, between 100 and 20000
          - guidance_scale: int, between 1 and 10
          - seed: int
        """
        body = {
            "image": (
                os.path.split(self.parameters["image"])[1],
                open(self.parameters["image"], "rb"),
                "application/json"
            )
        }

        if "texture_resolution" in self.parameters:
            body["texture_resolution"] = self.parameters[
                "texture_resolution"
            ]

        if "foreground_ratio" in self.parameters:
            body["foreground_ratio"] = str(self.parameters["foreground_ratio"])

        if "remesh" in self.parameters:
            body["remesh"] = self.parameters["remesh"]

        if "vertex_count" in self.parameters:
            body["vertex_count"] = str(self.parameters["vertex_count"])

        if "target_type" in self.parameters:
            body["target_type"] = self.parameters["target_type"]

        if "target_count" in self.parameters:
            body["target_count"] = str(self.parameters["target_count"])

        if "guidance_scale" in self.parameters:
            body["guidance_scale"] = str(self.parameters["guidance_scale"])

        if "seed" in self.parameters:
            body["seed"] = str(self.parameters["seed"])

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - image
          - mode
        """
        parameters = kwargs

        if "image" not in kwargs or not os.path.isfile(kwargs["image"]):
            msg = "parameter `image` is not given or not a valid file"
            raise ValueError(msg)

        if "mode" not in kwargs:
            msg = "parameter `mode` is not given"
            raise ValueError(msg)

        return parameters
