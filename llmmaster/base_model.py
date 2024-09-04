from threading import Thread


class BaseModel(Thread):
    '''
    Base model for all LLMs and relevant models.
    '''
    def __init__(self, api_key: str = '', **kwargs):
        '''
        Arguments in kwargs:
          - model: model name defined by provider
          - prompt: messege or request to model
          - additional args: parameters for differenct model type
            (e.g. max_tokens, temperature, size, quality, etc.)
        2024-09-03: added new argument `api_key`
        '''
        super().__init__()
        self.response = ''
        self.api_key = api_key
        self.parameters = self._verify_arguments(**kwargs)

    def _verify_arguments(self, **kwargs):
        return kwargs
