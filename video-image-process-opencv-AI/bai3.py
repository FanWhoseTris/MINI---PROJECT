import matplotlib.pyplot as plt

# Xử lý và hiển thị hình ảnh
image = 'b1.jpg'  # Hình ảnh đã được xử lý
plt.imshow(image)
plt.show()

# Lưu hình ảnh ra file
output_path = "path_to_save_image.png"  # Đường dẫn và tên file để lưu
plt.savefig(output_path)
