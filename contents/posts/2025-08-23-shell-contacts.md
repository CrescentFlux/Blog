# 基本命令复习

```
#重命名文件夹
mv old-name new-name
#创建文件夹
New-Item -Name "file-name" -ItemType "File"
#初始化git仓库
git init && git add . && git commit 
#实时记录
gc -Wait
#回溯
git restore\checkout .
#回溯记录
git log
#重命名分支
git branch -M main
#查看分支名称
git branch
#检查当前的远程地址
git remote -v
#删除现有远程地址
git remote remove origin
#重新添加远程地址
git remote add origin git@github.com
#只添加特定文件时不要加引号
git add file-name
#用管理员权限启动服务时：运行之后设置服务为手动启动并且启动服务
Set-Service -Name ssh-agent -StartupType Manual
Start-Service ssh-agent
#在当前shell中启动一个管理员权限的新的窗口
Start-Process powersell -Verb runAs
#检查文件是否存在
Test-Path C:\Users\chinaname\other-namefile
#查看某个目录下的所有文件
Get-ChildItem C:\Users\chinaname\other-namefile
#复制文件
Copy-Item "filepath-name"
#全盘搜索可能包含id_*的文件
Get-ChildItem -Path C:\ -Name id_* -File -ErrorAction SilentContinue | Where-Object {$_like "id_*"}
#查看当前目录下有没有包含关键词的文件
Get-ChildItem -Path . -Name id_*
#检查当前的远程地址
git remote -v
#创建一个新的工作目录
cd 或者 mkdir D:\
#打开文件
notepad file-path

 ```

 # shell配置

 ```
 #执行关联命令
 git remote add origin https://github.com/username/repository-name.git
 #尝试推送
 git push -u origin main 
 ######SSH注意事项######
 #生成SSH密钥
 ssh-keygen -t name -C "email@example.com" (ssh不会自动创建不存在的目录，注意先创建目录，再生成密钥)
 #将公钥添加到Github显示公钥内容
 cat ~/.ssh/file-name  -> settings
 #之后测试连接 and push 
 ssh -T git@github.com //ssh -T -i D:\projects\ssh_keys\keysname git@github.com
 git push -u origin main
//
 #配置git                                
 git config user.name "Admin"          
 git config user.email "name@example.com"
 #&&配置git使用新密钥
 cd D:D:\projects\
 git config core.sshCommand "ssh -i  D:\projects\ssh_keys\keysname "
 #添加远程仓库(不会检查这个仓库是否真的存在，不能推送空仓库，分支名一致，远程地址一致)
 git remote add origin git@github.com:ADMIN/File.repository.git
 #从远程拉取内容
 git pull origin main
 #添加文件并推送
 git add .
 git commit -m "new start"
 git push -u origin main


```
## 注意事项
```
 ##中文路径循环限制###
 C：\Users\china-name\.ssh\contents {  known_hosts 已知主机记录 known_hosts.old 旧的已知主机记录  config SSH 配置文件 }
 #<1>Permission denied 
 #启动SSH代理-添加密钥到代理-测试连接
 Get-Service ssh-agent | Set-Service -StartupType Manual -PassThru | Start-Service
 ssh-add ~/.ssh/keysname
 ssh -T git@github.com


 #<2>Access is denied#
 #以管理员身份运行
 Get-Service ssh-agent |Set-Service -StartupType Manual -PassThru | Start-Service


 #<3>could not create directory#{中文路径循环限制}#
 #绝对路径指定系统寻找known_hosts文件 ->push   ssh内部的库无法正确解析包含中文的路径
 ssh -o UserKnownHostsFile="C: \Users\china-name\.ssh\known_hosts"
 #$HOME变量（确保.ssh存在并且明确指定Known_hosts 文件的正确路径）
 New-Item -ItemType Dicrectory -Path "$HOME\.ssh" -Force
 ssh -o UserKnownHostsFile="$HOME\.ssh\Known_hosts" -T git@github.com


#<4>让所有连接包括git push都使用正确的Known_hosts文件
notepad "$HOME\.ssh\config"
#[1]在notepad中配置SSH客户端的文件
Host github.com
     HostName github.com
     User git
     IdentityFile ~/.ssh/keys-name
     UserKnownHostsFile ~/.ssh/Known_hosts

#[2]使用绝对路径
$env:GIT_SSH_COMMAND = "ssh -o UserKnownHostsFile=C :/Users/china-name/.ssh/known_hosts"

#[3]给git看的临时环境变量
$env:GIT_SSH_COMMAND = "ssh -o UserKnownHostsFiles=$HOME\.ssh\known_hosts";git push -u origin main
GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=$HOME\.ssh\known_hosts" &&push   (bash not shell)

#[4]全绝对路径
ssh -o UserKnownHostsFile="C:\Users\china-name\.ssh\known_hosts"  ;git push -u origin main
#手动创建known_hosts文件（获取GitHub指纹-手动添加到known_hosts文件）
ssh-keyscan github.com
ssh-keyscan github.com>>"$HOME\.ssh\Known_hosts";git push -u origin main

#[5]命令行生成文件导致的编码问题->直接手动创建hosts文件,进行替换，编码选择ANSI 或者 UTF-8,测试是否询问指纹验证；确实系统信任GitHub服务器
#authenticity can not be established -> permission denied
 github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==
 github.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87pRexKs80lVdJsjY2Mih+2l4U0aV2ogZyH+6l4TQnWE=
 github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
 #(5.1)测试agent是否运行并且查看SSH调试详细信息（管理员权限启动服务）
 Start-Service ssh-agent
 ssh-add ~/.ssh/keysfile-name
 ssh -T git@github.com
 git push -u origin main
 ssh -T -v git@githubcom
 #(5.2)直接执行push时指定密钥或者设置临时环境变量绕过agent
 git -c core.sshCommand="ssh -i C:Users\china-name\.ssh\keys-file" push
 $env:GIT_SSH_COMMAND = "ssh -i C:Users\china-name\.ssh\keys-file" push   if -> no such file or directory 
 ssh-add $HOME/.ssh/keys-filename  or ssh-add C:\Users\china-name\.ssh\keysname
 #(5.3)push时直接用git push 指定密钥文件路径
 git -c core.sshCommand= "ssh -i C:\Users\chinaname\.ssh\keyname" push -u origin main
 #(5.4)使用短名称路径
 cmd /c dir /x %USERPROFILE%  or 
 $ShortPath = (Get-Item $HOME).FullName
 cmd /c dir /x $ShortPath | Select-String $ShortPath//获取短名称
 git -c core.sshCommand="ssh -i C:Users\china-name\.ssh\keys-file" push -u origin main
#(5.5)确保SSH正确运行&&git远程是SSH&&push没有使用SSH认证&&git配置是否被覆盖
git remote remove origin
git remote add origin git@github.com:NAME/file.git
git -c core.sshCommand="ssh -i C:Users\china-name\.ssh\keys-file" push -u origin main//明确指定git使用哪个密钥文件
#[6]终极诊断
#详细测试SSH连接，查看认证全过程&查看当前所有的和SSH相关环境变量是否冲突&查看当前SSH代理加载了那些密钥，缓存是否加载错误密钥&查看详细的GIT配置
ssh -T -v git@github.com
Get-ChildItem env: | Where-Object{$_.Name -like "*SSH*" -or $_.Name -like "*GIT*"}
ssh-add -L
git config --list --show-origin

The-sametime 使用全新的明确的SSH命令来推送
cd D:\filepath
Start-Process -Wait -NoNewWindow git  -c core.sshCommand="ssh -i C:Users\china-name\.ssh\keys-file" push -u origin main"

#[7]确保密钥添加到SSH代理
Get-Service ssh-agent
ssh-add C:\Users\chinaname\.ssh\keyfile
ssh-add -l
git push -u origin main

#[8]确保hub上已经创建了仓库，确保仓库名一致，使用绝对路径推送  &&permission denied
git remote remove origin
git remote add origin git@github.com:NAME/file.git
git -c core.sshCommand="ssh -i D: projects\keys-file" push -f -u origin main"
&& $env : GIT_SSH_COMMAND = "ssh -i D: /projects/keys-file" push -f -u origin main
&& $env : GIT_SSH_COMMAND = "ssh -i D: /projects/keys-file -o UserKnownHostsFile=/dev/null -o StrictHostChecking=no" #使用正斜杠避免路径问题，禁用已知主机检查，正确指定key路径
&& 创建SSH配置文件{
    Test-Path D: /projects/keys-file
    mkdir -Force ~/.ssh/config
    text:
        Host github.com
        HostName github.com
        User git
        IdentityFile D: /projects/keys-file
        IdentitiesOnly yes
        StrictHostKeyChecking no
        UserKnownHostsFile /dev/null
}
#key权限
icacls D: /projects/keys-file:r
icacls D: /projects/keys-file:r "$env:USERNAME:(R)"
&& icacls "D: /projects/keys-file" /inheritance:r /grant:r "$env:USERNAME:(F)"
icacls D: /projects/keys-file
#SSH连接测试
ssh -T -i D: /projects/keys-file git@github.com
#确保key添加到settings


 ```


 ### checkout 注意事项
 ```
 <1>使用避免vim的方式合并
 git pull origin main --allow-unrelated-histories --no-edit
 #或者先设置编辑器
 git config --global core.editor "code --wait"
 git pull origin main --allow-unrelated-histories
 <2>预防Vim问题
 git config --global core.editor "code --wait"//设置VS为默认编辑器
 git config --global core.editor "false"//不进入编辑器
 <3>分支历史冲突问题
 git commit --no-edit