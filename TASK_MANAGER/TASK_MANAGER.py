import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
from pathlib import Path


# =========================================================
# FILE
# =========================================================

FILE_NAME = Path(__file__).parent / "tasks.json"


# =========================================================
# LOAD TASKS
# =========================================================

def load_tasks():

    try:
        with open(FILE_NAME, "r") as file:
            tasks = json.load(file)

            # Make old V2/V3 tasks compatible
            for task in tasks:

                if "priority" not in task:
                    task["priority"] = "Medium"

                if "due_date" not in task:
                    task["due_date"] = "No due date"

            return tasks

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:

        messagebox.showerror(
            "Error",
            "tasks.json is corrupted or empty."
        )

        return []


# =========================================================
# SAVE TASKS
# =========================================================

def save_tasks():

    with open(FILE_NAME, "w") as file:

        json.dump(
            tasks,
            file,
            indent=4
        )


# =========================================================
# DISPLAY TASKS
# =========================================================

# This list stores the actual indexes of the tasks
# currently displayed in the Listbox.

displayed_indices = []


def refresh_tasks(indices=None):

    global displayed_indices

    listbox.delete(
        0,
        tk.END
    )

    # If no indexes are supplied,
    # display every task.
    if indices is None:

        displayed_indices = list(
            range(len(tasks))
        )

    else:

        displayed_indices = indices

    # Display the selected tasks

    for index in displayed_indices:

        task = tasks[index]

        if task["completed"]:
            status = "✓"
        else:
            status = "☐"

        priority = task.get(
            "priority",
            "Medium"
        )

        due_date = task.get(
            "due_date",
            "No due date"
        )

        display_text = (
            f"{status}  "
            f"{task['task']}  |  "
            f"Priority: {priority}  |  "
            f"Due: {due_date}"
        )

        listbox.insert(
            tk.END,
            display_text
        )


# =========================================================
# GET SELECTED TASK
# =========================================================

def get_selected_index():

    selected = listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a task first."
        )

        return None

    listbox_index = selected[0]

    # Convert displayed Listbox index
    # into the actual tasks[] index.

    actual_index = displayed_indices[
        listbox_index
    ]

    return actual_index


# =========================================================
# 1. ADD TASK
# =========================================================

def add_task():

    task_name = task_entry.get().strip()

    if task_name == "":

        messagebox.showwarning(
            "Warning",
            "Task cannot be empty!"
        )

        return

    priority = new_priority_var.get()

    due_date = due_date_entry.get().strip()

    # No date entered
    if due_date == "":

        due_date = "No due date"

    else:

        try:

            datetime.strptime(
                due_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format."
            )

            return

    new_task = {

        "task": task_name,

        "completed": False,

        "priority": priority,

        "due_date": due_date
    }

    tasks.append(
        new_task
    )

    save_tasks()

    refresh_tasks()

    # Clear input fields

    task_entry.delete(
        0,
        tk.END
    )

    due_date_entry.delete(
        0,
        tk.END
    )

    new_priority_var.set(
        "Medium"
    )

    messagebox.showinfo(
        "Success",
        "Task added successfully!"
    )


# =========================================================
# 2. VIEW TASKS
# =========================================================

def view_tasks():

    # Reset filters

    search_entry.delete(
        0,
        tk.END
    )

    filter_priority_var.set(
        "All"
    )

    filter_status_var.set(
        "All"
    )

    refresh_tasks()

    if len(tasks) == 0:

        messagebox.showinfo(
            "Tasks",
            "No tasks found!"
        )


# =========================================================
# 3. COMPLETE TASK
# =========================================================

def complete_task():

    index = get_selected_index()

    if index is None:
        return

    task = tasks[index]

    if task["completed"]:

        messagebox.showinfo(
            "Information",
            "Task is already completed!"
        )

        return

    task["completed"] = True

    save_tasks()

    refresh_tasks(
        displayed_indices
    )

    messagebox.showinfo(
        "Success",
        "Task completed successfully!"
    )


# =========================================================
# 4. DELETE TASK
# =========================================================

def delete_task():

    index = get_selected_index()

    if index is None:
        return

    task = tasks[index]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete '{task['task']}'?"
    )

    if confirm:

        tasks.pop(index)

        save_tasks()

        # Refresh everything
        refresh_tasks()

        messagebox.showinfo(
            "Success",
            "Task deleted successfully!"
        )


# =========================================================
# 5. EDIT TASK
# =========================================================

