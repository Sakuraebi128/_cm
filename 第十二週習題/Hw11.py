import numpy as np
from collections import Counter

def solve_ode_general(coefficients):
    # 1. 求解特徵方程的根
    roots = np.roots(coefficients)
    
    # 2. 處理數值誤差：將極小的虛部或實部歸零，並進行四捨五入以便統計重根
    clean_roots = []
    for r in roots:
        real = round(r.real, 10)
        imag = round(r.imag, 10)
        # 如果虛部極小，視為實根
        if abs(imag) < 1e-9:
            clean_roots.append(complex(real, 0))
        else:
            clean_roots.append(complex(real, imag))
            
    # 3. 統計根的重數
    # 複數根必須成對處理，我們只取虛部 > 0 的部分來生成 cos/sin
    root_counts = Counter(clean_roots)
    
    solutions = []
    processed_roots = set()
    term_count = 1

    for r, m in root_counts.items():
        if r in processed_roots:
            continue
            
        real_part = r.real
        imag_part = r.imag

        if abs(imag_part) < 1e-10:
            # 情況 A: 實根 (包括重根)
            # y = C*e^(rx), C*x*e^(rx), ..., C*x^(m-1)*e^(rx)
            for i in range(m):
                x_pow = f"x^{i}" if i > 1 else ("x" if i == 1 else "")
                solutions.append(f"C_{term_count}{x_pow}e^({real_part}x)")
                term_count += 1
            processed_roots.add(r)
        else:
            # 情況 B: 複數根 (alpha +/- beta*i)
            # 找到對應的共軛根
            conj_r = complex(real_part, -imag_part)
            processed_roots.add(r)
            processed_roots.add(conj_r)
            
            # 複數根的重數通常成對出現
            for i in range(m):
                x_pow = f"x^{i}" if i > 1 else ("x" if i == 1 else "")
                exp_part = f"e^({real_part}x)" if abs(real_part) > 1e-10 else ""
                
                # 生成 cos 項
                solutions.append(f"C_{term_count}{x_pow}{exp_part}cos({abs(imag_part)}x)")
                term_count += 1
                # 生成 sin 項
                solutions.append(f"C_{term_count}{x_pow}{exp_part}sin({abs(imag_part)}x)")
                term_count += 1

    return "y(x) = " + " + ".join(solutions)

# --- 測試主程式 ---
if __name__ == "__main__":
    # 測試案例比照您的需求
    test_cases = [
        ("實數單根", [1, -3, 2]),
        ("實數重根", [1, -4, 4]),
        ("複數共軛根", [1, 0, 4]),
        ("複數重根", [1, 0, 2, 0, 1]),
        ("高階重根", [1, -6, 12, -8])
    ]

    for title, coeffs in test_cases:
        print(f"\n--- {title}範例 ---")
        print(f"方程係數: {coeffs}")
        print(solve_ode_general(coeffs))
