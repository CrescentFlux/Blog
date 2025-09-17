# ROS配置
- **安装**(官方网址https://www.ros.org)
```
1. 查看ubuntu版本 
lsb_release -a/-d
24.04(Noble) ROS2 Jazzy
22.04(Jammy) ROS2 Humble(LTS)
22.04(Focal) ROS1 Noetic(LTS)

2. 启用Universe仓库
sudo apt update && sudo apt install curl -y(更新系统)
sudo apt install software-properties-common
sudo add-apt-repository universe

3. 设置ROS2 apt仓库，将ROS2的软件源仓库添加到你的系统
- github的原始文件服务器 `https://raw.githubusercontent.com `
sudo curl -sSL https://raw.githubusercontent.com/ros/master/ros/ros.asc -o ~/ros.asc

4. 在ROS中获取最新的类目依赖总清单
echo "deb [arch=$(dpkg --print-architecture)signed-by=/usr/share/keyrings/ros-archive-keyrings.gpg](密钥路径)
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main"|(源路径)
sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null(sudo tee添加权限)

5. 更新软件包并安装ros2
sudo apt update
sudo apt install ros-jazzy-desktop-full -y (桌面完整版)

6. 配置环境，需要让终端知道ROS2命令的位置添加到特定文件里面
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc

7. 安装编译工具和依赖管理工具
sudo apt install python3-rosdep2 python3-colcon-common-extensions

8. 初始化并更新rosdep(一个用于安装依赖的工具)
sudo rosdop init
rosdep update

```

- demo测试
```
1.开启新的终端窗口加载新的环境变量
source /opt/ros/jazzy/setup.bash
printenv | grep ROS

2.启动ROS核心
ros2 run turtlesim turtlesim_node

3.启动键盘控制节点(另外一个终端)
ros2 run turtlesim turtle_teleop_key

3.查看内部发生什么
ros2 topic list

```

## 网络连接问题注意事项
### **1. 为代理配置Terminal网络环境(curl,wget,apt)**
1. 找到代理端口号(Port)
```
- 查找正在监听的端口号
netstat -tulpn | grep LISEN
```
- 作为客户端时不需要专门配置一个端口给自己用系统会随机分配一个临时端口给某次连接使用，用完后回收
- 作为服务端必须提前固定占用一个端口并对外宣布端口号
- 每个需要接收网络数据的程序都要配置唯一的端口号接收信息，端口是网络程序唯一门牌号

2. 理解回环地址
- 不是用来上网的公网ip,而是一个特殊的，固定的内部代号
- 127.0.0.1指的是正在使用的这台电脑自己(localhost)

3. 在端口号中设置环境变量(Environment Variables)
```
- 仅仅当前会话有效
export http_proxy="http://127.0.0.1:YOUR_PORT"
export https_proxy="https:/127.0.0.1:YOUR_PORT"
#设置完成后需要关闭所有终端重新启动才会生效
#测试是否成功
curl -I https://www.google.com
```
```
- 将代理设置写入配置文件(永久生效，不需要手动export)，.bashrc直接设置
nano ~/.bashrc
export http_proxy="http://127.0.0.1:YOUR_PORT"
export https_proxy="https:/127.0.0.1:YOUR_PORT"
source ~/.bashrc
#注意：
系统所有的网络请求包括apt update都会试图走代理文件，当某个源出问题时临时取消代理设置只会对当前这个终端窗口生效，不会影响永久设置
unset http_proxy
unset https_proxy
sudo apt update
```
### **2. sudo权限继承环境变量的注意事项**
1. 注意添加sudo权限之后，环境变量可能会失效,需要让sudo继承代理环境
- 配置sudoers,让sudo自动继承代理环境变量
```
1.编辑特定的配置文件
sudo visudo (/etc/sudoers,避免使用vim,nano直接修改文件)
2.取消注释,确认保留keep指定的环境变量env,保存退出
Defalut env_keep +="http_proxy https_proxy"
3.关闭当前所有的终端窗口然后重新打开一个新的终端窗口并且测试
sudo curl -sSL https://raw.githubusercontent.com/ros/master/ros/ros.asc -o ~/ros.asc
```
2. 注意不同位置的区别：
```
~/ros.asc：
~符号代表了家目录，用户对家目录拥有完全的读写权限，不会被系统拒绝
/usr/share/keyrings/ros-archive-keyring.gpg：
/usr/share/keyrings是一个系统级的，受保护的目录，普通用户即使用了sudo权限让curl工作时，可能会因为环境变量继承或安全策略等问题导致操作没有足够的权限而失败
-正确步骤：下载到家目录然后使用sudo mv纯粹权限极高的命令把文件从家目录搬到系统目录
sudo mv ~/ros.asc /usr/share/keyrings/ros-archive-keyring.gpg
```

### 3. 软件源验证及准备工作
#### 3.1 验证软件源是否被成功添加步骤
1. 临时关闭代理
```
-删除旧密钥
sudo rm /usr/share/keyrings/ros-archive-keyrings.gpg
-开启代理
export https_proxy-"http://127.0.0.1:port"
-下载到home目录
curl -sSL https://raw.githubusercontent.com/ros/master/ros/ros.asc -o ~/ros.asc
-移动密钥到系统位置
sudo mv ~/ros.asc /usr/share/keyrings/ros-archive-keyring.gpg
-关闭代理
unset https_proxy
-再次更新
sudo apt update
```
2. 验证步骤
```
-检查ros源有没有被正确添加
apt-cache policy | grep ros// 在当前本地的软件包缓存里搜索包含ros字母的包
sudo apt update | grep ros
apt-cache policy | grep packages.ros.org

-正确位置名称
http://packages.ros.org/ros2/ubuntu noble InRelease[number]
```
#### 3.2 准备工作
- **源列表文件唯一作用是告诉系统应该去哪里找软件，它本身不包含如何验证安全性的信息**
```
1. 自动查询电脑的硬件和系统版本，生成地图
$(dpkg--print-architecture) && echo$UBUNTU_CODENAME
-$(...)在运行的瞬间，自动获取信息并且把信息填充到命令里，最终把命令变成deb[arch=amd64 signed-by=...]http://...noble main
2.传递并且写入系统的任务清单
-管道符号表示把上一条的命令输出，塞给下一条命令当作输入
-echo "deb[...]":在屏幕上打印一行文本
-将收到的东西显示在屏幕上并且写入指定文件
sudo tee /etc/apt/sources.list.d/ros.list(源列表文件)
```

###  4. 公钥(ros.asc)验证
#### **4.1 基本概念**
- **公钥的唯一作用是让系统学会如何验证签名，它本身不包含任何要去哪里下载软件的信息**
- **apt update只下载清单，并且验证清单的签名**
- apt是非常注重安全的工具，它下载了ROS提供的软件列表之后，会用之前下载的官方印章GPG公钥去核对列表的数字签名；
- 公钥文件 (.asc或者.gpg):一个可能包含很多公钥文件格式和内容的公钥文件备案函
- 密钥指纹 ：某个特定公钥的shortened哈希值，唯一，用于快速，精确的定位；指纹是公钥的内在属性；
- 逻辑：在ROS的仓库拿到一份带有防伪盖章(指纹号)的最新的产品总清单(记录了名称，版本号，以及它们之间的依赖关系)，然后比对官方样本册里的指纹号是否存在并且一致进行真伪验证;

#### 4.2 其他验证方法
- 单独查询某个指纹号是否在全球密钥服务器管理局的信息，然后公示;
- 具体步骤
```
1.删除之前所有的可能干扰的密钥文件
sudo rm -f /etc/apt/trusted.gpg.d/ros-archive-keyring.gpg
sudo rm -f /usr/share/keyrings/ros-archive-keyring.gpg
2.直接获取(keyserver.ubuntu.com)
sudo gpg --homedir /tmp --nodefault-keyring --keyring /etc/apt/trusted.gpg.d/ros-archive-keyring.gpg --keyserver keyserver.ubuntu.com --recv-keys 指纹号
3.更新
sudo apt update
```
#### 4.3 密钥文件路径及排查方法
- **排查**
```
1. 检查密钥文件是否真的在系统里
gpg --list-keys --keyid-format long 指纹号
2. 检查apt现在信任哪些密钥文件
ls -la /etc/apt/trusted.gpg.d/
ls -la /usr/share/keyrings/
3.检查ROS源配置的具体内容是否正确
cat /etc/apt/sources.list.d/ros2.list
```
- **修复路径**
1. 指向实际位置
```
1. 修正密钥路径错误并且指向(signed-by)它实际所在的位置
sudo sed -i 's|/usr/share/keyrings/ros-archive-keyring.gpg|/etc/apt/trusted.gpg.d/ros-archive-keyring.gpg|g' /etc/apt/sources/list.d/ros2.list
2.检查清单
cat /etc/apt/sources/list.d/ros2.list
```
2. 指向官方推荐位置
```
-把密钥移动到规范位置
sudo mv /etc/apt/trusted.gpg.d/ros-archive-keyring.gpg /usr/share/keyrings/
-确保源列表指向规范位置
sudo sed -i 's|/etc/apt/trusted.gpg.d/ros-archive-keyring.gpg|/usr/share/keyrings/ros-archive-kering.gpg' /etc/apt/sources.lists.d/ros2.list
```

### 5. SSL/TLS通信
- **基本流程**
1. 本地发出接头信号(Client Hello)并且宣告支持的加密算法套件类型(A/B/C),并且生成一个随机数挑战码(client Random)用于后续生成最终钥匙，确保每次对话的钥匙都不同；
2. ROS服务器回应(Server Hello + Certificate)并且出示证件(SSL证书，上面有证书颁发机构CA的签名);并且告诉它的随机数挑战码(Server Random);
3. 本地核实证件(Certificate Verification),本地拿出内置的，绝对信任的根证书存储库，检查CA签发机关是否在名录上，用CA的公钥去核对证件上的防伪签名；
4. 生成最终会话钥匙(Key Exchange & Finished)
```
- 本地生成预备主密钥(Pre-Master Secret)：生成后用证件上的公钥把他加密，传给ROS
- 双方生成主密钥：现在双方都有client Random,server random,pre-master secret，用B体系将这三个数字混合计算，生成一把最终的主密钥
- 双方切换加密通道用主密钥加密解密
- 开始安全通信
```






