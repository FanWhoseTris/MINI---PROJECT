import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime, timedelta


class ShutdownScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Shutdown Scheduler")
        self.root.geometry("350x300")  # Kích thước cửa sổ
        self.root.attributes("-topmost", True)

        self.create_widgets()
        self.still = True

    def create_widgets(self):
        # Nhãn tiêu đề
        self.title_label = tk.Label(self.root, text="Shutdown Scheduler", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Nhãn và ô nhập liệu thời gian
        self.time_label = tk.Label(self.root, text="Enter time (minutes):", font=("Helvetica", 12))
        self.time_label.pack(pady=5)

        self.time_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.time_entry.pack(pady=5)

        # Nút Ok
        self.schedule_button = tk.Button(self.root, text="Ok", font=("Helvetica", 12, "bold"), bg="#5cb85c", fg="white",
                                         command=self.schedule_shutdown)
        self.schedule_button.pack(pady=10)

        # Nút Cancel
        self.cancel_button = tk.Button(self.root, text="Cancel", font=("Helvetica", 12, "bold"), bg="#d9534f",
                                       fg="white", command=self.cancel_shutdown)
        self.cancel_button.pack(pady=5)

        # Nhãn đếm ngược thời gian
        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.countdown_label.pack(pady=5)

        # Nhãn hiển thị thời gian tắt máy cụ thể
        self.scheduled_time_label = tk.Label(self.root, text="", font=("Helvetica", 12, "italic"))
        self.scheduled_time_label.pack(pady=5)

    def schedule_shutdown(self):
        try:
            minutes = self.time_entry.get()

            # Kiểm tra xem đầu vào có chứa ký tự không phải số không
            if not minutes.strip():
                return
            if not minutes.isdigit():
                raise ValueError("Invalid Input")

            minutes = int(minutes)
            seconds = minutes * 60

            # Lập lệnh tắt máy ngay lập tức
            shutdown_time = datetime.now() + timedelta(seconds=seconds)
            shutdown_time_str = shutdown_time.strftime("%H:%M:%S, %d/%m/%Y")
            self.scheduled_time_label.config(text=f"Scheduled Shutdown at: {shutdown_time_str}")

            os.system(f"shutdown /s /t {seconds}")  # Windows
            # os.system(f"sudo shutdown -h +{minutes}")  # Linux/Unix/MacOS
            self.still = True

            self.start_countdown(seconds)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def start_countdown(self, seconds):
        if seconds > 0 and self.still:
            mins, secs = divmod(seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.countdown_label.config(text=f"Shutting down in: {timeformat}")
            self.root.after(1000, self.start_countdown, seconds - 1)

    def cancel_shutdown(self):
        try:
            os.system("shutdown /a")  # Hủy lệnh tắt máy trong Windows
            self.countdown_label.config(text="Shutdown canceled.")
            self.scheduled_time_label.config(text="")
            self.still = False
        except:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownScheduler(root)
    root.mainloop()
