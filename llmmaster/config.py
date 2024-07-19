# API key settings
ADOBE_FIREFLY_CLIENT_ID_NAME = 'ADOBE_FIREFLY_CLIENT_ID'
ADOBE_FIREFLY_CLIENT_SECRET_NAME = 'ADOBE_FIREFLY_CLIENT_SECRET'
ANTHROPIC_KEY_NAME = 'ANTHROPIC_API_KEY'
GOOGLE_KEY_NAME = 'GOOGLE_API_KEY'
GROQ_KEY_NAME = 'GROQ_API_KEY'
OPENAI_KEY_NAME = 'OPENAI_API_KEY'
PERPLEXITY_KEY_NAME = 'PERPLEXITY_API_KEY'
STABLE_DIFFUSION_KEY_NAME = 'STABLE_DIFFUSION_API_KEY'


# Default models setting
DEFAULT_TTT_MODELS = {'anthropic': 'claude-3-5-sonnet-20240620',
                      'google': 'gemini-1.5-flash',
                      'groq': 'llama3-70b-8192',
                      'openai': 'gpt-4o',
                      'perplexity': 'llama-3-sonar-large-32k-online'}

DEFAULT_TTI_MODELS = {'openai_tti': 'dall-e-3',
                      'stable_diffusion_tti': 'core'}

DEFAULT_TTA_MODELS = {'openai_tts': 'tts-1'}

DEFAULT_ITT_MODELS = {'openai_itt': 'gpt-4o',
                      'google_itt': 'gemini-1.5-flash'}

DEFAULT_ITI_MODELS = {'openai_iti': 'dall-e-2',
                      'stable_diffusion_iti': 'v2beta'}

DEFAULT_VTT_MODELS = {'google_vtt': 'gemini-1.5-flash'}

DEFAULT_ATT_MODELS = {'openai_att': 'whisper-1'}


def _full_default_list():
    full_list = {}
    full_list.update(DEFAULT_TTT_MODELS)
    full_list.update(DEFAULT_TTI_MODELS)
    full_list.update(DEFAULT_TTA_MODELS)
    full_list.update(DEFAULT_ITT_MODELS)
    full_list.update(DEFAULT_ITI_MODELS)
    full_list.update(DEFAULT_ATT_MODELS)
    full_list.update(DEFAULT_VTT_MODELS)
    return full_list


FULL_DEFAULT_MODELS = _full_default_list()

# REST API settings
REQUEST_ACCEPTED = 202
REQUEST_OK = 200

PERPLEXITY_TTT_EP = 'https://api.perplexity.ai'

ADOBE_FIREFLY_TOKEN_PRE_EP = 'https://ims-na1.adobelogin.com/ims/token/v3?'
ADOBE_FIREFLY_TOKEN_POST_EP = '&grant_type=client_credentials&scope=openid,' \
    + 'AdobeID,firefly_enterprise,firefly_api,ff_apis'
ADOBE_FIREFLY_TTI_EP_BASE = 'https://firefly-api.adobe.io/'
ADOBE_FIREFLY_TTI_EP_GENERATE = '/images/generate'

STABLE_DIFFUSION_VERSION = 'v2beta'
STABLE_DIFFUSION_BASE_EP = 'https://api.stability.ai'

STABLE_DIFFUSION_TTI_EP = '/stable-image/generate'

STABLE_DIFFUSION_ITI_UPSCALE_CONSERVATIVE_EP = \
    '/stable-image/upscale/conservative'
STABLE_DIFFUSION_ITI_UPSCALE_CREATIVE_START_EP = \
    '/stable-image/upscale/creative'
STABLE_DIFFUSION_ITI_UPSCALE_CREATIVE_RESULT_EP = \
    '/stable-image/upscale/creative/result/{id}'
STABLE_DIFFUSION_ITI_EDIT_ERASE_EP = \
    '/stable-image/edit/erase'
STABLE_DIFFUSION_ITI_EDIT_INPAINT_EP = \
    '/stable-image/edit/inpaint'
STABLE_DIFFUSION_ITI_EDIT_OUTPAINT_EP = \
    '/stable-image/edit/outpaint'
STABLE_DIFFUSION_ITI_EDIT_SEARCH_AND_REPLACE_EP = \
    '/stable-image/edit/search-and-replace'
STABLE_DIFFUSION_ITI_EDIT_REMOVE_BACKGROUND_EP = \
    '/stable-image/edit/remove-background'

STABLE_DIFFUSION_ITV_START_EP = '/image-to-video'
STABLE_DIFFUSION_ITV_RESULT_EP = '/image-to-video/result/{id}'

# settings for summon
SUMMON_LIMIT = 32
WAIT_FOR_SUMMONING = 1

# Dummy prompt settings
PROVIDERS_NEED_DUMMY_PROMPT = ['openai_att', 'openai_iti',
                               'stable_diffusion_iti']
OPENAI_ITI_MODE_NEED_DUMMY_PROMPT = ['variations']
SD_ITI_MODE_NEED_DUMMY_PROMPT = ['erase', 'outpaint', 'remove_background']

