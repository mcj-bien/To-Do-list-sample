# main.py

# =========================================================
# FILE: main.py
# MEMBER 1 — MAIN PROGRAM
# =========================================================

from gui_layout import create_gui
from file_handler import load_tasks
from task_actions import tasks

load_tasks(tasks)

root = create_gui(tasks)

root.mainloop()


# =========================================================
# FILE: file_handler.py
# MEMBER 2 — FILE HANDLING
# =========================================================

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


# =========================================================
# FILE: task_actions.py
# MEMBER 3 — TASK ACTIONS
# =========================================================

from tkinter import messagebox
from file_handler import save_tasks, append_task

tasks = []

def add_task(entry_name, entry_desc, tree, refresh_table):

    name = entry_name.get().strip()

    desc = entry_desc.get().strip()

    if not name:

        messagebox.showwarning(
            "Validation",
            "Task name cannot be empty!"
        )

        return

    if not desc:

        messagebox.showwarning(
            "Validation",
            "Description cannot be empty!"
        )

        return

    task = {
        "name": name,
        "status": "Pending",
        "desc": desc
    }

    tasks.append(task)

    append_task(task)

    refresh_table()

    entry_name.delete(0, "end")

    entry_desc.delete(0, "end")


def mark_done(tree, refresh_table):

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Select",
            "Please select a task first."
        )

        return

    i = tree.index(selected[0])

    tasks[i]["status"] = "Done"

    save_tasks(tasks)

    refresh_table()


def delete_task(tree, refresh_table):

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Select",
            "Please select a task first."
        )

        return

    i = tree.index(selected[0])

    tasks.pop(i)

    save_tasks(tasks)

    refresh_table()


# =========================================================
# FILE: gui_layout.py
# MEMBER 4 — GUI LAYOUT
# =========================================================

import tkinter as tk
from tkinter import ttk

from task_actions import (
    add_task,
    mark_done,
    delete_task,
    tasks
)

from styles import apply_styles


def create_gui(tasks_list):

    root = tk.Tk()

    root.title("To-Do List Manager")

    root.geometry("640x460")

    root.resizable(False, False)

    # INPUT FRAME

    frame_input = tk.LabelFrame(
        root,
        text=" Add New Task ",
        padx=10,
        pady=8
    )

    frame_input.pack(fill="x", padx=12, pady=(10, 4))

    tk.Label(
        frame_input,
        text="Task Name:"
    ).grid(row=0, column=0)

    entry_name = tk.Entry(
        frame_input,
        width=35
    )

    entry_name.grid(row=0, column=1)

    tk.Label(
        frame_input,
        text="Description:"
    ).grid(row=1, column=0)

    entry_desc = tk.Entry(
        frame_input,
        width=35
    )

    entry_desc.grid(row=1, column=1)

    # BUTTON FRAME

    frame_btn = tk.Frame(root)

    frame_btn.pack(fill="x", padx=12, pady=4)

    # TABLE FRAME

    frame_table = tk.LabelFrame(
        root,
        text=" Task Records "
    )

    frame_table.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=4
    )

    cols = ("#", "Task Name", "Status", "Description")

    tree = ttk.Treeview(
        frame_table,
        columns=cols,
        show="headings",
        height=10
    )

    for col in cols:

        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True)

    status_var = tk.StringVar()

    def refresh_table():

        for row in tree.get_children():

            tree.delete(row)

        for idx, t in enumerate(tasks, start=1):

            tree.insert(
                "",
                tk.END,
                values=(
                    idx,
                    t["name"],
                    t["status"],
                    t["desc"]
                )
            )

        total = len(tasks)

        done = sum(
            1 for t in tasks
            if t["status"] == "Done"
        )

        status_var.set(
            f"Total: {total} Done: {done}"
        )

    tk.Button(
        frame_input,
        text="Add Task",
        command=lambda: add_task(
            entry_name,
            entry_desc,
            tree,
            refresh_table
        )
    ).grid(row=0, column=2, rowspan=2)

    tk.Button(
        frame_btn,
        text="Mark Done",
        command=lambda: mark_done(
            tree,
            refresh_table
        )
    ).pack(side="left")

    tk.Button(
        frame_btn,
        text="Delete Task",
        command=lambda: delete_task(
            tree,
            refresh_table
        )
    ).pack(side="left")

    tk.Label(
        root,
        textvariable=status_var,
        relief="sunken"
    ).pack(fill="x", side="bottom")

    apply_styles(tree)

    refresh_table()

    return root


# =========================================================
# FILE: styles.py
# MEMBER 5 — STYLING & DOCUMENTATION
# =========================================================

def apply_styles(tree):

    tree.tag_configure(
        "done",
        foreground="gray"
    )

    tree.tag_configure(
        "pending",
        foreground="black"
    )