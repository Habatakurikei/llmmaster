import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.config import DEFAULT_TOKENS
from llmmaster.text_to_text_models import AnthropicLLM
from llmmaster.text_to_text_models import CerebrasLLM
from llmmaster.text_to_text_models import GoogleLLM
from llmmaster.text_to_text_models import GroqLLM
from llmmaster.text_to_text_models import MistralLLM
from llmmaster.text_to_text_models import OpenAILLM
from llmmaster.text_to_text_models import PerplexityLLM
from llmmaster import LLMMaster


API_KEY = '''
'''


INSTANCE_CLASSES = {
    'anthropic': AnthropicLLM,
    'cerebras': CerebrasLLM,
    'google': GoogleLLM,
    'groq': GroqLLM,
    'mistral': MistralLLM,
    'openai': OpenAILLM,
    'perplexity': PerplexityLLM
}


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_label_empty():
    master = LLMMaster()
    entry = master.pack_parameters(provider='openai', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'': entry})
    assert 'Error' in str(e.value)


def test_label_number():
    master = LLMMaster()
    entry = master.pack_parameters(provider='openai', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({1: entry})
    assert 'Error' in str(e.value)


def test_provider_lacking():
    master = LLMMaster()
    entry = master.pack_parameters(prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_provider_empty():
    master = LLMMaster()
    entry = master.pack_parameters(provider='', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_provider_wrong():
    master = LLMMaster()
    entry = master.pack_parameters(provider='amazon', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_prompt_lacking():
    master = LLMMaster()
    entry = master.pack_parameters(provider='openai')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_prompt_empty():
    master = LLMMaster()
    entry = master.pack_parameters(provider='openai', prompt='')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_preset_api_key():
    '''
    2024-09-03: test for one-time api key.
    '''
    judgment = False
    master = LLMMaster()
    entry = master.pack_parameters(provider='openai', prompt='Hello.')
    # master.set_api_keys(API_KEY)
    master.summon({'test': entry})
    if isinstance(master.instances['test'], OpenAILLM):
        judgment = True
        print(f"parameters = {master.instances['test'].parameters}")
        print(f"api_key_pairs = {master.api_key_pairs}")
        print(f"api_key = {master.instances['test'].api_key}")
    master.dismiss()
    assert judgment is True


def test_instance_limit():
    '''
    Fail if api key is not set in the environment variable.
    '''
    master = LLMMaster()
    i = 1
    with pytest.raises(Exception) as e:
        while True:
            entry = master.pack_parameters(provider='openai', prompt='Hello.')
            master.summon({f'entry_{i:02d}': entry})
            i += 1
    assert 'limit' in str(e.value)


def test_ttt_instances(run_api):
    '''
    Fail if api key is not set in the environment variable.
    '''
    judgment = True
    master = LLMMaster()

    test_cases = [
        {'name': 'case_1', 'params': {'provider': 'openai', 'model': 'gpt-4o-mini', 'prompt': 'Hello.', 'max_tokens': 10000}},
        {'name': 'case_2', 'params': {'provider': 'anthropic', 'model': 'claude-3-haiku-20240307', 'prompt': 'Hello.', 'max_tokens': 0, 'temperature': -0.1, 'top_p': 0.1, 'top_k': 0}},
        {'name': 'case_3', 'params': {'provider': 'google', 'model': 'gemini-1.5-flash', 'prompt': 'Hello.', 'max_tokens': 5000, 'temperature': 1.1, 'top_p': 0.7, 'top_k': 30}},
        {'name': 'case_4', 'params': {'provider': 'groq', 'model': 'mixtral-8x7b-32768', 'prompt': 'Hello.', 'max_tokens': 100, 'temperature': 0.5, 'top_p': 0.5}},
        {'name': 'case_5', 'params': {'provider': 'perplexity', 'model': 'llama-3.1-sonar-small-128k-online', 'prompt': 'Hello.', 'temperature': 0.0}},
        {'name': 'case_6', 'params': {'provider': 'cerebras', 'model': 'llama3.1-8b', 'prompt': 'Hello.', 'max_tokens': 4096, 'temperature': 0.2, 'top_p': 0.2}},
        {'name': 'case_7', 'params': {'provider': 'mistral', 'model': 'mistral-small-latest', 'prompt': 'Hello.', 'max_tokens': 2000, 'temperature': 0.4, 'top_p': 0.3}}
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, tuple(INSTANCE_CLASSES.values())):
            judgment = False

    if run_api:
        # add --run-api option for making actual API calls test, paying API credit
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        print('Responses')
        for name, response in master.results.items():
            print(f'{name} = {response}')
            if not response:
                judgment = False

    print(f'Elapsed Time (sec) = {master.elapsed_time}')
    master.dismiss()

    assert judgment is True
