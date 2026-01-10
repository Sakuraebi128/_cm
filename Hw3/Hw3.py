import cmath

def root3(a, b, c, d):
    # 若 a = 0 代表不是三次方程式
    if a == 0:
        raise ValueError("a 不能為 0，否則不是三次方程式")

    # 改為標準形式 x^3 + px + q
    # 先做變數替換 x = y - b/(3a)
    p = (3*a*c - b*b) / (3*a*a)
    q = (2*b*b*b - 9*a*b*c + 27*a*a*d) / (27*a*a*a)

    # 判別式
    Δ = (q/2)**2 + (p/3)**3

    # Cardano formula
    u = (-q/2 + cmath.sqrt(Δ)) ** (1/3)
    v = (-q/2 - cmath.sqrt(Δ)) ** (1/3)

    # 三個根（複數皆可）
    y1 = u + v
    y2 = -(u + v)/2 + (u - v) * cmath.sqrt(3) * 1j / 2
    y3 = -(u + v)/2 - (u - v) * cmath.sqrt(3) * 1j / 2

    # 反代回 x = y - b/(3a)
    shift = b / (3*a)
    x1 = y1 - shift
    x2 = y2 - shift
    x3 = y3 - shift

    return (x1, x2, x3)


# 使用範例
if __name__ == "__main__":
    roots = root3(1, 0, 0, -1)  # x^3 - 1 = 0
    print("三個根：")
    for i, r in enumerate(roots, start=1):
        print(f"x{i} = {r}")
