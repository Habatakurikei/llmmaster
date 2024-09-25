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
- OpenAI (`dall-e-3`)
- Stable Diffusion (`core`)

### Text-to-Audio (Speech) Models
- ElevenLabs Speech (`eleven_multilingual_v2`)
- ElevenLabs Sound Effect (`dummy`)
- OpenAI (`tts-1`)
- Voicevox (`dummy`)

### Text-to-Video Models
- Luma Dream Machine (`dummy`)
- Pika.art (`dummy`)

### Image-to-Text Models
- OpenAI (`gpt-4o`)
- Google (`gemini-1.5-flash`)

### Image-to-Image Models
- Flux.1 via fal (`fal-ai/flux/dev/image-to-image`)
- OpenAI (`dall-e-2`)
- Stable Diffusion (`v2beta`)

### Image-to-Video Models
- Stable Diffusion (`v2beta`)
- Luma Dream Machine (`dummy`)

### Audio(Speech)-to-Text Models
- OpenAI (`whisper-1`)
- Google (`gemini-1.5-flash`)

### Audio-to-Audio Models
- ElevenLabs Audio Isolation (`dummy`)

### Video-to-Text Models (typical)
- Google (`gemini-1.5-flash`)

### Video-to-Video Models
- Luma Dream Machine (`dummy`)

Use highlighted word for `model` to make `LLMMaster` instance.

The `model` parameter is optional. If you do not specify the model, the default model defined in `config.py` will be used.

