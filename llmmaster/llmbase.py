from requests.models import Response

from .config import DEFAULT_TOKENS
from .config import LLM_PARAMS
from .config import TEMPERATURE
from .config import TOP_K
from .config import TOP_P
from .root_model import RootModel


class LLMBase(RootModel):
    """
    Base model for Text-To-Text models.
    """

    def __init__(self, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            msg = "Exception received in LLMBase"
            raise Exception(msg) from e

    def _call_llm(self, url: str = '') -> any:
        self.payload = {"headers": self._headers(), "json": self._body()}
        response = self._call_rest_api(url=url)
        return response.json() if isinstance(response, Response) else response

    def _body(self) -> dict:
        """
        Make request body for LLM.
        Set common parameters here.
        Inherit this method in each model to add model-specific parameters.
        Common parameters:
          - model (required): str
          - messages (required): list including prompt
          - max_tokens: int
          - temperature: float
          - top_p: float
          - top_k: int
        2025-01-12: system_prompt is added.
        """
        body = {
            "model": self.parameters["model"],
            "messages": [],
            "stream": False,
        }

        if "system_prompt" in self.parameters:
            body["messages"].append(
                {
                    "role": "system",
                    "content": self.parameters["system_prompt"],
                }
            )

        body["messages"].append(
            {
                "role": "user",
                "content": self.parameters["prompt"],
            }
        )

        for param in LLM_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Verify LLM common arguments.
        Copy kwargs to parameters, then overwrite each parameter.
        Note that those arguments are not strictly checked.
        Different models may have different requirements.
        Most common parameters are checked here.
          - max_tokens: 1 <= int
          - temperature: 0.0 <= float <= 2.0
          - top_p: 0.0 <= float <= 1.0
          - top_k: 0 <= int
        """
        parameters = kwargs

        if "max_tokens" in kwargs:
            buff = kwargs["max_tokens"]
            if 0 < buff:
                parameters["max_tokens"] = int(buff)
            else:
                parameters["max_tokens"] = DEFAULT_TOKENS

        if "temperature" in kwargs:
            buff = kwargs["temperature"]
            if 0 <= buff:
                parameters["temperature"] = float(buff)
            else:
                parameters["temperature"] = TEMPERATURE

        if "top_p" in kwargs:
            buff = kwargs["top_p"]
            if 0 <= buff:
                parameters["top_p"] = float(buff)
            else:
                parameters["top_p"] = TOP_P

        if "top_k" in kwargs:
            buff = kwargs["top_k"]
            if 0 <= buff:
                parameters["top_k"] = int(buff)
            else:
                parameters["top_k"] = TOP_K

        return parameters
