import json
import os

from requests.models import Response

from .config import ELEVENLABS_AISO_EP
from .config import ELEVENLABS_BASE_EP
from .config import ELEVENLABS_DUB_EP
from .config import ELEVENLABS_MORIOKI_VOICE_ID
from .config import ELEVENLABS_TTS_EP
from .config import ELEVENLABS_TTSE_EP
from .config import ELEVENLABS_TTVOICE_EP
from .config import ELEVENLABS_VOICECHANGE_EP
from .config import XI_API_KEY
from .multipart_formdata_model import MultipartFormdataModel
from .root_model import RootModel


class ElevenLabsBase:
    """
    Support for ElevenLabs API
    """

    def _query_parameters(self) -> str:
        """
        Specific parameters:
          - voice_id: str
          - output_format: str
        """
        query_string = ""

        if "voice_id" in self.parameters:
            query_string += (
                f"/{self.parameters['voice_id']}"
            )

        if "output_format" in self.parameters:
            query_string += (
                f"?output_format={self.parameters['output_format']}"
            )

        return query_string


class ElevenLabsTextToSpeech(RootModel, ElevenLabsBase):
    """
    Text-to-Speech
    """

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        url = ELEVENLABS_BASE_EP + ELEVENLABS_TTS_EP + self._query_parameters()
        self.response = self._call_rest_api(url)

    def _config_headers(self) -> None:
        self.auth_header = XI_API_KEY
        self.auth_prefix = ''

    def _body(self) -> dict:
        """
        Specific parameters:
          - voice_settings: dict
          - pronunciation_dictionary_locators: list of dict
          - seed: int
          - previous_text: str
          - next_text: str
          - previous_request_ids: list of str
          - next_request_ids: list of str
          - use_pvc_as_ivc: bool
          - apply_text_normalization: str, auto/on/off
        Note: language_code is not supported.
        """
        body = {
            "text": self.parameters["prompt"],
            "model_id": self.parameters["model"]
        }

        if "voice_settings" in self.parameters:
            body["voice_settings"] = self.parameters["voice_settings"]

        if "pronunciation_dictionary_locators" in self.parameters:
            body["pronunciation_dictionary_locators"] = (
                self.parameters["pronunciation_dictionary_locators"]
            )

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "previous_text" in self.parameters:
            body["previous_text"] = self.parameters["previous_text"]

        if "next_text" in self.parameters:
            body["next_text"] = self.parameters["next_text"]

        if "previous_request_ids" in self.parameters:
            body["previous_request_ids"] = (
                self.parameters["previous_request_ids"]
            )

        if "next_request_ids" in self.parameters:
            body["next_request_ids"] = self.parameters["next_request_ids"]

        if "use_pvc_as_ivc" in self.parameters:
            body["use_pvc_as_ivc"] = self.parameters["use_pvc_as_ivc"]

        if "apply_text_normalization" in self.parameters:
            body["apply_text_normalization"] = (
                self.parameters["apply_text_normalization"]
            )

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - voice_id
        """
        parameters = kwargs

        if "voice_id" not in kwargs:
            parameters["voice_id"] = ELEVENLABS_MORIOKI_VOICE_ID

        return parameters


class ElevenLabsTextToSoundEffect(RootModel):
    """
    Text-to-SoundEffect
    """

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        self.response = self._call_rest_api(
            url=ELEVENLABS_BASE_EP + ELEVENLABS_TTSE_EP
        )

    def _config_headers(self) -> None:
        self.auth_header = XI_API_KEY
        self.auth_prefix = ''

    def _body(self) -> dict:
        """
        Specific parameters:
          - text (required): str
          - duration_seconds: float
          - prompt_influence: float
        """
        body = {"text": self.parameters["prompt"]}

        if "duration_seconds" in self.parameters:
            body["duration_seconds"] = self.parameters["duration_seconds"]

        if "prompt_influence" in self.parameters:
            body["prompt_influence"] = self.parameters["prompt_influence"]

        return body


class ElevenLabsVoiceDesign(RootModel, ElevenLabsBase):
    """
    Voice Design (Text-to-Voice)
    """

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(
            url=(
                ELEVENLABS_BASE_EP +
                ELEVENLABS_TTVOICE_EP +
                self._query_parameters()
            )
        )
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _config_headers(self) -> None:
        self.auth_header = XI_API_KEY
        self.auth_prefix = ''

    def _body(self) -> dict:
        """
        Specific parameters:
          - voice_description (required): str
          - text: str to read aloud
          - auto_generate_text: bool
        Note: use either text or auto_generate_text
        """
        body = {
            "voice_description": self.parameters["voice_description"]
        }

        if "text" in self.parameters:
            body["text"] = self.parameters["text"]

        if "auto_generate_text" in self.parameters:
            body["auto_generate_text"] = self.parameters["auto_generate_text"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - voice_description
        """
        parameters = kwargs

        if "voice_description" not in kwargs:
            msg = "parameter `voice_description` is required"
            raise ValueError(msg)

        return parameters


