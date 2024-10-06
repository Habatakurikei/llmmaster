import requests

from .base_model import BaseModel
from .config import REQUEST_OK
from .config import RUNWAY_ASPECT_RATIO_LIST
from .config import RUNWAY_BASE_EP
from .config import RUNWAY_DURATION_LIST
from .config import RUNWAY_IMAGE_TO_VIDEO_EP
from .config import RUNWAY_RESULT_EP
from .config import RUNWAY_STATUS_IN_PROGRESS
from .config import RUNWAY_VERSION
from .config import WAIT_FOR_RUNWAY_RESULT


class RunwayBase(BaseModel):
    '''
    Base model for Runway API wrapper.
    Runway provides:
      1. Image-To-Video model (runway_itv)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for Runway'
            raise Exception(msg) from e

    def run(self):
        '''
        Implement run method for each model of sub-class.
        '''
        pass

    def _fetch_result(self, id=''):
        '''
        Common function to fetch result.
        '''
        answer = 'Generated model not found.'

        header = self._common_headers()
        url = RUNWAY_BASE_EP + RUNWAY_RESULT_EP.format(id=id)

        flg = True
        while flg:
            response = requests.request(method='GET',
                                        url=url,
                                        headers=header)
            # print(response.json().get('status'))
            if (response.status_code == REQUEST_OK and
               response.json().get('status') in RUNWAY_STATUS_IN_PROGRESS):
                self._wait(WAIT_FOR_RUNWAY_RESULT)
            else:
                answer = response
                flg = False

        return answer

    def _common_headers(self):
        '''
        Common headers for generation and result fetching.
        '''
        headers = {'Authorization': f'Bearer {self.api_key}'}
        headers.update({'X-Runway-Version': RUNWAY_VERSION})
        return headers


class RunwayImageToVideo(RunwayBase):
    '''
    Image-To-Video model
    Important: input accepts JPG, PNG or WebP format with up to 16MB.
    '''
    def run(self):
        '''
        Note:
        Return json of response request.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid video not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     json=self.parameters['data'])
            response = self._fetch_result(response.json().get('id'))

            if response.status_code == REQUEST_OK:
                answer = response.json()
            else:
                answer += str(response.json())

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected parameters:
          - promptImage (required): str
          - promptText: str
          - seed: int
          - watermark: bool
          - duration: int (5 or 10)
          - ratio: str (16:9 or 9:16)
        '''
        parameters = kwargs

        parameters.update(url=RUNWAY_BASE_EP+RUNWAY_IMAGE_TO_VIDEO_EP)
        parameters.update(headers=self._common_headers())
        parameters['headers'].update({'Content-Type': 'application/json'})

        # body data
        data = {'promptText': kwargs['prompt'],
                'model': kwargs['model']}

        # promptImage
        if 'promptImage' not in kwargs:
            raise ValueError('promptImage not given.')
        elif not isinstance(kwargs['promptImage'], str):
            msg = 'promptImage type not str.'
            raise ValueError(msg)
        else:
            data.update(promptImage=kwargs['promptImage'])

        # seed
        if 'seed' in kwargs and isinstance(kwargs['seed'], int):
            data.update(seed=kwargs['seed'])

        # watermark
        if 'watermark' in kwargs and isinstance(kwargs['watermark'], bool):
            data.update(watermark=kwargs['watermark'])

        # duration
        if 'duration' in kwargs and kwargs['duration'] in RUNWAY_DURATION_LIST:
            data.update(duration=kwargs['duration'])

        # ratio
        if 'ratio' in kwargs and kwargs['ratio'] in RUNWAY_ASPECT_RATIO_LIST:
            data.update(ratio=kwargs['ratio'])

        parameters.update(data=data)

        return parameters
