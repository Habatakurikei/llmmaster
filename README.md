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

## Supported LLM Providers and Models

LLM Master respects multi-modal approach. There are many generative AI models that can be used for different purposes.

There are 3 categories in LLM Master: major data formats, 3D models, and panorama models.

More models will be supported soon!

### Major Data Formats

The table below represents various conversion capabilities between different media types (text, image, audio/speech and video). Some conversions are available, some are pending or coming soon, and others are marked as not applicable (NA) at the moment.

Use highlighted word for parameter `provider` to make `LLMMaster` instance.

| From \ To | Text | Image | Audio | Video |
|-----------|------|-------|-------|-------|
| Text | `anthropic`, `cerebras`, `deepseek`, `google`, `groq`, `mistral`, `mistral_fim`, `openai`, `perplexity`, `sambanova`, `xai` | `flux1_fal_tti`, `lumaai_tti`, `openai_tti`, `stable_diffusion_tti`, adobe_firefly_tti (pending) | `elevenlabs_tts`, `elevenlabs_ttse`, `elevenlabs_voicedesign`, `openai` (audio output), `openai_tts`, `voicevox_tts` | `lumaai_ttv` |
| Image | `anthropic`, `google`, `groq`, `mistral`, `openai`, `sambanova`, `xai` | `flux1_fal_iti`, `lumaai_iti`, `openai_iti`, `stable_diffusion_iti` | NA | `lumaai_itv`, `runway_itv`, `stable_diffusion_itv` |
| Audio | `google_stt`, `groq_stt`, `openai` (audio input), `openai_stt` | NA | `elevenlabs_aiso`, `elevenlabs_voicechange`, | NA |
| Video | `google_vtt` | NA | NA | `lumaai_vtv` |

