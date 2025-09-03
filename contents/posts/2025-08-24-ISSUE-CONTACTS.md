# bash 基础命令
```
#切换盘符
cd d/file-name
cd /c/Users/user-name/.ssh
cd "C:\Users\user-name\.ssh"
#创建文件夹
mkdir file-name
#创建正确的目录结构
mkdir -p .github/ISSUE_TEMPLATE/
#查看准确的文件结构
find .-name ".github" -o -name "github" -o -name "*issue*" -o -name "*template*"
#显示隐藏文件
ls -la
#vim编辑遇到卡顿时用nano替换
nano .github/ISSUE_TEMPLATE/filename
{ctrl+o保存；ENTER确认文件名；ctrl+x退出；}
#显示当前路径
pwd
#打开markdown 文件时，不会检测文件名是否真的存在
code file-name
#打开整个仓库
code .
#特定打开某个文件
code "/d/file-name"
#创建多行文件333333
cat > d/doucument/file-name <<'EOF(文件结束)'
文件内容...
EOF
#创建文件
touch filename
touch .github/ISSUE_TEMPLETE/filename.md
#同时创建分级文件夹
mkdir -p .github/ISSUE_TEMPLATE
#git命令
git add ./github
#查看文件目录结构
tree .github/
find .github/
#查看是否创建了文件夹
ls -la |grep .github
#查看文件内容
cat .github/ISSUE_TEMPLATE/file-name.md
#返回上级目录
cd ..
cd /d/filename
#检查端口是否被占用
sudo ss -tulpn | grep ':number'
#添加正确的PATH环境变量
where code
which code
export PATH="$PATH:/c/Program Files/Microsoft VS Code
#vim编辑和退出
vim config
ESC -> :wq
#删除文件，注意正确的删除方法,不要跑错目录
rm -f file-name
#删除整个模板文件夹
rm -rf .github/ISSUE_TEMPLATE
#查看最近提交历史
git log --oneline -5
#显示远程仓库的实际文件树
git ls-remote --heads origin
#查看最新提交的文件列表
git ls-tree -r HEAD -- .github/ISSUE_TEMPLATE/
#直接检查远程文件内容
git show origin/main:.github/ISSUE_TEMPLATE/file-name.md
git show HEAD:.github/ISSUE_TEMPLATE/file-name.md
#基于main创建新功能分支
git checkout -b feature/user-authentication  ->{add-commit  -> push origin feature/user-authentication -> 完成后发起pull request合并到main}
git checkout -b hotfix/login-error ->{ add-commit  -> push origin hotfix/login-error ->快速测试后合并到main}
#检查文件编码
file -i README.md
#定期备份
cp README.md README.md_Backup_$(date +%Y%m%d).md
#避免危险命令
sed -i
#显示所有特殊字符
cat -A README.md
#丢弃不需要的修改
git restore filename.md


```
# ISSUE 注意事项

<1>. 模板文件格式必须时正确的yaml格式


<2>. 模板文件必须有正确的YAML front matter确保格式
```
---
name: "CNTACTS"
description:"CONTACTS"
about:"CONTACTS"
title:"CONTACTS"
labels:["enhancement"]
assignees:
    -username
---
### 正文内容
### TRUE TIPS OR Article

```
<3>. 创建模板文件-push之后的延时问题检查方法
```
    1. {//检查是否推送到远程仓库HEAD -> main, origin/main
    git status 
    git log
    git log --oneline -- .github/ISSUE_TEMPLATE/file-name
    git remote -v
    git push origin main
}
    2. https://github.com/USERNAME/REPOSITITORY-NAME/blob/main/.github/ISSUE_TEMPLATE/FILE-NAME.md(是否push成功)
       https://github.com/USERNAME/REPOSITITORY-NAME/tree/main/.github/ISSUE_TEMPLATE/FILE-NAME.md(是否push成功)
   
```
<4>. 理解仓库结构
```
     1. 包含main分支和其他分支，main下面包含Tree文件结构,tree包含文件内容{二进制大对象blob (这个路径指向一个文件) }和文件夹Tree；
     2. main分支合并过程 ；它包含了(稳定版);feature(新功能);hotfix(紧急修复);docs(文档更新);后三个分支用来合并新版本最后发布；
```

<5>. 路径问题
```
    ../../往上走两级   /issues/站内绝对路径   完整绝对路径https://
    https://github.com/UERSNAME/REPOSRITORY/issues/new?assigenees=UERSNAME&&labels=bug&template=filename.md
```

<6>.标签系统
```
    包含enhancement,documentation,discussion,bug
```
<7>. 缓存延迟问题
```
    1. README链接后面添加随机参数?v=1、2、3
    2. ？raw=true 查看原始文件 
       #直接访问原始文件
       curl https://raw.gitbusercontent.com/NAME/REPOSITOTRYNAME/main/README.md
       #比较本地和远程差异
       git diff origin/main README.md
```

### SSH认证

```
{SSH 代理启动 && 密钥添加到代理 && 认证失效}

killall ssh-agent
eval "$(ssh-agent -s)
ssh-add ~/.ssh/keys-name
git push origin main
ssh -T git@github.com

#编辑config
Host github.com
HostName ssh.github.com
Port 443
User git
IdentityFile "C:/doucuments/keys-id"
IdentitiesOnly yes


```