"""
Create 3 classes with interconnection between them (Student, Teacher,
Homework)
Use datetime module for working with date/time
1. Homework takes 2 attributes for __init__: tasks text and number of days to complete
Attributes:
    text - task text
    deadline - datetime.timedelta object with date until task should be completed
    created - datetime.datetime object when the task was created
Methods:
    is_active - check if task already closed
2. Student
Attributes:
    last_name
    first_name
Methods:
    do_homework - request Homework object and returns it,
    if Homework is expired, prints 'You are late' and returns None
3. Teacher
Attributes:
     last_name
     first_name
Methods:
    create_homework - request task text and number of days to complete, returns Homework object
    Note that this method doesn't need object itself
PEP8 comply strictly.
"""
from __future__ import annotations
import datetime as dt
from typing import Union


class Teacher:
    """A class representing a Teacher object."""

    def __init__(self, lname: str, fname: str) -> None:
        self.last_name = lname
        self.first_name = fname

    def create_homework(self, homework_text: str, num_completion_days: int) -> Homework:
        """Creates a Homework object from homework text and number of days."""
        return Homework(homework_text, num_completion_days)
    
    
class Student:
    """A class representing a Student object."""
    def __init__(self, lname: str, fname: str) -> None:
        self.last_name = lname
        self.first_name = fname

    def do_homework(self, homework: Homework) -> Union[None, Homework]:
        """Returns Homework object if active or None if inactive."""
        if not homework.is_active():
            print("You are late") 
            return None
        return homework
    

class Homework:
    """A class representing a Homework object."""
    def __init__(self, text: str, num_days_to_complete: int) -> None:
        self.text = text
        self.created = dt.datetime.now()
        self.deadline = dt.timedelta(num_days_to_complete)

    def is_active(self) -> bool:
        """Returns a boolean indicating whether the Homework is active."""
        return dt.datetime.now() <= self.created + self.deadline


if __name__ == '__main__':
    teacher = Teacher('Dmitry', 'Orlyakov')
    student = Student('Vladislav', 'Popov')
    print(teacher.last_name)  # Daniil
    print(student.first_name)  # Petrov

    expired_homework = teacher.create_homework('Learn functions', 0)
    print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text) # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    print(student.do_homework(oop_homework))
    print(student.do_homework(expired_homework))  # You are late