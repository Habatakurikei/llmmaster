import requests
from pathlib import Path

from .base_model import BaseModel
from .config import REQUEST_OK
from .config import TRIPO_ANIMATION_MODE
from .config import TRIPO_ANIMATION_OUT_FORMAT
from .config import TRIPO_BASE_EP
from .config import TRIPO_CONVERSION_FORMAT
from .config import TRIPO_CONVERSION_TEXTURE
from .config import TRIPO_MODELS
from .config import TRIPO_MODE_APRC
from .config import TRIPO_MODE_ARETARGET
from .config import TRIPO_MODE_ARIG
from .config import TRIPO_MODE_CONVERSION
from .config import TRIPO_MODE_IT3D
from .config import TRIPO_MODE_MV3D
from .config import TRIPO_MODE_REFINE
from .config import TRIPO_MODE_STYLIZE
from .config import TRIPO_MODE_TT3D
from .config import TRIPO_MULTIVIEW_MODES
from .config import TRIPO_RESULT_EP
from .config import TRIPO_STATUS_IN_PROGRESS
from .config import TRIPO_STYLIZATION_STYLE
from .config import TRIPO_TASK_EP
from .config import TRIPO_UPLOAD_EP
from .config import WAIT_FOR_TRIPO_RESULT


class TripoModelBase(BaseModel):
    '''
    Base model for Tripo API wrapper.
    Tripo provides:
      1. text_to_model (tripo_tt3d)
      2. image_to_model (tripo_it3d)
      3. multiview_to_model (tripo_mv3d)
      4. refine_model (tripo_refine)
      5. animate_prerigcheck (tripo_aprc)
      6. animate_rig (tripo_arig)
      7. animate_retarget (tripo_aretarget)
      8. stylize_model (tripo_stylization)
      9. convert_model (tripo_conversion)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for Tripo'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Return json-convereted response of request in dictionary.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid model not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     json=self.parameters['data'])
            response_json = response.json()
            response = self._fetch_result(response_json['data']['task_id'])

            if response.status_code == REQUEST_OK:
                answer = response.json()
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
        url = TRIPO_RESULT_EP.format(task_id=id)

        flg = True
        while flg:
            response = requests.request(method='GET',
                                        url=url,
                                        headers=header)
            response_json = response.json()
            if response_json['data']['status'] in TRIPO_STATUS_IN_PROGRESS:
                self._wait(WAIT_FOR_TRIPO_RESULT)
            else:
                answer = response
                flg = False
        return answer

    def _generation_headers(self):
        '''
        Common headers for generation.
        '''
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}
        return headers

    def _file_option(self, file_path: str = ''):
        '''
        Upload file to Tripo and get file token in dictionary for generation.
        '''
        to_load = Path(file_path)
        if not to_load.exists():
            ValueError(f'Image file not found: {file_path}')

        ext = to_load.suffix.replace('.', '')
        ext = 'jpeg' if ext == 'jpg' else ext

        url = TRIPO_BASE_EP + TRIPO_UPLOAD_EP
        headers = {'Authorization': f'Bearer {self.api_key}'}

        with open(file_path, 'rb') as fp:
            files = {'file': (file_path, fp, f'image/{ext}')}
            response = requests.post(url, headers=headers, files=files)

        response_json = response.json()
        token = response_json['data']['image_token']

        return {'type': ext, 'file_token': token}


class TripoTextTo3D(TripoModelBase):
    '''
    Output format: TBC
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - model_version: str
          - negative_prompt: str
          - text_seed: int
          - model_seed: int
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}
        data.update(type=TRIPO_MODE_TT3D)
        data.update(prompt=kwargs['prompt'])

        # model_version
        if ('model_version' in kwargs and
           kwargs['model_version'] in TRIPO_MODELS):
            data.update(model_version=kwargs['model_version'])

        # negative_prompt
        if ('negative_prompt' in kwargs and
           isinstance(kwargs['negative_prompt'], str)):
            data.update(negative_prompt=kwargs['negative_prompt'])

        # text_seed
        if 'text_seed' in kwargs and isinstance(kwargs['text_seed'], int):
            data.update(text_seed=kwargs['text_seed'])

        # model_seed
        if 'model_seed' in kwargs and isinstance(kwargs['model_seed'], int):
            data.update(model_seed=kwargs['model_seed'])

        parameters.update(data=data)

        return parameters


