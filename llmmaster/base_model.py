from threading import Thread


class BaseModel(Thread):
    '''
    Base model for all LLMs and relevant models.
    '''
    def __init__(self, **kwargs):
        '''
        Arguments in kwargs:
          - model: model name defined by provider
          - prompt: messege or request to model
          - additional args: parameters for differenct model type
            (e.g. max_tokens, temperature, size, quality, etc.)
        '''
        super().__init__()
        self.parameters = self._verify_arguments(**kwargs)
        self.response = ''

    def _verify_arguments(self, **kwargs):
        return kwargs
