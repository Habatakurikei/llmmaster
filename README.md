![llm_master_logo_full](https://github.com/Habatakurikei/llm_master/assets/131997581/35bc6932-def9-4595-a2b3-2c122fb4e61e)

# LLM Master

LLM Master is a Python library that provides a unified interface for interacting with multiple Large Language Models (LLMs) from different providers. It supports concurrent execution of multiple LLMs and easy management of API keys and model configurations.

## Supported LLM Providers

- Anthropic (Claude)
- Google (Gemini)
- Groq
- OpenAI (GPT)
- Perplexity

## Features

- Concurrent execution of multiple LLMs
- Easy configuration of API keys through environment variables
- Support for various models from each provider
- Customizable generation parameters (max tokens, temperature)
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

2. Import and use the LLMMaster class:

   ```python
   from llm_master import LLMMaster

   # Create an instance
   llm_master = LLMMaster()

   # Summon specific LLMs or use summon_all() for all supported LLMs
   llm_master.summon({'openai': 'gpt-4o', 'anthropic': 'claude-3-5-sonnet-20240620'})
   # or
   # llm_master.summon_all()

   # Run the LLMs with a prompt
   llm_master.run(prompt="Tell me a joke about programming", max_tokens=100, temperature=0.7)

   # Access the results
   for provider, response in llm_master.results.items():
       print(f"{provider} response: {response}")
   ```

## Customization

You can easily add new LLM providers or models by updating the `REGISTERED_LLM` dictionary and creating a new thread class for the provider.

## Update Plan

Currently one common prompt can be used for multiple LLM generation. In work to enable separate prompts for individual LLMs.

## Contributing

Contributions to LLM Master are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
