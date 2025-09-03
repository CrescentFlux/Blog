import os
import glob
from datetime import datetime

def find_latest_blog_file():
    """寻找最新的Markdown文件"""
    # 使用更宽泛的搜索模式
    search_pattern = "./war/*.md"  # 递归搜索所有子目录的md文件
    md_files = glob.glob(search_pattern, recursive=True)
    
    print(f"🐛 DEBUG: 找到 {len(md_files)} 个md文件")
    for file in md_files:
        print(f"🐛 DEBUG: 找到文件: {file}")
    
    if not md_files:
        return "暂无博客文件", []
    
    # 找出最新的文件
    latest_file = max(md_files, key=os.path.getmtime)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_name = os.path.basename(latest_file).replace('.md', '')
    
    print(f"🐛 DEBUG: 最新文件是: {latest_file}")
    print(f"🐛 DEBUG: 修改时间: {mod_time}")
    print(f"🐛 DEBUG: 文件名: {file_name}")
    
    return f"{mod_time.strftime('%Y-%m-%d')}: {file_name}", md_files

# 测试一下
latest_blog, all_files = find_latest_blog_file()
print(f"最终结果: {latest_blog}")