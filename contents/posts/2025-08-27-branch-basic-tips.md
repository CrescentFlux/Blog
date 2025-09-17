### 分支注意事项
<1>.基础命令
```
1. 查看
#查看远程分支有那些文件
git ls-tree -r --name-only origin/分支名
#只看某个文件是否存在
git show feature/feature-name:file.py
#如果远程文件过多可以过滤查找
git ls-tree -r --name-only origin/feature | grep "utils"
#在当前目录下查看git的状态并且显示详细信息
git status -uall
git status -- update-feature/
#查看远程仓库信息
git remote -v
#查看最近的提交历史
git log --oneline -5
#获取分支信息
git fetch origin


2. 搜索
#查看当前所有分支
git branch
git branch -a/-r
#精确搜索需要的分支
git branch -r | grep branch-name
#从远程拉取分支信息
git fetch origin
#检查是否有隐藏的文件
ls -a |grep "\.git(\.gitignore)"
#在当前目录查找文件在哪里
find . -name "name.md" -type f
#全局查找
find /d/ -name "name.py" -type f 2>/dev/null
#查看所有.md文件
ls -la *.py

3. 删除
#删除分支(先检查再删除)
git branch
git checkout main
git branch -d feature/feature-name
#删除新文件
git clean -f filename.md
#重置到主分支的状态保留工作区状态
git reset main --mixed
#重置分支指针(回退main)
git reset --soft main
#删除所有不需要的文件
git clean -fd (删除所有未跟踪的文件和目录)
#删除旧文件
git rm name.md

4. 提交
#撤销提交
git reset HEAD~
#添加目标文件
git add filename.py
#重新提交
git commit -m "rename"

5. 创建新分支
#基于主分支创建新分支
git switch -c feature/name
#安全创建新分支
git switch -b feature/newname

```
<2>. 复制部分文件注意事项
1. 复制某一分支下的文件夹到另外一个分支.注意先切换到目标分支
```
#从远程直接拉取某一分支的文件夹到目标分支，会同时覆盖目标分支同名文件夹下的所有文件
git checkout origin/featurename  doucument-name/(文件或这文件夹路径)
#同时复制多个文件夹
git checkout origin/featurename  doucument-name/   doucument-name2/
#被拉取后会自动添加到暂存区如果不需要暂存可以运行
git reset HEAD -- 文件路径
```
2. 一次性移动多个文件
```
mv 文件1.js 文件2.css dc.png 目标文件夹/
```
3. 切换分支
```
git switch origin/target-branch
git chechout origin/main(target-branch)
如果在分支上修改添加了文件，想保留修改，必须在切换分支之前提交之后再切换分支
```
4. 文件在同一个目录下且有命名规律
```
git checkout origin/devlot -- **/test/*.js
git checkout origin/main -- docs/*.md
```
5. 打包提交//

6. 只复制需要的文件到当前目录
```
cp /d/doucument/name.md ./
cp /d/doucument/name.md .
->add +commit
```


<3>. 重命名
1. 重命名文件夹
```
mv (远程保留旧文件名)->delete + create
git mv oldname newname ->renamed
```
2. 添加所有更改，或包括所有文件不只是目标文件
```
git add -A(新增，修改，删除的文件)
```


