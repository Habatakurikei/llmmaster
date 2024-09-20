import google.generativeai as genai
from anthropic import Anthropic
from cerebras.cloud.sdk import Cerebras
from groq import Groq
from mistralai import Mistral
from openai import OpenAI

from .base_model import BaseModel
from .config import DEFAULT_TOKENS
from .config import PERPLEXITY_TTT_EP
from .config import TEMPERATURE
from .config import TOP_P
from .config import TOP_K


class AnthropicLLM(BaseModel):
    '''
    List of available models as of 2024-09-03:
      - claude-3-5-sonnet-20240620
      - claude-3-opus-20240229
      - claude-3-sonnet-20240229
      - claude-3-haiku-20240307
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'AnthropicLLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            client = Anthropic(api_key=self.api_key)
            to_send = {'type': 'text', 'text': self.parameters['prompt']}

            response = client.messages.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                top_k=self.parameters['top_k'],
                messages=[{'role': 'user', 'content': [to_send]}])

            if hasattr(response, 'content'):
                message = response.content[0].text.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class CerebrasLLM(BaseModel):
    '''
    List of available models as of 2024-09-06:
      - llama3.1-8b
      - llama3.1-70b
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'CerebrasLLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            client = Cerebras(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices') and response.choices:
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class GroqLLM(BaseModel):
    '''
    List of available models as of 2024-09-03:
      - gemma-7b-it
      - gemma2-9b-it
      - llama-3.1-70b-versatile
      - llama-3.1-8b-instant
      - llama3-70b-8192
      - llama3-8b-8192
      - llama3-8b-8192
      - mixtral-8x7b-32768
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'GroqLLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            client = Groq(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class GoogleLLM(BaseModel):
    '''
    List of typical available models as of 2024-09-03:
      - gemini-1.5-pro
      - gemini-1.5-flash
      - gemini-1.5-pro-exp-0827
      - gemini-1.5-flash-exp-0827
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'GoogleLLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            genai.configure(api_key=self.api_key)
            generation_config = genai.GenerationConfig(
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                top_k=self.parameters['top_k'])

            model = genai.GenerativeModel(model_name=self.parameters['model'],
                                          generation_config=generation_config)
            response = model.generate_content(self.parameters['prompt'])

            if hasattr(response, 'text'):
                message = response.text.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class MistralLLM(BaseModel):
    '''
    List of typical available models as of 2024-09-06:
      - mistral-large-latest
      - mistral-medium-latest
      - mistral-small-latest
      - open-mistral-nemo
      - codestral-latest
      - mistral-embed
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'MistralLLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            client = Mistral(api_key=self.api_key)

            response = client.chat.complete(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class OpenAILLM(BaseModel):
    '''
    List of typical available models as of 2024-09-03:
      - gpt-4o
      - gpt-4o-2024-08-06
      - gpt-4o-mini
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAILLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            client = OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class PerplexityLLM(BaseModel):
    '''
    Use OpenAI library according to Perplexity formal document.
    List of available models as of 2024-09-03:
      - llama-3.1-sonar-small-128k-online
      - llama-3.1-sonar-large-128k-online
      - llama-3.1-sonar-huge-128k-online
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'PerplexityLLM'
            raise Exception(msg) from e

    def run(self):

        message = 'No response. '

        try:
            client = OpenAI(api_key=self.api_key, base_url=PERPLEXITY_TTT_EP)

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                top_p=self.parameters['top_p'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


def _verify_ttt_args(**kwargs):
    '''
    Expected inputs:
      - max_tokens: natural number between 1 and 4096 (in most providers)
      - temperature: positive float between 0 and 1
      - top_p: positive float between 0 and 1
      - top_k: positive integer
    '''
    parameters = kwargs

    if 'max_tokens' not in kwargs:
        parameters.update(max_tokens=DEFAULT_TOKENS)
    else:
        buff = kwargs['max_tokens']
        if isinstance(buff, int) and 0 < buff:
            pass
        else:
            parameters['max_tokens'] = DEFAULT_TOKENS

    if 'temperature' not in kwargs:
        parameters.update(temperature=TEMPERATURE)
    else:
        buff = kwargs['temperature']
        if isinstance(buff, float) and 0.0 <= buff and buff <= 1.0:
            pass
        else:
            parameters['temperature'] = TEMPERATURE

    if 'top_p' not in kwargs:
        parameters.update(top_p=TOP_P)
    else:
        buff = kwargs['top_p']
        if isinstance(buff, float) and 0.0 <= buff and buff <= 1.0:
            pass
        else:
            parameters['top_p'] = TOP_P

    if 'top_k' not in kwargs:
        parameters.update(top_k=TOP_K)
    else:
        buff = kwargs['top_k']
        if 0 < buff:
            parameters['top_k'] = int(buff)
        else:
            parameters['top_k'] = TOP_K

    return parameters
