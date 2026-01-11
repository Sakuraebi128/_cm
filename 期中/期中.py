import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

# === 1. 物理參數設定 ===
G = 9.8      # 重力加速度 (m/s^2)
L1 = 1.0     # 第一根擺桿長度 (m)
L2 = 1.0     # 第二根擺桿長度 (m)
M1 = 1.0     # 第一個擺錘質量 (kg)
M2 = 1.0     # 第二個擺錘質量 (kg)

# === 2. 定義微分方程 (雙擺運動公式) ===
def der_state(state, t):
    th1, w1, th2, w2 = state
    
    delta = th2 - th1
    
    # 這裡是最核心的物理公式：加速度推導
    den1 = (M1 + M2) * L1 - M2 * L1 * np.cos(delta) * np.cos(delta)
    dth1 = w1
    dw1 = (M2 * L1 * w1**2 * np.sin(delta) * np.cos(delta) +
           M2 * G * np.sin(th2) * np.cos(delta) +
           M2 * L2 * w2**2 * np.sin(delta) -
           (M1 + M2) * G * np.sin(th1)) / den1

    den2 = (L2 / L1) * den1
    dth2 = w2
    dw2 = (-M2 * L2 * w2**2 * np.sin(delta) * np.cos(delta) +
           (M1 + M2) * G * np.sin(th1) * np.cos(delta) -
           (M1 + M2) * L1 * w1**2 * np.sin(delta) -
           (M1 + M2) * G * np.sin(th2)) / den2
    
    return [dth1, dw1, dth2, dw2]

# === 3. 設定初始狀態與時間軸 ===
# 初始角度 (弧度): 120度與-10度，初速度皆為 0
initial_state = [np.radians(120), 0, np.radians(-10), 0]
t = np.linspace(0, 40, 1000)  # 模擬 40 秒，共 1000 個採樣點

# 求解 ODE
y = odeint(der_state, initial_state, t)

# 將角度轉換為直角座標 (x, y)
x1 = L1 * np.sin(y[:, 0])
y1 = -L1 * np.cos(y[:, 0])
x2 = x1 + L2 * np.sin(y[:, 2])
y2 = y1 - L2 * np.cos(y[:, 2])

# === 4. 建立動畫視窗 ===
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2, color='#1f77b4') # 擺桿與擺錘
trace, = ax.plot([], [], '-', lw=1, color='#ff7f0e', alpha=0.5) # 軌跡
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line.set_data([], [])
    trace.set_data([], [])
    time_text.set_text('')
    return line, trace, time_text

def animate(i):
    # 更新擺桿位置
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data(thisx, thisy)
    
    # 更新軌跡位置 (顯示前 100 步的軌跡)
    start = max(0, i-100)
    trace.set_data(x2[start:i], y2[start:i])
    
    time_text.set_text(time_template % (i*t[1]))
    return line, trace, time_text

ani = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=True, init_func=init)

plt.show()
