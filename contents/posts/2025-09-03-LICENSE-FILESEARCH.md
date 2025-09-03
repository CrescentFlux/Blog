# license实操
```
add file -> create a new file -> Name your file-> license
choose a license template -> preview and submit->commit changes
a new branch->propose changes->create pull request
Merge pull request -> confirm merge

```

# 文件查找
```
1. 分支
git switch main(切换)
git branch -a(查看所有分支)
git branch(只列出本地所有分支)
git reflog (查看最近所有的操作记录)
git branch -av(列出所有可能的分支包括本地没有Push的分支)

2. 查看详细的提交历史图
git log --oneline --graph --all --decorate
3. 在所有分支中搜索包含特定关键词的提交注释
git log --all --oneline --grep="auto"
4. 列出所有不被任何分支或标签引用的分支或提交
git fsck --full --no-reflogs --unreachable --lost-found | grep commit -d' ' -f3 | xargs -n 1 git log -n 1 --oneline
5. 查看某个特定提交的文件列表
git show --name-only 1234abc
git show 1234eds
6. 查看旧的提交里有什么文件
git ls-tree --name-only 1234abdc

```
# 理解指针
```
HEAD指针会指向可能没有被正式命名和branch的位置
Detached HEAD 分离头指针(只读模式)：可以指向旧的任意存档点(commit) 并且修改提交，注意是否确定绑定分支；
切换方法
1. git switch -f feature/clean-update(丢弃当前所有更改)
2. git switch -c feature/clean-update(切换修改之后同时在旧存档点建立新分支)

```

# 仓库移动的文件注意事项
```
1. 基础复制命令
cp /d/repositoryname/name.md（会把旧仓库的.git文件夹也复制过来）
cp /d/repositoryname/name.md . (一次复制一个类型的文件)

2. tar 命令打包排除(会把旧仓库的.git文件夹也复制过来)
tar --exclude='LICENSE' --exclude='update-feature' -czf temp.tar.gz .
tar -xzf /d/war/temp.tar.gz
rm /d/war/temp.tar.gz

3. 确认是否确实只连接对应的仓库
git remote -v
git remote remove origin
git remote add origin git@github.com/name/name.git

4. 检查是否有旧的配置残留
cat .git/config

5. 测试SSH是否连接正常
ssh -T git@github.com
如果不正常：测试ssh文件是否存在，并且启动代理
ls -la ~/.ssh/
mkdir ~/.ssh
eval "$(ssh-agent -s)"
ssh-add "D:/filename/key_name"

6. 注意接受不同步历史的合并
git commit --no-edit

7. 仓库地址问题
经常检查远程地址
git remote -v
注意为不同的仓库设置不同的远程名推送时明确指定远程仓库
git remote add new-repo git@github.com
git remote add old-repo git@github.com
推送时明确指定远程仓库
git push new-repo main

8.注意避免复制隐藏文件如.git
cp -r /d/file/* /d/F/ 2>/dev/null || true

```

# 理解不同的文件
```
1. .git
HEAD && config && description
objects/目录信息
logs/日志
refs/地址包含(remotes/ origin)
heads/
```
# 常见错误注意事项
```
git mv 只能追溯被添加到暂存区的文件(git add .)
cd 命令只切换文件夹目录，不改变git的分支状态，HEAD指向只和分支有关
注意规范操作记录
注意复制操作时文件夹不要混淆


```