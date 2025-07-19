#!/usr/bin/python3

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
        employee_name = user_data.get("name")

        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        total_tasks = len(todos_data)
        done_tasks = [task for task in todos_data if task.get("completed")]
        number_of_done_tasks = len(done_tasks)

        print("Employee {} is done with tasks({}/{}):".format(
            employee_name, number_of_done_tasks, total_tasks))

        for task in done_tasks:
            print("\t {}".format(task.get("title")))

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        sys.exit(1)
