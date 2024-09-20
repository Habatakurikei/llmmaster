import os
import time

from .config import ANTHROPIC_KEY_NAME
from .config import CEREBRAS_KEY_NAME
from .config import DALLE_KEY_NAME
from .config import DUMMY_KEY_NAME
from .config import ELEVENLABS_KEY_NAME
from .config import FAL_KEY_NAME
from .config import FULL_DEFAULT_MODELS
from .config import GOOGLE_KEY_NAME
from .config import GROQ_KEY_NAME
from .config import LUMAAI_KEY_NAME
from .config import MESHY_KEY_NAME
from .config import MISTRAL_KEY_NAME
from .config import OPENAI_ITI_MODE_NEED_DUMMY_PROMPT
from .config import OPENAI_KEY_NAME
from .config import PERPLEXITY_KEY_NAME
from .config import PIKAPIKAPIKA_KEY_NAME
from .config import PROVIDERS_NEED_DUMMY_PROMPT
from .config import SD_ITI_MODE_NEED_DUMMY_PROMPT
from .config import STABLE_DIFFUSION_KEY_NAME
from .config import SUMMON_LIMIT
from .config import WAIT_FOR_STARTING
from .audio_to_audio_models import ElevenLabsAudioIsolation
from .audio_to_text_models import GoogleSpeechToText
from .audio_to_text_models import OpenAISpeechToText
from .image_to_image_models import Flux1FalImageToImage
from .image_to_image_models import OpenAIImageToImage
from .image_to_image_models import StableDiffusionImageToImage
from .image_to_text_models import GoogleImageToText
from .image_to_text_models import OpenAIImageToText
from .image_to_video_models import StableDiffusionImageToVideo
from .lumaai_models import LumaDreamMachineImageToVideo
from .lumaai_models import LumaDreamMachineTextToVideo
from .lumaai_models import LumaDreamMachineVideoToVideo
from .meshy_models import MeshyImageTo3D
from .meshy_models import MeshyTextTo3D
from .meshy_models import MeshyTextTo3DRefine
from .meshy_models import MeshyTextToTexture
from .meshy_models import MeshyTextToVoxel
from .pikapikapika_models import PikaPikaPikaGeneration
from .text_to_audio_models import ElevenLabsTextToSoundEffect
from .text_to_audio_models import ElevenLabsTextToSpeech
from .text_to_audio_models import OpenAITextToSpeech
from .text_to_audio_models import VoicevoxTextToSpeech
from .text_to_image_models import Flux1FalTextToImage
from .text_to_image_models import OpenAITextToImage
from .text_to_image_models import StableDiffusionTextToImage
from .text_to_text_models import AnthropicLLM
from .text_to_text_models import CerebrasLLM
from .text_to_text_models import GoogleLLM
from .text_to_text_models import GroqLLM
from .text_to_text_models import MistralLLM
from .text_to_text_models import OpenAILLM
from .text_to_text_models import PerplexityLLM
from .video_to_text_models import GoogleVideoToText


