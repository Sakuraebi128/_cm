import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

class GeometryEngine:
    @staticmethod
    def get_line_intersection(a1, b1, c1, a2, b2, c2):
        """計算兩直線 ax + by + c = 0 的交點 (克拉瑪公式)"""
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9: return None  # 平行或重合
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        return Point(x, y)

    @staticmethod
    def get_line_circle_intersections(a, b, c, cx, cy, r):
        """計算直線 ax + by + c = 0 與圓 (x-cx)^2 + (y-cy)^2 = r^2 的交點"""
        # 平移圓心至原點，調整 c 值
        c_prime = a * cx + b * cy + c
        dist_sq = c_prime**2 / (a**2 + b**2)
        
        if dist_sq > r**2 + 1e-9: return [] # 無交點
        
        # 垂足點 (x0, y0) 在平移後的座標系
        x0 = -a * c_prime / (a**2 + b**2)
        y0 = -b * c_prime / (a**2 + b**2)
        
        if abs(dist_sq - r**2) < 1e-9: # 切點
            return [Point(x0 + cx, y0 + cy)]
        
        # 弦長的一半
        d = math.sqrt(r**2 - dist_sq)
        mult = math.sqrt(d**2 / (a**2 + b**2))
        return [
            Point(x0 + b * mult + cx, y0 - a * mult + cy),
            Point(x0 - b * mult + cx, y0 + a * mult + cy)
        ]

    @staticmethod
    def get_circle_intersections(c1_x, c1_y, r1, c2_x, c2_y, r2):
        """計算兩圓交點：透過相減得到公弦方程式，再求線圓交點"""
        # 展開圓方程式並相減得到直線: Ax + By + C = 0
        A = -2 * c1_x + 2 * c2_x
        B = -2 * c1_y + 2 * c2_y
        C = c1_x**2 + c1_y**2 - r1**2 - (c2_x**2 + c2_y**2 - r2**2)
        return GeometryEngine.get_line_circle_intersections(A, B, C, c1_x, c1_y, r1)

    @staticmethod
    def get_foot_of_perpendicular(p, a, b, c):
        """從點 p 向直線 ax + by + c = 0 做垂線，回傳垂足"""
        k = (a * p.x + b * p.y + c) / (a**2 + b**2)
        return Point(p.x - a * k, p.y - b * k)

class Triangle:
    def __init__(self, p1, p2, p3):
        self.vertices = [p1, p2, p3]

    def apply_transform(self, matrix):
        """套用 3x3 變換矩陣"""
        new_vertices = []
        for p in self.vertices:
            # 齊次座標 [x, y, 1]
            x_new = matrix[0][0] * p.x + matrix[0][1] * p.y + matrix[0][2] * 1
            y_new = matrix[1][0] * p.x + matrix[1][1] * p.y + matrix[1][2] * 1
            new_vertices.append(Point(x_new, y_new))
        self.vertices = new_vertices

    def translate(self, dx, dy):
        m = [[1, 0, dx], [0, 1, dy], [0, 0, 1]]
        self.apply_transform(m)

    def scale(self, s):
        m = [[s, 0, 0], [0, s, 0], [0, 0, 1]]
        self.apply_transform(m)

    def rotate(self, angle_deg):
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        m = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
        self.apply_transform(m)

    def __repr__(self):
        return f"Triangle: {self.vertices}"

# --- 測試與驗證 ---

# 1. 驗證垂線與畢氏定理
p_out = Point(0, 5) # 線外一點
# 直線 L: x - y = 0 (即 a=1, b=-1, c=0)
foot = GeometryEngine.get_foot_of_perpendicular(p_out, 1, -1, 0)
p_on_line = Point(0, 0) # 直線上隨便取一點

dist_sq = lambda p1, p2: (p1.x - p2.x)**2 + (p1.y - p2.y)**2
a2 = dist_sq(p_out, foot)
b2 = dist_sq(p_on_line, foot)
c2 = dist_sq(p_out, p_on_line)

print(f"垂足為: {foot}")
print(f"畢氏定理驗證: a² + b² = {a2+b2:.2f}, c² = {c2:.2f}")

# 2. 三角形變換
tri = Triangle(Point(0,0), Point(1,0), Point(0,1))
print(f"\n原始三角形: {tri}")
tri.translate(2, 3)
tri.rotate(90)
print(f"平移(2,3)並旋轉90度後: {tri}")
