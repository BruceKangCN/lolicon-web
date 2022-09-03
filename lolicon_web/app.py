#!/bin/env python3

from dataclasses import dataclass
import dataclasses
from typing import Optional, Sequence
from typing_extensions import Self
from aiohttp import web
import aiohttp


@dataclass
class ApiConfig:
    r18: int
    num: int
    size: Sequence[str]
    proxy: str
    uid: Optional[int]
    tags: Optional[Sequence[str]]
    dateAfter: Optional[int]
    dateBefore: Optional[int]

    @classmethod
    def default(cls) -> Self:
        return ApiConfig(
            r18=1,
            num=1,
            size=["original"],
            proxy="i.pixiv.re",
            uid=None,
            tags=None,
            dateAfter=None,
            dateBefore=None,
        )


@dataclass
class Config:
    api_url: str
    size: str
    params: ApiConfig

    @classmethod
    def default(cls) -> Self:
        return Config(
            api_url="https://api.lolicon.app/setu/v2",
            size="original",
            params=ApiConfig.default(),
        )


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
    app["config"] = Config.default()
    web.run_app(app)
