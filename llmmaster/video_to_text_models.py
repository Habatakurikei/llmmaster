import os
import time

import google.generativeai as genai

from .base_model import BaseModel
from .config import GOOGLE_KEY_NAME
from .config import WAIT_FOR_GOOGLE_VTT_UPLOAD
from .config import WAIT_FOR_GOOGLE_VTT_TIMEOUT


class GoogleVideoToText(BaseModel):
    '''
    List of typical available models as of 2024-07-04:
      - gemini-1.5-pro
      - gemini-1.5-flash
      - gemini-1.0-pro
    Note: Ensure the chosen model supports video processing.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'GoogleVideoToText'
            raise Exception(msg) from e

    def run(self):

        message = 'Video description not generated.'

        try:
            genai.configure(api_key=os.getenv(GOOGLE_KEY_NAME))

            model = genai.GenerativeModel(model_name=self.parameters['model'])
            video = self._upload_file()

            response = model.generate_content(
                [video, self.parameters['prompt']],
                request_options={'timeout': WAIT_FOR_GOOGLE_VTT_TIMEOUT})

            genai.delete_file(video.name)

            if hasattr(response, 'text'):
                message = response.text.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs:
        video_file = "/path/to/local/video2.mp4"
        '''
        parameters = kwargs

        if 'video_file' not in kwargs:
            msg = "'video_file' parameter is required with "
            msg += "at least one valid file path."
            raise ValueError(msg)

        return parameters

    def _upload_file(self):

        video_file = genai.upload_file(path=self.parameters['video_file'])

        while video_file.state.name == 'PROCESSING':
            time.sleep(WAIT_FOR_GOOGLE_VTT_UPLOAD)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == 'FAILED':
            raise ValueError('Failed to upload video file.')

        return video_file
