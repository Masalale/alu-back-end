#!/usr/bin/python3
"""
Script to export employee TODO list to CSV format
"""

import csv
import requests
import sys


def export_to_csv(user_id):
    """Export user's TODO list to CSV file"""
    # API endpoints
    user_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    todos_url = f"https://jsonplaceholder.typicode.com/todos?userId={user_id}"

    try:
        # Get user information
        user_response = requests.get(user_url)
        user_response.raise_for_status()
        user_data = user_response.json()
        username = user_data.get('username', '')

        # Get user's todos
        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        # Create CSV file
        filename = f"{user_id}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            # Write each todo as a row
            for todo in todos_data:
                writer.writerow([
                    str(user_id),
                    username,
                    str(todo.get('completed', False)),
                    todo.get('title', '')
                ])

        # Print the CSV content to console
        print(f"sylvain@ubuntu$ python3 1-export_to_CSV.py {user_id}")
        print(f"sylvain@ubuntu$ cat {user_id}.csv")
        with open(filename, 'r', encoding='utf-8') as csvfile:
            print(csvfile.read().strip())
        print("sylvain@ubuntu$")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1-export_to_CSV.py <user_id>")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
        export_to_csv(user_id)
    except ValueError:
        print("User ID must be an integer")
        sys.exit(1)
