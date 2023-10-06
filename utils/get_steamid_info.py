import requests
from models.models import SteamidData

def get_steamid_info(steamid):
    url = f"https://api.steamcmd.net/v1/info/{steamid}"

    response = requests.get(
        url,
        headers={"Accept":"application/json"}
    ).json()
        
    parsed_data = {
        "name" : response["data"][steamid]["common"]["name"],
        "buildid" : response["data"][steamid]["depots"]["branches"]["public"]["buildid"]
    }
    return parsed_data