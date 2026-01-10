def check_distributivity(a, b, c):
    # 驗證 a * (b + c) == a * b + a * c
    lhs = a * (b + c)
    rhs = (a * b) + (a * c)
    return lhs == rhs

def test_finite_field_axioms(p):
    print(f"--- 驗證有限體 GF({p}) ---")
    
    # 建立元素
    a = FiniteFieldElement(3, p)
    b = FiniteFieldElement(4, p)
    c = FiniteFieldElement(2, p)
    
    # 1. 驗證加法群特性
    add_group = FiniteFieldAddGroup(p)
    id_add = add_group.identity()
    print(f"加法單位元: {id_add}")
    print(f"加法逆元驗證 (a + (-a)): {a + (-a)} == {id_add}")
    
    # 2. 驗證乘法群特性 (非零元素)
    mul_group = FiniteFieldMulGroup(p)
    id_mul = mul_group.identity()
    print(f"乘法單位元: {id_mul}")
    print(f"乘法逆元驗證 (b * b^-1): {b * b.inverse()} == {id_mul}")
    
    # 3. 驗證運算子重載 (類似整數運算)
    res = (a + b) * c / b - a
    print(f"複合運算 (a+b)*c/b-a 結果: {res}")
    
    # 4. 驗證分配律
    is_dist = check_distributivity(a, b, c)
    print(f"分配律 a*(b+c) == a*b + a*c: {is_dist}")

if __name__ == "__main__":
    # 使用質數 7 作為例子
    test_finite_field_axioms(7)
