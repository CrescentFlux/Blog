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
// 最简方案：去掉递归查询，直接查 posts 文件夹
const username = 'CrescentFlux';
const repo = 'Blog';

// 直接查 posts 文件夹内容（不是整个仓库树）
fetch(`https://api.github.com/repos/${username}/${repo}/contents/contents/posts`)
  .then(response => response.json())
  .then(data => {
    // 统计 .md 文件
    let count = 0;
    data.forEach(item => {
      if (item.type === 'file' && item.name.endsWith('.md')) {
        count++;
      }
    });
    
    document.getElementById('noteCount').textContent = count;
    document.getElementById('noteCount').style.color = '#149b67ff';
  })
  .catch(error => {
    console.log('加载失败，显示缓存或默认值');
    document.getElementById('noteCount').textContent = '?';
    document.getElementById('noteCount').style.color = '#ff4757';
  });
</script>

## 📖 技术笔记索引
### 🔍快速检索
- **[按日期查看](https://github.com/CrescentFlux/Blog/tree/main/contents/posts)**

## 🕐成长仪表盘
### 🏆 成就系统
- ✅ Git推送大师
- 🔄 Algorithm
- ⏳ 技术分享者

## 🤝成长游戏区
### 💬 交流互动
<p>
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=bug&template=bug_report.md" target="_blank">🐛 报告Bug</a> | 
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=enhancement&template=feature_request.md" target="_blank">💡 提出建议</a> | 
  <a href="https://github.com/CrescentFlux/Blog/issues/new?assignees=CrescentFlux&labels=documentation+discussion&template=share_experience.md" target="_blank">🌟 分享经验</a>
</p>

> "🐅🌹心有猛虎，细嗅蔷薇"
