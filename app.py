import os

import discord

from discord.ext import commands
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.chains import (
    ConversationChain,
)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = False
intents.typing = False

bot = commands.Bot(command_prefix="/", intents=intents)

CHAIN_CACHE = {}


@bot.event
async def on_ready():
    start_message = f"Logged in as {bot.user} (ID: {bot.user.id})"
    print(f"{start_message}\n{('-' * len(start_message))}")

    # try:
    #     after_date = None
    #     if self.days:
    #         after_date = dt.datetime.utcnow() - dt.timedelta(days=self.days)

    #     channel = bot.get_channel(int(self.channel))
    #     async for msg in channel.history(after=after_date):  # type: ignore
    #         messages.append(msg)

    #     await bot.close()
    # except Exception as e:
    #     logger.error(f"Error fetching messages: {e}")
    #     await bot.close()


@bot.command()
async def chat(ctx, msg):
    """Execute query, keeping track of chat history."""

    user = ctx.author
    if user not in CHAIN_CACHE:
        CHAIN_CACHE[user] = make_chain(user)

    chain = CHAIN_CACHE[user]
    response = chain.run(msg)

    await ctx.send(response)


def make_chain(user, model="llama2"):
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            f"Greet {user} and make a joke about their name, then answer any questions."
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    llm = Ollama(model=model)
    memory = ConversationBufferMemory(llm=llm, return_messages=True)

    return ConversationChain(llm=llm, prompt=prompt_template, memory=memory)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
