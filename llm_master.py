import os
import time
from threading import Thread

import google.generativeai as genai
from anthropic import Anthropic
from groq import Groq
from openai import OpenAI


ANTHROPIC_KEY_NAME = 'ANTHROPIC_API_KEY'
GEMINI_KEY_NAME = 'GEMINI_API_KEY'
GROQ_KEY_NAME = 'GROQ_API_KEY'
OPENAI_KEY_NAME = 'OPENAI_API_KEY'
PERPLEXITY_KEY_NAME = 'PERPLEXITY_API_KEY'

PERPLEXITY_EP = 'https://api.perplexity.ai'

REGISTERED_LLM = {'anthropic': 'claude-3-5-sonnet-20240620',
                  'google': 'gemini-1.5-flash',
                  'groq': 'llama3-70b-8192',
                  'openai': 'gpt-4o',
                  'perplexity': 'llama-3-sonar-large-32k-online'}

MAX_TOKENS = 4096
TEMPERATURE = 0.7

SUMMON_LIMIT = 32
WAIT_FOR_SUMMONING = 1


class LLMMaster():
    '''
    Note: configure your API key in advance in your OS environment,
          using set (Win) or export (Mac/Linux) command for:
            - ANTHROPIC_API_KEY
            - GEMINI_API_KEY
            - GROQ_API_KEY
            - OPENAI_API_KEY
            - PERPLEXITY_API_KEY
    Usage:
      1. create this class instance.
      2. call summon to set a new LLM instance with prompot.
         Use pack_parameters() to make argument.
      3. call run to start text generation for each LLM instance.
      4. access self.results to get generated texts for each LLM instance.
      5. call dismiss to clear LLM instances and results, or finish work.
    '''
    def __init__(self):
        self.instances = {}
        self.results = {}

    def summon(self, entries={}):
        '''
        Set LLM instance. Provide argument in dictionary format as:
        {
            "label": {
                "provider": "openai",
                "model": "gpt-4o",
                "prompt": "text",
                "max_tokens": 4096,
                "temperature": 0.7
            }
        }
        See LLMInstanceCreator for input rules for each parameter.
        Acceptable for both cases of single entry and multiple entries.
        '''
        num_to_summon = len(entries.keys())

        if num_to_summon < 1 or SUMMON_LIMIT < num_to_summon:
            msg = f'LLM entries must be between 1 and 32 but {num_to_summon}.'
            raise ValueError(msg)

        generator = LLMInstanceCreator()

        for key, value in entries.items():

            if SUMMON_LIMIT < len(self.instances.keys()):
                msg = 'Number of LLM entries to summon reached to limit '
                msg = f'{SUMMON_LIMIT}.'
                raise Exception(msg)

            if key in self.instances.keys():
                msg = f'Duplicate label: {key}'
                raise Exception(msg)

            try:
                generator.verify(key, value)
                self.instances.update(generator.create())

            except Exception as e:
                msg = 'Error occurred while verifying or creating instance.'
                raise Exception(msg) from e

    def run(self):

        self.results = {}

        for instance in self.instances.values():
            time.sleep(WAIT_FOR_SUMMONING)
            instance.start()

        for instance in self.instances.values():
            instance.join()

        for label, instance in self.instances.items():
            buff = {label: instance.response}
            self.results.update(buff)

    def dismiss(self):
        self.instances = {}
        self.results = {}

    def pack_parameters(self, **kwargs):
        '''
        Use this function to make entry in dictionary format.
        '''
        return kwargs


class AnthropicLLM(Thread):
    '''
      - claude-3-5-sonnet-20240620
      - claude-3-opus-20240229
      - claude-3-sonnet-20240229
      - claude-3-haiku-20240307
    '''
    def __init__(self,
                 model=REGISTERED_LLM['anthropic'],
                 prompt='',
                 max_tokens=MAX_TOKENS,
                 temperature=TEMPERATURE):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = ''

    def run(self):

        msg = 'Summon Anthropic with '
        msg += f'{self.model}, {self.max_tokens}, {self.temperature}...'
        print(msg)

        message = 'No response.'

        try:
            client = Anthropic(api_key=os.getenv(ANTHROPIC_KEY_NAME))

            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{'role': 'user',
                          'content': [{'type': 'text', 'text': self.prompt}]}])

        except Exception as e:
            msg = 'Error occurred while creating Anthropic LLM instance.'
            raise Exception(msg) from e

        if hasattr(response, 'content'):
            message = response.content[0].text.strip()

        print(f'Anthropic responded =\n{message}\n')

        self.response = message


