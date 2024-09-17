import os
import time
from io import BytesIO

import requests
from openai import OpenAI
from openai.types.images_response import ImagesResponse
from PIL import Image

from .base_model import BaseModel
from .config import DEFAULT_ITI_MODELS
from .config import MAX_SEED
from .config import OPENAI_ITI_ACCEPTABLE_COLOR_MODE
from .config import OPENAI_ITI_DEFAULT_N
from .config import OPENAI_ITI_MAX_N
from .config import OPENAI_ITI_MODE_LIST
from .config import OPENAI_ITI_SIZE_LIST
from .config import REQUEST_ACCEPTED
from .config import STABLE_DIFFUSION_BASE_EP
from .config import STABLE_DIFFUSION_ITI_EDIT_ERASE_EP
from .config import STABLE_DIFFUSION_ITI_EDIT_INPAINT_EP
from .config import STABLE_DIFFUSION_ITI_EDIT_OUTPAINT_EP
from .config import STABLE_DIFFUSION_ITI_EDIT_REMOVE_BACKGROUND_EP
from .config import STABLE_DIFFUSION_ITI_EDIT_SEARCH_AND_REPLACE_EP
from .config import STABLE_DIFFUSION_ITI_OUTPUT_FORMATS
from .config import STABLE_DIFFUSION_ITI_UPSCALE_CONSERVATIVE_EP
from .config import STABLE_DIFFUSION_ITI_UPSCALE_CREATIVE_START_EP
from .config import STABLE_DIFFUSION_ITI_UPSCALE_CREATIVE_RESULT_EP
from .config import STABLE_DIFFUSION_CONSERVATIVE_CREATIVITY_MIN
from .config import STABLE_DIFFUSION_CONSERVATIVE_CREATIVITY_MAX
from .config import STABLE_DIFFUSION_CREATIVE_CREATIVITY_MIN
from .config import STABLE_DIFFUSION_CREATIVE_CREATIVITY_MAX
from .config import STABLE_DIFFUSION_GROW_MASK_MIN
from .config import STABLE_DIFFUSION_GROW_MASK_MAX
from .config import STABLE_DIFFUSION_OUTPAINT_LEFT_MAX
from .config import STABLE_DIFFUSION_OUTPAINT_UP_MAX
from .config import STABLE_DIFFUSION_OUTPAINT_RIGHT_MAX
from .config import STABLE_DIFFUSION_OUTPAINT_DOWN_MAX
from .config import STABLE_DIFFUSION_OUTPAINT_CREATIVITY_MIN
from .config import STABLE_DIFFUSION_OUTPAINT_CREATIVITY_MAX
from .config import REQUEST_OK
from .config import WAIT_FOR_UPSCALE_CREATIVE_RESULT


