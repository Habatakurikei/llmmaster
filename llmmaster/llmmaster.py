import time

from .config import FULL_DEFAULT_MODELS
from .config import PROVIDERS_NEED_DUMMY_PROMPT
from .config import OPENAI_ITI_MODE_NEED_DUMMY_PROMPT
from .config import SD_ITI_MODE_NEED_DUMMY_PROMPT
from .config import SUMMON_LIMIT
from .config import WAIT_FOR_SUMMONING
from .text_to_text_models import AnthropicLLM
from .text_to_text_models import GoogleLLM
from .text_to_text_models import GroqLLM
from .text_to_text_models import OpenAILLM
from .text_to_text_models import PerplexityLLM
from .text_to_image_models import OpenAITextToImage
from .text_to_image_models import StableDiffusionTextToImage
from .text_to_audio_models import OpenAITextToSpeech
from .image_to_text_models import OpenAIImageToText
from .image_to_text_models import GoogleImageToText
from .image_to_image_models import OpenAIImageToImage
from .image_to_image_models import StableDiffusionImageToImage
from .audio_to_text_models import OpenAIAudioToText
from .video_to_text_models import GoogleVideoToText

INSTANCE_CLASSES = {
    'anthropic': AnthropicLLM,
    'google': GoogleLLM,
    'groq': GroqLLM,
    'openai': OpenAILLM,
    'perplexity': PerplexityLLM,
    'openai_tti': OpenAITextToImage,
    'stable_diffusion_tti': StableDiffusionTextToImage,
    'openai_tts': OpenAITextToSpeech,
    'openai_itt': OpenAIImageToText,
    'google_itt': GoogleImageToText,
    'openai_iti': OpenAIImageToImage,
    'stable_diffusion_iti': StableDiffusionImageToImage,
    'openai_att': OpenAIAudioToText,
    'google_vtt': GoogleVideoToText
}


class LLMMaster():
    '''
    Note: configure your API key in advance in your OS environment,
          using set (Win) or export (Mac/Linux) command for:
            - ANTHROPIC_API_KEY
            - GOOGLE_API_KEY
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
        self.elapsed_time = 0

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
        Use self.pack_parameters() for batch parameters input.
        '''
        num_to_summon = len(entries.keys())

        if num_to_summon < 1 or SUMMON_LIMIT < num_to_summon:
            msg = f'LLM entries must be between 1 and 32 but {num_to_summon}.'
            raise ValueError(msg)

        creator = LLMInstanceCreator()

        for key, value in entries.items():

            if SUMMON_LIMIT < len(self.instances.keys()):
                msg = 'LLM entries to summon reached to limit {SUMMON_LIMIT} '
                msg += f'- now attempted to add {len(self.instances.keys())}.'
                raise Exception(msg)

            if key in self.instances.keys():
                msg = f'Duplicate label: {key}'
                raise Exception(msg)

            try:
                creator.verify(key, **value)
                self.instances.update(creator.create())

            except Exception as e:
                msg = 'Error occurred while verifying or creating instance.'
                raise Exception(msg) from e

    def run(self):

        self.results = {}
        start_time = time.time()

        for instance in self.instances.values():
            time.sleep(WAIT_FOR_SUMMONING)
            instance.start()

        for instance in self.instances.values():
            instance.join()

        end_time = time.time()
        self.elapsed_time = round(end_time - start_time, 3)

        for label, instance in self.instances.items():
            buff = {label: instance.response}
            self.results.update(buff)

    def dismiss(self):
        self.instances = {}
        self.results = {}

    def pack_parameters(self, **kwargs):
        '''
        Use this function to arrange entry parameters in dictionary format.
        '''
        return kwargs


class LLMInstanceCreator():
    '''
    Verify entry parameters and generate LLM instance in dictionary format.
    '''
    def __init__(self):
        self.label = ''
        self.parameters = {}
        self.verified_OK = False

    def verify(self, label: str, **kwargs):
        '''
        Check validity of minimum parameters for single entry.

        Arguments:
        - label: unique identifier in string for instance (mandatory)
            - empty str not acceptable
        - entry parameters in dictionary:
            - provider: string (mandatory)
            - model: string defined by provider
            - prompt: string (mandatory), empty str not acceptable
        '''
        self.verified_OK = False
        self.parameters = kwargs

        # 1. verify label
        if not label or not isinstance(label, str):
            raise Exception('No label given in input.')

        self.label = label

        # 2. verify provider
        if 'provider' not in kwargs:
            raise Exception('No provider given in input.')

        elif kwargs['provider'] not in FULL_DEFAULT_MODELS.keys():
            msg = 'Provider name not given or non-supported provider given: '
            msg += f'{kwargs["provider"]}.'
            raise ValueError(msg)

        # 3. verify model
        if 'model' not in kwargs or not kwargs['model']:
            self.parameters['model'] = FULL_DEFAULT_MODELS[kwargs['provider']]

        # 4. verify prompt
        if self._is_dummy_prompt_required(**kwargs) and 'prompt' not in kwargs:
            kwargs.update(prompt='dummy prompt to avoid error')

        if 'prompt' not in kwargs or not kwargs['prompt']:
            raise ValueError('Prompt not given.')

        self.verified_OK = True

    def create(self):
        '''
        Call only after verification confirmed passed.

        Returns: in dictionary format of
        - label: same as given in input
        - instance of LLM ready to run
        '''
        if not self.verified_OK:
            msg = 'Unable to create because not verified or no input.'
            raise Exception(msg)

        try:
            instance_class = INSTANCE_CLASSES.get(self.parameters['provider'])
            instance = instance_class(**self.parameters)

        except Exception as e:
            raise Exception('Failed creating LLM instance.') from e

        self.verified_OK = False

        return {self.label: instance}

    def _is_dummy_prompt_required(self, **kwargs):
        '''
        Check if a dummy prompt is required for the model.
        Return True or False.
        Need a dummpy prompt for the following cases:
        - OpenAIAudioToText
          - provider = openai_att
        - OpenAITextToImage
          - mode = variations
        - StableDiffusionImageToImage
          - provider = stable_diffusion_iti
          - mode = SD_ITI_TYPE_NEED_DUMMY_PROMPT
        '''
        answer = False

        if kwargs['provider'] not in PROVIDERS_NEED_DUMMY_PROMPT:
            pass

        else:
            if kwargs['provider'] == 'openai_att':
                answer = True

            elif kwargs['provider'] == 'openai_iti':
                if not hasattr(kwargs, 'mode'):
                    answer = True
                elif kwargs['mode'] in OPENAI_ITI_MODE_NEED_DUMMY_PROMPT:
                    answer = True

            elif kwargs['provider'] == 'stable_diffusion_iti':
                if not hasattr(kwargs, 'mode'):
                    answer = True
                elif kwargs['mode'] in SD_ITI_MODE_NEED_DUMMY_PROMPT:
                    answer = True

        return answer
