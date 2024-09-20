import fal_client
import requests
from fal_client import InProgress
from openai import OpenAI
from openai.types.images_response import ImagesResponse

from .base_model import BaseModel
from .config import FLUX1_FAL_TTI_MODELS
from .config import FLUX1_FAL_TTI_ASPECT_RATIO_LIST
from .config import MAX_SEED
from .config import OPENAI_TTI_DEFAULT_N
from .config import OPENAI_TTI_QUALITY_LIST
from .config import OPENAI_TTI_SIZE_LIST
from .config import STABLE_DIFFUSION_BASE_EP
from .config import STABLE_DIFFUSION_TTI_ASPECT_RATIO_LIST
from .config import STABLE_DIFFUSION_TTI_EP
from .config import STABLE_DIFFUSION_TTI_MODELS
from .config import STABLE_DIFFUSION_TTI_OUTPUT_FORMATS
from .config import STABLE_DIFFUSION_TTI_STYLE_PRESET_LIST
from .config import STABLE_DIFFUSION_VERSION
from .config import REQUEST_OK
from .config import WAIT_FOR_FLUX1_FAL_TTI_RESULT


class Flux1FalTextToImage(BaseModel):
    '''
    List of available models as of 2024-09-18
      - fal-ai/flux/dev
      - fal-ai/flux/schnell
    Important:
    Fal does not support API key import from instance creation.
    API key must be set in console with `FAL_KEY` environment variable.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'Flux1FalTextToImage'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Flux1FalTextToImage returns a dictionary including image url.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid image not generated. '

        try:
            handler = fal_client.submit(self.parameters['model'],
                                        arguments=self.parameters['arguments'])
            flg = True
            while flg:
                self._wait(WAIT_FOR_FLUX1_FAL_TTI_RESULT)
                status = handler.status(with_logs=True)
                flg = False if not isinstance(status, InProgress) else True
            answer = handler.get()

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected arguments:
          - model
          - prompt
          - image_size
          - num_inference_steps
          - seed
          - guidance_scale
          - sync_mode
          - num_images
          - enable_safety_checker
        '''
        parameters = kwargs

        if kwargs['model'] not in FLUX1_FAL_TTI_MODELS:
            parameters['model'] = FLUX1_FAL_TTI_MODELS[0]

        arguments = {'prompt': kwargs['prompt']}

        if ('image_size' in kwargs and
           kwargs['image_size'] in FLUX1_FAL_TTI_ASPECT_RATIO_LIST):
            arguments['image_size'] = kwargs['image_size']

        if ('num_inference_steps' in kwargs and
           isinstance(kwargs['num_inference_steps'], int)):
            arguments['num_inference_steps'] = kwargs['num_inference_steps']

        if 'seed' in kwargs and isinstance(kwargs['seed'], int):
            arguments['seed'] = kwargs['seed']

        if ('guidance_scale' in kwargs and
           isinstance(kwargs['guidance_scale'], float)):
            arguments['guidance_scale'] = kwargs['guidance_scale']

        if 'sync_mode' in kwargs and isinstance(kwargs['sync_mode'], bool):
            arguments['sync_mode'] = kwargs['sync_mode']

        if 'num_images' in kwargs and isinstance(kwargs['num_images'], int):
            arguments['num_images'] = kwargs['num_images']

        if ('enable_safety_checker' in kwargs and
           isinstance(kwargs['enable_safety_checker'], bool)):
            arguments['enable_safety_checker'] = \
                kwargs['enable_safety_checker']

        parameters.update(arguments=arguments)

        return parameters


class OpenAITextToImage(BaseModel):
    '''
    List of available models as of 2024-07-12:
      - dall-e-2
      - dall-e-3
    Acceptable sizes for dall-e-3: 1024x1024, 1024x1792 or 1792x1024
    Acceptable quality: standard, hd
    Output formats: png
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAITextToImage'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        OpenAITextToImage returns ImagesResponse class including image url.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid image not generated. '

        try:
            client = OpenAI(api_key=self.api_key)

            response = client.images.generate(
                model=self.parameters['model'],
                prompt=self.parameters['prompt'],
                size=self.parameters['size'],
                quality=self.parameters['quality'],
                n=self.parameters['n'])

            if isinstance(response, ImagesResponse):
                answer = response

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Overwrite from BaseModel for this particular model.
        Set parameters of size, quality and n.
        Note: n is fixed 1 for OpenAI due to stable image generation.
        '''
        parameters = kwargs

        if 'size' not in kwargs or kwargs['size'] not in OPENAI_TTI_SIZE_LIST:
            parameters.update(size=OPENAI_TTI_SIZE_LIST[0])
        else:
            parameters.update(size=kwargs['size'])

        if ('quality' not in kwargs or
           kwargs['quality'] not in OPENAI_TTI_QUALITY_LIST):
            parameters.update(quality=OPENAI_TTI_QUALITY_LIST[0])
        else:
            parameters.update(quality=kwargs['quality'])

        if 'n' not in kwargs:
            parameters.update(n=OPENAI_TTI_DEFAULT_N)
        else:
            parameters['n'] = OPENAI_TTI_DEFAULT_N

        return parameters


class StableDiffusionTextToImage(BaseModel):
    '''
    List of available models as of 2024-07-12:
      - core
      - ultra
    LLMMaster no longer supports Stable Diffusion 3
    Acceptable sizes: 16:9, 1:1, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21
    Output formats: jpeg, png, webp
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'StableDiffusionTextToImage'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Stable Diffusion returns binary data of generated image, but not URL.
        LLMMaster returns requests.models.Response class directly.
        Seed value is included in response.headers['Seed'] for reuse.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid image not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     files=self.parameters['files'],
                                     data=self.parameters['data'])

            if response.status_code == REQUEST_OK:
                answer = response
            else:
                answer += str(response.json())

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Overwrite from BaseModel for this particular model.
        Set parameters defined by the provider.
        '''
        parameters = {}

        # endpoint
        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' +
                    STABLE_DIFFUSION_VERSION +
                    STABLE_DIFFUSION_TTI_EP)

        if kwargs['model'] in STABLE_DIFFUSION_TTI_MODELS:
            endpoint = endpoint + '/' + kwargs['model']
        else:
            endpoint = endpoint + '/' + STABLE_DIFFUSION_TTI_MODELS[0]

        parameters.update(url=endpoint)

        # headers
        headers = {'authorization': f'Bearer {self.api_key}'}
        headers.update(accept='image/*')

        parameters.update(headers=headers)

        parameters.update(files={"none": ''})

        # body data
        data = {'prompt': kwargs['prompt']}

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_TTI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        if ('aspect_ratio' in kwargs and
           kwargs['aspect_ratio'] in STABLE_DIFFUSION_TTI_ASPECT_RATIO_LIST):
            data.update(aspect_ratio=kwargs['aspect_ratio'])

        if 'negative_prompt' in kwargs:
            data.update(negative_prompt=kwargs['negative_prompt'])

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if kwargs['model'] == 'core':
            if ('style_preset' in kwargs and kwargs['style_preset'] in
               STABLE_DIFFUSION_TTI_STYLE_PRESET_LIST):
                data.update(style_preset=kwargs['style_preset'])
            else:
                data.update(
                    style_preset=STABLE_DIFFUSION_TTI_STYLE_PRESET_LIST[0])

        parameters.update(data=data)

        return parameters
