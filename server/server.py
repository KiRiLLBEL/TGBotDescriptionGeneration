import asyncio
import logging
import json
import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from generate import generateDescription
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage

DEVICE = torch.device("cpu")

logging.basicConfig(level=logging.INFO)

tokenizer = AutoTokenizer.from_pretrained("KiRiLLBEl/MovieDescriptionGen", cache_dir="./model")
model = AutoModelForCausalLM.from_pretrained("KiRiLLBEl/MovieDescriptionGen", cache_dir="./model").to(DEVICE)

async def main() -> None:
    try:
        connection = await connect(os.environ["AMQP_URL"],)
    except Exception:
        logging.exception(" [x] connection not open")

    channel = await connection.channel()

    exchange = channel.default_exchange

    queue = await channel.declare_queue("rpc_queue")

    logging.info(" [x] Awaiting RPC requests")

    async with queue.iterator() as qiterator:
        message: AbstractIncomingMessage
        async for message in qiterator:
            try:
                async with message.process(requeue=False):
                    assert message.reply_to is not None
                    inputJson = message.body.decode("UTF-8")
                    inputMessage = json.loads(inputJson)
                    logging.info(" [x] Message from bot: %r", inputMessage['text'])
                    outputText = generateDescription(inputMessage['text'], model, tokenizer, DEVICE)
                    logging.info(" [x] Output text: %r", outputText)
                    inputMessage['text'] = outputText
                    outputJson = json.dumps(inputMessage)
                    response = outputJson.encode("UTF-8")
                    await exchange.publish(
                        Message(
                            body=response,
                            correlation_id=message.correlation_id,
                        ),
                        routing_key=message.reply_to,
                    )
                    logging.info(" [x] request complete")
            except Exception:
                logging.exception(" [x] Processing error for message %r", message)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(" [x] Server is down")