from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from dotenv import load_dotenv
import os, asyncio

load_dotenv()
set_tracing_disabled(True)

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider,
)

async def MyAgent(user_query, history=None):
    # Format the history into a single string for the agent
    conversation = ""
    if history:
        for message in history:
            role = message["role"]
            content = message["content"]
            conversation += f"{role}: {content}\n"
    
    # Add the current user query to the conversation
    conversation += f"user: {user_query}"

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Use the conversation history to answer questions accurately.",
        model=model,
    )

    # Pass the concatenated conversation string to the Runner
    result = await Runner.run(starting_agent=agent, input=conversation)
    return result.final_output