# main.py

from gui_layout import create_gui
from file_handler import load_tasks
from task_actions import tasks

# file_handler.py

from tkinter import messagebox

FILE = "tasks.txt"

def load_tasks(tasks):

    try:
        with open(FILE, "r") as f:

            for line in f:

                line = line.strip()

                if "|" in line:

                    parts = line.split("|", 2)

                    if len(parts) == 3:

                        tasks.append({
                            "name": parts[0],
                            "status": parts[1],
                            "desc": parts[2]
                        })

    except FileNotFoundError:
        pass

    except Exception as e:
        messagebox.showerror(
            "Load Error",
            f"Could not load tasks:\n{e}"
        )


def save_tasks(tasks):

    try:

        with open(FILE, "w") as f:

            for t in tasks:

                f.write(
                    f"{t['name']}|{t['status']}|{t['desc']}\n"
                )

    except Exception as e:

        messagebox.showerror(
            "Save Error",
            f"Could not save tasks:\n{e}"
        )


def append_task(task):

    try:

        with open(FILE, "a") as f:

            f.write(
                f"{task['name']}|{task['status']}|{task['desc']}\n"
            )

    except Exception as e:

        messagebox.showerror(
            "Append Error",
            f"Could not append task:\n{e}"
        )

load_tasks(tasks)

root = create_gui(tasks)

root.mainloop()