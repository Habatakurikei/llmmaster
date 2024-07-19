![llmmaster_logo_full](https://github.com/Habatakurikei/llmmaster/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

# LLM Master

LLM Master is a Python library that provides a unified interface for interacting with multiple Large Language Models (LLMs) from different providers. It supports concurrent execution of multiple LLMs and easy model configurations.

## Features

- Concurrent execution of multiple LLMs
- Support for various models from each provider
- Customizable generation parameters
  - Required parameters: `provider` and `prompt`
  - Optional parameters: `model` and particular parameters for different model
  - Exception: `prompt` is not required for Audio-to-Text Models and some modes of Image-to-Image Models.
- Thread-based execution for improved performance

## Supported LLM Providers and Models

LLMMaster respects multi-modal approach. 

The table below represents various conversion capabilities between different media types (text, image, audio, video). Some conversions are available, some are pending or coming soon, and others are marked as not applicable (NA) at the moment.

Use highlighted word for `provider` to make LLMMaster instance.

| From \ To | Text | Image | Audio | Video |
|-----------|------|-------|-------|-------|
| Text | `openai`, `anthropic`, `google`, `groq`, `perplexity` | `openai_tti`, `stable_diffusion_tti`, adobe_firefly_tti (pending) | `openai_tta`, google_tta (pending) | (pending) |
| Image | `openai_itt`, `google_itt` | `openai_iti`, `stable_diffusion_iti` | NA | stable_diffusion_itv (pending) |
| Audio | `openai_att` | NA | NA | NA |
| Video | `google_vtt` | NA | NA | NA |

And the list below represents the models that are supported by each provider. See each provider's documentation for full list.

Use highlighted word for `model` to make LLMMaster instance. The `model` parameter is optional. If you do not specify the model, the default model defined in `config.py` will be used.

### Text-to-Text Models (typical)
- Anthropic (`claude-3-5-sonnet-20240620`)
- Google (`gemini-1.5-flash`)
- Groq (`llama3-70b-8192`)
- OpenAI (`gpt-4o`)
- Perplexity (`llama-3-sonar-large-32k-online`)

### Text-to-Image Models
- OpenAI (`dall-e-3`, `dall-e-2`)
- Stable Diffusion (`core`, `ultra`)
- Adobe Firely (pending deployment)

### Text-to-Audio (Speech) Models
- OpenAI (`tts-1`, `tts-1-hd`)

### Image-to-Text Models (typical)
- OpenAI (`gpt-4o`)
- Google (`gemini-1.5-flash`)

### Image-to-Image Models
- OpenAI (`dall-e-2`)
- Stable Diffusion (`v2beta`)

### Video-to-Text Models (typical)
- Google (`gemini-1.5-flash`)

### Audio-to-Text Models
- OpenAI (`whisper-1`)

More models will be covered soon!

## Installation

To use LLM Master, you need to install the library. You can do this using pip:

```bash
pip install llmmaster
```

Relevant packages will also be installed.

## Usage

### Set API keys for your environment in advance

Set up your API keys as environment variables. Note that you do not have to set all of the API keys. You can set only the ones that you need.

**Important**: changed `GEMINI_API_KEY` to `GOOGLE_API_KEY` since ver. 0.1.4.

For Mac/Linux,

```
export ANTHROPIC_API_KEY="your_anthropic_key"
export GOOGLE_API_KEY="your_google_key"
export GROQ_API_KEY="your_groq_key"
export OPENAI_API_KEY="your_openai_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
```

For Windows,

```
SET ANTHROPIC_API_KEY=your_anthropic_key
SET GOOGLE_API_KEY=your_google_key
SET GROQ_API_KEY=your_groq_key
SET OPENAI_API_KEY=your_openai_key
SET PERPLEXITY_API_KEY=your_perplexity_key
SET STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
```

### Use cases

  1. Using **single Text-to-Text** LLM

This is the most basic usage of LLM Master. `openai_instance` is actually a unique label to manage multiple instances in case. You may set any string for it.

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
# print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
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
# print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

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
# print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
```

  4. Using **Text-to-Audio** Models

```python
from llmmaster import LLMMaster
from llmmaster.config import OPENAI_TTS_VOICE_OPTIONS

master = LLMMaster()

to_say = "Do not concentrate on the finger, or you will miss all that heavenly glory."

# try to generate all the voice patterns for a same saying
# capable for various audio formats: mp3, opus, aac, flac, wav and pcm
entries = []
for voice_pattern in OPENAI_TTS_VOICE_OPTIONS:
    case = {'provider': 'openai_tts', 'prompt': to_say, 'voice': voice_pattern, 'response_format': 'mp3'}
    entries.append({'name': f'openai_case_{voice_pattern}', 'params': case})

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in llmmaster.instances.items():
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
    print(f'Saved as {save_as} for {name}')

# Check elapsed time
# print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

master.dismiss()
```

  5. Using **Image-to-Text** Models

```python
from llmmaster import LLMMaster

master = LLMMaster()

# Online image URLs and local image paths are supported for Google.
# Online images are preferred for OpenAI.
inputs = [
    {
        'name': 'openai_itt_example',
        'params': {
            'provider': 'openai_itt',
            'model': 'gpt-4o',
            'prompt': 'Describe this image.',
            'image_url': ['https://example.com/image.jpg']
        }
    },
    {
        'name': 'google_itt_example',
        'params': {
            'provider': 'google_itt',
            'model': 'gemini-1.5-flash',
            'prompt': 'What might be differences between these pictures?',
            'image_url': ['https://example.com/image.png',
                          '/home/user/my_image.png']
        }
    }
]

for case in inputs:
    master.summon({case['name']: master.pack_parameters(**case['params'])})

print('Start running LLMMaster...')
master.run()

print(f'Results: {master.results}')

# print(f'Elapsed time: {master.elapsed_time} seconds')

master.dismiss()
```

  6. Using **Image-to-Image** Models

```python
from llmmaster import LLMMaster

master = LLMMaster()

inputs = [
    {
        'name': 'openai',
        'params': {
            'provider': 'openai_iti',
            'mode': 'variations',
            'image': '/home/user/test_image.png',
            'n': 2
        }
    },
    {
        'name': 'stable_diffusion',
        'params': {
            'provider': 'stable_diffusion_iti',
            'mode': 'remove_background',
            'file': '/home/user/test_image.png',
        }
    }]

for case in inputs:
    master.summon({case['name']: master.pack_parameters(**case['params'])})

print('Start running LLMMaster...')
master.run()

print('Results')
for name, response in master.results.items():
    print(f'{name}: {response}')

# print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  7. Using **Audio-to-Text** Models

```python
from llmmaster import LLMMaster

master = LLMMaster()

inputs = [
    {
        'name': 'openai_att_case_1',
        'params': {
            'provider': 'openai_att',
            'mode': 'translations',
            'file': '/home/user/test_speech.mp3',
            'response_format': 'json',
            'temperature': 0.0
        }
    },
    {
        'name': 'openai_att_case_2',
        'params': {
            'provider': 'openai_att',
            'mode': 'transcriptions',
            'file': '/home/user/test_speech.mp3',
            'response_format': 'text'
        }
    },
    {
        'name': 'openai_att_case_3',
        'params': {
            'provider': 'openai_att',
            'mode': 'transcriptions',
            'file': '/home/user/test_speech.mp3',
            'response_format': 'verbose_json'
        }
    }
]

for case in inputs:
    master.summon({case['name']: master.pack_parameters(**case['params'])})

master.run()

# different type of response given by different `response_format`
# also different by `transcriptions` or `translations
# handle with care
print('Results')
for name, response in master.results.items():
    print(f'{name}: {response}')

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

  8. Using **Video-to-Text** Model

```python
from llmmaster import LLMMaster

master = LLMMaster()

params = master.pack_parameters(
    provider='google_vtt',
    prompt='Describe attached video.',
    video_file='/home/user/sample-video.mp4')

master.summon({'video_to_text': params})
master.run()

print(f'Answer = {master.results["video_to_text"]}')
# print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

## Applications
- Multi-AI brainstorming web app monju [https://monju.ai](https://monju.ai). This app generates ideas from 3 different LLMs simultaneously, and then shows the result in a mindmap.

## Notes

- Please comply with the terms of service for each provider's API.
- Securely manage your API keys and be careful not to commit them to public repositories.
- There is a limit (32) to the number of LLM instances that can be created at once.
- Input parameters are not strictly checked by the rules defined by each provider. You may face an error due to some wrong paramer or combination of parameters.

## Customization

- You can easily adjust default models by updating the dictionary in `config.py` and creating a new thread class for the provider.
- You can also run an individual provider Model directly without using LLMMaster. See each class definition for details.

## Contributing

Contributions to LLM Master are welcome! Please feel free to submit a Pull Request and bug reports and feature requests through GitHub Issues.

## License

This project is licensed under the MIT License.

---

This project is under development. New features and support for additional providers may be added. Please check the repository for the latest information.
