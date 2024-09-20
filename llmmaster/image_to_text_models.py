from io import BytesIO

import google.generativeai as genai
import requests
from openai import OpenAI
from PIL import Image

from .base_model import BaseModel
from .config import DEFAULT_TOKENS


class OpenAIImageToText(BaseModel):
    '''
    Use GPT-4o or GPT4-Turbo family models.
    Note that all models do not support vision capability.
    Acceptable formats: png, jpg, webp and gif
    Only online images are supported for the moment.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'OpenAIImageToText'
            raise Exception(msg) from e

    def run(self):

        message = 'Valid text not generated. '

        try:
            client = OpenAI(api_key=self.api_key)

            content = [{"type": "text", "text": self.parameters['prompt']}]
            content.extend(self.parameters['image_url'])

            response = client.chat.completions.create(
                model=self.parameters['model'],
                max_tokens=self.parameters['max_tokens'],
                messages=[{"role": "user", "content": content}])

            if hasattr(response, 'choices'):
                message = response.choices[0].message.content.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs:
          - image_url: list of url strings such as:
            image_url = ["https://example.com/image1.jpg",
                         "https://example.com/image2.jpg"]
          - max_tokens: natural number between 1 and 4096 (in most providers)
          - detail: this parameter is not supported for LLMMaster.
        '''
        parameters = kwargs

        if 'image_url' not in kwargs:
            msg = "'image_url' parameter is required with at least one URL."
            raise ValueError(msg)

        image_url = []

        for entry in kwargs['image_url']:
            buff = {'type': 'image_url',
                    'image_url': {'url': self._sanitize_url(entry)}}
            image_url.append(buff)

        parameters.update(image_url=image_url)

        if 'max_tokens' not in kwargs:
            parameters.update(max_tokens=DEFAULT_TOKENS)

        else:
            buff = kwargs['max_tokens']
            if isinstance(buff, int) and 0 < buff:
                pass
            else:
                parameters['max_tokens'] = DEFAULT_TOKENS

        return parameters


class GoogleImageToText(BaseModel):
    '''
    Note: Ensure the chosen model supports image processing.
      Gemini models mainly support this function.
    Acceptable formats: png, jpg, webp, heic and heif
    Both online and offline (local) images are supported.
    '''
    def __init__(self, **kwargs):

        try:
            super().__init__(**kwargs)

        except Exception as e:
            msg = 'Error while verifying specific parameters for '
            msg += 'GoogleImageToText'
            raise Exception(msg) from e

    def run(self):

        message = 'Valid text not generated. '

        try:
            genai.configure(api_key=self.api_key)

            model = genai.GenerativeModel(model_name=self.parameters['model'])

            to_send = [self.parameters['prompt']]

            for entry in self.parameters['image_url']:
                if entry.startswith(('http://', 'https://')):
                    # Handle online images
                    response = requests.get(entry)
                    image = Image.open(BytesIO(response.content))
                else:
                    # Handle local images
                    image = Image.open(entry)
                to_send.append(image)

            response = model.generate_content(to_send)

            if hasattr(response, 'text'):
                message = response.text.strip()

        except Exception as e:
            message = str(e)

        self.response = message

    def _verify_arguments(self, **kwargs):
        '''
        Expected inputs are a list of url strings such as:
        image_url = ["https://example.com/image1.jpg",
                     "https://example.com/image2.jpg"]
        For both local or online images are supported.
        '''
        parameters = kwargs

        if 'image_url' not in kwargs:
            msg = "'image_url' parameter is required with at least one URL."
            raise ValueError(msg)

        return parameters
