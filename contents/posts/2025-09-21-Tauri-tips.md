1. 理解json文件（标准化表格）
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

2. 具体流程
```
# 安装Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
#进入项目目录
cd my-sticky-notes-app
#安装依赖
npm install
#启动开发
npm run tauri dev
-版本冲突问题
# 检查Rust版本
rustc --version
# 检查Cargo版本  
cargo --version
# 创建Tauri项目
npm create tauri-app my-sticky-notes-app
#更新前端 API 版本
npm install @tauri-apps/api@latest
#检查更新结果
npm list @tauri-apps/api

```

3. 配置过程
- 基本配置
```
// tauri.conf.json
"windows": [{
  "always_on_top": true,    // 始终置顶
  "decorations": false,     // 无标题栏
  "transparent": true,      // 透明背景
  "resizable": false,       // 固定大小
  "width": 300,
  "height": 200
}]
src/ - 前端代码（HTML/CSS/JS）
src-tauri/ - Rust 后端代码
index.html - 主页面文件
```
- 特点
```
系统托盘图标 - 最小化到托盘
全局快捷键 - 快速呼出便签
文件操作 - 自动保存到本地
多窗口 - 多个便签同时存在
```
- 功能扩展
```
# 编译成可执行文件
npm run tauri build
# 快捷方式
src-tauri/target/release/my-sticky-notes-app
# 创建自启动项
cp my-sticky-notes-app.desktop ~/.config/autostart/
```