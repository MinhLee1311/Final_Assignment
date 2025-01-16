import cv2
import numpy as np

# Đọc file ảnh mã QR
image_path = "distorted_qrcode2.png"
qr_image = cv2.imread(image_path)
if qr_image is None:
    print("Không thể đọc file ảnh")
    exit()

# Chuyển ảnh sang grayscale để xác định vùng mã QR
gray_image = cv2.cvtColor(qr_image, cv2.COLOR_BGR2GRAY)

# Tìm contour lớn nhất (giả định đó là vùng mã QR)
_, thresh = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not contours:
    print("Không tìm thấy vùng mã QR trong ảnh.")
    exit()

# Lấy contour lớn nhất
qr_contour = max(contours, key=cv2.contourArea)

# Tìm bounding box của vùng mã QR
x, y, w, h = cv2.boundingRect(qr_contour)

# Padding để khung lưới di chuyển vào trong
padding = 4  # căn chỉnh vị trí khung lưới bao phủ

# Điều chỉnh bounding box
x += padding
y += padding
w -= 2 * padding
h -= 2 * padding

# Crop vùng mã QR từ ảnh gốc
qr_region = qr_image[y:y+h, x:x+w]
gray_region = gray_image[y:y+h, x:x+w]

# Lấy kích thước của vùng mã QR
height, width, _ = qr_region.shape

# Số ô trong lưới
grid_size = 41

# Tạo một bản sao của vùng mã QR để vẽ lưới
overlay_image = qr_region.copy()

# Tính kích thước của mỗi ô vuông
cell_height = height / grid_size
cell_width = width / grid_size

# Vẽ lưới và kiểm tra màu trong từng ô
for row in range(grid_size):
    for col in range(grid_size):
        # Xác định tọa độ của ô vuông hiện tại
        start_x = int(col * cell_width)
        start_y = int(row * cell_height)
        end_x = int((col + 1) * cell_width)
        end_y = int((row + 1) * cell_height)

        # Crop vùng nhỏ tương ứng với ô vuông
        cell_region = gray_region[start_y:end_y, start_x:end_x]

        # Đếm số pixel màu đen và màu trắng trong ô
        black_count = np.sum(cell_region < 128)
        white_count = np.sum(cell_region >= 128)

        # Xác định màu cho ô dựa trên số lượng pixel
        if black_count > white_count:
            overlay_image[start_y:end_y, start_x:end_x] = (0, 0, 0)  # Tô đen
        else:
            overlay_image[start_y:end_y, start_x:end_x] = (255, 255, 255)  # Tô trắng


# # Vẽ lưới trên mã QR
# for i in range(grid_size + 1):
#     # Vẽ các đường ngang
#     start_point = (0, int(i * cell_height))
#     end_point = (width, int(i * cell_height))
#     cv2.line(overlay_image, start_point, end_point, (0, 255, 0), 1)

#     # Vẽ các đường dọc
#     start_point = (int(i * cell_width), 0)
#     end_point = (int(i * cell_width), height)
#     cv2.line(overlay_image, start_point, end_point, (0, 255, 0), 1)

# # đường viền ngoài cùng
# cv2.rectangle(overlay_image, (0, 0), (width - 1, height - 1), (0, 255, 0), 1)


## Xóa các phần nhiễu ở ngoài hình mã QR, hình nền:
# Đặt màu trắng cho toàn bộ ảnh trước
qr_image[:, :] = (255, 255, 255)

# Sau đó chèn lại vùng QR đã xử lý
qr_image[y:y+h, x:x+w] = overlay_image


# Hiển thị ảnh với lưới phủ
cv2.imshow("QR Code with Grid and Colored Cells", qr_image)

# Lưu ảnh mới với lưới
output_path = "image_sau_chuyen_doi.png"
cv2.imwrite(output_path, qr_image)
print(f"Ảnh đã được lưu tại {output_path}")

cv2.waitKey(0)
cv2.destroyAllWindows()
