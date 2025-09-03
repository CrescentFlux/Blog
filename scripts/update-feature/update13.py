import os
import glob
from datetime import datetime
import re

# 1. 获取最新博客（这部分已经工作）
def find_latest_blog_file():
    all_md_files = glob.glob("*.md")
    print(f"📁 找到 {len(all_md_files)} 个md文件")
    
    # 排除README.md和CHANGELOG.md
    blog_files = [f for f in all_md_files if f not in ['README.md', 'CHANGELOG.md']]
    print(f"📝 过滤后博客文件: {blog_files}")
    if not blog_files:
        return "暂无博客文件"
    
    latest_file = max(blog_files, key=os.path.getmtime)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_name = os.path.basename(latest_file).replace('.md', '')
    
   # result = f"{mod_time.strftime('%Y-%m-%d')}: {file_name}"
    result = f"📅[{mod_time.strftime('%Y-%m-%d')}: {file_name}](./{latest_file})"
    print(f"🎯 确定最新博客: {result}")
    return result

# 2. 更新README（添加详细调试）
def update_readme():
    print("🔄 开始更新README...")
    
    # 获取最新博客信息
    latest_blog = find_latest_blog_file()
    
    # 读取README内容
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ README读取成功")
    except Exception as e:
        print(f"❌ README读取失败: {e}")
        return
    
    # 检查是否存在标记
    pattern = r'<!--START_SECTION:latest_update-->.*<!--END_SECTION:latest_update-->'
    if not re.search(pattern, content, flags=re.DOTALL):
        print("❌ 在README中找不到更新标记！")
        print("请确保README中有以下内容:")
        print("<!--START_SECTION:latest_update-->")
        print("<!--END_SECTION:latest_update-->")
        return
    
    # 构建替换内容
    replacement = f'<!--START_SECTION:latest_update-->\n{latest_blog}\n<!--END_SECTION:latest_update-->'
    print(f"🛠️ 替换内容: {replacement}")
    
    # 执行替换
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 写回文件
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ README更新成功！")
    except Exception as e:
        print(f"❌ README写入失败: {e}")

# 运行更新
update_readme()