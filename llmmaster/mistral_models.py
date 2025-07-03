from .config import MISTRAL_AGENT_EP
from .config import MISTRAL_BASE_EP
from .config import MISTRAL_FIM_EP
from .config import MISTRAL_TTT_EP
from .llmbase import LLMBase


class MistralBase(LLMBase):
    """
    Mistral provides a language model with image input option.
    Use this model also for Image-To-Text.
    """

    def run(self, url: str) -> None:
        """
        Mistral needs to use different enWdpoint for different tasks.
        url: use constants from config.py for chat, fim, agent
        """
        self.response = self._call_llm(url=MISTRAL_BASE_EP+url)

    def _config_headers(self) -> None:
        self.extra_headers = {"Accept": "application/json"}

    def _body(self) -> dict:
        """
        Use common parameters for all Mistral models.
        Specific parameters:
          - stop: list of str
          - random_seed: int
          - response_format: dict
          - tools: dict
          - tool_choice: dict or str
          - presence_penalty: float
          - frequency_penalty: float
          - safe_prompt: bool
          - suffix: str or None
          - min_tokens: int or None
          - agent_id: str
        Note:
          - top_k parameter does not exist.
          - include keyword 'json' in prompt for json_object output.
        """
        body = super()._body()

        if "stop" in self.parameters:
            body["stop"] = self.parameters["stop"]

        if "random_seed" in self.parameters:
            body["random_seed"] = self.parameters["random_seed"]

        if "response_format" in self.parameters:
            body["response_format"] = self.parameters["response_format"]

        if "tools" in self.parameters:
            body["tools"] = self.parameters["tools"]

        if "tool_choice" in self.parameters:
            body["tool_choice"] = self.parameters["tool_choice"]

        if "presence_penalty" in self.parameters:
            body["presence_penalty"] = self.parameters["presence_penalty"]

        if "frequency_penalty" in self.parameters:
            body["frequency_penalty"] = self.parameters["frequency_penalty"]

        if "safe_prompt" in self.parameters:
            body["safe_prompt"] = self.parameters["safe_prompt"]

        if "suffix" in self.parameters:
            body["suffix"] = self.parameters["suffix"]

        if "min_tokens" in self.parameters:
            body["min_tokens"] = self.parameters["min_tokens"]

        if "agent_id" in self.parameters:
            body["agent_id"] = self.parameters["agent_id"]

        return body


class MistralLLM(MistralBase):
    """
    Chat completion model for Mistral
    """

    def run(self) -> None:
        super().run(MISTRAL_TTT_EP)


class MistralFIM(MistralBase):
    """
    FIM model for Mistral
    """

    def run(self) -> None:
        super().run(MISTRAL_FIM_EP)

    def _body(self) -> dict:
        body = super()._body()
        del body["messages"]
        body["prompt"] = self.parameters["prompt"]
        return body


class MistralAgent(MistralBase):
    """
    Agent model for Mistral
    """

    def run(self) -> None:
        super().run(MISTRAL_AGENT_EP)
