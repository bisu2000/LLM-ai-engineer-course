import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"
prompt="suggest a name for my clothing fashion brand "
# system

message_system = {
    "role": "system",
    "content": "you are a brand manager who suggest name for my clothing fashion company, name should be in one word,please suggest a perfect eye catchy name that reflects my brand work,one word only"

}
# message me role and content
message={
    "role": role,
    "content": prompt
}

messages=[message_system,message]

#temperature by default is 0 meaning safe , range [0,2]
response=client.chat.completions.create(model=model, messages=messages,temperature=1)

#print(response)

print("#######################################")

answer=response.choices[0].message.content
print(answer)

