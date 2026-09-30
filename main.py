import json
import time
from datetime import datetime
import threading
from zoneinfo import ZoneInfo

encoding = "utf-8"
TASK_FILE = "tasks.json"
APP_TIMEZONE = ZoneInfo("Asia/Bangkok")
tasks = []
tasks_lock = threading.RLock()


def reminder_loop():
    while True:
        check_reminders()
        time.sleep(1)


def check_reminders():
    now = datetime.now(APP_TIMEZONE)

    with tasks_lock:
        for task in tasks:
            if task.get("reminded", False):
                continue
            if task.get("complete", False):
                continue

            try:
                task_datetime = datetime.strptime(
                    task["date"] + " " + task["time"],
                    "%Y-%m-%d %H:%M"
                ).replace(tzinfo=APP_TIMEZONE)
            except (KeyError, TypeError, ValueError):
                print(f"Invalid date/time for task: {task.get('title', '(untitled)')}")
                continue

            if now >= task_datetime:
                print("\n======================")
                print("Reminders!!!")
                print(f"Task Title :{task.get('title', '(untitled)')}")
                print(f"Description :{task.get('des', '')}")
                print(f"Date :{task['date']} Time :{task['time']}")
                print("======================")

                task["reminded"] = True
                save_task()


def load_task():
    try:
        with open(TASK_FILE, "r", encoding=encoding) as file:
            loaded_tasks = json.load(file)
    except FileNotFoundError:
        print(f"Task file not found: {TASK_FILE}. Starting with an empty task list.")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in {TASK_FILE}. Starting with an empty task list.")
        return []

    if not isinstance(loaded_tasks, list):
        print(f"Invalid task data in {TASK_FILE}. Starting with an empty task list.")
        return []

    return loaded_tasks


def save_task():
    with tasks_lock:
        with open(TASK_FILE, "w", encoding=encoding) as file:
            json.dump(tasks, file, indent=4)


def get_task_number(prompt):
    try:
        number = int(input(prompt))
    except ValueError:
        print("Please enter a valid task number.")
        return None

    if not 1 <= number <= len(tasks):
        print("Task number is out of range.")
        return None
    return number - 1


def update_task(task, title, description, date, task_time, status):
    updated_date = date or task.get("date", "")
    updated_time = task_time or task.get("time", "")

    try:
        datetime.strptime(f"{updated_date} {updated_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return False

    date_changed = updated_date != task.get("date", "")
    time_changed = updated_time != task.get("time", "")

    if title:
        task["title"] = title
    if description:
        task["des"] = description
    task["date"] = updated_date
    task["time"] = updated_time
    if date_changed or time_changed:
        task["reminded"] = False

    if status.lower() in ["complete", "incomplete"]:
        task["complete"] = status.lower() == "complete"

    return True


def search_tasks():
    keyword = input("Search task title or description :").strip().casefold()

    if not keyword:
        print("Please enter a search keyword.")
        return

    maches = []

    with tasks_lock:
        for index ,task in enumerate(tasks ,start=1):
            title = task.get("title" ,"").casefold()
            description = task.get("des" ,"").casefold()

            if keyword in title or keyword in description:
                maches.append((index ,task))

    if not maches:
        print("No tasks found matching the keyword.")
        return

    print("\nSearch Results :")
    for index ,task in maches:
        status = "✓" if task.get("complete", False) else " "
        print(f"{index}.[{status}] {task.get('title', '(untitled)')} "
              f"{task.get('date', '-')} {task.get('time', '-')}")
        print(f"    Description: {task.get('des', '')}")


def main():
    global tasks
    tasks = load_task()

    reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
    reminder_thread.start()

    while True:
        print("\n=============================")
        print("=========To Do List =========")
        print("=============================")
        print("1. Add Tasks")
        print("2. Show Tasks")
        print("3. Complete Tasks")
        print("4. Edit Tasks")
        print("5. Delete Tasks")
        print("6. Search Tasks")
        print("7. Exit")

        choice = input("\nChoose : ")

        if choice == "1":
            print("Add Tasks")
            title = input("Task Title :")
            description = input("Description :")
            date = input("Date (YYYY-MM-DD) :")
            task_time = input("Time (HH:MM) :")

            try:
                datetime.strptime(f"{date} {task_time}", "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid date or time format.")
                continue

            tasks.append({
                "title": title,
                "des": description,
                "date": date,
                "time": task_time,
                "complete": False,
                "reminded": False,
            })
            save_task()
            print("Task Added")

        elif choice == "2":
            print("Show Tasks")
            print("\nYour Tasks :")
            for index, task in enumerate(tasks, start=1):
                status = "✓" if task.get("complete", False) else " "
                print(f"{index}.[{status}] {task.get('title', '(untitled)')} "
                      f"{task.get('date', '-')} {task.get('time', '-')}")
                print(f"    Description: {task.get('des', '')}")

        elif choice == "3":
            print("Complete Task")
            index = get_task_number("Enter Complete tasks number: ")
            if index is not None:
                tasks[index]["complete"] = True
                print(f"Task :{index + 1} Complete!!")
                save_task()

        elif choice == "4":
            print("Edit Tasks")
            index = get_task_number("Edit Task number :")
            if index is not None:
                task = tasks[index]
                print(f"Editing Task: {task.get('title', '(untitled)')}")
                new_title = input(f"New Title ({task.get('title', '')}): ")
                new_description = input(f"New Description ({task.get('des', '')}): ")
                new_date = input(f"New Date ({task.get('date', '')}): ")
                new_time = input(f"New Time ({task.get('time', '')}): ")
                new_status = input(f"Status Now :({'In complete' if task.get('complete', False) else 'complete'}) New Status (complete/incomplete) : ")

                if not update_task(
                    task, new_title, new_description, new_date, new_time, new_status
                ):
                    print("Invalid date or time format.")
                    continue

                save_task()
                print("Task Edited")

        elif choice == "5":
            print("Delete Tasks")
            index = get_task_number("Delete Task number :")
            if index is not None:
                tasks.pop(index)
                save_task()
                print("Task Deleted")

        elif choice == "6":
            print("Search Tasks")
            search_tasks()

        elif choice == "7":
            print("Exit")
            break

        else:
            print("***Invalid Input Value***")


if __name__ == "__main__":
    main()