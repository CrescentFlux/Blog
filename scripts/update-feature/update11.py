import os
import glob
from datetime import datetime
import re

def find_latest_blog_file():
    all_md_files = glob.glob("**/*.md", recursive=True)
    
    # 定义一个模式来识别博客文件，例如文件名以日期开头
    # 模式可根据你的实际命名规则调整
    blog_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')  # 匹配"YYYY-MM-DD"开头的文件名
    
    blog_files = [f for f in all_md_files if blog_pattern.match(os.path.basename(f))]
    
    # ... (后续筛选最新文件的逻辑)
    if not blog_files:
        return "暂无博客文件"
    
    latest_file = max(blog_files, key=os.path.getmtime)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_name = os.path.basename(latest_file).replace('.md', '')
    
    return f"{mod_time.strftime('%Y-%m-%d')}: {file_name}"

# 运行测试
latest_blog = find_latest_blog_file()
print(f"最新博客: {latest_blog}")