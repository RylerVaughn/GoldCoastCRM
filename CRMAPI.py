from Client_Resources import Client_Resources
from Messaging_Resources import Messaging_Resources
from datetime import datetime
from Message_Template import Message_Template
from Twilio_API import Twilio_API
from Client_Messaging_History import Client_Messaging_History
import time

class CRMAPI():
    def __init__(self):
        self.client_resources = Client_Resources()
        self.messaging_resources = Messaging_Resources()
        self.twilio_api = Twilio_API()
        self.cmhistory = Client_Messaging_History()

    def add_client(self, **kwargs) -> int:
        return self.client_resources.add_client(**kwargs)

    def get_detailed_client_info(self) -> list:
        return self.client_resources.detailed_clientel_info()
    
    def validate_id(self, id: str) -> bool:
        for client in self.client_resources.get_clientel():
            if client.id == int(id):
                return True
        return False

    def add_date_to_client(self, id: str, date_obj: datetime):
        self.client_resources.add_date(int(id), date_obj)

    def add_job(self, **kwargs) -> int:
       return self.client_resources.add_job(**kwargs)

    def get_job_selection(self, id: str) -> tuple:
        client_jobs = self.client_resources.get_jobs(int(id))
        client_job_selection = ''
        job_ids = []
        for job in client_jobs:
            job_ids.append(job.id)
            client_job_selection += f'{job.id}) {job}\n'
        return job_ids, client_job_selection.lstrip()
    
    def change_job_detail(self, variable_name: str, new_value: type, job_id: str, client_id: str):
        self.client_resources.change_job_detail(variable_name, new_value, int(job_id), int(client_id))

    def change_client_detail(self, variable_name: str, new_value: type, id: str):
        self.client_resources.change_client_detail(variable_name, new_value, int(id))

    def delete_client(self, client_id: str):
        return self.client_resources.delete_client(int(client_id))
    
    def add_messaging_template(self, message_body: str):
        self.messaging_resources.add_messaging_template(message_body)

    def get_messaging_templates(self) -> dict:
        return self.messaging_resources.get_messaging_templates()
    
    def change_message_body(self, new_body: str, message_id: int):
        self.messaging_resources.change_message_body(new_body, message_id)

    def delete_message_template(self, message_id) -> Message_Template:
        return self.messaging_resources.delete_message_template(message_id)
    
    def check_distribution_requirments(self) -> bool:
        if len(self.client_resources.get_clientel()) > 0 and len(self.messaging_resources.get_messaging_templates()) > 0:
            return True
        return False
    
    def validate_template_id(self, template_id):
        if template_id in self.messaging_resources.get_messaging_templates():
            return True
        return False
    
    def validate_client_ids(self, client_ids):
        clients = [c.id for c in self.client_resources.get_clientel()]
        for client_id in client_ids:
            if client_id not in clients or client_ids.count(client_id) > 1:
                return False
        return True
        
    def get_text_messages(self, client_ids: list, template_id: int) -> list:
        clients = self.client_resources.get_clients_by_ids(client_ids)
        template = self.messaging_resources.get_messaging_template(template_id)
        return self.transform_message_templates(clients, template)
    
    def check_client_message_duplicates(self, clients_ids: list, message_template: str):
        print()
        # check the client_message_history for scenarios where the same message it sent to a client twice.

    # transform raw message template into unique messages for each clients instance variables. Returns the body, and the client it will be routed to.
    def transform_message_templates(self, clients: list, template: int) -> tuple:
        messages = []
        for client in clients:
            message_template = template.body
            message_template = message_template.replace('{name}', client.name)
            message_template = message_template.replace('{number}', client.phone_number)
            message_template = message_template.replace('{tpy}', str(client.times_a_year))
            message_template = message_template.replace('{address}', client.address)
            messages.append((message_template, client))
        return messages
    
    # method that will check for unique and repeated message combos, will then send to specified clientel based on paramaters.
    def distribute_text_messages(self, client_ids: list, template_id: int) -> tuple:
        clients = self.client_resources.get_clients_by_ids(client_ids)
        template = self.messaging_resources.get_messaging_template(template_id)
        unique_clients, repeated_clients = self.check_message_uniqueness(clients, template_id)
        text_messages = self.transform_message_templates(clients, template)
        for text_message in text_messages:
            time.sleep(0.25)
            self.twilio_api.send_message(client_number=text_message[1].phone_number, message=text_message[0])
            print(f' --- Message Routed To {text_message[1].name} --- ')
            

    # return two lists, one full of unique clients, one full of previous clients who were sent this message.
    def check_message_uniqueness(self, clients: list, template_id: int) -> tuple:
        client_ids = [client.id for client in clients]
        unique_ids, repeated_ids = self.cmhistory.check_uniqueness(client_ids, template_id)
        unique_clients = [self.client_resources.get_client(client_id) for client_id in unique_ids]
        repeated_clients = [self.client_resources.get_client(client_id) for client_id in repeated_ids]
        return unique_clients, repeated_clients


