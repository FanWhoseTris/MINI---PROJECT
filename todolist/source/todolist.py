import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("476x421")
        self.iconbitmap('icontodo.ico')
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.create_task_table()

        self.task_list = []

        self.create_widgets()
        self.load_tasks()

    def create_task_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), start_date TEXT, completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))"
        )
        self.conn.commit()

    def create_widgets(self):
        self.task_entry = tk.Entry(self, width=40)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=3, padx=5)

        # Date and time selection widgets
        self.date_label = tk.Label(self, text="Date:")
        self.date_label.grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self, width=12)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.time_label = tk.Label(self, text="Time:")
        self.time_label.grid(row=1, column=2, padx=5, pady=5)
        self.time_entry = tk.Entry(self, width=10)
        self.time_entry.grid(row=1, column=3, padx=5, pady=5)

        self.task_listbox = tk.Listbox(self, width=60, height=15)
        self.task_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=3, column=0, padx=5)
        self.complete_button = tk.Button(self, text="Mark Complete", command=self.mark_complete)
        self.complete_button.grid(row=3, column=1, padx=5)
        self.load_button = tk.Button(self, text="Refresh", command=self.load_tasks)
        self.load_button.grid(row=3, column=3, padx=5)



    def add_task(self):
        task = self.task_entry.get().strip()
        start_date = self.date_entry.get().strip()
        start_time = self.time_entry.get().strip()

        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return

        due_date = "Not specified"
        if start_date and start_time:
            due_date = f"{start_date} {start_time}"

        self.cursor.execute("INSERT INTO tasks(task, due_date, start_date, completed) VALUES(?, ?, ?, ?)",
                            (task, due_date, start_date, 0))
        self.conn.commit()
        self.task_listbox.insert(tk.END, f"[ ] {task} (Start: {due_date})")
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = self.task_list[selected_index[0]][0]
            self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            self.conn.commit()
            self.load_tasks()

    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = self.task_list[selected_index[0]][0]
            print(task_id)
            self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
            self.conn.commit()
            self.load_tasks()

    def unmark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = self.task_list[selected_index[0]][0]
            print(task_id)
            self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
            self.conn.commit()
            self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.task_list.clear()
        incomplete_tasks = self.cursor.execute("SELECT id, task, due_date, start_date FROM tasks WHERE completed = 0").fetchall()
        for task in incomplete_tasks:
            start_date = task[2] if task[2] and task[2] != "Not specified" else "Not specified"
            self.task_listbox.insert(tk.END, f"[ ] {task[1]} |(Start: {start_date})")
            self.task_list.append(task)

        completed_tasks = self.cursor.execute("SELECT id, task, due_date, start_date FROM tasks WHERE completed = 1").fetchall()
        for task in completed_tasks:
            start_date = task[2] if task[2] and task[2] != "Not specified" else "Not specified"
            self.task_listbox.insert(tk.END, f"[X] {task[1]} |(Start: {start_date})")
            self.task_list.append(task)
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
