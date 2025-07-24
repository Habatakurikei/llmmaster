from .config import PERPLEXITY_TTT_EP
from .config import PERPLEXITY_TTT_PARAMS
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
          - search_mode: str (web or academic)
          - reasoning_effort: str (low, medium or high)
          - search_domain_filter: list
          - return_images: bool
          - return_related_questions: bool
          - search_recency_filter: str (month, week, day, hour)
          - search_after_date_filter: str
          - search_before_date_filter: str
          - last_updated_after_filter: str
          - last_updated_before_filter: str
          - presence_penalty: float
          - frequency_penalty: float
          - response_format: dict
          - web_search_options: dict
        Note:
          - Either frequency_penalty or presence_penalty can be set.
          - Example of "web_search_options": {"search_context_size": "high"}
        """
        body = super()._body()

        for param in PERPLEXITY_TTT_PARAMS:
            if param in self.parameters:
                body[param] = self.parameters[param]

        return body
