from tkinter import messagebox
import tkinter as tk
import sqlite3


class Changelist(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("EDIT SENTENCES")
        try:
            from ctypes import windll, byref, sizeof, c_int
            HWND = windll.user32.GetParent(self.winfo_id())
            self.iconbitmap("images/icon1.ico")
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
        except:
            pass
        self.configure(bg="#222121")
        self.attributes('-topmost', True)
        #self.listbox = tk.Listbox(self, bg="#222121", fg="#222121", width=19, height=3, font=("Helvetica", 43))
        #self.listbox.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):  # Changed to 6 to accommodate the scrollbar
            self.grid_columnconfigure(i, weight=1)

        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")
        self.listbox_frame.grid_rowconfigure(0, weight=1)
        self.listbox_frame.grid_columnconfigure(0, weight=1)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical")
        self.listbox = tk.Listbox(self.listbox_frame, width=19, height=3, bg="#222121", fg="#FFFFFF", font=("Helvetica", 43),
                                  yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        study_button =  tk.Button(self, text="Add", width=15, command=self.add, font=("Helvetica", 25))
        new_button =  tk.Button(self, text="Delete", width=15, command=self.delete, font=("Helvetica", 25))
        delete_button =  tk.Button(self, text="Edit", width=15, command=self.edit, font=("Helvetica", 25))
        del_button =  tk.Button(self, text="Reset", width=15, command=self.reset, font=("Helvetica", 25))
        check_button =  tk.Button(self, text="Refresh", width=15, command=self.load, font=("Helvetica", 25))
        study_button.grid(row=1, column=0, padx=10, pady=10)
        new_button.grid(row=1, column=1, padx=10, pady=10)
        delete_button.grid(row=1, column=2, padx=10, pady=10)
        del_button.grid(row=1, column=3, padx=10, pady=10)
        check_button.grid(row=1, column=4, padx=10, pady=10)
        self.vocab_list = []
        self.load()
    def load(self):
        try:
            for i in range(self.listbox.size()):
                self.listbox.delete(0)
            conn = sqlite3.connect('Database/sentences.db')
            c = conn.cursor()
            c.execute('''
                                        SELECT id, sentence, times 
                                        FROM sentences
                                    ''')
            rows = c.fetchall()
            print(rows)
            for index, line in enumerate(rows, start=0):
                self.listbox.insert(tk.END, f"#{line[0]}|{line[2]}|{line[1]} ")
                self.listbox.itemconfig(index, {'bg': '#222121'})
            self.vocab_list = rows
        except:
            messagebox.showerror("Error", f" Load Error !!!")
            print("ERROR: Load  Error !!!")
    def add(self):
        try:
            quick_add_list_window = tk.Toplevel(self)
            quick_add_list_window.title("Add")
            quick_add_list_window.geometry("300x160+800+600")
            quick_add_list_window.configure(bg="#222121")  # , fg="#ffffff", bg="#222121"
            quick_add_list_window.attributes('-topmost', True)
            list_name_label = tk.Label(quick_add_list_window, text="Sentence:", fg="#ffffff", bg="#222121")
            list_name_label.pack(padx=10, pady=2)

            list_name_entry = tk.Entry(quick_add_list_window)
            list_name_entry.pack(padx=10, pady=2)

            def add_text():
                list_name = list_name_entry.get().strip()
                if not list_name:
                    return
                conn = sqlite3.connect(f'Database/sentences.db')
                c = conn.cursor()
                c.execute("INSERT INTO sentences (sentence, times) VALUES (?, ?)", (list_name, '0'))

                conn.commit()
                conn.close()
                self.load()
                quick_add_list_window.destroy()

            ok_button = tk.Button(quick_add_list_window, text="OK", command=add_text, font=("Helvetica", 14))
            ok_button.pack(padx=10, pady=5)
        except:
            messagebox.showerror("Error", f" ADD Action ERROR!!!")
            print("ERROR: ADD Action ERROR!!!")
    def delete(self):
        try:
            selected_item = self.listbox.curselection()
            if selected_item:
                selected_item_text = self.listbox.get(selected_item).strip()
                if messagebox.askyesno("Delete", f"Do you sure to delete {selected_item_text}?"):
                    selected_item_index = selected_item[0]
                    print(selected_item_index)
                    print(selected_item_text)
                    conn = sqlite3.connect(f'Database/sentences.db')
                    c = conn.cursor()
                    c.execute(f'''DELETE FROM sentences WHERE id = ? AND sentence=? AND times = ?'''
                              , (self.vocab_list[selected_item_index][0], self.vocab_list[selected_item_index][1],
                                 self.vocab_list[selected_item_index][2],))
                    conn.commit()
                    conn.close()
                    self.load()
        except:
            messagebox.showerror("Error", f" delete Action ERROR!!!")
            print("ERROR: delete ERROR!!!")
    def edit(self):
        try:
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                quick_edit_window = tk.Toplevel(self)
                quick_edit_window.title("EDIT")
                quick_edit_window.geometry("300x150+550+700")
                quick_edit_window.configure(bg="#222121")
                quick_edit_window.attributes('-topmost', True)
                old_word_label = tk.Label(quick_edit_window, text="Old Sentence:", fg="#ffffff", bg="#222121")
                old_word_label.pack(padx=10, pady=5)
                old_word_entry = tk.Entry(quick_edit_window)
                old_word_entry.pack(padx=10, pady=5)
                sen = self.vocab_list[selected_index]
                old_word_entry.insert(0, sen[1])

                def comfirm_word_mean():
                    new_word = old_word_entry.get()
                    # self.listbox.delete(selected_index)
                    # self.listbox.insert(selected_index, f"{id}. {new_word} : {new_mean}")
                    conn = sqlite3.connect(f'Database/sentences.db')
                    c = conn.cursor()
                    c.execute(f'''
                                                    UPDATE sentences
                                                    SET sentence=?
                                                    WHERE id = ? AND sentence=? AND times = ?
                                                ''', (new_word, sen[0], sen[1],
                                                      sen[2],))
                    conn.commit()
                    conn.close()
                    self.load()
                    quick_edit_window.destroy()
                    return

                ok_button = tk.Button(quick_edit_window, text="OK", command=comfirm_word_mean, font=("Helvetica", 14))
                ok_button.pack(padx=10, pady=5)
        except:
            messagebox.showerror("Error", f" edit ERROR!!!")
            print("ERROR: edit ERROR!!!")
    def reset(self):
        try:
            conn = sqlite3.connect('Database/sentences.db')
            c = conn.cursor()

            # SQL query to update the 'times' column for all records
            c.execute('''
                            UPDATE sentences
                            SET times = 0
                        ''')

            conn.commit()
            conn.close()
            self.load()
        except:
            messagebox.showerror("Error", f" reset ERROR!!!")
            print("ERROR:reset ERROR!!!")

if __name__ == "__main__":
    cl = Changelist()
    cl.mainloop()
