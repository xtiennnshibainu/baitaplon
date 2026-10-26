""" 
# Cài các thư viện hệ thống và install  pandas
import sys
import subprocess
import os
 
print("1. Đang xin cấp quyền vượt rào môi trường uv để cài Pandas...")
# Thêm cờ --break-system-packages để ép uv cho phép cài đặt
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', '--break-system-packages'])
print("Đã cài xong Pandas!\n")

""" 

# Phân tích dữ liệu 
print("2. Đang tiến hành phân tích dữ liệu bank-full.csv...")
import pandas as pd # nhập thư viện pandas, gọi tắt là pd

# Đọc file gốc
df = pd.read_csv('bank-full.csv', sep=';') # pd.read_csv(): Hàm đọc file CSV và chuyển nó thành một đối tượng DataFrame (bảng dữ liệu 2 chiều, giống Excel).
                                           # df: Biến lưu trữ bảng dữ liệu này. "df" là viết tắt mặc định của DataFrame.

# Lọc điều kiện duration >= 60
df_filtered = df[df['duration'] >= 60].copy() # df['duration'] >= 60: Trả về một mảng Boolean (True/False). 
                                              # Dòng nào có duration >= 60 thì mang giá trị True, ngược lại là False.
                                              # Trong Pandas, nếu không có .copy(), df_filtered 
                                              # chỉ là một con trỏ (view) tham chiếu đến vùng nhớ của df gốc. Nếu sau này sửa đổi df_filtered, 
                                              # nó sẽ văng cảnh báo SettingWithCopyWarning và có thể làm hỏng data gốc.

# Chia 70% Train, 30% Test giữ nguyên thứ tự dòng; * 0.7 là lấy 70%; len(df_filtered): Đếm tổng số dòng sau khi lọc.
n_train = int(len(df_filtered) * 0.7) # int(): Ép kiểu về số nguyên (vì số lượng dòng không thể là số thập phân). Kết quả gán vào biến n_train (mốc cắt).
df_train = df_filtered.iloc[:n_train].copy() 
df_test = df_filtered.iloc[n_train:].copy()

""" 
.iloc (Integer Location): Hàm cắt (slice) bảng dữ liệu dựa trên chỉ số dòng (index) vật lý, bắt đầu từ 0.
[:n_train]: Lấy từ dòng số 0 đến sát dòng n_train (không bao gồm n_train). Cú pháp cắt mảng này hệt như trong C++ hay Python cơ bản.
[n_train:]: Lấy từ dòng n_train cho đến hết bảng.
Điểm bảo vệ: Đề bài yêu cầu "chia theo thứ tự tệp, không xáo trộn (shuffle)". Việc dùng .iloc cắt thẳng một nhát từ trên xuống dưới.
""" 

# Tạo thư mục và lưu file
os.makedirs('processed', exist_ok=True) # Yêu cầu hệ điều hành tạo một thư mục tên là processed. 
                                        # exist_ok=True: Nếu thư mục này đã tồn tại, bỏ qua lệnh tạo và không văng lỗi (tránh việc chạy code lần 2 bị sập).
df_filtered.to_csv('processed/bank-filtered.csv', index=False) # .to_csv(): Hàm xuất DataFrame thành file CSV lưu vào ổ cứng.
df_train.to_csv('processed/bank-train.csv', index=False) 
df_test.to_csv('processed/bank-test.csv', index=False)
# index=False: Rất quan trọng. Mặc định Pandas sẽ ghi thêm 1 cột ngoài cùng bên trái chứa số thứ tự dòng (0, 1, 2...). 
# Set index=False để vứt cột vô nghĩa đó đi, giữ nguyên cấu trúc số cột y như file raw ban đầu.

# Tính và in xác suất
total_train = len(df_train)
print(f"Tổng số mẫu tập Train: {total_train}")
for z in [90, 120, 180]:
    count_z = len(df_train[df_train['duration'] > z])
    p_z = count_z / total_train
    print(f"Tại z = {z}s: Số mẫu > {z} là {count_z} -> p_{z} = {p_z:.4f}")

Gán tổng số dòng của tập Train vào biến total_train. Chữ f trước chuỗi string (f-string) giúp nhúng trực tiếp biến số vào chuỗi thông qua cặp ngoặc {}.

"""
for z in [90, 120, 180]: Vòng lặp duyệt qua 3 ngưỡng thời gian yêu cầu của đề.
df_train['duration'] > z: Boolean Indexing. Tìm các dòng có cuộc gọi dài hơn mốc z.
count_z = len(...): Đếm số lượng các dòng thỏa mãn điều kiện đó.
p_z = count_z / total_train: Tính xác suất thực nghiệm (Số mẫu thỏa mãn / Không gian mẫu).
{p_z:.4f}: Kỹ thuật format số trong Python. Lấy giá trị của p_z và làm tròn đúng 4 chữ số thập phân (chữ f là float).
""" 

print("\nHOÀN TẤT! 3 file CSV đã xuất thành công vào thư mục 'processed'.")
