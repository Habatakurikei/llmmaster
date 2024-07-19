# this file may contain classes of:
# - text-to-speech model (TTS)
# - text-to-music model (TTM)
import os

from openai import OpenAI

from .base_model import BaseModel

from .config import OPENAI_KEY_NAME
from .config import OPENAI_TTS_RESPONSE_FORMAT_LIST
from .config import OPENAI_TTS_VOICE_OPTIONS
from .config import OPENAI_TTS_DEFAULT_SPEED
from .config import OPENAI_TTS_MAX_SPEED
from .config import OPENAI_TTS_MIN_SPEED


class OpenAITextToSpeech(BaseModel):
    '''
    List of available models as of 2024-07-04:
      - tts-1
      - tts-1-hd
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAITextToSpeech'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        OpenAI Text-To-Speech returns class.
        Save the generated audio using `response.stream_to_file()`.
        When failed to generate audio file, return value is given in str.
        Handle return value `answer` with care for different type in case of
        success and failure.
        '''
        # msg = f'Summon OpenAI Text-To-Speech with {self.parameters["model"]}'
        # print(msg)

        answer = 'Audio not generated.'

        try:
            client = OpenAI(api_key=os.getenv(OPENAI_KEY_NAME))

            response = client.audio.speech.create(
                model=self.parameters['model'],
                voice=self.parameters['voice'],
                input=self.parameters['prompt'],
                response_format=self.parameters['response_format'],
                speed=self.parameters['speed'])

            if response:
                answer = response

        except Exception as e:
            answer = str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs (common):
          - input = prompt
          - voice: alloy, echo, fable, onyx, nova, or shimmer
          - response_format: mp3, opus, aac, flac, wav, or pcm
          - speed: float between 0.25 and 4.0
        '''
        parameters = kwargs

        if ('voice' not in kwargs or
           kwargs['voice'] not in OPENAI_TTS_VOICE_OPTIONS):
            parameters.update(voice=OPENAI_TTS_VOICE_OPTIONS[0])

        if ('response_format' not in kwargs or
           kwargs['response_format'] not in OPENAI_TTS_RESPONSE_FORMAT_LIST):
            parameters.update(
                response_format=OPENAI_TTS_RESPONSE_FORMAT_LIST[0])

        if 'speed' not in kwargs:
            parameters.update(speed=OPENAI_TTS_DEFAULT_SPEED)
        else:
            buff = kwargs['speed']
            if (isinstance(buff, float) and
               OPENAI_TTS_MIN_SPEED <= buff and
               buff <= OPENAI_TTS_MAX_SPEED):
                pass
            else:
                parameters['speed'] = OPENAI_TTS_DEFAULT_SPEED

        return parameters
