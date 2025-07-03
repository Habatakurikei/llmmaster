from requests.models import Response

from .config import XAI_BASE_EP
from .config import XAI_TTT_EP
from .config import XAI_I2T_EP
from .config import XAI_LLM_PARAMS
from .config import XAI_I2T_PARAMS
from .llmbase import LLMBase
from .root_model import RootModel


class XAILLM(LLMBase):
    """
    XAI provides a powerful LLM model inluding vision model.
      - grok-2 and 3 with reasoning
      - vision
    """

    def run(self) -> None:
        self.response = self._call_llm(url=f"{XAI_BASE_EP}{XAI_TTT_EP}")

    def _body(self) -> dict:
        """
        Specific parameters:
          - deferred: bool or None (If set, the request returns a request id.)
          - frequency_penalty: float
          - logit_bias: dict or None
          - logprobs: bool
          - presence_penalty: float
          - response_format: dict
          - seed: int
          - stop: list of str
          - tools: dict or None
          - tool_choices: list
          - top_logprobs: int
          - user: str
          - search_parameters: dict
        Notes:
          - top_k parameter does not exist.
          - include keyword 'json' in prompt for json_object output.
          - 2025-06-01: search_parameters is added.
        """
        body = super()._body()

        for param in XAI_LLM_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body


class XAITextToImage(RootModel):
    """
    Text-to-Image by Grok. Same as DALL-E.
    """
    def run(self) -> None:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=f"{XAI_BASE_EP}{XAI_I2T_EP}")
        self.response = (
            response.json() if isinstance(response, Response) else response
        )

    def _body(self) -> dict:
        """
        Specific parameters:
          - n: int, 1 to 10
          - quality: str (not supported)
          - size: str (not supported)
          - response_format: str, url or b64_json
          - style: str (not supported)
          - user: str
        """
        body = {
            "prompt": self.parameters["prompt"],
            "model": self.parameters["model"]
        }

        for param in XAI_I2T_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body
