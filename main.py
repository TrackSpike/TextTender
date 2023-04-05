from imessage_reader import fetch_data
import json
import openai
import os
from gtp_message_context import GtpMessageContext
from time import sleep
from messages_reader import Message

config = json.load(open("config.json"))


class ChatBot:
    def __init__(self):
        config = json.load(open("config.json"))
        openai.api_key = config["OPENAI_API_KEY"]
        self.fd = fetch_data.FetchData()

    def send_message(self, target, message):
        print(f"Sending message to {target} with message: {message}")
        self.context.add_assistant_message(message)
        if not config["TEST_MODE"]:
            os.system(f'osascript sendMessage.applescript {target} "{message}"')

    def generate_response(self):
        print(self.context)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context.to_json(),
        )
        return response.choices[0].message.content.replace("'", "").replace('"', "")

    def build_context(self, depth):
        self.context = GtpMessageContext(
            system_message=config["SYSTEM_MESSAGE"], maxlen=depth
        )
        # Docs state that the messages are sorted by order but wasn't the case for me
        # Sorting them manually here works.
        messages = [Message(*x) for x in self.fd.get_messages()]
        messages = [x for x in messages if x.user_id == config["RECIPIENT_NUMBER"]]
        messages.sort(key=lambda x: x.date)

        for message in messages[::-1]:
            if message.is_from_me:
                self.context.add_assistant_message(message.message, prepend=True)
            else:
                self.context.add_user_message(message.message, prepend=True)

            if self.context.is_full:
                print("Context built: \n", self.context)
                return

    # Going to rewite
    def get_new_message(self):
        messages = [Message(*x) for x in self.fd.get_messages()]
        messages = [x for x in messages if x.user_id == config["RECIPIENT_NUMBER"]]
        messages.sort(key=lambda x: x.date)
        if messages[-1].is_from_me == False:
            return messages[-1]
        else:
            return None


def main():
    chatBot = ChatBot()

    while True:
        if new_message := chatBot.get_new_message():
            print("New messages from target")
            chatBot.build_context(config["CONTEXT_DEPTH"])
            response = chatBot.generate_response()
            # Send your automated message!
            chatBot.send_message(config["RECIPIENT_NUMBER"], response)
        else:
            print("No new messages from target")

        sleep(10)


if __name__ == "__main__":
    main()
