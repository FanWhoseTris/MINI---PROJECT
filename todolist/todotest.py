import tkinter as tk
import sqlite3
import time
from datetime import datetime, timedelta

class TodoListApp:
    def __init__(self, root):
        self.root = root

        # Thiết lập các thuộc tính của cửa sổ
        self.root.title("Todo List")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#222121")

        # Sự kiện FocusIn và FocusOut
        self.root.bind('<FocusIn>', self.on_focus_in)
        self.root.bind('<FocusOut>', self.on_focus_out)

        # Kết nối với cơ sở dữ liệu SQLite
        self.conn = sqlite3.connect('todolist.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Ô nhập liệu để thêm task
        self.entry = tk.Entry(self.root, width=16, font=("Helvetica", 16, 'bold'), bg="#444444", fg="#ffffff", insertbackground="#ffffff")
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        # Gán sự kiện nhấn Enter cho ô nhập liệu
        self.entry.bind('<Return>', self.add_task_event)

        # Frame để chứa các nút ở trên Listbox
        self.buttons_frame = tk.Frame(self.root, bg="#222121")
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        # Nút Add Task và Delete Task nằm trong buttons_frame
        self.add_button = tk.Button(self.buttons_frame, text="Add", command=self.add_task, width=9, bg="#333333", fg="#ffffff")
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_task, width=9, bg="#333333", fg="#ffffff")
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Frame chứa cả Listbox và Scrollbar
        self.listbox_frame = tk.Frame(self.root, bg="#222121")
        self.listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tạo thanh cuộn
        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox với chế độ chọn nhiều task
        self.task_list = tk.Listbox(self.listbox_frame, selectmode=tk.EXTENDED, font=("Helvetica", 16, 'bold'), bg="#444444", fg="#ffffff", selectbackground="#555555", selectforeground="#ffffff", yscrollcommand=self.scrollbar.set)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Kết nối scrollbar với Listbox
        self.scrollbar.config(command=self.task_list.yview)

        # Binding để xử lý drag and drop
        self.task_list.bind('<B1-Motion>', self.drag_task)
        self.task_list.bind('<ButtonRelease-1>', self.drop_task)

        self.dragged_item_index = None

        # Load tasks from database
        self.load_tasks()

        # Frame chứa Label "Min:", Entry, nút OK, và label đếm ngược thời gian
        self.timer_frame = tk.Frame(self.root, bg="#222121")
        self.timer_frame.pack(fill=tk.X, padx=10, pady=10)

        self.min_label = tk.Label(self.timer_frame, text="Min:", font=("Helvetica", 12), bg="#222121", fg="#ffffff")
        self.min_label.pack(side=tk.LEFT, padx=5)

        self.minutes_entry = tk.Entry(self.timer_frame, width=5, font=("Helvetica", 12), bg="#444444", fg="#ffffff")
        self.minutes_entry.pack(side=tk.LEFT, padx=5)

        self.ok_button = tk.Button(self.timer_frame, text="Ok", command=self.start_timer, width=5, bg="#333333", fg="#ffffff")
        self.ok_button.pack(side=tk.LEFT, padx=5)

        # Label đếm ngược thời gian đặt ngang hàng
        self.countdown_label = tk.Label(self.timer_frame, font=("Helvetica", 16, 'bold'), bg="#222121", fg="#ffffff")
        self.countdown_label.pack(side=tk.LEFT, padx=10)

        # Biến để lưu trữ ID của hàm after
        self.after_id = None

        # Label hiển thị thời gian kết thúc đếm ngược
        self.end_time_label = tk.Label(self.root, font=("Helvetica", 14), bg="#222121", fg="#ffffff")
        self.end_time_label.pack(padx=10, pady=10)

    def create_table(self):
        # Tạo bảng task nếu nó chưa tồn tại
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_task(self):
        task = self.entry.get()
        if task:
            self.cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            self.conn.commit()
            self.task_list.insert(tk.END, task)
            self.entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_list.curselection()
        for index in reversed(selected):
            task = self.task_list.get(index)
            self.cursor.execute('DELETE FROM tasks WHERE task = ?', (task,))
            self.conn.commit()
            self.task_list.delete(index)

    def add_task_event(self, event):
        self.add_task()

    def drag_task(self, event):
        # Lấy index của task hiện tại
        selected = self.task_list.curselection()
        if selected:
            self.dragged_item_index = selected[0]
            # Tính toán lại vị trí tương đối của con trỏ chuột với listbox
            y = event.y
            index = self.task_list.nearest(y)
            if index != self.dragged_item_index:
                # Di chuyển item
                task = self.task_list.get(self.dragged_item_index)
                self.task_list.delete(self.dragged_item_index)
                self.task_list.insert(index, task)
                self.task_list.selection_set(index)
                self.dragged_item_index = index

    def drop_task(self, event):
        # Reset dragged item index
        self.dragged_item_index = None

    def load_tasks(self):
        # Load tasks từ cơ sở dữ liệu và hiển thị trong Listbox
        self.cursor.execute('SELECT task FROM tasks')
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.task_list.insert(tk.END, task[0])

    def start_timer(self):
        minutes = self.minutes_entry.get()
        if minutes.isdigit():
            total_seconds = int(minutes) * 60

            # Hủy bỏ đếm ngược hiện tại nếu có
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)

            # Tính toán và hiển thị thời gian kết thúc
            end_time = datetime.now() + timedelta(seconds=total_seconds)
            end_time_str = end_time.strftime('%I:%M %p')
            self.end_time_label.config(text=f"End Time: {end_time_str}")
            popup = tk.Toplevel(self.root)
            PopUpTimer(popup, int(minutes), 0)
            self.countdown(total_seconds)


    def countdown(self, remaining_seconds):
        if remaining_seconds >= 0:
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            self.countdown_label.config(text=f"{minutes:02d}:{seconds:02d}")

            # Lưu lại ID của hàm after
            self.after_id = self.root.after(1000, self.countdown, remaining_seconds - 1)

    def on_focus_in(self, event):
        # Khi focus vào ứng dụng, đặt màu nền bình thường và tắt trong suốt
        self.root.configure(bg="#222121")
        self.root.attributes('-alpha', 1.0)
        self.root.attributes('-transparentcolor', '')

    def on_focus_out(self, event):
        # Khi mất focus, đặt trong suốt
        self.root.configure(bg="#222121")
        self.root.attributes('-transparentcolor', '#222121')
        self.root.attributes('-alpha', 0.3)

    def __del__(self):
        # Đóng kết nối cơ sở dữ liệu khi ứng dụng kết thúc
        self.conn.close()

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
    app = TodoListApp(root)
    root.mainloop()
