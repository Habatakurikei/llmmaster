from .config import DEEPSEEK_LLM_PARAMS
from .config import DEEPSEEK_TTT_EP
from .llmbase import LLMBase


class DeepSeekLLM(LLMBase):
    """
    DeepSeek provides a reasonable LLM model.
    """

    def run(self) -> None:
        self.response = self._call_llm(url=DEEPSEEK_TTT_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - thinking: enabled, disabled
          - reasoning_effort: high, max
          - response_format: text or json_object in dict
          - stop: object or None
          - tools: list of dict
          - tool_choice: dict
          - logprobs: bool or None
          - top_logprobs: int or None
          - user_id: str
        Notes:
          - top_k parameter does not exist.
          - include keyword 'json' in prompt for json_object output.
          - 2026-05-27: `thinking` parameter added.
        """
        body = super()._body()

        for param in DEEPSEEK_LLM_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body
