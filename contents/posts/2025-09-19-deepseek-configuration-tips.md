# **SDK**
## 1. 基本操作
```
sudo apt install python3-pip
sudo apt install python3.12-venv
python3 -m venv venv
source venv/bin.activate
pip install deepseek-sdk --upgrade
pip list | grep deepseek
pip uninstall deepseek-sdk
pip cache purge
```
## 2. 排查方向和注意事项
```
1. 检查python路径
which python
echo "python路径:$(which python)"
ls -la 查找到的路径/直接查看文件内容

2.测试终端直接导入是否正常
python -c "from deepseek_sdk import DeepSeek;print(" 导入成功 ")"

3.直接查看下载的包
pip show deepseek-sdk
ls -la /查找路径之后的输出/venv/lib/python3.12/site-packages/deepseek_sdk/
ls -la /home/admin/桌面/projetsname/venv/lib/python3.12/site-packages/ | grep deep
ls -la /home/admin/桌面/projetsname/venv/lib/python3.12/site-packages/deepseek_sdk/__init__.py 
#查看是否只有dist-info目录，只有deepseek_sdk包目录，
#pip安装了包的元数据信息，但是没有安装实际的包文件导致python找不到模块
# 可能原因sdk是pypl是第三方开发的不完整的包

4.检查搜索路径
python -c "import sys;print('搜索路径：');[print(p) for p in sys.path]"
```
# **requests**
## 1. 基本操作
```
pip install requests
which python
pip list | grep requests
```
## 2. 测试终端工作是否正常
```
- 测试系统python
/usr/bin/python3 -c "import requests; print('✅ 系统Python的requests正常')"
使用单引号包裹字符串
python3 -c "import requests; print('测试requests')"
或者使用转义引号
python3 -c "import requests; print(\"测试requests\")"
- 测试虚拟环境python
./venv/bin/python -c "import requests; print('✅ 虚拟环境requests正常')"
```
## 3. vscode本身问题
- **终端测试成功但VS Code里报错，这是VS Code的配置问题**
### **3.1 重启VS Code并重新选择解释器**
```
1.VS Code没有使用你的虚拟环境VS Code还在用系统Python而不是你的虚拟环境Python
2.解决方法
完全关闭VS Code
重新打开项目
按 Ctrl+Shift+P
    输入 Python: Select Interpreter  --> 这里没有这个选项时no matching commands查看右下角的python有没有显示版本号
    选择 /venv/bin/python 路径
    使用VS Code的UI选择解释器
    点击VS Code右下角的Python版本号（如果有）
    或者点击状态栏的"选择Python解释器"
```
### **3.2 扩展问题**
- **检查扩展状态VS Code的Python扩展没有正确加载或激活**
```
 1. 重新加载VS Code窗口
    按 Ctrl+Shift+P
    输入 Developer: Reload Window
    回车执行
    2.检查Python扩展状态
    按 Ctrl+Shift+X 打开扩展面板
    找到Python扩展（Microsoft的）
    查看是否已启用，如果没有就启用
    # 检查已安装的扩展
    code --list-extensions | grep -i python

2. 看VS Code底部状态栏：
    如果看到 Python 3.x.x 或类似显示 → 扩展已启用
    如果什么都没有 → 扩展可能未启用或未激活

3. 检查Python扩展是否真的在工作：
    # 在VS Code终端中运行
    code --list-extensions | grep python

4. 检查pylance扩展状态检查;pylance语言服务器有没有使用正确的虚拟环境路径
   检查现有的扩展是否冲突，卸载不需要的扩展防止扩展之间依赖混乱
   pylance+python+python debugger
```
### **3.3 路径问题**
-  **手动创建强制配置文件**（无论扩展状态）
```
在项目根目录创建 .vscode/settings.json 文件
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.pythonPath": "./venv/bin/python",
    "python.analysis.extraPaths": [
        "./venv/lib/python3.12/site-packages"
    ]
}
```
-  **在vscode里设置直接手动编辑配置文件：用配置文件方法设置解释器路径**
```
    按 Ctrl+Shift+P
    输入 Preferences: Open Settings (JSON)
    在用户设置中添加：
json
{
    "python.defaultInterpreterPath": "/home/admin/your/path/venv/bin/python"
} 
```
-  **检查vscode是否正确读取配置文件**
```
    解决方法：
    ls -la .vscode/settings.json # 检查配置文件是否存在且路径正确
    cat .vscode/settings.json     # 检查文件内容
    ls -la .vscode/  # 检查文件权限（应该是644）
```
-  **VS Code是否真的读取了配置**
```
    在VS Code中：
    按 Ctrl+Shift+P
    输入 >Preferences: Open Settings (JSON)
    查看输出的是用户设置还是工作区设置
```
-  **在VS Code中直接设置**
```
    按 Ctrl+, 打开设置
    搜索 python default interpreter path
    手动输入：/home/crescentflux/桌面/npc-battle-game/venv/bin/python
```
-  **使用绝对路径导入（绕过配置）**
```
    在代码开头添加：
    import sys
    sys.path.append('/home/your-path/venv/lib/python3.12/site-packages')
    import requests
    print("✅ 强制导入成功")
```
### **3.4 检查包是否存在和实际使用的路径**
```
# 检查当前工作区路径
pwd
# 应该是: /home/admin/桌面/game
# 检查VS Code实际使用的Python路径
python -c "import sys; print('实际使用的Python:', sys.executable)"
# 检查requests包位置
python -c "import requests; print('requests路径:', requests.__file__)"
```

### **3.5 检查vs code的工作区缓存是否损坏**
```
# 关闭VS Code
pkill -f code
# 删除VS Code的工作区缓存
rm -rf ~/.config/Code/User/workspaceStorage/
# 重新打开项目
code /your/projects/path/
# 定期运行清理缓存
rm -rf ~/.config/Code/User/workspaceStorage/*
```