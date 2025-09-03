import os
import glob
from datetime import datetime

# 强制指定正确的工作目录
#correct_path = "/d/war"  # 你的项目绝对路径
correct_path = "D: \\war" 
os.chdir(correct_path)   # 强制切换到正确路径

print(f"🔒 已锁定工作目录: {os.getcwd()}")

def find_latest_blog_file():
    """寻找最新的Markdown文件"""
    # 方法1：直接指定当前目录
    md_files = glob.glob("*.md")  # 只在当前目录查找
    
    # 如果找不到，尝试递归查找
    if not md_files:
        md_files = glob.glob("**/*.md", recursive=True)
    
    print(f"📁 找到 {len(md_files)} 个md文件:")
    for file in md_files:
        full_path = os.path.abspath(file)
        print(f"   - {file} (完整路径: {full_path})")
    
    if not md_files:
        return "暂无博客文件"
    
    # 找出最新的文件
    latest_file = max(md_files, key=os.path.getmtime)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_name = os.path.basename(latest_file).replace('.md', '')
    
    return f"{mod_time.strftime('%Y-%m-%d')}: {file_name}"

# 运行测试
latest = find_latest_blog_file()
print(f"🎯 最新博客: {latest}")

# 调试：显示当前目录所有文件
print("\n📋 当前目录所有文件:")
for item in os.listdir('.'):
    item_path = os.path.join(os.getcwd(), item)
    if os.path.isfile(item_path):
        print(f"   - {item} (文件)")
    else:
        print(f"   - {item}/ (文件夹)")