import tkinter as tk


class SearchBar:

    def __init__(self, root):
        self.master = root
        self.master.title("")
        self.master.overrideredirect(1)
        self.master.attributes('-transparentcolor', '#222121')
        self.flag = False
        self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight() // 2}+0+0")
        self.master.configure(bg="#222121")
        self.master.attributes('-alpha', 0.7)
        self.master.attributes('-toolwindow', True)
        self.master.attributes('-topmost', True)
        self.master.bind("<B1-Motion>", self.move_window)
        self.create_gui()

    def create_gui(self):
        self.text_label = tk.Label(self.master, text="", font=("Helvetica", 43, 'bold'), bg="#222121", fg="#FFFFFF")
        self.text_label.grid(row=0, column=0, sticky="w")
        self.type_text(
            "Lorem Ipsum chỉ đơn giản là một đoạn văn bản giả, được dùng vào việc trình bày và dàn trang phục vụ cho in ấn.")  # Call type_text to start typing the text

    def type_text(self, text, index=0):
        if index < len(text):
            current_text = self.text_label.cget("text")
            self.text_label.config(text=current_text + text[index])
            index += 1
            self.master.after(100, self.type_text, text, index)
        else:
            self.after_typing()

    def after_typing(self):
        # Lower or hide the window after the text is fully displayed
        self.master.after(1000, self.hide_window)  # Adjust the delay as needed (1000 ms = 1 second)

    def hide_window(self):
        self.master.withdraw()
        self.master.after(3000, self.show_window)  # Show the window again after 3 seconds

    def show_window(self):
        self.master.deiconify()

    def move_window(self, event):
        self.master.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    def clear_all_widgets(self, root):
        for widget in root.winfo_children():
            widget.destroy()

    def closing(self, para=None):
        self.clear_all_widgets(self.master)
        try:
            self.master.destroy()
        except:
            return


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    search_bar = tk.Toplevel(root)
    SB = SearchBar(search_bar)
    search_bar.mainloop()