class ElevenLabsAudioIsolation(MultipartFormdataModel):
    """
    Audio Isolation
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=ELEVENLABS_BASE_EP + ELEVENLABS_AISO_EP
        )

    def _config_headers(self) -> None:
        self.auth_header = XI_API_KEY
        self.auth_prefix = ''

    def _body(self) -> dict:
        """
        Call this method to get the body in subclasses
        Specific parameters:
          - audio (required): str, local audio file to process
        """
        return {
            "audio": (
                os.path.split(self.parameters["audio"])[1],
                open(self.parameters["audio"], "rb"),
                "application/json"
            )
        }

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - audio
        """
        parameters = kwargs

        if "audio" not in kwargs or not os.path.isfile(kwargs["audio"]):
            msg = "parameter `audio` is not given or not a valid file"
            raise ValueError(msg)

        return parameters


class ElevenLabsVoiceChanger(MultipartFormdataModel, ElevenLabsBase):
    """
    Voice Changer
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=(
                ELEVENLABS_BASE_EP +
                ELEVENLABS_VOICECHANGE_EP +
                self._query_parameters()
            )
        )

    def _config_headers(self) -> None:
        self.auth_header = XI_API_KEY
        self.auth_prefix = ''

    def _body(self) -> dict:
        """
        Specific parameters:
          - audio (required): str, local audio file to process
          - model_id: str as model
          - voice_settings: dict
          - seed: int
          - remove_background_noise: bool
        """
        body = {
            "audio": (
                os.path.split(self.parameters["audio"])[1],
                open(self.parameters["audio"], "rb"),
                "application/json"
            ),
            "model_id": self.parameters["model"]
        }

        if "voice_settings" in self.parameters:
            body["voice_settings"] = json.dumps(
                self.parameters["voice_settings"]
            )

        if "seed" in self.parameters:
            body["seed"] = str(self.parameters["seed"])

        if "remove_background_noise" in self.parameters:
            body["remove_background_noise"] = str(
                self.parameters["remove_background_noise"]
            )

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - audio
          - voice_id
        """
        parameters = kwargs

        if "audio" not in kwargs or not os.path.isfile(kwargs["audio"]):
            msg = "parameter `audio` is not given or not a valid file"
            raise ValueError(msg)

        if "voice_id" not in kwargs:
            parameters["voice_id"] = ELEVENLABS_MORIOKI_VOICE_ID

        return parameters


class ElevenLabsDub(MultipartFormdataModel):
    """
    Dub
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=ELEVENLABS_BASE_EP + ELEVENLABS_DUB_EP
        )

    def _config_headers(self) -> None:
        self.auth_header = XI_API_KEY
        self.auth_prefix = ""

    def _body(self) -> dict:
        """
        Specific parameters:
          - target_lang (required): str
          - file: audio file
          - name: str as project name
          - source_url: sr
          - source_lang: str
          - num_speakers: int
          - watermark: bool
          - start_time: int
          - end_time: int
          - highest_resolution: bool
          - drop_background_audio: bool
          - use_profanity_filter: bool
          Note: use either file or source_url
        """

        body = {"target_lang": self.parameters["target_lang"]}

        if "file" in self.parameters:
            file_ext = os.path.split(self.parameters["file"])[1]
            body["file"] = (
                file_ext,
                open(self.parameters["file"], "rb"),
                f"audio/{file_ext.split('.')[-1]}"
            )

        if "name" in self.parameters:
            body["name"] = self.parameters["name"]

        if "source_url" in self.parameters:
            body["source_url"] = self.parameters["source_url"]

        if "source_lang" in self.parameters:
            body["source_lang"] = self.parameters["source_lang"]

        if "num_speakers" in self.parameters:
            body["num_speakers"] = str(self.parameters["num_speakers"])

        if "watermark" in self.parameters:
            body["watermark"] = str(self.parameters["watermark"])

        if "start_time" in self.parameters:
            body["start_time"] = str(self.parameters["start_time"])

        if "end_time" in self.parameters:
            body["end_time"] = str(self.parameters["end_time"])

        if "highest_resolution" in self.parameters:
            body["highest_resolution"] = str(
                self.parameters["highest_resolution"]
            )

        if "drop_background_audio" in self.parameters:
            body["drop_background_audio"] = str(
                self.parameters["drop_background_audio"]
            )

        if "use_profanity_filter" in self.parameters:
            body["use_profanity_filter"] = str(
                self.parameters["use_profanity_filter"]
            )

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - target_lang
        """
        parameters = kwargs

        if "target_lang" not in kwargs:
            msg = "parameter `target_lang` is required"
            raise ValueError(msg)

        return parameters
