![llmmaster_logo_full](https://github.com/Habatakurikei/llmmaster/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

[![Downloads](https://static.pepy.tech/badge/llmmaster)](https://pepy.tech/project/llmmaster)
[![Downloads](https://static.pepy.tech/badge/llmmaster/month)](https://pepy.tech/project/llmmaster)
[![Downloads](https://static.pepy.tech/badge/llmmaster/week)](https://pepy.tech/project/llmmaster)

# LLM Master

LLM Master, L2M2 in short, is a powerful engine to boost your creativity by working with multiple generative AIs.

This is a Python library that provides a unified interface for interacting with multiple Large Language Models (LLMs) and multimedia generative AI models from different providers.

## Features

- Support for various models from each provider
- Concurrent execution of multiple LLMs and multimedia generative AI models
- Thread-based execution for improved performance
- Customizable generation parameters
  - Required parameters: `provider` and `prompt`
  - Optional parameters: `model` and particular parameters for different model
  - **Exception:** `prompt` is not required for some dedicated models. Follow the instructions released by provider.

## Supported LLM Providers and Models

LLM Master respects multi-modal approach. There are many generative AI models that can be used for different purposes.

There are 2 categories in LLM Master: major data formats and 3D models.

  1. **Major Data Formats**

The table below represents various conversion capabilities between different media types (text, image, audio/speech and video). Some conversions are available, some are pending or coming soon, and others are marked as not applicable (NA) at the moment.

Use highlighted word for `provider` to make `LLMMaster` instance.

| From \ To | Text | Image | Audio | Video |
|-----------|------|-------|-------|-------|
| Text | `anthropic`, `cerebras`, `google`, `groq`, `mistral`, `openai`, `perplexity` | `flux1_fal_tti`, `openai_tti`, `stable_diffusion_tti`, adobe_firefly_tti (pending) | `elevenlabs_tts`, `elevenlabs_ttse`, `openai_tts`, `voicevox_tts`, google_tta (pending) | `pikapikapika_ttv`, `lumaai_ttv` |
| Image | `google_itt`, `openai_itt` | `flux1_fal_iti`, `openai_iti`, `stable_diffusion_iti` | NA | `stable_diffusion_itv`, `lumaai_itv` |
| Audio | `google_stt`, `openai_stt` | NA | `elevenlabs_aiso` | NA |
| Video | `google_vtt` | NA | NA | `lumaai_vtv` |

And the list below represents the models that are supported by each provider. See each provider's documentation for full list.

### Text-to-Text Models (typical)
- Anthropic (`claude-3-haiku-20240307`)
- Cerebras (`llama3.1-8b`)
- Google (`gemini-1.5-flash`)
- Groq (`llama-3.1-8b-instant`)
- MistralAI (`mistral-small-latest`)
- OpenAI (`gpt-4o-mini`)
- Perplexity (`llama-3.1-sonar-small-128k-online`)

### Text-to-Image Models
- Flux.1 via fal (`fal-ai/flux/dev`)
- OpenAI (`dall-e-3`, `dall-e-2`)
- Stable Diffusion (`core`, `ultra`)
- Adobe Firely (pending deployment)

### Text-to-Audio (Speech) Models
- ElevenLabs Speech (`eleven_multilingual_v2`)
- ElevenLabs Sound Effect (`dummy`)
- OpenAI (`tts-1`, `tts-1-hd`)
- Voicevox (`dummy`)

### Text-to-Video Models
- Luma Dream Machine (`dummy`)
- Pika.art (`dummy`)

### Image-to-Text Models (typical)
- OpenAI (`gpt-4o`)
- Google (`gemini-1.5-flash`)

### Image-to-Image Models
- Flux.1 via fal (`fal-ai/flux/dev/image-to-image`)
- OpenAI (`dall-e-2`)
- Stable Diffusion (`v2beta`)

### Image-to-Video Models
- Stable Diffusion (`v2beta`)
- Luma Dream Machine (`dummy`)

### Audio-to-Audio Models
- ElevenLabs Audio Isolation (`dummy`)

### Audio(Speech)-to-Text Models (typical)
- OpenAI (`whisper-1`)
- Google (`gemini-1.5-flash`)

### Video-to-Text Models (typical)
- Google (`gemini-1.5-flash`)

### Video-to-Video Models
- Luma Dream Machine (`dummy`)

Use highlighted word for `model` to make `LLMMaster` instance.

The `model` parameter is optional. If you do not specify the model, the default model defined in `config.py` will be used.

**Important:** You need to install Voicevox engine separately for `voicevox_tts`. See [Voicevox](https://voicevox.hiroshiba.jp/) for details.

  2. **3D Models**

From ver. 0.2.2, LLM Master supports 3D models thanks to Meshy API. Here are the list of supported models:

  - MeshyTextToTexture: `meshy_tttx`
  - MeshyTextTo3D: `meshy_tt3d`
  - MeshyTextTo3DRefine: `meshy_tt3d_refine`
  - MeshyTextToVoxel: `meshy_ttvx`
  - MeshyImageTo3D: `meshy_it3d`

More models will be supported soon!

## Installation

To use LLM Master, you need to install the library. You can do this using pip:

```bash
pip install llmmaster
```

Relevant packages will also be installed.

## Usage

### Set API keys for your environment

Set up your API keys as environment variables. Note that you do not have to set all of the API keys as shown below. You can set only the ones that you need.

**Important**: changed `GEMINI_API_KEY` to `GOOGLE_API_KEY` since ver. 0.1.4.

For Mac/Linux,

```
export ANTHROPIC_API_KEY="your_anthropic_key"
export CEREBRAS_API_KEY="your_cerebras_key"
export GOOGLE_API_KEY="your_google_key"
export GROQ_API_KEY="your_groq_key"
export MISTRAL_API_KEY="your_mistral_key"
export OPENAI_API_KEY="your_openai_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
export MESHY_API_KEY="your_meshy_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"
export PIKAPIKAPIKA_API_KEY="your_pikapikapika_key"
export LUMAAI_API_KEY="your_lumaai_key"
export FAL_KEY="your_fal_key"
```

For Windows (cmd),

```
SET ANTHROPIC_API_KEY=your_anthropic_key
SET CEREBRAS_API_KEY=your_cerebras_key
SET GOOGLE_API_KEY=your_google_key
SET GROQ_API_KEY=your_groq_key
SET MISTRAL_API_KEY=your_mistral_key
SET OPENAI_API_KEY=your_openai_key
SET PERPLEXITY_API_KEY=your_perplexity_key
SET STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
SET MESHY_API_KEY=your_meshy_key
SET ELEVENLABS_API_KEY=your_elevenlabs_key
SET PIKAPIKAPIKA_API_KEY=your_pikapikapika_key
SET LUMAAI_API_KEY=your_lumaai_key
SET FAL_KEY=your_fal_key
```

For Windows (PowerShell)

```
$env:ANTHROPIC_API_KEY="your_anthropic_key"
$env:CEREBRAS_API_KEY="your_cerebras_key"
$env:GOOGLE_API_KEY="your_google_key"
$env:GROQ_API_KEY="your_groq_key"
$env:MISTRAL_API_KEY="your_mistral_key"
$env:OPENAI_API_KEY="your_openai_key"
$env:PERPLEXITY_API_KEY="your_perplexity_key"
$env:STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
$env:MESHY_API_KEY="your_meshy_key"
$env:ELEVENLABS_API_KEY="your_elevenlabs_key"
$env:PIKAPIKAPIKA_API_KEY="your_pikapikapika_key"
$env:LUMAAI_API_KEY="your_lumaai_key"
$env:FAL_KEY="your_fal_key"
```

### Set API keys prepared in text file

This is new since ver. 0.4.0. Your API keys are also set to LLMMaster from a saved text file, e.g. `api_key_pairs.txt`. The format shall be the following:

```
ANTHROPIC_API_KEY=your_anthropic_key
CEREBRAS_API_KEY=your_cerebras_key
GOOGLE_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key
MISTRAL_API_KEY=your_mistral_key
OPENAI_API_KEY=your_openai_key
PERPLEXITY_API_KEY=your_perplexity_key
STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
MESHY_API_KEY=your_meshy_key
ELEVENLABS_API_KEY=your_elevenlabs_key
PIKAPIKAPIKA_API_KEY=your_pikapikapika_key
LUMAAI_API_KEY=your_lumaai_key
```

Read the file in python script as string, then load to a `LLMMaster` instance. Explain in use cases.

This is useful for third-party application usage.

Note that `FAL_KEY` is only loaded from the OS environmental variable.

### Use cases

You can find and download these use case codes in folder [usecases](https://github.com/Habatakurikei/llmmaster/tree/main/usecases).

**Important:** How to handle or save generated contents? LLM Master basically returns raw output defined by each provider. Some models return REST API Response object from the requests library, while some other models return bytes object of media or specific class instance defined by provider. See [RESULTSTYPE.md](https://github.com/Habatakurikei/llmmaster/blob/main/RESULTSTYPE.md) for brief description of what type of object is returned.

  1. Using **single Text-to-Text** LLM

This is the most basic usage of LLM Master.

In the code below, `openai_instance` is actually a unique label to manage multiple instances. You may set any string for it.

This case uses an API key of OpenAI from enriroment variable.

```python
from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure LLM instance
llmmaster.summon({
    "openai_instance": llmmaster.pack_parameters(
        provider="openai",
        model="gpt-4o-mini",
        prompt="Hello, how are you?",
        max_tokens=100,
        temperature=0.7
    )
})

# Run LLM
print('Start running LLMMaster...')
llmmaster.run()

# Get results
results = llmmaster.results
print(f'OpenAI responded: {results["openai_instance"]}')

# Check elapsed time
print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
```

The following case is way of using API keys written in a text file instead of environment variable.

```python
from pathlib import Path
from llmmaster import LLMMaster

api_key_text = Path("api_key_pairs.txt").read_text(encoding="utf-8")

master = LLMMaster()

parameters = master.pack_parameters(provider="openai",
                                    prompt="Hello, how are you?")
master.set_api_keys(api_key_text)
print(f'API key pairs: {master.api_key_pairs}')

master.summon({"openai": parameters})
master.run()

results = master.results
print(f'OpenAI responded: {results["openai"]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  2 Using **multiple Text-to-Text** LLMs simultaneously

```python
from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure LLM instance
llmmaster.summon({
    "openai_instance": llmmaster.pack_parameters(
        provider="openai",
        prompt="Summarize the main ideas of quantum computing."
    ),
    "anthropic_instance": llmmaster.pack_parameters(
        provider="anthropic",
        prompt="Explain the concept of artificial general intelligence."
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in llmmaster.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
llmmaster.run()

# Get results
for instance, response in llmmaster.results.items():
    print(f'{instance} responded: {response}')

# Check elapsed time
print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
```

  3. Using **Text-to-Image** Models

```python
import requests
from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure LLM instance
llmmaster.summon({
    "openai_image": llmmaster.pack_parameters(
        provider="openai_tti",
        model="dall-e-3",
        prompt="A futuristic cityscape with flying cars and holographic billboards",
        size="1792x1024",
        quality="hd"
    ),
    "stable_diffusion_image": llmmaster.pack_parameters(
        provider="stable_diffusion_tti",
        model="core",
        prompt="A serene landscape with a mountain lake at sunset",
        aspect_ratio="16:9",
        style_preset="cinematic"
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in llmmaster.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
llmmaster.run()

# Get results
response = llmmaster.results["openai_image"]
if hasattr(response, 'data'):
    image_response = requests.get(response.data[0].url)
    if image_response.status_code == 200:
        with open("openai_image.png", 'wb') as f:
            f.write(image_response.content)
        print("openai_image.png saved")

response = llmmaster.results["stable_diffusion_image"]
if isinstance(response, bytes):
    with open("stable_diffusion_image.png", 'wb') as f:
        f.write(response)
    print("stable_diffusion_image.png saved")

# Check elapsed time
print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
```

  4. Using **Text-to-Audio** (Text-to-Speech) Models

4.1 OpenAI

```python
from llmmaster import LLMMaster
from llmmaster.config import OPENAI_TTS_VOICE_OPTIONS

master = LLMMaster()

to_say = "Do not concentrate on the finger, or you will miss all that heavenly glory."

# try to generate all the voice patterns for a same saying
entries = []
for voice_pattern in OPENAI_TTS_VOICE_OPTIONS:
    case = {'provider': 'openai_tts',
            'prompt': to_say,
            'voice': voice_pattern,
            'response_format': 'mp3'}
    entries.append({'name': f'openai_tts_{voice_pattern}', 'params': case})

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')
for name, response in master.results.items():
    save_as = f"{name}.mp3"
    with open(save_as, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    print(f'Saved as {save_as} for case {name}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

4.2 ElevenLabs

```python
import elevenlabs
from llmmaster import LLMMaster

master = LLMMaster()

to_say = "Do not concentrate on the finger, or you will miss all that heavenly glory."

test_case = master.pack_parameters(provider='elevenlabs_tts', prompt=to_say)

master.summon({'elevenlabs_tts': test_case})

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')
if master.results['elevenlabs_tts']:
    save_as = f"elevenlabs_tts.mp3"
    elevenlabs.save(master.results['elevenlabs_tts'], save_as)
    print(f'Saved as {save_as} for case {name}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  5. Using **Text-to-Video** Models

```python
import requests
from llmmaster import LLMMaster

# Create an instance of LLMMaster
master = LLMMaster()

# Configure LLM instance
prompt = 'A cute robot boy flying high to the space.'
camera = {'zoom': 'out'}
parameters = {"guidanceScale":16,"motion":2,"negativePrompt": "ugly"}

params = master.pack_parameters(provider='pikapikapika_ttv',
                                prompt=prompt,
                                style='Anime',
                                sfx=True,
                                frameRate=24,
                                aspectRatio='16:9',
                                camera=camera,
                                parameters=parameters)

master.summon({'pikapikapika_ttv': params})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')
response = master.results['pikapikapika_ttv'].json()

if 'resultUrl' in response['videos'][0] and response['videos'][0]:
    res = requests.get(response['videos'][0]['resultUrl'])
    if res.status_code == 200:
        filename = f'pikapikapika_ttv_test_video.mp4'
        with open(filepath, 'wb') as f:
            f.write(res.content)
            print(f'Saved as {filepath}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  6. Using **Image-to-Text** Models

```python
from llmmaster import LLMMaster

master = LLMMaster()

# Online images are preferred for OpenAI.
# Online images and local image paths are both supported for Google.
# Change "image_url" for your case
entries = [
    {
        'name': 'openai_itt_case',
        'params': {
            'provider': 'openai_itt',
            'model': 'gpt-4o',
            'prompt': 'Describe each image.',
            'image_url': ['https://example.com/image-1.jpg',
                          'https://example.com/image-2.jpg']
        }
    },
    {
        'name': 'google_itt_case',
        'params': {
            'provider': 'google_itt',
            'model': 'gemini-1.5-flash',
            'prompt': 'What might be differences between these pictures?',
            'image_url': ['https://example.com/image.png',
                          '/home/user/my_image.png']
        }
    }
]

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

print('Start running LLMMaster...')
master.run()

for entry, result in master.results.items():
    print(f'{entry} responded: {result}')

print(f'Elapsed time: {master.elapsed_time} seconds')

master.dismiss()
```

  7. Using **Image-to-Image** Models

```python
import requests
from llmmaster import LLMMaster

master = LLMMaster()

test_image = '/home/user/test_image.png'

entries = [
    {
        'name': 'openai',
        'params': {
            'provider': 'openai_iti',
            'mode': 'variations',
            'image': test_image,
            'n': 2
        }
    },
    {
        'name': 'stable_diffusion',
        'params': {
            'provider': 'stable_diffusion_iti',
            'mode': 'remove_background',
            'image': test_image,
        }
    }]

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

print('Start running LLMMaster...')
master.run()

print('Results')

# Get results
response = master.results["openai"]
if hasattr(response, 'data'):
    for i in range(len(response.data)):
        image_response = requests.get(response.data[i].url)
        if image_response.status_code == 200:
            filename = f"openai_{i+1:02}.png"
            with open(filename, 'wb') as f:
                f.write(image_response.content)
            print(f'Image No. {i+1:2} saved as {filename}')
        else:
            print(f'Image No. {i+1:2} failed to download')

response = master.results["stable_diffusion"]
if isinstance(response, bytes):
    with open("stable_diffusion_result.png", 'wb') as f:
        f.write(response)
    print("stable_diffusion_result.png saved")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  8. Using **Image-to-Video** Model

```python
from llmmaster import LLMMaster

master = LLMMaster()

# Set a path of local image file
# Change "image" for your case
entry = master.pack_parameters(
    provider='stable_diffusion_itv',
    image='/home/user/test-image.png')

master.summon({'sd_itv': entry})

print('Start running LLMMaster...')
master.run()

print('Results')
response = master.results["sd_itv"]
if isinstance(response, bytes):
    with open("sd_itv.mp4", 'wb') as f:
        f.write(response)
    print("sd_itv.mp4 saved")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  9. Using **Audio-to-Text** (Speech-to-Text) Models

```python
from llmmaster import LLMMaster

master = LLMMaster()

speech_file = '/home/user/sample-speech.mp3'

entries = [
    {
        'name': 'openai_stt_1',
        'params': {
            'provider': 'openai_stt',
            'mode': 'translations',
            'file': speech_file,
            'response_format': 'json',
            'temperature': 0.0
        }
    },
    {
        'name': 'openai_stt_2',
        'params': {
            'provider': 'openai_stt',
            'mode': 'transcriptions',
            'file': speech_file,
            'response_format': 'text'
        }
    },
    {
        'name': 'openai_stt_3',
        'params': {
            'provider': 'openai_stt',
            'mode': 'transcriptions',
            'file': speech_file,
            'response_format': 'verbose_json'
        }
    },
    {
        'name': 'google_stt',
        'params': {
            'provider': 'google_stt',
            'prompt': 'What does the speaker imply?',
            'audio_file': speech_file
        }
    }
]

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

print(f'Start running LLMMaster...')
master.run()

# Different type of response given by different
# `response_format`, `transcriptions` or `translations` mode
# Handle with care for output
print('Results')
for name, response in master.results.items():
    print(f'{name}: {response}')

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  10. Using **Video-to-Text** Model

```python
from llmmaster import LLMMaster

master = LLMMaster()

# Set a path of local video file
# Change "video_file" for your case
params = master.pack_parameters(
    provider='google_vtt',
    prompt='Describe attached video.',
    video_file='/home/user/sample-video.mp4')

master.summon({'video_to_text': params})

print('Start running LLMMaster...')
master.run()

print(f'Answer = {master.results["video_to_text"]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  11. Using **3D Models** (Meshy)

```python
import requests
from requests.models import Response
from llmmaster import LLMMaster

REQUEST_OK = 200
TEST_OUTPUT_PATH = 'test-outputs'

master = LLMMaster()

# This is a case of generating Voxel model from text prompt
params = master.pack_parameters(provider='meshy_ttvx',
                                prompt='A cute robot boy.',
                                negative_prompt='ugly, low resolution')

master.summon({'meshy_ttvx_test': params})

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')

if isinstance(master.results['meshy_ttvx_test'], Response):

    json_result = master.results['meshy_ttvx_test'].json()

    # Meshy returns several different model formats
    for key, value in json_result['model_urls'].items():
        if value:
            res = requests.get(value)
            if res.status_code == REQUEST_OK:
                filename = f'meshy_ttvx_test.{key}'
                filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                with open(filepath, 'wb') as f:
                    f.write(res.content)
                print(f'Saved as {filepath}')

    # Meshy also returns thumbnail png for preview
    if 'thumbnail_url' in json_result:
        res = requests.get(json_result['thumbnail_url'])
        if res.status_code == REQUEST_OK:
            filename = 'meshy_ttvx_test_thumbnail.png'
            filepath = os.path.join(TEST_OUTPUT_PATH, filename)
            with open(filepath, 'wb') as f:
                f.write(res.content)
            print(f'Saved as {filepath}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  12. Using **Video-to-Video** Model

```python
import requests
from llmmaster import LLMMaster

master = LLMMaster()

prompt = 'The boy exploring the space finds Mars.'

# Use generated video in Luma or public image in web.
# This is a case to extend video with generated frame.
keyframes={
    "frame0": {
    "type": "generation",
    "id": "uuid-generated-by-lumaai"
    }
}

params = master.pack_parameters(provider='lumaai_vtv',
                                prompt=prompt,
                                keyframes=keyframes)
master.set_api_keys(API_KEY)
master.summon({'lumaai_vtv': params})

print('Start running LLMMaster...')
master.run()

print('Results')
response = master.results["lumaai_vtv"]
res = requests.get(response['assets']['video'])
if res.status_code == 200:
    with open("lumaai_vtv.mp4", 'wb') as f:
        f.write(res.content)
    print("lumaai_vtv.mp4 saved")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

## Applications
- [Zoltraak Klein](https://github.com/Habatakurikei/zoltraakklein): [Zoltraak](https://github.com/dai-motoki/zoltraak) is a framework of digital content plant, generating texts/codes, images, speeches and videos. LLMMaster is core interface for external AI services.
- Multi-AI brainstorming web app monju [https://monju.ai](https://monju.ai). This app generates ideas from 3 different LLMs simultaneously, and then shows the result in mindmap.

## Notes

### General

- Please comply with the terms of service for each provider's API.
- Securely manage your API keys and be careful not to commit them to public repositories.
- Input parameters are not strictly checked by the rules defined by each provider. You may face an error due to some wrong paramer or combination of parameters.

### Initial arguments for LLMMaster

- There is a limit to the number of LLM instances that can be created at once. This limit is adjustable by one of the new arguments, `summon_limit`, default is 100.
- If you apply multiple model entries in a single LLMMaster instance, running simultaneously, each entry will start in a certain period of interval. This is a strict limitation of providers for security reason. The minimum interval should be 1 second but this value is adjustable with another argument `wait_for_starting`.

Both arguments shall be set in the following manner:

```python
from llmmaster import LLMMaster
master = LLMMaster(summon_limit=150, wait_for_starting=2.5)
```

## Customization

- You can easily adjust default models by updating the dictionary in `config.py` and creating a new thread class for the provider.
- You can also run an individual provider Model directly without using LLMMaster. See each class definition for details.

## Contributing

Contributions to LLM Master are welcome! Please feel free to submit a Pull Request and bug reports and feature requests through GitHub Issues.

## License

This project is licensed under the MIT License.

---

This project is under development. New features and support for additional providers may be added. Please check the repository for the latest information.
