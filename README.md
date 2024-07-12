![llmmaster_logo_full](https://github.com/Habatakurikei/llmmaster/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

# LLM Master

LLM Master is a Python library that provides a unified interface for interacting with multiple Large Language Models (LLMs) from different providers. It supports concurrent execution of multiple LLMs and easy management of API keys and model configurations.

## Supported LLM Providers

### Text-to-Text Models
- Anthropic (Claude)
- Google (Gemini)
- Groq
- OpenAI (GPT)
- Perplexity

### Text-to-Image Models
- OpenAI (Dall-E)
- Stable Diffusion (comming soon)

Text-to-Speech models and more models will be covered!

## Features

- Concurrent execution of multiple LLMs
- Easy configuration of API keys through environment variables
- Support for various models from each provider
- Customizable generation parameters
  - Required parameters: `provider` and `prompt`
  - Optional parameters: `model` and particular parameters for different model
- Thread-based execution for improved performance

## Installation

To use LLM Master, you need to install the library. You can do this using pip:

```
pip install llmmaster
```

Relevant packages will also be installed.

## Usage

1. Set up your API keys as environment variables:

For Mac/Linux,

   ```
   export ANTHROPIC_API_KEY="your_anthropic_key"
   export GEMINI_API_KEY="your_gemini_key"
   export GROQ_API_KEY="your_groq_key"
   export OPENAI_API_KEY="your_openai_key"
   export PERPLEXITY_API_KEY="your_perplexity_key"
   ```

For Windows,

   ```
   SET ANTHROPIC_API_KEY=your_anthropic_key
   SET GEMINI_API_KEY=your_gemini_key
   SET GROQ_API_KEY=your_groq_key
   SET OPENAI_API_KEY=your_openai_key
   SET PERPLEXITY_API_KEY=your_perplexity_key
   ```

2. Use cases

  * Using single LLM

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

  * Using multiple LLMs simultaneously

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
