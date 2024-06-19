import tkinter as tk
import os
import webbrowser
from tkinter import messagebox
import datetime
import sys

class FileOpenerApp:
    def __init__(self):
        self.file_paths = []
        self.load_data()
        self.check_and_open_files()

    def load_data(self):
        try:
            with open("data.txt", "r", encoding="utf-8") as file:
                for line in file:
                    name, file_path, time_str = line.strip().split(" - ")
                    self.file_paths.append((name, file_path, time_str))
        except FileNotFoundError:
            pass

    def check_and_open_files(self):
        now = datetime.datetime.now()
        opened_any = False  # Đánh dấu xem có mở tệp nào hay không
        for name, file_path, time_str in self.file_paths:
            if self.is_time_to_open(now, time_str):
                #print("ok---------------------")
                self.show_open_file_notification(name, file_path)
                opened_any = True
        if not opened_any:
            #print("Không có đường dẫn nào cần mở. Chương trình sẽ được tắt.")
            # Thoát chương trình khi không có đường dẫn cần mở
            exit()
    def is_time_to_open(self, now, time_str):
        hour = now.hour  # Lấy giờ
        minute = now.minute  # Lấy phút
        #print(f"Giờ: {hour}")
        #print(f"Phút: {minute}")
        time_hour, time_minute, time_ampm = self.parse_time(time_str)
        if time_ampm == 'PM':
            time_hour = self.convert_12_hour_to_24_hour(time_hour,time_ampm)
        #print(f"{time_hour}-{time_minute}-{time_ampm}")

        if hour == int(time_hour):
            if minute >= time_minute:
                return True
        elif hour > int(time_hour):
            return True

        return False

    def convert_12_hour_to_24_hour(self, hour_str, am_pm):
        # Chuyển chuỗi giờ và am_pm sang đối tượng datetime
        time_str = f"{hour_str} {am_pm}"
        time_obj = datetime.datetime.strptime(time_str, "%I %p")

        # Chuyển đối tượng datetime về chuỗi định dạng 24 giờ
        time_24_hour = time_obj.strftime("%H")

        return time_24_hour

    def parse_time(self,time_str):
        time_parts = time_str.split(" ")
        hour, minute = map(int, time_parts[0].split(":"))
        am_pm = time_parts[1].upper()
        return hour, minute, am_pm

    def show_open_file_notification(self, name, path):
        message = f"Bạn có muốn mở {name}?\n\n =====>>>{path}"
        if tk.messagebox.askyesno("Open Path", message):
            self.open_path(path)


    def open_path(self,path):
        try:
            if os.path.exists(path):
                os.startfile(path)
                print(f"Opening {path}")
            else:
                webbrowser.open(path)
                print(f"Opening web link: {path}")
        except Exception as e:
            print(f"Error opening path: {e}")

if __name__ == "__main__":
    app = FileOpenerApp()
