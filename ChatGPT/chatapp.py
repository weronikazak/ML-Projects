import gradio as gr
import openai

openai.api_key = open('key.txt', 'r').read().strip('\n')

message_history = []

def predict(inp):
    global message_history
    message_history.append({"role": "user", "content": inp})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion['choices'][0]['message']['content']
    print(reply_content)
    message_history.append({"role": "assistant", "content": reply_content})
    response = [(message_history[0]['content'], message_history[i+1]["content"]) for i in range(2, len(message_history)-1, 2)]
    return reply_content

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder='Type you message here').style(container=False)
        txt.submit(predict, txt, chatbot)
        txt.submit(None, None, txt, _js="()=> {''}")

demo.launch()