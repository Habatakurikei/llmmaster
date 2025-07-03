import os

from requests.models import Response

from .config import OPENAI_BASE_EP
from .config import OPENAI_IMAGE_EDIT_EP
from .config import OPENAI_IMAGE_VARIATIONS_EP
from .config import OPENAI_TRANSCRIPTION_EP
from .config import OPENAI_TRANSLATION_EP
from .config import OPENAI_TTI_EP
from .config import OPENAI_TTS_EP
from .config import OPENAI_TTS_VOICE_DEFAULT
from .config import OPENAI_TTT_EP
from .llmbase import LLMBase
from .multipart_formdata_model import MultipartFormdataModel
from .multipart_formdata_model import SpeechToTextBase
from .root_model import RootModel


class OpenAILLM(LLMBase):
    """
    OpenAI provides a typical LLM model.
    This model supports multi-modal input/output:
      - Text input
      - Image input
      - Audio input/output
    Note:
      - Image input is only for online image URL, not local image path.
      - Audio input needs a prompt, which might differ from Speech-To-Text.
      - Audio output is not Text-To-Speech but an answer to the prompt.
    """

    def run(self) -> None:
        self.response = self._call_llm(url=OPENAI_BASE_EP + OPENAI_TTT_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - store: bool
          - reasoning_effort: low, medium or high in str
          - metadata: dict
          - frequency_penalty: float
          - logit_bias: map
          - logprobs: bool or None
          - top_logprobs: int or None
          - max_completion_tokens: int
          - modalities: list
          - prediction: dict
          - audio: dict
          - presence_penalty: float
          - response_format: text or json_object in dict
          - seed: int
          - service_tier: str
          - stop: object or None
          - tools: list
          - tool_choice: tool or dict
          - parallel_tool_calls: bool
          - user: str
        Notes:
          - max_tokens is deprecated, use max_completion_tokens instead.
          - consider multi-modal input like audio
          - top_k parameter does not exist.
          - include keyword 'json' in prompt for json_object output.
        """
        body = super()._body()

        # OpenAI does not support max_tokens any more
        # Remove max_tokens from body if it exists
        if "max_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters["max_tokens"]
        if "max_tokens" in body:
            del body["max_tokens"]

        # Parameters defined by OpenAI
        if "max_completion_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters[
                "max_completion_tokens"
            ]

        if "store" in self.parameters:
            body["store"] = self.parameters["store"]

        if "reasoning_effort" in self.parameters:
            body["reasoning_effort"] = self.parameters["reasoning_effort"]

        if "metadata" in self.parameters:
            body["metadata"] = self.parameters["metadata"]

        if "frequency_penalty" in self.parameters:
            body["frequency_penalty"] = self.parameters["frequency_penalty"]

        if "logit_bias" in self.parameters:
            body["logit_bias"] = self.parameters["logit_bias"]

        if "logprobs" in self.parameters:
            body["logprobs"] = self.parameters["logprobs"]

        if "top_logprobs" in self.parameters:
            body["top_logprobs"] = self.parameters["top_logprobs"]

        if "modalities" in self.parameters:
            body["modalities"] = self.parameters["modalities"]

        if "prediction" in self.parameters:
            body["prediction"] = self.parameters["prediction"]

        if "audio" in self.parameters:
            body["audio"] = self.parameters["audio"]

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

        if "tools" in self.parameters:
            body["tools"] = self.parameters["tools"]

        if "tool_choice" in self.parameters:
            body["tool_choice"] = self.parameters["tool_choice"]

        if "parallel_tool_calls" in self.parameters:
            body["parallel_tool_calls"] = self.parameters[
                "parallel_tool_calls"
            ]

        if "user" in self.parameters:
            body["user"] = self.parameters["user"]

        return body


class OpenAITextToSpeech(RootModel):
    """
    TTS for read-aloud
    """

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        self.response = self._call_rest_api(url=OPENAI_BASE_EP + OPENAI_TTS_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - model (required): tts-1 or tts-1-hd in str
          - input (required): text to speak up as prompt
          - voice (required): whose voice in str
          - response_format: mp3, opus, aac, flac, wav, and pcm in str
          - speed: float between 0.25 and 4.0
        """
        body = {
            "model": self.parameters["model"],
            "input": self.parameters["prompt"],
            "voice": self.parameters["voice"]
        }

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "speed" in self.parameters:
            body["speed"] = self.parameters["speed"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - voice
        """
        parameters = kwargs

        if "voice" not in kwargs:
            parameters["voice"] = OPENAI_TTS_VOICE_DEFAULT

        return parameters


class OpenAISpeechToText(SpeechToTextBase):
    """
    List of available models as of 2024-07-17:
      - whisper-1
    Covered modes for this class:
      - transcriptions
      - translations
    Acceptable audio formats: mp3, mp4, mpeg, mpga, m4a, wav, and webm
    Output formats: json, text, srt, verbose_json, or vtt
    Timestamp granularities for verbose_json: word, segment, or both in list
    This class does not require prompt.
    Note that translation supports only into English for the moment.
    """

    def run(self) -> None:
        """
        Unable to convert json if response_format is text.
        Use response.text instead. Default response_format is json.
        """
        subsequent_ep = (
            OPENAI_TRANSLATION_EP
            if self.parameters["mode"] == "translations"
            else OPENAI_TRANSCRIPTION_EP
        )
        response = self._call_llm(url=OPENAI_BASE_EP + subsequent_ep)
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
          - response_format: str, json, text, srt, verbose_json, or vtt
          - temperature: float, between 0 and 1
        Expected parameters (only for transcripts):
          - language: str, ISO 639-1 format like 'en'
          - timestamp_granularities: list, ["word"] or ["segment"] or both
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

        if "timestamp_granularities" in self.parameters:
            body["timestamp_granularities"] = self.parameters[
                "timestamp_granularities"
            ]

        return body


class OpenAITextToImage(RootModel):
    """
    Text-to-Image
    Popular as DALL-E
    """
    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=OPENAI_BASE_EP + OPENAI_TTI_EP)
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _body(self) -> dict:
        """
        Specific parameters:
          - n: int
          - quality: str, standard or hd
          - size: str, 256x256, 512x512, or 1024x1024
          - response_format: str, url or b64_json
          - style: str, natural or comic
          - user: str
        """
        body = {
            "prompt": self.parameters["prompt"],
            "model": self.parameters["model"]
        }

        if "n" in self.parameters:
            body["n"] = self.parameters["n"]

        if "quality" in self.parameters:
            body["quality"] = self.parameters["quality"]

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "size" in self.parameters:
            body["size"] = self.parameters["size"]

        if "style" in self.parameters:
            body["style"] = self.parameters["style"]

        if "user" in self.parameters:
            body["user"] = self.parameters["user"]

        return body


class OpenAIImageToImage(MultipartFormdataModel):
    """
    List of available models as of 2024-07-12:
      - dall-e-2
    Covered edit modes for this class:
      - variations
      - edits
    Acceptable image format: png (RGB) only, RGBA is not supported.
    """

    def run(self) -> None:
        """
        Unable to convert json if response_format is text.
        Use response.text instead. Default response_format is json.
        """
        subsequent_ep = (
            OPENAI_IMAGE_EDIT_EP
            if self.parameters["mode"] == "edits"
            else OPENAI_IMAGE_VARIATIONS_EP
        )
        response = self._call_llm(url=OPENAI_BASE_EP + subsequent_ep)
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _body(self) -> dict:
        """
        Specific parameters:
          - prompt: str only for 'edits'
          - model (required): str, dall-e-2 only
          - image (required): str, path to image file (PNG only)
          - mask: str, path to mask file (PNG only)
          - n: int, number of images to generate
          - response_format: str, url or b64_json
          - size: str, size of image to generate
          - user: str
        Special parameters for LLMMaster:
          - mode (required): str, either 'edits' or 'variations'
        """
        body = {
            "model": "dall-e-2",
            "image": (
                os.path.split(self.parameters["image"])[1],
                open(self.parameters["image"], "rb"),
                "image/png"
            )
        }

        if "prompt" in self.parameters:
            body["prompt"] = self.parameters["prompt"]

        if "mask" in self.parameters:
            body["mask"] = (
                os.path.split(self.parameters["mask"])[1],
                open(self.parameters["mask"], "rb"),
                "image/png"
            )

        if "n" in self.parameters:
            body["n"] = str(self.parameters["n"])

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "size" in self.parameters:
            body["size"] = self.parameters["size"]

        if "user" in self.parameters:
            body["user"] = self.parameters["user"]

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