class GroqLLM(Thread):
    '''
    List of available models as of 2024-07-04:
      - llama3-8b-8192
      - llama3-70b-8192
      - mixtral-8x7b-32768
      - gemma-7b-it
      - gemma2-9b-it
    '''
    def __init__(self,
                 model=REGISTERED_LLM['groq'],
                 prompt='',
                 max_tokens=MAX_TOKENS,
                 temperature=TEMPERATURE):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        msg = 'Summon Groq with '
        msg += f'{self.model}, {self.max_tokens}, {self.temperature}...'
        print(msg)

        message = 'No response.'

        try:
            client = Groq(api_key=os.environ.get(GROQ_KEY_NAME))

            response = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{'role': 'user', 'content': self.prompt}])

        except Exception as e:
            msg = 'Error occurred while creating Groq LLM instance.'
            raise Exception(msg) from e

        if hasattr(response, 'choices'):
            message = response.choices[0].message.content.strip()

        print(f'Groq responded =\n{message}\n')

        self.response = message


class GoogleLLM(Thread):
    '''
    List of typical available models as of 2024-07-04:
      - gemini-1.5-pro
      - gemini-1.5-flash
      - gemini-1.0-pro
    '''
    def __init__(self,
                 model=REGISTERED_LLM['google'],
                 prompt='',
                 max_tokens=MAX_TOKENS,
                 temperature=TEMPERATURE):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        msg = 'Summon Google with '
        msg += f'{self.model}, {self.max_tokens}, {self.temperature}...'
        print(msg)

        message = 'No response.'

        try:
            genai.configure(api_key=os.getenv(GEMINI_KEY_NAME))
            generation_config = genai.GenerationConfig(
                temperature=self.temperature)

            model = genai.GenerativeModel(model_name=self.model,
                                          generation_config=generation_config)
            response = model.generate_content(self.prompt)

        except Exception as e:
            msg = 'Error occurred while creating Google LLM instance.'
            raise Exception(msg) from e

        if hasattr(response, 'text'):
            message = response.text.strip()

        print(f'Google responded =\n{message}\n')

        self.response = message


class OpenAILLM(Thread):
    '''
    List of typical available models as of 2024-07-04:
      - gpt-4o
      - gpt-4o-2024-05-13
      - gpt-4-0613
      - gpt-4
      - gpt-3.5-turbo-0125
      - gpt-3.5-turbo-instruct-0914
    '''
    def __init__(self,
                 model=REGISTERED_LLM['openai'],
                 prompt='',
                 max_tokens=MAX_TOKENS,
                 temperature=TEMPERATURE):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        msg = 'Summon OpenAI with '
        msg += f'{self.model}, {self.max_tokens}, {self.temperature}...'
        print(msg)

        message = 'No response.'

        try:
            client = OpenAI(api_key=os.getenv(OPENAI_KEY_NAME))

            response = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{'role': 'user', 'content': self.prompt}])

        except Exception as e:
            msg = 'Error occurred while creating OpenAI LLM instance.'
            raise Exception(msg) from e

        if hasattr(response, 'choices'):
            message = response.choices[0].message.content.strip()

        print(f'OpenAI responded =\n{message}\n')

        self.response = message


