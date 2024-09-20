# API key settings
ADOBE_FIREFLY_CLIENT_ID_NAME = 'ADOBE_FIREFLY_CLIENT_ID'
ADOBE_FIREFLY_CLIENT_SECRET_NAME = 'ADOBE_FIREFLY_CLIENT_SECRET'
ANTHROPIC_KEY_NAME = 'ANTHROPIC_API_KEY'
CEREBRAS_KEY_NAME = 'CEREBRAS_API_KEY'
DALLE_KEY_NAME = 'DALLE_API_KEY'
DUMMY_KEY_NAME = 'DUMMY_API_KEY'
ELEVENLABS_KEY_NAME = 'ELEVENLABS_API_KEY'
FAL_KEY_NAME = 'FAL_KEY'
GOOGLE_KEY_NAME = 'GOOGLE_API_KEY'
GROQ_KEY_NAME = 'GROQ_API_KEY'
LUMAAI_KEY_NAME = 'LUMAAI_API_KEY'
MESHY_KEY_NAME = 'MESHY_API_KEY'
MISTRAL_KEY_NAME = 'MISTRAL_API_KEY'
OPENAI_KEY_NAME = 'OPENAI_API_KEY'
PERPLEXITY_KEY_NAME = 'PERPLEXITY_API_KEY'
PIKAPIKAPIKA_KEY_NAME = 'PIKAPIKAPIKA_API_KEY'
STABLE_DIFFUSION_KEY_NAME = 'STABLE_DIFFUSION_API_KEY'
TRIPO_KEY_NAME = 'TRIPO_API_KEY'

# Default models setting
DEFAULT_TTT_MODELS = {'anthropic': 'claude-3-haiku-20240307',
                      'cerebras': 'llama3.1-8b',
                      'google': 'gemini-1.5-flash',
                      'groq': 'llama-3.1-8b-instant',
                      'mistral': 'mistral-small-latest',
                      'openai': 'gpt-4o-mini',
                      'perplexity': 'llama-3.1-sonar-small-128k-online'}

DEFAULT_TTI_MODELS = {'flux1_fal_tti': 'fal-ai/flux/dev',
                      'openai_tti': 'dall-e-3',
                      'stable_diffusion_tti': 'core'}

DEFAULT_TTA_MODELS = {'elevenlabs_tts': 'eleven_multilingual_v2',
                      'elevenlabs_ttse': 'dummy',
                      'openai_tts': 'tts-1',
                      'voicevox_tts': 'dummy'}

DEFAULT_ITT_MODELS = {'google_itt': 'gemini-1.5-flash',
                      'openai_itt': 'gpt-4o'}

DEFAULT_ITI_MODELS = {'flux1_fal_iti': 'fal-ai/flux/dev/image-to-image',
                      'openai_iti': 'dall-e-2',
                      'stable_diffusion_iti': 'v2beta'}

DEFAULT_ITV_MODELS = {'stable_diffusion_itv': 'v2beta'}

DEFAULT_ATT_MODELS = {'google_stt': 'gemini-1.5-flash',
                      'openai_stt': 'whisper-1'}

DEFAULT_ATA_MODELS = {'elevenlabs_aiso': 'dummy'}

DEFAULT_VTT_MODELS = {'google_vtt': 'gemini-1.5-flash'}

DEFAULT_MESHY_MODELS = {'meshy_tttx': 'dummy',
                        'meshy_tt3d': 'meshy-3',
                        'meshy_tt3d_refine': 'dummy',
                        'meshy_ttvx': 'dummy',
                        'meshy_it3d': 'dummy'}

DEFAULT_PIKAPIKAPIKA_MODELS = {'pikapikapika_ttv': 'dummy'}

DEFAULT_LUMAAI_MODELS = {'lumaai_ttv': 'dummy',
                         'lumaai_itv': 'dummy',
                         'lumaai_vtv': 'dummy'}


def _full_default_list():
    full_list = {}
    full_list.update(DEFAULT_TTT_MODELS)
    full_list.update(DEFAULT_TTI_MODELS)
    full_list.update(DEFAULT_TTA_MODELS)
    full_list.update(DEFAULT_ITT_MODELS)
    full_list.update(DEFAULT_ITI_MODELS)
    full_list.update(DEFAULT_ITV_MODELS)
    full_list.update(DEFAULT_ATT_MODELS)
    full_list.update(DEFAULT_ATA_MODELS)
    full_list.update(DEFAULT_VTT_MODELS)
    full_list.update(DEFAULT_MESHY_MODELS)
    full_list.update(DEFAULT_PIKAPIKAPIKA_MODELS)
    full_list.update(DEFAULT_LUMAAI_MODELS)
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