class TripoImageTo3D(TripoModelBase):
    '''
    Output format: TBC
    Important: this model does not require prompt.
    '''
    def run(self):
        '''
        Upload image file before generating.
        '''
        self.parameters['data'].update(
            file=self._file_option(self.parameters['file']))
        super().run()

    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - file: path to local image file, used in _file_option()
          - model_version: str
          - model_seed: int
        Options only for model_version == v2.0-20240919
          - face_limit: int
          - texture: bool
          - pbr: bool
          - texture_seed: int
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}
        data.update(type=TRIPO_MODE_IT3D)

        # model_version
        if ('model_version' in kwargs and
           kwargs['model_version'] in TRIPO_MODELS):
            data.update(model_version=kwargs['model_version'])

        # model_seed
        if 'model_seed' in kwargs and isinstance(kwargs['model_seed'], int):
            data.update(model_seed=kwargs['model_seed'])

        # face_limit
        if 'face_limit' in kwargs and isinstance(kwargs['face_limit'], int):
            data.update(face_limit=kwargs['face_limit'])

        # texture
        if 'texture' in kwargs and isinstance(kwargs['texture'], bool):
            data.update(texture=kwargs['texture'])

        # pbr
        if 'pbr' in kwargs and isinstance(kwargs['pbr'], bool):
            data.update(pbr=kwargs['pbr'])

        # texture_seed
        if ('texture_seed' in kwargs and
           isinstance(kwargs['texture_seed'], int)):
            data.update(texture_seed=kwargs['texture_seed'])

        parameters.update(data=data)

        return parameters


class TripoMultiviewTo3D(TripoModelBase):
    '''
    Output format: TBC
    Important: this model does not require prompt.
    '''
    def run(self):
        '''
        Upload image file before generating.
        '''
        files = []
        for entry in self.parameters['files']:
            files.append(self._file_option(entry))
        self.parameters['data'].update(files=files)
        super().run()

    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - files: path to 3 image files (front, side, back), _file_option()
          - mode: LEFT or RIGHT in str
          - model_version: str
          - orthographic_projection: bool
          - model_seed: int
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}
        data.update(type=TRIPO_MODE_MV3D)

        # mode
        if 'mode' in kwargs and kwargs['mode'] in TRIPO_MULTIVIEW_MODES:
            data.update(mode=kwargs['mode'])
        else:
            data.update(mode=TRIPO_MULTIVIEW_MODES[0])

        # model_version
        if ('model_version' in kwargs and
           kwargs['model_version'] in TRIPO_MODELS):
            data.update(model_version=kwargs['model_version'])

        # orthographic_projection
        if ('orthographic_projection' in kwargs and
           isinstance(kwargs['orthographic_projection'], bool)):
            data.update(
                orthographic_projection=kwargs['orthographic_projection'])

        # model_seed
        if 'model_seed' in kwargs and isinstance(kwargs['model_seed'], int):
            data.update(model_seed=kwargs['model_seed'])

        parameters.update(data=data)

        return parameters


class TripoRefineModel(TripoModelBase):
    '''
    Output format: TBC
    Important: this model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - draft_model_task_id: str
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}
        data.update(type=TRIPO_MODE_REFINE)
        if ('draft_model_task_id' in kwargs and
           isinstance(kwargs['draft_model_task_id'], str)):
            data.update(draft_model_task_id=kwargs['draft_model_task_id'])
        else:
            ValueError('draft_model_task_id is required.')

        parameters.update(data=data)

        return parameters


class TripoAnimationPreRigCheck(TripoModelBase):
    '''
    Output format: TBC
    Important: this model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - original_model_task_id: str
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}
        data.update(type=TRIPO_MODE_APRC)
        if ('original_model_task_id' in kwargs and
           isinstance(kwargs['original_model_task_id'], str)):
            data.update(
                original_model_task_id=kwargs['original_model_task_id'])
        else:
            ValueError('original_model_task_id is required.')

        parameters.update(data=data)

        return parameters


