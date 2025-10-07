# Rtree
## 基础知识
- **定义**
```
R树是B树在多维空间的扩展，它使用层次化的最小边界矩形(MBR)来组织空间对象，支持高效的范围查询、最近邻查询等空间操作。
```

- **MBR（最小边界矩形）**
    - 定义：包含对象的最小轴对齐矩形
    - 性质：保守近似、快速计算
    - 操作：重叠检测、合并、面积计算

- **R树基本结构**
    - 节点类型：叶子节点 vs 非叶子节点
    - 条目结构：(MBR, 子指针) 或 (MBR, 数据指针)
    - 树性质：平衡树、高度一致
- **空间索引基础**
    - 空间数据：空间数据是描述物体在二维或三维空间中位置、形状、大小和相互关系的数据
    - 空间索引：快速排除不相关区域；减少碰撞检测计算量；高效空间聚合查询；优化空间查询性能
    - 与传统索引的差异
性能特征对比：

|方面	|传统索引|	空间索引|
---|---|---
|索引构建|	基于标量值排序|	基于空间聚类|
|查询优化	|范围扫描、二分查找	|空间剪枝、MBR过滤|
|数据分布|	均匀分布易处理	|空间聚集是常态|
|扩展维度	|单维索引简单|	多维索引复杂度高|

- **特性**

|特性|	描述|	重要性|
---|---|---
|平衡性|	所有叶子节点在同一层	|保证查询性能O(log n)|
|层次MBR	|父节点MBR包含所有子节点MBR|实现快速剪枝|
|动态更新	|支持插入删除而不重建	|适用动态数据集|
|空间局部性	|相近对象在树中相邻	|提高缓存效率|


## 注意事项
- R树的核心思想是用 最小边界矩形（MBR） 来近似表示复杂的空间对象
- 每个R树节点都对应一个 最小边界矩形（MBR），它包含了该节点所有子节点/数据的边界范围
- R树从B树继承了两个重要特性：自平衡和面向磁盘的优化
- 在R树中，叶子节点存储的是实际数据的MBR和指向数据的指针
- 非叶子节点存储的是其子节点的聚合MBR和指向子节点的指针
- 指针关系要点

|关系	|正确关系|
---|---
|父子关系|	双向指针：父节点→子节点，子节点→父节点|
|条目结构|	包含MBR + 子节点指针（非叶子）或数据（叶子）|
|根节点|	可能分裂（树长高）或压缩（树变矮）|

- 概念区分

|概念|	正确理解|
---|---
|MBR 用途|	近似边界框，用于快速空间剪枝|
|节点 vs 条目|	节点是容器，条目是连接单元（MBR+子指针/数据）|
|树结构	|平衡树，叶子节点存储数据引用，非叶子节点存储子节点引用|

- 算法设计

|决策|	设计原理|
---|---
|子树选择	|最小化MBR膨胀，保持树结构紧凑|
|分裂策略|	空间聚类优化，减少查询时的重叠区域|
|重新插入	|延迟重构，避免删除引起的连锁反应|
|容量管理|	动态范围（m到M），平衡存储效率与查询性能|

- 健壮性编码要点

|实践|	正确方式|
---|---
|方法设计|	单一职责，每个方法只完成一个明确任务|
|错误处理|	防御性编程，检查关键数据结构和指针|
|状态管理	|确保操作过程中的数据一致性|
|调试支持	|详尽的日志输出，便于跟踪复杂操作流程|

