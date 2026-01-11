import numpy as np

def entropy(p):
    p = np.array(p)
    return -np.sum(p * np.log2(p + 1e-12)) # 加上極小值避免 log(0)

def cross_entropy(p, q):
    p, q = np.array(p), np.array(q)
    return -np.sum(p * np.log2(q + 1e-12))

def kl_divergence(p, q):
    return cross_entropy(p, q) - entropy(p)

def mutual_information(p_xy):
    # p_xy 是聯合機率分佈矩陣
    p_xy = np.array(p_xy)
    p_x = np.sum(p_xy, axis=1)
    p_y = np.sum(p_xy, axis=0)
    mi = 0
    for i in range(len(p_x)):
        for j in range(len(p_y)):
            if p_xy[i,j] > 0:
                mi += p_xy[i,j] * np.log2(p_xy[i,j] / (p_x[i] * p_y[j]))
    return mi

# 驗證 cross_entropy(p, p) 是最小值
p = [0.7, 0.3]
q = [0.6, 0.4] # 稍有偏離的 q
q_match = [0.7, 0.3] # 等於 p 的 q

ce_p_q = cross_entropy(p, q)
ce_p_p = cross_entropy(p, q_match)

print(f"H(p, q): {ce_p_q:.4f}")
print(f"H(p, p): {ce_p_p:.4f} (即為熵)")
print(f"驗證 H(p, p) <= H(p, q): {ce_p_p <= ce_p_q}")
