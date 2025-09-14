## 理解snap
- **获取最新版本**
- **工作机制核心理解**
1. 接口是snap包获取特定权限的系统通道,snag接口必须同时存在于plug和slot端
2. 理解系统中不同的接口(snap interface)
```
1. 硬件访问类：控制对物理设备的访问
camera:摄像头
joystick:游戏手柄
opengl:显卡用于图形加速
u2f-devices:U2F/WebAuthn安全密钥
hardware-observe:读取硬件信息
2. 文件系统访问类：控制对磁盘文件的读写
home:访问用户家目录
personal-files:访问特定个人文件或者目录
removable-media:访问u盘，移动硬盘等可移动存储
system-files:访问系统文件
content:与其他snap共享只读数据
3. 网络相关类
network基本的网络访问
network-bind:绑定端口
avahi-observe:在局域网内发现和被发现
4.桌面集成类
desktop，desktop-launch，unity7，x11，wayland显示图形界面，启动其他程序，与桌面shell交互有关
secreen-inhibit-control：阻止系统休眠或者锁屏
browser-support：允许使用现代浏览器的某些功能
5. 系统控制与监控类
cups-control：控制打印
fwupd固件更新
login-session-observe：查看谁登陆了
mount-observe（只读权限）：mount-control（读写和控制权限），查看控制和磁盘挂载
shundown：关机和重启
upower-observe：读取电池状态
snapd-control：与snaped守护进程通信，管理其他snap
6.特权与后台服务类
packagekit-control：控制软件包更新
snap-refresh-observe：查看snap更新状态

```
- **基本命令**
1. 检查
```
1. 列出自动连接的核心接口
snap info appname
2. 检查app的清单文件
snap list appname
cat /snap/appname/current/meta/snap.yaml | grep plugs
3. 检查系统上可用的输入法接口
snap interface | grep -i ibus
snap interface | grep -i fcitx
4. 列出包含这些关键词的snap包,确认安装模式
snap list | grep -E '(obsidian|vscode|code)'
5.某个应用当前连接的所有接口
snap connections obsidian
snap info obsidian | grep -A 10 "plugs:"
6.查看已安装的snap应用
snap list
7.查看某个接口的详细信息
snap interface fcitx
8.查看某个应用的所有接口
snap connections obsdian |grep fcitx
snap connections code | grep fcitx
#手动启动输入法命令
fcitx5 -d
#检查输入法配置
fcitx5-configtool
#检查已经安装的相关的输入法
apt list --installed | grep fcitx
9.查看他们声明的接口
snap info 应用名 | grep -A 20 "plugs:"
10. 查看在snap 环境下的环境变量
snap run --shell 应用名 env | grep -i fcitx
# 查看当前终端环境下的环境变量
env | grep -E '(GTK_IM_MODULE|QT_IM_MODULE|XMODIFIERS)
11. 查看snap的运行信息
snap run --strace 应用名 | head -20
12. 查看snap的confinement的详细状态
snap get 应用名 confinement
13. 查看正在运行的snap 
snap services
```
2. 连接
```
#连接接口
sudo snap connect [应用名]:[接口名] =>重启
# 安装
snap install 软件名
```
3. 验证是否连接成功
```
snap connections | grep -E '(obsidian|code)' | grep ibus
```


- **通过脚本文件修改传递正确的环境变量**
```
cat > ~/启动应用名.sh << 'EOF'

export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
exec /snap/bin/应用名 "$@"

EOF
chomd +x ~/启动应用名.sh

~/启动应用名.sh
```

- **obsdian中配置中文输入法的方式**
```
1. 直接编写脚本
echo '#!/bin/bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
/snap/bin/obsidian' > ~/启动obsdian.sh

chmod +x ~/启动obsidan.sh

2. 使用nano修改环境变量
nano ~/.profile
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export SDL_IM_MODULE=fcitx

crtl+x enter// 保存文件退出
source ~/.profile//重新加载配置
env | grep -i fcitx//验证结果
```

