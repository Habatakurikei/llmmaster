from requests.models import Response

from .config import MESHY_BASE_EP
from .config import MESHY_IT3D_EP
from .config import MESHY_MODE_PREVIEW
from .config import MESHY_MODE_REFINE
from .config import MESHY_REMESH_EP
from .config import MESHY_STATUS_IN_PROGRESS
from .config import MESHY_TT3D_EP
from .config import MESHY_TTTX_EP
from .config import WAIT_FOR_MESHY_RESULT
from .root_model import RootModel
from .utils import meshy_image_input


class MeshyBase(RootModel):
    """
    Base model for Meshy API wrapper.
    Meshy provides:
      1. Text-To-3D model (meshy_tt3d)
      2. Text-To-3D refine (meshy_tt3d_refine)
      3. Image-To-3D model (meshy_it3d)
      4. Remesh model (meshy_remesh)
      5. Text-To-Texture model (meshy_tttx)
    2025-02-04: Text-To-Voxel model (meshy_ttvx) is deprecated.
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in MeshyBase"
            raise Exception(msg) from e

    def _call_llm(self, url: str = '') -> any:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=url)
        if isinstance(response, Response):
            response = self._fetch_result(
                url=f"{url}/{response.json().get('result')}",
                wait_time=WAIT_FOR_MESHY_RESULT
            )
        return response.json() if isinstance(response, Response) else response

    def _is_task_ongoing(self, response: Response) -> bool:
        return response.json().get("status") in MESHY_STATUS_IN_PROGRESS


class MeshyTextTo3D(MeshyBase):
    """
    Text-To-3D
    2025-02-04: renamed as preview mode
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{MESHY_BASE_EP}{MESHY_TT3D_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - mode (required): `preview`
          - art_style: str
          - seed: int
          - ai_model: str
          - topology (only for meshy-4): str
          - target_polycount (only for meshy-4): int
          - should_remesh: bool
          - symmetry_mode: off/on/auto
        """
        body = {
            "mode": MESHY_MODE_PREVIEW,
            "prompt": self.parameters["prompt"]
        }

        if "art_style" in self.parameters:
            body["art_style"] = self.parameters["art_style"]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        # support legacy model parameter
        if "ai_model" in self.parameters:
            body["ai_model"] = self.parameters["ai_model"]
        elif self.parameters.get("model") != "dummy":
            body["ai_model"] = self.parameters["model"]

        if "topology" in self.parameters:
            body["topology"] = self.parameters["topology"]

        if "target_polycount" in self.parameters:
            body["target_polycount"] = self.parameters["target_polycount"]

        if "should_remesh" in self.parameters:
            body["should_remesh"] = self.parameters["should_remesh"]

        if "symmetry_mode" in self.parameters:
            body["symmetry_mode"] = self.parameters["symmetry_mode"]

        return body


class MeshyTextTo3DRefine(MeshyBase):
    """
    Text-To-3D Refine
    Use this class after made base model with MeshyTextTo3D.
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{MESHY_BASE_EP}{MESHY_TT3D_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - mode (required): `refine`
          - preview_task_id (required): str
          - enable_pbr: bool
        """
        body = {
            "mode": MESHY_MODE_REFINE,
            "preview_task_id": self.parameters["preview_task_id"],
        }

        if "enable_pbr" in self.parameters:
            body["enable_pbr"] = self.parameters["enable_pbr"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - preview_task_id
        """
        parameters = kwargs

        if "preview_task_id" not in kwargs:
            msg = "parameter `preview_task_id` is required"
            raise ValueError(msg)

        return parameters


class MeshyImageTo3D(MeshyBase):
    """
    Image-To-3D
    Acceptable input file types: jpg, jpeg and png
    Both local file path and online URLs are supported
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{MESHY_BASE_EP}{MESHY_IT3D_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - image_url (required): source image path
          - ai_model: str
          - topology (only for meshy-4): str
          - target_polycount (only for meshy-4): int
          - should_remesh: bool
          - enable_pbr: bool
          - should_texture: bool
          - symmetry_mode: off/on/auto
        """
        body = {"image_url": meshy_image_input(self.parameters["image_url"])}

        # support legacy model parameter
        if "ai_model" in self.parameters:
            body["ai_model"] = self.parameters["ai_model"]
        elif self.parameters.get("model") != "dummy":
            body["ai_model"] = self.parameters["model"]

        if "topology" in self.parameters:
            body["topology"] = self.parameters["topology"]

        if "target_polycount" in self.parameters:
            body["target_polycount"] = self.parameters["target_polycount"]

        if "should_remesh" in self.parameters:
            body["should_remesh"] = self.parameters["should_remesh"]

        if "enable_pbr" in self.parameters:
            body["enable_pbr"] = self.parameters["enable_pbr"]

        if "should_texture" in self.parameters:
            body["should_texture"] = self.parameters["should_texture"]

        if "symmetry_mode" in self.parameters:
            body["symmetry_mode"] = self.parameters["symmetry_mode"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - image_url
        """
        parameters = kwargs

        if "image_url" not in kwargs:
            msg = "parameter `image_url` is required"
            raise ValueError(msg)

        return parameters


class MeshyRemeshModel(MeshyBase):
    """
    Remesh model
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{MESHY_BASE_EP}{MESHY_REMESH_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - input_task_id (required): str
          - target_formats: list of str from glb, fbx, obj, usdz, blend, stl
          - topology: str
          - target_polycount: int
          - resize_height: float
          - origin_at: str
        """
        body = {
            "input_task_id": self.parameters["input_task_id"],
        }

        if "target_formats" in self.parameters:
            body["target_formats"] = self.parameters["target_formats"]

        if "topology" in self.parameters:
            body["topology"] = self.parameters["topology"]

        if "target_polycount" in self.parameters:
            body["target_polycount"] = self.parameters["target_polycount"]

        if "resize_height" in self.parameters:
            body["resize_height"] = self.parameters["resize_height"]

        if "origin_at" in self.parameters:
            body["origin_at"] = self.parameters["origin_at"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - input_task_id
        """
        parameters = kwargs

        if "input_task_id" not in kwargs:
            msg = "parameter `input_task_id` is required"
            raise ValueError(msg)

        return parameters


class MeshyTextToTexture(MeshyBase):
    """
    Text-To-Texture
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{MESHY_BASE_EP}{MESHY_TTTX_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - model_url (required): str
          - object_prompt (required): str
          - style_prompt (required): str
          - enable_original_uv: bool
          - enable_pbr: bool
          - resolution: str, 1024/2048/4096
          - negative_prompt: str
          - art_style: str
        """
        body = {
            "model_url": self.parameters["model_url"],
            "object_prompt": self.parameters["object_prompt"],
            "style_prompt": self.parameters["style_prompt"],
        }

        if "enable_original_uv" in self.parameters:
            body["enable_original_uv"] = self.parameters["enable_original_uv"]

        if "enable_pbr" in self.parameters:
            body["enable_pbr"] = self.parameters["enable_pbr"]

        if "resolution" in self.parameters:
            body["resolution"] = self.parameters["resolution"]

        if "negative_prompt" in self.parameters:
            body["negative_prompt"] = self.parameters["negative_prompt"]

        if "art_style" in self.parameters:
            body["art_style"] = self.parameters["art_style"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - model_url
          - object_prompt
          - style_prompt
        """
        parameters = kwargs

        if "model_url" not in kwargs:
            msg = "parameter `model_url` is required"
            raise ValueError(msg)

        if "object_prompt" not in kwargs:
            msg = "parameter `object_prompt` is required"
            raise ValueError(msg)

        if "style_prompt" not in kwargs:
            msg = "parameter `style_prompt` is required"
            raise ValueError(msg)

        return parameters
