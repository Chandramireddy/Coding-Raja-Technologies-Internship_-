import datetime

class Task:
    def __init__(self, description, priority='medium', due_date=None, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date  # Should be a datetime.date object
        self.completed = completed

    def __str__(self):
        status = 'Completed' if self.completed else 'Pending'
        return f"[{status}] {self.description} (Priority: {self.priority})" + \
               (f" - Due: {self.due_date.strftime('%Y-%m-%d')}" if self.due_date else "")

    def mark_as_completed(self):
        self.completed = True

import pickle

class TaskManager:
    def __init__(self, data_file):
        self.tasks = []
        self.data_file = data_file
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_as_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_as_completed()
            self.save_tasks()

    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task}")

    def save_tasks(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open(self.data_file, 'rb') as f:
                self.tasks = pickle.load(f)
        except FileNotFoundError:
            self.tasks = []

    def get_task(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    def clear_tasks(self):
        self.tasks = []
        self.save_tasks()


import datetime

def print_menu():
    print("Command Menu:")
    print("  1. Add Task")
    print("  2. Remove Task")
    print("  3. Mark Task as Completed")
    print("  4. List Tasks")
    print("  5. Exit")
    print()

def get_date_input():
    while True:
        date_str = input("Enter due date (YYYY-MM-DD) or leave empty: ").strip()
        if date_str == "":
            return None
        try:
            year, month, day = map(int, date_str.split('-'))
            return datetime.date(year, month, day)
        except ValueError:
            print("Invalid date format. Please enter again.")

def main():
    data_file = "tasks.pickle"  # You can change the filename or path as needed
    task_manager = TaskManager(data_file)

    while True:
        print_menu()
        choice = input("Enter command number: ").strip()

        if choice == '1':
            description = input("Enter task description: ").strip()
            priority = input("Enter priority (high/medium/low, default=medium): ").strip().lower()
            if priority not in ['high', 'medium', 'low']:
                priority = 'medium'
            due_date = get_date_input()
            task = Task(description, priority, due_date)
            task_manager.add_task(task)
            print("Task added!\n")

        elif choice == '2':
            task_manager.list_tasks()
            index = int(input("Enter task number to remove: ")) - 1
            task_manager.remove_task(index)
            print("Task removed!\n")

        elif choice == '3':
            task_manager.list_tasks()
            index = int(input("Enter task number to mark as completed: ")) - 1
            task_manager.mark_task_as_completed(index)
            print("Task marked as completed!\n")

        elif choice == '4':
            task_manager.list_tasks()
            print()

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid command. Please enter a number between 1 and 5.\n")

if __name__ == '__main__':
    main()