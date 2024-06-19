import tkinter as tk
from tkinter import filedialog
class AutoOpenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Open Application")
        try:
            self.iconbitmap("autopen.ico")
        except Exception as e:
            print(e)
        self.file_paths = []

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entries for file path
        # Labels and Entries for program name
        tk.Label(self, text="Program Name:").grid(row=0, column=0, sticky="w")
        self.program_name_var = tk.StringVar()
        self.program_name_entry = tk.Entry(self, width=50, textvariable=self.program_name_var)
        self.program_name_entry.grid(row=0, column=1, columnspan=3)
        tk.Label(self, text="File Path:").grid(row=1, column=0, sticky="w")
        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(self, width=50, textvariable=self.file_path_var)
        self.file_path_entry.grid(row=1, column=1, columnspan=3)
        tk.Button(self, text="Browse", command=self.browse_file).grid(row=1, column=4, padx=10)

        # Labels and Entries for hour, minute, and AM/PM
        tk.Label(self, text="Hour:").grid(row=2, column=0, sticky="w")
        self.hour_var = tk.IntVar()
        self.hour_entry = tk.Entry(self, width=5, textvariable=self.hour_var)
        self.hour_entry.grid(row=2, column=1, sticky="w")
        tk.Label(self, text="Minute:").grid(row=2, column=2, padx=10, sticky="w")
        self.minute_var = tk.IntVar()
        self.minute_entry = tk.Entry(self, width=5, textvariable=self.minute_var)
        self.minute_entry.grid(row=2, column=3, sticky="w")
        tk.Label(self, text="AM/PM:").grid(row=2, column=4, padx=10, sticky="w")
        self.am_pm_var = tk.StringVar(value="AM")
        self.am_pm_entry = tk.Entry(self, width=5, textvariable=self.am_pm_var)
        self.am_pm_entry.grid(row=2, column=5, sticky="w")

        # Button to add file and time to listbox
        tk.Button(self, text="Add", command=self.add_to_listbox).grid(row=2, column=6, padx=10)

        # Listbox to display added files and times
        self.listbox = tk.Listbox(self, width=60, height=10)
        self.listbox.grid(row=3, column=0, columnspan=7, padx=10, pady=10)
        self.load_data()
        # Button to delete selected file and time from listbox
        tk.Button(self, text="Delete", command=self.delete_file).grid(row=4, column=0, pady=5)

        # Button to refresh the application
        tk.Button(self, text="Refresh", command=self.refresh_app).grid(row=4, column=6, pady=5)
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_var.set(file_path)

    def add_to_listbox(self):
        program_name = self.program_name_var.get()
        path = self.file_path_var.get()
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        am_pm = self.am_pm_var.get()

        if program_name and path and hour != "" and minute != "":
            time_str = f"{hour:02d}:{minute:02d} {am_pm.upper()}"
            entry = f"{program_name} - {path} - {time_str}"
            le = f"{program_name} - {time_str} - {path}"
            self.listbox.insert(tk.END, le)
            self.file_paths.append((entry,))
            self.program_name_var.set('')
            self.file_path_var.set('')
            self.hour_var.set(0)
            self.minute_var.set(0)
            self.am_pm_var.set("AM")
            self.save_data()

    def delete_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.listbox.delete(selected_index)
            del self.file_paths[selected_index[0]]
            self.save_data()

    def refresh_app(self):
        self.file_path_var.set('')
        self.hour_var.set(0)
        self.minute_var.set(0)
        self.am_pm_var.set("AM")

    def save_data(self):
        with open("data.txt", "w", encoding="utf-8") as file:
            for entry in self.file_paths:
                file.write(f"{entry[0]}\n")

    def load_data(self):
        try:
            with open("data.txt", "r", encoding="utf-8") as file:
                for line in file:
                    name,file_path, time_str = line.strip().split(" - ")
                    self.file_paths.append((name,file_path, time_str))
                    self.listbox.insert(tk.END, f"{name} - {time_str} - {file_path}")
        except FileNotFoundError:
            pass

    '''def check_and_open_files(self):
        while True:
            now = datetime.datetime.now().strftime("%I:%M %p")  # Lấy thời gian hiện tại (ví dụ: 01:30 PM)
            for file_path, time_str in self.file_paths:
                if self.is_time_to_open(now, time_str) and not  self.is_file_open(file_path):
                    self.show_open_file_notification(file_path)
            time.sleep(30)
            #time.sleep(9000)'''

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = AutoOpenApp()
    app.run()
