import json
import logging
import os

from dotenv import load_dotenv


class SettingsLoader:
    def __init__(self):
        """
        Initializes the SettingsLoader. It first checks if the specified .env file exists.
        If the .env file is found, it loads environment variables from it. Otherwise,
        it falls back to loading configuration from JSON secrets files.

        :param env_file: The name of the environment file (default: .env).
        :param secrets_dir_path: The directory path for the JSON secrets (default: /vault/secrets).
        :param secrets_file_name: The name of the JSON secrets file (default: appsecrets.json).
        """

        self.env_file = ".env"
        self.secrets_dir_path = "/vault/secrets"
        self.secrets_file_name = "appsecrets.json"
        self.config = None

        try:
            if os.path.exists(self.env_file):
                logging.info("Loading secrets from .env file")
                self._load_env_file()
            else:
                logging.info("Loading secrets from JSON config")
                self._load_json_config()
        except Exception as e:
            logging.error(f"Error loading secrets: {e}", exc_info=True)
            raise
        
    def _load_env_file(self):
        """
        Loads the environment variables from the .env file.
        """
        load_dotenv(self.env_file)

    def _load_json_config(self):
        """
        Loads configuration data from a JSON file and sets them as environment variables.
        If the main secrets file is not found, it falls back to the development secrets file (devappsecrets.json).
        """
        try:
            secrets_path = os.path.join(self.secrets_dir_path, self.secrets_file_name)
            logging.info(f"Loading secrets from {secrets_path}")

            with open(secrets_path) as json_data_file:
                self.config = json.load(json_data_file)

        except FileNotFoundError:
            logging.warning("Settings not found. Defaulting to local devappsecrets.json")
            with open("devappsecrets.json") as json_data_file:
                self.config = json.load(json_data_file)

        # Set environment variables from loaded config
        for key, value in self.config.items():
            os.environ[key] = str(value)

    def get(self, key: str, default: str = None) -> str:
        """
        Retrieves the value of the environment variable or config key.
        If the .env file is present, it fetches from environment variables.
        If the .env file is absent, it fetches from the JSON config.

        :param key: The key to retrieve.
        :param default: The default value if the key is not found (default: None).
        :return: The value of the environment variable or config key.
        """
        if self.config is not None:
            # Fetch from JSON config if .env does not exist
            return self.config.get(key, default)
        else:
            # Fetch from environment variables if .env exists
            return os.getenv(key, default)
