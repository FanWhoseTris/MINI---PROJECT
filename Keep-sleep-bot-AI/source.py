try:
    import tkinter as tk
    from tkinter import simpledialog
    from datetime import datetime
    import subprocess
    import os
    import time


    class Thongbao:
        def __init__(self, time):
            self.time = time
            self.root = tk.Tk()

        def show_notification(self):
            self.root.title("Thông Báo")
            self.root.attributes('-topmost', True)
            self.root.geometry("1000x500+300+100")
            thoi_gian_hien_tai = datetime.now()
            self.root.config(bg="red")
            try:
                icon_path = "revise.ico"
                self.root.iconbitmap(default=icon_path)
            except Exception as e:
                print(e)

            # Tạo và đặt nhãn thứ nhất
            self.label1 = tk.Label(self.root, text="Trí ơi", font=("Arial", 52, "underline"), bg="yellow")
            self.label1.pack(pady=10)  # Thêm khoảng cách dưới nhãn

            # Tạo và đặt nhãn thứ hai
            self.label2 = tk.Label(self.root, text="Tập trung vào!", font=("Arial", 61), bg="yellow")
            self.label2.pack(pady=10)  # Thêm khoảng cách dưới nhãn

            # Tạo và đặt nhãn thứ ba
            thoi_gian_con_lai = self.time - thoi_gian_hien_tai
            gio_con_lai = int(thoi_gian_con_lai.total_seconds() // 3600)
            phut_con_lai = int((thoi_gian_con_lai.total_seconds() % 3600) // 60)
            # os.system(f"shutdown /a")
            # os.system(f"shutdown /s /t {thoi_gian_con_lai.total_seconds()}")
            self.label3 = tk.Label(self.root, text=f"Bạn chỉ còn {gio_con_lai} giờ {phut_con_lai} phút",
                                   font=("Arial", 61),
                                   bg="yellow")
            self.label3.pack(pady=10)  # Thêm khoảng cách dưới nhãn

            # Gắn kết sự kiện nhấn phím Space với hàm click_button
            self.root.bind("<space>", self.click_button)

            # Tạo nút nhấn
            self.button = tk.Button(self.root, text="Tôi sẽ tập trung", command=lambda: self.click_button(),
                                    font=("Arial", 34),
                                    fg="red", bg="yellow")
            self.button.pack(pady=20)  # Thêm khoảng cách dưới nút

            # Tạo nút Set để đặt số giờ kết thúc
            self.sb = tk.Button(self.root, text="Set", command=self.set_end_time, font=("Arial", 16))
            self.sb.pack(side=tk.LEFT)
            self.cb = tk.Button(self.root, text="Count", command=lambda: self.open_file(), font=("Arial", 16))
            self.cb.pack(side=tk.RIGHT)

            self.root.mainloop()

        def set_end_time(self):
            # Hiển thị hộp thoại để nhập số giờ kết thúc
            h = simpledialog.askinteger("Đặt thời gian kết thúc", "Nhập số giờ:")
            m = simpledialog.askinteger("Đặt thời gian kết thúc", "Nhập số phút:")
            thoi_gian_moc = datetime(datetime.now().year, datetime.now().month, datetime.now().day, h, m)
            if h is not None and m is not None:
                # Lưu số giờ kết thúc vào tệp time.txt
                with open("time.txt", "w") as f:
                    f.write(str(thoi_gian_moc))
                self.up(thoi_gian_moc)
            return

        def up(self, time):
            self.time = time
            thoi_gian_hien_tai = datetime.now()
            # print(self.time)
            # print(thoi_gian_hien_tai)
            thoi_gian_con_lai = self.time - thoi_gian_hien_tai
            gio_con_lai = int(thoi_gian_con_lai.total_seconds() // 3600)
            phut_con_lai = int((thoi_gian_con_lai.total_seconds() % 3600) // 60)
            self.label3.config(text=f"Bạn chỉ còn {gio_con_lai} giờ {phut_con_lai} phút")
            # os.system(f"shutdown /a")
            # os.system(f"shutdown /s /t {thoi_gian_con_lai.total_seconds()}")
            return

        def open_file(self):
            file_path = 'sleep.py'
            try:
                if os.path.exists(file_path):
                    subprocess.Popen(["python", file_path])
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                # Nếu tệp .py không tồn tại, thử mở tệp .exe thay thế
                exe_file = os.path.splitext(file_path)[0] + ".exe"
                if os.path.exists(exe_file):
                    subprocess.Popen([exe_file])
                else:
                    print(f"File not found: {file_path} or {exe_file}")

        def click_button(self, event=None):
            self.root.destroy()


    def open_file(file_path):
        try:
            if os.path.exists(file_path):
                subprocess.Popen(["python", file_path])
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            # Nếu tệp .py không tồn tại, thử mở tệp .exe thay thế
            exe_file = os.path.splitext(file_path)[0] + ".exe"
            if os.path.exists(exe_file):
                subprocess.Popen([exe_file])
            else:
                print(f"File not found: {file_path} or {exe_file}")


    if __name__ == "__main__":
        start_time = 21
        minu = 0
        with open("time.txt", "r") as f:
            line = f.readlines()
        lin = line[0].split(" ")
        lines = lin[1].split(":")
        # print(lines[0])
        if lines[0] != "" or lines[0] != " " or lines[0] != None:
            start_time = int(lines[0])
            minu = int(lines[1])
            thoi_gian_moc = datetime(datetime.now().year, datetime.now().month, datetime.now().day, start_time, minu)
        # print(time)
        # print(thoi_gian_moc)
        open_file("sleep.py")
        while True:
            now = datetime.now()
            # print(now)
            if int(now.minute) == 45:
                # open_file("sleep.py")  # Mở tệp nếu chưa mở
                thongbao = Thongbao(thoi_gian_moc)
                thongbao.show_notification()
                time.sleep(60)
        # thongbao = Thongbao(thoi_gian_moc)
        # thongbao.show_notification()
except Exception as e:
    print(e)