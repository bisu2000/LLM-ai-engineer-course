import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key missing")

client = Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"

#structure it
from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    email: str
    # Make it optional because the model may return incomplete JSON.
    issue: str


schema=Ticket.model_json_schema()

response_format={
    "type": "json_object"
}


system_prompt = f"""
You are a JSON extraction engine.
Extract the personal information from the customer ticket and output ONLY valid JSON.

Use this schema (fields and types):
{schema}

If a field is missing, still include it in JSON with value null.
"""


message_system = {
    "role":"system",
    "content": system_prompt
}

text="Hello My name is Biswajit. Yesterday I broke up with my girlfriend sheetal I have an iphone which is not working at all. My address is kolkata. My email is abc@gmail.com. My contact number is 82100"
prompt=f"""
This is a customer ticket.please extract the personal information from this.
{text}
"""

# message me role and content 
message = {
    "role":role,
    "content":prompt
}

messages=[message_system,message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)


answer = response.choices[0].message.content
print(answer)


# isko padhte kaise hai
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

# (Optional) debug if model output misses required fields
# print("Parsed JSON:", data_file)



# inko pass kr sakte hai aage!
print(ticket.name)
print(ticket.email)
print(ticket.issue)
