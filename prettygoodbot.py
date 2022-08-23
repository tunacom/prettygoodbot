import datetime
import discord
import json
import os
import random

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
ICONS_DIR = os.path.join(os.path.dirname(__file__), 'icons')
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'discord_token')


def get_name_and_icon():
    """Return the configured server name and icon for this day of the week."""
    config = json.load(open(CONFIG_PATH))
    day = str(datetime.datetime.today().weekday())

    if day in config:
        return config[day]['name'], config[day]['icon']

    default = config['default']
    entry = random.choice(default)
    return entry['name'], entry['icon']


class PrettyGoodClient(discord.Client):
    """Client for the pretty good bot."""

    async def on_ready(self):
        guilds = self.fetch_guilds()
        async for guild in guilds:
            # TODO(tuna): discord.py contains a type check that breaks if the
            # server has no verification level set. Explicitly set one to work
            # around it. Remove this once it's fixed upstream.
            verification_level = guild.verification_level
            if verification_level is None:
                verification_level = discord.VerificationLevel.none

            name, icon = get_name_and_icon()
            icon_data = open(os.path.join(ICONS_DIR, icon), 'rb').read()
            await guild.edit(name=name,
                             icon=icon_data,
                             verification_level=verification_level)

        await self.close()


def main():
    """Run the client."""
    with open(TOKEN_PATH) as handle:
        token = handle.read().strip()

    intents = discord.Intents.default()
    client = PrettyGoodClient(intents=intents)
    client.run(token)


if __name__ == '__main__':
    main()
