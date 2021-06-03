from ..models import Autobase as AutobaseDatabase
from .. import app
from . import default_config
from .twitter_autobase import Autobase as AutobaseApp
import logging

logger = logging.getLogger(__name__)

autobase_app = dict()
# {'app_name':object, 'app_name_2':'error'}

# Change default_config type object to dictionary
default_config_dict = dict()
tmp_dict = default_config.__dict__
for key in list(default_config.__dict__)[list(default_config.__dict__).index('CONSUMER_KEY'):]:
    default_config_dict[key] = tmp_dict[key]
default_config = default_config_dict.copy()
del tmp_dict
del default_config_dict

def update_config(new_dict:dict):
    config_dict = default_config.copy()
    config_dict.update(new_dict)
    return type('autobase config', (object,), config_dict)

for data in AutobaseDatabase.query.all():
    new_dict = dict()
    data_dict = data.__dict__
    for key in data_dict.keys():
        if key in list(default_config):
            new_dict[key] = data_dict[key]
    try:
        autobase_app[data.name] = AutobaseApp(update_config(new_dict))
        autobase_app[data.name].app_name = data.name
    except Exception:
        autobase_app[data.name] = 'error'
        logger.error(f'app_name: {data.name}; owner_username: {data.owner.username}')

# Register webhook url to twitter
if app.config['SERVER'] == 'ngrok':
    from .twitter_autobase import webhook_manager as webMan
    from requests import get
    from threading import Thread
    from time import sleep

    callback_url = webMan.connect_ngrok(app.config['NGROK_TOKEN'])
    def register_webhook():
        while get(callback_url).status_code != 200:
            sleep(1)
        for key in list(autobase_app):
            if autobase_app[key] == 'error':
                continue
            webMan.register_webhook(
                callback_url + '/callback',
                autobase_app[key].app_name,
                autobase_app[key].credential)
    Thread(target=register_webhook).start()

elif app.config['SERVER'] == 'heroku':
    # Register webhook is executed when user add new app in website
    pass

else:
    from sys import exit
    logger.error("SERVER in .env must be 'ngrok' or 'heroku'")
    exit()