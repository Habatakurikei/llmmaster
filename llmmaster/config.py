# API key settings
ADOBE_FIREFLY_CLIENT_ID_NAME = 'ADOBE_FIREFLY_CLIENT_ID'
ADOBE_FIREFLY_CLIENT_SECRET_NAME = 'ADOBE_FIREFLY_CLIENT_SECRET'
ANTHROPIC_KEY_NAME = 'ANTHROPIC_API_KEY'
GEMINI_KEY_NAME = 'GEMINI_API_KEY'
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

DEFAULT_ITT_MODELS = {'openai_itt': 'gpt-4o',
                      'google_itt': 'gemini-1.5-flash'}


def _full_default_list():
    full_list = {}
    full_list.update(DEFAULT_TTT_MODELS)
    full_list.update(DEFAULT_TTI_MODELS)
    full_list.update(DEFAULT_ITT_MODELS)
    return full_list


FULL_DEFAULT_MODELS = _full_default_list()

# REST API settings
PERPLEXITY_TTT_EP = 'https://api.perplexity.ai'
ADOBE_FIREFLY_TOKEN_PRE_EP = 'https://ims-na1.adobelogin.com/ims/token/v3?'
ADOBE_FIREFLY_TOKEN_POST_EP = '&grant_type=client_credentials&scope=openid,' \
    + 'AdobeID,firefly_enterprise,firefly_api,ff_apis'
ADOBE_FIREFLY_TTI_EP_BASE = 'https://firefly-api.adobe.io/'
ADOBE_FIREFLY_TTI_EP_GENERATE = '/images/generate'
STABLE_DIFFUSION_TTI_EP = \
    'https://api.stability.ai/v2beta/stable-image/generate/'

REQUEST_OK = 200

# settings for summon
SUMMON_LIMIT = 32
WAIT_FOR_SUMMONING = 1

# TTI setting
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# TTT settings
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
