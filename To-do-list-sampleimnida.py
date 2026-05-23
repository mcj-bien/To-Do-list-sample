# main.py

from gui_layout import create_gui
from file_handler import load_tasks
from task_actions import tasks

load_tasks(tasks)

root = create_gui(tasks)

root.mainloop()