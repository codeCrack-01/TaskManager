import re
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
import enum

# Define the Enum type
class Status(enum.Enum):
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(Enum(Status), default=Status.NOT_STARTED)


# Create the Engine and Base_Class
engine = create_engine('sqlite:///tasks.db')

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

#############################################
# Defining my own CLI Program !
flag = False
        
def is_enum_value(string):
    return string in Status._value2member_map_

def enum_key_from_value(value):
    for key, member in Status.__members__.items():
        if member.value == value:
            return key
    return None  # Return None if the value isn't found in the enum

def clearAll():
    session.query(Task).delete()
    session.commit()
    print("Deleted all tasks !")

def addTask():
    title = input("\nEnter the Task Title:\n")
    status = input("Enter the Status [Not Started][In Progress][Completed]:\n")

    if is_enum_value(status):
        task = Task(title=title, status=enum_key_from_value(status))
        session.add(task)
        session.commit()
        print('Task was added succesfully !')
    else:
        print("Invalid Status!")

def showTask():
    # Query the table
    all_tasks = session.query(Task).all()
    print('\n')

    # Print the results
    # Print column names
    column_names = Task.__table__.columns.keys()
    print("| " + f"{' | '.join(column_names)}")

    # Print the results row by row
    for task in all_tasks:
        print(f"| {task.id} | {task.title} | {task.status}")

def updateTask():
    id_value = int(input("\nEnter the task id:\n"))
    new_status = input('Enter the new status [Not Started][In Progress][Completed]:\n')

    try:
        target = session.query(Task).filter_by(id=id_value).first()
        target.status = enum_key_from_value(new_status) # type: ignore
        session.commit()
        print("Status Updated !")

    except Exception : 
        print('Invalid Syntax !')

def deleteTask():
    id_value = int(input("\nEnter the task id:\n"))
    try:
        target = session.query(Task).filter_by(id=id_value).first()
        session.delete(target)
        session.commit()
        print("Task Deleted !")

    except Exception : 
        print('Invalid Input !')

def changeTask():
    id_value = int(input("\nEnter the task id:\n"))
    new_title = input('Enter the new title\n')

    try:
        target = session.query(Task).filter_by(id=id_value).first()
        target.title = enum_key_from_value(new_title) # type: ignore
        session.commit()
        print("Title Updated !")

    except Exception : 
        print('Invalid Syntax !')

def QuitApp():
    lastCheck = input('\nAre you sure you want to quit? [Y/n]:\n').lower()

    if (lastCheck == 'y'):
        print("\nExiting the App !")
        global flag
        flag = True
    else:
        return

def userGuide():
    print('''\n##############################################################################
--------------------------
WELOCME TO THE USER GUIDE!
--------------------------

Following are the commands with description:

[1]  .addTask: "Use this command to add a new task to your list."

[2]  .showTask: "Use this command to display your current list of tasks."

[3]  .updateTask: "Use this command to update the task status."

[4]  .changeTask: "Use this command to modify task title."

[5]  .deleteTask: "Use this command to delete a specific task from list."

[6]  .clearAll: "Use this command to clear all tasks from your list."

[7]  .help: "Use this command to display this guide."

[8]  .quit: "Use this command to exit the task management system."

_____________________________________________________________________________
! IMPORTANT !

The 'status' type only supports three values:

[1] "Not Started"
[2] "In Progress"
[3] "Completed"

##############################################################################''')

def checkResponse(response):
    match response:
        case '.addtask':
            return addTask()
        case '.showtask':
            return showTask()
        case '.updatetask':
            updateTask()
        case '.changetask':
            changeTask()
        case '.deletetask':
            deleteTask()
        case '.clearall':
            clearAll()
        case '.help':
            userGuide()
        case '.quit':
            QuitApp()
        case _:
            print("Invalid Syntax! Type '.help' for user guidance.")

#############################################

print("\nWelcome to the task Manager!")

while flag is False:
    print("\nUse the following Commands:")
    print("[.addTask  .showTask  .updateTask  .changeTask  .deleteTask  .clearAll  .help  .quit]")

    user_response = input().lower()
    checkResponse(response=user_response)


