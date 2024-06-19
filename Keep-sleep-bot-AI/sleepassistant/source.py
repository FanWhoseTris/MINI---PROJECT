import tkinter as tk
from datetime import datetime, timedelta


class Thongbao:
    def __init__(self, root,time ):
        self.root = root
        self.root.title("Thông Báo")
        self.root.geometry("900x500+400+100")
        thoi_gian_hien_tai = datetime.now()
        self.time = time
        # Tạo và đặt nhãn thứ nhất
        self.label1 = tk.Label(root, text="Trí ơi", font=("Arial", 43))
        self.label1.pack(pady=10)  # Thêm khoảng cách dưới nhãn

        # Tạo và đặt nhãn thứ hai
        self.label2 = tk.Label(root, text="Tập trung vào", font=("Arial", 61))
        self.label2.pack(pady=10)  # Thêm khoảng cách dưới nhãn
        # Tạo và đặt nhãn thứ hai
        self.label2 = tk.Label(root, text=f"Bạn chỉ còn {int((self.time- thoi_gian_hien_tai).total_seconds())} giây", font=("Arial", 61))
        self.label2.pack(pady=10)  # Thêm khoảng cách dưới nhãn
        # Tạo nút nhấn
        self.button = tk.Button(root, text="Tôi sẽ tập trung", command=self.click_button, font=("Arial", 34))
        self.button.pack(pady=20)  # Thêm khoảng cách dưới nút

    def click_button(self):
        self.root.destroy()

class ThongBaoSoGiayConLai:
    def __init__(self, thoi_gian_moc):
        self.thoi_gian_moc = thoi_gian_moc
        self.root = tk.Tk()
        self.root.title("Thông Báo Số Giây Còn Lại")
        self.root.attributes('-topmost', True)
        self.root.config(bg="yellow")
        self.root.geometry("200x70+0+0")
        try:
            icon_path = "revise.ico"
            self.root.iconbitmap(default=icon_path)
        except Exception as e:
            print(e)
        self.label = tk.Label(self.root, text="Số giây còn lại:",bg="yellow",font=("Helvetica", 16),fg="red")
        self.label.pack()

        self.so_giay_var = tk.StringVar()
        self.so_giay_label = tk.Label(self.root, textvariable=self.so_giay_var,bg="yellow",font=("Helvetica", 25),fg="red")
        self.so_giay_label.pack()

        self.cap_nhat_so_giay()
        self.root.after(1000, self.cap_nhat_so_giay)

    def cap_nhat_so_giay(self):
        thoi_gian_hien_tai = datetime.now()
        thoi_gian_con_lai = self.thoi_gian_moc - thoi_gian_hien_tai
        so_giay_con_lai = int(thoi_gian_con_lai.total_seconds())
        self.so_giay_var.set(str(so_giay_con_lai))
        self.root.after(1000, self.cap_nhat_so_giay)

    def chay(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Sử dụng lớp ThongBaoSoGiayConLai
    thoi_gian_moc = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 21, 0)  # Thời gian mốc 9 giờ PM
    #app = ThongBaoSoGiayConLai(thoi_gian_moc)
    #app.chay()
    approot = tk.Tk()
    app = Thongbao(approot,thoi_gian_moc)
    approot.mainloop()


