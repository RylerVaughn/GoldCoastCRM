from DatabaseManager import SQL_Manager

class Client_Messaging_History():
    def __init__(self):
        self.DBM = SQL_Manager()
        self.records = {}
        self.load_records(self.DBM.load_messaging_records())

    # document what template has been sent to what client to increase uniqueness.
    def add_record(self, template_id: int, client_id: int):
        if template_id not in self.records:
            self.records[template_id] = []
        self.records[template_id].append(client_id)

    #arguments are a list of tuples from the DBM and returns a records dictionary.
    def load_records(self, raw_records: list):
        for record in raw_records:
            self.add_record(record[0], record[1])

    def check_uniqueness(self, client_ids: list, template_id: int) -> tuple:
        unique = []
        repeated = []
        if template_id in self.records:
            for client_id in self.records[template_id]:
                if client_id in client_ids:
                    repeated.append(client_id)
                else:
                    unique.append(client_id)
            return unique, repeated
        else:
            return client_ids, []