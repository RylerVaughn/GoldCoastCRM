from textwrap import wrap

class Message_Template():
    def __init__(self, body: str, message_id: int):
        self.body = body
        self.records = set
        self.__id = message_id

    @property
    def id(self) -> int:
        return id
    
    def add_record(self, client_id: int) -> bool:
        if client_id in self.records:
            return False
        self.records.add(client_id)

    def __str__(self):
        return f"{self.__id}) : '{'\n'.join(wrap(text=self.body, width=45))}'"
    
    def __repr__(self):
        return f"{self.__id}) :  {'\n'.join(wrap(text=self.body, width=45))}"