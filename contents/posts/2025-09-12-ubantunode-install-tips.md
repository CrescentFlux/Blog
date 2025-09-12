# UBANTU安装node注意事项
- 使用node version manager ：专门管理和切换多个nodejs的管理工具
```
1.安装操作
#安装curl
sudo apt update
sudo apt install curl
curl version
#安装nvm(.nvm/)官方脚本install.sh将下载的内容通过管道传递给bash来运行
curl -o- https://raw.githubusercontent.com/nvm/v0.39.7/install.sh |bash
#关闭终端或者运行，安装脚本会将初始代码添加到./bashrc中
source ~/.bashrc
nvm --version
#安装nodejs-最新的LTS长期支持版本
nvm install --lts
#安装某个特定版本
nvm install 18
#查看已经安装的版本
nvm ls
#切换某个使用版本
nvm use 18
```
2.执行层
注意要在具体的某个项目目录下进入目录然后使用nvm来安装nodejs版本；位置在项目目录下的node_modules/



# python 环境安装注意事项
- 为每一个新项目使用python3 -m venv 创建虚拟环境，并在激活环境之后在安装包
- 一个项目，一个虚拟环境
```
1.进入项目目录
cd ~/文档/my-python-project
2.创建虚拟环境
python3 -m venv venv
3.激活虚拟环境
source venv/bin/activate
4.推出虚拟环境
(venv)deativate

```

# 解决code中文输入黄色文本框包裹干扰视野的问题
- 理解settings大概设置

1. Text Editor(文本编辑器)
```
Cursor光标：设置光标的样式闪烁频率是否平滑移动
Find查找替换：是否大小敏感，是否高亮所有结果
Font字体：设置代码的字体，字号，行高
Formatting格式化：设置代码自动排版的规则比如缩进用空格还是tab
Minimap缩略图：控制所在中文
Suggestions:智能语音助手：控制代码自动不全弹窗的出现时机，排序方式；
```
2. workbench工作台
```
appearance切换整个软件的颜色主题，图标主题
breadcrumbs：路径导航，控制编辑器顶部那个显示文件路径的导航条
editor management：编辑器管理，控制标签页的行为，比如是否预览模式，怎么分组排列
settings editor：设置编辑器
zen mode：一键开启极致专注模式只有代码
screencast mode:屏幕广播模式，开启后屏幕上会显示按下的快捷键，适合录制作教程
```
3. features
```
explorer资源管理器：控制左侧文件管理书的行为，比日是否显示隐藏文件，怎么排序
search控制全项目的搜索的功能，比如是否忽略某些文件夹，是否区分大小写
debug：核心开发功能，控制如何调试代码
testing：控制代码测试框架的运行和显示方式
source control：源代码控制，控制git的集成，比如显示文件变更，提交代码
terminal：控制内置终端行为字体，配色
tasks：配置自定义的自动化脚本
problems：控制如何显示代码错误和警告
output输出：控制各种插件的工具输出日志的窗口
accessibiility singals辅助功能
```
4. applications
```
proxy：设置代理服务器
keyboard查看和修改所有键盘快捷键的映射关系
update：更新code的操作
telemetry遥测：选择是否向微软发送匿名数据
settings sync设置同步：微软或者github账号登陆，所有的设置插件，快捷键同步到任何电脑上
```
5. extensions 插件:一些内置或者添加的扩展

- 黄色文本框包裹问题属于 Text Editor，署名Indication UI
```
1. 它的作用是直观的告诉你现在正在输入的字符和编辑器默认的编码比如UTF-8下的字符看起来有什么不同；当输入中文时它会占用多个字符；
2. 这个黄色的框就把多个字节组合成一个字符，作为一个整体框起来了，视觉上指示这是一个扩展字符；
3. 它属于VS正常功能，用于视觉化显示非ASCII字符的字节范围；
```

- 解决方法
```
1. 打开命令面板crtl+shift+p
2. 输入命令>Preferences:Open User Settings (JSON)回车
3. 编辑配置文件settings.json

{//关闭所有类型的UNICODE高亮
    "editor.unicodeHighlight,ambiguousCharacters:false,
    "editor.unicodeHighlight.invisableCharacters:false,
    "editor.unicodeHighlight.nonBasicASCII:false,
    "editor.unicodeHighlight.includeComments:false,
    "editor.unicodeHighlight.includeStrings:false,
}
```






