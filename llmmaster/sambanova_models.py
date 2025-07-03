from .config import SAMBANOVA_TTT_EP
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
        Specific parameters:
          - stop: object or None
        """
        body = super()._body()

        if "stop" in self.parameters:
            body["stop"] = self.parameters["stop"]

        return body
