from tkinter import *
from tkinter import messagebox

TEXT_COLOR = "#149414"

FONT = "Helvetica 14"

class Note():
    def __init__(self):
        self.window = Tk()
        self.window.title("Ghi Nhớ")
        self.window.geometry("511x359")
        self.file_entry = Entry(self.window, bg="#353740", fg=TEXT_COLOR, font=FONT)
        self.file_entry.pack(pady=5, padx=10)

        self.note_text = Text(self.window, wrap="word", height=10, width=40)
        self.note_text.pack(pady=5, padx=10)

        save_button = Button(self.window, text="Lưu", command=self.save_note)
        save_button.pack(side=LEFT, padx=5, pady=5)

        load_button = Button(self.window, text="Tải", command=self.load_note)
        load_button.pack(side=RIGHT, padx=5, pady=5)

    def save_note(self):
        filename = self.file_entry.get()
        if not filename:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên file.")
            return
        note_text = self.note_text.get("1.0", "end-1c")
        with open(f"data/{filename}.txt", "w", encoding="utf-8") as file:
            file.write(note_text)
        messagebox.showinfo("Lưu thành công", "Ghi nhớ đã được lưu thành công!")

    def load_note(self):
        filename = self.file_entry.get()
        if not filename:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên file cần tải.")
            return
        try:
            with open(f"data/{filename}.txt", "r", encoding="utf-8") as file:
                note_text = file.read()
                self.note_text.delete("1.0", "end")
                self.note_text.insert("1.0", note_text)
        except FileNotFoundError:
            messagebox.showwarning("Không tìm thấy ghi nhớ", f"Không tìm thấy file {filename}.txt!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Note()
    app.run()
