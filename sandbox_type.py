from typing import List,Optional
def process_items(names:List[str],limit:Optional[int]=None)->List[str]:
    """截取名字列表，如果limit不为None，则返回前limit个名字，否则返回所有名字"""
    if limit is not None:
        return names[:limit]
    return names
# print(process_items(["alice", "bob", "charlie"], 2))
# result: int = process_items(["x", "y"], 1)   类型错误测试
# result: list[str] = process_items(["x", "y"], 1)  正确
