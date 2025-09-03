import subprocess
import re

def get_git_log():
    try:
        print("🐛 DEBUG: 开始执行 get_git_log()")
        result = subprocess.run([
            'git',
            'log',
            '--since="2025-08-20"',
            '--pretty=format:- %s (%ad)',
            '--date=short',
            '-n',
            '5'
        ], capture_output=True)
        
        print(f"🐛 DEBUG: git命令返回码: {result.returncode}")
        print(f"🐛 DEBUG: 原始输出: {repr(result.stdout)}")
        
        decoded_output = result.stdout.decode('utf-8')
        print(f"🐛 DEBUG: 解码后输出: {repr(decoded_output)}")
        
        return decoded_output
        
    except UnicodeDecodeError:
        print("🐛 DEBUG: 遇到编码错误，尝试GBK解码")
        return result.stdout.decode('gbk', errors='ignore')
    except Exception as e:
        print(f"🐛 DEBUG: 发生未知错误: {e}")
        return ""

print("🐛 DEBUG: 脚本开始执行")
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
print(f"🐛 DEBUG: 读取README内容，长度: {len(content)} 字符")

new_log = get_git_log()
print(f"🐛 DEBUG: 获取到的git日志: {repr(new_log)}")

pattern = r'<!--START_SECTION:latest_update-->.*<!--END_SECTION:latest_update-->'
print(f"🐛 DEBUG: 使用的正则模式: {pattern}")

replacement = f'<!--START_SECTION:latest_update-->\n{new_log}\n<!--END_SECTION:latest_update-->'
print(f"🐛 DEBUG: 准备替换的内容: {repr(replacement)}")

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
print(f"🐛 DEBUG: 替换后内容长度: {len(new_content)} 字符")

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("🐛 DEBUG: 文件写入完成！")

print("🐛 DEBUG: 脚本执行结束")