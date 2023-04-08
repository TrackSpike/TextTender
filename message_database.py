from imessage_reader import fetch_data
from messages_reader import Message
import json


class MessageDatabase:
    def __init__(self):
        self.config = json.load(open("config.json"))
        self.fd = fetch_data.FetchData()
        self.last_seen_messages = self.load_messages()

    def load_messages(self):
        return {
            Message(*x)
            for x in self.fd.get_messages()
            if x[0] in self.config["RECIPIENTS"] and x[5] == 0
        }

    def get_all_messages(self):
        # replace with self.last_seen_messages
        return [Message(*x) for x in self.fd.get_messages()]

    def get_new_messages(self):
        temp = self.load_messages()
        newMessage = temp - self.last_seen_messages
        self.last_seen_messages = temp
        return newMessage
