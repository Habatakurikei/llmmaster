import os

from requests.models import Response

from .config import TRIPO_BASE_EP
from .config import TRIPO_MODE_APRC
from .config import TRIPO_MODE_ARETARGET
from .config import TRIPO_MODE_ARIG
from .config import TRIPO_MODE_CONVERSION
from .config import TRIPO_MODE_IT3D
from .config import TRIPO_MODE_MV3D
from .config import TRIPO_MODE_REFINE
from .config import TRIPO_MODE_STYLIZE
from .config import TRIPO_MODE_TEXTURE
from .config import TRIPO_MODE_TT3D
from .config import TRIPO_RESULT_EP
from .config import TRIPO_STATUS_IN_PROGRESS
from .config import TRIPO_TASK_EP
from .config import WAIT_FOR_TRIPO_RESULT
from .root_model import RootModel
from .utils import tripo_image_input


class TripoBase(RootModel):
    """
    Base model for Tripo API wrapper.
    Tripo provides:
      1. text_to_model (tripo_tt3d)
      2. image_to_model (tripo_it3d)
      3. multiview_to_model (tripo_mv3d)
      4. texture_model (tripo_texture)
      5. refine_model (tripo_refine)
      6. animate_prerigcheck (tripo_aprc)
      7. animate_rig (tripo_arig)
      8. animate_retarget (tripo_aretarget)
      9. stylize_model (tripo_stylization)
      10. convert_model (tripo_conversion)
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in TripoBase"
            raise Exception(msg) from e

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        if isinstance(response, Response):
            response_json = response.json()
            response = self._fetch_result(
                url=(
                    TRIPO_BASE_EP +
                    TRIPO_RESULT_EP.format(
                        task_id=response_json["data"]["task_id"]
                    )
                ),
                wait_time=WAIT_FOR_TRIPO_RESULT
            )

        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _is_task_ongoing(self, response: Response) -> bool:
        response_json = response.json()
        return response_json["data"]["status"] in TRIPO_STATUS_IN_PROGRESS


class TripoTextTo3D(TripoBase):
    """
    Text-To-3D
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - model_version: str of model
          - negative_prompt: str
          - image_seed: int to determine process
          - model_seed: int to determine geometry
        Additional optional parameters:
          - face_limit: int
          - texture: bool, to enable texture
          - pbr: bool, to enable pbr
          - texture_seed: int
          - texture_quality: str, detailed, standard
          - auto_size: bool, True to make realistic size
          - style: str, define style
          - quad: bool, True to make quad mesh output
        """
        body = {
            "type": TRIPO_MODE_TT3D,
            "model_version": self.parameters["model"],
            "prompt": self.parameters["prompt"]
        }

        if "negative_prompt" in self.parameters:
            body["negative_prompt"] = self.parameters["negative_prompt"]

        if "image_seed" in self.parameters:
            body["image_seed"] = self.parameters["image_seed"]

        if "model_seed" in self.parameters:
            body["model_seed"] = self.parameters["model_seed"]

        if "face_limit" in self.parameters:
            body["face_limit"] = self.parameters["face_limit"]

        if "texture" in self.parameters:
            body["texture"] = self.parameters["texture"]

        if "pbr" in self.parameters:
            body["pbr"] = self.parameters["pbr"]

        if "texture_seed" in self.parameters:
            body["texture_seed"] = self.parameters["texture_seed"]

        if "texture_quality" in self.parameters:
            body["texture_quality"] = self.parameters["texture_quality"]

        if "auto_size" in self.parameters:
            body["auto_size"] = self.parameters["auto_size"]

        if "style" in self.parameters:
            body["style"] = self.parameters["style"]

        if "quad" in self.parameters:
            body["quad"] = self.parameters["quad"]

        return body


class TripoImageTo3D(TripoBase):
    """
    Image-To-3D
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - model_version: str of model
          - file (required): image input
          - model_seed: int to determine geometry
        Additional optional parameters:
          - face_limit: int
          - texture: bool, to enable texture
          - pbr: bool, to enable pbr
          - texture_seed: int
          - texture_quality: str, detailed, standard
          - auto_size: bool, True to make realistic size
          - style: str, define style
          - quad: bool, True to make quad mesh output
          - texture_alignment: original_image or geometry
          - orientation: align_image or default
        """
        body = {
            "type": TRIPO_MODE_IT3D,
            "model_version": self.parameters["model"],
            "file": tripo_image_input(
                image_path=self.parameters["file"],
                api_key=self.api_key
            )
        }

        if "model_seed" in self.parameters:
            body["model_seed"] = self.parameters["model_seed"]

        if "face_limit" in self.parameters:
            body["face_limit"] = self.parameters["face_limit"]

        if "texture" in self.parameters:
            body["texture"] = self.parameters["texture"]

        if "pbr" in self.parameters:
            body["pbr"] = self.parameters["pbr"]

        if "texture_seed" in self.parameters:
            body["texture_seed"] = self.parameters["texture_seed"]

        if "texture_quality" in self.parameters:
            body["texture_quality"] = self.parameters["texture_quality"]

        if "auto_size" in self.parameters:
            body["auto_size"] = self.parameters["auto_size"]

        if "style" in self.parameters:
            body["style"] = self.parameters["style"]

        if "quad" in self.parameters:
            body["quad"] = self.parameters["quad"]

        if "texture_alignment" in self.parameters:
            body["texture_alignment"] = self.parameters["texture_alignment"]

        if "orientation" in self.parameters:
            body["orientation"] = self.parameters["orientation"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - file
        """
        parameters = kwargs

        if "file" not in kwargs or not os.path.isfile(kwargs["file"]):
            msg = "parameter `file` is not given or not a valid file"
            raise ValueError(msg)

        return parameters


