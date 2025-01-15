import cv2
import numpy as np

# Đọc ảnh
image_path = "M:/CHUYEN_NGANH/THI_GIAC_MAY_TINH/CUOI_KY/C3.jpg"  # Đường dẫn tới ảnh bài làm


# Chuyển sang thang xám
image_color = cv2.imread(image_path)
gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)


# Hiển thị vùng ảnh (chỉnh sửa tọa độ theo từng vùng)
def extract_region(image, x, y, w, h):
    return image[y:y+h, x:x+w]

# Ví dụ: Vùng 

_, binary_image = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
mssv_region = extract_region(binary_image, 1798, 353, 290, 691)
md_region = extract_region(binary_image, 2174, 353, 145, 691)
part_1_1_region = extract_region(binary_image, 218, 1243, 398, 601)
part_1_2_region = extract_region(binary_image, 776, 1243, 398, 601)

part_2_1_region = extract_region(binary_image, 225, 2064, 181, 262)
part_2_2_region = extract_region(binary_image, 411, 2064, 210, 262)
part_2_3_region = extract_region(binary_image, 786, 2064, 175, 262)
part_2_4_region = extract_region(binary_image, 970, 2064, 210, 262)

part_3_1_region = extract_region(binary_image, 222, 2589, 239, 656)
part_3_2_region = extract_region(binary_image, 581, 2589, 237, 656)
part_3_3_region = extract_region(binary_image, 937, 2589, 243, 656)
part_3_4_region = extract_region(binary_image, 1295, 2589, 237, 656)
part_3_5_region = extract_region(binary_image, 1652, 2589, 240, 656)
part_3_6_region = extract_region(binary_image, 2009, 2589, 238, 656)
##########################################################################
def extract_mssv_from_bubbles(num_columns,num_rows,region):
    # Định nghĩa số cột và hàng (số lượng ô)
    # Tính kích thước của mỗi ô
    cell_width = 48 #mssv_region.shape[1] // num_columns
    cell_height =  69 #mssv_region.shape[0]  // num_rows

    # Biến lưu MSSV
    mssv = ""

    # Duyệt qua từng cột (chữ số trong MSSV)
    for col in range(num_columns):
        detected_digit = -1  # Biến lưu số đã phát hiện

        # Duyệt qua từng hàng trong cột (số từ 0 đến 9)
        for row in range(num_rows):
            # Cắt từng ô
            cell_x = col * cell_width
            cell_y = row * cell_height
            cell_roi = region[cell_y:cell_y+cell_height, cell_x:cell_x+cell_width]
            # cv2.imshow(f"Cell at ({col}, {row})", cell_roi)
            # số điểm đen trên 1 cell
            #print(f"NONZERO: {cv2.countNonZero(cell_roi)}")
            # Kiểm tra nếu ô được tô đen (tính tổng số điểm đen)
            if cv2.countNonZero(cell_roi) < 2400:
                detected_digit = row  # Ghi nhận hàng (chữ số)
        # Thêm chữ số vào MSSV (nếu tìm thấy)
        if detected_digit != -1:
            mssv += str(detected_digit)
        else:
            mssv += "?"  # Nếu không tìm thấy số, đặt dấu "?" để kiểm tra lỗi
    # In ra kết quả để kiểm tra
    #print(f"Extracted MSSV: {mssv},{cell_height},{cell_width}")
    return mssv
# Trích xuất MSSV
###################################################################
def extract_part_1_from_bubbles(num_columns,num_rows,region,num):
    # Định nghĩa số cột và hàng (số lượng ô)
    # Tính kích thước của mỗi ô
    cell_width = 97 #mssv_region.shape[1] // num_columns
    cell_height = 60 #mssv_region.shape[0]  // num_rows
    answer =""
    for row in range(num_rows):
        detected_digit = -1  # Biến lưu số đã phát hiện
        for col in range(num_columns):
            # Cắt từng ô
            cell_x = col * cell_width
            cell_y = row * cell_height
            cell_roi = region[cell_y:cell_y+cell_height, cell_x:cell_x+cell_width]
            # số điểm đen trên 1 cell
            #cv2.imshow(f"Cell at ({col}, {row})", cell_roi)
            #print(f"NONZERO: {cv2.countNonZero(cell_roi)}")
            # Kiểm tra nếu ô được tô đen (tính tổng số điểm đen)
            if cv2.countNonZero(cell_roi) < 5200:
                detected_digit = row  # Ghi nhận hàng (chữ số)
                column_label = chr(ord('A') + col)  # Chuyển cột thành ký tự (A, B, C, ...)
        if detected_digit != -1:
            if num == 1:
                answer += str(detected_digit + 1) + column_label + "\n "
            elif num ==2:
                answer += str(detected_digit + 11) + column_label + "\n "
        else:
            answer += "?\n "  
    return answer
