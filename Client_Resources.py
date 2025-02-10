from Consumer import Consumer
from DatabaseManager import SQL_Manager

class Client_Resources():
    def __init__(self):
        self.DBM = SQL_Manager()
        self.clients = self.translate_into_consumer(self.DBM.load_client_packages())

    def add_client(self, **kwargs) -> int:
        client_id = self.DBM.add_client(**kwargs)
        kwargs['id'] = client_id
        self.clients[client_id] = Consumer(**kwargs)
        return client_id

    def get_clientel(self) -> list:
        return list(self.clients.values())
    
    def get_clients_by_ids(self, client_ids) -> list:
        return [self.clients[client_id] for client_id in client_ids]
    
    def translate_into_consumer(self, cds) -> dict:
        client_dictionary = {}
        for id, d in cds.items():
            consumer_obj = Consumer(**d)
            client_dictionary[id] = consumer_obj
        return client_dictionary
    
    def delete_client(self, client_id: int) -> Consumer:
        self.DBM.delete_client(client_id)
        return self.clients.pop(client_id)
            
    def detailed_clientel_info(self) -> list:
        client_reps = []
        for client in self.get_clientel():
            string = ''
            string += '-'*30
            string += f'\nName: {client.name}\nID: {client.id}\nContact: {client.phone_number}\nJobs a Year: {client.times_a_year}'
            string += f'\nAddress: {client.address}'
            if len(client.details) > 0:
                string += f'\nBio: {client.details}'
            if len(client.jobs) > 0:
                string += f'\nDocumented Jobs:\n  {"\n  ".join(map(lambda job: job.__str__(), client.jobs))}'
            string += f'\n{'-'*30}'
            client_reps.append(string)
        return client_reps

    def add_job(self, **kwargs) -> int:
        job_id, client_id = self.DBM.add_job(**kwargs)
        kwargs['job_id'] = job_id
        self.clients[client_id].add_job(**kwargs)
        return job_id
        
    def replace_date(self, client_id: int, date_index: int, new_date_obj):
        self.clients[client_id].dates[date_index] = new_date_obj
    
    def get_jobs(self, id: int) -> list:
        client = self.clients[id]
        return client.jobs
            
    def str_format_dates(self, dates: list) -> list:
        return [date.strftime('%Y / %m / %d') for date in dates]
            
    def get_client(self, id: int):
        return self.clients[id]
    
    def change_job_detail(self, column_name: str, new_value: type, job_id: int, client_id: int):
        self.DBM.change_job_detail(column_name, new_value, job_id)
        setattr(self.clients[client_id].get_job(job_id), column_name, new_value)

    def change_client_detail(self, variable_name: str, new_value: type, id: int):
        self.DBM.change_client_detail(variable_name, new_value, id)
        setattr(self.clients[id], variable_name, new_value)
        