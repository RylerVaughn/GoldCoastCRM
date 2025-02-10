from datetime import datetime

class Job():
    def __init__(self, date: datetime, payment: float, id: int):
        self.date = date
        self.payment = payment
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id
    
    def __str__(self):
        return f'Date of job : {self.date}, Payment: {self.payment}, Job ID: {self.__id}'