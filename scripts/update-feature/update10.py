import os
import glob
from datetime import datetime

# 自动获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print(f"🔒 已锁定工作目录: {os.getcwd()}")

# 剩下的代码保持不变...
def find_latest_blog_file():
    md_files = glob.glob("*.md")
    print(f"📁 找到 {len(md_files)} 个md文件:")
    for file in md_files:
        print(f"   - {file}")
    
    if not md_files:
        return "暂无博客文件"
    
    latest_file = max(md_files, key=os.path.getmtime)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_name = os.path.basename(latest_file).replace('.md', '')
    
    return f"{mod_time.strftime('%Y-%m-%d')}: {file_name}"

# 运行测试
latest = find_latest_blog_file()
print(f"🎯 最新博客: {latest}")