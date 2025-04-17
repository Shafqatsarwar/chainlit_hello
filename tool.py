import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from openai.types.responses import ResponseTextDeltaEvent
from agents.tool import function_tool

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    # Option 1: Raise an error immediately
    raise ValueError("GEMINI_API_KEY environment variable not set or found.")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/", # Still needs verification
)
# Model:
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client = provider,
)
# Cofigrations
run_config = RunConfig(
    model = model,
    model_provider = provider,
    tracing_disabled = True
)
@function_tool("get_weather")
def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  # Example logic
  return f"The weather in {location} is 22 degrees {unit}."

@function_tool("piaic_student_finder")
def student_finder(student_roll: int) -> str:
  """
  find the UMT student based on the roll number
  """
  data = {1: "Qasim",
          2: "Sir Zia",
          3: "Daniyal",
          4: "Khan",
          5: "Sarwar",
          6: "Lion",
          7: "Azlan"}

  return data.get(student_roll, "Not Found")

# Agent:
agent1 = Agent(
    instructions="You are a helpful assistant. Use get weather tool to provide weather information for any location. Use piaic_student_finder tool to find the UMT student based on the roll number.",
    name="UMT Support Assistant",
    tools=[get_weather, student_finder] # Add the function tool to the agent
)
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I'm the UMT Lahore Support Agent. How can I assist you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    msg= cl.Message(content = "")
    await msg.send()

    # Standard interface
    history.append({"role": "user", "content": message.content})
    result = Runner.run_streamed(
        agent1,
        input = history,
        run_config = run_config,
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    # await cl.Message(content=result.final_output).send()
