from imessage_reader import fetch_data
import json
import openai
import os
from gtp_message_context import GtpMessageContext
from time import sleep
from messages_reader import Message
from collections import defaultdict

config = json.load(open("config.json"))


class ChatBot:
    def __init__(self, target, system_message):
        openai.api_key = config["OPENAI_API_KEY"]
        self.target = target
        self.system_message = system_message

    def send_message(self, message):
        print(f"Sending message to {self.target} with message: {message}")
        self.context.add_assistant_message(message)
        if not config["TEST_MODE"]:
            os.system(f'osascript sendMessage.applescript {self.target} "{message}"')

    def generate_response(self):
        print(self.context)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context.to_json(),
        )
        return response.choices[0].message.content.replace("'", "").replace('"', "")

    def build_context(self, depth, messages):
        self.context = GtpMessageContext(
            system_message=self.system_message, maxlen=depth
        )
        # Docs state that the messages are sorted by order but wasn't the case for me
        # Sorting them manually here works.
        messages = [x for x in messages if x.user_id == self.target]
        messages.sort(key=lambda x: x.date)

        for message in messages[::-1]:
            if message.is_from_me:
                self.context.add_assistant_message(message.message, prepend=True)
            else:
                self.context.add_user_message(message.message, prepend=True)

            if self.context.is_full:
                print("Context built: \n", self.context)
                return


class MessageDatabase:
    def __init__(self):
        self.fd = fetch_data.FetchData()
        self.last_seen_messages = self.load_messages()

    def load_messages(self):
        return {
            Message(*x)
            for x in self.fd.get_messages()
            if x[0] in config["RECIPIENTS"] and x[5] == 0
        }

    def get_all_messages(self):
        # replace with self.last_seen_messages
        return [Message(*x) for x in self.fd.get_messages()]

    def get_new_messages(self):
        temp = self.load_messages()
        newMessage = temp - self.last_seen_messages
        self.last_seen_messages = temp
        return newMessage


def main():
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
