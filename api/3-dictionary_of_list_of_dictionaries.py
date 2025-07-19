#!/usr/bin/python3
"""
A script that exports information about all employees' TODO list progress to a JSON file.
"""

import json
import requests
import sys


if __name__ == "__main__":
    base_url = "https://jsonplaceholder.typicode.com"
    users_url = "{}/users".format(base_url)
    todos_url = "{}/todos".format(base_url)

    try:
        # Get all users
        users_response = requests.get(users_url)
        users_response.raise_for_status()
        users_data = users_response.json()

        # Get all todos
        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        # Create a dictionary to store user info by ID
        users_dict = {}
        for user in users_data:
            users_dict[user.get("id")] = user.get("username")

        # Build the JSON structure
        all_employees_data = {}
        
        for todo in todos_data:
            user_id = todo.get("userId")
            user_id_str = str(user_id)
            username = users_dict.get(user_id, "")

            # Initialize user's list if not exists
            if user_id_str not in all_employees_data:
                all_employees_data[user_id_str] = []

            # Add task to user's list
            task_dict = {
                "username": username,
                "task": todo.get("title"),
                "completed": todo.get("completed")
            }
            all_employees_data[user_id_str].append(task_dict)

        # Write to JSON file
        file_name = "todo_all_employees.json"
        with open(file_name, mode='w') as json_file:
            json.dump(all_employees_data, json_file)

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        sys.exit(1)
