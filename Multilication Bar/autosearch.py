import sys
import google.generativeai as palm
from translate import Translator
import webbrowser
import pyttsx3
from datetime import datetime
import time
from customtkinter import *
import queue
import ctypes
import win32gui
import win32console
from colorama import Fore, Style, Back
import openai
import threading
from tkinter import filedialog, Toplevel, Tk, messagebox, Listbox

set_appearance_mode("Dark")
set_default_color_theme("blue")


class SearchBar:

    def __init__(self, root):
        self.master = root
        try:
            from ctypes import windll, byref, sizeof, c_int
            HWND = windll.user32.GetParent(self.master.winfo_id())
            #self.master.iconbitmap("Database/bar_icon.ico")
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
            #messagebox.showerror("Error", f"Failed to set window attributes: {e}")

        self.master.title("")
        self.master.overrideredirect(1)
        self.flag = True
        self.master.geometry(f"470x50+{self.master.winfo_screenwidth() // 2}+0")
        self.master.configure(bg="#222121")
        self.master.attributes('-alpha', 0.7)
        self.master.attributes('-toolwindow', True)
        self.master.attributes('-topmost', True)
        self.master.attributes('-transparentcolor', '#222121')
        self.master.bind("<B1-Motion>", self.move_window)

        self.text_input = CTkTextbox(self.master, width=340, height=1, font=("Helvetica", 25, 'bold'), corner_radius=7)
        self.text_input.grid(column=1, row=1, sticky="nsew")
        self.text_input.bind("<KeyRelease>", self.show_suggestions)
        #self.text_input.bind("<FocusIn>", self.show_suggestions)
        #self.text_input.bind("<FocusOut>", self.hide_suggestions)
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

        self.suggestion_listbox = Listbox(self.master, bg="#333333", fg="white", font=("Helvetica", 15), height=4)
        self.suggestion_listbox.grid(column=1, row=2, sticky="nsew", columnspan=2)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self.on_suggestion_select)
        self.suggestion_listbox.grid_remove()  # Ẩn Listbox ban đầu

        self.suggestions = ["Hello, how are you?", "Good morning!", "good pro", "What is the weather today?", "Open Google","open cc","open 1111",
                            "Play music", "Set an alarm for 7 AM"]

        for i in range(5):
            self.master.grid_rowconfigure(i, weight=2)
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=2)
    def move_window(self, event):
        self.master.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
        #self.flag = not self.flag
        self.suggestion_listbox.grid_remove()
        self.text_input.grid_remove()
        self.search_button.grid_remove()
        self.size_button.configure(text='+', width=110, height=50)
        self.master.geometry(f"60x50")
        self.flag = False

    def resizebar(self):

        if self.flag:
            self.text_input.grid()
            self.search_button.grid()
            self.size_button.configure(text='-', width=43, height=10)
            self.master.geometry(f"470x50")
            self.flag = False
        else:
            self.suggestion_listbox.grid_remove()
            self.text_input.grid_remove()
            self.search_button.grid_remove()
            self.size_button.configure(text='+', width=110, height=50)
            self.master.geometry(f"60x50")
            self.flag = True
    def on_shift_enter(self, event=None):
        current_cursor_position = self.text_input.index(END)
        self.text_input.insert(current_cursor_position, "")
    def on_search(self, event=None):
        query = self.text_input.get("1.0", END).strip()
        self.text_input.delete("1.0", END)
        if query == '\\':
            self.resizebar()
        elif query == 'clb':
            self.closing()
        return
    def show_suggestions(self, event):
        input_text = self.text_input.get("1.0", END).strip().lower()
        self.suggestion_listbox.delete(0, END)
        if input_text:
            matching_suggestions = [s for s in self.suggestions if input_text in s.lower()]
            print(matching_suggestions)
            if matching_suggestions:
                self.master.geometry(
                    f"470x{20 * len(matching_suggestions) + 50}")
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
    def hide_suggestions(self, event):
        self.suggestion_listbox.grid_remove()
    def on_suggestion_select(self, event):
        index = self.suggestion_listbox.curselection()
        print(index)
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
    def closing(self):
        sys.exit()


if __name__ == "__main__":
    root = CTk()
    root.withdraw()
    search_bar = CTkToplevel(root)
    SB = SearchBar(search_bar)
    search_bar.mainloop()
