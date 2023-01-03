#!/bin/env python3

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence
from typing_extensions import Self
from aiohttp import web
import toml

from route import routes


@dataclass
class ApiConfig:
    r18: int = 1
    num: int = 1
    size: Sequence[str] = field(default_factory=lambda: ["original"])
    proxy: str = "i.pixiv.re"
    uid: Optional[int] = None
    tag: Optional[Sequence[str]] = None
    dateAfter: Optional[int] = None
    dateBefore: Optional[int] = None

    def update(self, new: dict) -> Self:
        for k, v in new.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self


@dataclass
class Config:
    api_url: str = "https://api.lolicon.app/setu/v2"
    size: str = "original"
    params: ApiConfig = ApiConfig()

    def update(self, new: dict) -> Self:
        for k, v in new.items():
            if k == "api_url":
                self.api_url = v
            elif k == "size":
                self.size = v
            elif k == "params":
                self.params.update(v)
        return self


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    app["config"] = Config()

    p = Path("/etc") / "lolicon" / "config.toml"
    if p.exists():
        app["config"].update(toml.load(p))

    web.run_app(app)
