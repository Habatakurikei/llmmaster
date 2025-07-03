from .config import PERPLEXITY_TTT_EP
from .llmbase import LLMBase


class PerplexityLLM(LLMBase):
    """
    Perplexity provides a Web-based LLM.
    """

    def run(self) -> None:
        self.response = self._call_llm(url=PERPLEXITY_TTT_EP)

    def _body(self) -> dict:
        """
        Specific parameters:
          - frequency_penalty: float
          - presence_penalty: float
          - return_images (closed beta): bool
          - return_related_questions (closed beta): bool
          - search_domain_filter (closed beta): list
          - search_recency_filter: month, week, day, hour in string
        Note: either frequency_penalty or presence_penalty can be set.
        """
        body = super()._body()

        if "frequency_penalty" in self.parameters:
            body["frequency_penalty"] = self.parameters["frequency_penalty"]

        if "presence_penalty" in self.parameters:
            body["presence_penalty"] = self.parameters["presence_penalty"]

        if "return_images" in self.parameters:
            body["return_images"] = self.parameters["return_images"]

        if "return_related_questions" in self.parameters:
            body["return_related_questions"] = self.parameters[
                "return_related_questions"
            ]

        if "search_domain_filter" in self.parameters:
            body["search_domain_filter"] = self.parameters[
                "search_domain_filter"
            ]

        if "search_recency_filter" in self.parameters:
            body["search_recency_filter"] = self.parameters[
                "search_recency_filter"
            ]

        return body
