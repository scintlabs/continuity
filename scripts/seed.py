import asyncio
import sys

import aiohttp

ingest_url = "http://localhost:8000/ingest"


async def seed_file(path):
    text = open(path).read()
    async with aiohttp.ClientSession() as session:
        async with session.post(ingest_url, json={"text": text, "type": "doc"}) as resp:
            result = await resp.json()
            print(path, result)


async def main(paths):
    await asyncio.gather(*(seed_file(p) for p in paths))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
