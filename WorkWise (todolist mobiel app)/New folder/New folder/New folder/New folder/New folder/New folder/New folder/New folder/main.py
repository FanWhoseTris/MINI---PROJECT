from kivy.properties import NumericProperty, ListProperty, StringProperty, Clock
from kivy.uix.anchorlayout import AnchorLayout
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
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog

class EfficiencyScreen(Screen):
    pass
# Khởi tạo phiên bản dbsqlite
db = Database()

class NoteDialog(MDDialog):
    def __init__(self, list_item=None, **kwargs):
        super().__init__(**kwargs)
        self.list_item = list_item
        self.task_id = list_item.pk if list_item else None
        self.ids.note_text.text = ""  # Reset the note text when opening the dialog


class DialogContent(MDBoxLayout):
    """Nội dung của hộp thoại để tạo nhiệm vụ"""

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
            self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
            self.hour = 0  # Giờ bắt đầu (mặc định là 0)
            self.minute = 0  # Phút bắt đầu (mặc định là 0)
        except Exception as e:
            print(e)


    def show_date_picker(self):
        try:
            """Hiển thị bộ chọn ngày"""
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_date_save)
            date_dialog.open()
        except Exception as e:
            print(e)


    def show_time_picker(self):
        try:
            """Hiển thị bộ chọn giờ và phút"""
            time_dialog = MDTimePicker()
            time_dialog.bind(on_save=self.on_time_save)
            time_dialog.open()
        except Exception as e:
            print(e)


    def on_date_save(self, instance, value, date_range):
        try:
            date = value.strftime('%A %d %B %Y')
            self.ids.date_text.text = str(date)
        except Exception as e:
            print(e)


    def on_time_save(self, instance, value):
        try:
            self.hour = value.hour
            self.minute = value.minute
            self.ids.time_text.text = f"{self.hour:02d}:{self.minute:02d}"
        except Exception as e:
            print(e)


# Sau khi tạo database.py
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Mục danh sách tùy chỉnh với checkbox"""

    def __init__(self, pk=None, **kwargs):
        try:
            super().__init__(**kwargs)
            self.pk = pk
        except Exception as e:
            print(e)


    def mark(self, check, the_list_item):
        try:
            """Đánh dấu nhiệm vụ là hoàn thành hoặc chưa hoàn thành"""
            if check.active == True:
                the_list_item.text = '[s]' + the_list_item.text + '[/s]'
                db.mark_task_as_complete(the_list_item.pk)
            else:
                the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))
        except Exception as e:
            print(e)


    def delete_item(self, the_list_item):
        try:
            """Xóa nhiệm vụ"""
            self.parent.remove_widget(the_list_item)
            db.delete_task(the_list_item.pk)
        except Exception as e:
            print(e)


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
class CircularProgressBar(AnchorLayout):
    set_value = NumericProperty(0)
    value = NumericProperty(0)
    bar_color = ListProperty([1, 0, 100 / 255])
    bar_width = NumericProperty(10)
    text = StringProperty("0%")
    duration = NumericProperty(0.5)
    counter = 0

    def __init__(self, **kwargs):
        try:
            super(CircularProgressBar, self).__init__(**kwargs)
            self.counter = 0
            Clock.schedule_once(self.animate, 0)
        except Exception as e:
            print(e)


    def animate(self, *args):
        try:
            Clock.schedule_interval(self.percent_counter, self.duration / self.value)
        except Exception as e:
            print(e)


    def percent_counter(self, *args):
        try:
            if self.counter < self.value:
                self.counter += 1
                self.text = f"{self.counter}%"
                self.set_value = self.counter
            else:
                Clock.unschedule(self.percent_counter)
        except Exception as e:
            print(e)


# Lớp MainApp
class MainApp(MDApp):
    task_list_dialog = None
    task_edit_dialog = None
    list_items = []
    show_add_task_button = True

    def build(self):

            self.theme_cls.primary_palette = "Orange"
            self.create_menu()
            self.note_dialog = None


    def create_menu(self):
        try:
            menu_items = [
                {
                    "viewclass": "OneLineIconListItem",
                    "text": "Trở Về",
                    "on_release": lambda x=f"Return": self.menu_callback(x),
                },
                {
                    "viewclass": "OneLineIconListItem",
                    "text": "Hiệu Suất Làm Việc",
                    "on_release": lambda x=f"EfficiencyScreen": self.menu_callback(x),
                },
            ]
            self.menu = MDDropdownMenu(
                caller=self.root.ids.menu_btn,
                items=menu_items,
                width_mult=4,
            )
        except Exception as e:
            print(e)


    def show_menu(self):
        try:
            # Hiển thị menu thả xuống khi người dùng nhấp vào nút Menu
            self.menu.open()
        except Exception as e:
            print(e)


    def menu_callback(self, screen_name):
        try:
            self.menu.dismiss()
            if screen_name == "EfficiencyScreen":
                self.root.ids.screen_manager.current = "efficiency_screen"
            if screen_name == "Return":
                self.root.ids.screen_manager.current = "main_screen"
        except Exception as e:
            print(e)

    def show_task_dialog(self):
        try:
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
        except Exception as e:
            print(e)


    def edit_task(self, task_text, date, time, task_id):
        try:
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
        except Exception as e:
            print(e)

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
        try:
            self.task_list_dialog.dismiss()
        except Exception as e:
            print(e)


    def close_edit_dialog(self):
        try:
            if self.task_edit_dialog:
                self.task_edit_dialog.dismiss()
        except Exception as e:
            print(e)


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
        try:
            time_diff = (task_datetime - datetime.now()).total_seconds()

            # Đợi đến thời gian bắt đầu nhiệm vụ
            time.sleep(time_diff)

            # Gửi thông báo
            notification_title = "WorkWise Task Reminder"
            notification_message = f"Task: {task_text}"
            notification.notify(title=notification_title, message=notification_message)
        except Exception as e:
            print(e)

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

    def show_note_dialog(self, list_item=None):
        if not self.note_dialog:
            self.note_dialog = NoteDialog()
        self.note_dialog.list_item = list_item
        if list_item:
            note = db.get_note_by_task_id(list_item.pk)
            self.note_dialog.ids.note_text.text = note if note else ""
        self.note_dialog.open()

    def save_note_and_close_dialog(self):
        note_text = self.note_dialog.ids.note_text.text
        if self.note_dialog.task_id:
            db.create_note_for_task_id(self.note_dialog.task_id, note_text)
        self.note_dialog.dismiss()

if __name__ == '__main__':
    app = MainApp()
    app.run()