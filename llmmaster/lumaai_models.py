import json

from lumaai import LumaAI

from .base_model import BaseModel
from .config import LUMAAI_ASPECT_RATIO_LIST
from .config import LUMAAI_STATUS_IN_PROGRESS
from .config import WAIT_FOR_LUMAI_RESULT


class LumaDreamMachineBase(BaseModel):
    '''
    Base model for Luma AI API wrapper.
    Luma AI provides:
      1. Text-To-Video model (ttv)
      2. Image-To-Video model (itv)
      3. Video-To-Video model (vtv)
    Commonize init and run for these models.
    Separately define _verify_arguments() due to different parameters.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for Luma AI'
            raise Exception(msg) from e

    def run(self):
        '''
        Implement run method for each model of sub-class.
        '''
        pass

    def _fetch_result(self, instance: LumaAI, id: str):
        '''
        Fetch result from LumaAI instance.
        '''
        answer = ''
        flg = True
        while flg:
            status = instance.generations.get(id=id)
            if status.state in LUMAAI_STATUS_IN_PROGRESS:
                self._wait(WAIT_FOR_LUMAI_RESULT)
            else:
                answer = json.loads(status.json())
                flg = False
        return answer


class LumaDreamMachineTextToVideo(LumaDreamMachineBase):
    '''
    Text-To-Video model
    '''
    def run(self):
        '''
        Note:
        Return json of response Generation class defined in LumaAI.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid video not generated. '

        try:
            client = LumaAI(auth_token=self.api_key)

            response = client.generations.create(
                prompt=self.parameters['prompt'],
                loop=self.parameters['loop'],
                aspect_ratio=self.parameters['aspect_ratio'])

            answer = self._fetch_result(instance=client, id=response.id)

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
        aspect_ratio: str
        loop: bool
        '''
        parameters = kwargs

        if 'loop' in kwargs and isinstance(kwargs['loop'], bool):
            pass
        else:
            parameters.update(loop=False)

        if ('aspect_ratio' in kwargs and
           isinstance(kwargs['aspect_ratio'], str) and
           kwargs['aspect_ratio'] in LUMAAI_ASPECT_RATIO_LIST):
            pass
        else:
            parameters.update(aspect_ratio=LUMAAI_ASPECT_RATIO_LIST[0])

        return parameters


class LumaDreamMachineImageToVideo(LumaDreamMachineBase):
    '''
    Image-To-Video model
    Important: input accepts only JPG, not PNG.
    '''
    def run(self):
        '''
        Note:
        Return json of response Generation class defined in LumaAI.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid video not generated. '

        try:
            client = LumaAI(auth_token=self.api_key)

            response = client.generations.create(
                prompt=self.parameters['prompt'],
                keyframes=self.parameters['keyframes'])

            answer = self._fetch_result(instance=client, id=response.id)

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
        frame0: URL of image for the start frame
        frame1: URL of image for the end frame
        '''
        parameters = kwargs

        keyframes = {}
        if 'frame0' in kwargs and isinstance(kwargs['frame0'], str):
            keyframes.update(frame0={
                'type': 'image',
                'url': self._sanitize_url(kwargs['frame0'])
            })
        if 'frame1' in kwargs and isinstance(kwargs['frame1'], str):
            keyframes.update(frame1={
                'type': 'image',
                'url': self._sanitize_url(kwargs['frame1'])
            })

        parameters.update(keyframes=keyframes)
        return parameters


class LumaDreamMachineVideoToVideo(LumaDreamMachineBase):
    '''
    Video-To-Video model
    Important: image input is acceptable but only JPG, not PNG.
    '''
    def run(self):
        '''
        Note:
        Return json of response Generation class defined in LumaAI.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid video not generated. '

        try:
            client = LumaAI(auth_token=self.api_key)

            response = client.generations.create(
                prompt=self.parameters['prompt'],
                keyframes=self.parameters['keyframes'])

            answer = self._fetch_result(instance=client, id=response.id)

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected options:
        frame0: URL of image or video for the start frame
        frame1: URL of image or video for the end frame
        '''
        parameters = kwargs

        if 'keyframes' in kwargs and isinstance(kwargs['keyframes'], dict):
            pass
        else:
            parameters.update(keyframes={})

        return parameters
