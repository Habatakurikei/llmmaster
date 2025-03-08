from .config import XAI_TTT_EP
from .llmbase import LLMBase


class XAILLM(LLMBase):
    """
    XAI provides a powerful LLM model inluding vision model.
      - grok-2(-latest)
      - grok-2-vision(-latest)
      - grok-beta
      - grok-vision-beta
    """

    def run(self) -> None:
        self.response = self._call_llm(url=XAI_TTT_EP)

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
        Notes:
          - top_k parameter does not exist.
          - include keyword 'json' in prompt for json_object output.
        """
        body = super()._body()

        if "deferred" in self.parameters:
            body["deferred"] = self.parameters["deferred"]

        if "frequency_penalty" in self.parameters:
            body["frequency_penalty"] = self.parameters["frequency_penalty"]

        if "logit_bias" in self.parameters:
            body["logit_bias"] = self.parameters["logit_bias"]

        if "logprobs" in self.parameters:
            body["logprobs"] = self.parameters["logprobs"]

        if "presence_penalty" in self.parameters:
            body["presence_penalty"] = self.parameters["presence_penalty"]

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "seed" in self.parameters:
            body["seed"] = self.parameters["seed"]

        if "stop" in self.parameters:
            body["stop"] = self.parameters["stop"]

        if "tools" in self.parameters:
            body["tools"] = self.parameters["tools"]

        if "tool_choices" in self.parameters:
            body["tool_choices"] = self.parameters["tool_choices"]

        if "top_logprobs" in self.parameters:
            body["top_logprobs"] = self.parameters["top_logprobs"]

        if "user" in self.parameters:
            body["user"] = self.parameters["user"]

        return body
