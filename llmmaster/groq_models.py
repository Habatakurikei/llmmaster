from requests.models import Response

from .config import GROQ_BASE_EP
from .config import GROQ_STT_PARAMS
from .config import GROQ_TRANSCRIPTION_EP
from .config import GROQ_TRANSLATION_EP
from .config import GROQ_TTS_EP
from .config import GROQ_TTS_PARAMS
from .config import GROQ_TTS_VOICE_DEFAULT
from .config import GROQ_TTT_EP
from .config import GROQ_TTT_PARAMS
from .llmbase import LLMBase
from .multipart_formdata_model import SpeechToTextBase
from .root_model import RootModel


class GroqLLM(LLMBase):
    """
    Groq is a cloud-native provider of AI infrastructure.
    Providing LPU (Language Processing Unit) for fast LLM inference.
    Use this model also for Image-To-Text.
    """

    def run(self) -> None:
        self.response = self._call_llm(url=GROQ_BASE_EP + GROQ_TTT_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - frequency_penalty: float
          - logit_bias: dict or None (not supported yet)
          - logprobs: bool or None (not supported yet)
          - max_completion_tokens: int or None
          - n: int or None (n=1 only now)
          - parallel_tool_calls: bool or None
          - presence_penalty: float
          - response_format: text or json_object in dict
          - seed: int or None
          - service_tier: str or None
          - stop: list of str or None
          - tool_choice: str or dict
          - tools: list of dict or None
          - top_logprobs: int or None
          - user: str or None
        2026-05-28: new parameters
          - citation_options: enabled/disabled
          - compound_custom: dict or None
          - disable_tool_validation: bool
          - documents: list or None
          - include_reasoning: bool or None
          - reasoning_effort: default/low/medium/high or None
          - reasoning_format: hidden/raw/parsed or None
          - search_settings: dict or None
        Notes:
          - top_k is not supported
          - do not use max_tokens but max_completion_tokens instead
          - image_url shall be included in messages
        """
        body = super()._body()

        # Groq does not support max_tokens
        # Remove max_tokens from body if it exists
        if "max_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters["max_tokens"]
        if "max_tokens" in body:
            del body["max_tokens"]

        # Parameters defined by Groq
        if "max_completion_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters[
                "max_completion_tokens"
            ]

        for param in GROQ_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body


class GroqSpeechToText(SpeechToTextBase):
    """
    Covered modes for this class:
      - transcriptions
      - translations
    Supported files: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
    Note: "Content-Type": "multipart/form-data" is not used in headers.
    """

    def run(self) -> None:
        """
        Unable to convert json if response_format is text.
        Use response.text instead. Default response_format is json.
        """
        subsequent_ep = (
            GROQ_TRANSLATION_EP
            if self.parameters["mode"] == "translations"
            else GROQ_TRANSCRIPTION_EP
        )
        response = self._call_llm(url=GROQ_BASE_EP + subsequent_ep)
        if self.parameters["response_format"] == "text":
            self.response = (
                response.text if isinstance(response, Response) else response
            )
        else:
            self.response = (
                response.json() if isinstance(response, Response) else response
            )

    def _body(self) -> dict:
        """
        Specific parameters:
          - prompt: str
          - response_format: json, text or verbose_json
          - temperature: float
        Parameters for transcriptions:
          - language: str
          - timestamp_granularities: list or None
        Special parameters for LLMMaster:
          - mode (required): 'transcriptions' or 'translations'
        """
        body = super()._body()

        if "temperature" in self.parameters:
            body["temperature"] = str(self.parameters["temperature"])

        for param in GROQ_STT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body


class GroqTextToSpeech(RootModel):
    """
    2026-05-28 added: TTS for read-aloud
    """

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        self.response = self._call_rest_api(url=GROQ_BASE_EP + GROQ_TTS_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - model (required): str
          - input (required): text to speak up as prompt
          - voice (required): whose voice in str
          - response_format: flac, mp3, mulaw, ogg, wav in str
          - sample_rate: int
          - speed: float between 0.5 and 5.0
        """
        body = {
            "model": self.parameters["model"],
            "input": self.parameters["prompt"],
        }

        for param in GROQ_TTS_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - voice
        """
        parameters = kwargs

        if "voice" not in kwargs:
            parameters["voice"] = GROQ_TTS_VOICE_DEFAULT

        return parameters
