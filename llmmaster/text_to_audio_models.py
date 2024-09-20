# this file may contain classes of:
# - text-to-speech model (TTS)
# - text-to-sound model (TTSE)
# - text-to-music model (TTM)
import requests
from elevenlabs import Voice
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from openai import OpenAI

from .base_model import BaseModel
from .config import ELEVENLABS_TTS_MODELS
from .config import ELEVENLABS_DEFAULT_VOICE_ID
from .config import ELEVENLABS_DEFAULT_STABILITY
from .config import ELEVENLABS_DEFAULT_SIMILARITY
from .config import ELEVENLABS_DEFAULT_PROMPT_INFLUENCE
from .config import OPENAI_TTS_RESPONSE_FORMAT_LIST
from .config import OPENAI_TTS_VOICE_OPTIONS
from .config import OPENAI_TTS_DEFAULT_SPEED
from .config import OPENAI_TTS_MAX_SPEED
from .config import OPENAI_TTS_MIN_SPEED
from .config import VOICEVOX_BASE_EP
from .config import VOICEVOX_QUERY_EP
from .config import VOICEVOX_SYNTHESIS_EP
from .config import VOICEVOX_DEFAULT_VOICE_ID
from .config import REQUEST_OK


class OpenAITextToSpeech(BaseModel):
    '''
    List of available models as of 2024-07-04:
      - tts-1
      - tts-1-hd
    Output formats: mp3, opus, aac, flac and pcm
    Voice variations: alloy, echo, fable, onyx, nova, and shimmer
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
        answer = 'Valid speech not generated. '

        try:
            client = OpenAI(api_key=self.api_key)

            response = client.audio.speech.create(
                model=self.parameters['model'],
                voice=self.parameters['voice'],
                input=self.parameters['prompt'],
                response_format=self.parameters['response_format'],
                speed=self.parameters['speed'])

            if response:
                answer = response

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs (common):
          - input = prompt
          - voice: str
          - response_format: str
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


class ElevenLabsTextToSpeech(BaseModel):
    '''
    List of available models as of 2024-07-29:
      - eleven_multilingual_v2
      - see ELEVENLABS_TTS_MODELS for full list but not recommended to use
    Output formats: mp3
    Voice variations: see formal document
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'ElevenLabsTextToSpeech'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        ElevenLabs Text-To-Speech returns binary audio data.
        Save the generated audio using `elevenlabs.save()`.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid speech not generated. '

        try:
            client = ElevenLabs(api_key=self.api_key)

            response = client.generate(text=self.parameters['prompt'],
                                       voice=self.parameters['voice'],
                                       model=self.parameters['model'])

            if response:
                answer = response

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs:
          - model_id: str
          - language_code: str
          - voice_settings: VoiceSettings class
          - seed: int
          - previous_text: str
          - next_text: str
          - pronunciation_dictionary_locators: list
          - previous_request_ids: list
          - next_request_ids: list
        '''
        parameters = kwargs

        # model
        if kwargs['model'] in ELEVENLABS_TTS_MODELS:
            pass
        else:
            parameters.update(model=ELEVENLABS_TTS_MODELS[0])

        # voice_id
        if 'voice_id' in kwargs and isinstance(kwargs['voice_id'], str):
            voice_id = kwargs['voice_id']
        else:
            voice_id = ELEVENLABS_DEFAULT_VOICE_ID

        # voice settings
        if ('stability' in kwargs and isinstance(kwargs['stability'], float)):
            stability = kwargs['stability']
        else:
            stability = ELEVENLABS_DEFAULT_STABILITY

        if ('similarity_boost' in kwargs and
           isinstance(kwargs['similarity_boost'], float)):
            similarity_boost = kwargs['similarity_boost']
        else:
            similarity_boost = ELEVENLABS_DEFAULT_SIMILARITY

        if ('style' in kwargs and isinstance(kwargs['style'], int)):
            style = kwargs['style']
        else:
            style = 0.0

        if ('use_speaker_boost' in kwargs and
           isinstance(kwargs['use_speaker_boost'], bool)):
            use_speaker_boost = kwargs['use_speaker_boost']
        else:
            use_speaker_boost = True

        voice_settings = VoiceSettings(stability=stability,
                                       similarity_boost=similarity_boost,
                                       style=style,
                                       use_speaker_boost=use_speaker_boost)

        voice = Voice(voice_id=voice_id, settings=voice_settings)

        parameters.update(voice=voice)

        return parameters


class ElevenLabsTextToSoundEffect(BaseModel):
    '''
    No specific model for this function.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'ElevenLabsTextToSoundEffect'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        ElevenLabs Text-To-Sound returns binary audio data.
        Save the generated audio using `elevenlabs.save()`.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid sound not generated. '

        try:
            client = ElevenLabs(api_key=self.api_key)

            response = client.text_to_sound_effects.convert(
                text=self.parameters['prompt'],
                duration_seconds=self.parameters['duration_seconds'],
                prompt_influence=self.parameters['prompt_influence'])

            if response:
                answer = response

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        """
        Verify and process arguments for Voicevox Text-to-Speech.
        Expected inputs:
          - duration_seconds: int/float
          - prompt_influence: float
        """
        parameters = kwargs

        if 'duration_seconds' in kwargs:
            pass
        else:
            parameters.update(duration_seconds=None)

        if 'prompt_influence' in kwargs:
            pass
        else:
            parameters.update(
                prompt_influence=ELEVENLABS_DEFAULT_PROMPT_INFLUENCE)

        return parameters


class VoicevoxTextToSpeech(BaseModel):
    '''
    Voicevox Text-to-Speech model
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'VoicevoxTextToSpeech'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        Voicevox Text-To-Speech returns binary audio data.
        Save the generated audio using `wb`.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid speech not generated. '

        try:
            res_query = requests.post(
                url=VOICEVOX_BASE_EP+VOICEVOX_QUERY_EP,
                params=self.parameters['params'])

            if res_query.status_code == REQUEST_OK:
                answer = self._query_to_speech(res_query.text)
            else:
                answer += f'Error: {res_query.text}'

        except Exception as e:
            answer += f'Error: {str(e)}'

        self.response = answer

    def _verify_arguments(self, **kwargs):
        """
        Verify and process arguments for Voicevox Text-to-Speech.
        Expected inputs:
          - speaker: int
        """
        parameters = kwargs

        params = {'text': kwargs['prompt']}

        if ('speaker' in kwargs and
           isinstance(kwargs['speaker'], int) and
           0 < kwargs['speaker']):
            params['speaker'] = kwargs['speaker']
        else:
            params['speaker'] = VOICEVOX_DEFAULT_VOICE_ID

        parameters.update(params=params)

        return parameters

    def _query_to_speech(self, query_json: str):
        '''
        Convert query json to speech
        '''
        headers = {'Content-Type': 'application/json'}
        params = {'speaker': self.parameters['params']['speaker']}
        res_synth = requests.post(
            url=VOICEVOX_BASE_EP+VOICEVOX_SYNTHESIS_EP,
            headers=headers,
            params=params,
            data=query_json)
        return res_synth
