import discord
import requests
from config import DISCORD_TOKEN_API

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

RASA_URL = 'http://localhost:5005/webhooks/rest/webhook'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Send the user's message to Rasa
    user_message = {"sender": str(message.author.id), "message": message.content}
    response = requests.post(RASA_URL, json=user_message)

    if response.status_code == 200:
        rasa_responses = response.json()
        for res in rasa_responses:
            await message.channel.send(res.get("text", "I didn't understand that."))
    else:
        await message.channel.send("I'm having trouble connecting to the server.")


DISCORD_TOKEN = DISCORD_TOKEN_API
client.run(DISCORD_TOKEN)