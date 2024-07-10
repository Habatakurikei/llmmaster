import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llm_master'))

import pytest

from llm_master import LLMMaster


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


def test_ttt_parameters():
    master = LLMMaster()
    judgment = True
    to_summon = {}

    buff = master.pack_parameters(provider='openai', prompt='Hello.')
    to_summon.update(case_1=buff)

    buff = master.pack_parameters(
        provider='anthropic', prompt='Hello.', max_tokens=0, temperature=-0.1)
    to_summon.update(case_2=buff)

    buff = master.pack_parameters(
        provider='google', prompt='Hello.', max_tokens=4097, temperature=1.1)
    to_summon.update(case_3=buff)

    buff = master.pack_parameters(
        provider='groq', prompt='Hello.', max_tokens=100, temperature=0.5)
    to_summon.update(case_4=buff)

    buff = master.pack_parameters(
        provider='perplexity', prompt='Hello.', temperature=0.0)
    to_summon.update(case_5=buff)

    master.summon(to_summon)
    master.run()

    for _, value in master.results.items():
        if not value:
            judgment = False

    assert judgment is True

# def test_ttt_models():
#     master = LLMMaster()
#     providers_list = ['openai', 'anthropic', 'google', 'groq', 'perplexity']
#     judgment = True
#
#     to_summon = {}
#     for i, entry in enumerate(providers_list):
#         params = master.pack_parameters(provider=entry, prompt='Hello!')
#         buff = {f"label_{i:02d}": params}
#         to_summon.update(buff)
#
#     master.summon(to_summon)
#     master.run()
#
#     for _, value in master.results.items():
#         if not value:
#             judgment = False
#
#     assert judgment is True


# def test_tti_models():
#     master = LLMMaster()
#     providers_list = ['openai_tti']
#     prompt = 'An anime girl saying Hello.'
#     judgment = True
#
#     to_summon = {}
#     for i, entry in enumerate(providers_list):
#         params = master.pack_parameters(provider=entry, prompt=prompt)
#         buff = {f"label_{i:02d}": params}
#         to_summon.update(buff)
#
#     master.summon(to_summon)
#     master.run()
#
#     for _, value in master.results.items():
#         if not value:
#             judgment = False
#
#     assert judgment is True