class OpenAIImageToImage(BaseModel):
    '''
    List of available models as of 2024-07-12:
      - dall-e-2
    Covered edit modes for this class:
      - variations
      - edits
    Acceptable image format: png only
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAIImageToImage'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        OpenAI Image-To-Image returns class ImagesResponse.
        Save the generated image by accesing `data.url` for both
        single output and multiple outputs case.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Editted image not found. '

        try:
            client = OpenAI(api_key=self.api_key)

            if self.parameters['mode'] == 'variations':
                response = client.images.create_variation(
                    model=self.parameters['model'],
                    image=self.parameters['image'],
                    n=self.parameters['n'],
                    size=self.parameters['size'])
            elif (self.parameters['mode'] == 'edits' and
                  'mask' in self.parameters):
                response = client.images.edit(
                    model=self.parameters['model'],
                    image=self.parameters['image'],
                    mask=self.parameters['mask'],
                    prompt=self.parameters['prompt'],
                    n=self.parameters['n'],
                    size=self.parameters['size'])
            elif (self.parameters['mode'] == 'edits' and
                  'mask' not in self.parameters):
                response = client.images.edit(
                    model=self.parameters['model'],
                    image=self.parameters['image'],
                    prompt=self.parameters['prompt'],
                    n=self.parameters['n'],
                    size=self.parameters['size'])
            else:
                raise Exception("Unexpected type of process selected.")

            if isinstance(response, ImagesResponse):
                answer = response

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs:
          - mode (required): either 'edits' or 'variations'
          - image (required): str, path to image file (PNG only)
          - mask: str, path to mask file (PNG only)
          - n: int, number of images to generate
          - size: str, size of image to generate
        '''
        parameters = kwargs

        if 'mode' not in kwargs:
            raise ValueError("'mode' parameter is required")
        elif kwargs['mode'] not in OPENAI_ITI_MODE_LIST:
            raise ValueError(f"'mode' {kwargs['mode']} is not valid")

        if 'image' not in kwargs:
            raise ValueError("'image' parameter is required")
        elif not os.path.isfile(kwargs['image']):
            raise ValueError(f"'image' {kwargs['image']} is not a valid file")
        else:
            parameters['image'] = self._get_byte_image(kwargs['image'])

        if 'mask' in kwargs and os.path.isfile(kwargs['mask']):
            parameters['mask'] = self._get_byte_image(kwargs['mask'])

        if 'size' in kwargs and kwargs['size'] in OPENAI_ITI_SIZE_LIST:
            pass
        else:
            parameters.update(size=OPENAI_ITI_SIZE_LIST[0])

        if 'n' not in kwargs:
            parameters.update(n=OPENAI_ITI_DEFAULT_N)
        else:
            buff = int(kwargs['n'])
            if isinstance(buff, int) and 0 < buff and buff <= OPENAI_ITI_MAX_N:
                pass
            else:
                parameters['n'] = OPENAI_ITI_DEFAULT_N

        return parameters

    def _get_byte_image(self, to_convert):
        '''
        Convert PNG file into bytes.
        Also convert color format to RGBA if not acceptable.
        OpenAI accepts RBGA, LA and L of color formats.
        '''
        byte_arr = BytesIO()
        with Image.open(to_convert) as image:
            if image.mode not in OPENAI_ITI_ACCEPTABLE_COLOR_MODE:
                image = image.convert('RGBA')
            image.save(byte_arr, format='PNG')
        return byte_arr.getvalue()


