

class ManagedFile:
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"🔓打开文件: {self.filename} (模式: {self.mode})")
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file   # 返回的文件对象会赋值给 `as` 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"已关闭文件: {self.filename}")
        # 如果发生了异常，exc_type 不为 None，可以在这里决定是否吞掉异常
        # 这里选择不吞，让异常继续传播
        if exc_type:
            print(f"发生异常: {exc_type.__name__}: {exc_val}")
        return False   # False 表示不抑制异常，True 表示吞掉异常
    
if __name__ == "__main__":
    # 正常写入
    with ManagedFile("test_context.txt", "w") as f:
        f.write("Hello from custom context manager!\n")
        f.write("Second line.")
    
    print("=" * 30)

    # 读取
    with ManagedFile("test_context.txt", "r") as f:
        content = f.read()
        print(f"读取内容:\n{content}")
    
    print("=" * 30)

    # 故意触发异常，验证 __exit__ 仍会执行
    try:
        with ManagedFile("test_context.txt", "r") as f:
            data = f.read()
            raise ValueError("手动触发异常")
    except ValueError:
        print("异常被外部捕获，文件已正常关闭")