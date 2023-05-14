from transformers import AutoTokenizer, AutoModelForCasualLM
import torch
import os

MODEL_NAME = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCasualLM.from_pretrained(MODEL_NAME)

model = model.half().cuda()

inp = "What colour is sky?"

input_ids = tokenizer.encode(inp, return_tensor='pt').cuda()

with torch.cuda.amp.autocast():
    output = model.generate(input_ids, max_length=256, 
                            do_sample=True, early_stopping=True,
                            eos_token_id = model.config.eos_token_id,
                            num_return_sequences=1, temperature=0.9,
                            top_k=50, top_p=0.95)
    
output = output.cpu()

output_text = tokenizer.decode(output[0], skip_special_tokens=False)
print(output_text)