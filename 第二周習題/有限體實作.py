class FiniteFieldElement:
    def __init__(self, value, p):
        self.p = p
        self.value = value % p

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}(mod {self.p})"

    def __add__(self, other):
        return FiniteFieldElement(self.value + other.value, self.p)

    def __sub__(self, other):
        return FiniteFieldElement(self.value - other.value, self.p)

    def __mul__(self, other):
        return FiniteFieldElement(self.value * other.value, self.p)

    def __truediv__(self, other):
        # 使用費馬小定理求逆元：a^(p-2) % p
        return self * other.inverse()

    def __neg__(self):
        return FiniteFieldElement(-self.value, self.p)

    def inverse(self):
        if self.value == 0:
            raise ZeroDivisionError("0 has no multiplicative inverse")
        # pow(base, exp, mod) 效率最高
        return FiniteFieldElement(pow(self.value, self.p - 2, self.p), self.p)

    def __eq__(self, other):
        return self.value == other.value and self.p == other.p

# 符合 group_axioms.py 要求的群包裝類別
class FiniteFieldAddGroup:
    def __init__(self, p): self.p = p
    def op(self, a, b): return a + b
    def identity(self): return FiniteFieldElement(0, self.p)
    def inverse(self, a): return -a

class FiniteFieldMulGroup:
    def __init__(self, p): self.p = p
    def op(self, a, b): return a * b
    def identity(self): return FiniteFieldElement(1, self.p)
    def inverse(self, a): return a.inverse()
