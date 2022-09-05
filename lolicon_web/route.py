from aiohttp import web
import aiohttp
import dataclasses

routes = web.RouteTableDef()


@routes.get("/setu")
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
