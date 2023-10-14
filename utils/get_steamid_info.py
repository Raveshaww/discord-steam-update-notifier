import aiohttp
import asyncio


async def get_steamid_info(steamid):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.steamcmd.net/v1/info/{steamid}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                parsed_data = {
                    "name": data["data"][steamid]["common"]["name"],
                    "buildid": data["data"][steamid]["depots"]["branches"]["public"]["buildid"]
                }
                return parsed_data
            else:
                return None

# Seperate function for clarity


async def mass_get_steamid_info(steamids):
    async with aiohttp.ClientSession() as session:
        async def fetch_steamid_info(steamid):
            url = f"https://api.steamcmd.net/v1/info/{steamid}"
            async with session.get(url, headers={"Accept": "application/json"}) as response:
                if response.status == 200:
                    data = await response.json()
                    parsed_data = {
                        "steamid": steamid,
                        "name": data["data"][steamid]["common"]["name"],
                        "buildid": data["data"][steamid]["depots"]["branches"]["public"]["buildid"]
                    }
                    return parsed_data
                else:
                    return None

        # Use asyncio.gather to make concurrent requests
        results = await asyncio.gather(*[fetch_steamid_info(steamid) for steamid in steamids])

        return results
