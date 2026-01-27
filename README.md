# 🌐 我的技术成长花园
> 编程 | Git & PowerShell &  Algorithm | 开源分享

<div style="text-align: center; margin: 2rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
  <h3>📚 知识库状态</h3>
  <p>本花园正在持续培育中，目前已有：</p>
  <div style="font-size: 2.5rem; font-weight: bold; color: #2c8c3f;" id="noteCount">--</div>
  <p>篇技术笔记扎根于此。</p>
  <p style="font-size: 0.9em; color: #666; margin-top: 1rem;"><i>💕数据动态更新于每次提交后</i></p>
</div>

<script>
// 配置区：请修改下面的 username 和 repo 为你的信息！
const username = 'CrescentFlux'; // 你的GitHub用户名
const repo = 'Blog'; // 你的仓库名，例如这里用 'STORY'，请确认
const folderPath = 'contents/posts'; // 要统计的文件夹路径，如 '技术笔记'。留空则统计整个仓库。

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

## 📚 技术笔记索引
### 🔍快速检索
- **[按日期查看](https://github.com/CrescentFlux/Blog/tree/main/contents/posts)**

## 🕐成长仪表盘
### 🏆 成就系统
- ✅ Git推送大师
- 🔄 PowerShell
- ⏳ 技术分享者

## 🤝成长游戏区
### 💬 交流互动
<p>
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=bug&template=bug_report.md" target="_blank">🐛 报告Bug</a> | 
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=enhancement&template=feature_request.md" target="_blank">💡 提出建议</a> | 
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=documentation+discussion&template=share_experience.md" target="_blank">🌟 分享经验</a>
</p>

> "🐅🌹心有猛虎，细嗅蔷薇"
