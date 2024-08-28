import sqlite3
import sys
from customtkinter import *
from tkinter import Listbox, END, messagebox

set_appearance_mode("Dark")
set_default_color_theme("blue")


class SearchBar:

    def __init__(self, root):
        self.master = root
        try:
            from ctypes import windll, byref, sizeof, c_int
            HWND = windll.user32.GetParent(self.master.winfo_id())
            title_bar_color = 0x00242424
            title_text_color = 0x00FFFFFF
            windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                35,
                byref(c_int(title_bar_color)),
                sizeof(c_int))
            windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                36,
                byref(c_int(title_text_color)),
                sizeof(c_int))
        except Exception as e:
            pass

        self.master.title("")
        self.master.overrideredirect(1)
        self.flag = False
        self.master.geometry(f"470x50+{self.master.winfo_screenwidth() // 2}+0")
        self.master.configure(bg="#222121")
        self.master.attributes('-alpha', 0.7)
        self.master.attributes('-toolwindow', True)
        self.master.attributes('-topmost', True)
        self.master.attributes('-transparentcolor', '#222121')
        self.master.bind("<B1-Motion>", self.move_window)

        self.text_input = CTkTextbox(self.master, width=340, height=1, font=("Helvetica", 25, 'bold'), corner_radius=7)
        self.text_input.grid(column=1, row=1, sticky="nsew")
        self.show_suggests = True
        self.text_input.bind("<KeyRelease>", self.show_suggestions)
        self.text_input.bind("<Return>", self.on_search)
        self.text_input.bind("<Shift-Return>", self.on_shift_enter)

        self.search_button = CTkButton(self.master, text="➤➤➤", font=('Times New Roman', 16, 'bold'),
                                       fg_color="transparent", hover_color="#333030", text_color="yellow", width=16,
                                       height=4, corner_radius=25, command=self.on_search)
        self.search_button.grid(column=2, row=1, padx=1, pady=3, sticky="nsew")

        self.size_button = CTkButton(self.master, text="-", font=('Times New Roman', 34, 'bold'),
                                     fg_color="transparent", hover_color="#333030", text_color="yellow", width=43,
                                     height=10, corner_radius=25, command=self.resizebar)
        self.size_button.grid(column=0, row=1, padx=3, pady=3, sticky="nsew")

        self.suggestion_listbox = Listbox(self.master, bg="#333333", fg="white", font=("Helvetica", 16), height=4)
        self.suggestion_listbox.grid(column=0, row=2, sticky="nsew", columnspan=3)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self.on_suggestion_select)
        self.suggestion_listbox.grid_remove()

        self.display_frame = CTkFrame(self.master, width=450, height=100, fg_color="transparent")
        self.display_frame.grid(column=0, row=2, columnspan=3, sticky="nsew")
        self.display_frame.grid_remove()
        self.show_frame = False
        self.command = {
            "guide": self.guiding,
            "clb": self.closing,
            "show": self.show,
            "add": self.add,
            "del": self.delete,
            "db": self.connect,
        }
        self.suggest = [
            "guide",
            "clb",
            "show",
            "add(name,path)",
            "del(name)",
            "db( name )",
        ]
    def guiding(self, para=None):
        try:
            self.display_frame.grid_remove()
            self.suggestion_listbox.delete(0, END)
            self.show_suggests = False
            self.show_frame = False
            self.flag = False
            self.suggestion_listbox.grid_remove()
            self.master.geometry(f"470x{20 * len(self.suggest) + 50}")
            self.suggestion_listbox.configure(height=len(self.suggest))
            for cmd in self.suggest:
                self.suggestion_listbox.insert(END, cmd)
        except Exception as err:
            messagebox.showerror("Error Guide", f"{err} !!!")
            return
    def show(self, para=None):
        try:
            conn = sqlite3.connect('Database/databar.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT ID, name, place FROM databar''')
            records = cursor.fetchall()
            conn.close()

            if records == []:
                return
            print(records)
            self.show_frame = True
            self.show_suggests = False
            self.clear_all_widgets(self.display_frame)
            self.master.geometry(f"470x{30 * len(records) + 50}")
            self.display_frame.grid()
            for index, record in enumerate(records):
                ID, name, place = record
                label_id = CTkLabel(self.display_frame, text=f"ID: {ID}", text_color="white")
                label_id.grid(row=index, column=0, pady=1)
                label_name = CTkLabel(self.display_frame, text="   |Name:", text_color="white")
                label_name.grid(row=index, column=1, pady=1)
                entry_name = CTkEntry(self.display_frame, width=70)
                entry_name.insert(0, name)
                entry_name.grid(row=index, column=2, pady=1)
                label_place = CTkLabel(self.display_frame, text="   |Path:", text_color="white")
                label_place.grid(row=index, column=3, pady=1)
                entry_place = CTkEntry(self.display_frame, width=280)
                entry_place.insert(0, place)
                entry_place.grid(row=index, column=4, pady=1)
        except Exception as err:
            messagebox.showerror("Error show", f"{err} !!!")
            return
    def connect(self, para=None):
        try:
            if not para:
                return
            def save():
                values = []
                for e in entry_values:
                    values.append(e.get().strip())
                print(values)
                conn = sqlite3.connect(f'''{path}''')
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO {name} {tuple(cols)} VALUES {tuple(values)}")
                print("đẫ thêm", values, " vào ", name)
                conn.commit()
                conn.close()
                self.show_frame = False
                self.show_suggests = True
                self.clear_all_widgets(self.display_frame)
                self.master.geometry(f"470x50")
                self.display_frame.grid_remove()
                return
            def get_path(name):
                conn = sqlite3.connect('Database/databar.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT place FROM databar WHERE name = ?''', (name,))
                records = cursor.fetchall()
                conn.close()
                if not records:
                    return None
                return records[0][0]
            def get_column(name, path):
                print(path)
                conn = sqlite3.connect(f'''{path}''')
                cursor = conn.cursor()
                cursor.execute(f'PRAGMA table_info("{name}")')
                columns_info = cursor.fetchall()
                non_primary_key_columns = [info[1] for info in columns_info if info[5] == 0]
                print("Tên các cột không có PRIMARY KEY trong bảng 'learnlist':", non_primary_key_columns)
                if not non_primary_key_columns:
                    return None
                return non_primary_key_columns
            def get_table_name(path):
                print(path)
                # db(TEMP)
                conn = sqlite3.connect(f'''{path}''')
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                if not tables:
                    return
                return [table[0] for table in tables][0]
            path = get_path(para)
            if not path:
                return
            name = get_table_name(path)
            print(name, " ", path)
            if not name:
                return
            cols = get_column(name, path)
            if not cols:
                return
            self.show_frame = True
            self.show_suggests = False
            self.clear_all_widgets(self.display_frame)
            self.master.geometry(f"470x{40 * len(cols) + 50}")
            self.display_frame.grid()
            entry_values = []
            for index, col_name in enumerate(cols):
                id = CTkLabel(self.display_frame, text=f"{index + 1}/", text_color="white")
                id.grid(row=index, column=0, padx=5, pady=5)
                label_id = CTkLabel(self.display_frame, text=f"{col_name}:", text_color="white")
                label_id.grid(row=index, column=1, padx=5, pady=5)
                entry_col = CTkEntry(self.display_frame, width=100)
                entry_col.grid(row=index, column=3, padx=5, pady=5)
                entry_values.append(entry_col)
            save_button = CTkButton(self.display_frame, text="Add+", font=('Times New Roman', 16, 'bold'), width=25,
                                    command=save)
            save_button.grid(row=0, column=4, padx=5, pady=5)
            return
        except Exception as err:
            messagebox.showerror("Error connect", f"{err} !!!")
            return
    def add(self, para=None):
        try:
            if not para or ',' not in para:
                return
            para = para.split(',')
            name = para[0].strip()
            path = para[1].strip()
            if path.startswith('"') and path.endswith('"'):
                path = path.replace('"', "").replace('"', "")
            if name and path:
                ###
                conn = sqlite3.connect('Database/databar.db')
                cursor = conn.cursor()
                cursor.execute('''
                                            INSERT INTO databar (name, place)
                                            VALUES (?, ?)
                                            ''', (name, path))
                conn.commit()
                print("Đã thêm vào database:", name, " | ", path)
                conn.close()
                ###
                self.show()
            return
        except Exception as err:
            messagebox.showerror("Error add", f"{err} !!!")
            return
    def delete(self, para=None):
        try:
            if not para:
                return
            print(para)
            conn = sqlite3.connect('Database/databar.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM databar WHERE name = ? OR ID = ?', (para, para,))
            conn.commit()
            print("đã xóa ", para)
            conn.close()
            self.display_frame.grid_remove()
            self.suggestion_listbox.delete(0, END)
            self.show_suggests = False
            self.show_frame = False
            self.flag = False
            self.suggestion_listbox.grid_remove()
            self.master.geometry(f"470x50")
            self.show()
            return
        except Exception as err:
            messagebox.showerror("Error delete", f"{err} !!!")
            return
    def move_window(self, event):
        self.master.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
        self.display_frame.grid_remove()
        self.suggestion_listbox.grid_remove()
        self.text_input.grid_remove()
        self.search_button.grid_remove()
        self.size_button.configure(text='+', width=55, height=50)
        self.master.geometry(f"60x50")
        self.flag = False
    def resizebar(self, para=None):
        if self.flag:
            self.text_input.grid()
            self.search_button.grid()
            self.size_button.configure(text='-', width=43, height=10)
            self.master.geometry(f"470x50")
            self.flag = False
        else:
            self.display_frame.grid_remove()
            self.suggestion_listbox.grid_remove()
            self.text_input.grid_remove()
            self.search_button.grid_remove()
            self.size_button.configure(text='+', width=55, height=50)
            self.master.geometry(f"60x50")
            self.flag = True
            self.show_suggests = True
            self.show_frame = False
    def on_shift_enter(self, event=None):
        current_cursor_position = self.text_input.index(END)
        self.text_input.insert(current_cursor_position, "")
    def on_search(self, event=None):
        try:
            command = self.text_input.get("1.0", END).strip()
            self.text_input.delete("1.0", END)
            if command:
                param = ""
                if '(' in command and command.endswith(')'):
                    command, param = command[:-1].split('(', 1)
                if command in self.command:
                    print("command:", command)
                    print("para:", param)
                    self.command[command](param.strip())
                else:
                    self.show_frame = False
                    self.show_suggests = True
                    print(f"Unknown command: {command}")
            return
        except Exception as err:
            messagebox.showerror("Error on_search", f"{err} !!!")
            return
    def show_suggestions(self, event):
        if not self.show_suggests:
            return
        else:
            self.display_frame.grid_remove()
        self.flag = False
        input_text = self.text_input.get("1.0", END).strip().lower()
        self.suggestion_listbox.delete(0, END)
        if input_text:
            matching_suggestions = [command for command in self.suggest if input_text in command]
            if matching_suggestions:
                self.master.geometry(f"470x{20 * len(matching_suggestions) + 50}")
                self.suggestion_listbox.configure(height=len(matching_suggestions))
                self.suggestion_listbox.grid()
                for suggestion in matching_suggestions:
                    self.suggestion_listbox.insert(END, suggestion)
            else:
                self.suggestion_listbox.grid_remove()
                self.master.geometry(f"470x50")
        else:
            self.suggestion_listbox.grid_remove()
            self.master.geometry(f"470x50")
    def on_suggestion_select(self, event):
        index = self.suggestion_listbox.curselection()
        if index:
            selected_suggestion = self.suggestion_listbox.get(index)
            self.text_input.delete("1.0", END)
            self.text_input.insert(END, selected_suggestion)
            self.suggestion_listbox.delete(0, END)
            self.suggestion_listbox.grid_remove()
            self.master.geometry(f"470x50")
    def clear_all_widgets(self, root):
        for widget in root.winfo_children():
            widget.destroy()
    def closing(self, para=None):
        try:
            self.master.destroy()
            sys.exit()
        except:
            return


if __name__ == "__main__":
    root = CTk()
    root.withdraw()
    search_bar = CTkToplevel(root)
    SB = SearchBar(search_bar)
    search_bar.mainloop()
