import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pika
import traceback, sys
import codecs
import os
tokenizer = AutoTokenizer.from_pretrained("MovieDescriptionGen")
model = AutoModelForCausalLM.from_pretrained("MovieDescriptionGen")
amqp_url = os.environ['AMQP_URL']
conn_params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue="first-queue")
channel2 = connection.channel()
channel2.queue_declare(queue="second-queue")

print("waiting for messages, To exit press CTRL+C")

def callback(ch, method, properties, body):
    input = codecs.decode(body, 'UTF-8')
    print(input)
    id, in_text = input.split("&")
    text = f"<s>Название: {in_text}\n"
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
    output = str(id) + "&" + generated_text
    print(output)
    channel2.basic_publish(exchange='', routing_key='second-queue', body=output)

channel.basic_consume(on_message_callback=callback, queue="first-queue")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)

