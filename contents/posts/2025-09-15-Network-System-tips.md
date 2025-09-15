# 理解网络
1. **网络依赖关系 network-manager 属于系统功能层**
- DNS解析-软件源-清理缓存重新连接逻辑的前提是manger正常
- **网络配置**
```
1.检查网卡(有线网卡，无线网卡)和设备状态（是否正确获取IP地址）
ip addr show  / ifconfig
- 手动启动网卡
sudo ip link set wp-name up

2. 连接网络
sudo dhclient
- 安装无线工具
sudo apt install wireless-tools iw

3.连接wifi
- 查看可用的设备
sudo iw dev
- 扫描附近的网络
sudo iwlist wlan0 scan | grep ESSID
- 使用wpa_supplicant连接wifi(这是一次性连接命令)
sudo wpa_supplicant -B -i wlan0 -c <(wpa_passphrase "yourwifi-name" "password")>
- 用钥匙连接网络
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant.conf -B
- 检查wifi连接状态
sudo iw dev wlan0 link

4.设置ip地址和门牌号
- 获取ip地址
sudo dhclient wlan0
ip neigh show
- 如果获取失败尝试设置静态ip地址
sudo ip addr add 路由器地址 dev 无线网卡名称
sudo ip addr add 111.123.123.100/25 dev 网卡名称

5. 设置网关中转站
- sudo ip route add default via 路由器ip地址
sudo ip route add default via 111.123.1.1

6.设置dns智能导航仪,负责把网络上的域名翻译解析成IP地址
- 手动添加一个众所周知的可靠的DNS地址写入系统的DNS配置文件
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf

7.测试结果
- 测试网络连接
ping -c 1.11.1.1
- 尝试连接
sudo iwconfig wpname essid "your-wifi" "password"
- 测试网络恢复
nslookup baidu.com
ping -c baidu.com

8.诊断修复工具
- 安装网络诊断工具
sudo apt install curl wget net-tools//用curl测试网络是否真的连接通
- 检查网络驱动
lspci | grep -i network
lsmod | grep -i wifi
- 重启网络服务
sudo service network-manager restart
```


# 系统层

## **硬件层Network Manager**
1. 无线/有线网卡-物理网络设备
2. 声卡
3. 显卡-图形显示
4. 存储设备
5. USB控制器-外设连接

## **硬件信息提供层**
1. lspci 查看pci设备信息
2. lsusb 查看usb设备信息
3. udev 设备管理服务创建设备文件
4. /proc/ 内核提供的设备信息接口
5. /sys/ 系统设备信息文件系统

## **GUI**
- **系统不依赖GUI运行**
- **横跨多个层级**
1. 显示硬件层
-  物理设备
2. 图形核心层
- 显卡驱动
- DRM/KMS直接渲染管理器
- OpenGL/Vulkan图形API
- Wayland/X11显示服务器协议核心
3. 图形服务层
- Xrog/Wayland显示服务器
- 窗口管理器(MUtter,kwin)
- 合成器 (Compositor)
- 输入管理(鼠标键盘触摸)
4. GUI框架层
- GTK(GNOME系列应用)
- Qt(KDE系列应用)
- Electron(跨平台应用)
- Flutter(新一代跨平台)
5. GUI应用层
- 文件管理器(Nautilus,Dolphin)
- 系统设置(gnome-control-center)
- 网络管理小程序
- 软件中心

- **常用基本命令**
```
1. 安装图形环境包，拉回所有依赖
sudo apt install ubuntu-up
2. 移除图形界面
sudo apt purge gdm3 gnome-shell
3. tty命令
首次登陆记得输入用户名和密码而不是sudo
输入密码没有任何反馈时直接按回车键重新执行sudo命令
4.注意事项
GRUB菜单不响应键盘时，通常不是系统死机，而是键盘驱动在引导阶段尚未加载，此时尝试强制重启并且自动修复
```

## 系统功能层(主动层)UserSpace

### 模块化分层
- **应用接口层UserSpace**
1. 网络管理器app - 图形化wifi设置
2. 终端命令 -ip,ping,curl
3. 软件中心 -图形化软件管理
4. GUI,CLI工具,用户程序

- **系统服务层UserSpace**
1. NetworkManger -网络连接管理
2. systemd-resolved -DNS解析服务
3. apt/apt-get/synaptic -软件包管理,解决依赖，下载
4. 日志服务 -系统运行日志

- **网络协议桟UserSpace**
1. 自动获取ip分配 - DHCP客户端
2. 网络管理连接调度中心 - NetWorkManger
3. DNS解析工具 - systemd-resolved
4. 防火墙 -ufw/firewalld
5. 功能：连接wifi,配置ip,设置dns ：服务 ：怎么使用网络


### 举例
- **APT**
1. 主要功能：update install remove upgrade (提供友好的软件管理界面)
2. 定位：高级用户接口
3. 层级：应用层的系统工具：系统包管理工具/应用层/工具层/
2. 基本命令
```
1.清理apt缓存
sudo rm -rf /var/lib/apt/lists/*
sudo apt clean
sudo apt update
2.update install remove upgrade etc
```