ACTIVE_MODELS = {
    'anthropic': {'model': AnthropicLLM,
                  'key': ANTHROPIC_KEY_NAME},
    'cerebras': {'model': CerebrasLLM,
                 'key': CEREBRAS_KEY_NAME},
    'google': {'model': GoogleLLM,
               'key': GOOGLE_KEY_NAME},
    'groq': {'model': GroqLLM,
             'key': GROQ_KEY_NAME},
    'mistral': {'model': MistralLLM,
                'key': MISTRAL_KEY_NAME},
    'openai': {'model': OpenAILLM,
               'key': OPENAI_KEY_NAME},
    'perplexity': {'model': PerplexityLLM,
                   'key': PERPLEXITY_KEY_NAME},
    'openai_tti': {'model': OpenAITextToImage,
                   'key': DALLE_KEY_NAME},
    'stable_diffusion_tti': {'model': StableDiffusionTextToImage,
                             'key': STABLE_DIFFUSION_KEY_NAME},
    'flux1_fal_tti': {'model': Flux1FalTextToImage,
                      'key': FAL_KEY_NAME},
    'flux1_fal_iti': {'model': Flux1FalImageToImage,
                      'key': FAL_KEY_NAME},
    'elevenlabs_tts': {'model': ElevenLabsTextToSpeech,
                       'key': ELEVENLABS_KEY_NAME},
    'elevenlabs_ttse': {'model': ElevenLabsTextToSoundEffect,
                        'key': ELEVENLABS_KEY_NAME},
    'elevenlabs_aiso': {'model': ElevenLabsAudioIsolation,
                        'key': ELEVENLABS_KEY_NAME},
    'openai_tts': {'model': OpenAITextToSpeech,
                   'key': OPENAI_KEY_NAME},
    'voicevox_tts': {'model': VoicevoxTextToSpeech,
                     'key': DUMMY_KEY_NAME},
    'openai_itt': {'model': OpenAIImageToText,
                   'key': OPENAI_KEY_NAME},
    'google_itt': {'model': GoogleImageToText,
                   'key': GOOGLE_KEY_NAME},
    'openai_iti': {'model': OpenAIImageToImage,
                   'key': DALLE_KEY_NAME},
    'stable_diffusion_iti': {'model': StableDiffusionImageToImage,
                             'key': STABLE_DIFFUSION_KEY_NAME},
    'stable_diffusion_itv': {'model': StableDiffusionImageToVideo,
                             'key': STABLE_DIFFUSION_KEY_NAME},
    'google_stt': {'model': GoogleSpeechToText,
                   'key': GOOGLE_KEY_NAME},
    'openai_stt': {'model': OpenAISpeechToText,
                   'key': OPENAI_KEY_NAME},
    'google_vtt': {'model': GoogleVideoToText,
                   'key': GOOGLE_KEY_NAME},
    'meshy_tttx': {'model': MeshyTextToTexture,
                   'key': MESHY_KEY_NAME},
    'meshy_tt3d': {'model': MeshyTextTo3D,
                   'key': MESHY_KEY_NAME},
    'meshy_tt3d_refine': {'model': MeshyTextTo3DRefine,
                          'key': MESHY_KEY_NAME},
    'meshy_ttvx': {'model': MeshyTextToVoxel,
                   'key': MESHY_KEY_NAME},
    'meshy_it3d': {'model': MeshyImageTo3D,
                   'key': MESHY_KEY_NAME},
    'pikapikapika_ttv': {'model': PikaPikaPikaGeneration,
                         'key': PIKAPIKAPIKA_KEY_NAME},
    'lumaai_ttv': {'model': LumaDreamMachineTextToVideo,
                   'key': LUMAAI_KEY_NAME},
    'lumaai_itv': {'model': LumaDreamMachineImageToVideo,
                   'key': LUMAAI_KEY_NAME},
    'lumaai_vtv': {'model': LumaDreamMachineVideoToVideo,
                   'key': LUMAAI_KEY_NAME}
}


