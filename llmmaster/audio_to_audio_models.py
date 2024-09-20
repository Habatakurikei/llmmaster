import os

from elevenlabs.client import ElevenLabs

from .base_model import BaseModel


class ElevenLabsAudioIsolation(BaseModel):
    '''
    No specific model for this function.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'ElevenLabsAudioIsolation'
            raise Exception(msg) from e

    def run(self):
        '''
        Note:
        ElevenLabs Audio Isolation returns binary audio data.
        Save the generated audio using `elevenlabs.save()`.
        But when failed to generate, return value is given in str.
        Handle return value `answer` with care for different type
        in case of success and failure.
        '''
        answer = 'Valid audio not generated. '

        try:
            client = ElevenLabs(api_key=self.api_key)

            response = client.audio_isolation.audio_isolation(
                audio=self.parameters['audio'])

            if response:
                answer = response

        except Exception as e:
            answer += str(e)

        self.response = answer

    def _verify_arguments(self, **kwargs):
        """
        Verify and process arguments for Voicevox Text-to-Speech.
        Expected inputs:
          - audio: file path to original audio
        """
        parameters = kwargs

        if 'audio' in kwargs and os.path.isfile(kwargs['audio']):
            parameters['audio'] = open(kwargs['audio'], 'rb')
        else:
            msg = f'Invalid audio file given {kwargs["audio"]}'
            raise ValueError(msg)

        return parameters