- **snap特性**
1. 进阶检查命令
```
#snap安全隔离机制
1. 直接检查二进制文件
ls -la /usr/bin/env
file /usr/bin/env
ldd /usr/bin/env
- 在snap环境中检查
snap run --shell 应用名称
which env
file /usr/bin/env
exit

2.检测env
snap run --shell code  // snap run --shell code env
which env
file /usr/bin/env
- 系统env
which env
file /usr/bin/env
- 检查snap内部环境变量
snap run --shell code 
echo $PATH
echo $LD_LIBRARY_PATH
env | grep SNAP
exit

3.检查snap的可执行文件
ls -la /snap/code/current
ls -la /snap/ob/current
这里注意electron-launch 专用和command.sh通用的区别

4.检查元数据
cat /snap/code/current/meta/snap.yaml | grep -A 10 "apps:"
cat /snap/ob/current/meta/snap.yaml | grep -A 10 "apps:"
- 直接进入snap的shell环境手动检查
snap run --shell code
env | grep -i fcitx
exit

5.检查架构兼容性
- 检查系统架构
uname -m
- 检查snap架构
snap list --all code
snap list --all 应用名称

6.检查snap配置
- 检查snap运行时的配置
sudo cat /var/lib/snapd/seed/snaps/
ls /var/lib/snapd/snaps
- 检查snap的安全配置
sudo cat /var/lib/snapd/apparmor/profiles/snap.code.*
sudo cat /var/lib/snapd/apparmor/profiles/snap.ob.*
- 使用 stace追踪系统调用
strace -f -e trace=execve snap run code 2>&1 | grep -i fcitx
- 查看环境变量传递
strace -f -e trace=execve,clone snap run code 2>&1 | head -50

7.检查snap本身的状态
- 检查服务状态
sudo systemctl status snapd
- 检查snap日志
sudo journactl -u snapd -f
- 尝试修复
sudo snap repair
sudo systemctl restart snapd
- 检查磁盘空间和inode
df -h
df -i

8.检查snap环境完整性
- 检查核心snap是否正常
snap list |grep -E '(core|snapd)'
- 重新安装核心组件
sudo snap install core --dangerous --classic
- 检查已安装的snap
snap list --all
- 检查 snap版本兼容性
snap debug connectivity
- 检查详细的错误信息
strace -f -e trace=file snap run --shell code ls 2>&1 | head -50

9.重置snap环境
- 完全重置snap环境
sudo systemctl stop snapd
sudo rm -rf /var/lib/snapd/*
sudo apt purge snapd
sudp apt install snapd
- 重新安装应用
sudo snap install 应用名 --classic
- 检查是否修复
snap run --shell code env | head -5

10. 完全重建snap
- 备份已安装的snap列表
snap list > ~/snap-backup.txt
- 完全清除并重装snapd
sudo systemctl stop snapd
sudo apt purge snapd
sudp rm -rf /var/lib/snapd/snap/home/*/snap
sudo apt updates
sudo apt install snapd
- 重启系统
sudo reboot
- 重新安装应用
sudo snap install 应用名 --classic
- 测试是否正常运行
# 直接测试核心
/snap/snapd/current/usr/lib/snapd/snap-confine --version
# 最基础的方式运行
sudo /usr/lib/snapd/snap-confine snap.code.code /usr/bin/env --version
snap run --shell code env | head -5
```

2. 双重安全机制
- **AppArmor安全策略enforcement**
1. enforce模式，违规阻止
2. complain模式，违规放行
- **Seccomp BPF过滤器**
- **动态链接器重定向**
```
# 不包含完整的动态链接器环境
- 检查动态链接器
sudo find /snap/code/206 -name "ld*" -type f  //ld负责加载程序
# 不包含bash,env,ls
- 检查snap内部文件系统视图
sudo ls -la /snap/code/206
sudo ls -la /snap/code/206/usr/bin/
- 尝试调用snap内部的工具
/snap/code/206/usr/bin/bash -c "echo '测试内部shell '"
- 检查 snap的挂载命名空间
snap run --strace-code ls / 2>&1 |head -20

```
- 查看安全规则
```
1. 查看AppArmor策略
sudo aa-status | grep -i snap
sudo cat /var/lib/snapd/apparmor/profiles/snap.code. *2>/dev/null

2.查看seccomp过滤器
sudo snap debug seccomp |grep -A 10 -B 10 "env"
sudo cat /proc/self/status | grep -i seccomp

3.查看snap的完整调试信息
sudo snap debug sandbox-features
sudo demsg | grep -i seccomp | tail -10

4.查看详细的系统调用阻塞,捕获错误
strace -f -e trace=execve snap run --shell code env 2>&1 |head -20\
strace -f -e trace=execve,seccomp snap run --shell code env 2>&1 |head -30

5.检查现有的沙箱功能
sudo snap debug snadbox-features
sudo snap debug lsm

6.直接调试snap confinement
- 手动运行snap-confine调试
sudo  /usr/lib/snapd/snap-confine --debug snap.code.code /usr/bin/env --version
- 检查snap的运行环境
sudo /usr/lib/snapd/snap-exec --shell snap.code.code env
- 检查snap的安全上下文
ps aux | grep snap
sudo aa-status |grep code
-检查snap的 cgroup限制
cat /proc/$(pgrep -f "snap.code.code")/cgroup

7. 检查所有的snap安全配置
- 启用snap调试日志
sudo systemctl stop snapd
sudo /usr/lib/snapd/snapd -debug 2>&1 | tee /tmp/snapd-debug.log
- 检查所有的snap安全配置
sudo apparmor_parser -r /var/lib/snapd/apparmor/profiles/*
- 检查snap数据库完整性
sudo sqlite3 /var/lib/snapd/state.json "SELECT * FROM snaps"

```
- 重置安全策略
```
1. 强制重置
sudo apparmor_parser -R /var/lib/snapd/apparmor/profiles/snap.code.*
2. 重新加载策略
sudo systemctl reload apparmor
3. 测试修复
snap run --shell code env | head -5
4. 临时禁用所有安全设置
sudo systemctl stop apparmor
sudo swapoff -a
4. 恢复安全设置
sudo systemctl start apparor
```








## --classic模式
- snap 包可以不受严格的沙盒限制相当于有可能的权限，interface表示真正拥有的权限
- 绕过接口权限检查直接使用系统环境


## deb模式
- 安装注意事项
- 系统核心工具
```
#安装
sudo dpkg -i 软件名
sudo apt-get install -f #修复依赖
```

## 从仓库安装
```
通过apt安装
sudo apt update
sudo apt install fcitx5 etc
```

## Appimage
- 注意添加权限
- 临时使用
```
chmod +x 软件名.AppImage
./软件名称.appimage

```