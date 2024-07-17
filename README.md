![llmmaster_logo_full](https://github.com/Habatakurikei/llmmaster/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

# LLM Master

LLM Master is a Python library that provides a unified interface for interacting with multiple Large Language Models (LLMs) from different providers. It supports concurrent execution of multiple LLMs and easy model configurations.

## Features

- Concurrent execution of multiple LLMs
- Support for various models from each provider
- Customizable generation parameters
  - Required parameters: `provider` and `prompt`
  - Optional parameters: `model` and particular parameters for different model
  - Exception: `prompt` is not required for Audio-to-Text Models.
- Thread-based execution for improved performance

## Supported LLM Providers and Models

LLMMaster respects multi-modal approach. 

The table below represents various conversion capabilities between different media types (text, image, audio, video). Some conversions are available, some are pending or coming soon, and others are marked as not applicable (NA) at the moment.

Use highlighted word for `provider` to make LLMMaster instance.

| From \ To | Text | Image | Audio | Video |
|-----------|------|-------|-------|-------|
| Text | `openai`, `anthropic`, `google`, `groq`, `perplexity` | `openai_tti`, `stable_diffusion_tti`, adobe_firefly_tti (pending) | openai_tta, google_tta (soon) | (pending) |
| Image | `openai_itt`, `google_itt` | openai_iti (soon), stable_diffusion_iti (soon) | NA | NA |
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

### Image-to-Text Models (typical)
- OpenAI (`gpt-4o`)
- Google (`gemini-1.5-flash`)

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
        model="gpt-4o",
        prompt="Hello, what's the weather like today?",
        max_tokens=100,
        temperature=0.7
    )
})

# Run LLM
llmmaster.run()

# Get results
results = llmmaster.results
print(results["openai_instance"])

# Clear instances
llmmaster.dismiss()
```

  2 Using **multiple Text-to-Text** LLMs simultaneously

```python
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

llmmaster.run()

results = llmmaster.results
print(results["openai_instance"])
print(results["anthropic_instance"])
```

  3. Using **Text-to-Image** Models

```python
from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure image generation instance
llmmaster.summon({
    "openai_image": llmmaster.pack_parameters(
        provider="openai_tti",
        model="dall-e-3",
        prompt="A futuristic cityscape with flying cars and holographic billboards",
        size="1024x1024",
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

# Run image generation
llmmaster.run()

# Get results
results = llmmaster.results

# The result is given as a URL for OpenAI.
print("OpenAI DALL-E 3 image URL:", results["openai_image"])

# The result is given as a binary data for Stable Diffusion.
if isinstance(results["stable_diffusion_image"], bytes):
    with open("stable_diffusion_image.png", 'wb') as f:
        f.write(results["stable_diffusion_image"])
        print("stable_diffusion_image.png saved")

# Clear instances
llmmaster.dismiss()
```

  4. Using **Image-to-Text** Models

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

master.run()

print(f'Results: {master.results}')
```

  5. Using **Video-to-Text** Model

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
```

  6. Using **Audio-to-Text** Models

```python
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
```

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
