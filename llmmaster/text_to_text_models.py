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
from .config import TOP_K
from .config import TOP_P


class AnthropicLLM(BaseModel):
    '''
    Anthropic, the provider of Claude.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class CerebrasLLM(BaseModel):
    '''
    Cerebras provides a dedicated chip for fast LLM inference.
    Supporting Llama models.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class GroqLLM(BaseModel):
    '''
    Groq is a cloud-native provider of AI infrastructure.
    Providing LPU (Language Processing Unit) for fast LLM inference.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class GoogleLLM(BaseModel):
    '''
    Google, the provider of Gemini and Gemma.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class MistralLLM(BaseModel):
    '''
    Mistral is a French provider of LLM.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class OpenAILLM(BaseModel):
    '''
    OpenAI, the provider of GPT.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class PerplexityLLM(BaseModel):
    '''
    Perplexity provides a RAG-based LLM.
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
            message += str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


def _verify_ttt_args(**kwargs):
    '''
    Expected parameters:
      - max_tokens: int, 4096 in most providers
      - temperature: float, between 0 and 1
      - top_p: float, between 0 and 1
      - top_k: int, positive values
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
