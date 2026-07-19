def read_large_file(file_path: str):
    """逐行读取文件，每次 yield 一行，不一次性加载全部内容到内存"""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()  
# 先创建一个测试文件
with open("sample.log", "w", encoding="utf-8") as f:
    f.write("line1: info\nline2: warning\nline3: error\n")

# 使用生成器逐行读取
if __name__ == "__main__":
    for line in read_large_file("sample.log"):
        print(f"处理行: {line}")

# 列表推导式（立即生成全部数据）
squares_list = [x*x for x in range(10_000_000)]  # 可能耗尽内存

# 生成器表达式（惰性）
squares_gen = (x*x for x in range(10_000_000))   # 几乎不占内存
print(next(squares_gen))  # 0
print(next(squares_gen))  # 1