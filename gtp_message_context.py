from enum import Enum
from collections import deque
from prettytable import PrettyTable, MARKDOWN


class GtpMessageContext:
    def __init__(self, system_message, maxlen=10):
        self._messages = deque(maxlen=maxlen)
        self.system_message = system_message

    def add_user_message(self, message, prepend=False):
        if prepend:
            self._messages.appendleft((self.clean(message), Role.USER))
        else:
            self._messages.append((self.clean(message), Role.USER))

    def add_assistant_message(self, message, prepend=False):
        if prepend:
            self._messages.appendleft((self.clean(message), Role.ASSISTANT))
        else:
            self._messages.append((self.clean(message), Role.ASSISTANT))

    def to_json(self):
        return [{"role": "system", "content": self.system_message}] + [
            {"role": role.name.lower(), "content": message}
            for message, role in self._messages
        ]

    def clean(self, message):
        if not message:
            return ""
        return message.replace("'", "").replace('"', "")

    @property
    def is_full(self):
        return self._messages != None and len(self._messages) >= self._messages.maxlen

    def __str__(self):
        table = PrettyTable()
        table.field_names = ["Message", "Role"]
        table.set_style(MARKDOWN)
        table._max_width = {"Role": 20, "Message": 50}
        table.add_row([self.system_message, Role.SYSTEM])
        table.add_rows(self._messages)
        return table.get_string()


class Role(Enum):
    USER = 1
    SYSTEM = 2
    ASSISTANT = 3
