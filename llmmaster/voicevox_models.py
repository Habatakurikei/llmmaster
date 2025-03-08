from .config import VOICEVOX_BASE_EP
from .config import VOICEVOX_QUERY_EP
from .config import VOICEVOX_SYNTHESIS_EP
from .root_model import RootModel


class VoicevoxTextToSpeech(RootModel):
    """
    Voicevox Text-to-Speech model.
    Expected to use this engine in local host.
    Active the engine before using this model.
    """

    def run(self) -> None:
        """
        Generate contents in 2 steps:
          1. make query from text
          2. generate contents from query in step 1
        Note:
          - Voicevox returns binary audio data.
          - save the generated audio using `wb`.
        """
        self.payload = {"headers": self._headers(), "params": self._body()}
        query = self._call_rest_api(url=VOICEVOX_BASE_EP+VOICEVOX_QUERY_EP)

        self.payload = {
            "headers": self._headers(),
            "params": {"speaker": self.parameters["speaker"]},
            "data": query.text
        }
        self.response = self._call_rest_api(
            url=VOICEVOX_BASE_EP+VOICEVOX_SYNTHESIS_EP
        )

    def _config_headers(self) -> None:
        """
        Voicevox does not require authentication.
        """
        self.auth_header = ""

    def _body(self) -> None:
        """
        Specific parameters:
          - text (required): text to speak up as prompt
          - speaker (required): int
        """
        return {
            "text": self.parameters["prompt"],
            "speaker": self.parameters["speaker"]
        }

    def _verify_arguments(self, **kwargs):
        """
        Check required parameters:
          - speaker
        """
        parameters = kwargs

        if "speaker" not in kwargs:
            parameters["speaker"] = 1

        return parameters