########################################################################
def extract_part_2_from_bubbles(num_columns,num_rows,region,num):
    # Định nghĩa số cột và hàng (số lượng ô)
    # Tính kích thước của mỗi ô
    cell_width = region.shape[1] // num_columns
    cell_height = region.shape[0]  // num_rows

    threshold = 5600 if num == 1 else 5400 if num == 3 else 6500  # Ngưỡng tùy thuộc vào num
    answer = ""
    for row in range(num_rows):
        detected_col = -1  # Biến lưu số đã phát hiện
        for col in range(num_columns):
            # Cắt từng ô
            cell_x = col * cell_width
            cell_y = row * cell_height
            cell_roi = region[cell_y:cell_y+cell_height, cell_x:cell_x+cell_width]
            # cv2.imshow(f"Cell at ({col}, {row})", cell_roi)
            # số điểm đen trên 1 cell
            # Kiểm tra nếu ô được tô đen (tính tổng số điểm đen)
            if cv2.countNonZero(cell_roi) < threshold:  # Ngưỡng tùy chỉnh
                detected_col = "ĐÚNG" if col == 0 else "SAI"  # Ghi nhận trạng thái cột
        row_label = chr(ord('A') + row)
        if detected_col != -1:
            answer += f"{num}{row_label} :{detected_col}\n "
        else:
            answer += f"{num}{row_label} ?\n "  # Nếu không phát hiện, trả về "?"
    return answer
###################################################################################
def extract_part_3_from_bubbles(num_columns,num_rows,region,num):
    # Định nghĩa số cột và hàng (số lượng ô)
    # Tính kích thước của mỗi ô
    cell_width = region.shape[1] // num_columns
    cell_height = region.shape[0]  // num_rows

    symbols = ["-", ","] + [str(i) for i in range(10)]
    answer = f"{num}: "  
    for col in range(num_columns):
        detected_symbol = " "  # Biến lưu số đã phát hiện
        for row in range(num_rows):
            # Cắt từng ô
            cell_x = col * cell_width
            cell_y = row * cell_height
            cell_roi = region[cell_y:cell_y+cell_height, cell_x:cell_x+cell_width]
            # cv2.imshow(f"Cell at ({col}, {row})", cell_roi)
            # số điểm đen trên 1 cell
            # Kiểm tra nếu ô được tô đen (tính tổng số điểm đen)
            if cv2.countNonZero(cell_roi) < 3000:
                detected_symbol = symbols[row]
                break
        answer += detected_symbol
    return answer
########################################################################################
mssv = extract_mssv_from_bubbles(6,9,mssv_region)
md = extract_mssv_from_bubbles(3,9,md_region)
answer_part_1_1 = extract_part_1_from_bubbles(4,10,part_1_1_region,1)
answer_part_1_2 = extract_part_1_from_bubbles(4,10,part_1_2_region,2)

answer_part_2_1 = extract_part_2_from_bubbles(2,4,part_2_1_region,1)
answer_part_2_2 = extract_part_2_from_bubbles(2,4,part_2_2_region,2)
answer_part_2_3= extract_part_2_from_bubbles(2,4,part_2_3_region,3)
answer_part_2_4 = extract_part_2_from_bubbles(2,4,part_2_4_region,4)

answer_part_3_1 = extract_part_3_from_bubbles(4,11,part_3_1_region,1)
answer_part_3_2 = extract_part_3_from_bubbles(4,11,part_3_2_region,2)
answer_part_3_3 = extract_part_3_from_bubbles(4,11,part_3_3_region,3)
answer_part_3_4 = extract_part_3_from_bubbles(4,11,part_3_4_region,4)
answer_part_3_5 = extract_part_3_from_bubbles(4,11,part_3_5_region,5)
answer_part_3_6 = extract_part_3_from_bubbles(4,11,part_3_6_region,6)

print(f"MSSV: {mssv}")
print(f"Ma De: {md}")
print(f"Anwer_part1:\n {answer_part_1_1}\n {answer_part_1_2}")
print(f"Anwer_part2:\n {answer_part_2_1}\n {answer_part_2_2}\n {answer_part_2_3}\n {answer_part_2_4}")
print(f"Anwer_part3:\n {answer_part_3_1}\n {answer_part_3_2}\n {answer_part_3_3}\n {answer_part_3_4}\n {answer_part_3_5}\n {answer_part_3_6}")

