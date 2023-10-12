# Discord Bot - Game Update Notifier
A Discord bot that will notify users when a game server has been updated. This can be helpful for finding out when a game has gone through some updates, and can help people decide to jump back into a game with friends after a hiatus. 
# To Do
- Change get_steamid_info to accept several steamids
    - This is to allow us to utilize a single request session when we want to run the scheduled task to check if something has updated
    - Alternatively, have this be its own function in get_steamid_info.py for the sake of clarity
- Look into moving everything, steamcmd.py and the upcoming background task, into cog(s)
- logging
- Add error handling for the database connection
- Discord notification
    - Schedule process to check for updates
    - send notifications upon change
# Notes
- Valheim dedicated server steamid is 896660
- Example json output from steamcmd api is `pretty_json.json`
- Working with Alembic
    - `alembic revision --autogenerate -m "<some_comment_here>"`
    - `alembic upgrade heads`