### mbr需要安全检查
- 安全检查
1. 删除操作后的空节点
```
// 删除数据后，节点可能变空
delete(mbr, data) {
  const found = this._findLeaf(this.root, mbr, data);
  const { node, entryIndex } = found;
  node.entries.splice(entryIndex, 1);  // 删除条目
  
  // 此时节点可能变空，但_updateMBR仍然会被调用
  this._updateMBR(node);  // ⚠️ 如果node.entries为空，entry.mbr可能不存在
}
```
2. 分裂过程中的临时状态
```
_splitNode(node) {
  // 在分裂过程中，节点状态可能不一致
  const [seed1, seed2] = this._pickSeeds(node.entries);
  
  // 此时如果其他操作介入，可能看到不一致的状态
  this._updateMBR(someOtherNode);  // ⚠️ 可能遇到无效条目
}
```
3. 数据损坏或编程错误
```
// 有人可能错误地修改了数据结构
node.entries.push({ 
  data: '错误数据', 
  // 忘记添加 mbr 属性！
});

// 或者
node.entries[0].mbr = null;  // 意外设置为null
```
4. 安全检查操作
```
// 假设有这样一个节点
const problemNode = {
  isLeaf: true,
  entries: [
    { mbr: new MBR(1,1,2,2), data: 'A' },
    { data: 'B' },  // ❌ 忘记mbr属性！
    { mbr: new MBR(3,3,4,4), data: 'C' }
  ]
};
// 原始代码会崩溃：
_updateMBR(problemNode) {
  for (let entry of node.entries) {
    minX = Math.min(minX, entry.mbr.minX);  // ⚠️ 第二次循环：entry.mbr 是 undefined!
    // Uncaught TypeError: Cannot read properties of undefined (reading 'minX')
  }
}
// 安全版本会优雅处理：
_updateMBR(problemNode) {
  for (let entry of node.entries) {
    if (entry.mbr) {  // ✅ 检查mbr是否存在
      minX = Math.min(minX, entry.mbr.minX);  // 跳过有问题的条目
    }
  }
}
```
```
风险1：压缩树操作
_condenseTree(node) {
  // 收集条目准备重新插入
  removedNodes.push(...current.entries);
  // 清理parent指针
  current.entries.forEach(entry => {
    entry.parent = null;
  });
  // 如果此时条目结构有问题，后续操作会失败
}
风险2:重新插入操作
// 重新插入收集的条目
for (let entry of removedNodes) {
  this._insert(entry, this.root);  // ⚠️ 如果entry.mbr无效，插入会失败
}
```
- 节点MBR无效
```
在 _findLeaf 方法中，还在使用 entry.mbr.equals(mbr)，但是那个有问题的 MBR 对象缺少 equals 方法。
将 equals 调用替换为直接比较：
for (let i = 0; i < node.entries.length; i++) {
      if (node.entries[i].mbr.equals(mbr) && node.entries[i].data === data) {
        return { node, entryIndex: i };
      }
    }
那个显示为 Object { minX: 1, minY: 1, maxX: 6, maxY: 4 } 的 MBR 对象是一个普通对象，不是 MBR 类的实例，所以它没有 equals 方法
 _findLeaf(node, mbr, data) {
  // 6. 如果节点MBR与目标MBR不重叠，返回false
  //🧪安全检查
  if (!node || !node.mbr || typeof node.mbr.overlaps !== 'function') {
    return null;
  }

  if (!node.mbr.overlaps(mbr)) {
     console.error('节点MBR无效:', node.mbr);
    return null;
  }
  if (node.isLeaf) {
    // 7. 在叶子节点中查找匹配的条目/数据对象
    for (let i = 0; i < node.entries.length; i++) {
      if (node.entries[i].mbr.equals(mbr) && node.entries[i].data === data) {
        return { node, entryIndex: i };
      }
    }
  } else {
    // 8. 在非叶子节点中递归查找子节点
    for (let entry of node.entries) {
      if (entry.mbr.overlaps(mbr)) {
        const found = this._findLeaf(entry.child, mbr, data);
        if (found) return found;
      }
    }
  }
  return null;
}
- tree 变量未定义;这个是因为变量作用域问题
```
### 防御性编程
- **并发修改问题**
```
index = -1//找不到匹配的条目
// 假设在某个时间点：
// 父节点 P 有条目指向子节点 C
// 但在我们执行 findIndex 之前，其他代码修改了父节点
// 时间线：
// T1: 父节点 P.entries = [entryA, entryB, entryC] 其中 entryB.child = C
// T2: 其他代码执行了 P.entries.splice(1, 1)  // 移除了 entryB
// T3: 我们的代码执行 findIndex(entry => entry.child === C) // 返回 -1
```
- **根节点特殊情况**
```
时序问题：更新根节点引用 vs 更新所有子节点的 parent 指针不是原子操作
性能考虑：遍历更新所有子节点的 parent 指针代价很高
算法设计：RTree 通常不维护双向的完整一致性，以换取更好的性能
```
- **这种不一致是分布式系统（即使是单机内存中的对象关系）中常见的"最终一致性"问题。防御性编程就是为了处理这种现实世界中的不完美情况**
```
"节点认为自己的父节点" vs "父节点认为这是自己的子节点" 可能不一致
1.根节点引用改变，但当前节点还指向旧的根节点
// 初始状态
this.root = rootNode;      // 根节点是 rootNode
current.parent = rootNode; // 当前节点的父节点是根节点
// 某个操作改变了根节点（比如根节点分裂）
this.root = newRootNode;   // 现在根节点变成了 newRootNode
// 但是 current.parent 还指向旧的 rootNode
console.log(current !== this.root); // true，因为 current ≠ newRootNode
console.log(current.parent);        // rootNode（旧的根节点）
console.log(this.root);             // newRootNode（新的根节点）
// 问题：旧的 rootNode 可能已经被回收，或者它的条目中不包含 current
2.父节点被修改，但子节点还保留旧的父引用
// 初始正确的父子关系
parentNode.entries = [entry1, entry2, entry3];
// 其中 entry2.child = current;
current.parent = parentNode;
// 某个操作修改了 parentNode 的条目
parentNode.entries = [entry4, entry5]; // 完全替换了条目数组
// 现在：
// current.parent 仍然指向 parentNode
// 但 parentNode.entries 中已经没有指向 current 的条目了
const index = parentNode.entries.findIndex(entry => entry.child === current);
// index = -1，因为找不到匹配的条目
```
- **内存或数据损坏**
内存损坏"更多指的是数据一致性被破坏，而不是真正的内存位被修改
```
1. 引用失效（Dangling References）
// 场景：对象被删除但引用还在
let parent = new RTreeNode(false);
let current = new RTreeNode(true);
current.parent = parent;
// 然后某个操作删除了 parent
parent = null; // 或者被垃圾回收
// 但 current.parent 还指向那个内存位置
console.log(current.parent); // 可能不是 null，而是无效引用
2. 数据竞争（Data Races）
// 虽然不是真正的多线程，但异步操作可能导致类似问题
async function dangerousOperation() {
  const parent = current.parent;
  // 在 await 期间，其他代码可能修改了 parent.entries
  await someAsyncOperation();
  // 现在 parent.entries 可能已经被其他操作修改
  const index = parent.entries.findIndex(entry => entry.child === current);
  // index 可能为 -1
}
3.意外的对象修改
// 第三方代码或插件可能意外修改对象
// 假设有个调试工具或浏览器插件
parent.entries = []; // 被外部代码清空
// 或者深拷贝/序列化过程中出错
const serialized = JSON.stringify(parent);
const restored = JSON.parse(serialized);
// restored.entries 可能不完整
4.原型链污染
// 有人可能修改了 Array.prototype
Array.prototype.findIndex = function() { return -1; }; // 恶意的修改
// 现在所有的 findIndex 调用都返回 -1
const index = parent.entries.findIndex(entry => entry.child === current);
// 总是返回 -1，即使实际上存在匹配项
```
- **在高级语言中处理这个问题**
```
    复杂的状态管理：RTree 维护着复杂的对象关系图
    异步操作：即使单线程，Promise 和 async/await 也可能导致时序问题
    外部干扰：浏览器扩展、开发工具可能意外修改对象
    序列化/反序列化：保存到 localStorage 或通过网络传输可能损坏数据
    框架或库的干扰：某些 JavaScript 框架可能代理或包装对象
```
- **算法边界情况**
```
在状态转换期间的短暂不一致窗口
核心问题：状态更新不是原子操作
在 _handleRootSplit 过程中，树的根节点发生了变化，但这个变化需要多个步骤完成，在此期间树处于不一致状态。
状态转换的原子性很重要：
```
```
_handleRootSplit(oldNode, group1, group2) {
  // 🕒 T1: 开始分裂，此时树状态：
  // this.root = oldNode (旧的根节点)
  // oldNode.parent = null (根节点没有父节点)
  // 所有子节点都正确指向 oldNode 作为父节点
  const newRoot = new RTreeNode(false);
  // 🕒 T2: 创建了新根节点，但还没有设置关系
  // this.root 还是 oldNode
  // newRoot 是孤立节点
  const entry1 = new RTreeEntry(group1.mbr, group1);
  const entry2 = new RTreeEntry(group2.mbr, group2);
  newRoot.entries.push(entry1, entry2);
  // 🕒 T3: 设置了新根节点的条目，但父指针还没更新
  // group1.parent 还是 oldNode (错误的!)
  // group2.parent 还是 oldNode (错误的!)
  this._updateMBR(newRoot);
  // 🕒 T4: 更新了根节点引用 - 这是关键步骤！
  this.root = newRoot;  // ⚡️ 树现在有新的根节点了
  // 🕒 T5: 但子节点的 parent 指针还没有更新！
  // group1.parent 仍然指向 oldNode
  // group2.parent 仍然指向 oldNode
  // 这就产生了不一致
}
假设在 T4-T5 这个时间窗口，另一个操作介入：场景1和场景2
```
```
场景1
class RTree {
  _handleRootSplit(oldNode, group1, group2) {
    console.log("步骤1: 创建新根节点");
    const newRoot = new RTreeNode(false);
    console.log("步骤2: 设置新根节点的条目");
    newRoot.entries.push(
      new RTreeEntry(group1.mbr, group1),
      new RTreeEntry(group2.mbr, group2)
    );
    console.log("步骤3: 更新根节点引用");
    this.root = newRoot; // ⚡️ 关键变化点
    
    // ⚠️ 问题：在这个时间点，如果有人访问树：
    // - this.root 指向 newRoot (新根)
    // - 但 group1.parent 还是 oldNode (旧根)
    // - group2.parent 还是 oldNode (旧根)
    console.log("步骤4: 更新子节点的parent指针");
    group1.parent = newRoot;  // 现在才更新
    group2.parent = newRoot;  // 现在才更新
    console.log("步骤5: 完成，状态一致");
  }
  // 假设在步骤3和步骤4之间，这个函数被调用
  someOtherOperation() {
    console.log("当前根节点:", this.root === newRoot); // true
    console.log("group1的父节点:", group1.parent === oldNode); // true ❌
    // 不一致状态！
  }
}
```
```
// 场景2：并发操作（即使是单线程的异步操作）
async function dangerousScenario() {
  // 操作1：开始根节点分裂
  tree._handleRootSplit(oldNode, group1, group2);
  // 执行到 T4：this.root = newRoot 已完成
  // 但 T5：子节点parent指针更新还没完成
  
  // 操作2：另一个异步操作试图访问树
  await someAsyncTask();
  
  // 现在调用删除操作
  tree.delete(someMBR, someData);
  
  // 在 _condenseTree 中：
  let current = someNode;
  while (current !== this.root) { // this.root 是 newRoot
    const parent = current.parent; // 但 current.parent 可能是 oldNode
    
    // 问题：oldNode 可能已经被清理，或者它的状态无效
    const index = parent.entries.findIndex(entry => entry.child === current);
    // 可能返回 -1，因为 oldNode 不再是有效的父节点
  }
}
```
```
//解决方法//
1.原子性更新（推荐）
_handleRootSplit(oldNode, group1, group2) {
  const newRoot = new RTreeNode(false);
  // 先建立完整的关系
  const entry1 = new RTreeEntry(group1.mbr, group1);
  const entry2 = new RTreeEntry(group2.mbr, group2);
  newRoot.entries.push(entry1, entry2);
  // 更新所有子节点的parent指针
  group1.parent = newRoot;
  group2.parent = newRoot;
  // 最后才更新根节点引用
  this.root = newRoot; // 现在状态是一致的
}
2.防御性编程
_condenseTree(node) {
  let current = node;
  while (current !== this.root) {
    const parent = current.parent;
    // 检查父子关系一致性
    if (!parent) break;
    const index = parent.entries.findIndex(entry => entry.child === current);
    if (index === -1) {
      // 检测到不一致，安全处理
      console.warn('检测到父子关系不一致，安全退出');
      break;
    }
    // ... 正常处理
  }
}
```
2. **代码实现**
```
//===================================核心逻辑+测试逻辑================================//
//===========R树的基础构建块==============//
class RTreeEntry {
    //R树中非常重要的核心组件//条目//RTreeEntry 是文件夹里的文件（或者子文件夹的快捷方式）
    //RTreeEntry 确保了：边界框、子指针、数据三位一体;不需要维护多个数组的对应关系;代码更清晰，不容易出错
  constructor(mbr, child = null, data = null) {
    this.mbr = mbr;     // 边界框
    this.child = child; // 指向子节点（非叶子节点）
    this.data = data;   // 实际数据（叶子节点）
  }
}
//=========MBR类负责几何计算=========//
class MBR {
  constructor(minX, minY, maxX, maxY) {
    this.minX = minX;//这个矩形在整个坐标系中的最左边位置
    this.minY = minY;//这个矩形在整个坐标系中的最右边位置
    this.maxX = maxX;//这个矩形在整个坐标系中的最下边位置
    this.maxY = maxY;//这个矩形在整个坐标系中的最上边位置
    }
    //==========几何属性：面积计算=============//
    //MBR 自己的业务逻辑
     // 添加 equals 方法
  equals(other) {
    if (!other) return false;
    return this.minX === other.minX && 
           this.minY === other.minY &&
           this.maxX === other.maxX && 
           this.maxY === other.maxY;
  }
    // 计算面积//area() 和 extend() 是矩形的几何属性，不是树的操作
  area(){
    // 13. 面积 = 宽度 × 高度
    return (this.maxX - this.minX) * (this.maxY -this.minY);
  }
  //==========几何操作：扩展边界===========//
//扩展当前MBR以包含另一个MBR
//JavaScript类对方法顺序比较敏感：// 先定义基础方法// 再定义复杂方法
//在插入过程中，选择子节点的标准是选择面积增量更小的那个
//节点分裂是为了维持R树的平衡特性
//更新节点MBR时，需要遍历所有条目来计算新的边界
  extend(other) {//这两个方法应该放在 MBR 类里面，而不是 RTree 类里面//面向对象设计原则：职责分离
    //几何操作//自我扩展
    // 1. 更新边界以包含另一个MBR
    this.minX = Math.min(this.minX, other.minX);
    this.minY = Math.min(this.minY, other.minY);
    this.maxX = Math.max(this.maxX, other.maxX);
    this.maxY = Math.max(this.maxY, other.maxY);
    return this;//返回修改后的自己为了支持链式调用
  }
  //======几何关系：重叠检测=====//
   //--2.检查两个MBR是否重叠--//
  //比较它们在共享的坐标系中的位置关系
  overlaps(other) {//充分必要条件
    //1.数学上如果只是边界接触没有实际重叠区域，通常不算重叠；
    //2.加等号查询边界情况：如果查询矩形刚好碰到某个数据的边界，我们通常希望返回这个数据；性能考虑：包含等号的判断稍微快一点；实用主义：在空间索引中，边界接触通常被视为"相关"；
    const xOverlap = this.minX <= other.maxX && this.maxX >= other.minX;// 检查X轴投影重叠
    const yOverlap = this.minY <= other.maxY && this.maxY >= other.minY;// 检查Y轴投影重叠 
    return xOverlap && yOverlap;
    //return this.minX <= other.maxX && this.maxX >= other.minX &&
    //this.minY <= other.maxY && this.maxY >= other.minY;
  }
  toString() {
    return `(${this.minX},${this.minY},${this.maxX},${this.maxY})`;
  }
}

//============树的管理单元===========//
class RTreeNode {//RTreeEntry 类是 R树中非常重要的核心组件;它是树的"连接单元"//节点
    //RTreeNode 是文件夹
  constructor(isLeaf = false) {//标识是否为叶子节点（布尔值，true/false）
    this.isLeaf =isLeaf;//开关
    this.entries = []; //容器//存储条目的数组//一个节点包含多个条目//叶子节点的条目：指向实际数据//非叶子节点的条目：指向子节点
    this.mbr = null;//边界框//该节点的最小边界矩形（MBR对象或null）//每个节点只有一个MBR，表示整个节点的覆盖范围//用于快速判断"是否需要搜索这个节点的子树"
    this.parent = null;// ✅添加 parent 指针
}
}
//========插入逻辑========//
class RTree {//RTree 类：负责树结构管理//
    constructor(maxEntries = 4) {
    this.root = new RTreeNode(true);  //✅根节点是叶子节点
    this.maxEntries = maxEntries;
    this._updateMBR(this.root);       //✅初始化根节点MBR
  }
  insert(mbr, data) {
    const entry = new RTreeEntry(mbr, null, data);//是用户要存储的实际数据，不是树节点
    //从根节点开始插入新条目
    this._insert(entry,this.root);
  }
  //---插入核心方法---//
  _insert(entry, node) {
    // 1.如果当前节点是叶子节点，直接添加
    // ✅设置条目的 parent 指针（如果是叶子节点）
    entry.parent = node;

    if (node.isLeaf) {// 检查当前正在处理的节点是否为叶子节点//已经是布尔值，直接使用即可，不需要 =true
      node.entries.push(entry);
      //1.1更新节点的MBR
      this._updateMBR(node);
      //1.2如果节点超过容量，需要分裂
      if (node.entries.length > this.maxEntries) {
        this._splitNode(node);
      }
      return;
    }
    //2. 如果不是叶子节点，选择最优子树进行插入
    let bestChild = this._chooseSubtree(entry, node);
    this._insert(entry, bestChild);
  }
  //----选择最优子树---//
  _chooseSubtree(entry, node) {//确保返回的是节点而不是条目
  let bestChild = null;//记录当前最优的子节点
  let minAreaIncrease = Infinity;//记录当前最小的面积增量//Infinity作为一个很大的初始值，确保第一个计算的值一定会比它小
  //1.遍历所有子节点，找出插入新数据后MBR膨胀最小的那个
  for (let childEntry of node.entries) {
    //2. 获取子节点信息
    const child = childEntry.child;//子节点对象
    const originalArea = child.mbr.area();//子节点当前的面积
    // 3. 创建扩展后的MBR（包含新条目）//加入新节点之后内部节点的新面积
    const expandedMBR = new MBR(
      child.mbr.minX, child.mbr.minY, 
      child.mbr.maxX, child.mbr.maxY
    );
    expandedMBR.extend(entry.mbr);//扩展以包含新点
    // 4. 计算面积增量 = 扩展后面积 - 原始面积
    //通过计算每个子节点容纳新数据所需的"额外空间代价"，选择代价最小的路径
    //贪心算法：在每一步都做出局部最优选择，从而期望获得全局较优的结果
    const areaIncrease = expandedMBR.area()-originalArea;
    // 5. 选择面积增量最小的子节点
    //决胜规则，处理是平局情况//多标准决策//
    if (areaIncrease < minAreaIncrease || //当前子节点的面积增量更小，直接选择它
        (areaIncrease === minAreaIncrease && originalArea < bestChild.mbr.area())) {//如果面积增量相同，选择原始面积也就是没有插入新的子节点之前内部节点的mbr面积更小的那个
        //决胜规则体现了R树的自我优化机制：首要目标：最小化MBR膨胀面积增量；次要目标：优先选择原本就紧凑的MBR；
        //小面积的MBR通常意味着数据更集中、更紧凑；保持小MBR的"纯洁性"有助于维持整体树的效率；大面积的MBR可能已经比较"松散"，再添加数据影响较小
            minAreaIncrease = areaIncrease;
      bestChild = child;
      //算法设计中如何平衡不同优化目标；最优性：总是选择面积增量最小的子节点；公平性：当增量相同时，给紧凑的小MBR优先权；效率：通过保持MBR紧凑，维持查询性能
    }
  }
  return bestChild;
}
//-----更新节点的mbr----//
//节点MBR vs 条目MBR:
//节点MBR需要包含它所有条目MBR的边界(需要计算);每个条目都有自己的MBR;
  _updateMBR(node) {
  if (node.entries.length === 0) return;
  // 1. 重新计算节点的MBR（包含所有条目的MBR）
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (let entry of node.entries) {
     // ✅ 简单安全检查
    if (!entry.mbr) {
      console.warn("条目缺少MBR:", entry);
      continue;
    }
    minX = Math.min(minX, entry.mbr.minX);//所有条目的最小minX
    minY = Math.min(minY, entry.mbr.minY);//所有条目的最小minY
    maxX = Math.max(maxX, entry.mbr.maxX);// 所有条目的最大maxX
    maxY = Math.max(maxY, entry.mbr.maxY);// 所有条目的最大maxY
  }
   // ✅ 确保创建的是 MBR 实例，不是普通对象
  //node.mbr = new MBR(minX, minY, maxX, maxY);//创建全新的MBR对象
  // ✅ 确保创建 MBR 实例
  if (minX !== Infinity) {
    node.mbr = new MBR(minX, minY, maxX, maxY);
  } else {
    node.mbr = null;
  }
}

//------分裂节点-----//
//维护树结构//先定义被调用的方法
//在某些JavaScript引擎中，当方法包含条件调用时，可能会在解析阶段就检查被调用方法是否存在
//在分裂过程中设置 parent 指针
_handleSplitResult(oldNode, group1, group2){
  if (oldNode === this.root) {
    // 情况1：分裂的是根节点
    this._handleRootSplit(oldNode, group1, group2);
  } else {
    // 情况2：分裂的是普通节点  
    this._handleNormalSplit(oldNode, group1, group2);
  }
}
_handleRootSplit(oldNode, group1, group2) {
  //// 🎯 职责：专门处理根节点分裂
  // 1. 创建新的根节点
  const newRoot = new RTreeNode(false); // 非叶子节点
  // 2. 创建两个新条目指向分裂出的两个组
  const entry1 = new RTreeEntry(group1.mbr, group1);
  const entry2 = new RTreeEntry(group2.mbr, group2);
  // 3. 把新条目加入新根节点
  newRoot.entries.push(entry1, entry2);
   // 🕒 4: ✅关键步骤：设置子节点的parent指针
  group1.parent = newRoot;  // group1现在知道父节点是newRoot
  group2.parent = newRoot;  // group2现在知道父节点是newRoot
  // 5. 计算新根的MBR
  this._updateMBR(newRoot);
  // 6. ✅关键步骤；更新树的根节点引用
  this.root = newRoot;
  //  🕒 7: 现在oldNode成为孤立节点，可以被垃圾回收
}
_handleNormalSplit(oldNode, group1, group2) {
   // 🎯 职责：专门处理内部节点分裂
  // 1. 找到父节点维护指针//获取父节点
  const parent = oldNode.parent;
  // 2. 在父节点中找到oldNode对应的条目指针
  const oldEntryIndex = parent.entries.findIndex(entry => 
    entry.child === oldNode
  );
  // 3. 移除原来的条目指针
  parent.entries.splice(oldEntryIndex, 1);
  // 🕒 T: ⚠️ 关键步骤：设置新节点的parent指针//从父节点移除 oldNode 的引用 - 避免悬空引用
  group1.parent = parent;  // group1的父节点是parent
  group2.parent = parent;  // group2的父节点是parent
  // 4. 添加两个新条目指针
  parent.entries.push(
    new RTreeEntry(group1.mbr, group1),
    new RTreeEntry(group2.mbr, group2)
  );
  // 5. 更新父节点的MBR
  this._updateMBR(parent);
  // 6. 如果父节点也超容了，继续分裂！
  if (parent.entries.length > this.maxEntries) {
    this._splitNode(parent); // 递归分裂
  }
}
//-----分裂逻辑-----//
//理解节点分裂
//插入之后叶子节点满了导致的分裂
//节点分裂时，通常选择 找两个"差异最大"的两个条目作为新组的种子：1.建立清晰的分组边界：让两个初始组在空间上明显分离；2.避免后续纠结：如果种子很相似，后面分配剩余条目时会很困难；3.促进紧凑性：差异大的种子自然引导形成紧凑的子MBR
//分裂的目标是让新产生的两个MBR尽可能"方正"，并且总面积和重叠面积都尽可能小
//如果分裂一直传递到根节点，当根节点分裂时，会创建新的根节点，树的高度会增加1
//找到两个MBR合并后"浪费空间"最多的组合
// 选择种子时要用extend计算合并MBR
//const combinedMBR = seed1.mbr.extend(seed2.mbr);//extend 方法会修改原对象//seed1.MBR这个变量指向的同一个对象，它的内部属性被修改了
// 将seed1的MBR扩展，使其能够包含seed2的MBR：它现在能同时包含原来的seed1区域和seed2区域////需要创建副本，避免修改原对象
  _splitNode(node) {
  // 1. 选择两个种子条目 - 这里调用_pickSeeds
  const [seed1, seed2] = this._pickSeeds(node.entries);
  // 2. 创建两个新组
  const group1 = new RTreeNode(node.isLeaf);
  const group2 = new RTreeNode(node.isLeaf);
  // 3. 把种子分别放入两个组
  group1.entries.push(seed1);
  group2.entries.push(seed2);
  // 4. 初始化组的MBR
  group1.mbr = new MBR(seed1.mbr.minX, seed1.mbr.minY, seed1.mbr.maxX, seed1.mbr.maxY);
  group2.mbr = new MBR(seed2.mbr.minX, seed2.mbr.minY, seed2.mbr.maxX, seed2.mbr.maxY);
  // 5.创建剩余条目列表
  //_pickSeeds 只选出了两个起点，而不是把所有条目都分好组//种子选择建立宏观框架，条目分配完成微观优化
  const remainingEntries = node.entries.filter(
    entry => entry !== seed1 && entry !== seed2//从节点的所有条目中，过滤掉那两个已经被选为种子的条目，剩下的就是还需要分配的条目
  );
  // 6. 分配剩余条目
  while (remainingEntries.length > 0) {
    //平衡检查//实现了复杂的系统稳定性保障
    //R树的容量规则：每个节点必须满足：最小条目数 <= 当前条目数 <= 最大条目数//通常：最小条目数 = ceil(最大条目数 / 2)
    if (group1.entries.length + remainingEntries.length <= Math.ceil(this.maxEntries / 2)) {//把剩余所有条目都分配给group1
        //左边：group1当前条目数 + 剩余条目总数//强制把剩余条目都给组1，确保它达到最小容量
        //预防性思维：通过数学计算提前发现"这个组可能永远无法达到健康状态"，然后立即采取纠正措施
        //没有节点会过于稀疏（影响查询效率）；树的高度保持稳定（避免退化成链表）；空间局部性得以维持（相近的数据确实分在一起）
      for (let entry of remainingEntries) {//强制分配
        group1.entries.push(entry);//把条目加入组1
        group1.mbr.extend(entry.mbr);//扩展组1的MBR
      }
      break;
    } 
    if (group2.entries.length + remainingEntries.length <= Math.ceil(this.maxEntries / 2)) {
      for (let entry of remainingEntries) {
        group2.entries.push(entry);
        group2.mbr.extend(entry.mbr);
      }
      break;
    }
    // 7. 选择下一个条目并分配
    const nextEntry = this._pickNext(remainingEntries, group1, group2);
    //在剩下的这些条目中，哪个条目的分配决策最明确//逐个处理剩余条目，而不是一次性处理所有
    //每个条目的分配都会改变组的MBR，进而影响后续条目的分配决策//每个决策都基于当前最新的组状态
    // 8.计算面积增量（用副本）//基于最新状态决策如何分配//决策问题
    const copy1 = new MBR(group1.mbr.minX, group1.mbr.minY, group1.mbr.maxX, group1.mbr.maxY);
    const copy2 = new MBR(group2.mbr.minX, group2.mbr.minY, group2.mbr.maxX, group2.mbr.maxY);
    //选择最偏向某个组的条目，也就是两个面积增量差异最大的条目
    const areaIncrease1 = copy1.extend(nextEntry.mbr).area() - group1.mbr.area();
    const areaIncrease2 = copy2.extend(nextEntry.mbr).area() - group2.mbr.area();
    if (areaIncrease1 < areaIncrease2) {
      group1.entries.push(nextEntry);
      group1.mbr.extend(nextEntry.mbr);
    } else {
      group2.entries.push(nextEntry);
      group2.mbr.extend(nextEntry.mbr);
    }
    // 移除已分配的条目
    //避免重复处理移除元素不用指针而用移除//更直观；性能更好：不需要维护额外的数据结构；逻辑清晰：空数组直接表示工作完成
    const index = remainingEntries.indexOf(nextEntry);
    remainingEntries.splice(index, 1);
  }
  // 9. 处理分裂结果
  this._handleSplitResult(node, group1, group2);//分裂操作的收尾工作
  //当我们把节点成功分成 group1 和 group2 后，需要解决：原节点怎么办；新节点如何接入树中；父节点需要更新吗
  //维持树结构：确保分裂后的节点正确接入树中//向上传播：分裂可能引发连锁反应，需要向上处理//更新边界：父节点的MBR需要反映子节点的变化//处理根节点特例：根节点分裂是唯一让树长高的机会
}
//创建副本避免修改原对象-选择种子
//无副作用计算//函数式编程的思维
//创建副本// 只在副本上操作//原对象不受影响
//浪费空间越大 = 两个种子差异越大 = 越应该作为初始分组//通过选择浪费空间最大的组合作为种子，R树确保初始分组就有很好的空间分离性，为后续的条目分配打下良好基础
//两个种子差异很大，适合作为不同组的起点//通过最大化初始差异，为后续创造有序分组奠定基础
//如果合并两个矩形会产生大量空白区域，说明它们本来就不应该在一起;算法不试图调和所有矛盾，而是承认某些东西本质就不该在一起
//层次化解决复杂性：通过先解决"最大的分歧"种子选择，剩下的问题就变得简单：通过建立清晰的宏观结构，来简化微观决策；
//空间换时间：浪费的空间 = 分离的代价 = 未来效率的投资：今天浪费"的空白空间：换来了明天查询时能快速排除整个子树
//包容差异性是有成本的：应该明确知道什么时候应该分离，而不是强行包容
//尊重本质差异，不要强行融合所有东西；通过建立清晰边界来创造整体效率
//有时候分离比融合更有利于系统健康；投资于结构性空白，收获运行时的流畅
_pickSeeds(entries) {
  let bestPair = null;//还没有找到任何一对好的种子
  let maxWastedSpace = -Infinity;//目前找到的最大浪费空间是负无穷
  //如果强行把这两个矩形分在同一组，会产生多少无效空间；找浪费空间最大的组合
  for (let i = 0; i < entries.length; i++) {//每个可能的配对
    for (let j = i + 1; j < entries.length; j++) {
      // 创建副本进行计算，不修改原MBR
      const copy1 = new MBR(entries[i].mbr.minX, entries[i].mbr.minY, 
                           entries[i].mbr.maxX, entries[i].mbr.maxY);//做一个和entries[i] 的完全一样的复制品
      const combinedMBR = copy1.extend(entries[j].mbr);//扩展副本//同时包含 entries[i] 和 entries[j]
      const wastedSpace = combinedMBR.area() - entries[i].mbr.area() - entries[j].mbr.area();//计算这对的浪费空间
      if (wastedSpace > maxWastedSpace) {//发现新纪录
        maxWastedSpace = wastedSpace;//更新纪录成绩
        bestPair = [entries[i], entries[j]];//更新纪录保持者
      }
  }
  return bestPair;
}
}
//找到立场最鲜明的条目
_pickNext(remainingEntries, group1, group2) {//排序问题
  let maxAreaDifference = -Infinity;
  let bestEntry = null;
  // 1.遍历所有剩余条目，找到"最偏向"某个组的条目
  for (let entry of remainingEntries) {
    // 计算放入组1的面积增量（用副本）
    const copy1 = new MBR(group1.mbr.minX, group1.mbr.minY, group1.mbr.maxX, group1.mbr.maxY);
    const areaIncrease1 = copy1.extend(entry.mbr).area() - group1.mbr.area();
    // 计算放入组2的面积增量（用副本）
    const copy2 = new MBR(group2.mbr.minX, group2.mbr.minY, group2.mbr.maxX, group2.mbr.maxY);
    const areaIncrease2 = copy2.extend(entry.mbr).area() - group2.mbr.area();
    // 计算两个面积增量的差异
    const areaDifference = Math.abs(areaIncrease1 - areaIncrease2);
    // 选择差异最大的条目（最偏向某个组）
    if (areaDifference > maxAreaDifference) {
      maxAreaDifference = areaDifference;
      bestEntry = entry;
    }
  }
  return bestEntry;//只返回条目，不返回计算结果
}
//========== 查询逻辑============//
//查询优化的核心思想是通过MBR重叠检查快速排除不相关的子树
//在R树查询中，最重要的性能优化是空间剪枝
//如果查询矩形与节点MBR不重叠，该节点的所有子树都不需要搜索
//相比于暴力扫描所有数据，R树查询的优势是能够快速剪枝不相关子树
//查询性能取决于树的平衡性，而不是数据总量
//最坏情况下，R树查询需要检查所有数据
search(queryMBR) { // 范围查询：找到所有与查询矩形重叠的数据
    const results = [];//创建空数组 results 来收集结果
    this._search(this.root, queryMBR, results);//1.从根节点开始搜索//从根节点开始递归搜索
    return results;
  }
  _search(node, queryMBR, results) {
     // ✅ 添加 MBR 验证
    if (!node.mbr || !node.mbr.overlaps(queryMBR)) {//1. 重要的剪枝：如果节点MBR与查询区域不重叠，就直接返回
      return;
    }
    // ✅ 验证条目的 MBR
    for (let entry of node.entries) {//2.如果条目MBR与查询MBR重叠
      if (entry.mbr.overlaps(queryMBR)) {
        if (node.isLeaf) {// 3.叶子节点：找到匹配的数据
          results.push(entry.data);
        } else {//4. 非叶子节点：递归搜索子节点
          this._search(entry.child, queryMBR, results);
        }
      }
    }}
//=========== 删除逻辑=============//
delete(mbr, data) {
// 删除操作比插入更复杂，因为可能引起树的结构调整/重平衡
// 树收缩操作的目的是保持树的平衡性
// 重新插入策略避免了频繁的节点分裂与合并
// 最坏情况下，删除操作的时间复杂度是O(log n)
// 如果删除后根节点只有一个子节点，树的高度会降低
    // 1. 从根节点开始查找并删除
    const found = this._findLeaf(this.root, mbr, data);
    if (!found) return false;
    const { node, entryIndex } = found;
    // 2. 从叶子节点中删除条目
    node.entries.splice(entryIndex, 1);
    // 3. 更新节点的mbr
    this._updateMBR(node);
    // 4. 如果节点条目数过少，需要下溢处理
    if (node.entries.length < Math.ceil(this.maxEntries / 2) && node !== this.root) {
      this._condenseTree(node);
    }
    // 5. 如果根节点只有一个子节点，需要直接删除
    if (this.root.entries.length === 1 && !this.root.isLeaf) {
      this.root = this.root.entries[0].child;
    }
    
    return true;
  }
  //---查找叶子节点---//
 _findLeaf(node, mbr, data) {
  // 6. 如果节点MBR与目标MBR不重叠，返回false
  if (!node.mbr || !node.mbr.overlaps) {
    console.warn("节点MBR无效:", node.mbr);
    return null;
  }
  if (!node.mbr.overlaps(mbr)) {
    return null;
  }
  if (node.isLeaf) {
    // 7. 在叶子节点中查找匹配的条目/数据对象
    for (let i = 0; i < node.entries.length; i++) {
      const entry = node.entries[i];
      // ✅ 使用直接比较，避免 equals 方法
      if (entry.mbr && 
          entry.mbr.minX === mbr.minX && 
          entry.mbr.minY === mbr.minY &&
          entry.mbr.maxX === mbr.maxX && 
          entry.mbr.maxY === mbr.maxY &&
          entry.data === data) {
        return { node, entryIndex: i };
      }
    }
  } else {
    // 8. 在非叶子节点中递归查找子节点
    for (let entry of node.entries) {
      // ✅ 添加安全检查
      if (entry.mbr && entry.mbr.overlaps && entry.mbr.overlaps(mbr)) {
        const found = this._findLeaf(entry.child, mbr, data);
        if (found) return found;
      }
    }
  }
  return null;
}
//---树收缩操作---//
//压缩树的完整流程：从下溢节点开始向上遍历；如果遇到下溢节点：从父节点中移除，并收集其所有条目；如果节点健康：只需更新MBR；最后会重新插入所有收集的条目
_condenseTree(node) {
  const removedNodes = [];
  let current = node;
  // 9. 从叶子节点向上直到根节点
  while (current !== this.root) {
    const parent = current.parent;
    // ✅ 添加 null 检查
    if (!parent) {
      console.warn("警告: 找到 null parent，停止压缩");
      break;
    }
    // ✅ 先定义 index
    const index = parent.entries.findIndex(entry => entry.child === current);
    //在父节点的条目数组中查找指向当前子节点的那个条目的索引
    //找到父节点：const parent = current.parent;查找索引：const index = parent.entries.findIndex(...) 
    //1.找到当前节点在父节点中的位置
    //2.检查是否下溢：if (current.entries.length < ...)
    //3.安全删除：if (index !== -1) - 确保真的找到了才删除
    //4.收集条目：把要删除节点的所有条目保存起来
    //5.清理指针：避免内存泄漏
    //6.重新插入：把收集的条目重新插入到树
    if (current.entries.length < Math.ceil(this.maxEntries / 2)) {
      // 10. 节点条目数太少，需要移除该节点并收集其条目
      //防御性编程：即使理论上不应该发生，实践中也要检查
      // ✅ 安全检查
      if (index !== -1) {
        // ❌ 这里使用了 index，但 index 还没有定义！
        //index = -1，找不到匹配的条目
       //防止oldRoot已经不是根节点了，但子节点不知道的情况
        const removedEntry = parent.entries.splice(index, 1)[0];
        // 收集当前节点的所有条目
        removedNodes.push(...current.entries);
        // 更新被移除条目的 parent 指针
        current.entries.forEach(entry => {
          entry.parent = null;//🎯清理被移除节点的所有条目的父指针//// 重要：避免循环引用
          //1. 清理循环引用，避免内存泄漏；2. 防止后续操作访问到无效的父节点；3. 重置状态，为重新插入做准备// 被移除的条目要重新插入到树的其他位置
          // 它们应该像"新条目"一样，没有父节点关系
        });
        console.log(`✅ 压缩: 移除下溢节点，收集了 ${current.entries.length} 个条目`);
      } else {
        console.warn("⚠️ 压缩: 在父节点中找不到当前节点");
      }
    } else {
      // 11. 节点仍然健康，只需更新 mbr
      this._updateMBR(current);
      console.log("✅ 压缩: 节点健康，更新MBR");
    }
    current = parent;
    console.log(`✅ 压缩: 移除下溢节点，收集了 ${current.entries.length} 个条目`);
        console.log(`✅ 压缩: 重新插入 ${removedNodes.length} 个条目`);
        console.log("✅ 压缩树操作完成");
  }
  
  // 12. 重新插入被删除的条目，避免数据不完整
  console.log(`✅ 压缩: 重新插入 ${removedNodes.length} 个条目`);
  for (let entry of removedNodes) {
    // ✅ 重置 parent 指针
    entry.parent = null;
    this._insert(entry, this.root);
  } 
  console.log("✅ 压缩树操作完成");
}
// 在 RTree 类中添加调试方法：检查树的 MBR 状态
debugTreeMBRs(node = this.root, level = 0) {
  const indent = '  '.repeat(level);
  console.log(`${indent}节点层级 ${level}:`);
  console.log(`${indent}MBR:`, node.mbr);
  console.log(`${indent}MBR类型:`, node.mbr?.constructor?.name);
  console.log(`${indent}有overlaps方法:`, typeof node.mbr?.overlaps === 'function');
  
  if (node.isLeaf) {
    node.entries.forEach((entry, i) => {
      console.log(`${indent}  条目${i}:`, entry.mbr);
      console.log(`${indent}  条目MBR类型:`, entry.mbr?.constructor?.name);
    });
  } else {
    node.entries.forEach((entry, i) => {
      this.debugTreeMBRs(entry.child, level + 1);
    });
  }
}
}
//====测试删除操作逻辑=======//
// 在您的代码最后添加这个测试类
class RTreeTest {
  constructor() {
    this.tree = new RTree(2, 3); // 最小2个条目，最大3个条目
  }
testDelete() {
    console.log("=== R树删除操作测试 ===\n");
    // 1. 插入测试数据
    const testData = [
      { mbr: new MBR(1, 1, 2, 2), data: 'A' },
      { mbr: new MBR(3, 1, 4, 2), data: 'B' },
      { mbr: new MBR(1, 3, 2, 4), data: 'C' },
      { mbr: new MBR(3, 3, 4, 4), data: 'D' },
      { mbr: new MBR(5, 1, 6, 2), data: 'E' },
      { mbr: new MBR(5, 3, 6, 4), data: 'F' }
    ];
    console.log("1. 插入初始数据:");
    testData.forEach(item => {
      this.tree.insert(item.mbr, item.data);
      console.log(`   插入: ${item.data} ${item.mbr.toString()}`);
    });
    // 2. 打印初始树结构
    console.log("\n2. 初始树结构:");
    this.printTreeStructure(this.tree.root);
    this.validateTree(this.tree.root);
    // 3. 测试删除不会引起下溢的情况
    console.log("\n3. 测试删除 E (不会引起下溢):");
    const result1 = this.tree.delete(new MBR(5, 1, 6, 2), 'E');
    console.log(`   删除结果: ${result1 ? '成功' : '失败'}`);
    this.printTreeStructure(this.tree.root);
    this.validateTree(this.tree.root);
    // 4. 测试删除会引起下溢的情况
    console.log("\n4. 测试删除 B (会引起下溢):");
    const result2 = this.tree.delete(new MBR(3, 1, 4, 2), 'B');
    console.log(`   删除结果: ${result2 ? '成功' : '失败'}`);
    this.printTreeStructure(this.tree.root);
    this.validateTree(this.tree.root);
    // 5. 测试删除不存在的元素
    console.log("\n5. 测试删除不存在的元素:");
    const result3 = this.tree.delete(new MBR(10, 10, 11, 11), 'X');
    console.log(`   删除结果: ${result3 ? '成功' : '失败'} (期望: 失败)`);
    // 6. 验证最终数据完整性
    console.log("\n6. 最终数据验证:");
    this.verifyRemainingData(['A', 'C', 'D', 'F']);
  }
  // 打印树结构
  printTreeStructure(node, level = 0) {
    const indent = '  '.repeat(level);
    if (node.isLeaf) {
      const entries = node.entries.map(e => `${e.data}${e.mbr.toString()}`).join(', ');
      console.log(`${indent}叶子节点 [${entries}]`);
    } else {
      console.log(`${indent}非叶子节点`);
      node.entries.forEach(entry => {
        console.log(`${indent}  MBR: ${entry.mbr.toString()}`);
        this.printTreeStructure(entry.child, level + 2);
      });
    }
  }
  // 验证树的完整性
  validateTree(node) {
    if (!node) return true;
    // 检查节点条目数
    if (node !== this.tree.root && node.entries.length < Math.ceil(this.tree.maxEntries / 2)) {
      console.log("   ❌ 错误: 节点下溢!");
      return false;
    }
    if (node.entries.length > this.tree.maxEntries) {
      console.log("   ❌ 错误: 节点过载!");
      return false;
    }
    // 递归验证子节点
    if (!node.isLeaf) {
      for (let entry of node.entries) {
        if (!this.validateTree(entry.child)) {
          return false;
        }
      }
    }
    console.log("   ✅ 节点验证通过");
    return true;
  }
  // 验证剩余数据
  verifyRemainingData(expectedData) {
    console.log("   期望剩余数据:", expectedData);
    // 这里应该实现一个搜索所有数据的方法来验证
    // 简化版本：手动检查
    console.log("   实际树结构如上所示");
    let allValid = true;
    for (let data of expectedData) {
      // 检查每个期望的数据是否在树中
      const found = this.searchData(this.tree.root, data);
      if (!found) {
        console.log(`   ❌ 数据 ${data} 丢失!`);
        allValid = false;
      }
    }
    if (allValid) {
      console.log("   ✅ 所有期望数据都存在");
    }
  }
  // 搜索数据（简化实现）
  searchData(node, targetData) {
    if (node.isLeaf) {
      return node.entries.some(entry => entry.data === targetData);
    } else {
      for (let entry of node.entries) {
        if (this.searchData(entry.child, targetData)) {
          return true;
        }
      }
      return false;
    }
  }
}
// 运行测试
const test = new RTreeTest();
test.testDelete();

//=========插入查询验证逻辑=========//
//console.log("=== R树测试开始 ===");
//testRTree();
//console.log("=== R树测试结束 ===");
//RTreeEntry is not defined：没有定义；定义顺序不对//按依赖顺序定义所有类
// 1. 测试MBR类的函数
function testMBR() {
  console.log("🧪 测试MBR类基本功能...");
  const mbr1 = new MBR(1, 1, 3, 3);
  const mbr2 = new MBR(2, 2, 4, 4);
  console.log("MBR1 面积:", mbr1.area()); // 应该为4
  console.log("MBR2 面积:", mbr2.area()); // 应该为4
  console.log("是否重叠:", mbr1.overlaps(mbr2)); // 应该为true
  mbr1.extend(mbr2);
  console.log("扩展后MBR1:", `(${mbr1.minX},${mbr1.minY},${mbr1.maxX},${mbr1.maxY})`); // 应该为(1,1,4,4)
  console.log("扩展后面积:", mbr1.area()); // 应该为9
  console.log("✅ MBR测试完成\n");
}
// 在测试中使用
//console.log("=== 调试树状态 ===");//重复调用了两次 testRTree() ❌ 注释掉这行
//tree.debugTreeMBRs(); ❌ 注释掉这行
// 2. 测试R树的函数
function testRTree() {
    // 修复测试代码 - 确保 tree 变量存在
  console.log("🚀 开始测试R树插入逻辑...");
  const tree = new RTree(4);//✅ 这里定义了tree
  const testData = [
    { mbr: new MBR(1, 1, 1, 1), data: "点A" },
    { mbr: new MBR(2, 2, 2, 2), data: "点B" },
    { mbr: new MBR(3, 3, 3, 3), data: "点C" },
    { mbr: new MBR(4, 4, 4, 4), data: "点D" },
    { mbr: new MBR(5, 5, 5, 5), data: "点E" },
  ];
  console.log("\n📝 逐步插入测试数据：");
  for (let i = 0; i < testData.length; i++) {
    const { mbr, data } = testData[i];
    console.log(`\n--- 插入第${i + 1}个点: ${data} ---`);
    tree.insert(mbr, data);
    console.log(`插入 ${data} 后:`, {
      isLeaf: tree.root.isLeaf,
      entriesCount: tree.root.entries.length,
      mbr: tree.root.mbr ? `(${tree.root.mbr.minX},${tree.root.mbr.minY},${tree.root.mbr.maxX},${tree.root.mbr.maxY})` : "null"
    });
    if (i === 4) {
      console.log("🎯 第5个点应该触发分裂！");
      console.log("根节点条目数:", tree.root.entries.length);
      if (tree.root.entries.length > 1) {
        console.log("✅ 分裂成功！树高度增加了");
      }
    }
  }
  console.log("\n🔍 测试查询功能：");
  const query = new MBR(2, 2, 4, 4);
  const results = tree.search(query);
  console.log(`查询区域 (2,2,4,4) 的结果:`, results);
  return tree;//✅ 返回 tree 以便后续使用
}
console.log("=== R树测试开始 ===");
testRTree();// // ❌ 这里调用了，但没有保存返回值
testMBR() ;
console.log("=== R树测试结束 ===");
/// 运行测试的正确方式
console.log("=== R树测试开始 ===");
const tree = testRTree();  // ✅ 现在 tree 有定义了
testMBR();
// 调试树状态（现在 tree 已定义）
console.log("=== 调试树状态 ===");
if (tree) {
  // 在 RTree 类中添加这个调试方法
  tree.debugTreeMBRs();//  // ❌ 这个 tree 变量在第16行才定义
} else {
  console.log("tree 未定义");
}
console.log("=== R树测试结束 ===")
//节点MBR无效: Object { minX: 1, minY: 1, maxX: 6, maxY: 4 }这个 MBR 对象缺少方法，说明它不是 MBR 类的实例。
///⚠️ 节点下溢是"良性"错误：
//这个"节点下溢"错误实际上是测试程序检测到的，不是运行时错误。它说明：
//删除操作确实引起了节点下溢 - 这是预期的行为
//测试程序检测到了这个下溢 - 测试逻辑在工作
//但压缩树操作可能没有完全处理好 - 这是可以优化的地方
```
