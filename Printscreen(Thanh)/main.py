import sqlite3
import tkinter as tk
import datetime
import  random
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
        self.emoticons = [
            "（っ＾▿＾）", "(っ˘▽˘)っ", "（*＾3＾)", "(^_^)/", "＼（＾∀＾）／", "＼(^o^)／", "(≧◡≦)",
            "ヽ(＾Д＾)ﾉ", "(*•̀ᴗ•́*)", "(≧▽≦*)", "(≧∇≦*)", "٩(◕‿◕)۶",
            "ヽ(´▽`)/", "(o^▽^o)", "(＾-＾)ノ", "(*≧ω≦)", "(⌒‿⌒)", "(☆▽☆)", "(^_−)☆",
            "(・∀・)", "＼(＾▽＾)／", "(≧∇≦o)", "＼(^o^)／", "ヽ(＾Д＾)ﾉ", "(*^▽^*)", "(＾◡＾)", "(◕‿◕)",
            "(*>▽<*)", "(≧▽≦)／", "o(〃＾▽＾〃)o", "＼(≧▽≦)／", "(*≧ω≦)", "o(≧▽≦)o", "＼(＾▽＾)／",
            "(^▽^)", "(✯◡✯)", "o(∩_∩)o", "(´∇ﾉ｀)", "(≧◡≦)", "(^ｰ^)", "(´• ω •`)",
            "(*≧ω≦)", "o(≧▽≦)o", "o(^▽^)o", "(＾∇＾)", "o(≧ω≦)o", "(*>▽<*)", "(✯◡✯)", "(^▽^)",
            "(´∇ﾉ｀)", "(^ｰ^)", "(´• ω •`)", "(•̀ᴗ•́)و", "( •̀ ω •́ )و",
            "٩(◕‿◕｡)۶", "٩(｡•́‿•̀｡)۶", "(∩^o^)", "o(〃・ω・)o", "ヽ(・∀・)ﾉ", "٩(◕‿◕)۶",
            "(｡♥‿♥｡)", "٩(◕‿◕｡)۶", "٩(｡•́‿•̀｡)۶", "(≧∇≦*)ゝ", "(*⌒▽⌒*)","💪(•̀o•́)ง",  # Cố gắng lên!
            "(ง'̀-'́)ง",  # Chiến đấu hết mình!
            "ᕦ(ò_óˇ)ᕤ",  # Bạn có thể làm được!
            "(ง •̀_•́)ง",  # Đừng bỏ cuộc!
            "୧(＾ ᴗ ＾)୨",  # Tiến lên!
            "٩(๑•̀ㅂ•́)و",  # Hãy chiến thắng!
            "٩(｡•́‿•̀｡)۶",  # Không gì là không thể!
            "＼(≧▽≦)／",  # Hãy vươn lên!
            "（•̀ᴗ•́)و ̑̑",  # Bạn sẽ thành công!
            "o(>ω<)o",  # Đừng bỏ lỡ cơ hội!
            "(๑•̀ㅂ•́)و✧",  # Quyết tâm nào!
            "(*•̀ᴗ•́*)و ̑̑",  # Tiến bước thôi!
            "(•̀o•́)ง",  # Hãy kiên định!
            "(ง •̀_•́)ง",  # Hãy dũng cảm!
            "ᕦ(ò_óˇ)ᕤ"  # Bạn là người mạnh mẽ!,,
            ,"(｡◕‿◕｡)",  # Dễ thương
            "(◕‿◕✿)",  # Dễ thương với hoa
            "(*≧ω≦)",  # Dễ thương phấn khích
            "(｡♥‿♥｡)",  # Dễ thương với trái tim
            "(◕ᴗ◕✿)",  # Dễ thương và nhẹ nhàng
            "(≧◡≦)",  # Dễ thương vui vẻ
            "(✿◠‿◠)",  # Dễ thương và bình yên
            "(｡♥‿♥｡)",  # Dễ thương với tình yêu
            "(っ◔◡◔)っ",  # Dễ thương và ôm
            "(⌒‿⌒)",  # Dễ thương và cười
            "(^•ω•^)",  # Dễ thương như mèo
            "(≧ω≦)",  # Dễ thương hào hứng
            "(✯◡✯)",  # Dễ thương vui vẻ
            "(◕ω◕)",  # Dễ thương và tò mò
            "(*^‿^*)",  # Dễ thương và ngượng ngùng
            "(✿´‿`)",  # Dễ thương với hoa
            "(◕‿◕✿)",  # Dễ thương và tươi sáng
            "(っ˘ω˘ς )",  # Dễ thương và buồn ngủ
            "(｡•ω•｡)",  # Dễ thương và nhẹ nhàng
            "(｡･ω･｡)",  # Dễ thương và ngoan ngoãn
            "(･ω<)☆",  # Dễ thương và nháy mắt
            "(✿◠‿◠)",  # Dễ thương và thoải mái
            "(｡◕‿◕｡)",  # Dễ thương và cười
            "(*≧▽≦)",  # Dễ thương và hạnh phúc
            "(^ _ ^)/",  # Dễ thương và vẫy tay
            "(☆ω☆)",  # Dễ thương và ngạc nhiên
            "(｡♥‿♥｡)",  # Dễ thương và đáng yêu
            "( ͡° ᴥ ͡°)",  # Dễ thương và bí ẩn
            "(≧︿≦)",  # Dễ thương và buồn
            "(｡•‿•｡)",  # Dễ thương và tự hào
            "(≧◡≦)",  # Dễ thương và vui vẻ
            "(｡♥‿♥｡)",  # Dễ thương và yêu thương
            "(°◡°♡)",  # Dễ thương và ngọt ngào
            "(´｡• ᵕ •｡`)",  # Dễ thương và dịu dàng
            "( •ω• )",  # Dễ thương và hạnh phúc
            "(｡♥‿♥｡)",  # Dễ thương và yêu thương
            "(/•-•)/",  # Dễ thương và vẫy tay
            "(* ^ ω ^)",  # Dễ thương và cười
            "(๑˃ᴗ˂)ﻭ",  # Dễ thương và quyết tâm
            "(⁀ᗢ⁀)",  # Dễ thương và ngây thơ
            "(｡◕‿◕｡)",  # Dễ thương và ngạc nhiên
            "(◕‿◕✿)",  # Dễ thương và tươi sáng
            "(っ˘ω˘ς )",  # Dễ thương và buồn ngủ
            "(≧◡≦)",  # Dễ thương và hạnh phúc
            "(｡･ω･｡)",  # Dễ thương và ngoan ngoãn
            "(✿´‿`)",  # Dễ thương và tươi sáng
            "(o´▽`o)",  # Dễ thương và hào hứng
            "(✿╹◡╹)",  # Dễ thương và vui vẻ
            "(｡◕‿◕｡)",  # Dễ thương và ngọt ngào

        ]
        self.create_gui()
        self.chao()
        self.master.after(12000, self.chay)

    def create_gui(self):
        self.text_var = tk.StringVar(value="")
        self.text_label = tk.Label(self.master, text="", textvariable=self.text_var,
                                   font=("Helvetica", 16, 'bold'), bg="#222121", fg="#CCCC00",  # Đổi màu chữ và độ đậm
                                   wraplength=self.master.winfo_screenwidth() - 40, padx=20, pady=20)
        self.text_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

    def chao(self):
        try:
            current_hour = datetime.datetime.now().hour
            if 5 <= current_hour < 12:
                greeting = f"Chào buổi sáng, cậu chủ Trí🤗✨(～￣▽￣)～   {random.choice(self.emoticons)}"
            elif 12 <= current_hour < 18:
                greeting = f"Chào buổi chiều, cậu chủ Trí🤗✨(～￣▽￣)～   {random.choice(self.emoticons)}"
            else:
                greeting = f"Chào buổi tối, cậu chủ Trí🤗✨(～￣▽￣)～   {random.choice(self.emoticons)}"

            self.text = greeting
            self.current_text = ""
            self.show_window()
            for i in range(len(self.text)):
                self.master.after(int(i * 50), self._update_text, i)
            self.master.after(3000, self.pause)
        except:
            pass

    def say(self):
        try:
            print("say")
            self.text = f"{self.get_sentence_from_db()}     {random.choice(self.emoticons)}"
            print("self.text =", self.text)
            self.current_text = ""
            self.show_window()
            for i in range(len(self.text)):
                self.master.after(int(i * 50), self._update_text, i)
            self.master.after(int(len(self.text) * 50) + 2000, self.pause)
        except:
            pass
    def pause(self):
        # Dừng lại 3 giây
        self.master.after(3000, self.hide_window)
    def _update_text(self, index):
        if index < len(self.text):
            self.current_text += self.text[index]
            self.text_var.set(self.current_text)
    def get_sentence_from_db(self):
        try:
            conn = sqlite3.connect('Database/sentences.db')
            c = conn.cursor()
            c.execute('''
                                SELECT id, sentence, times 
                                FROM sentences
                            ''')
            result = c.fetchall()
            if result:
                result = random.choice(result)
                print(result)
                id, sentence, times = result
                c.execute('''
                                    UPDATE sentences
                                    SET times = ?
                                    WHERE id = ?
                                ''', (int(times) + 1, id))
                conn.commit()
                conn.close()
                return sentence
            conn.close()
            return ""
        except:
            pass
    def chay(self):
        print("chay(self)")
        self.say()
        self.master.after(1500000, self.chay)  # 2040 giây là 34 phút
        #self.master.after(30000, self.chay)

    def hide_window(self):
        self.text_var.set("")
        self.text_label.configure(text="")
        self.master.withdraw()
    def show_window(self):
        self.master.deiconify()

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
