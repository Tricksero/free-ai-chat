import configparser
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class Config:

    def __init__(self, config_file = BASE_DIR / "config.ini") -> None:
        """
        Initailisiert die Klasse und die Attribute.

        Args:
            config_file (str, optional): _description_. Defaults to "config.ini".
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_server_configs(self):
        return {
            "ip": self.config.get("server", "ip"),
            "port": self.config.get("server", "port"),
            "private_key": self.config.get("server", "private_key"),
            "public_key": self.config.get("server", "public_key"),
            "wait_for_response": self.config.get("server", "wait_for_response"),
            "recive_limit": int(self.config.get("server", "recive_limit")),
        }



    def get_gpt4all_setting(self):
        return {
            "default_model": self.config.get("gpt4all", "default_model"),
            "max_token": self.config.get("gpt4all", "max_token"),
        }

