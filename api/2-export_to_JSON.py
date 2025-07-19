#!/usr/bin/python3
"""
A script that, for a given employee ID, exports information about
his/her TODO list progress to a JSON file.
"""

import json
import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)

    base_url = "https://jsonplaceholder.typicode.com"
    user_url = "{}/users/{}".format(base_url, employee_id)
    todos_url = "{}/todos?userId={}".format(base_url, employee_id)

    try:
        user_response = requests.get(user_url)
        user_response.raise_for_status()
        user_data = user_response.json()
        username = user_data.get("username")

        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        # Build the JSON structure
        tasks_list = []
        for task in todos_data:
            task_dict = {
                "task": task.get("title"),
                "completed": task.get("completed"),
                "username": username
            }
            tasks_list.append(task_dict)

        # Create the final JSON structure
        json_data = {str(employee_id): tasks_list}

        # Write to JSON file
        file_name = "{}.json".format(employee_id)
        with open(file_name, mode='w') as json_file:
            json.dump(json_data, json_file)

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        sys.exit(1)
