from requests.models import Response

from .config import GROQ_BASE_EP
from .config import GROQ_TRANSCRIPTION_EP
from .config import GROQ_TRANSLATION_EP
from .config import GROQ_TTT_EP
from .llmbase import LLMBase
from .multipart_formdata_model import SpeechToTextBase


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

        if "frequency_penalty" in self.parameters:
            body["frequency_penalty"] = self.parameters["frequency_penalty"]

        if "parallel_tool_calls" in self.parameters:
            body["parallel_tool_calls"] = self.parameters[
                "parallel_tool_calls"
            ]

        if "presence_penalty" in self.parameters:
            body["presence_penalty"] = self.parameters["presence_penalty"]

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "service_tier" in self.parameters:
            body["service_tier"] = self.parameters["service_tier"]

        if "stop" in self.parameters:
            body["stop"] = self.parameters["stop"]

        if "tool_choice" in self.parameters:
            body["tool_choice"] = self.parameters["tool_choice"]

        if "tools" in self.parameters:
            body["tools"] = self.parameters["tools"]

        if "top_logprobs" in self.parameters:
            body["top_logprobs"] = self.parameters["top_logprobs"]

        if "user" in self.parameters:
            body["user"] = self.parameters["user"]

        return body


class GroqSpeechToText(SpeechToTextBase):
    """
    List of available models as of 2025-01-15:
      - whisper-large-v3-turbo
      - whisper-large-v3
      - distil-whisper-large-v3-en
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
        Special parameters for LLMMaster:
          - mode (required): 'transcriptions' or 'translations'
        """
        body = super()._body()

        if "prompt" in self.parameters:
            body["prompt"] = self.parameters["prompt"]

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "temperature" in self.parameters:
            body["temperature"] = str(self.parameters["temperature"])

        if "language" in self.parameters:
            body["language"] = self.parameters["language"]

        return body