STABLE_DIFFUSION_ITV_VERSION = 'v2beta'
STABLE_DIFFUSION_ITV_START_EP = '/image-to-video'
STABLE_DIFFUSION_ITV_RESULT_EP = '/image-to-video/result/{id}'

MESHY_BASE_EP = 'https://api.meshy.ai'

MESHY_TTTX_START_EP = '/v1/text-to-texture'
MESHY_TT3D_START_EP = '/v2/text-to-3d'
MESHY_TTVX_START_EP = '/v1/text-to-voxel'
MESHY_IT3D_START_EP = '/v1/image-to-3d'

TRIPO_BASE_EP = 'https://api.tripo3d.ai/v2/openapi'
TRIPO_RESULT_EP = 'wss://api.tripo3d.ai/v2/openapi/task/watch/{tid}'
TRIPO_UPLOAD_EP = '/upload'
TRIPO_TASK_EP = '/task'
TRIPO_WALLET_EP = '/user/balance'

PIKAPIKAPIKA_BASE_EP = 'https://api.pikapikapika.io/web'
PIKAPIKAPIKA_GENERATION_EP = '/generate'
PIKAPIKAPIKA_LIPSYNC_EP = '/lipSync'
PIKAPIKAPIKA_ADJUST_EP = '/adjust'
PIKAPIKAPIKA_EXTEND_EP = '/extend'
PIKAPIKAPIKA_UPSCALE_EP = '/upscale'
PIKAPIKAPIKA_RESULT_EP = '/jobs/{id}'

# settings for summon
SUMMON_LIMIT = 100
WAIT_FOR_STARTING = 1.0

# Dummy prompt settings
PROVIDERS_NEED_DUMMY_PROMPT = ['openai_stt', 'stable_diffusion_itv',
                               'elevenlabs_aiso',
                               'meshy_tttx', 'meshy_tt3d_refine', 'meshy_it3d']
OPENAI_ITI_MODE_NEED_DUMMY_PROMPT = ['variations']
SD_ITI_MODE_NEED_DUMMY_PROMPT = ['erase', 'outpaint', 'remove_background']

# Text-To-Text settings
# Note:
# top_p is common for all models but top_k is only for anthropic and google.
# Not available for openai, groq and perplexity (OpenAI-based models).
DEFAULT_TOKENS = 4096
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 50

ANTHROPIC_MODELS = ['claude-3-haiku-20240307',
                    'claude-3-sonnet-20240229',
                    'claude-3-opus-20240229',
                    'claude-3-5-sonnet-20240620']

CEREBRAS_MODELS = ['llama3.1-8b', 'llama3.1-70b']

GOOGLE_MODELS = ['gemini-1.5-flash',
                 'gemini-1.5-pro',
                 'gemini-1.5-flash-exp-0827',
                 'gemini-1.5-pro-exp-0827']

GROQ_MODELS = ['gemma-7b-it', 'gemma2-9b-it',
               'llama-3.1-70b-versatile', 'llama-3.1-8b-instant',
               'llama3-70b-8192', 'llama3-8b-8192',
               'llama3-8b-8192', 'mixtral-8x7b-32768']

MISTRAL_MODELS = ['mistral-small-latest', 'mistral-medium-latest',
                  'mistral-large-latest', 'open-mistral-nemo',
                  'codestral-latest', 'mistral-embed']

OPENAI_MODELS = ['gpt-4o-mini', 'gpt-4o', 'gpt-4o-2024-08-06']

PERPLEXITY_MODELS = ['llama-3.1-sonar-small-128k-online',
                     'llama-3.1-sonar-large-128k-online',
                     'llama-3.1-sonar-huge-128k-online']

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

FLUX1_FAL_TTI_MODELS = ['fal-ai/flux/dev', 'fal-ai/flux/schnell']
FLUX1_FAL_TTI_ASPECT_RATIO_LIST = ['square_hd', 'square',
                                   'portrait_4_3', 'portrait_16_9',
                                   'landscape_4_3', 'landscape_16_9']
WAIT_FOR_FLUX1_FAL_TTI_RESULT = 2.0

# Text-To-Audio settings
OPENAI_TTS_MODELS = ['tts-1', 'tts-1-hd']
OPENAI_TTS_VOICE_OPTIONS = ['alloy', 'echo', 'fable',
                            'onyx', 'nova', 'shimmer']
OPENAI_TTS_RESPONSE_FORMAT_LIST = ['mp3', 'opus', 'aac',
                                   'flac', 'wav', 'pcm']

OPENAI_TTS_MAX_SPEED = 4.0
OPENAI_TTS_MIN_SPEED = 0.25
OPENAI_TTS_DEFAULT_SPEED = 1.0

