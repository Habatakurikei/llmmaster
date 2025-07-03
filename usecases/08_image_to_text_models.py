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
web_image = ["https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"]

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
