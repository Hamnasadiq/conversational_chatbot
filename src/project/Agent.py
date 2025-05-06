from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, Tool
from dotenv import load_dotenv
from agents.run import RunConfig
from tavily import TavilyClient
from agents.tool import function_tool
import os, asyncio
import nest_asyncio
nest_asyncio.apply()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@function_tool
def web_search(query: str) -> str:

    """Use Tavily to perform a web search."""
    result = tavily_client.search(query)
    print(f"Tool Called: web_search with query='{query}'")
    return result['results'][0]['content'] if result['results'] else "No results found."


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
    conversation = ""
    if history:
        for message in history:
            role = message["role"]
            content = message["content"]
            conversation += f"{role}: {content}\n"
    conversation += f"user: {user_query}"

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Use the conversation history to answer questions accurately.",
        model=model,
        tools=[web_search]
        
    )

    result = await Runner.run(starting_agent=agent, input=conversation)
    return result.final_output
