from .config import SAMBANOVA_TTT_EP
from .config import SAMBANOVA_TTT_PARAMS
from .llmbase import LLMBase


class SambaNovaLLM(LLMBase):
    """
    SambaNova provides a fast LLM model with special inference chip.
    RDU (Reconfigurable Data Unit) is a special AI chip.
    Use this model also for Image-To-Text.
    """

    def run(self) -> None:
        self.response = self._call_llm(url=SAMBANOVA_TTT_EP)

    def _body(self) -> dict:
        """
        Specific parameters: 2026-05-29 updated, see config
        """
        body = super()._body()

        # SambaNova supports both max_tokens and max_completion_tokens
        # Use max_completion_tokens only for future deprecation of max_tokens
        if "max_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters["max_tokens"]
        if "max_tokens" in body:
            del body["max_tokens"]

        if "max_completion_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters[
                "max_completion_tokens"
            ]

        for param in SAMBANOVA_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body
