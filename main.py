import json
import openai
from time import sleep
from chat_bot import ChatBot
from message_database import MessageDatabase


def main():
    config = json.load(open("config.json"))
    openai.api_key = config["OPENAI_API_KEY"]
    messageDb = MessageDatabase()
    chatBots = {}

    while True:
        if new_messages := messageDb.get_new_messages():
            print(new_messages)
            targets = set(x.user_id for x in new_messages)
            for target in targets:
                if target not in chatBots:
                    chatBots[target] = ChatBot(
                        target, config["RECIPIENTS"][target]["SYSTEM_MESSAGE"]
                    )
                chatBot = chatBots[target]
                # rebuilding every time... could be optimized
                chatBot.build_context(
                    config["CONTEXT_DEPTH"], messageDb.get_all_messages()
                )
                # Send your automated message!
                chatBot.send_message(chatBot.generate_response())
        else:
            print("No new messages from target")

        sleep(10)


if __name__ == "__main__":
    main()
