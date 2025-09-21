1. cryptography
- 包含C语言扩展，需要系统级的编译工具和依赖库才能从源码编译
- import语句必须单独成行，不能和其他代码写在同一行,删除任何合并的import语句
- 安装系统依赖
```
# 1. 更新包列表
sudo apt update
# 2. 安装编译所需的依赖
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
# 3. 重新尝试安装 cryptography
pip install cryptography
```
2. 无法正确识别解决方案
```
- 检查pip安装的cryptography是否被python路径正确搜索
# 1. 检查当前Python环境
which python
# 输出应该是: /home/你的路径/venv/bin/python
# 2. 检查cryptography安装位置
pip show cryptography | grep Location
# 检查这个路径是否包含在你的Python路径中
# 3. 检查Python的搜索路径
python -c "import sys; print('\n'.join(sys.path))"
# 查看pip show的路径是否在列表中
# 4. 直接测试导入
python -c "import cryptography; print(' 直接测试成功')"

```
3. 检查vs是否使用你的虚拟环境
```
1.在项目根目录创建 .vscode/settings.json：
{
    "python.defaultInterpreterPath": "/home/crescentflux/桌面/name/venv/bin/python",
    "python.analysis.extraPaths": [
        "/home/crescentflux/桌面/name/venv/lib/python3.12/site-packages"
    ],
    "python.autoComplete.extraPaths": [
        "/home/crescentflux/桌面/name/venv/lib/python3.12/site-packages"
    ],
    "python.linting.enabled": true
}

2. 手动导入路径
venv_path = "/home/crescentflux/桌面/name/venv/lib/python3.12/site-packages"
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

3.重启VS Code的语言服务器
按 Ctrl+Shift+P
输入 Python: Restart Language Server
回车执行
```

4. 理解json文件（标准化表格）
- 用来存储结构化的数据，结构化的数据格式;
- JSON的优势：
```
结构化：像表格一样有明确的字段和值
可读性：人类和机器都能轻松理解
标准化：所有程序都知道怎么处理JSON
扩展性：很容易添加新字段
```
- 配置json;settings.json
```
地址簿 = [
    "/当前项目文件夹",      
    "/系统库路径",          
    "/虚拟环境库路径"       
]
执行命令 venv/bin/python
存放工具包 venv/lib/python3.12/site-packages
```
-  数据JSON;存储程序运行产生的数据
```{
    "conversations": [
        {"user": "你好", "user": "你好！", "time": "2025-09-21"},
    ],
    "user_preferences": {
        "language": "zh",
    }
}
```