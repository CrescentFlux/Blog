1. **注意ACS和ASCII的区别**：
- ACS : using system-tools to slove 
```
win+r ->msconfig -> 系统配置 ->引导 ->引导选项 ->安全引导 ->最小->确定
重新启动之后，将SATA的模式从RST转变为AHCI(高级主机控制接口)
```

- 修改时选择sata operation  ==> (setup->storage interface存储接口)
按住上下箭头建来选中并且按回车键确认选择或者直接按住F10选择save configeration and exit yes

- bios不同模块的理解
```
device configeration:(硬件查询信息台)(port,model number,serial number,size,status,controller type,controller interface)
supportassist os recovery(恢复出场设置)
bios update(更新)
diagnositcs(硬件诊断中心)
bios setup(主板系统设置)

```

2. **克隆远程仓库的注意事项和步骤：**
```
ssh-keygen -t filename -C"your-email" ->
ssh -T git@github.com
git clone git@github.com:user-name/repositotiry-name
git config --global user.email"you-email.com"
git config --global user.name"your-name"
git add .
git commit -m
git push origin main

```

3. **文件安装注意事项**
- APPIMAGE 
```
#创建
1.创建一个存放appimage的固定文件比如applications,将现有的appimage移动过去；
2.创建桌面快捷方式(.desktop文件)
nano ~/.local/share/applications/appname.desktop
#文本编辑器编写对应文件

[Desktop Entry]
Version=1.0
Type=Application
Name=appname
Comment=appname - A powerful knowledge base
Exec=/home/adminname/Applications/appname.AppImage --no-sandbox
Icon=appname
Categories=Office;
Terminal=false
StartupWMClass=appname
注意CRTL+o保存文件 -> CRTL +x退出文件

3.赋予启动器文件执行权限
chmod +x ~/.local/share/application/appname.desktop
  
#卸载软件
1. 删除application对应文件
2. 删除配置文件(.config/,.cache/,.local/share)
```
- SNAP
```
sudo find <关键词>
sudo snap install <软件包名>
sudo snap install code --classic(不加参数时无法访问绝大多数系统文件)
snap list (查看已安装)
which appname 查看安装的软件是在哪个路径下
~/snap/appname 配置文件位置

卸载软件:
1. 确认它是如何安装的 which code
2.#如果路径显示为/usr/bin/code，表示他是从官方途径下载的deb包
sudo apt remove code//常用的清除命令
sudo apt purge code //彻底清除配置
sudo apt autoremove//最好运行一下自动清理
.config/删除配置文件
#如果路径显示为/usr/local/bin/code或者～/bin/code意味着从官网下载deb并且使用了dpkg来安装的
sudo apt remove code
dpkg --list | grep code
sudo apt purge<package-name>
3.删除配置文件.config
4.验证code命令是否存在


```

4. other tips
- using refus to install iso-file  path:https://refus.ie/zh/
- https://github.com/search or https:github.com/apppname/appname/releases to find app.deb(x64)




