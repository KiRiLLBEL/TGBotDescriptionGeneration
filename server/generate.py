import torch

def generateDescription(prompt: str, model, tokenizer, DEVICE) -> str:
    """Генерация описания по названию prompt полученному от бота"""
    text = f"<s>Название: {prompt}\n"
    input = tokenizer(text, padding=True, truncation=True, max_length=256, return_tensors="pt")
    out = model.generate(
        input['input_ids'], 
        do_sample=True,
        temperature=0.8,
        top_k=30,
        top_p=0.85,
        max_length=256,
        min_length=100,
        repetition_penalty=1.1,
        use_cache=True,
        attention_mask=input['attention_mask']
    ).cpu()
    generated_text = tokenizer.batch_decode(out, skip_special_tokens=True)[0]
    return generated_text