class TripoAnimationRig(TripoModelBase):
    '''
    Output format: glb or fbx
    Important: this model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - original_model_task_id: str
          - out_format: glb or fbx in str
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}

        data.update(type=TRIPO_MODE_ARIG)
        if ('original_model_task_id' in kwargs and
           isinstance(kwargs['original_model_task_id'], str)):
            data.update(
                original_model_task_id=kwargs['original_model_task_id'])
        else:
            ValueError('original_model_task_id is required.')

        if ('out_format' in kwargs and
           kwargs['out_format'] in TRIPO_ANIMATION_OUT_FORMAT):
            data.update(out_format=kwargs['out_format'])

        parameters.update(data=data)

        return parameters


class TripoAnimationRetarget(TripoModelBase):
    '''
    Output format: glb or fbx
    Important: this model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - original_model_task_id: str
          - out_format: glb or fbx in str
          - bake_animation: bool
          - animation: str
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}

        data.update(type=TRIPO_MODE_ARETARGET)
        if ('original_model_task_id' in kwargs and
           isinstance(kwargs['original_model_task_id'], str)):
            data.update(
                original_model_task_id=kwargs['original_model_task_id'])
        else:
            ValueError('original_model_task_id is required.')

        if ('animation' in kwargs and
           kwargs['animation'] in TRIPO_ANIMATION_MODE):
            data.update(animation=kwargs['animation'])
        else:
            data.update(animation=TRIPO_ANIMATION_MODE[0])

        if ('out_format' in kwargs and
           kwargs['out_format'] in TRIPO_ANIMATION_OUT_FORMAT):
            data.update(out_format=kwargs['out_format'])

        if ('bake_animation' in kwargs and
           isinstance(kwargs['bake_animation'], bool)):
            data.update(bake_animation=kwargs['bake_animation'])

        parameters.update(data=data)

        return parameters


class TripoStylization(TripoModelBase):
    '''
    Output format: TBC
    Important: this model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - original_model_task_id: str
          - style: str
          - block_size: int (for only minecraft)
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}

        data.update(type=TRIPO_MODE_STYLIZE)
        if ('original_model_task_id' in kwargs and
           isinstance(kwargs['original_model_task_id'], str)):
            data.update(
                original_model_task_id=kwargs['original_model_task_id'])
        else:
            ValueError('original_model_task_id is required.')

        if 'style' in kwargs and kwargs['style'] in TRIPO_STYLIZATION_STYLE:
            data.update(style=kwargs['style'])
        else:
            data.update(style=TRIPO_STYLIZATION_STYLE[0])

        if 'block_size' in kwargs and isinstance(kwargs['block_size'], int):
            data.update(block_size=kwargs['block_size'])

        parameters.update(data=data)

        return parameters


class TripoConversion(TripoModelBase):
    '''
    Output format: TBC
    Important: this model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - original_model_task_id: str
          - format: str
          - quad: bool
          - force_symmetry: bool
          - face_limit: int
          - flatten_bottom: bool
          - flatten_bottom_threshold: float
          - texture_size: int
          - texture_format: str
          - pivot_to_center_bottom: bool
          - scale_factor: int
        '''
        parameters = kwargs

        parameters.update(url=TRIPO_BASE_EP+TRIPO_TASK_EP)
        parameters.update(headers=self._generation_headers())

        # body data
        data = {}

        data.update(type=TRIPO_MODE_CONVERSION)
        if ('original_model_task_id' in kwargs and
           isinstance(kwargs['original_model_task_id'], str)):
            data.update(
                original_model_task_id=kwargs['original_model_task_id'])
        else:
            ValueError('original_model_task_id is required.')

        if 'format' in kwargs and kwargs['format'] in TRIPO_CONVERSION_FORMAT:
            data.update(format=kwargs['format'])
        else:
            data.update(format=TRIPO_CONVERSION_FORMAT[0])

        if 'quad' in kwargs and isinstance(kwargs['quad'], bool):
            data.update(quad=kwargs['quad'])

        if ('force_symmetry' in kwargs and
           isinstance(kwargs['force_symmetry'], bool)):
            data.update(force_symmetry=kwargs['force_symmetry'])

        if 'face_limit' in kwargs and isinstance(kwargs['face_limit'], int):
            data.update(face_limit=kwargs['face_limit'])

        if ('flatten_bottom' in kwargs and
           isinstance(kwargs['flatten_bottom '], bool)):
            data.update(flatten_bottom=kwargs['flatten_bottom'])

        if ('flatten_bottom_threshold' in kwargs and
           isinstance(kwargs['flatten_bottom_threshold'], float)):
            data.update(
                flatten_bottom_threshold=kwargs['flatten_bottom_threshold'])

        if ('texture_size' in kwargs and
           isinstance(kwargs['texture_size'], int)):
            data.update(texture_size=kwargs['texture_size'])

        if ('texture_format' in kwargs and
           kwargs['texture_format'] in TRIPO_CONVERSION_TEXTURE):
            data.update(texture_format=kwargs['texture_format'])

        if ('pivot_to_center_bottom' in kwargs and
           isinstance(kwargs['pivot_to_center_bottom'], bool)):
            data.update(
                pivot_to_center_bottom=kwargs['pivot_to_center_bottom'])

        if ('scale_factor' in kwargs and
           isinstance(kwargs['scale_factor'], int)):
            data.update(scale_factor=kwargs['scale_factor'])

        parameters.update(data=data)

        return parameters
