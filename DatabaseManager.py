import mysql.connector
from datetime import datetime, date
import os

class SQL_Manager():
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.database = 'crm'
        self.password = os.environ.get('MYSQL_PASS')

    def load_client_packages(self) -> dict:
        client_tuples = self.get_clients_table()
        clients = {}
        for i in range(len(client_tuples)):
            clients[client_tuples[i][0]] = {
                'name': client_tuples[i][1],
                'id': client_tuples[i][0],
                'address': client_tuples[i][2],
                'phone_number': client_tuples[i][3],
                'details': client_tuples[i][4],
                'tp': client_tuples[i][5],
                'jobs': self.get_jobs_by_id(client_tuples[i][0])
            }
        return clients
    
    # function that grabs jobs from the job table that correspond to the given client_id
    def get_jobs_by_id(self, id: int) -> list:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT * FROM jobs WHERE client_id = %s'
        value = (id,)
        cursor.execute(query, value)
        jobs = cursor.fetchall()
        mydb.close()
        if len(jobs) > 0:
            return jobs
        return None

    def get_dates_from_tuple(self, tup) -> list:
        dates = []
        for value in tup:
            if isinstance(value, date):
                dates.append(value)
        return dates

    def get_connection(self):
        connection = mysql.connector.connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password
        )
        return connection
    
    def add_client(self, **kwargs) -> int:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'INSERT INTO clients(name, address, phone_number, details, yearly_jobs) VALUES (%s, %s, %s, %s, %s)'
        values = (
            kwargs.get('name', 'NaN'),
            kwargs.get('address', 'NaN'),
            kwargs.get('phone_number', 0.0),
            kwargs.get('details', ''),
            kwargs.get('tp', 0)
        )
        cursor.execute(query, values)
        client_id = cursor.lastrowid
        mydb.commit()
        mydb.close()
        return client_id
    
    def change_job_detail(self, column_name: str, new_value: type, job_id: int):
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = f'UPDATE jobs SET {column_name} = %s WHERE job_id = %s'
        values = (new_value, job_id)
        cursor.execute(query, values)
        mydb.commit()
        mydb.close()

    def delete_client(self, client_id):
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'DELETE FROM clients WHERE client_id = %s'
        cursor.execute(query, (client_id,))
        mydb.commit()
        mydb.close()

    def add_job(self, **kwargs) -> int:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'INSERT INTO jobs(payment, client_id, job_date) VALUES (%s, %s, %s)'
        values = (
            kwargs.get('payment', 0.0),
            kwargs.get('client_id'),
            kwargs.get('date', datetime(1999, 1, 1))
        )
        cursor.execute(query, values)
        mydb.commit()
        mydb.close()
        return cursor.lastrowid, kwargs.get('client_id')

    def get_client_by_name(self, name):
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT * FROM clients WHERE name = %s'
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        mydb.close()
        return result
    
    def get_clients_table(self) -> list:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT * FROM clients'
        cursor.execute(query)
        response = cursor.fetchall()
        mydb.close()
        return response
    
    # returns the job table as a list of tuples in the form (job_id, payment, client_id, job_date)
    def get_jobs_table(self) -> list:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT * FROM jobs'
        cursor.execute(query)
        response = cursor.fetchall()
        mydb.close()
        return response
    
    def get_joined_client_table(self) -> list:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT * FROM clients LEFT JOIN jobs ON clients.client_id = jobs.client_id'
        cursor.execute(query)
        response = cursor.fetchall()
        mydb.close()
        return response
    
    def change_client_detail(self, column_name, new_value, id: int):
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = f"UPDATE clients SET {column_name} = %s WHERE client_id = %s"
        values = (new_value, id)
        cursor.execute(query, values)
        mydb.commit()
        mydb.close()       

    def add_messaging_template(self, message_body: str) -> int:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'INSERT INTO messages(body) VALUES(%s)'
        value = (message_body,) 
        cursor.execute(query, value)
        mydb.commit()
        template_id = cursor.lastrowid
        mydb.close()
        return template_id
    
    def load_message_templates(self) -> list:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT * FROM messages'
        cursor.execute(query)
        response = cursor.fetchall()
        mydb.close()
        return response
    
    def change_message_body(self, new_body: str, message_id: int):
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'UPDATE messages SET body = %s WHERE message_id = %s'
        values = (new_body, message_id)
        cursor.execute(query, values)
        mydb.commit()
        mydb.close()

    def delete_message_template(self, message_id):
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'DELETE FROM messages WHERE message_id = %s'
        values = (message_id,)
        cursor.execute(query, values)
        mydb.commit()
        mydb.close()

    def load_messaging_records(self) -> list:
        mydb = self.get_connection()
        cursor = mydb.cursor()
        query = 'SELECT message_id, client_id FROM clientmessaginghistory'
        cursor.execute(query)
        mydb.close()
        return cursor.fetchall()

