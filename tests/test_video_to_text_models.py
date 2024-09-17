import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.video_to_text_models import GoogleVideoToText
from llmmaster import LLMMaster


API_KEY = '''
'''


INSTANCE_CLASSES = {
    'google': GoogleVideoToText
}


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_google_vtt(run_api):
    judgment = True
    master = LLMMaster()

    google_vtt_test = master.pack_parameters(provider='google_vtt',
                                             prompt='Describe attached video.',
                                             video_file='test-inputs/test_video.mp4')
    master.set_api_keys(API_KEY)
    master.summon({'google_vtt_test': google_vtt_test})

    for key, value in master.instances.items():
        print(f'{key} = {value.parameters}')
        if not isinstance(value, GoogleVideoToText):
            judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        print('Responses')
        for key, value in master.results.items():
            print(f'{key} = {value}')
            if not value:
                judgment = False

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True