# Text-To-Text settings
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# Text-To-Image settings
MAX_SEED = 4294967294

ADOBE_FIREFLY_CONTENT_CLASS = ['art', 'photo']
ADOBE_FIREFLY_TTI_MODELS = ['v3', 'v2']
ADOBE_FIREFLY_TTI_SIZE_LIST = [{"width": 2048, "height": 2048},
                               {"width": 2304, "height": 1792},
                               {"width": 1792, "height": 2304},
                               {"width": 2688, "height": 1536},
                               {"width": 1344, "height": 768},
                               {"width": 1152, "height": 896},
                               {"width": 896, "height": 1152},
                               {"width": 1024, "height": 1024}]
ADOBE_FIREFLY_DEFAULT_N = 1
ADOBE_FIREFLY_MAX_N = 4

OPENAI_TTI_SIZE_LIST = ['1024x1024', '1024x1792', '1792x1024',
                        '256x256', '512x512']
OPENAI_TTI_QUALITY_LIST = ['hd', 'standard']
OPENAI_TTI_DEFAULT_N = 1
OPENAI_TTI_MAX_N = 10

STABLE_DIFFUSION_TTI_MODELS = ['ultra', 'core']
STABLE_DIFFUSION_TTI_OUTPUT_FORMATS = ['png', 'jpeg', 'webp']
STABLE_DIFFUSION_TTI_ASPECT_RATIO_LIST = ['1:1', '16:9', '21:9', '2:3',
                                          '3:2', '4:5', '5:4', '9:16', '9:21']
STABLE_DIFFUSION_TTI_STYLE_PRESET_LIST = ['anime', '3d-model', 'analog-film',
                                          'cinematic', 'comic-book',
                                          'digital-art', 'enhance',
                                          'fantasy-art', 'isometric',
                                          'line-art', 'low-poly',
                                          'modeling-compound', 'neon-punk',
                                          'origami', 'photographic',
                                          'pixel-art', 'tile-texture']

# Text-To-Audio settings
OPENAI_TTS_MODELS = ['tts-1', 'tts-1-hd']
OPENAI_TTS_VOICE_OPTIONS = ['alloy', 'echo', 'fable',
                            'onyx', 'nova', 'shimmer']
OPENAI_TTS_RESPONSE_FORMAT_LIST = ['mp3', 'opus', 'aac',
                                   'flac', 'wav', 'pcm']

OPENAI_TTS_MAX_SPEED = 4.0
OPENAI_TTS_MIN_SPEED = 0.25
OPENAI_TTS_DEFAULT_SPEED = 1.0

# Image-To-Image settings
OPENAI_ITI_DEFAULT_N = 1
OPENAI_ITI_MAX_N = 10
OPENAI_ITI_SIZE_LIST = ['1024x1024', '512x512', '256x256']
OPENAI_ITI_MODE_LIST = ['edits', 'variations']
OPENAI_ITI_ACCEPTABLE_COLOR_MODE = ['RGBA', 'LA', 'L']

STABLE_DIFFUSION_ITI_MODE_LIST = ['upscale_conservative', 'upscale_creative',
                                  'erase', 'inpaint', 'outpaint',
                                  'search_and_replace', 'remove_background']
STABLE_DIFFUSION_ITI_OUTPUT_FORMATS = ['png', 'jpeg', 'webp']
STABLE_DIFFUSION_CREATIVITY_DEFAULT = 0.3
STABLE_DIFFUSION_CONSERVATIVE_CREATIVITY_MIN = 0.2
STABLE_DIFFUSION_CONSERVATIVE_CREATIVITY_MAX = 0.5
STABLE_DIFFUSION_CREATIVE_CREATIVITY_MIN = 0.0
STABLE_DIFFUSION_CREATIVE_CREATIVITY_MAX = 0.35
STABLE_DIFFUSION_GROW_MASK_MIN = 0
STABLE_DIFFUSION_GROW_MASK_MAX = 20
STABLE_DIFFUSION_OUTPAINT_LEFT_MAX = 2000
STABLE_DIFFUSION_OUTPAINT_RIGHT_MAX = 2000
STABLE_DIFFUSION_OUTPAINT_UP_MAX = 2000
STABLE_DIFFUSION_OUTPAINT_DOWN_MAX = 2000
STABLE_DIFFUSION_OUTPAINT_CREATIVITY_MIN = 0.0
STABLE_DIFFUSION_OUTPAINT_CREATIVITY_MAX = 1.0
WAIT_FOR_UPSCALE_CREATIVE_RESULT = 5

# Audio-To-Text settings
OPENAI_ATT_MODE_LIST = ['transcriptions', 'translations']
OPENAI_ATT_RESPONSE_FORMAT_LIST = ['json', 'text', 'srt',
                                   'verbose_json', 'vtt']
OPENAI_ATT_DEFAULT_TIMESTAMP_GRANULARITIES = ['word', 'segment']

# Video-To-Text settings
WAIT_FOR_GOOGLE_VTT_UPLOAD = 5
WAIT_FOR_GOOGLE_VTT_TIMEOUT = 600
