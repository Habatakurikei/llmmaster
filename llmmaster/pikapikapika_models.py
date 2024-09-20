import requests

from .base_model import BaseModel
from .config import PIKAPIKAPIKA_BASE_EP
from .config import PIKAPIKAPIKA_GENERATION_EP
# from .config import PIKAPIKAPIKA_LIPSYNC_EP
# from .config import PIKAPIKAPIKA_ADJUST_EP
# from .config import PIKAPIKAPIKA_EXTEND_EP
# from .config import PIKAPIKAPIKA_UPSCALE_EP
from .config import PIKAPIKAPIKA_RESULT_EP
from .config import PIKAPIKAPIKA_ASPECT_RATIO_LIST
from .config import PIKAPIKAPIKA_MAX_FPS
from .config import PIKAPIKAPIKA_STYLE_LIST
from .config import WAIT_FOR_PIKAPIKAPIKA_RESULT
from .config import REQUEST_OK


class PikaPikaPikaModelBase(BaseModel):
    '''
    Base model for PikaPikaPika.art API wrapper.
    PikaPikaPika.art provides:
      1. Text-To-Video model (ttv)
      2. LipSync model (lipsync)
      3. Adjust model (adjust)
      4. Extend model (extend)
      5. Upscale model (upscale)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for PikaPikaPika'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Return raw response of request.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid video not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     json=self.parameters['data'])

            json = response.json()
            response = self._fetch_result(id=json['job']['id'])

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
        answer = 'Generated result not found.'

        header = {'Authorization': f'Bearer {self.api_key}'}

        ep = PIKAPIKAPIKA_BASE_EP + PIKAPIKAPIKA_RESULT_EP.format(id=id)

        flg = True
        while flg:
            response = requests.request(method='GET', url=ep, headers=header)
            json = response.json()
            if json['job']['status'] != 'finished':
                self._wait(WAIT_FOR_PIKAPIKAPIKA_RESULT)
            else:
                answer = response
                flg = False

        return answer


class PikaPikaPikaGeneration(PikaPikaPikaModelBase):
    '''
    Output format:
    This model does not require prompt.
    '''
    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
        style: str
        sfx: bool
        frameRate: int
        aspectRatio: str
        camera: dict
        parameters: dict
        '''
        parameters = kwargs

        endpoint = PIKAPIKAPIKA_BASE_EP + PIKAPIKAPIKA_GENERATION_EP
        parameters.update(url=endpoint)

        # headers
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}

        parameters.update(headers=headers)

        # body data
        data = {'promptText': kwargs['prompt']}

        # style
        if 'style' in kwargs and kwargs['style'] in PIKAPIKAPIKA_STYLE_LIST:
            data.update(style=kwargs['style'])

        # sound effects
        if 'sfx' in kwargs and isinstance(kwargs['sfx'], bool):
            data.update(sfx=kwargs['sfx'])

        # options
        options = {'extend': False}

        if ('frameRate' in kwargs and
           isinstance(kwargs['frameRate'], int) and
           0 < kwargs['frameRate'] and
           kwargs['frameRate'] <= PIKAPIKAPIKA_MAX_FPS):
            options.update(frameRate=kwargs['frameRate'])
        else:
            options.update(frameRate=PIKAPIKAPIKA_MAX_FPS)

        if ('aspectRatio' in kwargs and
           kwargs['aspectRatio'] in PIKAPIKAPIKA_ASPECT_RATIO_LIST):
            options.update(aspectRatio=kwargs['aspectRatio'])
        else:
            options.update(aspectRatio=PIKAPIKAPIKA_ASPECT_RATIO_LIST[0])

        if 'camera' in kwargs and isinstance(kwargs['camera'], dict):
            options.update(camera=kwargs['camera'])

        if 'parameters' in kwargs and isinstance(kwargs['parameters'], dict):
            options.update(parameters=kwargs['parameters'])

        data.update(options=options)

        parameters.update(data=data)

        return parameters
