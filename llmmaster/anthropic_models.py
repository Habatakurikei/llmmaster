from .config import ANTHROPIC_TTT_EP
from .config import ANTHROPIC_VERSION_HEADER
from .config import DEFAULT_TOKENS
from .config import X_API_KEY
from .llmbase import LLMBase


class AnthropicLLM(LLMBase):
    """
    Anthropic provides a language model with image input option.
    Use this model also for Image-To-Text.
    2025-02-24: added thinking prompt
    """

    def run(self) -> None:
        self.response = self._call_llm(url=ANTHROPIC_TTT_EP)

    def _config_headers(self) -> None:
        self.auth_header = X_API_KEY
        self.auth_prefix = ""
        self.extra_headers = {
            "anthropic-version": ANTHROPIC_VERSION_HEADER
        }
        if "thinking" in self.parameters:
            self.extra_headers["anthropic-beta"] = "output-128k-2025-02-19"

    def _body(self) -> dict:
        """
        Specific parameters:
          - metadata: {'user_id': uuid} or None
          - stop_sequences: list of str
          - system: str
          - tool_choice: dict
          - tools: list of objects
        Note:
          - unable to set system role but assistant is used instead.
        """
        body = super()._body()

        for message in body["messages"]:
            if message["role"] == "system":
                message["role"] = "assistant"

        if "metadata" in self.parameters:
            body["metadata"] = self.parameters["metadata"]

        if "stop_sequences" in self.parameters:
            body["stop_sequences"] = self.parameters["stop_sequences"]

        if "system" in self.parameters:
            body["system"] = self.parameters["system"]

        if "tool_choice" in self.parameters:
            body["tool_choice"] = self.parameters["tool_choice"]

        if "tools" in self.parameters:
            body["tools"] = self.parameters["tools"]

        if "thinking" in self.parameters:
            body["thinking"] = self.parameters["thinking"]

        return body

    def _verify_arguments(self, **kwargs) -> dict:
        """
        Check required parameters:
          - max_tokens
        """
        parameters = kwargs

        if "max_tokens" not in kwargs:
            parameters["max_tokens"] = DEFAULT_TOKENS

        return parameters
