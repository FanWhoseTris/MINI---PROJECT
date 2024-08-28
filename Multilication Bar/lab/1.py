import tkinter as tk

class PopUpTimer:
    def __init__(self, root, minutes, seconds):
        self.root = root
        self.minutes = minutes
        self.seconds = seconds

        self.root.title("")
        self.root.overrideredirect(1)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#222121")
        self.root.geometry(f"+0+0")

        # Cho phép di chuyển cửa sổ
        self.root.bind("<B1-Motion>", self.move_window)

        # Nhãn hiển thị thời gian đếm ngược
        self.label = tk.Label(self.root, text=f"{self.minutes:02d}:{self.seconds:02d}", font=("Helvetica", 20), bg="#222121", fg="#ffffff")
        self.label.pack()
        self.close_button = tk.Button(self.root, text="X", command=self.root.destroy, bg="#444444", fg="#ffffff", bd=0)
        self.close_button.pack(side=tk.TOP)
        # Nút để đóng cửa sổ


        # Đặt cửa sổ trong suốt và trên cùng
        self.root.attributes('-transparentcolor', '#222121')
        self.root.attributes('-alpha', 0.7)

        # Bắt đầu đếm ngược
        self.update_timer()

    def update_timer(self):
        if self.minutes > 0 or self.seconds > 0:
            if self.seconds == 0:
                self.minutes -= 1
                self.seconds = 59
            else:
                self.seconds -= 1

            self.label.config(text=f"{self.minutes:02d}:{self.seconds:02d}")

            # Cập nhật mỗi giây
            self.root.after(1000, self.update_timer)
        else:
            self.timer_finished()

    def timer_finished(self):
        self.label.config(text="Time's up!")
        self.root.attributes('-alpha', 1.0)  # Làm cửa sổ hoàn toàn hiện diện khi hết thời gian

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root}+{event.y_root}')

if __name__ == "__main__":
    root = tk.Tk()
    app = PopUpTimer(root, 1, 0)  # Đếm ngược từ 1 phút 0 giây
    root.mainloop()