def edit_task():

    index = get_selected_index()

    if index is None:
        return

    task = tasks[index]

    # Put old task information into input fields

    task_entry.delete(
        0,
        tk.END
    )

    task_entry.insert(
        0,
        task["task"]
    )

    new_priority_var.set(
        task.get(
            "priority",
            "Medium"
        )
    )

    due_date_entry.delete(
        0,
        tk.END
    )

    old_date = task.get(
        "due_date",
        "No due date"
    )

    if old_date != "No due date":

        due_date_entry.insert(
            0,
            old_date
        )

    # Remember which task is being edited

    global editing_index

    editing_index = index

    # Change Add Task button into Save Edit

    add_button.config(
        text="Save Edit",
        command=save_edit
    )

    messagebox.showinfo(
        "Edit Task",
        "Edit the fields and click 'Save Edit'."
    )


# =========================================================
# SAVE EDIT
# =========================================================

def save_edit():

    global editing_index

    if editing_index is None:
        return

    task_name = task_entry.get().strip()

    if task_name == "":

        messagebox.showwarning(
            "Warning",
            "Task cannot be empty!"
        )

        return

    priority = new_priority_var.get()

    due_date = due_date_entry.get().strip()

    if due_date == "":

        due_date = "No due date"

    else:

        try:

            datetime.strptime(
                due_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format."
            )

            return

    # Update the existing task

    tasks[editing_index]["task"] = task_name

    tasks[editing_index]["priority"] = priority

    tasks[editing_index]["due_date"] = due_date

    save_tasks()

    # Reset edit mode

    editing_index = None

    add_button.config(
        text="Add Task",
        command=add_task
    )

    # Clear fields

    task_entry.delete(
        0,
        tk.END
    )

    due_date_entry.delete(
        0,
        tk.END
    )

    new_priority_var.set(
        "Medium"
    )

    refresh_tasks()

    messagebox.showinfo(
        "Success",
        "Task updated successfully!")


# =========================================================
# 6. SEARCH TASK
# =========================================================

def search_tasks():

    search_text = search_entry.get().strip().lower()

    if search_text == "":

        refresh_tasks()

        return

    results = []

    for index, task in enumerate(tasks):

        if search_text in task["task"].lower():

            results.append(index)

    refresh_tasks(
        results
    )

    if len(results) == 0:

        messagebox.showinfo(
            "Search",
            "No matching tasks found!"
        )


# =========================================================
# 7. FILTER TASKS
# =========================================================

def filter_tasks():

    selected_priority = filter_priority_var.get()

    selected_status = filter_status_var.get()

    results = []

    for index, task in enumerate(tasks):

        priority_match = True
        status_match = True

        # Priority filter

        if selected_priority != "All":

            if task.get(
                "priority",
                "Medium"
            ) != selected_priority:

                priority_match = False

        # Status filter

        if selected_status == "Completed":

            if not task["completed"]:

                status_match = False

        elif selected_status == "Pending":

            if task["completed"]:

                status_match = False

        # If both filters match,
        # add the task.

        if priority_match and status_match:

            results.append(index)

    refresh_tasks(
        results
    )

    if len(results) == 0:

        messagebox.showinfo(
            "Filter",
            "No tasks match the selected filters."
        )


# =========================================================
# 8. EXIT
# =========================================================

def exit_program():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:

        root.destroy()


# =========================================================
# CLEAR SEARCH
# =========================================================

def show_all():

    search_entry.delete(
        0,
        tk.END
    )

    filter_priority_var.set(
        "All"
    )

    filter_status_var.set(
        "All"
    )

    refresh_tasks()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "To-Do Manager V4"
)

root.geometry(
    "900x600"
)

root.resizable(
    False,
    False
)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="TO-DO MANAGER V4",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=20
)


# =========================================================
# INPUT FRAME
# =========================================================

input_frame = tk.Frame(root)

input_frame.pack(
    pady=10
)


# Task

tk.Label(
    input_frame,
    text="Task:"
).grid(
    row=0,
    column=0,
    padx=5
)

task_entry = tk.Entry(
    input_frame,
    width=35
)

task_entry.grid(
    row=0,
    column=1,
    padx=5
)


# NEW TASK PRIORITY

tk.Label(
    input_frame,
    text="New Task Priority:"
).grid(
    row=0,
    column=2,
    padx=5
)

new_priority_var = tk.StringVar()

new_priority_var.set(
    "Medium"
)

new_priority_menu = tk.OptionMenu(
    input_frame,
    new_priority_var,
    "High",
    "Medium",
    "Low"
)

new_priority_menu.grid(
    row=0,
    column=3,
    padx=5
)


# Due Date

tk.Label(
    input_frame,
    text="Due Date:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=10
)

due_date_entry = tk.Entry(
    input_frame,
    width=20
)

due_date_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=10
)


tk.Label(
    input_frame,
    text="YYYY-MM-DD"
).grid(
    row=1,
    column=2,
    padx=5
)


# Add / Save Edit button

add_button = tk.Button(
    input_frame,
    text="Add Task",
    command=add_task,
    width=12
)

