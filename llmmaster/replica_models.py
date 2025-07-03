from requests.models import Response

from .config import REPLICA_BASE_EP
from .config import REPLICA_DEFAULT_SPEAKER
from .config import REPLICA_TTS_EP
from .config import REPLICA_TTS_PARAMS
from .config import X_API_KEY
from .root_model import RootModel


class ReplicaTextToSpeech(RootModel):
    """
    Replica Text-to-Speech model.
    """

    def run(self) -> None:
        """
        Generate speech from text:
        """
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=REPLICA_BASE_EP+REPLICA_TTS_EP)
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _config_headers(self) -> None:
        self.auth_header = X_API_KEY
        self.auth_prefix = ""

    def _body(self) -> None:
        """
        Specific parameters:
          - text (required): str as prompt
          - model_chain (required): str as model
          - speaker_id (required): str
          - extensions: list[str]
          - sample_rate: int
          - bit_rate: int
          - global_pace: float
          - language_code: str
          - global_pitch: float
          - auto_pitch: bool
          - global_volume: float
          - voice_preset_id: str
          - efects_preset_id: str
          - user_metadata: dict
          - user_tags: list[str]
        """
        body = {
            "text": self.parameters["prompt"],
            "model_chain": self.parameters["model"],
            "speaker_id": self.parameters["speaker_id"],
        }

        for param in REPLICA_TTS_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body

    def _verify_arguments(self, **kwargs):
        """
        Check required parameters:
          - speaker_id
        """
        parameters = kwargs

        if "speaker_id" not in kwargs:
            parameters["speaker_id"] = REPLICA_DEFAULT_SPEAKER

        return parameters
