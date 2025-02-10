from DatabaseManager import SQL_Manager
from Message_Template import Message_Template

class Messaging_Resources():
    def __init__(self):
        self.DBM = SQL_Manager()
        self.message_templates = self.translate_to_templates(self.DBM.load_message_templates())

    def add_messaging_template(self, message_body: str) -> int:
        template_id = self.DBM.add_messaging_template(message_body)
        self.message_templates[template_id] = Message_Template(message_body, template_id)

    def get_messaging_templates(self) -> dict:
        return self.message_templates
    
    def translate_to_templates(self, template_tuples: list) -> dict:
        message_templates = {}
        for tup in template_tuples:
            message_templates[tup[0]] = Message_Template(tup[1], tup[0])
        return message_templates
    
    def change_message_body(self, new_body: str, message_id: int):
        self.DBM.change_message_body(new_body, message_id)
        self.message_templates[message_id].body = new_body

    def delete_message_template(self, message_id: int) -> Message_Template:
        self.DBM.delete_message_template(message_id)
        return self.message_templates.pop(message_id)
    
    def get_messaging_template(self, template_id: int) -> Message_Template:
        return self.message_templates[template_id]
