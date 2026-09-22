import json
import time
from datetime import datetime
import threading
from zoneinfo import ZoneInfo

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
                print("======================")
                print("Reminders!!!")
                print(f"Task Title :{task.get('title', '(untitled)')}")
                print(f"Date :{task['date']} Time :{task['time']}")
                print("======================")

                task["reminded"] = True
                save_task()


def load_task():
    with open(TASK_FILE, "r") as file:
        return json.load(file)


def save_task():
    with tasks_lock:
        with open(TASK_FILE, "w") as file:
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
        print("4. Delete Tasks")
        print("5. Exit")

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

        elif choice == "3":
            print("Complete Task")
            index = get_task_number("Enter Complete tasks number: ")
            if index is not None:
                tasks[index]["complete"] = True
                print(f"Task :{index + 1} Complete!!")
                save_task()

        elif choice == "4":
            print("Delete Tasks")
            index = get_task_number("Delete Task number :")
            if index is not None:
                tasks.pop(index)
                save_task()
                print("Task Deleted")

        elif choice == "5":
            print("Exit")
            break

        else:
            print("***Invalid Input Value***")


if __name__ == "__main__":
    main()