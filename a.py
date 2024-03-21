import eel
import os
import json
import requests
from datetime import datetime

eel.init('web')

class TaskManager:
    def __init__(self):
        self.users = []  # Initialize an empty list for users
        self.tasks = {}  # Initialize an empty dictionary for tasks

    def user_exists(self, username):
        return any(user['username'] == username for user in self.users)

    def register_user(self, username, password):
        if not self.user_exists(username):
            self.users.append({'username': username, 'password': password})
            self.tasks[username] = []
            self.save_data()
            return True
        return False

    def login_user(self, username, password):
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def logout_user(self):
        return True

    def add_task(self, task, category, time, username):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_with_metadata = f'{task} ({category}) - {timestamp}' if time == '' else f'{task} ({category}) at {time} - {timestamp}'
        self.tasks[username].append(task_with_metadata)
        self.save_data()

    def delete_task(self, index, username):
        if 0 <= index < len(self.tasks[username]):
            del self.tasks[username][index]
            self.save_data()

    def edit_task(self, index, new_task, username):
        if 0 <= index < len(self.tasks[username]):
            self.tasks[username][index] = new_task
            self.save_data()

    def get_tasks(self, username):
        return self.tasks.get(username, [])

    def save_data(self):
        data = {'users': self.users, 'tasks': self.tasks}
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.users = data.get('users', [])
                self.tasks = data.get('tasks', {})

    def make_external_request(self):
        try:
            response = requests.get()
            if response.status_code == 200:
                return response
            else:
                return {'error': f'Request failed with status code {response.status_code}'}
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}

# Create an instance of the TaskManager class
task_manager = TaskManager()

# Expose the methods of the TaskManager instance to the Eel application
eel.expose(task_manager.user_exists)
eel.expose(task_manager.register_user)
eel.expose(task_manager.login_user)
eel.expose(task_manager.logout_user)
eel.expose(task_manager.add_task)
eel.expose(task_manager.delete_task)
eel.expose(task_manager.edit_task)
eel.expose(task_manager.get_tasks)
eel.expose(task_manager.save_data)
eel.expose(task_manager.load_data)
eel.expose(task_manager.make_external_request)

# Load data when the application starts
task_manager.load_data()

# Start the Eel application
eel.start('main.html', size=(800, 600))
