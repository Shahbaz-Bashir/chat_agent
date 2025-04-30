import chainlit as cl

from agents import Agent, Runner, OpenAIChatCompletionsModel,AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client= AsyncOpenAI(

    api_key=os.getenv("GEMINI_API_KEY"),
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)
agent = Agent(
    name = "assistant",
    instructions = "You will response my  query",
model=model
)

@cl.on_chat_start
async def start():
    cl.user_session.set('history',[])

@cl.on_message
async def main(message:cl.Message):
    msg = cl.Message(
        content ="",
    )
    await msg.send()
    f = open("history.txt", "a")
    f.write("User: " + message.content + "\n")
    history = cl.user_session.get("history")
    history.append({'role': 'user', 'content': message.content})
    
    ai_reponse =  Runner.run_streamed(agent, history)
    async for event in ai_reponse.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            raw_txt = event.data.delta
            await msg.stream_token(raw_txt)




response = Runner.run_sync(
    starting_agent=agent,
    input="tell me about lahore"
    
)
print( response.final_output)