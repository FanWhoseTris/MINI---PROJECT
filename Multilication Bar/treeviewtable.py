import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar

class SearchBar:

    def __init__(self, root):
        self.master = root
        self.master.title("Sentences Table")
        self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight() // 2}+0+0")
        self.master.configure(bg="#222121")
        self.master.attributes('-alpha', 0.7)
        self.master.attributes('-toolwindow', True)
        self.master.attributes('-topmost', True)
        self.create_gui()
        self.chay()

    def create_gui(self):
        self.tree = ttk.Treeview(self.master, columns=("id", "sentence", "times"), show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("sentence", text="Sentence")
        self.tree.heading("times", text="Times")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("sentence", width=300, anchor=tk.W)
        self.tree.column("times", width=100, anchor=tk.CENTER)

        # Add a vertical scrollbar
        scrollbar = Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('Database/sentences.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sentences")
        rows = cursor.fetchall()
        conn.close()

        # Clear existing data
        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def chay(self):
        self.load_data()
        self.master.after(3600000, self.chay)  # Refresh every hour (3600000 milliseconds)

    def hide_window(self):
        self.master.withdraw()

    def show_window(self):
        self.master.deiconify()

    def clear_all_widgets(self, root):
        for widget in root.winfo_children():
            widget.destroy()

    def closing(self, para=None):
        self.clear_all_widgets(self.master)
        try:
            self.master.destroy()
        except:
            return

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    search_bar = tk.Toplevel(root)
    SB = SearchBar(search_bar)
    search_bar.mainloop()
