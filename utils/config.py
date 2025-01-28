from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, YamlConfigSettingsSource


class LoggerConfig(BaseModel):
    path: Path
    module: list[str]
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class RunConfig(BaseModel):
    simulation: bool


class I2cConnectionSettings(BaseModel):
    address: PositiveInt
    bus: PositiveInt


class I2cMapping(BaseModel):
    raspberry: I2cConnectionSettings
    esp_sensors: I2cConnectionSettings
    esp_steppers: I2cConnectionSettings


class Config(BaseSettings):
    """Project Configuration.

    Example:
        ```python
        from utils.config import Config

        class Foo:
            def __init__(self):
                self.config = Config()
        ```
    """

    model_config = SettingsConfigDict(yaml_file="config.yml")

    log: LoggerConfig
    run: RunConfig
    i2c_mapping: I2cMapping

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define the priority for different sources of configuration.

        The configuration is loaded from the following sources
        (in descending order of priority) :

            1. Arguments passed to the Settings class initialiser.
            2. Environment variables
            3. Variables loaded from the `.env` file.
            4. Variables loaded from the `config.yml` file
            5. The default field values for the Settings model.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
        )
