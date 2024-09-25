import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import elevenlabs
import pytest
from requests.models import Response

from llmmaster import LLMMaster


TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture(scope="session", autouse=True)
def setup_api_client():
    pass


def pytest_addoption(parser):
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Run tests that make actual API calls"
    )


def verify_instance(instance, expected_class):
    answer = True
    print(f"Parameters = {instance.parameters}")
    print(f"API Key = {instance.api_key}")
    answer = False if not isinstance(instance, expected_class) else True
    return answer


def execute_llmmaster(master: LLMMaster):
    '''
    This function is used for dict output with text content.
    Raise exception for unexpected outputs.
    '''
    print('Execute LLMMaster')

    try:
        master.run()
    except Exception as e:
        msg = f"An error occurred during API calls: {str(e)}"
        raise Exception(msg)

    print('Responses')

    for key, result in master.results.items():
        if isinstance(result, dict):
            print(f"Result for {key} = {json.dumps(result, indent=2)}")
            write_json(save_as=f'{key}.json', output=result)
        else:
            msg = f"Failed to generate in {key}: {result}"
            raise Exception(msg)

    print(f"Elapsed time in total (sec): {master.elapsed_time}")


def write_json(save_as: str, output: dict):

    if not os.path.isdir(TEST_OUTPUT_PATH):
        os.makedirs(TEST_OUTPUT_PATH)

    filepath = os.path.join(TEST_OUTPUT_PATH, save_as)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'Saved as {filepath}')


def run_llmmaster(master: LLMMaster):
    '''
    This function is used for text output.
    Print output anyway.
    '''
    print('Run LLMMaster')

    try:
        master.run()
    except Exception as e:
        msg = f"An error occurred during API calls: {str(e)}"
        raise Exception(msg)

    print('Responses')

    for key, result in master.results.items():
        if isinstance(result, dict):
            print(f"Result for {key} = {json.dumps(result, indent=2)}")
            write_json(save_as=f'{key}.json', output=result)
        else:
            print(f"Result for {key}, type ({type(result)}) = {result}")

    print(f"Elapsed time in total (sec): {master.elapsed_time}")


def execute_elevenlabs(master: LLMMaster):
    '''
    This function is used for ElevenLabs.
    '''
    print('Run API for ElevenLabs')

    try:
        master.run()
    except Exception as e:
        pytest.fail(f"An error occurred during API calls: {str(e)}")

    print('Responses')

    for key, result in master.results.items():
        if isinstance(result, str):
            msg = f"Failed to generate in {key}: {result}"
            raise Exception(msg)
        else:
            filepath = os.path.join(TEST_OUTPUT_PATH, f'{key}.mp3')
            elevenlabs.save(result, filepath)
            print(f'Saved as {filepath} for {key}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")


def execute_restapi(master: LLMMaster, format: str):
    '''
    This function is used for general REST API.
    Save response data in json and binary format.
    '''
    print('Run API for REST API')

    try:
        master.run()
    except Exception as e:
        pytest.fail(f"An error occurred during API calls: {str(e)}")

    print('Responses')

    for name, response in master.results.items():
        if isinstance(response, Response):
            save_response(response, key=name, format=format)
        else:
            msg = f"Failed to generate in {name}: {response}"
            raise Exception(msg)

    print(f"Elapsed time in total (sec): {master.elapsed_time}")


def save_response(response: Response,
                  key: str = '',
                  format: str = ''):
    '''
    Save response data of REST API in json and binary format.
    Arguments:
      - response: object returned from requests get/post
      - key: base file name for json and binary
      - format: extension, e.g. jpg, png, wav, mp4
    Remarks:
      - response.connection not implemented
      - response.raw not implemented
    '''
    response_dict = {
        'status_code': response.status_code,
        'headers': dict(response.headers),
        'url': response.url,
        'encoding': response.encoding,
        'reason': response.reason,
        'elapsed': str(response.elapsed),
        'cookies': {k: v for k, v in response.cookies.items()},
        'history': [
            {
                'url': r.url,
                'status_code': r.status_code,
                'reason': r.reason
            } for r in response.history
        ],
        'request': {
            'method': response.request.method,
            'url': response.request.url,
            'headers': dict(response.request.headers),
        }
    }

    # response.request.body
    buff = response.request.body
    if isinstance(buff, bytes):
        response_dict['request']['body'] = "Binary data output."
    elif isinstance(buff, str):
        response_dict['request']['body'] = buff
    else:
        response_dict['request']['body'] = None

    # response.text
    if ('text' in response.headers['Content-Type'] or
       'xml' in response.headers['Content-Type']):
        response_dict['text'] = response.text
    else:
        response_dict['text'] = "Non-text content output."

    # handle response.content based on its type
    if hasattr(response, 'content') and isinstance(response.content, bytes):
        save_as = os.path.join(TEST_OUTPUT_PATH, f'{key}.{format}')
        with open(save_as, 'wb') as f:
            f.write(response.content)
        msg = f"Binary content saved to {save_as}"
        response_dict['content'] = msg
        print(msg)

    # save to JSON file
    save_as = os.path.join(TEST_OUTPUT_PATH, f"{key}.json")
    with open(save_as, 'w', encoding='utf-8') as f:
        json.dump(response_dict, f, indent=4, ensure_ascii=False)
    print(f'Response information saved to {save_as}')
