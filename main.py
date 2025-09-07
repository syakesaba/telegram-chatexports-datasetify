import asyncio
import json
from typing import List
import duckdb

from data_models import Chat, Message

TTL_REPLY = 1  # replies
TTL_SECONDS = 60 * 60 * 24  # 24 hours
RESULT_JSON_FILE = "result.json"
MAX_CONTEXT_MESSAGE = 4  # 3 user sends + 1 model answers


async def get_sorted_messages(chat: Chat) -> List[Message]:
    return sorted(chat.messages, key=lambda x: int(x.date_unixtime))


async def get_text_messages(chat: Chat) -> List[Message]:
    messages = [
        message
        for message in chat.messages
        if message.media_type is None
        and message.photo is None
        and message.text_entities != []
    ]
    return messages


async def get_index_of_model_chat(chat: Chat) -> List[int]:
    return [
        i
        for i, message in enumerate(chat.messages)
        if message.from_id == "user" + str(chat.id)
    ]


async def recurse_messsages(chat: Chat, model_index: List[int]) -> List[Message]:
    for idx in model_index:
        model_message = chat.messages[idx]
        context = []
        i = 0
        message_idx = idx
        while len(context) < MAX_MESSAGES and message_idx <= 0:
            chat.messages[idx - i]


async def get_textized_text_entities(message: Message):
    return " ".join([text_entity.text for text_entity in message.text_entities])


async def main(file_name: str) -> None:
    with open(file_name, "r", encoding="utf-8") as f:
        export_data = json.load(f)
    chat = Chat.model_validate(export_data)
    print(
        f"Total Messages: {len(chat.messages)}",
        flush=True,
    )
    chat.messages = await get_sorted_messages(chat)
    chat.messages = await get_text_messages(chat)
    print(f"Text Messages: {len(chat.messages)}", flush=True)
    model_index = await get_index_of_model_chat(chat)
    print(f"Model Messages: {len(model_index)}", flush=True)
    print(model_index, flush=True)
    # for message in chat.messages:
    #     print("============")
    #     print(await get_textized_text_entities(message))


if __name__ == "__main__":
    asyncio.run(main(file_name=RESULT_JSON_FILE))
