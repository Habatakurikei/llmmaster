import os

import requests

from .base_model import BaseModel
from .config import MAX_SEED
from .config import REQUEST_ACCEPTED
from .config import STABLE_DIFFUSION_BASE_EP
from .config import STABLE_DIFFUSION_ITV_CFG_SCALE_DEFAULT
from .config import STABLE_DIFFUSION_ITV_CFG_SCALE_MIN
from .config import STABLE_DIFFUSION_ITV_CFG_SCALE_MAX
from .config import STABLE_DIFFUSION_ITV_MOTION_BUCKET_DEFAULT
from .config import STABLE_DIFFUSION_ITV_MOTION_BUCKET_MIN
from .config import STABLE_DIFFUSION_ITV_MOTION_BUCKET_MAX
from .config import STABLE_DIFFUSION_ITV_RESULT_EP
from .config import STABLE_DIFFUSION_ITV_START_EP
from .config import REQUEST_OK
from .config import WAIT_FOR_ITV_RESULT


class StableDiffusionImageToVideo(BaseModel):
    '''
    Model: v2beta fixed as of 2024-07-20
    Acceptable formats: png and jpg
    Acceptable dimentions: 1024x576, 576x1024, 768x768
    Output format: mp4 only
    This model does not require prompt.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'StableDiffusionImageToVideo'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Stable Diffusion returns binary data of generated video in mp4 format.
        LLMMaster returns requests.models.Response class directly.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid video not generated. '

        try:
            response = requests.post(self.parameters['url'],
                                     headers=self.parameters['headers'],
                                     files=self.parameters['files'],
                                     data=self.parameters['data'])

            response = self._fetch_result(response.json().get('id'))

            if response.status_code == REQUEST_OK:
                answer = response
            else:
                answer += str(response.json())

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
          - cfg_scale (required): int,
          - motion_bucket_id (required): int,
          - seed: int
        '''
        parameters = kwargs

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITV_START_EP)

        parameters.update(url=endpoint)

        endpoint = (STABLE_DIFFUSION_BASE_EP + '/' + kwargs['model'] +
                    STABLE_DIFFUSION_ITV_RESULT_EP)

        parameters.update(url_result=endpoint)

        # headers
        headers = {'authorization': f'Bearer {self.api_key}'}

        parameters.update(headers=headers)

        # files
        if not os.path.isfile(kwargs['image']):
            msg = f"'image' {kwargs['image']} is not a valid file"
            raise ValueError(msg)
        else:
            with open(kwargs['image'], "rb") as f:
                parameters.update(files={'image': f.read()})

        # body data
        data = {}

        if 'cfg_scale' not in kwargs:
            data.update(cfg_scale=STABLE_DIFFUSION_ITV_CFG_SCALE_DEFAULT)
        else:
            cfg_scale = kwargs['cfg_scale']
            if (isinstance(cfg_scale, int) and
               STABLE_DIFFUSION_ITV_CFG_SCALE_MIN <= cfg_scale and
               cfg_scale <= STABLE_DIFFUSION_ITV_CFG_SCALE_MAX):
                data.update(cfg_scale=cfg_scale)
            else:
                data.update(cfg_scale=STABLE_DIFFUSION_ITV_CFG_SCALE_DEFAULT)

        if 'motion_bucket_id' not in kwargs:
            data.update(
                motion_bucket_id=STABLE_DIFFUSION_ITV_MOTION_BUCKET_DEFAULT
                )
        else:
            motion_bucket_id = kwargs['motion_bucket_id']
            if (isinstance(motion_bucket_id, int) and
               STABLE_DIFFUSION_ITV_MOTION_BUCKET_MIN <= motion_bucket_id and
               motion_bucket_id <= STABLE_DIFFUSION_ITV_MOTION_BUCKET_MAX):
                data.update(motion_bucket_id=motion_bucket_id)
            else:
                data.update(
                    motion_bucket_id=STABLE_DIFFUSION_ITV_MOTION_BUCKET_DEFAULT
                )

        if 'seed' in kwargs:
            seed = kwargs['seed']
            if isinstance(seed, int) and 0 <= seed and seed <= MAX_SEED:
                data.update(seed=seed)

        parameters.update(data=data)

        return parameters

    def _fetch_result(self, id=''):
        '''
        Fetch result for image-to-video conversion
        '''
        answer = 'Generated file not found.'

        ep = self.parameters['url_result'].replace('{id}', id)

        headers_result = self.parameters['headers']
        headers_result.update(accept='video/*')

        flg = True

        while flg:
            response = requests.request(method='GET',
                                        url=ep,
                                        headers=headers_result)

            if response.status_code == REQUEST_ACCEPTED:
                self._wait(WAIT_FOR_ITV_RESULT)

            else:
                answer = response
                flg = False

        return answer
