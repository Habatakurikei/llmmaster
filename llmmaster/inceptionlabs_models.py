from .config import INCEPTIONLABS_BASE_EP
from .config import INCEPTIONLABS_FIM_EP
from .config import INCEPTIONLABS_TTT_EP
from .config import INCEPTIONLABS_TTT_PARAMS
from .llmbase import LLMBase


class InceptionLabsLLM(LLMBase):
    """
    Inception Labs provides Mercury Code: diffusion type text generation.
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=f"{INCEPTIONLABS_BASE_EP}{INCEPTIONLABS_TTT_EP}"
        )

    def _body(self) -> dict:
        """
        Specific parameters:
          - frequency_penalty: float
          - presence_penalty: float
          - stop: list of str
          - diffusing: bool
          - tools: list of dict
        Notes:
          - top_k is not supported
        """
        body = super()._body()

        for param in INCEPTIONLABS_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body


class InceptionLabsFIM(LLMBase):
    """
    Fill-In-The-Middle model for Inception Labs.
    """

    def run(self) -> None:
        self.response = self._call_llm(
            url=f"{INCEPTIONLABS_BASE_EP}{INCEPTIONLABS_FIM_EP}"
        )

    def _body(self) -> dict:
        """
        Specific parameters: TTT parameters and following,
          - suffix: str
        Notes: messages is not used for FIM.
        """
        body = super()._body()

        del body["messages"]

        for param in INCEPTIONLABS_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        body["prompt"] = self.parameters["prompt"]
        body["suffix"] = self.parameters["suffix"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - suffix
        """
        kwargs = super()._verify_arguments(**kwargs)

        if "suffix" not in kwargs:
            msg = "parameter `suffix` is required"
            raise ValueError(msg)

        return kwargs
