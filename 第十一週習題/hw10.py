import math
import cmath

# 傅立葉正轉換 DFT
def dft(f):
    N = len(f)
    F = []
    for k in range(N):
        s = 0
        for n in range(N):
            angle = -2j * math.pi * k * n / N
            s += f[n] * cmath.exp(angle)
        F.append(s)
    return F

# 傅立葉逆轉換 IDFT
def idft(F):
    N = len(F)
    f = []
    for n in range(N):
        s = 0
        for k in range(N):
            angle = 2j * math.pi * k * n / N
            s += F[k] * cmath.exp(angle)
        f.append(s / N)
    return f

# 測試用訊號
f = [1, 2, 3, 4]

# 正轉換
F = dft(f)
print("DFT(F) =", F)

# 逆轉換
f_recovered = idft(F)
print("IDFT(f) =", f_recovered)
