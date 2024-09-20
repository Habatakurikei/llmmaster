import requests

from .base_model import BaseModel
from .config import MESHY_BASE_EP
from .config import MESHY_IT3D_START_EP
from .config import MESHY_TT3D_START_EP
from .config import MESHY_TTTX_START_EP
from .config import MESHY_TTVX_START_EP
from .config import MESHY_TT3D_MODELS
from .config import MESHY_TT3D_STYLES_LIST
from .config import MESHY_TT3D_TEXTURE_RICHNESS_LIST
from .config import MESHY_TTTX_RESOLUTION_LIST
from .config import MESHY_TTTX_STYLES_LIST
from .config import MESHY_VOXEL_SHRINK_LIST
from .config import MESHY_STATUS_FOR_RESULT
from .config import REQUEST_OK
from .config import WAIT_FOR_MESHY_RESULT


class MeshyModelBase(BaseModel):
    '''
    Base model for Meshy API wrapper.
    Meshy provides:
      1. Text-To-Texture model (tttx)
      2. Text-To-3D model (tt3d)
      3. Text-To-3D refine (tt3dr)
      4. Text-To-Voxel model (ttvx)
      5. Image-To-3D model (it3d)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for Meshy'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Return raw response of request.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid model not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     json=self.parameters['data'])

            response = self._fetch_result(response.json().get('result'))

            if response.status_code == REQUEST_OK:
                answer = response
            else:
                answer += str(response.json())

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _fetch_result(self, id=''):
        '''
        Common function to fetch result.
        '''
        answer = 'Generated model not found.'

        header = {'Authorization': f'Bearer {self.api_key}'}
        ep = self.parameters['url'] + f'/{id}'

        flg = True

        while flg:
            response = requests.request(method='GET',
                                        url=ep,
                                        headers=header)

            if response.json().get('status') not in MESHY_STATUS_FOR_RESULT:
                self._wait(WAIT_FOR_MESHY_RESULT)
            else:
                answer = response
                flg = False

        return answer


class MeshyTextToTexture(MeshyModelBase):
    '''
    Output format:
    This model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
          ai_model: str
          art_style: str
          negative_prompt: str
          seed: int
        '''
        parameters = kwargs

        endpoint = MESHY_BASE_EP + MESHY_TTTX_START_EP
        parameters.update(url=endpoint)

        # headers
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}

        parameters.update(headers=headers)

        # body data
        data = {}

        # model_url
        if 'model_url' not in kwargs:
            raise ValueError('"model_url" not given.')
        elif not isinstance(kwargs['model_url'], str):
            msg = '"model_url" type not str.'
            raise ValueError(msg)
        else:
            data.update(model_url=kwargs['model_url'])

        # object_prompt
        if 'object_prompt' not in kwargs:
            raise ValueError('"object_prompt" not given.')
        elif not isinstance(kwargs['object_prompt'], str):
            msg = '"object_prompt" type not str.'
            raise ValueError(msg)
        else:
            data.update(object_prompt=kwargs['object_prompt'])

        # style_prompt
        if 'style_prompt' not in kwargs:
            raise ValueError('"style_prompt" not given.')
        elif not isinstance(kwargs['style_prompt'], str):
            msg = '"style_prompt" type not str.'
            raise ValueError(msg)
        else:
            data.update(style_prompt=kwargs['style_prompt'])

        # enable_original_uv
        if ('enable_original_uv' in kwargs and
           isinstance(kwargs['enable_original_uv'], bool)):
            data.update(enable_original_uv=kwargs['enable_original_uv'])

        # negative_prompt
        if ('negative_prompt' in kwargs and
           isinstance(kwargs['negative_prompt'], str)):
            data.update(negative_prompt=kwargs['negative_prompt'])

        # enable_pbr
        if 'enable_pbr' in kwargs and isinstance(kwargs['enable_pbr'], bool):
            data.update(enable_pbr=kwargs['enable_pbr'])

        # resolution
        if ('resolution' in kwargs and
           kwargs['resolution'] in MESHY_TTTX_RESOLUTION_LIST):
            data.update(resolution=kwargs['resolution'])

        # art_style
        if ('art_style' in kwargs and
           kwargs['art_style'] in MESHY_TTTX_STYLES_LIST):
            data.update(art_style=kwargs['art_style'])

        parameters.update(data=data)

        return parameters


class MeshyTextTo3D(MeshyModelBase):
    '''
    Output format: glb, fbx, usdz, obj and mtl
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
          ai_model: str
          art_style: str
          negative_prompt: str
          seed: int
        '''
        parameters = kwargs

        endpoint = MESHY_BASE_EP + MESHY_TT3D_START_EP
        parameters.update(url=endpoint)

        # headers
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}

        parameters.update(headers=headers)

        # body data
        data = {}
        data.update(mode='preview')
        data.update(prompt=kwargs['prompt'])

        # ai_model
        if 'model' in kwargs and kwargs['model'] in MESHY_TT3D_MODELS:
            data.update(ai_model=kwargs['model'])

        # art_style
        if ('art_style' in kwargs and
           kwargs['art_style'] in MESHY_TT3D_STYLES_LIST):
            data.update(art_style=kwargs['art_style'])

        # negative_prompt
        if ('negative_prompt' in kwargs and
           isinstance(kwargs['negative_prompt'], str)):
            data.update(negative_prompt=kwargs['negative_prompt'])

        # seed
        if ('seed' in kwargs and isinstance(kwargs['seed'], int)):
            data.update(seed=kwargs['seed'])

        parameters.update(data=data)

        return parameters


class MeshyTextTo3DRefine(MeshyModelBase):
    '''
    Use this class after made base model with MeshyTextTo3D.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
          mode (required): 'refine' fixed
          preview_task_id (required): str
          texture_richness: str
        '''
        parameters = kwargs

        endpoint = MESHY_BASE_EP + MESHY_TT3D_START_EP
        parameters.update(url=endpoint)

        # headers
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}

        parameters.update(headers=headers)

        # body data
        data = {}
        data.update(mode='refine')

        if 'preview_task_id' not in kwargs:
            raise ValueError('"preview_task_id" not given.')
        elif not isinstance(kwargs['preview_task_id'], str):
            msg = '"preview_task_id" type not str.'
            raise ValueError(msg)
        else:
            data.update(preview_task_id=kwargs['preview_task_id'])

        if ('texture_richness' in kwargs and
           kwargs['texture_richness'] in MESHY_TT3D_TEXTURE_RICHNESS_LIST):
            data.update(texture_richness=kwargs['texture_richness'])

        parameters.update(data=data)

        return parameters


class MeshyTextToVoxel(MeshyModelBase):
    '''
    Output format: glb and vox
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
          voxel_size_shrink_factor (required): int
          negative_prompt: str
          seed: int
        '''
        parameters = kwargs

        endpoint = MESHY_BASE_EP + MESHY_TTVX_START_EP
        parameters.update(url=endpoint)

        # headers
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}

        parameters.update(headers=headers)

        # body data
        data = {}
        data.update(prompt=kwargs['prompt'])

        # voxel_size_shrink_factor
        if ('voxel_size_shrink_factor' in kwargs and
           kwargs['voxel_size_shrink_factor'] in MESHY_VOXEL_SHRINK_LIST):
            buff = kwargs['voxel_size_shrink_factor']
        else:
            buff = MESHY_VOXEL_SHRINK_LIST[0]

        data.update(voxel_size_shrink_factor=buff)

        # negative_prompt
        if ('negative_prompt' in kwargs and
           isinstance(kwargs['negative_prompt'], str)):
            data.update(negative_prompt=kwargs['negative_prompt'])

        # seed
        if ('seed' in kwargs and isinstance(kwargs['seed'], int)):
            data.update(seed=kwargs['seed'])

        parameters.update(data=data)

        return parameters


class MeshyImageTo3D(MeshyModelBase):
    '''
    Acceptable formats: jpg, jpeg and png
    Output format: glb, fbx and usdz
    This model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
          voxel_size_shrink_factor (required): int
          negative_prompt: str
          seed: int
        '''
        parameters = kwargs

        endpoint = MESHY_BASE_EP + MESHY_IT3D_START_EP
        parameters.update(url=endpoint)

        # headers
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}

        parameters.update(headers=headers)

        # body data
        data = {}

        # image_url
        if 'image_url' not in kwargs:
            raise ValueError('"image_url" not given.')
        elif not isinstance(kwargs['image_url'], str):
            msg = f'"image_url" type not str but {type(kwargs["image_url"])}.'
            raise ValueError(msg)
        else:
            data.update(image_url=kwargs['image_url'])

        # enable_pbr
        if 'enable_pbr' in kwargs and isinstance(kwargs['enable_pbr'], bool):
            data.update(enable_pbr=kwargs['enable_pbr'])

        parameters.update(data=data)

        return parameters
