# pylint: disable=unused-import
import os

try:
    from .config_local import TOKEN, OWNER, OWNER_NAME
except ImportError:
    TOKEN = os.getenv('ASSIST_BOT_TOKEN')
    OWNER = os.getenv('ASSIST_BOT_OWNER')
    OWNER_NAME = os.getenv('ASSIST_BOT_OWNER_NAME')
