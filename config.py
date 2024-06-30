from dotenv import load_dotenv
import os
import json
import boto3
import pydantic
from typing import Optional, Union
import validators
from dynaconf import Dynaconf

# Load environment variables
load_dotenv()

# Use Dynaconf for hierarchical configuration
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True
)

class Settings(pydantic.BaseSettings):
    ELASTICSEARCH_URL: str
    INDEX_NAME: str
    MODEL_NAME: str
    LOG_LEVEL: str
    MAX_ITERATIONS: int

    @pydantic.validator('ELASTICSEARCH_URL')
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Invalid URL for ELASTICSEARCH_URL")
        return v

    @pydantic.validator('MAX_ITERATIONS')
    def validate_iterations(cls, v):
        if not isinstance(v, int) or v <= 0 or v > 1000:
            raise ValueError("MAX_ITERATIONS must be a positive integer between 1 and 1000")
        return v

    class Config:
        env_file = '.env'

settings = Settings(**dynaconf_settings.as_dict())

def reload_config():
    global settings
    dynaconf_settings.reload()
    settings = Settings(**dynaconf_settings.as_dict())
