import os

from requests_toolbelt.multipart.encoder import MultipartEncoder

from .config import MULTIPART_BOUNDARY
from .root_model import RootModel


class MultipartFormdataModel(RootModel):
    """
    Special model for Content-Type = multipart/form-data
    Used in Speech-to-Text, Image-to-Image and Stable Diffusion
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in MultipartFormdataModel"
            raise Exception(msg) from e

    def _call_llm(self, url: str = '') -> any:
        """
        Call the LLM API with the multipart/form-data payload.
        """
        encoded = MultipartEncoder(
            fields=self._body(),
            boundary=MULTIPART_BOUNDARY
        )
        headers = self._headers()
        headers["Content-Type"] = encoded.content_type
        self.payload = {"headers": headers, "data": encoded}
        return self._call_rest_api(url=url)


class SpeechToTextBase(MultipartFormdataModel):
    """
    Base class for Speech-to-Text models
    Used in OpenAISpeechToText and GroqSpeechToText
    """

    def _body(self) -> dict:
        """
        Call this method to get the body in subclasses
        Specific parameters:
          - model (required): str
          - file (required): str, local audio file to process
        Special parameters for LLMMaster:
          - mode (required): str, either transcriptions or translations
        """
        return {
            "model": self.parameters["model"],
            "file": (
                os.path.split(self.parameters["file"])[1],
                open(self.parameters["file"], "rb"),
                "application/json"
            )
        }

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - mode
          - file
        """
        parameters = kwargs

        if "mode" not in kwargs:
            parameters["mode"] = "transcriptions"

        if "file" not in kwargs or not os.path.isfile(kwargs["file"]):
            msg = "parameter `file` is not given or not a valid file"
            raise ValueError(msg)

        return parameters
