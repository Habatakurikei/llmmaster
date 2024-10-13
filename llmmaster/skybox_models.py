import requests
from PIL import Image

from .base_model import BaseModel
from .config import REQUEST_OK
from .config import SKYBOX_BASE_EP
from .config import SKYBOX_EXPORT_EP
from .config import SKYBOX_EXPORT_RESULT_EP
from .config import SKYBOX_GENERATION_EP
from .config import SKYBOX_GENERATION_RESULT_EP
from .config import SKYBOX_STATUS_IN_PROGRESS
from .config import WAIT_FOR_SKYBOX_RESULT


class SkyboxBase(BaseModel):
    '''
    Base model for Skybox API wrapper.
    Skybox provides:
      1. Text-To-Panorama model (skybox_ttp)
      2. Panorama-To-Image/Video model (skybox_ptiv)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for Skybox'
            raise Exception(msg) from e

    def run(self):
        '''
        Implement run method for each model of sub-class.
        '''
        pass

    def _fetch_result(self, id=''):
        '''
        Implement fetch result method for each model of sub-class.
        '''
        pass

    def _common_headers(self):
        '''
        Common headers for generation and result fetching.
        '''
        headers = {'x-api-key': self.api_key}
        return headers


class SkyboxTextToPanorama(SkyboxBase):
    '''
    Text-To-Panorama model
    '''
    def run(self):
        '''
        Note:
        Return json of response request.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid model not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     data=self.parameters['data'])
            response = self._fetch_result(id=response.json().get('id'))

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

        header = self._common_headers()
        url = SKYBOX_BASE_EP + SKYBOX_GENERATION_RESULT_EP.format(id=id)

        flg = True
        while flg:
            response = requests.request(method='GET',
                                        url=url,
                                        headers=header)
            res_json = response.json().get('request')
            # print(res_json['status'])
            if (response.status_code == REQUEST_OK and
               res_json['status'] in SKYBOX_STATUS_IN_PROGRESS):
                self._wait(WAIT_FOR_SKYBOX_RESULT)
            else:
                answer = response
                flg = False

        return answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          skybox_style_id (required): int
          prompt (required): str
          negative_text: str
          enhance_prompt: bool
          seed: int
          remix_imagine_id: int
          control_image: binary/base64/url
          control_model: str
          webhook_url: str
        '''
        parameters = kwargs

        parameters.update(url=SKYBOX_BASE_EP+SKYBOX_GENERATION_EP)
        parameters.update(headers=self._common_headers())

        # body data
        data = {'prompt': kwargs['prompt']}

        if 'skybox_style_id' not in kwargs:
            msg = 'skybox_style_id is required.'
            raise ValueError(msg)
        data['skybox_style_id'] = kwargs['skybox_style_id']

        if 'negative_text' in kwargs:
            data['negative_text'] = kwargs['negative_text']

        if ('enhance_prompt' in kwargs and
           isinstance(kwargs['enhance_prompt'], bool)):
            data['enhance_prompt'] = kwargs['enhance_prompt']

        if 'seed' in kwargs and isinstance(kwargs['seed'], int):
            data['seed'] = kwargs['seed']

        if ('remix_imagine_id' in kwargs and
           isinstance(kwargs['remix_imagine_id'], int)):
            data['remix_imagine_id'] = kwargs['remix_imagine_id']

        if 'control_image' not in kwargs:
            pass
        elif isinstance(kwargs['control_image'], str):
            if kwargs['control_image'].startswith(('http://', 'https://')):
                data['control_image'] = kwargs['control_image']
            else:
                data['control_image'] = Image.open(kwargs['control_image'])

        if 'control_model' in kwargs:
            data['control_model'] = kwargs['control_model']

        if 'webhook_url' in kwargs:
            data['webhook_url'] = kwargs['webhook_url']

        parameters.update(data=data)

        return parameters


class SkyboxPanoramaToImageVideo(SkyboxBase):
    '''
    Panorama-To-Image/Video model
    '''
    def run(self):
        '''
        Note:
        Return json of response request.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid output not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     data=self.parameters['data'])
            response = self._fetch_result(id=response.json().get('id'))

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

        header = self._common_headers()
        url = SKYBOX_BASE_EP + SKYBOX_EXPORT_RESULT_EP.format(id=id)

        flg = True
        while flg:
            response = requests.request(method='GET',
                                        url=url,
                                        headers=header)
            res_json = response.json()
            # print(res_json['status'])
            if (response.status_code == REQUEST_OK and
               res_json['status'] in SKYBOX_STATUS_IN_PROGRESS):
                self._wait(WAIT_FOR_SKYBOX_RESULT)
            else:
                answer = response
                flg = False

        return answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          skybox_id (required): str
          type_id (required): int
            1: jpg, 2: png, 3: cube map,
            4: HDRI HDR, 5: HDRI EXR, 6: depth map,
            7: mp4 landscape, 8: mp4 portrait, 9: mp4 square
          webhook_url: str
        '''
        parameters = kwargs

        parameters.update(url=SKYBOX_BASE_EP+SKYBOX_EXPORT_EP)
        parameters.update(headers=self._common_headers())

        # body data
        data = {}

        if 'skybox_id' not in kwargs:
            msg = 'skybox_id is required.'
            raise ValueError(msg)
        data['skybox_id'] = kwargs['skybox_id']

        if 'type_id' not in kwargs or not isinstance(kwargs['type_id'], int):
            msg = 'type_id is required and must be int.'
            raise ValueError(msg)
        data['type_id'] = kwargs['type_id']

        if 'webhook_url' in kwargs:
            data['webhook_url'] = kwargs['webhook_url']

        parameters.update(data=data)

        return parameters
