import bot.db_client
import bot.tg_client
import time

def check_and_get_msg_chat_id(update):
    if "message" in update:
        msg = update["message"]
    else:
        return None, None
    chat = msg.get("chat") if isinstance(msg, dict) else None
    chat_id = chat.get("id") if isinstance(chat, dict) else None
    return msg, chat_id

def main() -> None:
    next_update_offset = 0
    try:
        while True:
            updates = bot.tg_client.getUpdates(next_update_offset)
            bot.db_client.persist_updates(updates)
            for update in updates:
                msg, chat_id = check_and_get_msg_chat_id(update)
                text = None
                if msg is not None:
                    text = msg.get("text")
                if chat_id is not None:
                    if text:
                        bot.tg_client.sendMessage(chat_id=chat_id, text=text)
                    else:
                        bot.tg_client.sendMessage(chat_id=chat_id, text="Отправляй мне только текстовые сообщения")
                print(".", end="", flush=True)
                next_update_offset = max(next_update_offset, update["update_id"] + 1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == "__main__":
    main()