**Important:**
  - You need to install Voicevox engine separately for `voicevox_tts`. See [Voicevox](https://voicevox.hiroshiba.jp/) for details.
  - `pikapikapika_ttv` was deprecated and removed at v1.0.0.

### 3D Models

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
- TripoTextureModel: `tripo_texture`
- TripoRefineModel: `tripo_refine`
- TripoAnimationPreRigCheck: `tripo_aprc`
- TripoAnimationRig: `tripo_arig`
- TripoAnimationRetarget: `tripo_aretarget`
- TripoStylization: `tripo_stylize`
- TripoConversion: `tripo_conversion`

From ver. 1.0.0, LLMMaster also supports Stable Diffusion 3D modeling API.

- Stable Fast 3D (SF3D) and Stable Point Aware 3D (SPAR) : `stable_diffusion_it3d`

### Panorama Models

Are you not satisfied with just generating images and 3D models? From ver. 0.8.0, LLM Master supports Skybox API that generates 360-degree panoramic images and videos.

The following classes and provider keys are available:

- SkyboxTextToPanorama: `skybox_ttp`
- SkyboxPanoramaToImageVideo: `skybox_ptiv` (export function)

## Installation

To use LLM Master, you need to install the library. You can do this using pip:

```bash
pip install llmmaster
```

Relevant packages will also be installed.

## Set API keys before use

Most of the API services are paid, meaning LLM Master can be used by the subscribers of these providers. Prepare your own API keys in advance.

LLM Master provides 2 way to set your API keys to access the services.

### Set as environmental variables

This is common to use the API if to run over your local computer. Use the commands below for your OS.

Note that you do not have to set all of the API keys as shown below. You can set only the ones that you need.

**Important**: changed `GEMINI_API_KEY` to `GOOGLE_API_KEY` since ver. 0.1.4.

For Mac/Linux,

```
export ANTHROPIC_API_KEY="your_API_key"
export CEREBRAS_API_KEY="your_API_key"
export DALLE_API_KEY="your_API_key"
export DEEPSEEK_API_KEY="your_API_key"
export ELEVENLABS_API_KEY="your_API_key"
export FAL_KEY="your_API_key"
export GOOGLE_API_KEY="your_API_key"
export GROQ_API_KEY="your_API_key"
export LUMAAI_API_KEY="your_API_key"
export MESHY_API_KEY="your_API_key"
export MISTRAL_API_KEY="your_API_key"
export OPENAI_API_KEY="your_API_key"
export PERPLEXITY_API_KEY="your_API_key"
export PIKAPIKAPIKA_API_KEY="your_API_key"
export RUNWAY_API_KEY="your_API_key"
export SAMBANOVA_API_KEY="your_API_key"
export SKYBOX_API_KEY="your_API_key"
export STABLE_DIFFUSION_API_KEY="your_API_key"
export TRIPO_API_KEY="your_API_key"
export XAI_API_KEY="your_API_key"
```

For Windows (cmd),

```
SET ANTHROPIC_API_KEY="your_API_key"
SET CEREBRAS_API_KEY="your_API_key"
SET DALLE_API_KEY="your_API_key"
SET DEEPSEEK_API_KEY="your_API_key"
SET ELEVENLABS_API_KEY="your_API_key"
SET FAL_KEY="your_API_key"
SET GOOGLE_API_KEY="your_API_key"
SET GROQ_API_KEY="your_API_key"
SET LUMAAI_API_KEY="your_API_key"
SET MESHY_API_KEY="your_API_key"
SET MISTRAL_API_KEY="your_API_key"
SET OPENAI_API_KEY="your_API_key"
SET PERPLEXITY_API_KEY="your_API_key"
SET PIKAPIKAPIKA_API_KEY="your_API_key"
SET RUNWAY_API_KEY="your_API_key"
SET SAMBANOVA_API_KEY="your_API_key"
SET SKYBOX_API_KEY="your_API_key"
SET STABLE_DIFFUSION_API_KEY="your_API_key"
SET TRIPO_API_KEY="your_API_key"
SET XAI_API_KEY="your_API_key"
```

For Windows (PowerShell)

```
$env:ANTHROPIC_API_KEY="your_API_key"
$env:CEREBRAS_API_KEY="your_API_key"
$env:DALLE_API_KEY="your_API_key"
$env:DEEPSEEK_API_KEY="your_API_key"
$env:ELEVENLABS_API_KEY="your_API_key"
$env:FAL_KEY="your_API_key"
$env:GOOGLE_API_KEY="your_API_key"
$env:GROQ_API_KEY="your_API_key"
$env:LUMAAI_API_KEY="your_API_key"
$env:MESHY_API_KEY="your_API_key"
$env:MISTRAL_API_KEY="your_API_key"
$env:OPENAI_API_KEY="your_API_key"
$env:PERPLEXITY_API_KEY="your_API_key"
$env:PIKAPIKAPIKA_API_KEY="your_API_key"
$env:RUNWAY_API_KEY="your_API_key"
$env:SAMBANOVA_API_KEY="your_API_key"
$env:SKYBOX_API_KEY="your_API_key"
$env:STABLE_DIFFUSION_API_KEY="your_API_key"
$env:TRIPO_API_KEY="your_API_key"
$env:XAI_API_KEY="your_API_key"
```

### Load API keys prepared in text file

This is new since ver. 0.4.0. Your API keys are also set to `LLMMaster` from a saved text file, e.g. `api_key_pairs.txt`. The format shall be the following:

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

## Use cases

You can find and download all the use case codes in folder [usecases](https://github.com/Habatakurikei/llmmaster/tree/main/usecases). Most of the basic use cases generating texts, images, videos, audio and 3D models are covered.

In another folder [tests](https://github.com/Habatakurikei/llmmaster/tree/main/tests), you will also find much more detailed usage for each provider.

In this document, some typical cases are introduced.

### Using single Text-to-Text LLM

This is the most basic usage of LLM Master.

In the code below, `openai_instance` is actually a unique label to manage multiple instances. You may set any string for it.

This case uses an API key of OpenAI from enriroment variable.

```python
import json

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

# Create an instance of LLMMaster
key = "openai_instance"
master = LLMMaster()

# Configure LLM instance
master.summon(
    {
        key: master.pack_parameters(
            provider="openai",
            model="gpt-4o-mini",
            prompt="Hello, how are you?",
            max_tokens=100,
            temperature=0.7
        )
    }
)

# Run LLM
print("Start running LLMMaster...")
master.run()

# Show results
result_text = extract_llm_response(master.results[key])
print(f"Response: {result_text}")

# Save results to a JSON file
save_as = "results.json"
with open(save_as, "w", encoding="utf-8") as f:
    json.dump(master.results[key], f, indent=4, ensure_ascii=False)
print(f"Results saved to {save_as}")

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instance
master.dismiss()
```

The following case is way of using API keys written in a text file instead of environment variable.

```python
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
key = "openai"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
print(f"API key pairs (print for debug purpose): {master.api_key_pairs}")

master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            prompt="Hello, how are you?"
        )
    }
)
master.run()

print(f"Response: {extract_llm_response(master.results[key])}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

**Important**: Since v1.0.0, output is `str`, `dict` or raw response of `requests`. See section "Handling generated contents" for details.

LLM outputs also contain multiple items in JSON format. You can utilize an original response or extract the text part. A text response can be extracted by importing a utility function. Declare `from llmmaster.utils import extract_llm_response` and use `extract_llm_response()`.

### Multiple Text-to-Text LLMs run simultaneously

One of the advantages of using LLM Master is to run multiple models at once. This is another example that uses 10 different providers through a single call.

```python
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "Who are you?"
provider_list = [
    "anthropic", "cerebras", "deepseek", "google", "groq", "mistral",
    "openai", "perplexity", "sambanova", "xai"
]

# Create an instance of LLMMaster
master = LLMMaster()
master.set_api_keys(api_key_pairs)

# Configure LLM instance
for provider in provider_list:
    master.summon(
        {
            provider: master.pack_parameters(
                provider=provider,
                prompt=prompt
            )
        }
    )

# You can check what parameters are set before run
print("Parameters (print for debug purpose).")
for label, instance in master.instances.items():
    print(f"{label} = {instance.parameters}")

# Run LLM
print("Start running LLMMaster...")
master.run()

# Get results
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
```

### Reasoning and Web Search Models

Since API calls have become more and more versatile and complicated, LLM Master faced errors in some new functionality. The library needed to be re-developed from scratch.

From v1.0.0, LLM Master can also handle the reasoning (thinking) models and web search capability. Here is an example.

```python
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "What will happen in the technological singularity?"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "openai_o1": master.pack_parameters(
            provider="openai",
            model="o1",
            prompt=prompt,
            reasoning_effort="high",
        ),
        "google_search": master.pack_parameters(
            provider="google",
            model="gemini-1.5-flash",
            prompt=prompt,
            dynamic_threshold=0.0
        ),
        "perplexity_reasoning": master.pack_parameters(
            provider="perplexity",
            model="sonar-reasoning",
            prompt=prompt
        ),
        "deepseek_reasoner": master.pack_parameters(
            provider="deepseek",
            model="deepseek-reasoner",
            prompt=prompt
        )
    }
)
master.run()

print("Responses.")
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

### Audio input and output (OpenAI)

OpenAI provides audio input and output. This is different from speech-to-text and text-to-speech. The users can communicate with AI using not text but voice.

LLMMaster is not capable of real-time API but possible for file-based voice communication with the OpenAI models.

The code below is a use case of audio input.

```python
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response
from llmmaster.utils import openai_audio_prompt

key = "openai"
api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
audio_prompt = openai_audio_prompt(
    prompt="What does he want to say?",
    audio_path="./audio_input.wav"
)

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            model="gpt-4o-audio-preview",
            prompt=audio_prompt
        )
    }
)
master.run()

print(f"Response: {extract_llm_response(master.results[key])}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

Another example on audio output.

```python
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import decode_base64

key = "openai"
api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            model="gpt-4o-audio-preview",
            prompt="Hi, how are you?",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
        )
    }
)
master.run()

