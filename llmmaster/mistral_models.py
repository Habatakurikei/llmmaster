from .config import MISTRAL_AGENT_EP
from .config import MISTRAL_BASE_EP
from .config import MISTRAL_FIM_EP
from .config import MISTRAL_TTT_EP
from .config import MISTRAL_TTT_PARAMS
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
        2026-05-29: added more parameters.
        """
        body = super()._body()

        for param in MISTRAL_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

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