- **软件源(Software Sources)**
1. 定位：软件分发基础设施
2. 层级：属于服务层的基础设施：/服务层/资源层
2. 仓库配置
```
1.检查仓库配置更换软件源
sudo sed -i 's/cn.archieve.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
sudo apt update
2.直接编辑源列表文件
sudo nano /etc/apt/sources.list
3.更新软件列表
sudo apt clean
sudo rm -rf /var/lib/apt/lists/*
sudo apt update
```


##  核心层Kernel Space
- 系统保护机制：系统不止一个内核或者只有一个内核时安全限制只会标记为删除
### 组成
- **内核(Kernel)**
1. linux内核 -管理所有硬件和进程
2. 系统调用 -应用程序与内核的通信接口
3. 进程调度 -决定哪个程序先运行
- **内核驱动层**
1. 网卡驱动 =让系统识别无线网卡
2. 文件系统驱动 =读写不同格式的磁盘
3. 设备驱动 =各种硬件设备的驱动程序

- **基础系统库 - 程序的砖块**
1. glibc-c语言标准库
2. libcrypto -加密算法库
3. libssl -ssl/tsl加密库

-  **硬件控制层 - 设备管理**
1. udev- 动态设备管理，自动识别U盘，打印机
2. modprobe- 内核模块加载/卸载
- 文件系统 - 数据存储基础
1. ext4/xfs/btrfs - 文件系统格式
2. mount - 磁盘挂载系统
3. inode管理 - 文件元数据管理

- **包管理引擎**
1. dpkg -Debian/ubuntu 包管理核心
2. rpm -RedHat/CentOS 包管理核心
3. pacman -ArchLinux 包管理核心

- **基础网络站 - 网络通信核心**
1. Ip分配 - 内核ip桟
2. 域名解析 - 内核socket
3. 连接管理 - 网卡驱动
4. 防火墙核心 - iptables/nftables
5. 路由表管理 -路线-（数据包转发的决策系统，数据包从哪个网卡发出去那里）-(网络路径选择 内核维护和查询根据目标选择最佳路径 自动运行)
6. TCP/IP协议桟 -格式标准-(跨平台通用，靠近硬件，自动运行用户不可见)-(IP,TCP,UDP,ICMP协议)
7. 功能： 数据包如何传输，网卡怎么驱动，防火墙怎么过滤：能力：如何实现通信


### 举例
- **dpkg，rpm**
1. 主要功能：实际安装处理, 不负责处理依赖关系，直接对软件包进行操作
2. 定位：真正的软件安装引擎
3. 层级：核心层的系统组件
4. 基本命令
```
1. 删除
# 查看当前正在使用的内核版本
uname -r
sudo dpkg --purge linux-etc
2. 安装
sudo dpkg install appname
```

- **交互举例**

| 层级 (功能)    |       命令        | 作用   |权限|
| --------|------------------|:-----|-----|
| 硬件信息层 |` lspci -v  `       | 查看设备信息 | 只读 不控制 |
| 核心层 |`modprobe iwlwifi `  | 加载驱动 | 读写权限高 直接操作硬件 访问物理内存 内核模块编程 特权层 | 
| 功能层 |`nmcli device connect`| 连接网络 | 读写权限受限  通过系统调用间接访问 只访问虚拟内存 应用程序编程 普通权限|

| 层级 (运行空间)    |       命令        |
| --------|------------------|
| UserSpace         | `systemctl list-units --type=service `|
| Kernel Space |  `lsmod  cat /proc/net/dev `|



## 系统文件
- **文件系统驱动翻译**
1. ext4/xfs/brtfs驱动 -不同文件格式的读写能力
2. 网络文件系统驱动(nfs/cifs) -访问网络存储
3. 虚拟文件系统(VFS) -统一所有文件系统的接口
- **存储管理**
1. 磁盘分区管理(fdisk/parted)-划分存储空间
2. 逻辑卷管理(LVM)- 灵活调整存储容量
3. RAID管理-磁盘冗余阵列
- **文件操作核心**
1. inode管理
2. 块分配算法 -磁盘空间分配
3. 缓存机制 - 读写性能优化
- **挂载系统分配**
1. mount/umount挂在和卸载
2. /etc/fstab自动挂载配置
3. autofs按需自动挂载

- **特有功能**
```
mkfs.ext4 /dev/sda1 创建文件系统
tune2fs -l /dev/sda1调整文件系统参数
xfs_repair /dev/sdb1修复文件系统
```

- **流程**
应用程序 -> 系统调用 -> 虚拟文件系统VFS -> 具体文件系统驱动 -> 磁盘驱动  -> 硬件层
读取文件 ->  open() -> 统一接口       -> ext4驱动       -> SATA驱动  -> 硬盘



