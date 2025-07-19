import os

from requests.models import Response

from .config import OPENAI_BASE_EP
from .config import OPENAI_IMAGE_EDIT_EP
from .config import OPENAI_IMAGE_VARIATIONS_EP
from .config import OPENAI_ITI_PARAMS
from .config import OPENAI_STT_PARAMS
from .config import OPENAI_TRANSCRIPTION_EP
from .config import OPENAI_TRANSLATION_EP
from .config import OPENAI_TTI_EP
from .config import OPENAI_TTI_PARAMS
from .config import OPENAI_TTS_EP
from .config import OPENAI_TTS_PARAMS
from .config import OPENAI_TTS_VOICE_DEFAULT
from .config import OPENAI_TTT_EP
from .config import OPENAI_TTT_PARAMS
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

        for param in OPENAI_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

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

        for param in OPENAI_TTS_PARAMS:
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

        for param in OPENAI_STT_PARAMS:
            if param in self.parameters:
                body[param] = str(self.parameters[param])

        return body


class OpenAITextToImage(RootModel):
    """
    Text-to-Image as of 2025-07-19
      - dall-e-2
      - dall-e-3
      - gpt-image-1
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
          For Dall-E:
            - n: int
            - quality: str, standard or hd
            - size: str, 256x256, 512x512, or 1024x1024
            - response_format: str, url or b64_json
            - style: str, natural or comic
            - user: str
          For GPT-Image-1:
            - background: transparent, opaque, auto
            - moderation: str or None
            - n: int
            - output_compression: int
            - output_format: png, jpeg or webp
            - quality: high, medium or low
            - size: 1024x1024, 1536x1024, 1024x1536
            - user: str
        """
        body = {
            "prompt": self.parameters["prompt"],
            "model": self.parameters["model"]
        }

        for param in OPENAI_TTI_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body


class OpenAIImageToImage(MultipartFormdataModel):
    """
    List of available models as of 2025-07-19:
      - dall-e-2
      - gpt-image-1
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

        if "mask" in self.parameters:
            body["mask"] = (
                os.path.split(self.parameters["mask"])[1],
                open(self.parameters["mask"], "rb"),
                "image/png"
            )

        for param in OPENAI_ITI_PARAMS:
            if param in self.parameters:
                body[param] = str(self.parameters[param])

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
