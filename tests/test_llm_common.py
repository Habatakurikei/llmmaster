import pytest

from conftest import load_api_keys
from llmmaster import LLMMaster


def test_label_empty():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(provider='perplexity', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'': entry})
    assert 'Error' in str(e.value)


def test_label_number():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(provider='perplexity', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({1: entry})
    assert 'Error' in str(e.value)


def test_provider_lacking():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_provider_empty():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(provider='', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_provider_wrong():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(provider='amazon', prompt='Hello.')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_prompt_lacking():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(provider='perplexity')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_prompt_empty():
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    entry = master.pack_parameters(provider='perplexity', prompt='')
    with pytest.raises(Exception) as e:
        master.summon({'test': entry})
    assert 'Error' in str(e.value)


def test_instance_limit():
    '''
    Fail if api key is not set in the environment variable.
    '''
    master = LLMMaster()
    master.set_api_keys(load_api_keys())
    i = 1
    with pytest.raises(Exception) as e:
        while True:
            entry = master.pack_parameters(provider='perplexity',
                                           prompt='Hello.')
            master.summon({f'entry_{i:02d}': entry})
            i += 1
    assert 'limit' in str(e.value)
