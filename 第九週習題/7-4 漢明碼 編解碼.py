def hamming_74_encode(data):
    # data: 4-bit list, e.g., [d1, d2, d3, d4]
    d1, d2, d3, d4 = data
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    # 編碼順序常用: [p1, p2, d1, p3, d2, d3, d4]
    return [p1, p2, d1, p3, d2, d3, d4]

def hamming_74_decode(received):
    # received: 7-bit list
    p1, p2, d1, p3, d2, d3, d4 = received
    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s3 = p3 ^ d2 ^ d3 ^ d4
    
    syndrome = s1 + (s2 << 1) + (s3 << 2)
    
    if syndrome != 0:
        print(f"偵測到錯誤！錯誤發生在位置: {syndrome}")
        # 修正對應位置的位元
        received[syndrome-1] ^= 1
        
    return [received[2], received[4], received[5], received[6]]

# 測試
msg = [1, 0, 1, 1]
encoded = hamming_74_encode(msg)
print(f"原始編碼: {encoded}")

# 模擬一個錯誤 (將第3個位元翻轉)
encoded[2] ^= 1 
print(f"傳輸後錯誤: {encoded}")

decoded = hamming_74_decode(encoded)
print(f"修正後結果: {decoded}")
