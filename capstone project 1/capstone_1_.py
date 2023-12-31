import os
from datetime import datetime

def reg_user():
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print('This username already exists. Please choose a different username.')
            continue
        
        else:
            while True:
                new_password = input("New Password: ")
                confirm_password = input("Confirm Password: ")
                    
                if new_password == confirm_password:
                    print("New user added")
                    username_password[new_username] = new_password
                    with open("user.txt", "w") as out_file:
                        user_data = []
                        for k in username_password:
                            user_data.append(f"{k};{username_password[k]}")
                        out_file.write("\n".join(user_data))
                        break
                else:
                    print("Passwords do no match.")
                    continue
            break
                
def add_task():
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
                continue

        # Then get the current date.
        curr_date = datetime.now()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)

        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

        add_another_task = input('Would you like to add another task? y/n \n').lower()

        if add_another_task != 'y':
            break

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
       '''
    while True: 
        
        for index, t in enumerate(task_list):
            if t['username'] == curr_user:
                disp_str = f"Task: \t\t {t['title']}\n"
                print(index, disp_str)

            
        task_selector_input = input('''Enter the number of the task you would you like to view or 
        enter -1 to return to the main menu. \n''')
            
        try:
            task_selector = int(task_selector_input)

            if task_selector == -1:
                break

            elif task_selector < len(task_list):
                
                t = task_list[task_selector]
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)

        except ValueError:
            print('Invalid input. Please try again.')
            continue

        mark_or_edit = input('''Would you like to mark this task as complete or would
        you like to edit the task? (mark/edit) \n''').lower()
        print()
        
        if mark_or_edit == 'mark':
            
            with open("tasks.txt", "r") as task_file:
                lines = task_file.readlines()
                task_index = task_selector
                task_line = lines[task_index].strip().split(';')
                task_line[5] = 'Yes'
                lines[task_index] = ';'.join(task_line) + '\n'
            
            with open("tasks.txt", "w") as task_file:
                task_file.writelines(lines)
            
            print('Your task has now been marked as complete.')

        elif mark_or_edit == 'edit':
            username_or_date = input('''Would you like to change the user assigned to the task
            or the due date of the task? (user/date) \n''').lower()
            print()

            if username_or_date == 'user':
                changed_username = input('Please enter the new username: ')

                with open("tasks.txt", "r") as task_file:
                    task_data = task_file.read().split("\n")
                    task_data = [t for t in task_data if t != ""]

                    for t_str in task_data:
                        task_components = t_str.split(';')
                        task_components[0] = changed_username

                    if changed_username not in username_password:
                        print('This is not a registered user. Please try again.')
                        with open("tasks.txt", "w") as task_file:
                            task_file.writelines(changed_username)
                            continue
                    else:
                        break
                    
            elif username_or_date == 'date':
                
                while True:
                    try:
                        new_due_date = input('Please enter the new due date (YYYY-MM-DD): ')
                        new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        break
                    except ValueError:
                        print('Invalid date format. Please enter the date as YYYY-MM-DD.')

                with open("tasks.txt", "r") as task_file:
                    lines = task_file.readlines()
                    lines = [t for t in lines if t != ""]

                with open("tasks.txt", "w") as task_file:
                    for t_str in lines:
                        task_components = t_str.split(';')
                        task_components[3] = new_due_date_time.strftime(DATETIME_STRING_FORMAT)
                        new_due_date_time_str = ';'.join(task_components)
                        task_file.write(new_due_date_time_str)
        else:
            print('Invalid input. Please try again.')
            continue

def generate_reports():
    ''' Collects information about the total number of users and tasks and
    displays this information in a readable manner. Also collects information
    about the total number of tasks assigned to each user and displays each user's
    statistics in a percentage for tasks that are: complete, incomplete and overdue. '''
    num_tasks = len(task_list)
    num_users = len(username_password.keys())
    todays_date = datetime.now()

    with open('tasks.txt', 'r+') as task_file:
        lines = task_file.readlines()
        
        num_tasks_completed = 0
        num_tasks_incomplete = 0
        num_tasks_overdue = 0

        for task_line in lines:
            task_components = task_line.strip().split(';')
            check_tasks = task_components[5]

            if check_tasks == 'Yes':
                num_tasks_completed += 1
            else:
                num_tasks_incomplete += 1

            due_date_str = task_components[3]
            due_date = datetime.strptime(due_date_str, DATETIME_STRING_FORMAT)


            if due_date < todays_date:
                num_tasks_overdue += 1

        if num_tasks != 0:
            num_tasks_incomplete_percentage = num_tasks_incomplete/ num_tasks * 100
            num_tasks_overdue_percentage = num_tasks_overdue/ num_tasks * 100
        else:
            num_tasks_incomplete_percentage = '0'
            num_tasks_overdue_percentage = '0'

    task_overview_str = "-----------------------------------\n"
    task_overview_str += f"Total number of tasks: \t\t {num_tasks}\n"
    task_overview_str += f"Number of tasks completed: \t {num_tasks_completed}\n"
    task_overview_str += f"Number of tasks incomplete: \t {num_tasks_incomplete}\n"
    task_overview_str += f"Number of tasks overdue: \t\t {num_tasks_overdue}\n"
    task_overview_str += f"Percentage of tasks incomplete: \t {num_tasks_incomplete_percentage} %\n"
    task_overview_str += f"Percentage of tasks overdue: \t\t {num_tasks_overdue_percentage} %\n"
    task_overview_str += "-----------------------------------\n"

    with open('task_overview.txt', 'w') as file:
        file.write(task_overview_str)

    user_statistics = []

    for user in username_password.keys():
        total_user_tasks = 0
        user_tasks_complete = 0
        user_tasks_incomplete = 0
        user_tasks_overdue = 0

        for task in task_list:
            if task.get('username') == user:
                total_user_tasks += 1
                
                if not task.get('completed'):
                    user_tasks_incomplete += 1
                else:
                    user_tasks_complete += 1

                due_date = task.get('due_date')
        
                if due_date < todays_date:
                    user_tasks_overdue += 1

        if total_user_tasks != 0:
            user_tasks_complete_percentage = user_tasks_complete / total_user_tasks * 100
            user_tasks_incomplete_percentage = user_tasks_incomplete / total_user_tasks * 100
            user_tasks_overdue_percentage = user_tasks_overdue / total_user_tasks * 100
        else:
            user_tasks_complete_percentage = '0'
            user_tasks_incomplete_percentage = '0'
            user_tasks_overdue_percentage = '0'
            
        if num_tasks != 0:
            total_user_tasks_percentage = total_user_tasks/ num_tasks * 100
        else:
            total_user_tasks_percentage = '0'

        user_data = {
            "user": user,
            "total_user_tasks": total_user_tasks,
            "total_user_tasks_percentage": total_user_tasks_percentage,
            "user_tasks_complete_percentage": user_tasks_complete_percentage,
            "user_tasks_incomplete_percentage": user_tasks_incomplete_percentage,
            "user_tasks_overdue_percentage": user_tasks_overdue_percentage
        }

        user_statistics.append(user_data)


    with open('user_overview.txt', 'w') as file:
        for user_data in user_statistics:

            user_overview_str = "-----------------------------------\n"
            user_overview_str += f"User: {user_data['user']}\n"
            user_overview_str += f'Total number of users registered:   \t\t\t {num_users}\n'
            user_overview_str += f'Total number of tasks generated and tracked: \t\t {num_tasks}\n'
            user_overview_str += f"Total number of tasks assigned to the user: \t\t {user_data['total_user_tasks']}\n"
            user_overview_str += f"Percentage of total number of tasks assigned to the user: {user_data['total_user_tasks_percentage']} %\n"
            user_overview_str += f"Percentage of user tasks completed: \t {user_data['user_tasks_complete_percentage']} %\n"
            user_overview_str += f"Percentage of user tasks incomplete: \t {user_data['user_tasks_incomplete_percentage']} %\n"
            user_overview_str += f"Percentage of user tasks overdue: \t {user_data['user_tasks_overdue_percentage']} %\n"
            user_overview_str += "-----------------------------------\n"

            file.write(user_overview_str)




DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    print()

    if menu == 'r':
        reg_user()
       
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
                
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks. This option works by reading the contents from the task_overview.txt
            and user_overview.txt files.'''
        
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")   

        with open('task_overview.txt','r') as task_file:
            task = task_file.read()
        print(task)

        with open('user_overview.txt','r') as user_file:
            user_info = user_file.read()
        print(user_info)

    elif menu == 'gr' and curr_user == 'admin':
        '''If the user is the admin they can generate a report about the number of users,
            tasks assigned to the user, tasks completed and incomplete as well as tasks 
            overdue. To view the report, the user must be the admin and select the 'ds' 
            option from the menu.'''
        
        if not os.path.exists('task_overview.txt'):
            with open('task_overview.txt', 'w') as default_file:
                pass

        if not os.path.exists('user_overview.txt'):
            with open('user_overview.txt', 'w') as default_file:
                pass
    
        generate_reports()
        print ('Your report has been generated. Please select the display statistics option from the main menu to view.')

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
        continue
