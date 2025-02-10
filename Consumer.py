from datetime import datetime
from Job import Job

class Consumer():
    def __init__(self, **kwargs):    
        self.name = kwargs.get('name', 'NaN')
        self.phone_number = kwargs.get('phone_number', 'NaN')
        self.details = kwargs.get('details', '')
        self.times_a_year = kwargs.get('tp', 2)
        self.address = kwargs.get('address', 'NaN')
        self.__id = kwargs.get('id')
        self.jobs = []
        if kwargs.get('jobs') is not None:
            self.load_jobs(kwargs.get('jobs'))

    def add_job(self, **kwargs):
        self.jobs.append(
            Job(
                kwargs.get('date'),
                kwargs.get('payment', 0.0),
                kwargs.get('job_id')
            )
        )

    def load_jobs(self, jt: list):
        [self.jobs.append(Job(date=job[3], payment=job[1], id=job[0])) for job in jt]

    def get_job(self, job_id: int) -> Job:
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None
    
    @property
    def id(self):
        return self.__id

    def __str__(self):
            return f"Name: {self.name}, Phone Number: {self.phone_number}, Address: {self.address}"
    
    def __repr__(self):
            return f"Name: {self.name}, Phone Number: {self.phone_number}, Address: {self.address}"
