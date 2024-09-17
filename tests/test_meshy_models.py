import os
import sys
import requests
from requests.models import Response

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.config import REQUEST_OK
from llmmaster.meshy_models import MeshyTextToTexture
from llmmaster.meshy_models import MeshyTextTo3D
from llmmaster.meshy_models import MeshyTextTo3DRefine
from llmmaster.meshy_models import MeshyTextToVoxel
from llmmaster.meshy_models import MeshyImageTo3D
from llmmaster import LLMMaster


API_KEY = '''
'''


PROMPT ='A Japanese anime girl inspired by Akira Toriyama. Light blue hair, ponytail, pink dress, full body.'
TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_meshy_text_to_3d_instances(run_api):
    '''
    Comment/Uncomment API key handling from environment variable or constant above.
    '''
    judgment = True
    master = LLMMaster()

    id = ''

    meshy_tt3d_test = master.pack_parameters(provider='meshy_tt3d',
                                             prompt=PROMPT,
                                             art_style='cartoon',
                                             negative_prompt='ugly, low resolution')
    master.set_api_keys(API_KEY)
    master.summon({'meshy_tt3d_test': meshy_tt3d_test})

    print(f"Parameters = {master.instances['meshy_tt3d_test'].parameters}")
    print(f"API Key = {master.instances['meshy_tt3d_test'].api_key}")

    if not isinstance(master.instances['meshy_tt3d_test'], MeshyTextTo3D):
        judgment = False

    # step 1 to make text-to-3d model
    if run_api:
        print('Run API for Text-To-3D')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        print('Responses for Text-To-3D, getting id')
        if not isinstance(master.results['meshy_tt3d_test'], Response):
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        else:
            json_result = master.results['meshy_tt3d_test'].json()
            print(f"json_result = {json_result}")
            for key, value in json_result['model_urls'].items():
                if value:
                    res = requests.get(value)
                    if res.status_code == REQUEST_OK:
                        filename = f'meshy_tt3d_test.{key}'
                        filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                        with open(filepath, 'wb') as f:
                            f.write(res.content)
                        print(f'Saved as {filepath}')

            if 'thumbnail_url' in json_result and json_result['thumbnail_url']:
                res = requests.get(json_result['thumbnail_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_tt3d_test_thumbnail.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'video_url' in json_result and json_result['video_url']:
                res = requests.get(json_result['video_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_it3d_test_video.mp4'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'id' in json_result:
                id = json_result['id']
                print(f"id = {id}")

    # step 2 to refine the model
    if run_api and id != '':

        print('Going to refine the model')
        master.dismiss()

        meshy_tt3d_refine_test = master.pack_parameters(provider='meshy_tt3d_refine', preview_task_id=id)
        master.set_api_keys(API_KEY)
        master.summon({'meshy_tt3d_refine_test': meshy_tt3d_refine_test})

        print(f"Parameters = {master.instances['meshy_tt3d_refine_test'].parameters}")

        if not isinstance(master.instances['meshy_tt3d_refine_test'], MeshyTextTo3DRefine):
            pytest.fail(f"Wrong type for MeshyTextTo3DRefine: {type(master.instances['meshy_tt3d_refine_test'])}")

        print('Run API for Refine')

        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        print('Responses for Refine')
        if not isinstance(master.results['meshy_tt3d_refine_test'], Response):
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        else:
            json_result = master.results['meshy_tt3d_refine_test'].json()
            print(f"json_result = {json_result}")
            for key, value in json_result['model_urls'].items():
                if value:
                    res = requests.get(value)
                    if res.status_code == REQUEST_OK:
                        filename = f'meshy_tt3d_test_refined.{key}'
                        filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                        with open(filepath, 'wb') as f:
                            f.write(res.content)
                        print(f'Saved as {filepath}')

            if 'thumbnail_url' in json_result and json_result['thumbnail_url']:
                res = requests.get(json_result['thumbnail_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_tt3d_test_thumbnail_refined.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'video_url' in json_result and json_result['video_url']:
                res = requests.get(json_result['video_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_tt3d_test_video_refined.mp4'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment is True


def test_meshy_text_to_texture_instances(run_api):
    judgment = True
    master = LLMMaster()

    model_url = 'https://habatakurikei.com/dlfiles/zoltraak/model.glb'
    object_prompt = 'A girl in a pink dress with ponytail hair.'
    style_prompt = 'cherry blossum like kimono style outfit'

    meshy_tttx_test = master.pack_parameters(provider='meshy_tttx',
                                             model_url=model_url,
                                             object_prompt=object_prompt,
                                             style_prompt=style_prompt,
                                             art_style='japanese-anime',
                                             negative_prompt='ugly, low resolution',
                                             resolution='1024')
    master.set_api_keys(API_KEY)
    master.summon({'meshy_tttx_test': meshy_tttx_test})

    print(f"Parameters = {master.instances['meshy_tttx_test'].parameters}")

    if not isinstance(master.instances['meshy_tttx_test'], MeshyTextToTexture):
        judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        if not isinstance(master.results['meshy_tttx_test'], Response):
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        else:
            json_result = master.results['meshy_tttx_test'].json()
            print(f"json_result = {json_result}")

            for key, value in json_result['model_urls'].items():
                if value:
                    res = requests.get(value)
                    if res.status_code == REQUEST_OK:
                        filename = f'meshy_tttx_test.{key}'
                        filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                        with open(filepath, 'wb') as f:
                            f.write(res.content)
                        print(f'Saved as {filepath}')

            if 'thumbnail_url' in json_result and json_result['thumbnail_url']:
                res = requests.get(json_result['thumbnail_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_tttx_test_thumbnail.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'texture_urls' in json_result:
                texture_urls = json_result['texture_urls']
                for i, entry in enumerate(texture_urls):
                    for key, value in entry.items():
                        if value:
                            res = requests.get(value)
                            if res.status_code == REQUEST_OK:
                                filename = f'meshy_tttx_test_texture_{i}_{key}.png'
                                filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                                with open(filepath, 'wb') as f:
                                    f.write(res.content)
                                print(f'Saved as {filepath}')

    print(f"Elapsed time (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment is True


def test_meshy_text_to_voxel_instances(run_api):
    judgment = True
    master = LLMMaster()

    meshy_ttvx_test = master.pack_parameters(provider='meshy_ttvx',
                                             prompt=PROMPT,
                                             negative_prompt='ugly, low resolution')
    master.set_api_keys(API_KEY)
    master.summon({'meshy_ttvx_test': meshy_ttvx_test})

    print(f"Parameters = {master.instances['meshy_ttvx_test'].parameters}")

    if not isinstance(master.instances['meshy_ttvx_test'], MeshyTextToVoxel):
        judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        if not isinstance(master.results['meshy_ttvx_test'], Response):
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        else:
            json_result = master.results['meshy_ttvx_test'].json()
            print(f"json_result = {json_result}")
            for key, value in json_result['model_urls'].items():
                if value:
                    res = requests.get(value)
                    if res.status_code == REQUEST_OK:
                        filename = f'meshy_ttvx_test.{key}'
                        filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                        with open(filepath, 'wb') as f:
                            f.write(res.content)
                        print(f'Saved as {filepath}')

            if 'thumbnail_url' in json_result and json_result['thumbnail_url']:
                res = requests.get(json_result['thumbnail_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_ttvx_test_thumbnail.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

    print(f"Elapsed time (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment is True


def test_meshy_image_to_3d_instances(run_api):
    judgment = True
    master = LLMMaster()

    image_url='https://assets.st-note.com/img/1725449361-rjBEAFQSfC6oecXxh718RndG.png'

    meshy_it3d_test = master.pack_parameters(provider='meshy_it3d',
                                             image_url=image_url)
    master.set_api_keys(API_KEY)
    master.summon({'meshy_it3d_test': meshy_it3d_test})

    print(f"Parameters = {master.instances['meshy_it3d_test'].parameters}")

    if not isinstance(master.instances['meshy_it3d_test'], MeshyImageTo3D):
        judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        if not isinstance(master.results['meshy_it3d_test'], Response):
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        else:
            json_result = master.results['meshy_it3d_test'].json()
            print(f"json_result = {json_result}")
            for key, value in json_result['model_urls'].items():
                if value:
                    res = requests.get(value)
                    if res.status_code == REQUEST_OK:
                        filename = f'meshy_it3d_test.{key}'
                        filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                        with open(filepath, 'wb') as f:
                            f.write(res.content)
                        print(f'Saved as {filepath}')

            if 'thumbnail_url' in json_result and json_result['thumbnail_url']:
                res = requests.get(json_result['thumbnail_url'])
                if res.status_code == REQUEST_OK:
                    filename = f'meshy_it3d_test_thumbnail.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'texture_urls' in json_result:
                texture_urls = json_result['texture_urls']
                for i, entry in enumerate(texture_urls):
                    for key, value in entry.items():
                        if value:
                            res = requests.get(value)
                            if res.status_code == REQUEST_OK:
                                filename = f'meshy_it3d_test_texture_{i}_{key}.png'
                                filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                                with open(filepath, 'wb') as f:
                                    f.write(res.content)
                                print(f'Saved as {filepath}')

    print(f"Elapsed time (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment is True