class PerplexityLLM(Thread):
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
    def __init__(self,
                 model=REGISTERED_LLM['perplexity'],
                 prompt='',
                 max_tokens=MAX_TOKENS,
                 temperature=TEMPERATURE):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        msg = 'Summon Perplexity with '
        msg += f'{self.model}, {self.max_tokens}, {self.temperature}...'
        print(msg)

        message = 'No response.'

        try:
            client = OpenAI(api_key=os.getenv(PERPLEXITY_KEY_NAME),
                            base_url=PERPLEXITY_EP)

            response = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{'role': 'user', 'content': self.prompt}])

        except Exception as e:
            msg = 'Error occurred while creating Perplexity LLM instance.'
            raise Exception(msg) from e

        if hasattr(response, 'choices'):
            message = response.choices[0].message.content.strip()

        print(f'Perplexity responded =\n{message}\n')

        self.response = message


class LLMInstanceCreator():
    '''
    Verify entry parameters and generate LLM instance in dictionary format.
    '''
    def __init__(self):
        self.label = ''
        self.provider = ''
        self.model = ''
        self.prompt = ''
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        self.verified_OK = False

    def verify(self, label='', parameters={}):
        '''
        Check validity of each parameter for given single entry.

        Arguments:
        - label: unique identifier in string for instance (mandatory)
            - empty str not acceptable
        - entry parameters in dictionary:
            - provider: string (mandatory)
            - model: string defined by provider
            - prompt: string (mandatory), empty str not acceptable
            - max_tokens: natural number between 1 and 4096 (in most providers)
            - temperature: positive float between 0 and 1
        '''
        self.verified_OK = False

        # 1. verify label
        if not any(label):
            raise Exception('No label given in input.')

        self.label = label

        # 2. verify provider
        if ('provider' not in parameters or
           parameters['provider'] not in REGISTERED_LLM.keys()):
            msg = 'Provider name not given or non-supported provider given.'
            raise ValueError(msg)

        self.provider = parameters['provider']

        # 3. verify model
        if 'model' not in parameters or not any(parameters['model']):
            self.model = REGISTERED_LLM[self.provider]
        else:
            self.model = parameters['model']

        # 4. verify prompt
        if 'prompt' not in parameters or not any(parameters['prompt']):
            raise ValueError('Prompt not given.')

        self.prompt = parameters['prompt']

        # 5. verify max_tokens
        if 'max_tokens' not in parameters:
            self.max_tokens = MAX_TOKENS

        else:
            buff = parameters['max_tokens']
            if isinstance(buff, int) and 0 < buff and buff <= MAX_TOKENS:
                self.max_tokens = buff
            else:
                self.max_tokens = MAX_TOKENS

        # 6. verify temperature
        if 'temperature' not in parameters:
            self.temperature = TEMPERATURE

        else:
            buff = parameters['temperature']
            if isinstance(buff, float) and 0.0 <= buff and buff <= 1.0:
                self.temperature = buff
            else:
                self.temperature = TEMPERATURE

        self.verified_OK = True

    def create(self):
        '''
        Call only after verification confirmed passed.

        Returns: in dictionary format of
        - label: same as given in input
        - instance of LLM ready to run
        '''
        if not self.verified_OK:
            msg = 'Unable to generate because not verified or no input.'
            raise Exception(msg)

        if self.provider == 'anthropic':
            instance = AnthropicLLM(model=self.model,
                                    prompt=self.prompt,
                                    max_tokens=self.max_tokens,
                                    temperature=self.temperature)

        elif self.provider == 'google':
            instance = GoogleLLM(model=self.model,
                                 prompt=self.prompt,
                                 max_tokens=self.max_tokens,
                                 temperature=self.temperature)

        elif self.provider == 'groq':
            instance = GroqLLM(model=self.model,
                               prompt=self.prompt,
                               max_tokens=self.max_tokens,
                               temperature=self.temperature)

        elif self.provider == 'openai':
            instance = OpenAILLM(model=self.model,
                                 prompt=self.prompt,
                                 max_tokens=self.max_tokens,
                                 temperature=self.temperature)

        elif self.provider == 'perplexity':
            instance = PerplexityLLM(model=self.model,
                                     prompt=self.prompt,
                                     max_tokens=self.max_tokens,
                                     temperature=self.temperature)

        else:
            msg = f'Unknown provider name given {self.provider}'
            raise Exception(msg)

        self.verified_OK = False

        return {self.label: instance}