class StableDiffusionImageToImage(BaseModel):
    '''
    Model: v2beta fixed
    Covered edit modes for this class:
      - upscale_conservative
      - upscale_creative
      - erase
      - inpaint
      - outpaint
      - search_and_replace
      - remove_background
    Modes that prompt is not required:
      - erase
      - outpaint
      - remove_background
    Acceptable image format: png, jpeg, webp
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'StableDiffusionImageToImage'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Stable Diffusion Image-To-Image returns class.
        Save the generated image by accesing output[0].url.
        When failed to generate image file, return value is given in str.
        Handle return value `answer` with care for different type in case of
        success and failure.
        '''
        answer = 'Editted image not found. '

        try:
            response = self._execute_api_call(self.parameters['url'],
                                              self.parameters['headers'],
                                              self.parameters['files'],
                                              self.parameters['data'])

            if self.parameters['mode'] == 'upscale_creative':
                response = self._fetch_result(response.json().get('id'))

            if response.status_code == REQUEST_OK:
                answer = response
            else:
                answer += str(response.json())

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        """
        Expected inputs:
          - model (required): str, model name, fixed v2beta
          - image (required): str, path to image file
          - for rest of arguments, see each function by mode
        """
        parameters = {}

        # header for REST API
        headers = {'authorization': f'Bearer {self.api_key}'}
        headers.update(accept='image/*')

        parameters.update(headers=headers)

        # correct default model to fix v2beta
        # this process is critical to make endpoint for each mode
        default_model = DEFAULT_ITI_MODELS['stable_diffusion_iti']
        if kwargs['model'] not in default_model:
            kwargs['model'] = default_model
            parameters.update(model=default_model)

        # Check if the image file is valid
        if not os.path.isfile(kwargs['image']):
            msg = f"'image' {kwargs['image']} is not a valid file"
            raise ValueError(msg)
        else:
            with open(kwargs['image'], "rb") as f:
                parameters.update(files={'image': f.read()})

        # rest of parameters are verified in each mode
        if kwargs['mode'] == 'upscale_conservative':
            parameters.update(self._verify_upscale_conservative_args(**kwargs))
        elif kwargs['mode'] == 'upscale_creative':
            parameters.update(self._verify_upscale_creative_args(**kwargs))
        elif kwargs['mode'] == 'erase':
            parameters.update(self._verify_erase_args(**kwargs))
        elif kwargs['mode'] == 'inpaint':
            parameters.update(self._verify_inpaint_args(**kwargs))
        elif kwargs['mode'] == 'outpaint':
            parameters.update(self._verify_outpaint_args(**kwargs))
        elif kwargs['mode'] == 'search_and_replace':
            parameters.update(self._verify_search_and_replace_args(**kwargs))
        elif kwargs['mode'] == 'remove_background':
            parameters.update(self._verify_remove_background_args(**kwargs))
        else:
            raise ValueError(f"Invalid mode: {kwargs['mode']}")

        # add mask if exist
        if 'mask' in parameters:
            parameters['files'].update(mask=parameters['mask'])
            parameters.pop('mask')

        return parameters

    # common execute function for REST API call
    def _execute_api_call(self, endpoint='', headers={}, files={}, data={}):

        return requests.post(endpoint,
                             headers=headers,
                             files=files,
                             data=data)

    # fetch result function for upscale creative
    def _fetch_result(self, id=''):

        answer = 'Editted file not found.'
        ep = self.parameters['url_result'].replace('{id}', id)

        flg = True

        while flg:
            response = requests.request(method='GET',
                                        url=ep,
                                        headers=self.parameters['headers'])

            if response.status_code == REQUEST_ACCEPTED:
                time.sleep(WAIT_FOR_UPSCALE_CREATIVE_RESULT)

            else:
                answer = response
                flg = False

        return answer

    # parameter check function for individual case
    def _verify_upscale_conservative_args(self, **kwargs):
        '''
        Expected options:
          - creativity: float, creativity value
          - negative_prompt: str, negative prompt
          - seed: int, seed value
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_UPSCALE_CONSERVATIVE_EP)

        parameters.update(url=endpoint)

        # data body
        data = {'prompt': kwargs['prompt']}

        if 'negative_prompt' in kwargs:
            data.update(negative_prompt=kwargs['negative_prompt'])

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        if 'creativity' in kwargs:
            creativity = kwargs['creativity']
            if (isinstance(creativity, float) and
               STABLE_DIFFUSION_CONSERVATIVE_CREATIVITY_MIN <= creativity and
               creativity <= STABLE_DIFFUSION_CONSERVATIVE_CREATIVITY_MAX):
                data.update(creativity=creativity)

        parameters.update(data=data)

        return parameters

    def _verify_upscale_creative_args(self, **kwargs):
        '''
        Expected options:
          - creativity: float, creativity value
          - negative_prompt: str, negative prompt
          - seed: int, seed value
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_UPSCALE_CREATIVE_START_EP)

        parameters.update(url=endpoint)

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_UPSCALE_CREATIVE_RESULT_EP)

        parameters.update(url_result=endpoint)

        # data body
        data = {'prompt': kwargs['prompt']}

        if 'negative_prompt' in kwargs:
            data.update(negative_prompt=kwargs['negative_prompt'])

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        if 'creativity' in kwargs:
            creativity = kwargs['creativity']
            if (isinstance(creativity, float) and
               STABLE_DIFFUSION_CREATIVE_CREATIVITY_MIN <= creativity and
               creativity <= STABLE_DIFFUSION_CREATIVE_CREATIVITY_MAX):
                data.update(creativity=creativity)

        parameters.update(data=data)

        return parameters

    def _verify_erase_args(self, **kwargs):
        '''
        Expected options:
          - mask: str, path to mask file
          - grow_mask: int, grow mask value
          - seed: int, seed value
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_EDIT_ERASE_EP)

        parameters.update(url=endpoint)

        # additional files of mask (optional)
        if 'mask' in kwargs and os.path.isfile(kwargs['mask']):
            with open(kwargs['mask'], "rb") as f:
                parameters.update(mask=f.read())

        # data body
        data = {}

        if 'grow_mask' in kwargs:
            grow_mask = kwargs['grow_mask']
            if (isinstance(grow_mask, int) and
               STABLE_DIFFUSION_GROW_MASK_MIN <= grow_mask and
               grow_mask <= STABLE_DIFFUSION_GROW_MASK_MAX):
                data.update(grow_mask=grow_mask)

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        parameters.update(data=data)

        return parameters

    def _verify_inpaint_args(self, **kwargs):
        '''
        Expected options:
          - mask: str, path to mask file
          - grow_mask: int, grow mask value
          - negative_prompt: str, negative prompt
          - seed: int, seed value
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_EDIT_INPAINT_EP)

        parameters.update(url=endpoint)

        # additional files of mask (optional)
        if 'mask' in kwargs and os.path.isfile(kwargs['mask']):
            with open(kwargs['mask'], "rb") as f:
                parameters.update(mask=f.read())

        # data body
        data = {'prompt': kwargs['prompt']}

        if 'grow_mask' in kwargs:
            grow_mask = kwargs['grow_mask']
            if (isinstance(grow_mask, int) and
               STABLE_DIFFUSION_GROW_MASK_MIN <= grow_mask and
               grow_mask <= STABLE_DIFFUSION_GROW_MASK_MAX):
                data.update(grow_mask=grow_mask)

        if 'negative_prompt' in kwargs:
            data.update(negative_prompt=kwargs['negative_prompt'])

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        parameters.update(data=data)

        return parameters

    def _verify_outpaint_args(self, **kwargs):
        '''
        Expected options:
          - left: int, left value
          - right: int, right value
          - up: int, up value
          - down: int, down value
          - creativity: float, creativity value
          - prompt: str, prompt
          - seed: int, seed value
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_EDIT_OUTPAINT_EP)

        parameters.update(url=endpoint)

        # data body
        data = {}

        if 'left' in kwargs:
            left = kwargs['left']
            if (isinstance(left, int) and
               0 <= left and left <= STABLE_DIFFUSION_OUTPAINT_LEFT_MAX):
                data.update(left=left)

        if 'right' in kwargs:
            right = kwargs['right']
            if (isinstance(right, int) and
               0 <= right and right <= STABLE_DIFFUSION_OUTPAINT_RIGHT_MAX):
                data.update(right=right)

        if 'up' in kwargs:
            up = kwargs['up']
            if (isinstance(up, int) and
               0 <= up and up <= STABLE_DIFFUSION_OUTPAINT_UP_MAX):
                data.update(up=up)

        if 'down' in kwargs:
            down = kwargs['down']
            if (isinstance(down, int) and
               0 <= down and down <= STABLE_DIFFUSION_OUTPAINT_DOWN_MAX):
                data.update(down=down)

        if 'creativity' in kwargs:
            creativity = kwargs['creativity']
            if (isinstance(creativity, float) and
               STABLE_DIFFUSION_OUTPAINT_CREATIVITY_MIN <= creativity and
               creativity <= STABLE_DIFFUSION_OUTPAINT_CREATIVITY_MAX):
                data.update(creativity=creativity)

        if 'prompt' in kwargs:
            data.update(prompt=kwargs['prompt'])

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        parameters.update(data=data)

        return parameters

    def _verify_search_and_replace_args(self, **kwargs):
        '''
        Expected options:
          - search_prompt (required): str, search prompt
          - negative_prompt: str, negative prompt
          - grow_mask: int, grow mask value
          - seed: int, seed value
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_EDIT_SEARCH_AND_REPLACE_EP)

        parameters.update(url=endpoint)

        # data body
        data = {'prompt': kwargs['prompt']}

        if 'search_prompt' not in kwargs:
            raise ValueError("'search_prompt' is required")
        else:
            data.update(search_prompt=kwargs['search_prompt'])

        if 'negative_prompt' in kwargs:
            data.update(negative_prompt=kwargs['negative_prompt'])

        if 'grow_mask' in kwargs:
            grow_mask = kwargs['grow_mask']
            if (isinstance(grow_mask, int) and
               STABLE_DIFFUSION_GROW_MASK_MIN <= grow_mask and
               grow_mask <= STABLE_DIFFUSION_GROW_MASK_MAX):
                data.update(grow_mask=grow_mask)

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        parameters.update(data=data)

        return parameters

    def _verify_remove_background_args(self, **kwargs):
        '''
        Expected options:
          - output_format: str, output format
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITI_EDIT_REMOVE_BACKGROUND_EP)

        parameters.update(url=endpoint)

        # data body
        data = {}

        if ('output_format' in kwargs and
           kwargs['output_format'] in STABLE_DIFFUSION_ITI_OUTPUT_FORMATS):
            data.update(output_format=kwargs['output_format'])

        parameters.update(data=data)

        return parameters
