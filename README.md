# Discord Bot - Game Update Notifier
A Discord bot that will notify users when a game server has been updated. This can be helpful for finding out when a game has gone through some updates, and can help people decide to jump back into a game with friends after a hiatus. 
# To Do
- logging
- Discord notification
    - Schedule process to check for updates
    - send notifications upon change
- Move sqlalchemy to async code
    - may need to move away from alembic, if not implement a slight workaround, since it doesn't support an async driver
# Notes
- Valheim dedicated server steamid is 896660
- Example json output from steamcmd api is `pretty_json.json`
- Working with Alembic
    - `alembic revision --autogenerate -m "<some_comment_here>"`
    - `alembic upgrade heads`