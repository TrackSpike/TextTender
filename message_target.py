class MessageTarget:
    def __init__(self, name, number, system_message):
        self.name = name
        self.number = number
        self.system_message = system_message

    @classmethod
    def from_dict(cls, dict):
        return cls(dict["name"], dict["number"], dict["system_message"])
