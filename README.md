![llm_master_logo_full](https://github.com/Habatakurikei/llm_master/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

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
  - Mandatory parameters: `provider` and `prompt`
  - Optional parameters: `model` and particular parameters for different model
- Thread-based execution for improved performance

## Installation

To use LLM Master, you need to install the required dependencies. You can do this using pip:

```
pip install anthropic google-generativeai groq openai
```

## Usage

1. Set up your API keys as environment variables:

   ```
   export ANTHROPIC_API_KEY="your_anthropic_key"
   export GEMINI_API_KEY="your_gemini_key"
   export GROQ_API_KEY="your_groq_key"
   export OPENAI_API_KEY="your_openai_key"
   export PERPLEXITY_API_KEY="your_perplexity_key"
   ```

2. Use cases

  * Using single LLM

```python
from llm_master import LLMMaster

# Create an instance of LLMMaster
llm_master = LLMMaster()

# Configure LLM instance
llm_master.summon({
    "openai_instance": llm_master.pack_parameters(
        provider="openai",
        model="gpt-4o",
        prompt="Hello, what's the weather like today?",
        max_tokens=100,
        temperature=0.7
    )
})

# Run LLM
llm_master.run()

# Get results
results = llm_master.results
print(results["openai_instance"])

# Clear instances
llm_master.dismiss()
```

  * Using multiple LLMs simultaneously

```python
llm_master.summon({
    "openai_instance": llm_master.pack_parameters(
        provider="openai",
        prompt="Summarize the main ideas of quantum computing."
    ),
    "anthropic_instance": llm_master.pack_parameters(
        provider="anthropic",
        prompt="Explain the concept of artificial general intelligence."
    )
})

llm_master.run()

results = llm_master.results
print(results["openai_instance"])
print(results["anthropic_instance"])
```

## Notes

- Please comply with the terms of service for each provider's API.
- Securely manage your API keys and be careful not to commit them to public repositories.
- There is a limit (32) to the number of LLM instances that can be created at once.

## Customization

- You can easily adjust default models by updating the dictionary in `config.py` and creating a new thread class for the provider.
- You can also run an individual provider LLM without using LLMMaster but each defined class.

## Contributing

Contributions to LLM Master are welcome! Please feel free to submit a Pull Request and bug reports and feature requests through GitHub Issues.

## License

This project is licensed under the MIT License.

---

This project is under development. New features and support for additional providers may be added. Please check the repository for the latest information.
