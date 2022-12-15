import torch

def generateDescription(prompt: str, model, tokenizer) -> str:
    """Генерация описания по названию prompt полученному от бота"""
    text = f"<s>Название: {prompt}\n"
    input_ids = tokenizer.encode(text, return_tensors="pt")
    model.eval()
    with torch.no_grad():
        out = model.generate(input_ids, 
                            do_sample=True,
                            num_beams=2,
                            temperature=1.5,
                            top_p=0.9,
                            max_length=512
                            )
    generated_text = list(map(tokenizer.decode, out))[0]
    generated_text = generated_text.replace("<s>", "")
    generated_text = generated_text.replace("<\s>","")
    return generated_text