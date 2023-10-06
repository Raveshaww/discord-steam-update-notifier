# Discord Bot - Game Update Notifier
A Discord bot that will notify users when a game server has been updated. This can be helpful for finding out when a game has gone through some updates, and can help people decide to jump back into a game with friends after a hiatus. 
# To Do
- Fix delete "route"
- Change list output to include build id
- Think about multiple tables to reduce duplicate data when additional servers are using the bot
- error handling
- logging
- Discord notification
    - Schedule process to check for updates
    - send notifications upon change
# Notes
- Valheim dedicated server steamid is 896660
- Example json output from steamcmd api is `pretty_json.json`\