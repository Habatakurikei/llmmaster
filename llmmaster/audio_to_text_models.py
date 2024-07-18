import os

from openai import OpenAI

from .base_model import BaseModel

from .config import OPENAI_ATT_DEFAULT_TIMESTAMP_GRANULARITIES
from .config import OPENAI_ATT_MODE_LIST
from .config import OPENAI_ATT_RESPONSE_FORMAT_LIST
from .config import OPENAI_KEY_NAME
from .config import TEMPERATURE


class OpenAIAudioToText(BaseModel):
    '''
    List of available models as of 2024-07-17:
      - whisper-1
    Note that translation supports only into English for the moment.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAIAudioToText'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        OpenAI Audio-to-Text returns class Translation or Transcription.
        These classes may contain multiple attributes of str, list or dict:
        `text`, `task`, `language`, `duration`, `segments` and `words`
        When failed to process audio file, return value is given in str.
        Handle return value `answer` with care for different type in case of
        success and failure. Also differ from `response_format`.
        '''
        # msg = f'Summon OpenAI Audio-to-Text with {self.parameters["model"]}'
        # print(msg)

        answer = 'Text not generated.'

        try:
            client = OpenAI(api_key=os.getenv(OPENAI_KEY_NAME))

            if self.parameters['mode'] == 'translations':
                # print('OpenAI Audio-to-Text: translations')
                response = client.audio.translations.create(
                    model=self.parameters['model'],
                    file=self.parameters['file'],
                    response_format=self.parameters['response_format'],
                    temperature=self.parameters['temperature'])

            elif (self.parameters['mode'] == 'transcriptions' and
                  self.parameters['response_format'] == 'verbose_json'):
                # print('OpenAI Audio-to-Text: verbose_json transcriptions')
                tg = self.parameters['timestamp_granularities']
                response = client.audio.transcriptions.create(
                    model=self.parameters['model'],
                    file=self.parameters['file'],
                    response_format=self.parameters['response_format'],
                    temperature=self.parameters['temperature'],
                    language=self.parameters['language'],
                    timestamp_granularities=tg)

            else:
                # print('OpenAI Audio-to-Text: general transcriptions')
                response = client.audio.transcriptions.create(
                    model=self.parameters['model'],
                    file=self.parameters['file'],
                    response_format=self.parameters['response_format'],
                    temperature=self.parameters['temperature'],
                    language=self.parameters['language'])

            if response:
                # print(f'OpenAI Audio-to-Text: response = {response}')
                answer = response

        except Exception as e:
            answer = str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs (common):
          - mode: either transcriptions or translations
          - file: local audio file to process
          - response_format: json, text, srt, verbose_json, or vtt
          - temperature: positive float between 0 and 1
        Expected inputs (only for transcripts):
          - language: ISO 639-1 format like 'en'
          - timestamp_granularities: ["word"] or ["segment"] or both in list
        '''
        parameters = kwargs

        if 'mode' not in kwargs or kwargs['mode'] not in OPENAI_ATT_MODE_LIST:
            msg = "'mode' parameter is not selected properly from "
            msg += f"{OPENAI_ATT_MODE_LIST} but {kwargs['mode']} given."
            raise ValueError(msg)

        if 'file' in kwargs and os.path.isfile(kwargs['file']):
            parameters['file'] = open(kwargs['file'], 'rb')
        else:
            msg = f'Invalid audio file given {kwargs["file"]}'
            raise ValueError(msg)

        if 'response_format' not in kwargs:
            parameters['response_format'] = OPENAI_ATT_RESPONSE_FORMAT_LIST[0]

        if 'temperature' not in kwargs:
            parameters['temperature'] = TEMPERATURE
        else:
            buff = kwargs['temperature']
            if isinstance(buff, float) and 0.0 <= buff and buff <= 1.0:
                pass
            else:
                parameters['temperature'] = TEMPERATURE

        if 'language' not in kwargs:
            parameters['language'] = 'ja'

        if (kwargs['response_format'] == 'verbose_json' and
            ('timestamp_granularities' not in kwargs or
           not isinstance(kwargs['timestamp_granularities'], list))):
            parameters['timestamp_granularities'] = \
                OPENAI_ATT_DEFAULT_TIMESTAMP_GRANULARITIES

        return parameters