print("Save output audio.")
decode_base64(
    master.results[key]["choices"][0]["message"]["audio"]["data"],
    save_as="./audio_output.wav",
)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

### Vision input for LLMs

It is not well-known that many providers support image-to-text process, i.e. the vision input LLM. A concern is different providers define different input format of image and prompt.

With support of utility functions in LLM Master, the vision input function is a good option to support your activity.

```python
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response
from llmmaster.utils import anthropic_vision_prompt
from llmmaster.utils import google_vision_prompt
from llmmaster.utils import xai_vision_prompt
from llmmaster.utils import groq_vision_prompt
from llmmaster.utils import mistral_vision_prompt
from llmmaster.utils import openai_vision_prompt
from llmmaster.utils import sambanova_vision_prompt

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "What is this image about?"
local_image = ["./test_image.png"]
web_image = ["https://www.example.com/images/test.png"]

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "anthropic": master.pack_parameters(
            provider="anthropic",
            prompt=anthropic_vision_prompt(prompt, local_image),
        ),
        "google": master.pack_parameters(
            provider="google",
            prompt=google_vision_prompt(prompt, local_image),
        ),
        "xai": master.pack_parameters(
            provider="xai",
            prompt=xai_vision_prompt(prompt, local_image),
            model="grok-2-vision-latest"
        ),
        "groq": master.pack_parameters(
            provider="groq",
            prompt=groq_vision_prompt(prompt, local_image),
            model="llama-3.2-11b-vision-preview"
        ),
        "mistral": master.pack_parameters(
            provider="mistral",
            prompt=mistral_vision_prompt(prompt, local_image),
            model="pixtral-12b-2409"
        ),
        "openai": master.pack_parameters(
            provider="openai",
            prompt=openai_vision_prompt(prompt, web_image)
        ),
        "sambanova": master.pack_parameters(
            provider="sambanova",
            prompt=sambanova_vision_prompt(prompt, local_image),
            model="Llama-3.2-11B-Vision-Instruct"
        )
    }
)
master.run()

print("Results")
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
```

