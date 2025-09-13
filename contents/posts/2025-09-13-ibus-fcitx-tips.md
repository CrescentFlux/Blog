# IBUS在code中光标无法跟随问题解决方案
- **ibus程序会认为处理code这种预编辑文本是输入法自己的事，会自己创建一个独立的，悬浮的窗口来显示拼音和候选词**
- **修复ibus**
1. 修改添加参数ibus方式启动code的方式
```
code --disable-features=UseOzonePlatform --enable-features=WebRTCPipWireCapturer,使用X11框架适配ibus
```
2. 强制配置基本Ibus的输入法
```
sudo apt install ibus ibus-libpinyin --reinstall -y
im-config -n ibus
ibus restart
sudo apt update
sudo apt install -f -y
注销重新登查看问题是否解决

```
3. ibus其他注意事项

```
#Ibus下code无法接收中文数据的问题
1. # 在启动code的瞬间强制o适用所有必要的环境变量和IBUS输入法框架正确连接
env GTK_IM_MODULE=ibus QT_IM_MODULE=ibus XMODIFIERS=@im=ibus code
2. #永久修改启动环境变量
sudo nano /usr/share/applications/code.desktop
Exec=env GTK_IM_MOUDLE=ibus QT_IM_MOUDLE=ibus XMODIFIERS=@im=ibus /usr/share/code/code --unity-launch %F

#查找ibus的设置:
ibus-setup

#重启ibus守护进程
ibus-daemon

#环境变量配置
export GTK_IM_MOUDLE=ibus
export QT_IM_MOUDLE=ibus
export XMODIFIERS=@im=ibus

```

- **卸载选择fcitx5**
1. 检查目前系统运行的输入法并且卸载登出检查是否运行成功
```
#检查im配置
im-config -m
#检查进程
ps aux | grep ibus
#检查软件包状态
dpkg -l | grep -i ibus
#移除ibus的包
sudo apt remove --purge ibus  ->sudo apt autoremove --purge
#检查已安装的包
dpkg -l \*ibus\*
#检查进程
ps aux \| grep ibus

```
2. 卸载后系统输入法指向可能还是ibus,手动修正输入法配置为fctix5
```
#修改当前配置选择fctix5并且重启电脑，为框架增添中文输入法
im-config
```


# fctix5安装注意事项

- **理解不同的模块**
1. fctix5(核心框架) 
2. fctix5-chinese-addons(中文插件)
3. fctix5-frontend-gtk4/gtk3(对接GTK，GNOME桌面，GIMP,CODE(底层是ELectron))
4. fcitx5-frontend-qt5(对接QT,KDE桌面，office,virtualbox,etc)
5. fcitx5-module-kimpanel(follow，对接内部所有用户不依赖外部程序)
6. kcm-fcitx5和fcitx5-config-qt(图形化配置界面，控制面板，设置输入法，切换皮肤，调整快捷键)
7. fcitx5-frontend-kimpanel(对接KDE Plasma桌面深度整合,与桌面环境深度集成)
8. fcitx5-config-qt(通用，适合于任何桌面环境，GNOME,KDE,XFCE),需要作为一个应用程序启动
9. kcm-fcitx5(KDE控制面板，专用只适用与KDE Plasma桌面，只针对KDE桌面用户)，被集成在KDE桌面系统设置里

- **安装**
```
sudo apt install fcitx5-frontend-kimpanel 
sudo apt install fcitx5-frontend-gtk4 fcitx5-frontend-qt5
sudo apt install fcitx5-module-kimpanel
sudo apt install kcm-fcitx5

#安装正确的fcitx5和正确的中文支持
sudo apt install fcitx5 fcitx5-chinese-addons f
sudo apt install fcitx5-frontend-gtk4 fcitx-frontend-qt5
sudo apt install fcitx5-module-kimpanel
sudo apt install fcitx5-config-qt

```
- **检查配置**
1. 检查已安装的组件
```
dpkg -l | grep fcitx 登出
fcitx5 -r --replace
```
2. 打开配置界面
```
fcitx5-configtool
注意系统设置和配置的区别：系统设置体现用什么输入法；配置主要运行输入法怎么工作候选框切换
```

- **其他注意事项**
```
1. 基本移除命令
#直接重新配置
sudo apt install --reinstall fcitx5*
#系统自带软件包恢复
sudo apt install --reinstall fcitx5 fcitx5-chinese-addons
#移除当前版本fcitx5
sudo apt remove fcitx5 fcitx5-chinese-addons fcitx5-chineseaddons-bin

2. 软件源的问题
<1>.主仓库(Main Repositotry)`http://security.ubuntu.com/ubuntu`
<2>.镜像仓库(Mirror Repository)`http://mirrors.tuna.tsinghua.edu.cn/ubuntu`
<3>.PPA(Personal Package Archive)
#添加ppa仓库获取最新版本时没有release文件
sudo add-apt-repository ppa:fcitx-team/stable
sudo apt update //更新
#软件源问题出错解决
sudo add-apt-repository --remove ppa:fctix-team/stable
```

# 快速检测系统状态
- **理解层次化结构**
```
1. 内核层Linux Kernel
2. 显示与服务gdm3(登陆界面),Xorg/Wayland
3. 桌面环境gnome-shell,nautilus(文件)
4. 应用层面ibus,libreoffice,etc

```

- **检查桌面环境包是否存在**
 ```
 #检查ubuntu桌面元包是否已安装
 dpkg -l ubuntu-desktop(配置单)
 #检查gnome桌面核心组件是否已安装
 dpkg -l gnome-shell gnome-session gdm3(桌面环境和登陆界面)
 #检查图形管理器和关键库
 dpkg -l libibus-1.0.5 Xorg(显示与服务) lightdm(关键库)
  
 ii已安装
 un未安装
 rc已删除但配置没有清除

 ```
- **修复被删除的组件并且更新状态**
```
#更新软件列表
sudo apt update
#修复所有误删的依赖关系
sudo apt install -reinstall ubuntu-desktop
sudo apt install ubuntu-desktop
#修复依赖
sudo apt --fix-broken install
#gdm3被删除
sudo apt install gdm3
sudo apt install lightdm

#检测是否正常能够运行
dpkg -l ubuntu-desktop gnome-shell gdm3 xrog libibus-1.0-5
#确保遗留下来的不再被任何程序需要的的依赖包清理掉
sudo apt autoremove
sudo apt update 
```

- **模拟命令沙盘推演**
```
#模拟删除dry-run.如果执行删除会发生什么
sudo apt remove --simulate ibus*
#查询依赖，要删除的软件被谁需要
apt rdepends ibus
#删除前查看该包的详细信息
apt show ibus
```




