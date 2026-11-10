import pandas as pd
import numpy as np

# 1. Đọc dữ liệu tập train 
df_train = pd.read_csv('bank-train.csv')

# Đề bài yêu cầu t0 = 60. Lọc những cuộc gọi >= 60 giây.
t0 = 60
df_valid = df_train[df_train['duration'] >= t0]
total_train_calls = len(df_valid)

print(f"Tổng số cuộc gọi hợp lệ (>= 60s) trong tập train: {total_train_calls}")

# 2. Các mốc thời gian z cần kiểm tra theo đề
z_values = [90, 120, 180]
p_z_dict = {}

# 3. Tính tỷ lệ thực tế p_z cho từng mốc z
print("\n--- TÍNH TỶ LỆ p_z ---")
for z in z_values:
    # Đếm số cuộc gọi vượt mức z
    exceed_z_count = len(df_valid[df_valid['duration'] > z])
    p_z = exceed_z_count / total_train_calls
    
    # Kiểm tra điều kiện đề bài: p_z = 0 phải loại khỏi phép log và báo cáo
    if p_z == 0:
        print(f"CẢNH BÁO: Tại z = {z}, p_z = 0. Loại khỏi phép tính log.")
    else:
        p_z_dict[z] = p_z
        print(f"Tại z = {z}: p_z = {p_z:.6f}")

# Kiểm tra điều kiện: thiếu hai mức hợp lệ thì không ước lượng
if len(p_z_dict) < 2:
    print("\nTHẤT BẠI: Không đủ 2 mức hợp lệ để ước lượng tham số.")
else:
    print("\n--- ƯỚC LƯỢNG THAM SỐ THETA ---")
    
    # 4. Hàm tính theta chung
    def calculate_theta(model_name, x_z_func):
        sum_xz_log_pz = 0
        sum_xz_squared = 0
        
        for z, p_z in p_z_dict.items():
            x_z = x_z_func(z)
            log_pz = np.log(p_z)
            
            sum_xz_log_pz += (x_z * log_pz)
            sum_xz_squared += (x_z ** 2)
            
        # Công thức nghiệm tối ưu
        theta = - (sum_xz_log_pz / sum_xz_squared)
        
        print(f"\nMô hình {model_name}:")
        # Kiểm tra điều kiện theta = 0 không cho mật độ chuẩn hóa
        if theta <= 0:
            print(f"  -> THẤT BẠI: Tham số ước lượng Theta = {theta:.6f} (<= 0), không cho mật độ chuẩn hóa.")
        else:
            print(f"  -> Tham số ước lượng Theta = {theta:.6f}")
            
        return theta

    # 5. Chạy tính toán cho 2 mô hình theo công thức đề bài
    # Mô hình Pareto: x_z = log(z / t0), Theta chính là Alpha
    theta_pareto = calculate_theta("Pareto (Theta = Alpha)", lambda z: np.log(z / t0))
    
    # Mô hình Mũ (Exponential): x_z = z - t0, Theta chính là Lambda
    theta_exponential = calculate_theta("Mũ dịch (Theta = Lambda)", lambda z: z - t0)
