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
          - frequency_penalty: float
          - presence_penalty: float
          - response_format: text or json_object in dict
          - stop: object or None
          - tools: list of dict
          - tool_choice: dict
          - logprobs: bool or None
          - top_logprobs: int or None
        Notes:
          - top_k parameter does not exist.
          - include keyword 'json' in prompt for json_object output.
        """
        body = super()._body()

        if "frequency_penalty" in self.parameters:
            body["frequency_penalty"] = self.parameters["frequency_penalty"]

        if "presence_penalty" in self.parameters:
            body["presence_penalty"] = self.parameters["presence_penalty"]

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "stop" in self.parameters:
            body["stop"] = self.parameters["stop"]

        if "tools" in self.parameters:
            body["tools"] = self.parameters["tools"]

        if "tool_choice" in self.parameters:
            body["tool_choice"] = self.parameters["tool_choice"]

        if "logprobs" in self.parameters:
            body["logprobs"] = self.parameters["logprobs"]

        if "top_logprobs" in self.parameters:
            body["top_logprobs"] = self.parameters["top_logprobs"]

        return body
