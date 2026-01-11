import numpy as np
from scipy.linalg import lu

class LinearAlgebraLab:
    def __init__(self):
        # 建立一個測試用的方陣
        self.A = np.array([[4.0, 1.0, 2.0],
                           [1.0, 3.0, 0.0],
                           [2.0, 0.0, 5.0]])
        
        # 建立一個測試用的非方陣 (用於 SVD/PCA)
        self.X = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)

    # 1. 遞迴計算行列式
    def recursive_det(self, matrix):
        n = len(matrix)
        if n == 1: return matrix[0, 0]
        if n == 2: return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
        
        det = 0
        for j in range(n):
            # 取得餘子矩陣 (移除第 0 列與第 j 欄)
            sub_matrix = np.delete(np.delete(matrix, 0, axis=0), j, axis=1)
            det += ((-1)**j) * matrix[0, j] * self.recursive_det(sub_matrix)
        return det

    # 2. LU 分解計算行列式
    def lu_determinant(self, matrix):
        P, L, U = lu(matrix)
        # det(A) = det(P) * det(L) * det(U)
        # L 的對角線全為 1，所以 det(L)=1；U 的行列式為對角線乘積
        det_p = np.linalg.det(P) # P 是置換矩陣，其行列式為 1 或 -1
        det_u = np.prod(np.diag(U))
        return det_p * det_u

    # 3. 驗證三大分解 (LU, Eigen, SVD)
    def verify_decompositions(self):
        print("--- 開始驗證矩陣分解 ---")
        # LU 驗證
        P, L, U = lu(self.A)
        print(f"LU 分解相乘還原: {np.allclose(P @ L @ U, self.A)}")

        # 特徵值分解 (Eigen)
        evals, evecs = np.linalg.eig(self.A)
        reconstructed_eig = evecs @ np.diag(evals) @ np.linalg.inv(evecs)
        print(f"特徵值分解相乘還原: {np.allclose(reconstructed_eig, self.A)}")

        # SVD 分解
        U_s, S_s, Vh_s = np.linalg.svd(self.A)
        reconstructed_svd = U_s @ np.diag(S_s) @ Vh_s
        print(f"SVD 分解相乘還原: {np.allclose(reconstructed_svd, self.A)}")

    # 4. 用特徵值分解來做 SVD (A = U S V^T)
    def svd_from_eig(self, A):
        # 1. V 來自 A^T A 的特徵向量
        evals_v, V = np.linalg.eigh(A.T @ A)
        # 排序 (降序)
        idx = evals_v.argsort()[::-1]
        evals_v, V = evals_v[idx], V[:, idx]
        
        # 2. S (奇異值) 為 A^T A 特徵值的平方根
        S = np.sqrt(np.maximum(evals_v, 0))
        
        # 3. U = A @ V @ inv(Sigma)
        # 只處理非零奇異值以避免除以零
        S_inv = np.zeros_like(S)
        S_inv[S > 1e-10] = 1.0 / S[S > 1e-10]
        U = A @ V @ np.diag(S_inv)
        
        return U, S, V.T

    # 5. PCA 主成分分析 (使用 SVD 實作)
    def run_pca(self, X, n_components=1):
        # 中心化 (去均值)
        X_centered = X - np.mean(X, axis=0)
        # 使用 SVD
        U, S, Vh = np.linalg.svd(X_centered, full_matrices=False)
        # 投影到前 n 個主成分
        projected = X_centered @ Vh.T[:, :n_components]
        return projected

# --- 執行測試 ---
lab = LinearAlgebraLab()

print(f"1. 遞迴行列式結果: {lab.recursive_det(lab.A):.2f}")
print(f"2. LU 分解行列式結果: {lab.lu_determinant(lab.A):.2f}")
print("-" * 30)

lab.verify_decompositions()
print("-" * 30)

print("3. 使用特徵值分解實作 SVD:")
U_my, S_my, Vh_my = lab.svd_from_eig(lab.X)
print(f"   還原矩陣是否成功: {np.allclose(U_my @ np.diag(S_my) @ Vh_my, lab.X)}")

print("-" * 30)
pca_result = lab.run_pca(lab.X, n_components=1)
print(f"4. PCA 降維結果 (從 2D 降至 1D):\n{pca_result}")
