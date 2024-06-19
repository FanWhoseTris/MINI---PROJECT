from tkinter import *
from tkinter import messagebox
import math

current_player = 'X'

window = Tk()
window.title("Bảng caro 3x3")
window.geometry("300x300")

button1 = Button(window, text="", width=10, height=5)
button2 = Button(window, text="", width=10, height=5)
button3 = Button(window, text="", width=10, height=5)
button4 = Button(window, text="", width=10, height=5)
button5 = Button(window, text="", width=10, height=5)
button6 = Button(window, text="", width=10, height=5)
button7 = Button(window, text="", width=10, height=5)
button8 = Button(window, text="", width=10, height=5)
button9 = Button(window, text="", width=10, height=5)
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)
button4.grid(row=1, column=0)
button5.grid(row=1, column=1)
button6.grid(row=1, column=2)
button7.grid(row=2, column=0)
button8.grid(row=2, column=1)
button9.grid(row=2, column=2)

def click_button(button):
    global current_player
    if button["text"] == "":
        if current_player == "X":
            button["text"] = "X"
            current_player = "O"
            check_win()
            if not is_full():
                machine_play()
                current_player = "X"
                check_win()

def machine_play():
    empty_buttons = []
    for button in [button1, button2, button3, button4, button5, button6, button7, button8, button9]:
        if button["text"] == "":
            empty_buttons.append(button)
    if empty_buttons:
        scores = []
        for button in empty_buttons:
            button["text"] = "O"
            score = minimax(False)
            button["text"] = ""
            scores.append(score)
        max_score_index = scores.index(max(scores))
        selected_button = empty_buttons[max_score_index]
        selected_button["text"] = "O"

def evaluate():
    if check_line(button1, button2, button3):
        return 1 if button1["text"] == "X" else -1
    if check_line(button4, button5, button6):
        return 1 if button4["text"] == "X" else -1
    if check_line(button7, button8, button9):
        return 1 if button7["text"] == "X" else -1
    if check_line(button1, button4, button7):
        return 1 if button1["text"] == "X" else -1
    if check_line(button2, button5, button8):
        return 1 if button2["text"] == "X" else -1
    if check_line(button3, button6, button9):
        return 1 if button3["text"] == "X" else -1
    if check_line(button1, button5, button9):
        return 1 if button1["text"] == "X" else -1
    if check_line(button3, button5, button7):
        return 1 if button3["text"] == "X" else -1
    return 0

def check_line(button1, button2, button3):
    return button1["text"] == button2["text"] == button3["text"] != ""

def is_full():
    for button in [button1, button2, button3, button4, button5, button6, button7, button8, button9]:
        if button["text"] == "":
            return False
    return True

def minimax(is_maximizing):
    if check_win():
        return evaluate()
    if is_full():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for button in [button1, button2, button3, button4, button5, button6, button7, button8, button9]:
            if button["text"] == "":
                button["text"] = "O"
                eval = minimax(False)
                button["text"] = ""
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for button in [button1, button2, button3, button4, button5, button6, button7, button8, button9]:
            if button["text"] == "":
                button["text"] = "X"
                eval = minimax(True)
                button["text"] = ""
                min_eval = min(min_eval, eval)
        return min_eval

def check_win():
    if check_line(button1, button2, button3):
        win_message = f"Người chơi {button1['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button4, button5, button6):
        win_message = f"Người chơi {button4['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button7, button8, button9):
        win_message = f"Người chơi {button7['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button1, button4, button7):
        win_message = f"Người chơi {button1['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button2, button5, button8):
        win_message = f"Người chơi {button2['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button3, button6, button9):
        win_message = f"Người chơi {button3['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button1, button5, button9):
        win_message = f"Người chơi {button1['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif check_line(button3, button5, button7):
        win_message = f"Người chơi {button3['text']} thắng!"
        messagebox.showinfo("Kết quả", win_message)
        window.quit()
        return True
    elif is_full():
        messagebox.showinfo("Kết quả", "Hòa!")
        window.quit()
        return True
    else:
        return False

button1.bind("<Button-1>", lambda event: click_button(button1))
button2.bind("<Button-1>", lambda event: click_button(button2))
button3.bind("<Button-1>", lambda event: click_button(button3))
button4.bind("<Button-1>", lambda event: click_button(button4))
button5.bind("<Button-1>", lambda event: click_button(button5))
button6.bind("<Button-1>", lambda event: click_button(button6))
button7.bind("<Button-1>", lambda event: click_button(button7))
button8.bind("<Button-1>", lambda event: click_button(button8))
button9.bind("<Button-1>", lambda event: click_button(button9))

window.mainloop()
