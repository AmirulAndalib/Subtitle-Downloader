#!/usr/bin/python3
# coding: utf-8

"""
This module is for default setting.
"""
from __future__ import annotations
from os.path import dirname
from pathlib import Path
from typing import Any
import rtoml

app_name = "Subtitle-Downloader"
__version__ = "2.0.0"


dir_path = dirname(dirname(__file__)).replace("\\", "/")


class Platform:
    """
    Define all streaming service name
    """

    APPLETVPLUS = 'AppleTVPlus'
    CATCHPLAY = 'CatchPlay'
    DISNEYPLUS = 'DisneyPlus'
    FRIDAYVIDEO = 'FridayVideo'
    HBOGOASIA = 'HBOGOAsia'
    IQIYI = 'iQIYI'
    ITUNES = 'iTunes'
    KKTV = 'KKTV'
    LINETV = 'LineTV'
    MYVIDEO = 'MyVideo'
    NOWE = 'NowE'
    NOWPLAYER = 'NowPlayer'
    VIU = 'Viu'
    WETV = 'WeTV'


class Config:
    def __init__(self, **kwargs: Any):
        self.default_language: str = kwargs.get("default-language") or ""
        self.credentials: dict = kwargs.get("credentials") or {}
        self.directories: dict = kwargs.get("directories") or {}
        self.headers: dict = kwargs.get("headers") or {}
        self.nordvpn: dict = kwargs.get("nordvpn") or {}
        self.proxies: dict = kwargs.get("proxies") or {}

    @classmethod
    def from_toml(cls, path: Path) -> Config:
        if not path.exists():
            raise FileNotFoundError(f"Config file path ({path}) was not found")
        if not path.is_file():
            raise FileNotFoundError(
                f"Config file path ({path}) is not to a file.")
        return cls(**rtoml.load(path))


class Directories:
    def __init__(self) -> None:
        self.package_root = Path(__file__).resolve().parent.parent
        self.configuration = self.package_root / 'configs'
        self.downloads = self.package_root / 'downloads'
        self.cookies = self.package_root / 'cookies'
        self.logs = self.package_root / 'logs'


class Filenames:
    def __init__(self) -> None:
        self.log = directories.logs / "{app_name}_{log_time}.log"
        self.config = directories.configuration / "{service}.toml"
        self.root_config: Path = directories.package_root / "user_config.toml"


def mergeDictsOverwriteEmpty(d1, d2):
    res = d2.copy()
    for k, v in d1.items():
        if k not in d2 or d2[k] == '':
            res[k] = v
    return res


directories = Directories()
filenames = Filenames()

config = Config.from_toml(filenames.root_config)
if not config.directories.get('cookies'):
    config.directories['cookies'] = directories.cookies
if not config.directories.get('downloads'):
    config.directories['downloads'] = directories.downloads
config.directories['logs'] = directories.logs
credentials = config.credentials
user_agent = config.headers['User-Agent']
