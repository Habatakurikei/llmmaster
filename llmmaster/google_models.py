import mimetypes
import os

import requests
from requests.models import Response

from .config import GOOGLE_GEMINI_BASE_EP
from .config import GOOGLE_GEMINI_DELETE_EP
from .config import GOOGLE_GEMINI_FILE_LIST_EP
from .config import GOOGLE_GEMINI_TTT_EP
from .config import GOOGLE_GEMINI_UPLOAD_EP
from .config import GOOGLE_LLM_PARAMS
from .config import POSITIVE_RESPONSE_CODES
from .config import WAIT_FOR_GOOGLE_VTT_RESULT
from .root_model import RootModel


class GoogleGeminiBase(RootModel):
    """
    Common class for Google Gemini
    Note: only for Google, the API style is different from other providers.
    This class is defined independently although it inherits RootModel.
    """

    def __init__(self, **kwargs) -> None:
        self.uploaded_file_path = ""
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in GoogleGeminiBase"
            raise Exception(msg) from e

    def _endpoint(self) -> str:
        ep = GOOGLE_GEMINI_BASE_EP
        ep += GOOGLE_GEMINI_TTT_EP.format(model=self.parameters["model"])
        ep += f"?key={self.api_key}"
        return ep

    def _config_headers(self) -> None:
        self.auth_header = ""

    def _upload_url(
        self,
        mime_type: str = "application/json",
        file_size: int = 0,
        display_name: str = ""
    ) -> str:
        """
        Get upload url before uploading file
        """
        headers = {
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(file_size),
            "X-Goog-Upload-Header-Content-Type": mime_type,
            "Content-Type": "application/json",
        }

        metadata = {
            "file": {
                "display_name": display_name
            }
        }

        response = requests.post(
            f"{GOOGLE_GEMINI_BASE_EP}{GOOGLE_GEMINI_UPLOAD_EP}",
            params={"key": self.api_key},
            headers=headers,
            json=metadata
        )
        response.raise_for_status()

        return response.headers.get("X-Goog-Upload-URL", None)

    def _upload_file(
        self,
        upload_url: str = "",
        file_size: int = 0
    ) -> tuple[str, str]:
        """
        Upload file and get file URL and file name
        """
        headers = {
            "Content-Length": str(file_size),
            "X-Goog-Upload-Offset": "0",
            "X-Goog-Upload-Command": "upload, finalize",
        }

        with open(self.parameters["file"], "rb") as file:
            response = requests.post(upload_url, headers=headers, data=file)

        response.raise_for_status()
        response_json = response.json()

        return response_json["file"]["uri"], response_json["file"]["name"]

    def _delete_file(self, file_name: str) -> None:
        """
        Delete uploaded file
        """
        url = f"{GOOGLE_GEMINI_BASE_EP}{GOOGLE_GEMINI_DELETE_EP}/{file_name}"
        response = requests.delete(url, params={"key": self.api_key})
        response.raise_for_status()

    def _file_list(self) -> None:
        """
        Get uploaded file list
        Use only for debug
        """
        response = requests.get(
            f"{GOOGLE_GEMINI_BASE_EP}{GOOGLE_GEMINI_FILE_LIST_EP}",
            params={"key": self.api_key}
        )
        response.raise_for_status()
        print(f"Uploaded file list =\n{response.json()}")


class GoogleLLM(GoogleGeminiBase):
    """
    Google provides Gemini series for LLM.
      - Text-to-Text (TTT)
      - Image-to-Text (ITT)
    """

    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=self._endpoint())
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _body(self) -> dict:
        """
        See following for parameters details:
          - self._generation_config()
          - self._safety_settings()
        Note:
          - dynamic_threshold: float for web search, between 0 and 1
            - 0: always web search
            - 1: never web search
        """
        body = {
            "contents": [{"parts": []}]
        }

        if isinstance(self.parameters["prompt"], list):
            # vision input
            body["contents"][0]["parts"] = self.parameters["prompt"]
        else:
            # text input
            body["contents"][0]["parts"].append({
                    "text": self.parameters["prompt"]
                })

        if "system_prompt" in self.parameters:
            body["system_instruction"] = {
                "parts": {
                    "text": self.parameters['system_prompt']
                }
            }

        if "dynamic_threshold" in self.parameters:
            # web search
            body["tools"] = [
                {
                    "googleSearchRetrieval": {
                        "dynamicRetrievalConfig": {
                            "mode": "MODE_DYNAMIC",
                            "dynamicThreshold": self.parameters[
                                "dynamic_threshold"
                            ]
                        }
                    }
                }
            ]

        generation_config = self._generation_config()
        if generation_config:
            body["generationConfig"] = generation_config

        safety_settings = self._safety_settings()
        if safety_settings:
            body["safetySettings"] = safety_settings

        return body

    def _generation_config(self) -> dict:
        """
        Specific parameters:
          - stopSequences: list of str
          - responseMimeType: str
          - responseSchema: dict
          - responseModalities: list of following
              MODALITY_UNSPECIFIED, TEXT, IMAGE, AUDIO
          - candidateCount: int
          - maxOutputTokens: int
          - temperature: float
          - topP: float
          - topK: int
          - seed: int
          - presencePenalty: float
          - frequencyPenalty: float
          - responseLogprobs: bool
          - logprobs: int
          - enableEnhancedCivicAnswers: bool
          - speechConfig: dict
        """
        generation_config = {}

        for param in GOOGLE_LLM_PARAMS:
            if param in self.parameters:
                generation_config[param] = self.parameters[param]

        return generation_config

    def _safety_settings(self) -> dict:
        """
        Safety parameters:
          - category: str
          - threshold: str
        """
        safety_settings = {}

        if "category" in self.parameters:
            safety_settings["category"] = self.parameters["category"]

        if "threshold" in self.parameters:
            safety_settings["threshold"] = self.parameters["threshold"]

        return safety_settings


class GoogleSpeechVideoToText(GoogleGeminiBase):
    """
    Speech-to-Text (STT)
    Video-to-Text (VTT)
    """

    def run(self) -> None:
        self.response = self._call_llm()

    def _call_llm(self) -> any:
        mime_type = mimetypes.guess_type(self.parameters["file"])[0]
        file_size = os.path.getsize(self.parameters["file"])
        display_name = os.path.basename(self.parameters["file"])

        try:
            upload_url = self._upload_url(mime_type, file_size, display_name)
            file_uri, file_name = self._upload_file(upload_url, file_size)
        except Exception as e:
            return f"Error while uploading file: {e}"

        self.payload = {
            "headers": self._headers(),
            "json": {
                "contents": [{
                    "parts": [
                        {"text": self.parameters["prompt"]},
                        {
                            "file_data": {
                                "mime_type": mime_type,
                                "file_uri": file_uri
                            }
                        }
                    ]
                }]
            }
        }

        response = self._fetch_result()

        self._delete_file(file_name=file_name)

        return response.json() if isinstance(response, Response) else response

    def _fetch_result(self) -> any:
        response = None
        flg = True
        while flg:
            response = requests.request(
                method="POST",
                url=self._endpoint(),
                **self.payload
            )
            if response.status_code in POSITIVE_RESPONSE_CODES:
                flg = False
            else:
                self._wait(WAIT_FOR_GOOGLE_VTT_RESULT)
        return response

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
