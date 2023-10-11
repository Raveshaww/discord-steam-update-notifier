import aiohttp

## MODIFY ME TO ACCEPT A LIST OF INPUTS
async def get_steamid_info(steamid):
    url = f"https://api.steamcmd.net/v1/info/{steamid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                parsed_data = {
                    "name" : data["data"][steamid]["common"]["name"],
                    "buildid" : data["data"][steamid]["depots"]["branches"]["public"]["buildid"]
                }
                return parsed_data