import json
import logging

class ConfigError(Exception):
    """Custom exception for configuration loading errors."""
    pass

def load_config(config_file):
    """
    Load configuration from a JSON file.

    Args:
        config_file (str): Path to the JSON configuration file.

    Returns:
        dict: Loaded configuration as a dictionary.

    Raises:
        ConfigError: If the file is not found or the JSON is invalid.
    """
    try:
        # Open and read the configuration file with UTF-8 encoding
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_file} not found.")
        raise ConfigError(f"Configuration file {config_file} not found.")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file {config_file}.")
        raise ConfigError(f"Error decoding JSON from the configuration file {config_file}.")
