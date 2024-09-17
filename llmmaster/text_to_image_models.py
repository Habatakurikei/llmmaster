import requests
from openai import OpenAI
from openai.types.images_response import ImagesResponse

from .base_model import BaseModel
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