## Handling generated contents

How to handle or save generated contents? LLM Master basically returns raw output defined by each provider. Some models return REST API Response object from the requests library, while some other models return bytes object or base 64 encoded characters of media.

See [RESULTSTYPE.md](https://github.com/Habatakurikei/llmmaster/blob/main/RESULTSTYPE.md) for brief description of what type of object is returned.

## Applications
- [Zoltraak Klein](https://github.com/Habatakurikei/zoltraakklein): [Zoltraak](https://github.com/dai-motoki/zoltraak) is a framework of digital content plant, generating texts/codes, images, speeches and videos. LLMMaster is core interface for external AI services.
- Multi-AI brainstorming web app monju [https://monju.ai](https://monju.ai). This app generates ideas from 3 different LLMs simultaneously, and then shows the result in mindmap.

## Notes

### General

- Please comply with the terms of service for each provider's API.
- Securely manage your API keys and be careful not to commit them to public repositories.
- Input parameters are not strictly checked by the rules defined by each provider. You may face an error due to some wrong paramer or combination of parameters.

### Initial arguments for LLMMaster

- There is a limit to the number of LLM instances that can be created at once. This limit is adjustable by one of the new arguments, `summon_limit`, default is 150. This value must be a positive integer.
- If you apply multiple model entries in a single `LLMMaster` instance, running simultaneously, each entry will start in a certain period of interval. This is a strict limitation of providers for security reason. The minimum interval should be 1 second but this value is adjustable with another argument `wait_for_starting`. This value shall be a positive float suitable for `time.sleep()`.

Both arguments shall be set in the following manner:

```python
from llmmaster import LLMMaster
master = LLMMaster(summon_limit=150, wait_for_starting=2.5)
```

## Contributing

Contributions to LLM Master are welcome! Please feel free to submit a Pull Request and bug reports and feature requests through GitHub Issues.

## License

This project is licensed under the MIT License.

---

This project is under development. New features and support for additional providers may be added. Please check the repository for the latest information.
