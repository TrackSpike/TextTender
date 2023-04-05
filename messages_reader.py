# a wrapper class around the tuple (user_id, message, date, service, account, is_from_me)
class Message:
    def __init__(self, user_id, message, date, service, account_number, is_from_me):
        self.user_id: str = user_id
        self.message: str = message
        self.date: str = date
        self.service: str = service
        self.account_number: str = account_number
        self.is_from_me: bool = is_from_me == 1

    def __str__(self):
        return f"User ID: {self.user_id}\n Message: {self.message}\n Date: {self.date}\n Service: {self.service}\n Account: {self.account_number}\n Is from me: {self.is_from_me}\n"
