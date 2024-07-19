# LLMMaster Changelog

## [Unreleased]
- (pending) Adobe Firefly for Text-To-Image

## [0.1.6] - 2024-07-19
### Added
- Image-To-Image model classes
  - `OpenAIImageToImage`
  - `StableDiffusionImageToImage`
- `elapsed_time` attribute to `LLMMaster` class
### Changed
- adding dummpy prompt process to `LLMInstanceCreator.verify()`
- `OpenAITextToImage` returns `ImagesResponses` class, changed from plain text of image URL

## [0.1.5] - 2024-07-18
### Added
- Audio-To-Text model class
  - `OpenAIAudioToText`

## [0.1.4] - 2024-07-17
### Added
- Video-To-Text model class
  - `GoogleVideoToText`

## [0.1.3] - 2024-07-16
### Added
- Image-To-Text model classes
  - `OpenAIImageToText`
  - `GoogleImageToText`

## [0.1.2] - 2024-07-14
### Added
- Text-To-Image model classes
  - `OpenAITextToImage`
  - `StableDiffusionTextToImage`

## [0.1.1] - 2024-07-12
### Changed
- renamed package name from `llm-master` to `llmmaster` because hyphens and underscores were mixed up and made confusion
### Removed
- ver. 0.1.0 from `llm-master` and start 0.1.1 for new PyPI repository `llmmaster`

## [0.1.0] - 2024-07-10
### Added
- `BaseModel` class in `base_model.py`
- `verify()` function to `LLMInstanceCreator` class
- new folders, `llm_master` and `tests`
- test functions using pytest in folder `tests` and tested
- initial PyPI uploaded

## [0.0.3] - 2024-07-09
### Added
- Text-To_Image model
  - `OpenAITTI`
- `config.py`
- `setup.py`
### Changed
- separated files `text_to_text_models.py`, `text_to_image_models.py`

## [0.0.3] - 2024-07-09
### Changed
- `LLMInstanceCreator.create()`, simplified the process of creating LLM instances

## [0.0.2] - 2024-07-08
### Added
- `LLMInstanceCreator` class in `llm_master.py` for creating and verifying LLM instances
- `LLMMaster.pack_parameters()` method to help create entry dictionaries
- `LLMMaster.dismiss()` method to clear instances and results
- set limit to 32 for max instances
- run each thread in each 1 sec of interval due to API provider limitation
### Removed
- `LLMMaster.summon_all()` method
- `LLMMaster.split_llm_information()` method

## [0.0.1] - 2024-07-05
### Added
- uploaded the first version to GitHub
