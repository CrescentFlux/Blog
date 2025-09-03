import subprocess
import re
#import os
def get_git_log():
   # env = os.environ.copy
   # env['LC_ALL'] = 'C.UTF-8'

    result = subprocess.run([
         'git',
         'log',
        # '--oneline',
         '--since="2025-08-20",'
         '--pretty=format :"-  %s (%ad)',
         '--date=short',
         '-n',
       #  '5'],capture_output=True,text=True,encoding='utf-8')
         '5'],capture_output=True) 
                     
   # print("===DEBUG INFO ===")
  #  print("Return code :",result.returncode)
   # print("Stdout:",repr(result.stdout))
   # print("Stderr:",repr(result.stderr))
   # print("=================")

    print("DEBUG - RAW git output:")
    print(repr(result.stdout))

    decode_output = result.stdout.decode('utf-8')

    print("DEBUG - Decoded output:",repr(decode_output))
    return decode_output

with open('README.md','r',encoding='utf-8')as f :
     content = f.read()

new_log = get_git_log()
pattern = r'<!--START_SECTION:latest_update-->.*<!--END_SECTION:latest_update-->'
repalcement = f'<!--START_SECTION:latest_update-->\n{new_log}\n<!--END_SECTION:latest_update-->'
new_content = re.sub(pattern,repalcement,content,flags=re.DOTALL)


with open('README.md','w',encoding='utf-8')as f:
      f.write(new_content)