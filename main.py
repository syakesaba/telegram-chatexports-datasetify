import asyncio
import json
import csv
from typing import List
from collections.abc import AsyncGenerator

from data_models import Chat, Message

TTL_REPLY = 1  # replies
TTL_SECONDS = 60 * 60 * 12  # hours
RESULT_JSON_FILE = "result.json"
MAX_CONTEXT_MESSAGE = 10  # user sends + 1 model answers


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


async def recurse_messsages(
    chat: Chat, model_index: List[int]
) -> AsyncGenerator[List[Message], None]:  # AsyncGenerator[YieldType, SendType]
    # model_messageごとにcontextが作成される
    consumed_message_id = []
    for idx in reversed(model_index):
        message = chat.messages[idx]  # answer
        if message.id in consumed_message_id:
            # すでに評価済みのmodel_messageはとばす。
            continue
        consumed_message_id.append(message.id)
        context = [
            message,
        ]
        answer_date_unixtime = int(message.date_unixtime)  # UNIX EPOCH (seconds)
        i = 1
        is_turned = False
        while len(context) < MAX_CONTEXT_MESSAGE:
            # コンテキストが最大メッセージ保有数に達するまでループ
            next_idx = idx - i
            if next_idx <= 0:
                # チャットの最初のメッセージに到達した場合、次のメッセージを取得できないのでcontextは終了
                break
            next_message = chat.messages[next_idx]
            if answer_date_unixtime - int(next_message.date_unixtime) > TTL_SECONDS:
                # 直前のメッセージが回答よりもかなり前のメッセージの場合、contextは終了
                break
            if next_message.from_id == message.from_id:
                # 直前のメッセージと送信元IDが同じ場合、連続したメッセージとして纏めるためにcontextに連結
                context.append(next_message)
                consumed_message_id.append(next_message.id)
            else:
                # 直前のメッセージと送信元IDが異なる場合
                if is_turned:
                    # ターンが終わったコンテキストなので終了
                    break
                # ターンがまだ変わっていないコンテキストはターンを切り替え、次のメッセージへ
                context.append(next_message)
                consumed_message_id.append(next_message.id)
                is_turned = True
            message = next_message
            i = i + 1
        yield context


async def merge_context(
    chat: Chat, contexts: List[List[Message]]
) -> AsyncGenerator[List[List[str]], None]:
    model_id = "user" + str(chat.id)
    for context in contexts:
        q = ""
        a = ""
        for msg in [message for message in context if message.from_id != model_id]:
            q += await get_textized_text_entities(msg)
        for msg in [message for message in context if message.from_id == model_id]:
            a += await get_textized_text_entities(msg)
        yield [q, a]


async def get_textized_text_entities(message: Message):
    return "\n".join([text_entity.text for text_entity in message.text_entities])


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
    contexts = reversed(
        [
            context
            async for context in recurse_messsages(chat=chat, model_index=model_index)
        ]
    )
    qa = [qa async for qa in merge_context(chat=chat, contexts=contexts)]
    with open("output.csv", "w") as f:
        wf = csv.writer(
            f,
        )
        wf.writerow(["question", "answer"])
        wf.writerows(qa)


if __name__ == "__main__":
    asyncio.run(main(file_name=RESULT_JSON_FILE))
