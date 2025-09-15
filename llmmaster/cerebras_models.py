from .config import CEREBRAS_LLM_PARAMS
from .config import CEREBRAS_TTT_EP
from .llmbase import LLMBase


class CerebrasLLM(LLMBase):
    """
    Cerebras provides a dedicated chip for fast LLM inference
    Supporting Llama models
    """

    def run(self) -> None:
        self.response = self._call_llm(url=CEREBRAS_TTT_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - max_completion_tokens: int
          - response_format: dict or None
          - seed: int or None
          - stop: list of str or None
          - user: str or None
          - tool_choice: str or dict
          - tools: list of dict or None
        Note:
          - top_k is not supported
          - handle both max_tokens and max_completion_tokens
        """
        body = super()._body()

        # Cerebras does not support max_tokens
        # Remove max_tokens from body if it exists
        if "max_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters["max_tokens"]
        if "max_tokens" in body:
            del body["max_tokens"]

        # Parameters defined by Cerebras
        if "max_completion_tokens" in self.parameters:
            body["max_completion_tokens"] = self.parameters[
                "max_completion_tokens"
            ]

        for param in CEREBRAS_LLM_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body
