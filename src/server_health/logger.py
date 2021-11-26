import logging
import logging.config
import yaml
import os
from server_health.constants import default_logger

# Dynamically get /path/to/logging.yaml
MY_DIR = os.path.dirname(os.path.realpath(__file__))
LOGGING_CONFIG = f'{MY_DIR}/logging.yaml'


def setup_logging():

    # This function can be invoked in order to setup logging based on a
    # yaml config present in the root dir of this project
    try:
        with open(LOGGING_CONFIG, 'rt') as f:
            # Load config from logging.yaml file
            _config = yaml.safe_load(f.read())
            # Get the filename from the yaml configuration file
            magnificent_log_loc = _config['handlers']['magnificent_handler'][
                'filename']
            # We save so we can return it, and log to the console
            # So future developrs can figure out /path/to/magnificent.log
            mag_loc = f'{MY_DIR}/{magnificent_log_loc}'
            # Assign log location and initialise magnificent_handler
            _config['handlers']['magnificent_handler']['filename'] = mag_loc
            f.close()
        # Parse customised logger to be used project-wide
        logging.config.dictConfig(_config)

    except ValueError as e:
        # If
        logging.basicConfig(level=logging.INFO)
        logging.error(e)
        logging.error(
            'Error in Logging Configuration. Using default configuration')

    logger = logging.getLogger(default_logger)
    return logger, mag_loc
