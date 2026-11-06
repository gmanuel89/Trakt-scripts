# Import libraries
import logging
import logging.config
import json
import sys

## Retrieve logging level from configuration
def get_logging_level_from_config(config: dict) -> int:
    """Fetch logging level from a configuration JSON"""
    try:
        log_level_str = config.get('logging', {}).get('log_level', 'INFO').upper()
        print(f'Setting logging level to {log_level_str}...')
    except:
        print('Provided configuration cannot be parsed!')
        log_level_str = 'INFO'
    log_level = get_logging_level_from_string(log_level_str)
    print(f'Setting logging level to {log_level_str}...')
    return log_level

## Retrieve logging level from string
def get_logging_level_from_string(log_level_str: str) -> int:
    """Fetch logging level from a string"""
    log_level = logging.INFO
    try:
        if 'DEBUG' in log_level_str.upper():
            log_level = logging.DEBUG
        elif 'INFO' in log_level_str.upper():
            log_level = logging.INFO
        elif 'WARNING' in log_level_str.upper():
            log_level = logging.WARNING
        elif 'ERROR' in log_level_str.upper():
            log_level = logging.ERROR
        elif 'CRITICAL' in log_level_str.upper():
            log_level = logging.CRITICAL
        else:
            log_level = logging.INFO
    except:
        print(f'Provided level "{log_level_str} cannot be parsed!')
        log_level = logging.INFO
    return log_level
    
## Initialize logger
def initialize_logger(logger_name: str, log_file: str, logging_level: int, formatter='%(asctime)s [%(levelname)s] %(message)s', redirect_to_file=False, redirect_to_console=True) -> logging.Logger:
    # Initialize logger
    logger = logging.getLogger(logger_name)
    # Set logging level
    logger.setLevel(logging_level)
    # Set formatter
    formatter = logging.Formatter(formatter)
    # Create file handler (if not already existing) (this will result in multiple lines written)
    if not logger.hasHandlers():
        if redirect_to_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        if redirect_to_console:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
    # Prevent double logging if root logger is used
    logger.propagate = False
    # Return
    return logger

## Function to setup the logger globally
def setup_logger(config_json_file_path=None, logger_name='logger', log_file='app.log', default_logging_level='INFO', logging_formatter='%(asctime)s [%(levelname)s] %(message)s', redirect_to_file=False, redirect_to_console=True) -> logging.Logger:
    """Function to setup the logger globally"""
    # Configuration file provided
    if config_json_file_path:
        try:
            # Parse the configuration file
            config = json.loads(open(config_json_file_path).read())
            # Get logging level
            logging_level = get_logging_level_from_config(config)
        except:
            # Configuration file not found
            print(f'Configuration file {config_json_file_path} not found!')
            # Set default logging level
            print(f'Setting logging level to default ({default_logging_level})...')
            logging_level = get_logging_level_from_string(default_logging_level)
    else:
        # Set default logging level
        print(f'Setting logging level to default ({default_logging_level})...')
        logging_level = get_logging_level_from_string(default_logging_level)
    # Setup logger
    logger = initialize_logger(logger_name=logger_name, log_file=log_file, logging_level=logging_level, formatter=logging_formatter, redirect_to_console=redirect_to_console, redirect_to_file=redirect_to_file)
    # return
    return logger

## Function to setup the logger globally
def setup_logging(logging_config_json_file_path: str) -> None:
    """Function to setup the logger globally using a config file"""
    try:
        # Parse the configuration file
        print(f'Reading logging configuration from {logging_config_json_file_path} ...')
        with open(logging_config_json_file_path, 'r', encoding='utf8') as f:
            config = json.load(f)
        # Apply logging configuration
        logging.config.dictConfig(config)
    except:
        # Configuration file not found, apply default logging configuration
        print(f'Logging configuration file {logging_config_json_file_path} not found!')
        print('Applying default logging configuration...')
        logging.config.dictConfig(LOGGING_CONFIG_JSON)


## Default logging config JSON
LOGGING_CONFIG_JSON = {
  "version": 1,
  "disable_existing_loggers": False,

  "formatters": {
    "standard": {
      "format": "%(asctime)s [%(levelname)s] %(message)s"
    }
  },

  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "standard",
      "stream": "ext://sys.stdout"
    },
    "rotating_file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "standard",
      "maxBytes": 100 * 1024 * 1024,
      "backupCount": 20,
      "filename": "app.log",
      "encoding": 'utf-8'
    }
  },

  "root": {
    "level": "DEBUG",
    "handlers": ["console", "rotating_file"]
  }
}
