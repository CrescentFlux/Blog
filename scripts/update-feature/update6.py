import os
import glob 
from datetime import datetime

def find_lastest_blog_file():
    md_files = glob.glob("content/**/*.md",recursive=True)

    if not md_files:
        return "暂无博客文件"
    
    latest_file = max(md_files, key=os.path.getmtime)

    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_name = os.path.basename(latest_file).repalce('.md','')

    return f"{mod_time.strftime('%Y-%m-%d')}:{file_name}"

latest_blog = find_lastest_blog_file()
print(f"最新博客：{latest_blog}")