class LLMMaster():
    '''
    Note: prepare your API keys before calling summon().
      Either environment variables or in string from text file.
      See config.py for name defined in each provider.
    Usage:
      1. create this class instance.
        (optional) set summon_limit and wait_for_starting.
        Default of summon_limit is 100 and wait_for_starting is 1 second.
        wait_for_starting must not be shorter than 1 second.
      2. (optional) set API keys with set_api_keys() method.
      3. call summon() to set a new LLM/AI entry with parameters.
        Use pack_parameters() to make parameters into dictionary.
      4. call run() to start working for each entry.
      5. access self.results to get results for each LLM/AI entry.
      6. call dismiss() to clear entries and results, then finish work.
    2024-09-03: added `api_key_pairs` for one-time use.
    '''
    def __init__(self,
                 summon_limit: int = SUMMON_LIMIT,
                 wait_for_starting: float = WAIT_FOR_STARTING):
        self.api_key_pairs = {}
        self.instances = {}
        self.results = {}
        self.elapsed_time = 0

        self.summon_limit = summon_limit
        if wait_for_starting < WAIT_FOR_STARTING:
            self.wait_for_starting = WAIT_FOR_STARTING
        else:
            self.wait_for_starting = wait_for_starting

    def summon(self, entries: dict = {}):
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
        Acceptable for single entry or multiple entries at once.
        Use self.pack_parameters() for batch parameters input.
        '''
        num_to_summon = len(entries)

        if num_to_summon < 1 or self.summon_limit < num_to_summon:
            msg = f'LLM entries must be between 1 and {self.summon_limit} '
            msg += f'but {num_to_summon}.'
            raise ValueError(msg)

        creator = LLMInstanceCreator()

        for key, value in entries.items():

            if self.summon_limit < len(self.instances):
                msg = 'LLM entries to summon reached to limit '
                msg += f'{self.summon_limit} - now attempted to add '
                msg += f'{len(self.instances)}.'
                raise Exception(msg)

            if key in self.instances.keys():
                msg = f'Duplicate label: {key}'
                raise Exception(msg)

            try:
                creator.verify(label=key,
                               api_key_pairs=self.api_key_pairs,
                               **value)
                self.instances.update(creator.create())

            except Exception as e:
                msg = 'Error occurred while verifying or creating instance.'
                raise Exception(msg) from e

    def run(self):

        self.results = {}
        start_time = time.time()

        for instance in self.instances.values():
            time.sleep(self.wait_for_starting)
            instance.start()

        for instance in self.instances.values():
            instance.join()

        end_time = time.time()
        self.elapsed_time = round(end_time - start_time, 3)

        for label, instance in self.instances.items():
            buff = {label: instance.response}
            self.results.update(buff)

    def dismiss(self):
        self.api_key_pairs = {}
        self.instances = {}
        self.results = {}
        self.elapsed_time = 0

    def pack_parameters(self, **kwargs):
        '''
        Use this function to arrange entry parameters in dictionary format.
        '''
        return kwargs

    def set_api_keys(self, source: str):
        '''
        2024-09-03: load API keys from multiple-line text
        Format: APE_KEY = "your_key" or APE_KEY=your_key
        One key-pair per line.
        '''
        active_api_keys = [model['key'] for model in ACTIVE_MODELS.values()]
        lines = source.splitlines()
        for line in lines:
            buff = line.replace(" ", "").replace('"', "").replace("'", "")
            word_list = buff.split('=')
            if 1 < len(word_list) and word_list[0] in active_api_keys:
                self.api_key_pairs[word_list[0]] = word_list[1]


class LLMInstanceCreator():
    '''
    Verify entry parameters and generate LLM instance in dictionary format.
    '''
    def __init__(self):
        self.label = ''
        self.parameters = {}
        self.api_key = ''
        self.verified_OK = False

    def verify(self, label: str, api_key_pairs: dict, **kwargs):
        '''
        Check validity of minimum parameters for single entry.

        Arguments:
        - label (required): unique identifier in string for instance
            - empty str not acceptable
        - api_key_pairs (required): dictionary for API keys
        - entry parameters in dictionary:
            - provider (required): string
            - model: string defined by provider, default model is available
            - prompt (basically required): string, empty str not acceptable
        Steps:
          1. verify label
          2. verify provider
          3. verify model
          4. verify prompt
          5. verify api key
        '''
        self.verified_OK = False
        self.parameters = kwargs

        if not label or not isinstance(label, str):
            raise Exception('No label given in input.')
        self.label = label

        if 'provider' not in kwargs:
            raise Exception('No provider given in input.')
        elif kwargs['provider'] not in ACTIVE_MODELS.keys():
            msg = 'Provider name not given or non-supported provider given: '
            msg += f'{kwargs["provider"]}.'
            raise ValueError(msg)

        if 'model' not in kwargs or not kwargs['model']:
            self.parameters['model'] = FULL_DEFAULT_MODELS[kwargs['provider']]

        if self._is_dummy_prompt_required(**kwargs) and 'prompt' not in kwargs:
            kwargs.update(prompt='dummy prompt to avoid error')
        if 'prompt' not in kwargs or not kwargs['prompt']:
            raise ValueError('Prompt not given.')

        try:
            self.api_key = self._load_api_key(
                api_key_pairs, ACTIVE_MODELS[kwargs['provider']]['key'])
        except Exception as e:
            raise Exception(f'Failed finding API key. {e}') from e

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
            provider = self.parameters['provider']
            instance_class = ACTIVE_MODELS[provider]['model']
            instance = instance_class(api_key=self.api_key, **self.parameters)

        except Exception as e:
            raise Exception('Failed creating LLM instance.') from e

        self.verified_OK = False

        return {self.label: instance}

    def _load_api_key(self, api_key_pairs: dict, key_name: str):
        '''
        2024-09-03: find API key for provider (key_name) from environment
        variables or one-time API key pairs.
        '''
        value = os.getenv(key_name)
        value = value if value else api_key_pairs.get(key_name, None)
        if key_name == DUMMY_KEY_NAME:
            value = 'dummy'
        elif value is None:
            msg = f'{key_name} is not found in environment variables'
            msg += ' or one-time API key pairs.'
            raise Exception(msg)
        return value

    def _is_dummy_prompt_required(self, **kwargs):
        '''
        Check if a dummy prompt is required for the model.
        Return True or False.
        Need a dummpy prompt for the following cases:
        - OpenAISpeechToText
          - provider = openai_stt
        - OpenAITextToImage
          - mode = variations
        - StableDiffusionImageToImage
          - provider = stable_diffusion_iti
          - mode = SD_ITI_TYPE_NEED_DUMMY_PROMPT
        - StableDiffusionImageToVideo
          - provider = stable_diffusion_itv
        - MeshyTextToTexture
          - provider = meshy_tttx
        - MeshyTextTo3DRefine
          - provider = meshy_tt3d_refine
        - MeshyImageTo3D
          - provider = meshy_it3d
        - ElevenLabsAudioIsolation
          - provider = elevenlabs_aiso
        '''
        answer = False

        if kwargs['provider'] in PROVIDERS_NEED_DUMMY_PROMPT:
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