ELEVENLABS_TTS_MODELS = ['eleven_multilingual_v2', 'eleven_turbo_v2_5',
                         'eleven_turbo_v2', 'eleven_monolingual_v1',
                         'eleven_monolingual_v1']

ELEVENLABS_DEFAULT_VOICE_ID = '8EkOjt4xTPGMclNlh1pk'
# ELEVENLABS_DEFAULT_VOICE_ID = '21m00Tcm4TlvDq8ikWAM'
ELEVENLABS_DEFAULT_STABILITY = 1.0
ELEVENLABS_DEFAULT_SIMILARITY = 0.75
ELEVENLABS_DEFAULT_PROMPT_INFLUENCE = 0.3

VOICEVOX_BASE_EP = 'http://localhost:50021'
VOICEVOX_QUERY_EP = '/audio_query'
VOICEVOX_SYNTHESIS_EP = "/synthesis"
VOICEVOX_DEFAULT_VOICE_ID = 1


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
WAIT_FOR_UPSCALE_CREATIVE_RESULT = 5.0

# Image-To-Video settings
STABLE_DIFFUSION_ITV_CFG_SCALE_DEFAULT = 1.8
STABLE_DIFFUSION_ITV_CFG_SCALE_MIN = 0.0
STABLE_DIFFUSION_ITV_CFG_SCALE_MAX = 10.0
STABLE_DIFFUSION_ITV_MOTION_BUCKET_DEFAULT = 127
STABLE_DIFFUSION_ITV_MOTION_BUCKET_MIN = 1
STABLE_DIFFUSION_ITV_MOTION_BUCKET_MAX = 255
WAIT_FOR_ITV_RESULT = 5.0

# Audio-To-Text settings
OPENAI_STT_MODE_LIST = ['transcriptions', 'translations']
OPENAI_STT_RESPONSE_FORMAT_LIST = ['json', 'text', 'srt',
                                   'verbose_json', 'vtt']
OPENAI_STT_DEFAULT_TIMESTAMP_GRANULARITIES = ['word', 'segment']

# Audio-To-Audio settings
ELEVENLABS_STS_MODELS = ['eleven_multilingual_sts_v2', 'eleven_english_sts_v2']

# Video-To-Text settings
WAIT_FOR_GOOGLE_VTT_UPLOAD = 5.0
WAIT_FOR_GOOGLE_VTT_TIMEOUT = 600.0

# Meshy specific settings
MESHY_TT3D_MODELS = ['meshy-3', 'meshy-3-turbo']
MESHY_TT3D_STYLES_LIST = ['realistic', 'cartoon', 'low-poly',
                          'sculpture', 'pbr']

MESHY_TTTX_STYLES_LIST = ['realistic', 'fake-3d-cartoo', 'japanese-anime',
                          'cartoon-line-art', 'realistic-hand-drawn',
                          'fake-3d-hand-drawn', 'oriental-comic-ink']
MESHY_TTTX_RESOLUTION_LIST = ['1024', '2048', '4096']

MESHY_VOXEL_SHRINK_LIST = [8, 4, 2, 1]

MESHY_TT3D_TEXTURE_RICHNESS_LIST = ['high', 'medium', 'low', 'none']

MESHY_STATUS_EXPIRED = 'EXPIRED'
MESHY_STATUS_FAILED = 'FAILED'
MESHY_STATUS_IN_PROGRESS = 'IN_PROGRESS'
MESHY_STATUS_PENDING = 'PENDING'
MESHY_STATUS_SUCCEEDED = 'SUCCEEDED'
MESHY_STATUS_FOR_RESULT = ['SUCCEEDED', 'FAILED', 'EXPIRED']

WAIT_FOR_MESHY_RESULT = 5.0

# Tripo specific settings
TRIPO_MODELS = ['default', 'v2.0-20240919', 'v1.4-20240625', 'v1.3-20240522']
TRIPO_STATUS_IN_PROGRESS = ['running', 'queued']
WAIT_FOR_TRIPO_RESULT = 5.0

# PikaPikaPika.art specific settings
PIKAPIKAPIKA_STYLE_LIST = ['Anime', 'Moody', '3D', 'Watercolor', 'Natural',
                           'Claymation', 'Black & white']
PIKAPIKAPIKA_ASPECT_RATIO_LIST = ['16:9', '9:16', '1:1', '5:2', '4:5', '4:3']
PIKAPIKAPIKA_MAX_FPS = 24
WAIT_FOR_PIKAPIKAPIKA_RESULT = 5.0

# Luma AI specific settings
LUMAAI_ASPECT_RATIO_LIST = ['16:9', '4:3']
LUMAAI_STATUS_IN_PROGRESS = ['queued', 'dreaming']
WAIT_FOR_LUMAI_RESULT = 5.0
