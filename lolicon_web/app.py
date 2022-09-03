#!/bin/env python3

from dataclasses import dataclass, field
import dataclasses
from pathlib import Path
from typing import Optional, Sequence
from typing_extensions import Self
from aiohttp import web
import aiohttp
import toml


@dataclass
class ApiConfig:
    r18: int = 1
    num: int = 1
    size: Sequence[str] = field(default_factory=lambda: ["original"])
    proxy: str = "i.pixiv.re"
    uid: Optional[int] = None
    tags: Optional[Sequence[str]] = None
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


async def get_setu(req: web.Request) -> web.Response:
    config = req.app["config"]
    async with aiohttp.ClientSession() as session:
        data = dataclasses.asdict(config.params)
        async with session.post(config.api_url, json=data) as resp:
            data = await resp.json()
            if (msg := data["error"]) != "":
                return web.Response(text=msg)
            url = data["data"][0]["urls"][config.size]
        async with session.get(url) as resp:
            img = await resp.read()
        return web.Response(body=img, content_type=resp.content_type)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/setu", get_setu),
    ])
    app["config"] = Config()

    p = Path("/etc") / "lolicon" / "config.toml"
    if p.exists():
        app["config"].update(toml.load(p))

    web.run_app(app)
