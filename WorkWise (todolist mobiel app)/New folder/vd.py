import winsound
from win10toast import ToastNotifier

def timer(remider,seconds):
    notificator = ToastNotifier()
    notificator.show_toast("Reminder",f"""WorkWise Reminder in {seconds} Seconds""",duration=20)
    notificator.show_toast(f"Reminder",remider,duration=20)

    frequency=2500
    duration=1000
    winsound.Beep(frequency,duration)

if __name__ == "__main__":
    words = input("what:")
    sec = int(input("enter secs:"))
    timer(words,sec)