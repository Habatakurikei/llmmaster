![llmmaster_logo_full](https://github.com/Habatakurikei/llmmaster/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

# LLM Master

LLM Master is a Python library that provides a unified interface for interacting with multiple Large Language Models (LLMs) from different providers. It supports concurrent execution of multiple LLMs and easy management of API keys and model configurations.

## Features

- Concurrent execution of multiple LLMs
- Support for various models from each provider
- Customizable generation parameters
  - Required parameters: `provider` and `prompt`
  - Optional parameters: `model` and particular parameters for different model
- Thread-based execution for improved performance

## Supported LLM Providers and Models

LLMMaster respects multi-modal approach. 

The table below represents various conversion capabilities between different media types (text, image, audio, video). Some conversions are available, some are pending or coming soon, and others are marked as not applicable (NA) at the moment.

Use highlighted word for `provider` to make LLMMaster instance.

| From \ To | Text | Image | Audio | Video |
|-----------|------|-------|-------|-------|
| Text | `openai`, `anthropic`, `google`, `groq`, `perplexity` | `openai_tti`, `stable_diffusion_tti`, adobe_firefly_tti (pending) | google_tta (soon) | (pending) |
| Image | `openai_itt`, `google_itt` | openai_iti (soon), stable_diffusion_iti (soon) | NA | NA |
| Audio | openai_att (soon) | NA | NA | NA |
| Video | google_vtt (pending) | NA | NA | NA |

And the list below represents the models that are supported by each provider. See each provider's documentation for full list.

Use highlighted word for `model` to make LLMMaster instance. The `model` parameter is optional. If you do not specify the model, the default model will be used.

### Text-to-Text Models (typical)
- Anthropic (`claude-3-5-sonnet-20240620`)
- Google (`gemini-1.5-flash`)
- Groq (`llama3-70b-8192`)
- OpenAI (`gpt-4o`)
- Perplexity (`llama-3-sonar-large-32k-online`)

### Text-to-Image Models
- OpenAI (`dall-e-3`, `dall-e-2`)
- Stable Diffusion (`core`, `ultra`)

### Image-to-Text Models (typical)
- OpenAI (`gpt-4o`)
- Google (`gemini-1.5-flash`)

More models will be covered soon!

## Installation

To use LLM Master, you need to install the library. You can do this using pip:

```bash
pip install llmmaster
```

Relevant packages will also be installed.

## Usage

1. Set up your API keys as environment variables. Note that you do not have to set all of the API keys. You can set only the ones that you need.

For Mac/Linux,

```
export ANTHROPIC_API_KEY="your_anthropic_key"
export GEMINI_API_KEY="your_gemini_key"
export GROQ_API_KEY="your_groq_key"
export OPENAI_API_KEY="your_openai_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export STABLE_DIFFUSION_API_KEY="your_stable_diffusion_key"
```

For Windows,

```
SET ANTHROPIC_API_KEY=your_anthropic_key
SET GEMINI_API_KEY=your_gemini_key
SET GROQ_API_KEY=your_groq_key
SET OPENAI_API_KEY=your_openai_key
SET PERPLEXITY_API_KEY=your_perplexity_key
SET STABLE_DIFFUSION_API_KEY=your_stable_diffusion_key
```

2. Use cases

  * Using single Text-to-Text LLM

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

  * Using multiple Text-to-Text LLMs simultaneously

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

  * Using Text-to-Image Models

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

  * Using Image-to-Text Models

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

## Notes

- Please comply with the terms of service for each provider's API.
- Securely manage your API keys and be careful not to commit them to public repositories.
- There is a limit (32) to the number of LLM instances that can be created at once.
- Input parameters are not strictly checked by the rules defined by each provider. You may face an error due to some wrong paramer or combination of parameters.

## Customization

- You can easily adjust default models by updating the dictionary in `config.py` and creating a new thread class for the provider.
- You can also run an individual provider LLM without using LLMMaster but each defined class.

## Contributing

Contributions to LLM Master are welcome! Please feel free to submit a Pull Request and bug reports and feature requests through GitHub Issues.

## License

This project is licensed under the MIT License.

---

This project is under development. New features and support for additional providers may be added. Please check the repository for the latest information.