add_button.grid(
    row=1,
    column=3,
    padx=5
)


# =========================================================
# SEARCH FRAME
# =========================================================

search_frame = tk.Frame(root)

search_frame.pack(
    pady=10
)


tk.Label(
    search_frame,
    text="Search Task:"
).pack(
    side=tk.LEFT,
    padx=5
)


search_entry = tk.Entry(
    search_frame,
    width=30
)

search_entry.pack(
    side=tk.LEFT,
    padx=5
)


search_button = tk.Button(
    search_frame,
    text="Search Task",
    command=search_tasks,
    width=12
)

search_button.pack(
    side=tk.LEFT,
    padx=5
)


show_button = tk.Button(
    search_frame,
    text="Show All",
    command=show_all,
    width=12
)

show_button.pack(
    side=tk.LEFT,
    padx=5
)


# =========================================================
# FILTER FRAME
# =========================================================

filter_frame = tk.Frame(root)

filter_frame.pack(
    pady=10
)


# FILTER PRIORITY

tk.Label(
    filter_frame,
    text="Filter Priority:"
).pack(
    side=tk.LEFT,
    padx=5
)


filter_priority_var = tk.StringVar()

filter_priority_var.set(
    "All"
)

filter_priority_menu = tk.OptionMenu(
    filter_frame,
    filter_priority_var,
    "All",
    "High",
    "Medium",
    "Low"
)

filter_priority_menu.pack(
    side=tk.LEFT,
    padx=5
)


# FILTER STATUS

tk.Label(
    filter_frame,
    text="Filter Status:"
).pack(
    side=tk.LEFT,
    padx=10
)


filter_status_var = tk.StringVar()

filter_status_var.set(
    "All"
)

filter_status_menu = tk.OptionMenu(
    filter_frame,
    filter_status_var,
    "All",
    "Pending",
    "Completed"
)

filter_status_menu.pack(
    side=tk.LEFT,
    padx=5
)


filter_button = tk.Button(
    filter_frame,
    text="Filter Tasks",
    command=filter_tasks,
    width=12
)

filter_button.pack(
    side=tk.LEFT,
    padx=10
)


# =========================================================
# TASK LIST
# =========================================================

list_frame = tk.Frame(root)

list_frame.pack(
    pady=15
)


scrollbar = tk.Scrollbar(
    list_frame
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


listbox = tk.Listbox(
    list_frame,
    width=105,
    height=9,
    font=("Arial", 11),
    yscrollcommand=scrollbar.set
)

listbox.pack(
    side=tk.LEFT
)


scrollbar.config(
    command=listbox.yview
)


# =========================================================
# 8 V3 MENU ITEMS
# =========================================================

menu_label = tk.Label(
    root,
    text="MENU",
    font=("Arial", 14, "bold")
)

menu_label.pack(
    pady=5
)


button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)


# 1. ADD

add_menu_button = tk.Button(
    button_frame,
    text="1. Add Task",
    command=add_task,
    width=15
)

add_menu_button.grid(
    row=0,
    column=0,
    padx=5
)


# 2. VIEW

view_button = tk.Button(
    button_frame,
    text="2. View Tasks",
    command=view_tasks,
    width=15
)

view_button.grid(
    row=0,
    column=1,
    padx=5
)


# 3. COMPLETE

complete_button = tk.Button(
    button_frame,
    text="3. Complete Task",
    command=complete_task,
    width=15
)

complete_button.grid(
    row=0,
    column=2,
    padx=5
)


# 4. DELETE

delete_button = tk.Button(
    button_frame,
    text="4. Delete Task",
    command=delete_task,
    width=15
)

delete_button.grid(
    row=0,
    column=3,
    padx=5
)


# 5. EDIT

edit_button = tk.Button(
    button_frame,
    text="5. Edit Task",
    command=edit_task,
    width=15
)

edit_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=8
)


# 6. SEARCH

search_menu_button = tk.Button(
    button_frame,
    text="6. Search Task",
    command=search_tasks,
    width=15
)

search_menu_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=8
)


# 7. FILTER

filter_menu_button = tk.Button(
    button_frame,
    text="7. Filter Tasks",
    command=filter_tasks,
    width=15
)

filter_menu_button.grid(
    row=1,
    column=2,
    padx=5,
    pady=8
)


# 8. EXIT

exit_button = tk.Button(
    button_frame,
    text="8. Exit",
    command=exit_program,
    width=15
)

exit_button.grid(
    row=1,
    column=3,
    padx=5,
    pady=8
)


# =========================================================
# GLOBAL VARIABLES
# =========================================================

tasks = load_tasks()

editing_index = None


# =========================================================
# SHOW INITIAL TASKS
# =========================================================

refresh_tasks()


# =========================================================
# START GUI
# =========================================================

root.mainloop()