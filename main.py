import json

def load_task():
    with open("tasks.json" ,"r") as file:
        return json.load(file)

def save_task():
    with open("tasks.json" ,"w") as file:
        json.dump(tasks ,file ,indent=4)

tasks = load_task()
tasks_dec = []

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

    if choice == "1" :
        print("Add Tasks")
        title = input("Task Title :")
        des = input("Description :")
        date = input("Date (YYYY-MM-DD) :")
        time = input("Time (HH:MM) :")
        complete = False 

        task = {
        "title" : title,
        "des" : des,
        "date" : date,
        "time" : time,
        "complete" : False
    } 
        
        tasks.append(task)
        save_task()  
        print("Task Added")

    elif choice == "2":
        print("Show Tasks")
        print("\nYour Tasks :")
        for i ,task in enumerate(tasks ,start=1):
            if task["complete"]:
                status = "✓"
            else:
                status = " "

            print(f"{i}.[{status}] {task['title']} {task['date']} {task['time']}")

    elif choice == "3":
        print("Complete Task")
        number = int(input("Enter Complete tasks number"))

        tasks[number-1]["complete"] = True 
        print(f"Task :{number} Complete!!")
        save_task()

    elif choice == "4":
        print("Delete Tasks")
        Dnum = int(input("Delete Task number :"))
        tasks.pop(Dnum -1)
        save_task()
        print("Task Deleted")

    elif choice == "5":
        print("Exit")
        break

    else:
        print("***Invalid Input Value***")