import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.config import DEFAULT_TOKENS
from llmmaster.text_to_text_models import AnthropicLLM
from llmmaster.text_to_text_models import GoogleLLM
from llmmaster.text_to_text_models import GroqLLM
from llmmaster.text_to_text_models import OpenAILLM
from llmmaster.text_to_text_models import PerplexityLLM
from llmmaster import LLMMaster


INSTANCE_CLASSES = {
    'anthropic': AnthropicLLM,
    'google': GoogleLLM,
    'groq': GroqLLM,
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


def test_instance_limit():
    master = LLMMaster()
    i = 1
    with pytest.raises(Exception) as e:
        while True:
            entry = master.pack_parameters(provider='openai', prompt='Hello.')
            master.summon({f'entry_{i:02d}': entry})
            i += 1
    assert 'limit' in str(e.value)


def test_ttt_instances(run_api):
    judgment = True
    master = LLMMaster()

    test_cases = [
        {'name': 'case_1', 'params': {'provider': 'openai', 'prompt': 'Hello.'}},
        {'name': 'case_2', 'params': {'provider': 'anthropic', 'prompt': 'Hello.', 'max_tokens': 0, 'temperature': -0.1}},
        {'name': 'case_3', 'params': {'provider': 'google', 'prompt': 'Hello.', 'max_tokens': 5000, 'temperature': 1.1}},
        {'name': 'case_4', 'params': {'provider': 'groq', 'prompt': 'Hello.', 'max_tokens': 100, 'temperature': 0.5}},
        {'name': 'case_5', 'params': {'provider': 'perplexity', 'prompt': 'Hello.', 'temperature': 0.0}},
        {'name': 'case_6', 'params': {'provider': 'openai', 'model': 'gpt-4o-mini', 'prompt': 'Hello.', 'max_tokens': 10000}}
    ]

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
