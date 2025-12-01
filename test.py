from openai import OpenAI
import json
import requests


client = OpenAI(base_url="http://192.168.1.55:19990/v1", api_key='foo')

def get_my_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data["ip"]


tool_functions = {"get_my_ip": get_my_ip}

tools = [{
    "type": "function",
    "function": {
        "name": "get_my_ip",
        "description": "Get the current computer ip address",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }
}]

response = client.chat.completions.create(
    model=client.models.list().data[0].id,
    messages=[{"role": "user", "content": "What is my ip address?"}],
    tools=tools,
    tool_choice="auto"
)

tool_call = response.choices[0].message.tool_calls[0].function
print(f"Function called: {tool_call.name}")
print(f"Arguments: {tool_call.arguments}")
print(f"Result: {tool_functions[tool_call.name](**json.loads(tool_call.arguments))}")