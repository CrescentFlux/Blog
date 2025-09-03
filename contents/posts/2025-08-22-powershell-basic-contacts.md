# powershell运行注意事项

### <1>区分访问对象的属性和使用变量的命令

在powershell 中理解{$__.} 这个占位符表示管道传过来的每一个对象，然后用点号来反应他的属性

```
Get-Service | Where-Object {$_.Status -eq 'Running'}
Get-Service | Where Status -eq 'Running'查找正在运行的服务
Get-Service | Where-Object {$_.Name -like "*Update*"}查找名字里带更新的服务
Get-Service | Where-Object {$_.Status -eq 'Running'
-and $_.StartType -eq 'Automatic'}查找正在运行并且启动为自启动的服务
Get-Service | Select-Object Name, Status 只显示服务的名字和状态
cd D:\ls -Recurse | Where-Object { $_.Name -eq "8.18.md" }找到你的文件到底在哪

```

### <2>基本命令
文件增删改查
``` 
Get-Content gc, cat获取文件内容
Get-ChildItem ls, dir, gci列出文件目录
Get-Service gsv获取服务信息
Get-Process ps, gps获取进程信息
Set-Location cd, chdir切换工作目录
Copy-Item cp, copy复制文件或目录
Remove-Item rm, del, rd删除文件或目录
```
push操作
``` 

# 添加变更
git add .
# 提交备份，并留下记录
git commit -m "备份：又写了一段关于XXX的内容"
# 添加远程仓库地址
git remote add origin https://github.com/你的用户名/你的仓库名.git
# 将本地备份推送到远程
git push -u origin main

# 2 再次添加所有变更
git add .
# 提交备份，并留下记录
git commit -m "备份：又写了一段关于XXX的内容"
# 将本地备份推送到远程
git push 
#推送

#重命名分支
git branch -M main
# 还原到最后一次提交的状态
git restore .
# 强制还原所有文件
git checkout -- .
# 查看当前文件发生了什么变化
git status
# 查看 8.19.md 这个文件的历史修改记录
git log -p 8.19.md
# 查看最近一次修改了哪些具体内容
git show
#监听文件
gc "8.18.md" -Wait
Get-Content -Path "8.18.md" -Wait


#创建文件夹
mkdir
#创建文件
New

```


### <3>快速系统健康调查-记录名字和PID

``` 
# 1. 扫描所有正在运行的程序（进程）
ps | Sort-Object -Property CPU -Descending | Select-Object -First 20 > D:\baseline_processes.txt
# 2. 扫描所有启动项
Get-CimInstance Win32_StartupCommand | Select-Object Name, command, Location | Format-List > D:\baseline_startup.txt
# 3. 扫描所有计划任务
Get-ScheduledTask | Where-Object {$_.State -eq 'Ready'} | Select-Object TaskName, State > D:\baseline_tasks.txt
# 4. 扫描所有服务
Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object Name, DisplayName > D:\baseline_services.txt
# 根据进程名查找更多信息
ps -Name "badguy*" | Format-List *
```
