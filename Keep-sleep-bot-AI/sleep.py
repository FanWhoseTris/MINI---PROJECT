try:
    import tkinter as tk
    from datetime import datetime
    import os


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
            self.label = tk.Label(self.root, text="Số giây còn lại:", bg="yellow", font=("Helvetica", 16), fg="red")
            self.label.pack()

            self.so_giay_var = tk.StringVar()
            self.so_giay_label = tk.Label(self.root, textvariable=self.so_giay_var, bg="yellow",
                                          font=("Helvetica", 25), fg="red")
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
        start_time = 21
        minu = 0
        with open("time.txt", "r") as f:
            line = f.readlines()
        lin = line[0].split(" ")
        lines = lin[1].split(":")
        # print(lines[0])
        if lines[0] != "" or lines[0] != " " or lines[0] != None:
            start_time = int(lines[0])
            minu = int(lines[1])
            thoi_gian_moc = datetime(datetime.now().year, datetime.now().month, datetime.now().day, start_time, minu)
        thoi_gian_hien_tai = datetime.now()
        # print(self.time)
        # print(thoi_gian_hien_tai)
        thoi_gian_con_lai = thoi_gian_moc - thoi_gian_hien_tai
        # print(int(thoi_gian_con_lai.total_seconds()))
        os.system("shutdown -a")
        os.system(f"shutdown -s -t {int(thoi_gian_con_lai.total_seconds())}")
        # print(time)
        app = ThongBaoSoGiayConLai(thoi_gian_moc)
        app.chay()
except Exception as e:
    print(e)