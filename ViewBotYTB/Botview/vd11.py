from selenium import webdriver

# Khởi tạo WebDriver
driver = webdriver.Chrome()

# Link YouTube bạn muốn mở
youtube_url = "https://www.youtube.com/watch?v=9KDlWM-KUe8"

# Mở đường link
driver.get(youtube_url)
#movie_player > div.ytp-cued-thumbnail-overlay > button
# Dùng vòng lặp vô hạn để giữ cửa sổ mở
#movie_player > div.ytp-cued-thumbnail-overlay > button:nth-child(3)
while True:
    pass
