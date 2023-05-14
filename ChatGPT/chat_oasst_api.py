import requests
import json
import colorama

SERVER_IP = '10.0.0.18'
URL  ='http://' + SERVER_IP + ':5000/generate'

USERTOKEN = '<|prompter|>'
ENDTOKEN = '<|endoftext|>'
ASSISTANTTOKEN = '<|assistant|>'

MAX_CONTEXT_LENGTH = model.config.max_position_embeddings
print("Max context length:", MAX_CONTEXT_LENGTH)
ROOM_FOR_RESPONSE = 512

def prompt(inp):
    data = {"text": inp}
    headers = {"Content-type": 'application/json', 'Accept': 'text/plain'}
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    return response.json()['generated_text']

history = ''
while True:
    inp = input(">>>")
    context = history + USERTOKEN + inp + ENDTOKEN + ASSISTANTTOKEN
    output = prompt(context)
    history = output
    just_latest_asst_output = output.split(ASSISTANTTOKEN)[-1]
    print(colorama.For.GREEN + output + colorama.Style.RESET_ALL)