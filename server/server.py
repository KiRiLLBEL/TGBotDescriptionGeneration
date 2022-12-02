import asyncio
import logging
import json
import os
import aio_pika
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from generate import generateDescription
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
tokenizer = AutoTokenizer.from_pretrained("MovieDescriptionGen")
model = AutoModelForCausalLM.from_pretrained("MovieDescriptionGen")

logging.basicConfig(level=logging.INFO)

async def main() -> None:
    try:
        connection = await connect(os.environ['AMQP_URL'], channel_number=2,)
    except Exception:
        logging.exception("connection not open")

    channel = await connection.channel()

    exchange = channel.default_exchange

    queue = await channel.declare_queue("rpc_queue", durable=True)

    logging.info(" [x] Awaiting RPC requests")

    async with queue.iterator() as qiterator:
        message: AbstractIncomingMessage
        async for message in qiterator:
            try:
                async with message.process(requeue=True):
                    assert message.reply_to is not None
                    
                    inputJson = message.body.decode("UTF-8")
                    inputMessage = json.loads(inputJson)
                    outputText = generateDescription(inputMessage['text'], model, tokenizer)
                    logging.info("Output text: %r", outputText)
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

            except Exception:
                logging.exception("Processing error for message %r", message)
            try:
                await asyncio.Future()
            finally:
                await connection.close()

if __name__ == "__main__":
    asyncio.run(main())