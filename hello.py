import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model:
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client = provider,
)
# Cofigrations
run_config = RunConfig(
    model = model,
    model_provider = provider,
    tracing_disabled = True
)

# Agent:
agent1 = Agent(
    instructions="You are a helpful assistant.",
    name="UMT Support Assistant"
)

# Runner:
# result = Runner.run_sync(
#     agent1,
#     input = "What is capital of Pakistan?",
#     run_config = run_config,
# )
# print(result.final_output)

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent1,
        input = message.content,
        run_config = run_config,
    )
    await cl.Message(content=result.final_output).send()

# import os
# import chainlit as cl
# from dotenv import load_dotenv, find_dotenv
# from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

# load_dotenv(find_dotenv())

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider,
# )

# run_config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True
# )

# agent1 = Agent(
#     instructions="You are a helpful assistant.",
#     name="UMT Support Assistant"
# )

# @cl.on_message
# async def handle_message(message: cl.Message):
#     result = await Runner.run(
#         agent1,
#         input=message.content,
#         run_config=run_config,
#     )
#     await cl.Message(content=result.final_output).send() 