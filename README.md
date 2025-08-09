# Discord Bot - Game Update Notifier
A Discord bot that will notify users when a game server has been updated. This can be helpful for finding out when a game has gone through some updates, and can help people decide to jump back into a game with friends after a hiatus. 
## Requirements
You will need the following in order to run this bot:
- Discord API token.
- The ability to add a bot to the Discord server you would like to add it to.
- A PostgreSQL server
    - A database and user account used exclusively for this bot is also required.
- Docker installed on your system
    - Alternatively, you can run this code on a Linux system running Python 3.10.13. 
## How to Run the Bot:
The easiest way to run this bot would be via a Docker container. As of the time of writing, this bot is still being tested and frequently changed. As a result, we will build the docker image from this repo rather than pulling it from Docker Hub. Please note that you will need a PostgreSQL server, user, and database already made, as well as a Discord . This short guide will not cover these topics, as it is squarely focused on the bot itself.
- Clone this git repo to a directory of your choosing:
```
git clone git@github.com:Raveshaww/discord-steam-update-notifier.git
```
- Navigate into the newly created directory:
```
cd discord-steam-update-notifier
```
- Build the container image
```
docker build -t discord-steam-update-notifier .
```
- Run the container image
``` 
docker run -d -e DISCORD_TOKEN=<your_token_here> \
    -e POSTGRES_USERNAME=<your_postgres_user_here> \
    -e POSTGRES_PASSWORD=<your_postgres_user_pass_here> \
    -e POSTGRES_HOST=<your_postgress_hostname:port_here> \
    -e POSTGRES_DB=<your_postgres_database_name_here> \
    --name discord-steam-update-notifier \
    discord-steam-update-notifier
```
## How to Use the Bot
- The bot implements four commands:
    - `!steamid set_channel`
        - This command will set the channel this was used in as the channel to be used for update notifications.
    - `!steamid add <steamid_here>`
        - This command will inform the bot to track a specific for the Discord server.
        - Example usage:
            - `!steamid add 435150`
    - `!steamid remove <steamid_here>`
        - This command will inform the bot to stop tracking a specific Steamid for the Discord server
        - Example usage:
            - `!steamid add 435150`
    - `!steamid list`
        - This command will list all pieces of software currently tracked for the Discord server.
## To Be Implemented:
- Improved output aesthetics
- Logging
- Tests
- Move to Slash commands
## Maybe Implemented Someday:
- Start tracking by name rather than Steamid.
- "Hosted" solution.
    - This may be something I look into doing when and if I am ever in the financial position to do so.
# FAQs
- How do I find the Steamid of a specific piece of software on Steam?
    - The easiest way to find a Steamid for something on Steam is via [Steamdb](https://steamdb.info/)
- Why Steamids and not the human readable names? 
    - In short, I simply found it to be the least confusing way to go about picking the correct software to be tracked. There are often times many Steamids that have similar names, so it's easy to select the wrong Steamid. 