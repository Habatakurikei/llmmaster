# https://platform.tripo3d.ai/docs
import requests

from .base_model import BaseModel
from .config import TRIPO_BASE_EP
from .config import TRIPO_TASK_EP
from .config import TRIPO_RESULT_EP
from .config import TRIPO_MODELS
from .config import TRIPO_STATUS_IN_PROGRESS
from .config import WAIT_FOR_TRIPO_RESULT
from .config import REQUEST_OK


class TripoModelBase(BaseModel):
    '''
    Base model for Tripo API wrapper.
    Tripo provides:
      1. text_to_model (tt3d)
      2. image_to_model (it3d)
      3. multiview_to_model (3d)
      4. refine_model (refine)
      5. animate_prerigcheck ()
      6. animate_rig
      7. animate_retarget
      8. stylize_model
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
            response_json = response.json()

            response = self._fetch_result(response_json['data']['task_id'])

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
        global TRIPO_RESULT_EP

        answer = 'Generated model not found.'

        header = {'Authorization': f'Bearer {self.api_key}'}

        ep = TRIPO_RESULT_EP.format(tid = id)

        flg = True

        while flg:
            response = requests.request(method='GET',
                                        url=ep,
                                        headers=header)
            response_json = response.json()

            if response_json['data']['status'] in WAIT_FOR_TRIPO_RESULT:
                self._wait(WAIT_FOR_TRIPO_RESULT)
            else:
                answer = response
                flg = False

        return answer