class TripoMultiviewTo3D(TripoBase):
    """
    Multiview-To-3D
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - model_version: str of model
          - files (required): list of dict - front, left, back, right
        Additional optional parameters:
          - face_limit: int
          - texture: bool, to enable texture
          - pbr: bool, to enable pbr
          - texture_seed: int
          - texture_alignment: original_image or geometry
          - texture_quality: str, detailed, standard
          - auto_size: bool, True to make realistic size
          - orientation: align_image or default
          - quad: bool, True to make quad mesh output
        """
        body = {
            "type": TRIPO_MODE_MV3D,
            "model_version": self.parameters["model"],
            "files": []
        }

        for file in self.parameters["files"]:
            body["files"].append(tripo_image_input(
                image_path=file,
                api_key=self.api_key
            ))

        if "face_limit" in self.parameters:
            body["face_limit"] = self.parameters["face_limit"]

        if "texture" in self.parameters:
            body["texture"] = self.parameters["texture"]

        if "pbr" in self.parameters:
            body["pbr"] = self.parameters["pbr"]

        if "texture_seed" in self.parameters:
            body["texture_seed"] = self.parameters["texture_seed"]

        if "texture_alignment" in self.parameters:
            body["texture_alignment"] = self.parameters["texture_alignment"]

        if "texture_quality" in self.parameters:
            body["texture_quality"] = self.parameters["texture_quality"]

        if "auto_size" in self.parameters:
            body["auto_size"] = self.parameters["auto_size"]

        if "orientation" in self.parameters:
            body["orientation"] = self.parameters["orientation"]

        if "quad" in self.parameters:
            body["quad"] = self.parameters["quad"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - files
        """
        parameters = kwargs

        if "files" not in kwargs or not isinstance(kwargs["files"], list):
            msg = "parameter `files` is not given or not a list"
            raise ValueError(msg)

        return parameters


class TripoTextureModel(TripoBase):
    """
    Texture Model from original generated by Tripo
    Note: model_id should be made by model_version>=v2.0-20240919.
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - original_model_task_id (required): str
          - texture: bool, to enable texture
          - pbr: bool, to enable pbr
          - texture_seed: int
          - texture_alignment: original_image or geometry
          - texture_quality: str, detailed, standard`
        """
        body = {
            "type": TRIPO_MODE_TEXTURE,
            "model_version": self.parameters["model"],
            "original_model_task_id": self.parameters[
                "original_model_task_id"
            ]
        }

        if "texture" in self.parameters:
            body["texture"] = self.parameters["texture"]

        if "pbr" in self.parameters:
            body["pbr"] = self.parameters["pbr"]

        if "texture_seed" in self.parameters:
            body["texture_seed"] = self.parameters["texture_seed"]

        if "texture_alignment" in self.parameters:
            body["texture_alignment"] = self.parameters["texture_alignment"]

        if "texture_quality" in self.parameters:
            body["texture_quality"] = self.parameters["texture_quality"]

        return body


class TripoRefineModel(TripoBase):
    """
    Refine Model from draft generated by Tripo
    Note: models of model_version>=v2.0-20240919 for refine is not suppoted.
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - draft_model_task_id (required): str
        """
        body = {
            "type": TRIPO_MODE_REFINE,
            "draft_model_task_id": self.parameters["draft_model_task_id"]
        }
        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - draft_model_task_id
        """
        parameters = kwargs

        if "draft_model_task_id" not in kwargs:
            msg = "parameter `draft_model_task_id` is not given"
            raise ValueError(msg)

        return parameters


class TripoAnimationPreRigCheck(TripoBase):
    """
    Animation Pre Rig Check
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - original_model_task_id (required): str
        """
        return {
            "type": TRIPO_MODE_APRC,
            "original_model_task_id": self.parameters[
                "original_model_task_id"
            ]
        }

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - original_model_task_id
        """
        parameters = kwargs

        if "original_model_task_id" not in kwargs:
            msg = "parameter `original_model_task_id` is not given"
            raise ValueError(msg)

        return parameters


class TripoAnimationRig(TripoBase):
    """
    Animation Rig
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - original_model_task_id (required): str
          - out_format: glb or fbx in str
        """
        body = {
            "type": TRIPO_MODE_ARIG,
            "original_model_task_id": self.parameters[
                "original_model_task_id"
            ]
        }

        if "out_format" in self.parameters:
            body["out_format"] = self.parameters["out_format"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - original_model_task_id
        """
        parameters = kwargs

        if "original_model_task_id" not in kwargs:
            msg = "parameter `original_model_task_id` is not given"
            raise ValueError(msg)

        return parameters


class TripoAnimationRetarget(TripoBase):
    """
    Animation Retarget
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - original_model_task_id (required): str
          - animation (required): str
          - out_format: glb or fbx in str
          - bake_animation: bool
        """
        body = {
            "type": TRIPO_MODE_ARETARGET,
            "original_model_task_id": self.parameters[
                "original_model_task_id"
            ],
            "animation": self.parameters["animation"]
        }

        if "out_format" in self.parameters:
            body["out_format"] = self.parameters["out_format"]

        if "bake_animation" in self.parameters:
            body["bake_animation"] = self.parameters["bake_animation"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - original_model_task_id
          - animation
        """
        parameters = kwargs

        if "original_model_task_id" not in kwargs:
            msg = "parameter `original_model_task_id` is not given"
            raise ValueError(msg)

        if "animation" not in kwargs:
            msg = "parameter `animation` is not given"
            raise ValueError(msg)

        return parameters


class TripoStylization(TripoBase):
    """
    Stylization
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - original_model_task_id (required): str
          - style (required): str
          - block_size: int (for only minecraft)
        """
        body = {
            "type": TRIPO_MODE_STYLIZE,
            "original_model_task_id": self.parameters[
                "original_model_task_id"
            ],
            "style": self.parameters["style"]
        }

        if "block_size" in self.parameters:
            body["block_size"] = self.parameters["block_size"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - original_model_task_id
          - style
        """
        parameters = kwargs

        if "original_model_task_id" not in kwargs:
            msg = "parameter `original_model_task_id` is not given"
            raise ValueError(msg)

        if "style" not in kwargs:
            msg = "parameter `style` is not given"
            raise ValueError(msg)

        return parameters


class TripoConversion(TripoBase):
    """
    Conversion
    """

    def _body(self) -> dict:
        """
        Specific parameters:
          - original_model_task_id (required): str
          - format (required): str
          - quad: bool
          - force_symmetry: bool
          - face_limit: int
          - flatten_bottom: bool
          - flatten_bottom_threshold: float
          - texture_size: int
          - texture_format: str
          - pivot_to_center_bottom: bool
          - scale_factor: int
        """
        body = {
            "type": TRIPO_MODE_CONVERSION,
            "original_model_task_id": self.parameters[
                "original_model_task_id"
            ],
            "format": self.parameters["format"]
        }

        if "quad" in self.parameters:
            body["quad"] = self.parameters["quad"]

        if "force_symmetry" in self.parameters:
            body["force_symmetry"] = self.parameters["force_symmetry"]

        if "face_limit" in self.parameters:
            body["face_limit"] = self.parameters["face_limit"]

        if "flatten_bottom" in self.parameters:
            body["flatten_bottom"] = self.parameters["flatten_bottom"]

        if "flatten_bottom_threshold" in self.parameters:
            body["flatten_bottom_threshold"] = self.parameters[
                "flatten_bottom_threshold"
            ]

        if "texture_size" in self.parameters:
            body["texture_size"] = self.parameters["texture_size"]

        if "texture_format" in self.parameters:
            body["texture_format"] = self.parameters["texture_format"]

        if "pivot_to_center_bottom" in self.parameters:
            body["pivot_to_center_bottom"] = self.parameters[
                "pivot_to_center_bottom"
            ]

        if "scale_factor" in self.parameters:
            body["scale_factor"] = self.parameters["scale_factor"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - original_model_task_id
          - format
        """
        parameters = kwargs

        if "original_model_task_id" not in kwargs:
            msg = "parameter `original_model_task_id` is not given"
            raise ValueError(msg)

        if "format" not in kwargs:
            msg = "parameter `format` is not given"
            raise ValueError(msg)

        return parameters
