from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

app = Flask(__name__)

os.environ['CUDA_VISIBLE_DEVICES'] = '2'
MODEL_NAME = 'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

MAX_CONTEXT_LENGTH = model.config.max_position_embeddings
print("Max context length:", MAX_CONTEXT_LENGTH)
ROOM_FOR_RESPONSE = 512

model = model.half().cuda()


@app.route('/generate', methods=['POST'])
def generate():
    content = request.json
    inp = content.get("text", "")
    input_ids = tokenizer.encode(inp, return_tensors="pt").cuda()
    print("Context length is currently", input_ids.shape[1], "tokens")

    if input_ids.shape[1] > (MAX_CONTEXT_LENGTH - ROOM_FOR_RESPONSE):
        print('Context length is too long. Truncating')
        input_ids = input_ids[:, -(MAX_CONTEXT_LENGTH + ROOM_FOR_RESPONSE)]

    input_ids = input_ids.cuda()

    with torch.cuda.amp.autocast():
        output = model.generate(input_ids, max_length=2048,
                                do_sample=True, early_stopping=True,
                                eos_token_id = model.config.eos_token_id,
                                num_return_sequences=1)
        output = output.cpu()
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=False)

    return jsonify({'text': decoded_output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
