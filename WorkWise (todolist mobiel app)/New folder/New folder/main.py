from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from database import Database
from plyer import notification
from datetime import datetime
import time
import threading
from bisect import bisect

# Khởi tạo phiên bản dbsqlite
db = Database()

class DialogContent(MDBoxLayout):
    """Nội dung của hộp thoại để tạo nhiệm vụ"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
        self.hour = 0  # Giờ bắt đầu (mặc định là 0)
        self.minute = 0  # Phút bắt đầu (mặc định là 0)

    def show_date_picker(self):
        """Hiển thị bộ chọn ngày"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def show_time_picker(self):
        """Hiển thị bộ chọn giờ và phút"""
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save)
        time_dialog.open()

    def on_date_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

    def on_time_save(self, instance, value):
        self.hour = value.hour
        self.minute = value.minute
        self.ids.time_text.text = f"{self.hour:02d}:{self.minute:02d}"

# Sau khi tạo database.py
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Mục danh sách tùy chỉnh với checkbox"""

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        """Đánh dấu nhiệm vụ là hoàn thành hoặc chưa hoàn thành"""
        if check.active == True:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))

    def delete_item(self, the_list_item):
        """Xóa nhiệm vụ"""
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class DialogEdit(MDBoxLayout):
    """Nội dung của hộp thoại để chỉnh sửa nhiệm vụ"""

    def __init__(self, list_item, **kwargs):
        super().__init__(**kwargs)
        self.list_item = list_item
        self.ids.edit_task_text.text = list_item.text.strip("[b][/b]")
        self.ids.edit_date_text.text = list_item.secondary_text.split(" ")[-2]
        self.ids.edit_time_text.text = list_item.secondary_text.split(" ")[-1][:-1]

    def show_date_picker(self):
        """Hiển thị bộ chọn ngày"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def show_time_picker(self):
        """Hiển thị bộ chọn giờ và phút"""
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save)
        time_dialog.open()

    def on_date_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.edit_date_text.text = str(date)

    def on_time_save(self, instance, value):
        self.ids.edit_time_text.text = value.strftime('%H:%M')

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Vùng chứa checkbox bên trái"""

# Lớp MainApp
class MainApp(MDApp):
    task_list_dialog = None
    task_edit_dialog = None
    list_items = []

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.create_menu()

    def create_menu(self):
        # Danh sách các chức năng menu
        menu_items = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "Chức năng 1",
                "on_release": lambda x=f"Chức năng 1": self.menu_callback(x),
            },
            {
                "viewclass": "OneLineIconListItem",
                "text": "Chức năng 2",
                "on_release": lambda x=f"Chức năng 2": self.menu_callback(x),
            },
            # Thêm các chức năng khác tùy theo ý tưởng của bạn
        ]

        # Tạo menu thả xuống
        self.menu = MDDropdownMenu(
            caller=self.root.ids.menu_btn,
            items=menu_items,
            width_mult=4,
        )

    def show_menu(self):
        # Hiển thị menu thả xuống khi người dùng nhấp vào nút Menu
        self.menu.open()

    def menu_callback(self, text):
        # Xử lý chức năng khi người dùng chọn một chức năng từ menu
        self.menu.dismiss()
        # Xử lý logic tùy theo text (tên chức năng) được chọn

    def show_task_dialog(self):
        if self.task_list_dialog is None:
            content = DialogContent()
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=content,
            )
        else:
            content = self.task_list_dialog.content_cls

        content.ids.task_text.text = ''
        content.ids.date_text.text = ''
        content.ids.time_text.text = ''

        self.task_list_dialog.open()

    def edit_task(self, task_text, date, time, task_id):
        task_date = date + " " + time
        task_datetime = datetime.strptime(task_date, '%A %d %B %Y %H:%M')

        self.task_edit_dialog.content_cls.ids.edit_task_text.text = ''
        self.task_edit_dialog.content_cls.ids.edit_date_text.text = ''
        self.task_edit_dialog.content_cls.ids.edit_time_text.text = ''

        # Tìm kiếm và cập nhật mục danh sách cũ
        list_item = next((item for item in self.root.ids.container.children if item.pk == task_id), None)
        if list_item:
            list_item.text = '[b]' + task_text + '[/b]'
            list_item.secondary_text = task_date
            db.update_task(task_id, task_text, task_date)

            # Kiểm tra xem thời gian bắt đầu nhiệm vụ đã qua hay chưa
            current_datetime = datetime.now()
            if time != "" and task_datetime > current_datetime:
                # Lập lịch thông báo
                task_thread = threading.Thread(target=self.schedule_task_reminder, args=(task_text, task_datetime))
                task_thread.start()

        self.task_edit_dialog.dismiss()

    def on_start(self):
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()
            if not completed_tasks and not incompleted_tasks:
                # Đặt các giá trị đầu tiên về rỗng
                self.task_list_dialog.content_cls.ids.task_text.text = ''
                self.task_list_dialog.content_cls.ids.date_text.text = ''
                self.task_list_dialog.content_cls.ids.time_text.text = ''
            if incompleted_tasks:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

                    # Kiểm tra xem thời gian bắt đầu nhiệm vụ đã qua hay chưa
                    task_datetime = datetime.strptime(task[2], '%A %d %B %Y %H:%M')
                    current_datetime = datetime.now()
                    if task_datetime > current_datetime:
                        # Lập lịch thông báo
                        self.schedule_task_reminder(task[1], task_datetime)

            if completed_tasks:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text='[s]' + task[1] + '[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def close_edit_dialog(self):
        if self.task_edit_dialog:
            self.task_edit_dialog.dismiss()

    def add_task(self, task_text, date, time):
        if time == "":
            # Hiển thị cảnh báo khi chưa nhập thời gian
            self.show_time_warning_dialog()
            return

        task_date = date + " " + time
        task_datetime = datetime.strptime(task_date, '%A %d %B %Y %H:%M')

        created_task = db.create_task(task_text, task_date)

        add_task = ListItemWithCheckbox(pk=created_task[0], text='[b]' + created_task[1] + '[/b]',
                                        secondary_text=created_task[2])
        self.root.ids.container.add_widget(add_task)

        # Kiểm tra xem thời gian bắt đầu nhiệm vụ đã qua hay chưa
        current_datetime = datetime.now()
        if task_datetime > current_datetime:
            # Lập lịch thông báo
            task_thread = threading.Thread(target=self.schedule_task_reminder, args=(task_text, task_datetime))
            task_thread.start()

        self.task_list_dialog.dismiss()

    def schedule_task_reminder(self, task_text, task_datetime):
        time_diff = (task_datetime - datetime.now()).total_seconds()

        # Đợi đến thời gian bắt đầu nhiệm vụ
        time.sleep(time_diff)

        # Gửi thông báo
        notification_title = "WorkWise Task Reminder"
        notification_message = f"Task: {task_text}"
        notification.notify(title=notification_title, message=notification_message)

    def on_checkbox_active(self, checkbox, value, list_item):
        list_item.mark(checkbox, list_item)

    def on_checkbox_deactivate(self, checkbox, value, list_item):
        list_item.mark(checkbox, list_item)

    def delete_item(self, list_item):
        list_item.delete_item(list_item)

    def show_edit_dialog(self, list_item):
        if not self.task_edit_dialog:
            self.task_edit_dialog = MDDialog(
                title="Edit Task",
                type="custom",
                content_cls=DialogEdit(list_item=list_item),
            )
        self.task_edit_dialog.open()

    def edit_task(self, task_text, date, time, task_id):
        task_date = date + " " + time
        task_datetime = datetime.strptime(task_date, '%A %d %B %Y %H:%M')

        # Tìm kiếm và cập nhật mục danh sách cũ
        list_item = next((item for item in self.root.ids.container.children if item.pk == task_id), None)
        if list_item:
            list_item.text = '[b]' + task_text + '[/b]'
            list_item.secondary_text = task_date
            db.update_task(task_id, task_text, task_date)

            # Kiểm tra xem thời gian bắt đầu nhiệm vụ đã qua hay chưa
            current_datetime = datetime.now()
            if task_datetime > current_datetime:
                # Lập lịch thông báo
                task_thread = threading.Thread(target=self.schedule_task_reminder, args=(task_text, task_datetime))
                task_thread.start()

        self.task_edit_dialog.dismiss()


if __name__ == '__main__':
    app = MainApp()
    app.run()