import subprocess
import re

def get_git_log():
    try:
        result = subprocess.run([
            'git',
            'log',
            '--since="2025-08-20"',
            '--pretty=format:- %s (%ad)',
            '--date=short',
            '-n',
            '5'
        ], capture_output=True)

        
        return result.stdout.decode('utf-8')
    except UnicodeDecodeError:
        return result.stdout.decode('gbk', errors='ignore')

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_log = get_git_log()
pattern = r'<!--START_SECTION:latest_update-->.*<!--END_SECTION:latest_update-->'
replacement = f'<!--START_SECTION:latest_update-->\n{new_log}\n<!--END_SECTION:latest_update-->'
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)