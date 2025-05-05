import chainlit as cl
from Agent import MyAgent
import asyncio

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("history", [])
    await cl.Message("Hello! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    
    user_query = message.content
    history.append({"role": "user", "content": user_query})

    response = await MyAgent(user_query, history=history)
    history.append({"role": "Assistant", "content": response})

    cl.user_session.set("history", history)

    await cl.Message(
        content=f"{response}",
    ).send()