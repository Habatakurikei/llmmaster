# Data type in LLMMaster.results for each model

Brief summary of what type to be stored in LLMMaster.results for each model.

Here are typical cases how to handle in case of successful request:
- `str`: most of text-output models return str, which seems easiest to handle for next process in your program.
- `requests.models.Response`: REST API raw response from requests, including `status_code`. Save output (e.g. `master.results["stable_diffusion_tti"].content`) using the general python write function with "wb" option and extension like `png` and `mp4`. See formal document of `requests` library for full attributes. The response header may contain some important attribute like `master.results["stable_diffusion_tti"].headers["Seed"]` for image re-generation.
- `openai._legacy_response.HttpxBinaryResponseContent`: binary data of generated speech. Save using the general python write function with "wb" option and extension like `mp3` and `aac`.
- `ImagesResponse` class: specific for OpenAI text-to-image and image-to-image models. This class includes URLs for generated image and other information. For example, `master.results["openai_tti"].data[0].url` for the first generated image. See formal document for full attributes.
- `Translation` or `Transcription` class: specific for OpenAI speech-to-text models. These are actually texts but may contain plain text and timestamps. See formal document for how to decode.
- `TextToSpeechClient.convert.generator`: specific for ElevenLabs text-to-speech model. Use `elevenlabs.save(object, "output.mp3")` to save generated speech. Only mp3 format might be supported for the momoent.

In case of any error, the result will be stored as str. Print it to see problem details.

## Text-To-Text
  - AnthropicLLM: response.content[0].text.strip()
  - CerebrasLLM: response.choices[0].message.content.strip()
  - GroqLLM: response.choices[0].message.content.strip()
  - GoogleLLM: response.text.strip()
  - MistralLLM: response.choices[0].message.content.strip()
  - OpenAILLM: response.choices[0].message.content.strip()
  - PerplexityLLM: response.choices[0].message.content.strip()

## Text-To-Image
  - OpenAITextToImage: ImagesResponse class
  - StableDiffusionTextToImage: requests.models.Response class

## Text-To-Audio
  - OpenAITextToSpeech: openai._legacy_response.HttpxBinaryResponseContent object
  - ElevenLabsTextToSpeech: TextToSpeechClient.convert.generator object
  - VoicevoxTextToSpeech: requests.models.Response class

## Text-To-Video
  - PikaPikaPikaGeneration: requests.models.Response class

## Image-To-Text
  - OpenAIImageToText: response.choices[0].message.content.strip()
  - GoogleImageToText: response.text.strip()

## Image-To-Image
  - OpenAIImageToImage: ImagesResponse class
  - StableDiffusionImageToImage: requests.models.Response class

## Image-To-Video
  - StableDiffusionImageToVideo: requests.models.Response class

## Audio-To-Text
  - OpenAISpeechToText: Translation or Transcription class
  - GoogleSpeechToText: response.text.strip()

## Video-To-Text
  - GoogleVideoToText: response.text.strip()

## Meshy
  - MeshyTextToTexture: requests.models.Response class
  - MeshyTextTo3D: requests.models.Response class
  - MeshyTextTo3DRefine: requests.models.Response class
  - MeshyTextToVoxel: requests.models.Response class
  - MeshyImageTo3D: requests.models.Response class
