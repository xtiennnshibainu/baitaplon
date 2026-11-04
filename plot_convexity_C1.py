import numpy as np
import matplotlib.pyplot as plt

# 1. Khai báo dữ liệu đầu vào (Lấy từ báo cáo C2 - Tuần 2, tập Train)
t0 = 60
z_vals = np.array([90, 120, 180])
# Xác suất thực nghiệm p_z trên tập Train do C2 tính
p_z = np.array([0.8735, 0.7497, 0.5315]) 
ln_p_z = np.log(p_z)

# 2. Xây dựng hàm tính sai số log (Hàm mục tiêu S)
def calc_S(theta, x_vals):
    # S(theta) = tổng(ln(p_z) + theta * x_z)^2
    S = np.zeros_like(theta)
    for i in range(len(theta)):
        S[i] = np.sum((ln_p_z + theta[i] * x_vals)**2)
    return S

# 3. Tính toán cho mô hình Pareto (theta = alpha)
x_pareto = np.log(z_vals / t0)
# Tạo mảng giá trị alpha từ 0.1 đến 1.0 để vẽ đồ thị
alphas = np.linspace(0.1, 1.0, 100) 
S_pareto = calc_S(alphas, x_pareto)
alpha_optimal = 0.5124 # Giá trị tối ưu C2 đã tính

# 4. Tính toán cho mô hình Mũ dịch (theta = lambda)
x_exp = z_vals - t0
# Tạo mảng giá trị lambda từ 0.001 đến 0.01
lambdas = np.linspace(0.001, 0.01, 100)
S_exp = calc_S(lambdas, x_exp)
lambda_optimal = 0.00514 # Giá trị tối ưu C2 đã tính

# 5. Vẽ đồ thị Pareto
plt.figure(figsize=(8, 5))
plt.plot(alphas, S_pareto, 'b-', label='Hàm mục tiêu $S(\\alpha)$')
plt.plot(alpha_optimal, calc_S([alpha_optimal], x_pareto), 'ro', markersize=8, label=f'Cực tiểu toàn cục ($\\alpha^* = {alpha_optimal}$)')
plt.title('Tính lồi của hàm mục tiêu - Mô hình Pareto')
plt.xlabel('Tham số $\\alpha$')
plt.ylabel('Sai số $S(\\alpha)$')
plt.grid(True)
plt.legend()
plt.savefig('convexity_pareto.png', dpi=300) 

# 6. Vẽ đồ thị Mũ dịch
plt.figure(figsize=(8, 5))
plt.plot(lambdas, S_exp, 'g-', label='Hàm mục tiêu $S(\\lambda)$')
plt.plot(lambda_optimal, calc_S([lambda_optimal], x_exp), 'ro', markersize=8, label=f'Cực tiểu toàn cục ($\\lambda^* = {lambda_optimal}$)')
plt.title('Tính lồi của hàm mục tiêu - Mô hình Mũ dịch')
plt.xlabel('Tham số $\\lambda$')
plt.ylabel('Sai số $S(\\lambda)$')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) 
plt.grid(True)
plt.legend()
plt.savefig('convexity_exp.png', dpi=300) 
