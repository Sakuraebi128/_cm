# 程式一：直接計算 (會因為數值太小而溢位成 0.0)
p = 0.5
n = 10000
prob = p ** n
print(f"直接計算 0.5^10000 的機率為: {prob}")

# 程式二：使用對數計算 log(p^n) = n * log(p)
import math

log_prob = n * math.log10(p)
print(f"log10(0.5^10000) = {log_prob:.2f}")
print(f"這意味著機率約為 10^{log_prob:.2f}")
