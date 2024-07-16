import os

import google.generativeai as genai
from anthropic import Anthropic
from groq import Groq
from openai import OpenAI

from .base_model import BaseModel

from .config import ANTHROPIC_KEY_NAME
from .config import GOOGLE_KEY_NAME
from .config import GROQ_KEY_NAME
from .config import OPENAI_KEY_NAME
from .config import PERPLEXITY_KEY_NAME

from .config import PERPLEXITY_TTT_EP
from .config import MAX_TOKENS
from .config import TEMPERATURE


class AnthropicLLM(BaseModel):
    '''
    List of available models as of 2024-07-04:
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

        # msg = f'Summon Anthropic with {self.parameters["model"]}, '
        # msg += f'{self.parameters["max_tokens"]}, '
        # msg += f'{self.parameters["temperature"]}...'
        # print(msg)

        message = 'No response.'

        try:
            client = Anthropic(api_key=os.getenv(ANTHROPIC_KEY_NAME))

            to_send = {'type': 'text', 'text': self.parameters['prompt']}

            response = client.messages.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                messages=[{'role': 'user', 'content': [to_send]}])

            if hasattr(response, 'content'):
                message = response.content[0].text.strip()

        except Exception as e:
            message = str(e)

        # print(f'Anthropic responded =\n{message}\n')

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class GroqLLM(BaseModel):
    '''
    List of available models as of 2024-07-04:
      - llama3-8b-8192
      - llama3-70b-8192
      - mixtral-8x7b-32768
      - gemma-7b-it
      - gemma2-9b-it
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'GroqLLM'
            raise Exception(msg) from e

    def run(self):

        # msg = f'Summon Groq with {self.parameters["model"]}, '
        # msg += f'{self.parameters["max_tokens"]}, '
        # msg += f'{self.parameters["temperature"]}...'
        # print(msg)

        message = 'No response.'

        try:
            client = Groq(api_key=os.environ.get(GROQ_KEY_NAME))

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        # print(f'Groq responded =\n{message}\n')

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class GoogleLLM(BaseModel):
    '''
    List of typical available models as of 2024-07-04:
      - gemini-1.5-pro
      - gemini-1.5-flash
      - gemini-1.0-pro
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'GoogleLLM'
            raise Exception(msg) from e

    def run(self):

        # msg = f'Summon Google with {self.parameters["model"]}, '
        # msg += f'{self.parameters["max_tokens"]}, '
        # msg += f'{self.parameters["temperature"]}...'
        # print(msg)

        message = 'No response.'

        try:
            genai.configure(api_key=os.getenv(GOOGLE_KEY_NAME))
            generation_config = genai.GenerationConfig(
                temperature=self.parameters['temperature'])

            model = genai.GenerativeModel(model_name=self.parameters['model'],
                                          generation_config=generation_config)
            response = model.generate_content(self.parameters['prompt'])

            if hasattr(response, 'text'):
                message = response.text.strip()

        except Exception as e:
            message = str(e)

        # print(f'Google responded =\n{message}\n')

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class OpenAILLM(BaseModel):
    '''
    List of typical available models as of 2024-07-04:
      - gpt-4o
      - gpt-4o-2024-05-13
      - gpt-4-0613
      - gpt-4
      - gpt-3.5-turbo-0125
      - gpt-3.5-turbo-instruct-0914
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAILLM'
            raise Exception(msg) from e

    def run(self):

        # msg = f'Summon OpenAI with {self.parameters["model"]}, '
        # msg += f'{self.parameters["max_tokens"]}, '
        # msg += f'{self.parameters["temperature"]}...'
        # print(msg)

        message = 'No response.'

        try:
            client = OpenAI(api_key=os.getenv(OPENAI_KEY_NAME))

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        # print(f'OpenAI responded =\n{message}\n')

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


class PerplexityLLM(BaseModel):
    '''
    Use OpenAI library according to Perplexity formal document.
    List of available models as of 2024-07-04:
      - llama-3-sonar-small-32k-chat
      - llama-3-sonar-small-32k-online
      - llama-3-sonar-large-32k-chat
      - llama-3-sonar-large-32k-online
      - llama-3-8b-instruct
      - llama-3-70b-instruct
      - mixtral-8x7b-instruct
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'PerplexityLLM'
            raise Exception(msg) from e

    def run(self):

        # msg = f'Summon Perplexity with {self.parameters["model"]}, '
        # msg += f'{self.parameters["max_tokens"]}, '
        # msg += f'{self.parameters["temperature"]}...'
        # print(msg)

        message = 'No response.'

        try:
            client = OpenAI(api_key=os.getenv(PERPLEXITY_KEY_NAME),
                            base_url=PERPLEXITY_TTT_EP)

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                temperature=self.parameters['temperature'],
                messages=[{'role': 'user',
                           'content': self.parameters['prompt']}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        # print(f'Perplexity responded =\n{message}\n')

        self.response = message

    def _verify_arguments(self, **kwargs):
        return _verify_ttt_args(**kwargs)


def _verify_ttt_args(**kwargs):
    '''
    Expected inputs:
      - max_tokens: natural number between 1 and 4096 (in most providers)
      - temperature: positive float between 0 and 1
    '''
    parameters = kwargs

    if 'max_tokens' not in kwargs:
        parameters.update(max_tokens=MAX_TOKENS)

    else:
        buff = kwargs['max_tokens']
        if isinstance(buff, int) and 0 < buff and buff <= MAX_TOKENS:
            pass
        else:
            parameters['max_tokens'] = MAX_TOKENS

    if 'temperature' not in kwargs:
        parameters.update(temperature=TEMPERATURE)

    else:
        buff = kwargs['temperature']
        if isinstance(buff, float) and 0.0 <= buff and buff <= 1.0:
            pass
        else:
            parameters['temperature'] = TEMPERATURE

    return parameters
