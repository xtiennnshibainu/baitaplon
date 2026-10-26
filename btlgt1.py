"""
BÀI TẬP LỚN GIẢI TÍCH 1 - ĐỀ TÀI 13
Hợp phần C: Xử lý dữ liệu và Tiền chế biến (Data Preprocessing)
Họ và tên: Võ Nhật Xuân Tiên
MSSV: 2610339
Vai trò: C1 (Cơ sở lý thuyết & Tiền xử lý dữ liệu)
"""

import os
import pandas as pd

print("Đang tiến hành phân tích dữ liệu bank-full.csv...")

# 1. Đọc file gốc (phân cách bằng dấu chấm phẩy ';')
df = pd.read_csv('bank-full.csv', sep=';')

# 2. Lọc điều kiện duration >= 60s (t0 = 60)
df_filtered = df[df['duration'] >= 60].copy()

# 3. Chia 70% Train, 30% Test (giữ nguyên thứ tự dòng ban đầu)
n_train = int(len(df_filtered) * 0.7)
df_train = df_filtered.iloc[:n_train].copy()
df_test = df_filtered.iloc[n_train:].copy()

# 4. Tạo thư mục 'processed' và xuất các file CSV
os.makedirs('processed', exist_ok=True)
df_filtered.to_csv('processed/bank-filtered.csv', index=False)
df_train.to_csv('processed/bank-train.csv', index=False)
df_test.to_csv('processed/bank-test.csv', index=False)

# 5. Tính toán xác suất thực nghiệm p_z trên tập Train 
total_train = len(df_train)
print(f"Tổng số mẫu tập Train: {total_train}")
for z in [90, 120, 180]:
    count_z = len(df_train[df_train['duration'] > z])
    p_z = count_z / total_train
    print(f"Tại z = {z}s: Số mẫu > {z} là {count_z} -> p_{z} = {p_z:.4f}")

print("\n3 file CSV đã xuất thành công vào thư mục 'processed'.")
