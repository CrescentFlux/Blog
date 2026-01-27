# 🌱 我的技术成长花园
<div style="text-align: center; margin: 2rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
  <h3>📚 知识库生长状态</h3>
  <p>本花园正在持续培育中，目前已有：</p>
  <div style="font-size: 2.5rem; font-weight: bold; color: #2c8c3f;" id="noteCount">--</div>
  <p>篇技术笔记扎根于此。</p>
  <p style="font-size: 0.9em; color: #666; margin-top: 1rem;"><i>✨ 数据动态更新于每次提交后</i></p>
</div>

<script>
// 配置区：请修改下面的 username 和 repo 为你的信息！
const username = 'CrescentFlux'; // 你的GitHub用户名
const repo = 'Blog'; // 你的仓库名，例如这里用 'STORY'，请确认
const folderPath = ''; // 要统计的文件夹路径，如 '技术笔记'。留空则统计整个仓库。

// 组装 API 请求 URL
let apiUrl = `https://api.github.com/repos/${username}/${repo}/git/trees/HEAD?recursive=1`;

fetch(apiUrl)
  .then(response => response.json())
  .then(data => {
    // 筛选出 .md 文件，并可以根据路径过滤
    let files = data.tree.filter(item => 
      item.type === 'blob' && 
      item.path.endsWith('.md') &&
      (folderPath === '' || item.path.startsWith(folderPath))
    );
    // 更新页面上的数字
    document.getElementById('noteCount').textContent = files.length;
  })
  .catch(error => {
    console.error('获取数据失败:', error);
    document.getElementById('noteCount').textContent = '?';
    document.getElementById('noteCount').style.color = '#dc3545';
  });
</script>
> 每日编程修炼 | Git & PowerShell 学习笔记 | 开源分享

![GitHub Last Commit](https://img.shields.io/github/last-commit/CrescentFlow/My-Final-Blog)
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=CrescentFlow.My-Final-Blog)

## 📚 技术笔记索引

### Git 专题
- [Git推送问题解决方案](2025-08-23-shell-contacts.md)
- [分支管理技巧](2025-08-21-git-tips.md)

### PowerShell 专题  
- [PowerShell基础命令](2025-08-22-powershell-basic-contacts.md)

### 学习路径
- [我的技术学习路线图](learning-path.md)


## 🕐成长仪表盘




#### 🎯 当前重点
- ✅ Git高级技巧
- 🔄 PowerShell自动化
- ⏳ Shell脚本编程

#### 🏆 成就系统
- ✅ Git推送大师
- 🔄 PowerShell
- ⏳ 技术分享者




## 🤝成长游戏区

#### 🔍 快速检索
- [按日期查看](https://github.com/CrescentFlux/Blog/tree/main?sort=committerdate)
- [按标签筛选](#)  
#### 💬 交流互动
<p>
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=bug&template=bug_report.md" target="_blank">🐛 报告Bug</a> | 
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=enhancement&template=feature_request.md" target="_blank">💡 提出建议</a> | 
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=documentation+discussion&template=share_experience.md" target="_blank">🌟 分享经验</a>
</p>



> "🐅🌹心有猛虎，细嗅蔷薇"
