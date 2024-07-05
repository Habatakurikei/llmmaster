import os
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


class LLMMaster():
    '''
    Note: configure your API key in advance for your OS environment,
          using set (Win) or export (Mac/Linux) command for:
            - ANTHROPIC_API_KEY
            - GEMINI_API_KEY
            - GROQ_API_KEY
            - OPENAI_API_KEY
            - PERPLEXITY_API_KEY
    Usage:
      1. create a new instance
      2. call summon or summon_all to initialize the instance
      3. call run to start generation through LLM
      4. access self.result to get generated texts
    '''
    def __init__(self):
        self.to_summon = {}
        self.results = {}

    def summon(self, llms={}):
        '''
        Set a single LLM indicated in argument to run.
        Provide argument llms in dictionary format like {'vendor': 'model'},
        e.g. {'openai': 'gpt-4o'}, see REGISTERED_LLM for acceptable cases.
        Acceptable for either single model or multiple models setup.
        
        '''
        self.to_summon.update(llms)

    def summon_all(self):
        '''
        Set all the registerd typical LLMs to run.
        '''
        self.to_summon.update(REGISTERED_LLM)

    def run(self, prompt='', max_tokens=4096, temperature=0.7):

        self.results = {}
        threads = []

        for key, value in self.to_summon.items():

            if key == 'anthropic':
                instance = AnthropicLLM(model=value,
                                        prompt=prompt,
                                        max_tokens=max_tokens,
                                        temperature=temperature)

            elif key == 'google':
                instance = GoogleLLM(model=value,
                                     prompt=prompt,
                                     max_tokens=max_tokens,
                                     temperature=temperature)

            elif key == 'groq':
                instance = GroqLLM(model=value,
                                   prompt=prompt,
                                   max_tokens=max_tokens,
                                   temperature=temperature)

            elif key == 'openai':
                instance = OpenAILLM(model=value,
                                     prompt=prompt,
                                     max_tokens=max_tokens,
                                     temperature=temperature)

            elif key == 'perplexity':
                instance = PerplexityLLM(model=value,
                                         prompt=prompt,
                                         max_tokens=max_tokens,
                                         temperature=temperature)

            else:
                raise Exception(f'Vendor {key} is not supported.')

            threads.append(instance)
            instance.start()

        for instance in threads:
            instance.join()

        for instance in threads:
            self.results.update(instance.response)


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
                 max_tokens=4096,
                 temperature=0.7):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        print(f'Call Anthropic {self.model}...')

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
            raise Exception from e

        if hasattr(response, 'content'):
            message = response.content[0].text.strip()

        print(f'Anthropic responded =\n{message}\n')

        self.response.update(anthropic=message)


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
                 max_tokens=4096,
                 temperature=0.7):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        print(f'Call Groq {self.model}')

        message = 'No response.'

        try:
            client = Groq(api_key=os.environ.get(GROQ_KEY_NAME))

            response = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{'role': 'user', 'content': self.prompt}])

        except Exception as e:
            raise Exception from e

        if hasattr(response, 'choices'):
            message = response.choices[0].message.content.strip()

        print(f'Groq responded =\n{message}\n')

        self.response.update(groq=message)


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
                 max_tokens=65536,
                 temperature=0.7):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        print(f'Call Google {self.model}')

        message = 'No response.'

        try:
            genai.configure(api_key=os.getenv(GEMINI_KEY_NAME))
            generation_config = genai.GenerationConfig(
                temperature=self.temperature)

            model = genai.GenerativeModel(model_name=self.model,
                                          generation_config=generation_config)
            response = model.generate_content(self.prompt)

        except Exception as e:
            raise Exception from e

        if hasattr(response, 'text'):
            message = response.text.strip()

        print(f'Google responded =\n{message}\n')

        self.response.update(google=message)


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
                 max_tokens=4096,
                 temperature=0.7):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        print(f'Call OpenAI {self.model}')

        message = 'No response.'

        try:
            client = OpenAI(api_key=os.getenv(OPENAI_KEY_NAME))

            response = client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{'role': 'user', 'content': self.prompt}])

        except Exception as e:
            raise Exception from e

        if hasattr(response, 'choices'):
            message = response.choices[0].message.content.strip()

        print(f'OpenAI responded =\n{message}\n')

        self.response.update(openai=message)


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
                 max_tokens=4096,
                 temperature=0.7):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.response = {}

    def run(self):

        print(f'Call Perplexity {self.model}')

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
            raise Exception from e

        if hasattr(response, 'choices'):
            message = response.choices[0].message.content.strip()

        print(f'Perplexity responded =\n{message}\n')

        self.response.update(perplexity=message)


def split_llm_information(llm=''):
    '''
    Arrange dictionary format from text with slash for LLMMaster input.
    e.g. 'openai/gpt-4o' will return {'openai': 'gpt-4o'}
    '''
    items = llm.split('/')

    if len(items) != 2:
        msg = f'Length of entries must be 2 but {len(items)}: {llm}'
        raise Exception(msg)

    return {items[0]: items[1]}