**Important:** You need to install Voicevox engine separately for `voicevox_tts`. See [Voicevox](https://voicevox.hiroshiba.jp/) for details.

  2. **3D Models**

From ver. 0.2.2, LLM Master supports 3D models thanks to Meshy API. Here are the list of supported functions defined as class:

- MeshyTextToTexture: `meshy_tttx`
- MeshyTextTo3D: `meshy_tt3d`
- MeshyTextTo3DRefine: `meshy_tt3d_refine`
- MeshyTextToVoxel: `meshy_ttvx`
- MeshyImageTo3D: `meshy_it3d`

From ver. 0.6.0, LLM Master also supports Tripo 3D modeling API. The following classes and provider keys are available:

- TripoTextTo3D: `tripo_tt3d`
- TripoImageTo3D: `tripo_it3d`
- TripoMultiviewTo3D: `tripo_mv3d`
- TripoRefineModel: `tripo_refine`
- TripoAnimationPreRigCheck: `tripo_aprc`
- TripoAnimationRig: `tripo_arig`
- TripoAnimationRetarget: `tripo_aretarget`
- TripoStylization: `tripo_stylize`
- TripoConversion: `tripo_conversion`

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
export DALLE_API_KEY="your_openai_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"
export FAL_KEY="your_fal_key"
export GOOGLE_API_KEY="your_google_key"
export GROQ_API_KEY="your_groq_key"
export LUMAAI_API_KEY="your_lumaai_key"
export MESHY_API_KEY="your_meshy_key"
export MISTRAL_API_KEY="your_mistral_key"
export OPENAI_API_KEY="your_openai_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export PIKAPIKAPIKA_API_KEY="your_pikapikapika_key"
export STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
export TRIPO_API_KEY="your_tripo_key"
```

For Windows (cmd),

```
SET ANTHROPIC_API_KEY=your_anthropic_key
SET CEREBRAS_API_KEY=your_cerebras_key
SET DALLE_API_KEY=your_openai_key
SET ELEVENLABS_API_KEY=your_elevenlabs_key
SET FAL_KEY=your_fal_key
SET GOOGLE_API_KEY=your_google_key
SET GROQ_API_KEY=your_groq_key
SET LUMAAI_API_KEY=your_lumaai_key
SET MESHY_API_KEY=your_meshy_key
SET MISTRAL_API_KEY=your_mistral_key
SET OPENAI_API_KEY=your_openai_key
SET PERPLEXITY_API_KEY=your_perplexity_key
SET PIKAPIKAPIKA_API_KEY=your_pikapikapika_key
SET STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
SET TRIPO_API_KEY=your_tripo_key
```

For Windows (PowerShell)

```
$env:ANTHROPIC_API_KEY="your_anthropic_key"
$env:CEREBRAS_API_KEY="your_cerebras_key"
$env:DALLE_API_KEY="your_openai_key"
$env:ELEVENLABS_API_KEY="your_elevenlabs_key"
$env:FAL_KEY="your_fal_key"
$env:GOOGLE_API_KEY="your_google_key"
$env:GROQ_API_KEY="your_groq_key"
$env:LUMAAI_API_KEY="your_lumaai_key"
$env:MESHY_API_KEY="your_meshy_key"
$env:MISTRAL_API_KEY="your_mistral_key"
$env:OPENAI_API_KEY="your_openai_key"
$env:PERPLEXITY_API_KEY="your_perplexity_key"
$env:PIKAPIKAPIKA_API_KEY="your_pikapikapika_key"
$env:STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
$env:TRIPO_API_KEY="your_tripo_key"
```

### Set API keys prepared in text file

This is new since ver. 0.4.0. Your API keys are also set to LLMMaster from a saved text file, e.g. `api_key_pairs.txt`. The format shall be the following:

```
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key
PERPLEXITY_API_KEY=your_perplexity_key
STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
MESHY_API_KEY=your_meshy_key
ELEVENLABS_API_KEY=your_elevenlabs_key
LUMAAI_API_KEY=your_lumaai_key
```

You do not have to set all the API keys but include ones you want to use.

Read this text file in python script as string, then load through through `LLMMaster.set_api_keys()`. Explain details in use cases.

This is useful for third-party application usage.

Note that `FAL_KEY` is only loaded from the OS environmental variable according to the official API reference.

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
master = LLMMaster()

# Configure LLM instance
master.summon({
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
master.run()

# Get results
results = master.results
print(f'OpenAI responded: {results["openai_instance"]}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
```

The following case is way of using API keys written in a text file instead of environment variable.

```python
from pathlib import Path
from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")

master = LLMMaster()
master.set_api_keys(api_key_pairs)
print(f'API key pairs: {master.api_key_pairs}')

parameters = master.pack_parameters(provider="openai",
                                    prompt="Hello, how are you?")

master.summon({"openai": parameters})
master.run()

results = master.results
print(f'OpenAI responded: {results["openai"]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  2 Using **multiple Text-to-Text** LLMs simultaneously

```python
from pathlib import Path
from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")

# Create an instance of LLMMaster
master = LLMMaster()
master.set_api_keys(api_key_pairs)
print(f'API key pairs: {master.api_key_pairs}')

# Configure LLM instance
master.summon({
    "openai_instance": master.pack_parameters(
        provider="openai",
        prompt="Summarize the main ideas of quantum computing."
    ),
    "anthropic_instance": master.pack_parameters(
        provider="anthropic",
        prompt="Explain the concept of artificial general intelligence."
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
for instance, response in master.results.items():
    print(f'{instance} responded: {response}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
```

  3. Using **Text-to-Image** Models

```python
import requests
from llmmaster import LLMMaster

# Create an instance of LLMMaster
master = LLMMaster()

# Configure instances
master.summon({
    "openai_image": master.pack_parameters(
        provider="openai_tti",
        model="dall-e-3",
        prompt="A futuristic cityscape with flying cars in the clear sky",
        size="1792x1024",
        quality="hd"
    ),
    "stable_diffusion_image": master.pack_parameters(
        provider="stable_diffusion_tti",
        model="core",
        prompt="A serene landscape with a mountain lake at sunset",
        aspect_ratio="16:9",
        style_preset="cinematic"
    ),
    "flux1_fal_image": master.pack_parameters(
        provider="flux1_fal_tti",
        model="fal-ai/flux/schnell",
        prompt="A spaceship heading to Mars in the space",
        image_size="landscape_16_9",
        num_inference_steps=4
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run master
print('Start running LLMMaster...')
master.run()

# Get results
response = master.results["openai_image"]
if 'data' in response:
    image_response = requests.get(response['data'][0]['url'])
    if image_response.status_code == 200:
        with open("openai_image.png", 'wb') as f:
            f.write(image_response.content)
        print("openai_image.png saved")

response = master.results["stable_diffusion_image"]
if hasattr(response, 'content'):
    with open("stable_diffusion_image.png", 'wb') as f:
        f.write(response.content)
    print("stable_diffusion_image.png saved")

response = master.results["flux1_fal_image"]
if 'images' in response:
    image_response = requests.get(response['images'][0]['url'])
    if image_response.status_code == 200:
        with open("flux1_fal_image.png", 'wb') as f:
            f.write(image_response.content)
    print("flux1_fal_image.png saved")

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
```

  4. Using **Text-to-Audio** (Speech/Sound) Models

```python
import elevenlabs
from llmmaster import LLMMaster

to_say = "Hello World!"

master = LLMMaster()

# Configure instances
master.summon({
    "openai": master.pack_parameters(
        provider='openai_tts',
        prompt=to_say,
        voice='echo',
        speed=0.5,
        response_format='mp3'
    ),
    "elevenlabs_speech": master.pack_parameters(
        provider='elevenlabs_tts',
        prompt=to_say
    ),
    "elevenlabs_sound": master.pack_parameters(
        provider='elevenlabs_ttse',
        prompt='Drinking a glass of water.'
    ),
    "voicevox": master.pack_parameters(
        provider='voicevox_tts',
        prompt=to_say,
        speaker=0
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run master
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')

response = master.results['openai']
if response:
    save_as = "openai.mp3"
    with open(save_as, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    print(f'Saved as {save_as}')

if master.results['elevenlabs_speech']:
    save_as = "elevenlabs_speech.mp3"
    elevenlabs.save(master.results['elevenlabs_speech'], save_as)
    print(f'Saved as {save_as}')

if master.results['elevenlabs_sound']:
    save_as = "elevenlabs_sound.mp3"
    elevenlabs.save(master.results['elevenlabs_sound'], save_as)
    print(f'Saved as {save_as}')

response = master.results['voicevox']
if response.content:
    save_as = "voicevox.wav"
    with open(save_as, 'wb') as f:
        f.write(response.content)
    print(f'Saved as {save_as}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  5. Using **Text-to-Video** Models

```python
import requests
from llmmaster import LLMMaster

master = LLMMaster()

prompt = 'Japanese ladies in elegant kimono dancing in traditional tea room.'

pika_parameters = {
    "guidanceScale": 16,
    "motion": 2,
    "negativePrompt": "ugly"
}

# Configure instances
master.summon({
    "pikapikapika_ttv": master.pack_parameters(
        provider='pikapikapika_ttv',
        prompt=prompt,
        style='Anime',
        sfx=True,
        frameRate=24,
        aspectRatio='16:9',
        camera={'zoom': 'out'},
        parameters=pika_parameters
    ),
    "lumaai_ttv": master.pack_parameters(
        provider='lumaai_ttv',
        prompt=prompt,
        aspect_ratio='16:9',
        loop=True
    )
})

print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

print('Start running LLMMaster...')
master.run()

print('Responses')

response = master.results['pikapikapika_ttv']
if 'videos' in response:
    res = requests.get(response['videos'][0]['resultUrl'])
    if res.status_code == 200:
        save_as = "pikapikapika_ttv.mp4"
        with open(save_as, "wb") as f:
            f.write(res.content)
        print(f'Saved as {save_as}')

response = master.results['lumaai_ttv']
if 'assets' in response:
    res = requests.get(response['assets']['video'])
    if res.status_code == 200:
        save_as = "lumaai_ttv.mp4"
        with open(save_as, "wb") as f:
            f.write(res.content)
        print(f'Saved as {save_as}')

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

local_image = '/home/user/test_image.png'
image_url = 'https://example.com/image-1.jpg'

master = LLMMaster()
master.summon({
    "openai": master.pack_parameters(
        provider="openai_iti",
        mode='variations',
        image=local_image,
        n=1
    ),
    "stable_diffusion": master.pack_parameters(
        provider='stable_diffusion_iti',
        mode='remove_background',
        image=local_image,
    ),
    "flux1_fal": master.pack_parameters(
        provider="flux1_fal_iti",
        strength=0.95,
        image_url=image_url,
        prompt='Make smiling',
        image_size='landscape_16_9'
    )
})

print('Start running LLMMaster...')
master.run()

print('Results')

response = master.results["openai"]
if 'data' in response:
    image_response = requests.get(response['data'][0]['url'])
    if image_response.status_code == 200:
        with open("openai_iti.png", 'wb') as f:
            f.write(image_response.content)

response = master.results["stable_diffusion"]
if hasattr(response, 'content'):
    with open("stable_diffusion_iti.png", 'wb') as f:
        f.write(response.content)

response = master.results["flux1_fal"]
if 'images' in response:
    image_response = requests.get(response['images'][0]['url'])
    if image_response.status_code == 200:
        with open("flux1_fal_iti.png", 'wb') as f:
            f.write(image_response.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  8. Using **Image-to-Video** Model

```python
import requests
from llmmaster import LLMMaster

local_image = '/home/user/test_image.png'
image_url = 'https://example.com/image-1.jpg'

master = LLMMaster()
master.summon({
    "stable_diffusion": master.pack_parameters(
        provider='stable_diffusion_itv',
        image=local_image
    ),
    "lumaai": master.pack_parameters(
        provider='lumaai_itv',
        prompt='Make smiling',
        frame0=image_url
    )
})

print('Start running LLMMaster...')
master.run()

print('Results')

response = master.results["stable_diffusion"]
if hasattr(response, 'content'):
    with open("stable_diffusion_itv.mp4", 'wb') as f:
        f.write(response.content)

response = master.results["lumaai"]
if 'assets' in response:
    res = requests.get(response['assets']['video'])
    if res.status_code == 200:
        with open("lumaai_itv.mp4", "wb") as f:
            f.write(res.content)

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

print('Start running LLMMaster...')
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

  10. Using **Audio-to-Audio** Model

```python
# this function works to remove sound noise from source
import elevenlabs
from llmmaster import LLMMaster

audio_file = '/home/user/test_audio.m4a'
key = "elevenlabs_aiso"

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        audio=audio_file
    )
})

print('Start running LLMMaster...')
master.run()

print('Result')
if master.results[key]:
    save_as = f"{key}.mp3"
    elevenlabs.save(master.results[key], save_as)
    print(f'Saved as {save_as}')

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  11. Using **Video-to-Text** Model

```python
from llmmaster import LLMMaster

video_file = '/home/user/sample-video.mp4'
key = 'google_vtt'

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        prompt='Describe attached video.',
        video_file=video_file
    )
})

print('Start running LLMMaster...')
master.run()

print(f'Response = {master.results[key]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  12. Using **Video-to-Video** Model

```python
import requests
from llmmaster import LLMMaster

task_id = 'uuid-generated-by-lumaai'

master = LLMMaster()

# Use generated video in Luma or public image in web.
# This is a case to extend video with generated frame.
key = 'lumaai_vtv'
params = master.pack_parameters(
    provider=key,
    prompt='The boy exploring the space finds Mars.',
    keyframes={
        "frame0": {
            "type": "generation",
            "id": task_id
        }
    }
)

master.summon({key: params})
master.run()

response = master.results[key]
if 'assets' in response:
    res = requests.get(response['assets']['video'])
    if res.status_code == 200:
        with open(f"{key}.mp4", "wb") as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  13. Using **3D Models** (Meshy)

```python
import requests
from llmmaster import LLMMaster

key = 'meshy_tt3d'
negative_prompt = 'ugly, low resolution'
prompt = 'A cute robot boy.'

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        prompt=prompt,
        negative_prompt=negative_prompt
    )
})

print('Run master')
master.run()

print('Responses')
response = master.results[key]

# Meshy returns several different model formats
for format, url in response['model_urls'].items():
    if url:
        res = requests.get(url)
        if res.status_code == 200:
            with open(f"{key}.{format}", 'wb') as f:
                f.write(res.content)

# Meshy also returns thumbnail png for preview
if 'thumbnail_url' in response:
    res = requests.get(response['thumbnail_url'])
    if res.status_code == 200:
        with open(f"{key}.png", 'wb') as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  14. Using **3D Models** (Tripo)

```python
import requests
from llmmaster import LLMMaster

key = 'tripo_tt3d'
negative_prompt = 'ugly, low resolution'
prompt = 'A cute robot boy.'

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        prompt=prompt,
        negative_prompt=negative_prompt
    )
})

print('Run master')
master.run()

print('Responses')
response = master.results[key]

if 'data' in response:
    # Download model
    ext = response['data']['result']['model']['type']
    res = requests.get(response['data']['result']['model']['url'])
    if res.status_code == 200:
        with open(f"{key}.{ext}", "wb") as f:
            f.write(res.content)

    # Download model
    ext = response['data']['result']['rendered_image']['type']
    res = requests.get(response['data']['result']['rendered_image']['url'])
    if res.status_code == 200:
        with open(f"{key}.{ext}", "wb") as f:
            f.write(res.content)

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
