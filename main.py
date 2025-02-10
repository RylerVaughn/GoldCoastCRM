from Consumer import Consumer
from datetime import datetime, date as onlydate
from CRMAPI import CRMAPI
import mysql.connector
from Job import Job
import time

class UserInterface():
    def __init__(self):
        self.__client_api = CRMAPI()

    def execute(self):

        def returned():
            print("\nWelcome to your client relationship management system.")
            self_help()

        def self_help():
            print()
            print("Your options: ")
            print("1) View Client Resources.")
            print("2) View Messaging Resources.")
            print('3) Document a Job.')
            print('4) Distribute Messages.')
            print('x) Quit Application.')

        print('='*35)
        print()
        print("\nWelcome to your client relationship management system.")
        self_help()
        while True:
            command = input('\nInput > ')
            if command == '1':
                self.view_client_resources()
                returned()
            elif command == '2':
                self.view_messaging_resources()
                returned()
            elif command == '3':
                self.document_job()
                returned()
            elif command == '4':
                self.distribute_message_templates_to_clientel()
                returned()
            elif command.lower() == 'x':
                print("Quitting Application...")
                break
            else:
                print('|| Invalid Input. ||')
                self_help()

    def distribute_message_templates_to_clientel(self):
        if not self.__client_api.check_distribution_requirments():
            print('You need to have atleast one client and one messaging template to distribute messages.')
            return
        self.view_messaging_templates(edit_mode=True)
        print('Which messaging template would you like to use?')
        while True:
            template_id = self.validate_input('ID > ', int, 'Input must be a number.')
            if self.__client_api.validate_template_id(template_id):
                break
            print('Input must be within the available templates.')        
        print()
        print('What clients would you like to send this message to?')
        self.view_clientel(edit_mode=True)
        print('''
        To choose which clients to send this to,
        you have to seperate each id with a space
        like so : "1, 2, 3, 4".
        ''')
        time.sleep(2)
        print()
        while True:
            client_ids = self.validate_input("Client ID's > ", lambda string: [int(value) for value in string.split(' ')], 'Values must be seperated by spaces')
            if not self.__client_api.validate_client_ids(client_ids):
                print('Make sure every id given is within the available ids and that there is no duplicates.')
                continue
            break
            #line 78's function will check for duplicate messages sent to clients from the messaging history, implement the sending functionality first then get back to this.
        #execute = self.__client_api.check_client_message_duplicates()
        #
        example_message = self.__client_api.get_text_messages([client_ids[0]], template_id)
        #
        print()
        print(' ---- Example Message ---- ')
        print(f'{example_message[0][0]}')
        print()
        while True:
            choice = input('Continue? (Y/N) > ')
            if choice.upper() == 'Y':
                break
            elif choice.upper == 'N':
                print(' --- Task Disrupted --- ')
                return
            else:
                print(' | Invalid Input |')
        print()
        print(' --- Sending Messages --- ')
        time.sleep(1)
        try:
            self.__client_api.distribute_text_messages(client_ids, template_id)
        except:
            print('\n Error: Invalid phone number or server is down.')
    def view_messaging_resources(self):
        def self_help():
            print('\nOptions:')
            print('1) Add a messaging template.')
            print('2) View messaging templates.')
            print('3) Edit messaging templates.')
            print('x) Return.')

        print(f'\n{"="*35}')
        print('Welcome to your Messaging Resources.')
        self_help()
        while True:
            command = input('\nInput > ')
            if command == '1':
                self.add_messaging_template()
                self_help()
            elif command == '2':
                self.view_messaging_templates()
                self_help()
            elif command == '3':
                self.edit_messaging_templates()
                self_help()
            elif command == 'x':
                return
            else:
                print(' || Invalid Input || ')

    def edit_messaging_templates(self):
        messaging_templates = self.__client_api.get_messaging_templates()
        print()
        if len(messaging_templates) > 0:
            print(' --- Available Templates --- ')
            self.view_messaging_templates(edit_mode=True)
            while True:
                message_id = self.validate_input('\nWhat template would you like to edit? (Type their ID) > ', int, 'Input must be a number.') 
                if message_id in messaging_templates:
                    break
                print('ID must be within the range of existing IDs.')  
            print()
            print('What would you like to edit?')
            print('1) Change Message Body.')
            print('2) Delete Message.')
            print()
            while True:
                choice = self.validate_input('Input > ', int, 'Input must be a number.')
                if choice in (1, 2):
                    break
                print('Choice must be one of the options.')
            if choice == 1:
                self.change_message_body(messaging_templates, message_id)
                return
            elif choice == 2:
                self.delete_message_template(message_id)
        else:
            print(' --- No Templates Found --- ')

    def delete_message_template(self, message_id):
        print()
        confirm = input('Confirm Delete (Y) > ')
        if confirm.upper() == 'Y':
            deleted_message = self.__client_api.delete_message_template(message_id)
            print()
            print('Successfully deleted this message:')
            print(deleted_message)

    def change_message_body(self, messaging_templates: dict, message_id: int):
        print(self.message_body_rules())
        print()
        print(f'Old Message Body: {messaging_templates[message_id].body}')
        print()
        while True:
            new_message_body = input('New Message Body > ')
            confirm = input('Confirm Change? (Y) > ')
            if confirm.upper() == 'Y':
                break
            else:
                print(' --- Change Scratched --- ')
                return
        self.__client_api.change_message_body(new_message_body, message_id)

    def view_messaging_templates(self, edit_mode: bool=False) -> bool:
        messaging_templates = self.__client_api.get_messaging_templates()
        print()
        if len(messaging_templates) > 0:
            for template in messaging_templates:
                time.sleep(0.25)
                print('-'*35)
                print(f"{messaging_templates[template]}")
                print('-'*35)
                tof = True
        else:
            print(' --- No Templates Found --- ')
            tof = False
        if edit_mode:
            return
        print()
        input('Press any key to return.')
        return tof
    
    def message_body_rules(self) -> str:
        string = """
        Rules for messaging templates,
        If you want to add a detail about a specific client
        like maybe their name for example, you would want to
        Write {name}, every detail like that must be surrounded
        with curly brackets "{}". Some keywords you can use are:
        {name}, {number} (clients phone number), {address} (clients address)
        {tpy} (the amount of times a year they want the job done)
        """
        return string

    def add_messaging_template(self):
        print(self.message_body_rules())
        print()
        while True:
            message_body = input('Write Your Message Template (new lines automatically apply) > ')
            choice = input('Proceed with this template? (Y) > ')
            if choice.upper() == 'Y':
                break
        self.__client_api.add_messaging_template(message_body)

    def catch_id_num_error(self, user_input: str) -> bool:
        try:
            int(user_input)
            return False
        except:
            print('Input must either be "Exit" or a number.')
            return True

    def document_job(self):
        print('='*35)
        self.view_clientel(edit_mode=True)
        print()
        while True:
            print('\nSelect the client that provided the job for you by typing in their ID. ("Exit" to return)')
            id = input('ID > ')
            if id.upper()  == 'EXIT' or id == '':
                return
            if self.catch_id_num_error(id):
                continue
            if self.__client_api.validate_id(id):
                while True:
                    print()
                    print('Options:')
                    print('1) Document job done today.')
                    print('2) Document job done another time.')
                    command = input(' > ')
                    if command == '1':
                        date_of_job = datetime.now().date()
                        payment_of_job = self.get_payment_input()
                        break
                    elif command == '2':
                        date_of_job = self.get_date_input()
                        payment_of_job = self.get_payment_input()
                        break
                    else:
                        print('User input must be within the option range.')
                job_args = {
                    'payment': payment_of_job,
                    'date': date_of_job,
                    'client_id': int(id)
                }
                self.__client_api.add_job(**job_args)
                print(' --- Success --- ')
            else:
                print('Client id not found.')
                continue
            return

    def get_date_input(self) -> datetime:
        print()
        date = self.validate_input(
            'Input the date of the job (YYYY/MM/DD) > ',
            lambda x: datetime.strptime(x, '%Y/%m/%d'),
            'Error: Make sure input is in the format (YYYY/MM/DD).'
        )
        return date
    
    def get_payment_input(self) -> float:
        print()
        payment = self.validate_input('Payment from job > ', float, 'Input must be a number.')
        return payment

    def view_client_resources(self):

        def returned():
            print('\nWelcome to your Client Resources.')
            client_resource_help()

        def client_resource_help():
            print()
            print('Your options:')
            print('1) Add Client.')
            print('2) View Clientel.')
            print('3) Edit Clientel')
            print('x) Return.')    

        print('='*35)
        print('\nWelcome to your Client Resources.')
        client_resource_help()
        while True:
            command = input('\nInput > ')
            if command == '1':
                self.add_client()
                returned()
            elif command == '2':
                self.view_clientel()
                returned()
            elif command == '3':
                self.edit_clientel()
                returned()
            elif command == 'x':
                print('=====================================')
                return
            else:
                print('|| Invalid Input. ||')
                client_resource_help()

    def validate_bool_input(self, prompt: str, function , error_msg: str) -> type:
        while True:
            try:
                param = input(prompt)
                if not function(param):
                    print(error_msg)
                else:
                    return param
            except:
                print(error_msg)

    def validate_input(self, prompt: str, data_type: type, error_msg: str) -> type:
        while True:
            try:
                user_input = input(prompt)
                return data_type(user_input)
            except:
                print(error_msg)

    def edit_clientel(self):
        print('\n --- Availible clients --- \n')
        self.view_clientel(edit_mode=True)
        print('To choose which client to edit, please type in their ID.')
        print('("Exit" to leave.)')
        print()
        while True:
            id = input('ID > ')
            if id.upper() == 'EXIT':
                return
            if self.catch_id_num_error(id):
                continue
            if self.__client_api.validate_id(id=id):
                print()
                print('What to edit?')
                print('0 | Delete Client\n1 | Client Name\n2 | Client Phone Number\n3 | Details\n4 | Jobs a Year\n5 | Alter Job Details\n6 | Leave')
                print()
                while True:
                    choice = self.validate_input('Choice > ', int, 'User Input must be a number.')
                    if choice == 6:
                        return
                    if choice in range(0, 6):
                        break
                    print('Choice must be between 1 - 6.')
                if choice == 0:
                    client = self.__client_api.delete_client(id)
                    print(f' --- deleted {client.name} from clients. --- ')

                elif choice == 1:
                    client_name = input('New Client Name > ')
                    self.__client_api.change_client_detail('name', client_name, id=id)
                elif choice == 2:
                    client_number = input('New Client Phone Number > ')
                    self.__client_api.change_client_detail('phone_number', client_number, id=id)
                elif choice == 3:
                    details = input('Write a new bio for your client > ')
                    self.__client_api.change_client_detail('details', details, id)
                elif choice == 4:
                    jpy = self.validate_input('New Amount of Jobs Per Year > ', int, 'Input must be a number.')
                    self.__client_api.change_client_detail('times_a_year', jpy, id)
                    print(' --- Success --- ')
                elif choice == 5:
                    self.alter_job_details(id)
                return 
            else:
                print('ID not found.')

    def alter_job_details(self, id: str):
        print('jobs able to modify: \n')
        job_id = self.job_selection_prompt(id)
        print()
        print('What would you like to modify?')
        print('1) Job payment.')
        print('2) Date of job.') 
        while True:
            command = self.validate_input(' > ', int, 'Input must be a whole number.')
            if command == 1:
                new_job_payment = self.validate_input('Corrected Payment > ', float, 'Input must be a number.')
                self.__client_api.change_job_detail('payment', new_job_payment, job_id, id)
                break
            elif command == 2:
                new_date = self.validate_input(
                    'Corrected date of job (YYYY/MM/DD) > ', 
                    lambda date: datetime.strptime(date, '%Y/%m/%d'),
                    'Date must be formatted as YYYY/MM/DD.'
                )
                self.__client_api.change_job_detail('job_date', new_date, job_id, id)
                break
            else:
                print('Number must either be 1 or 2.')
                continue
        time.sleep(1)

        print('\n --- Success --- ')
        
    def job_selection_prompt(self, client_id) -> int:
        job_ids, prompt = self.__client_api.get_job_selection(client_id)
        print(prompt)
        job_id = self.validate_bool_input(
            'Type in the job ID you want to modify > ',
            lambda param: int(param) in job_ids,
            'Input must be within the job ids.'
        )
        return job_id

    def view_clientel(self, edit_mode: bool=False):
        client_representations = self.__client_api.get_detailed_client_info()
        if len(client_representations) > 0:
            for client in client_representations:
                time.sleep(0.25)
                print(client)
            print()
            while True:
                if edit_mode:
                    return
                choice = input('Return? (Yes) > ')
                if choice.upper() == 'YES' or choice == '':
                    return
                else:
                    print('Type "Yes" or click Enter to return')
        else:
            time.sleep(0.5)
            print("\n ---- No clients found. ---- ")

    def add_client(self):
        print('-'*20)
        while True:
            client_name = input("Client Name > ")
            job_choice = input('Would you like to mark down any previous jobs done with this client? (Y to proceed) > ')
            if job_choice.upper() == 'Y':
                job_payment = self.validate_input('Job Payment > ', float, 'Input must be a number.')
                date_of_job = self.validate_input(
                'Date of Job "Year/Month/Day" > ',
                lambda date: datetime.strptime(date, '%Y/%m/%d'),
                "Please type in the format of 'Year/Month/Day', make sure to input them as numbers, also make sure you input a valid date."
                )
            recurrment_plan = self.validate_input('How many times a year will they require this service > ', int, 'Input must be a number')
            client_phone_number = input("Please type in the correct phonenumber > +1 ").replace(' ', '')
            client_address = input('Clients Home Address > ')
            details_choice = input('Extra details (Y to proceed) > ')
            details = ''
            if details_choice.upper() == 'Y':    
                details = input('Write some details > ')
            while True:
                add_client = input('Document Client? (Y/N) > ')
                if add_client.upper() == 'Y':
                    client_args = {
                        'name': client_name,
                        'details': details,
                        'tp': recurrment_plan,
                        'phone_number': client_phone_number,
                        'address': client_address
                    }
                    client_id = self.__client_api.add_client(**client_args)
                if job_choice.upper() == 'Y':
                    job_args = {
                        'date': date_of_job,
                        'payment': job_payment,
                        'client_id': client_id
                    }
                    self.__client_api.add_job(**job_args)
                elif add_client.upper() == 'N':
                    time.sleep(0.5)
                    print(' --- Client was not documented. --- ')
                    return
                print(' --- Success --- ')
                time.sleep(1)
                return
                
if __name__ == '__main__':
    ui = UserInterface()
    ui.execute()
