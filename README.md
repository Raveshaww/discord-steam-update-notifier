# Discord Bot - Game Update Notifier
A Discord bot that will notify users when a game server has been updated. This can be helpful for finding out when a game has gone through some updates, and can help people decide to jump back into a game with friends after a hiatus. 
# To Do
- logging
- docs
- dockerfile
- tests
# Notes
- Working with Alembic
    - `alembic revision --autogenerate -m "<some_comment_here>"`
    - `alembic upgrade heads`
- The following environment variables are needed:
    - DISCORD_TOKEN
        - Can be obtained from the Discord Developer Portal
    - sqlalchemy.url
        - Contains the connection string to the postgresql database to be used. Please note that this must use an async driver like asyncpg.
    - alembic.url
        - Contains the connection string to the postgresql database for alembic to use. Unlike the SQLAlchemy url, this must be a sync driver like psycopg.