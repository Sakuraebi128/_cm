import cmath

def root2(a, b, c):
    """
    計算二次多項式 ax^2 + bx + c = 0 的兩個根
    （可為實數或複數）
    """
    if a == 0:
        raise ValueError("a 不能為 0，否則不是二次多項式")

    # 判別式
    D = b**2 - 4*a*c

    # 使用 cmath.sqrt，可處理複數
    sqrt_D = cmath.sqrt(D)

    # 兩個根
    x1 = (-b + sqrt_D) / (2*a)
    x2 = (-b - sqrt_D) / (2*a)

    return x1, x2
def f(x, a, b, c):
    return a*x**2 + b*x + c
# 測試範例（會產生複數根）
a, b, c = 1, 2, 5

x1, x2 = root2(a, b, c)

print("x1 =", x1)
print("x2 =", x2)

# 驗證 f(x) ≈ 0
print("驗證 x1:", cmath.isclose(f(x1, a, b, c), 0, abs_tol=1e-9))
print("驗證 x2:", cmath.isclose(f(x2, a, b, c), 0, abs_tol=1e-9))
