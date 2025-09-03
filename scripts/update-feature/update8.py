import os
import glob

# 打印当前工作目录
print(f"🕵️ 侦探当前位置: {os.getcwd()}")

# 打印当前目录下的所有内容
print("📁 当前目录内容:")
for item in os.listdir('.'):
    print(f"  - {item}")

# 尝试不同的搜索模式
patterns = [
   # "*.md",           # 当前目录
   # "./*.md",         # 当前目录（明确写法） 
    #"**/*.md",        # 递归搜索所有子目录
    "../*.md",        # 上级目录
]

for pattern in patterns:
    files = glob.glob(pattern, recursive=True)
    print(f"🔍 搜索模式 '{pattern}': 找到 {len(files)} 个文件")
    for file in files:
        print(f"    - {file}")