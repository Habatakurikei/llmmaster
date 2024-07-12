import os

from openai import OpenAI

from .base_model import BaseModel

from .config import OPENAI_KEY_NAME
from .config import OPENAI_TTI_SIZE_LIST
from .config import OPENAI_TTI_QUALITY_LIST
from .config import OPENAI_TTI_DEFAULT_SIZE
from .config import OPENAI_TTI_DEFAULT_QUALITY
from .config import OPENAI_TTI_DEFAULT_N


class OpenAITextToImage(BaseModel):
    '''
    List of available models as of 2024-07-04:
      - dall-e-2
      - dall-e-3
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAITextToImage'
            raise Exception(msg) from e

    def run(self):

        # msg = f'Summon OpenAI Text to Image with {self.parameters["model"]}'
        # print(msg)

        generated_url = 'Generated image URL not found.'

        try:
            client = OpenAI(api_key=os.getenv(OPENAI_KEY_NAME))

            response = client.images.generate(
                model=self.parameters['model'],
                prompt=self.parameters['prompt'],
                size=self.parameters['size'],
                quality=self.parameters['quality'],
                n=self.parameters['n'])

        except Exception as e:
            msg = 'Error occurred while creating OpenAI LLM instance.'
            raise Exception(msg) from e

        if hasattr(response, 'data'):
            generated_url = response.data[0].url

        # print(f'OpenAI responded =\n{generated_url}\n')

        self.response = generated_url

    def _verify_arguments(self, **kwargs):
        '''
        Overwrite from BaseModel for this particular model.
        Set parameters of size, quality and n
        '''
        parameters = kwargs

        if 'size' not in kwargs or kwargs['size'] not in OPENAI_TTI_SIZE_LIST:
            parameters.update(size=OPENAI_TTI_DEFAULT_SIZE)
        else:
            parameters.update(size=kwargs['size'])

        if ('quality' not in kwargs or
           kwargs['quality'] not in OPENAI_TTI_QUALITY_LIST):
            parameters.update(quality=OPENAI_TTI_DEFAULT_QUALITY)
        else:
            parameters.update(quality=kwargs['quality'])

        if 'n' not in kwargs:
            parameters.update(n=OPENAI_TTI_DEFAULT_N)
        else:
            buff = kwargs['n']
            if isinstance(buff, int) and 0 < buff and buff <= 3:
                pass
            else:
                parameters['n'] = OPENAI_TTI_DEFAULT_N

        return parameters
