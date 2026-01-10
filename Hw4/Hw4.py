import torch

def solve_poly_root(coeffs, learning_rate=0.01, iterations=2000, start_x=1.0):
    """
    使用梯度下降尋找多項式的實數根
    coeffs: 係數陣列 [c0, c1, c2, ... cn]，代表 c0 + c1*x + c2*x^2 + ...
    """
    # 將 x 設為需要計算梯度的張量，初始值建議隨機或給定一個起始點
    x = torch.tensor([float(start_x)], requires_grad=True)
    
    # 使用 Adam 優化器，它比單純的梯度下降更穩定，能自動調整學習率
    optimizer = torch.optim.Adam([x], lr=learning_rate)

    for i in range(iterations):
        optimizer.zero_grad() # 清除之前的梯度
        
        # 計算多項式 f(x) = sum(c_i * x^i)
        f_x = 0
        for degree, c in enumerate(coeffs):
            f_x += c * (x ** degree)
            
        # 定義損失函數 Loss = f(x)^2
        loss = f_x ** 2
        
        # 反向傳播計算梯度
        loss.backward()
        
        # 更新 x
        optimizer.step()
        
        # 每 400 次印出一次結果觀察進度
        if i % 400 == 0:
            print(f"Iteration {i}: x = {x.item():.6f}, f(x)^2 = {loss.item():.8f}")

    return x.item()

# --- 測試案例 ---
# 假設我們要解 f(x) = x^5 - 2x - 1 = 0  (n=5, 五次多項式)
# 係數對應 [c0, c1, c2, c3, c4, c5] -> [-1, -2, 0, 0, 0, 1]
my_coeffs = [-1.0, -2.0, 0.0, 0.0, 0.0, 1.0]

root = solve_poly_root(my_coeffs, start_x=1.5)

print("-" * 30)
print(f"最終求得的近似根 x ≈ {root:.8f}")
