# Model

## Dataset and training

В проекте используется модель [RuGPTLarge3](https://huggingface.co/sberbank-ai/rugpt3large_based_on_gpt2)

dataset: [films.csv](https://disk.yandex.ru/d/w7rPLt7Hz3bGYg)

parser: [parser.ipynb](/training/parser.ipynb)

Generation config:

- do_sample=True
- temperature=0.8
- top_k=30
- top_p=0.85
- repetition_penalty=1.1

Запрос производится в виде: `Название: <Text>`

## Saved model

[Ноутбук](/training/training.ipynb) с обучением модели.

[Ссылка](https://huggingface.co/KiRiLLBEl/MovieDescriptionGen) на обученную модель
