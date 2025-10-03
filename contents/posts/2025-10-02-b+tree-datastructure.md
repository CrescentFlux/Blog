# b+ Tree
## 基础知识
- m阶B+树 = 每个节点最多m个子节点（每个节点最多m-1个关键字；阶数 = 最大子节点数）
- 叶子节点通过指针连接成有序链表；所有数据都在最底层
- 优势
```
范围查询 id BETWEEN num1 AND num2
更高的输出：内部节点不存数据，能存更多指针
稳定的性能：所有查询都要走到叶子节点
顺序访问：叶子链表支持高效范围查询
缓存友好：内部节点可以完全缓存在内存中
```
- 劣势
```
指针一致性：分裂/合并时要同时维护树结构和链表
并发控制：范围查询时如何防止链表被修改
内存管理：内部节点和叶子节点可能不同时在内存中
递归(简洁性)+链表(动态性)=指针管理的复杂性
```
- 比较

|特性|	B树|	B+树|
---|---|---
|数据存储|	所有节点都存数据|	只有叶子节点存数据|
|叶子节点|	没有特殊连接|	形成有序链表|
|内部节点|	存数据+指针|	只存索引指针|
|查询优势|	点查询快|	范围查询极快|
|磁盘io|随机跳转不同分支（磁盘不友好）|顺序读取叶子节点（磁盘友好）；磁盘预加载生效|
|缓存效率|数据分散在所有节点，缓存效果差|内部节点可以完全缓存在内存中|

## 注意事项
1. **混淆点**
- **结构**
```
B+树内部节点: [20, 40]  ← 内部节点导航（纯目录）
              /     \
B+树叶子节点: [20→30] [40→50]  ← 这些才存储实际数据
              ↓  ↓     ↓  ↓
             数据 数据  数据 数据
内部节点: (关键字, 子节点指针)
叶子节点: (关键字, 实际行数据, next指针)-内部节点的关键字用于导航，不是定义范围
```
- **内部节点和叶子节点区分**

|特性|内部节点|叶子节点|
---|---|---
|分裂提升值|提升的数字遵循floor()|提升：新叶子的第一个关键字数字遵守ceil()|
|数据|不保留所有关键字在内部层|所有数据保留在叶子层|
|使命|纯导航，快速定位叶子节点；分裂时保持导航效率；不需要维护链表|存储所有实际数据形成有序链表；支持范围查询；分裂时保持数据连续性|

- **叶子节点链表创造了最优的局部性**
```
空间局部性：相邻的数据在磁盘上相邻存储
时间局部性：连续访问的数据会被一起缓存
预测性：可以预加载下一个叶子节点
这正好匹配了磁盘的物理特性：顺序读取比随机读取快100倍
B+树的叶子节点链表为真实工作进行负载优化
```
- **叶子节点溢出（溢出 = 节点的关键字数量超过了B+树规定的上限）**
``` 
- 溢出后的处理：分裂   
分裂确保链表保持有序，让范围查询能够通过线性扫描高效完成
保证性能：
通过分裂溢出节点，确保：
    树高度保持最小
    每个节点大小适中（适合磁盘页）
    查询性能可预测
触发条件：关键字数 > order - 1
```
- **分裂规则**
```
-叶子节点
1.先插入：不管溢出，先按顺序插入（B+树叶子分裂中，新插入的关键字进入后半部分）
2.后分裂：按位置平均分配
-在B+树中，提升的是新叶子节点的第一个关键字：
    插入时：先按顺序插入，不管溢出
    分裂时：按位置平分关键字（不是找中间值）
    提升时：新右叶子的第一个关键字提升到父节点
    保持：所有数据都在叶子层，内部节点只存索引
-分裂只改变数据分布和链表结构
```
- **路由规则**
```
- 每个叶子节点实际上代表一个连续的值域范围：这个"范围"是隐式的，由节点的第一个和最后一个关键字定义
- 维护叶子链表（箭头的重要性）；分裂后必须更新链表指针：箭头重新连接，保持了整个值域的有序性！
- 内部节点的同步更新：内部节点需要知道新的范围边界
- 每个叶子节点的范围是由它的第一个关键字和下一个叶子节点的第一个关键字决定的
- 叶子节点的关键字就是实际存储的数据，范围查询是通过链表线性扫描实现的，不是通过值域判断！叶子节点不维护显式的范围值，范围查询完全依赖链表遍历和关键字比较
-B+树叶节点不存储范围信息
```
- **ceil策略**
```
-对于m阶B+树：
    最大关键字数 = m-1
    最小关键字数 = ⌈m/2⌉ - 1
ceil策略的智慧在于让左节点更满，从而减少未来的分裂；减少了立即再次分裂的概率确保左节点总是≥右节点；
-在实践中，B+树分裂通常：
    对于偶数个关键字：左右平分
    对于奇数个关键字：左节点多一个
```
- **B+树设计基本原则**
```
只在溢出时分裂
只在不足时合并
不主动做"优化合并
对不同层级的节点采用不同的分裂策略
```
- **B+树向上生长的机制**
```
在叶子节点插入 → 叶子溢出 → 分裂叶子
                          ↓
                    父节点接收新关键字
                          ↓  
                    父节点也可能溢出
                          ↓
                    分裂内部节点
                          ↓
                    可能一直传递到根节点
```
- **平行数组key和data必须同时删除**
```
索引:     0        1        2        3
keys:   [10,     20,      25,      30]
        ↓        ↓        ↓        ↓
data:   ['data10','data20','data25','data30']
```
- **内部节点存储的是路由边界，不是实际数据的精确副本**
```
根节点: [20, 40]
     ↓     ↓     ↓
[10,20] [25,30] [40,50]
注意这里删除10后根节点不会变化，因为路由仍然正确：内部节点存储的是子树的起始边界，不是精确的key副本
```
- **B+树的所有节点（叶子和内部）使用相同的minKeys计算**
```
对于阶数为m的B+树：
    所有节点的最小key数 = ceil(m/2) - 1
    只有叶子节点存储实际数据，但key数量的约束是一样的
所以删除节点即使是第一个关键字也不需要更新父节点
```
- **方法比较**

|特性	|findLeaf(key)|	getFirstLeaf()|
---|---|---
|路径|	动态（根据key）|	固定（总是最左）|
|参数|	需要key|	无参数|
|结果|	包含key的叶子|	最小key的叶子|
|核心能力|精确查找：定位|顺序扫描：找到起点|
|算法复杂度|O(log n)|o(n)|///
|用途|	点操作,插入操作,删除操作	|范围查询起点,全表扫描,导出所有数据|

```
 findLeaf(key) {//找到包含某个键的叶子节点
        let node = this.root;
        while (!node.isLeaf) {
            const i = node.findKey(key);
            node = node.children[i];  //动态路径：根据key值选择不同分支；高效导航：O(log n)时间找到目标；通用性：适用于查找、插入、删除
        }
        return node;
    } 
    getFirstLeaf() {
        let node = this.root;
        while (!node.isLeaf) {
            node = node.children[0];  //固定路径：总是走最左边简单可靠：不会走错路；范围查询基础：全表扫描的起点
        }
        return node;
    }
    // 全表扫描（像遍历链表）
    let current = tree.getFirstLeaf();
    while (current) {
            console.log("当前叶子:", current.keys);
            current = current.next;
    }
```
2. **代码实现**
```
//基本属性
class BPlusTreeNode {
    constructor(order, isLeaf) {
        this.order = order;
        this.keys = [];
        this.children = [];  // 内部节点使用
        this.data = [];      // 叶子节点使用
        this.isLeaf = isLeaf;
        this.parent = null;
        this.next = null;    // 叶子节点链表
    }
    // ========== 公开方法 ========== //
    findKey(key) {
        let i = 0;
        while (i < this.keys.length && key > this.keys[i]) {
           i++;
        }
        return i;
        
    }
    // 在BPlusTreeNode类中
isOverflow() {
    const maxKeys = this.isLeaf ? this.order - 1 : this.order - 1;
    console.log(`  检查溢出 - 节点: [${this.keys.join(', ')}], 最大允许: ${maxKeys}, 当前: ${this.keys.length}, 是否溢出: ${this.keys.length > maxKeys}`);
    return this.keys.length > maxKeys;
}
    isUnderflow() {
        const minKeys = Math.ceil(this.order / 2) - 1;
        return this.keys.length < minKeys;
    }
    canLend() {
        const minKeys = Math.ceil(this.order / 2) - 1;
        return this.keys.length > minKeys;
    }
}
class BPlusTree {
    constructor(order = 4) {
        if (order < 3) {
            throw new Error('B+树阶数必须至少为3');//内存中的B+树：order=4~10（平衡性能）
        }
        this.order = order;
        this.root = new BPlusTreeNode(order, true);
        this.size = 0;  // 确保有这行
    }
    // ========== 公开接口 ========== //
    insert(key, data) {
        const leaf = this._findLeaf(key);
        this._insertIntoLeaf(leaf, key, data);
        this.size++;  // 更新大小
        if (leaf.isOverflow()) {
            this._handleOverflow(leaf);
        }
    }
    delete(key) {
        const leaf = this._findLeaf(key);
        const deleted = this._deleteFromLeaf(leaf, key);
        this.size--;  // 更新大小
        if (!deleted) return false;
        if (leaf.isUnderflow()) {
            this._handleUnderflow(leaf);
        }
        this._adjustRoot();
        return true;
    }
    search(key) {
        const leaf = this._findLeaf(key);
        const index = leaf.findKey(key);
        if (index < leaf.keys.length && leaf.keys[index] === key) {
            return leaf.data[index];
        }
        return null;
    }
    rangeQuery(startKey, endKey) {
        const results = [];
        let currentLeaf = this._findLeaf(startKey);
        while (currentLeaf) {
            for (let i = 0; i < currentLeaf.keys.length; i++) {
                const key = currentLeaf.keys[i];
                if (key > endKey) return results;  // 超过范围，立即返回
                if (key >= startKey) {
                    results.push({
                        key: key,
                        data: currentLeaf.data[i]
                    });
                }
            }
            currentLeaf = currentLeaf.next;
        }
        return results;
    }
    paginatedScan(startKey, pageSize, excludeStartKey = false) {
        const results = [];
        let current = this._findLeaf(startKey);
        let count = 0;
        
        while (current && count < pageSize) {
            for (let i = 0; i < current.keys.length; i++) {
                if (count >= pageSize) break;
                
                const key = current.keys[i];
                if (key > startKey || (key === startKey && !excludeStartKey)) {
                    results.push({
                        key: key,
                        data: current.data[i]
                    });
                    count++;
                }
            }
            current = current.next;
        }
        return results;
    }
    getFirstLeaf() {
        let node = this.root;
        while (!node.isLeaf) {
            node = node.children[0];
        }
        return node;
    }
    getSize() {
        return this.size;
    }
    isEmpty() {
        return this.size === 0;
    }
    clear() {
        this.root = new BPlusTreeNode(this.order, true);
        this.size = 0;
    }
    printTree() {
        console.log("🌳 B+树结构:");
        this._printNode(this.root, 0);
    }
    //验证树结构是否正确
    validateTree() {
        console.log("🔍 验证树结构...");
        try {
            this._validateNode(this.root);
            console.log("✅ 树结构验证通过");
            return true;
        } catch (error) {
            console.error("❌ 树结构错误:", error.message);
            return false;
        }
    }
    // 在BPlusTree类中添加调试方法
debugFindLeaf(key) {
    console.log(`🔍 查找叶子过程 - 查找key: ${key}`);
    let node = this.root;
    let level = 0;
    while (!node.isLeaf) {
        console.log(`   层级 ${level}: 内部节点 [${node.keys.join(', ')}]`);
        const index = node.findKey(key);
        console.log(`   key ${key} 应该去索引 ${index} -> 子节点`);
        node = node.children[index];
        level++;
    }
    console.log(`   找到叶子节点: [${node.keys.join(', ')}]`);
    const leafIndex = node.findKey(key);
    console.log(`   在叶子中的位置: ${leafIndex}, 叶子keys[${leafIndex}]: ${node.keys[leafIndex]}`);
    return node;
}
    // ========== 内部方法 ========== //
    
   // _findLeaf(key) {
   //     let node = this.root;
      //  while (!node.isLeaf) {
      //      const index = node.findKey(key);
      //      node = node.children[index];
       // }
      //  return node;
   // }
    // 临时替换 _findLeaf 方法进行调试
    _findLeaf(key) {
            return this.debugFindLeaf(key);
    }
    _insertIntoLeaf(leaf, key, data) {
        const index = leaf.findKey(key);
        leaf.keys.splice(index, 0, key);
        leaf.data.splice(index, 0, data);
    }
    _deleteFromLeaf(leaf, key) {
        const index = leaf.findKey(key);
        if (index < leaf.keys.length && leaf.keys[index] === key) {
            leaf.keys.splice(index, 1);
            leaf.data.splice(index, 1);
            return true;
        }
        return false;
    }
    _handleOverflow(node) {
    console.log(`🔄 处理溢出 - 节点: [${node.keys.join(', ')}], 是否叶子: ${node.isLeaf}, 是否溢出: ${node.isOverflow()}`);
    let newNode, promotedKey;
    if (node.isLeaf) {
        console.log("   执行叶子分裂...");
        const result = this._splitLeaf(node);
        newNode = result.newLeaf;
        promotedKey = result.promotedKey;
        console.log(`   分裂结果 - 原节点: [${node.keys.join(', ')}], 新节点: [${newNode.keys.join(', ')}], 提升key: ${promotedKey}`);
        // 维护叶子链表
        newNode.next = node.next;
        node.next = newNode;
    } else {
        console.log("   执行内部节点分裂...");
        const result = this._splitInternal(node);
        newNode = result.newNode;
        promotedKey = result.promotedKey;
    }
    
    this._insertIntoParent(node, promotedKey, newNode);
}
    _splitLeaf(leaf) {
        const midIndex = Math.ceil(leaf.keys.length / 2);
        const newLeaf = new BPlusTreeNode(this.order, true);
        newLeaf.keys = leaf.keys.slice(midIndex);
        newLeaf.data = leaf.data.slice(midIndex);
        leaf.keys = leaf.keys.slice(0, midIndex);
        leaf.data = leaf.data.slice(0, midIndex);
        return {
            newLeaf: newLeaf,
            promotedKey: newLeaf.keys[0]
        };
    }
    _splitInternal(node) {
        const midIndex = Math.floor(node.keys.length / 2);
        const promotedKey = node.keys[midIndex];
        const newInternal = new BPlusTreeNode(this.order, false);
        const allKeys = node.keys.slice();
        const allChildren = node.children.slice();
        newInternal.keys = allKeys.slice(midIndex + 1);
        newInternal.children = allChildren.slice(midIndex + 1);
        node.keys = allKeys.slice(0, midIndex);
        node.children = allChildren.slice(0, midIndex + 1);
        newInternal.children.forEach(child => {
            child.parent = newInternal;
        });
        return {
            newNode: newInternal,
            promotedKey: promotedKey
        };
    }
    _insertIntoParent(left, promotedKey, right) {
        const parent = left.parent;
        if (!parent) {
            this._createNewRoot(left, promotedKey, right);
            return;
        }
        const index = parent.findKey(promotedKey);
        parent.keys.splice(index, 0, promotedKey);
        parent.children.splice(index + 1, 0, right);
        right.parent = parent;
        if (parent.isOverflow()) {
            this._handleOverflow(parent);
        }
    }
    _createNewRoot(left, promotedKey, right) {
        const newRoot = new BPlusTreeNode(this.order, false);
        newRoot.keys.push(promotedKey);
        newRoot.children.push(left, right);
        left.parent = newRoot;
        right.parent = newRoot;
        this.root = newRoot;
    }
    _handleUnderflow(node) {
        if (node === this.root || !node.isUnderflow()) {
            return;
        }
        const parent = node.parent;
        const nodeIndex = parent.children.indexOf(node);
        const leftSibling = parent.children[nodeIndex - 1];
        const rightSibling = parent.children[nodeIndex + 1];
        if (leftSibling && leftSibling.canLend()) {
            this._borrowFromLeft(node, leftSibling, parent, nodeIndex);
        } else if (rightSibling && rightSibling.canLend()) {
            this._borrowFromRight(node, rightSibling, parent, nodeIndex);
        } else if (leftSibling) {
            this._mergeNodes(leftSibling, node, parent, nodeIndex - 1);
        } else if (rightSibling) {
            this._mergeNodes(node, rightSibling, parent, nodeIndex);
        }
    }
    _borrowFromLeft(node, leftSibling, parent, nodeIndex) {
        if (node.isLeaf) {
            const borrowedKey = leftSibling.keys.pop();
            const borrowedData = leftSibling.data.pop();
            node.keys.unshift(borrowedKey);
            node.data.unshift(borrowedData);
            parent.keys[nodeIndex - 1] = node.keys[0];
        } else {
            // 内部节点借key逻辑
            const borrowedKey = leftSibling.keys.pop();
            const borrowedChild = leftSibling.children.pop();
            
            node.keys.unshift(parent.keys[nodeIndex - 1]);
            node.children.unshift(borrowedChild);
            borrowedChild.parent = node;
            
            parent.keys[nodeIndex - 1] = borrowedKey;
        }
    }
    _borrowFromRight(node, rightSibling, parent, nodeIndex) {
        if (node.isLeaf) {
            const borrowedKey = rightSibling.keys.shift();
            const borrowedData = rightSibling.data.shift();
            node.keys.push(borrowedKey);
            node.data.push(borrowedData);
            parent.keys[nodeIndex] = rightSibling.keys[0];
        } else {
            // 内部节点借key逻辑
            const borrowedKey = rightSibling.keys.shift();
            const borrowedChild = rightSibling.children.shift();
            node.keys.push(parent.keys[nodeIndex]);
            node.children.push(borrowedChild);
            borrowedChild.parent = node;
            parent.keys[nodeIndex] = borrowedKey;
        }
    }
    _mergeNodes(left, right, parent, keyIndex) {
        if (left.isLeaf) {
            left.keys.push(...right.keys);
            left.data.push(...right.data);
            left.next = right.next;
        } else {
            left.keys.push(parent.keys[keyIndex], ...right.keys);
            left.children.push(...right.children);
            
            right.children.forEach(child => {
                child.parent = left;
            });
        }
        parent.keys.splice(keyIndex, 1);
        parent.children.splice(keyIndex + 1, 1);
        if (parent.isUnderflow()) {
            this._handleUnderflow(parent);
        }
    }
    _adjustRoot() {
        if (this.root.keys.length === 0 && !this.root.isLeaf) {
            this.root = this.root.children[0];
            this.root.parent = null;
        }
    }
    _printNode(node, level) {
        const indent = "  ".repeat(level);
        const nodeType = node.isLeaf ? "叶子" : "内部"; 
        console.log(`${indent}${nodeType}节点: [${node.keys.join(', ')}]`);  
        if (!node.isLeaf) {
            node.children.forEach(child => {
                this._printNode(child, level + 1);
            });
        }
        // 如果是叶子节点，显示链表
        if (node.isLeaf && node.next) {
            console.log(`${indent}  下一个叶子: [${node.next.keys.join(', ')}]`);
        }
    }
     _validateNode(node) {
        if (!node) throw new Error("节点为空");
        // 检查关键字数量
        if (node.isLeaf) {
            if (node.keys.length !== node.data.length) {
                throw new Error("叶子节点keys和data长度不匹配");
            }
        } else {
            if (node.keys.length + 1 !== node.children.length) {
                throw new Error("内部节点keys和children数量不匹配");
            }
        }
        // 递归检查子节点
        if (!node.isLeaf) {
            node.children.forEach(child => {
                if (child.parent !== node) {
                    throw new Error("父子指针不一致");
                }
                this._validateNode(child);
            });}}
}
// 使用调试方法
const tree = new BPlusTree(4);
tree.insert(10, "A");
tree.insert(20, "B");
tree.insert(25, "C");
tree.insert(30, "D");
tree.printTree();
tree.validateTree();
//完整测试
// 在浏览器控制台运行这个完整测试
function comprehensiveTest() {
    console.log("🧪 开始全面测试 B+树");
    const tree = new BPlusTree(4);
    // 阶段1：插入测试数据
    console.log("\n📥 阶段1 - 插入测试");
    const testData = [
        [10, "A"], [20, "B"], [25, "C"], [30, "D"], 
        [35, "E"], [40, "F"], [45, "G"], [50, "H"]
    ];
    testData.forEach(([key, value]) => {
        tree.insert(key, value);
        console.log(`   插入 ${key} -> ${value}`);//size属性是否正确初始化或更新
    });
    tree.printTree();
    console.log("当前树大小:", tree.getSize());
    // 阶段2：搜索测试
    console.log("\n🔍 阶段2 - 搜索测试");
    const searchTests = [10, 25, 35, 99]; // 99是不存在的
    searchTests.forEach(key => {
        const result = tree.search(key);
        console.log(`   搜索 ${key}: ${result || "未找到"}`);//范围查询却能找到这些key，说明搜索逻辑有问题
    });
    // 阶段3：范围查询测试
    console.log("\n📊 阶段3 - 范围查询测试");
    console.log("   范围 [15, 40]:", tree.rangeQuery(15, 40).map(item => item.key));
    console.log("   范围 [25, 45]:", tree.rangeQuery(25, 45).map(item => item.key));
    console.log("   范围 [5, 15]:", tree.rangeQuery(5, 15).map(item => item.key)); 
    // 阶段4：删除测试
    console.log("\n🗑️ 阶段4 - 删除测试");
    const deleteTests = [25, 35, 10, 99]; // 99是不存在的
    deleteTests.forEach(key => {
        const success = tree.delete(key);
        console.log(`   删除 ${key}: ${success ? "成功" : "失败"}`);
        if (success) {
            tree.printTree();
            console.log(`   删除后搜索 ${key}:`, tree.search(key));
            console.log("   当前树大小:", tree.getSize());
            tree.validateTree();
        }
    });
    // 阶段5：删除后的范围查询
    console.log("\n📊 阶段5 - 删除后范围查询");
    console.log("   最终范围 [15, 40]:", tree.rangeQuery(15, 40).map(item => item.key));
    // 阶段6：分页查询测试
    console.log("\n📄 阶段6 - 分页查询测试");
    console.log("   第一页 [从10开始, 3条]:", tree.paginatedScan(10, 3).map(item => item.key));
    console.log("   第二页 [从20开始, 3条, 排除20]:", tree.paginatedScan(20, 3, true).map(item => item.key));
    console.log("\n✅ 全面测试完成");
    return tree;
}
// 运行测试
const testTree = comprehensiveTest();
function quickDiagnosis() {
    console.log("🔧 快速诊断");
    const tree = new BPlusTree(4);
    // 插入几个测试数据
    tree.insert(25, "TEST25");
    tree.insert(30, "TEST30");
    tree.insert(35, "TEST35"); 
    console.log("当前树:");
    tree.printTree();
    console.log("\n诊断搜索:");
    console.log("搜索25:", tree.search(25));
    console.log("搜索30:", tree.search(30)); 
    console.log("搜索35:", tree.search(35));
    console.log("\n诊断删除:");
    console.log("删除25:", tree.delete(25));
    console.log("删除后搜索25:", tree.search(25));
    
    console.log("树大小:", tree.getSize());
}
//快速测试分裂逻辑
quickDiagnosis();
function testSplitLogic() {
    console.log("🧪 测试分裂逻辑");
    const tree = new BPlusTree(4);
    
    console.log("插入数据观察分裂...");
    tree.insert(10, "A");
    tree.insert(20, "B"); 
    tree.insert(25, "C");
    console.log("插入25后树结构:");
    tree.printTree();
    
    tree.insert(30, "D");
    console.log("插入30后树结构:");
    tree.printTree();
    
    tree.insert(35, "E");
    console.log("插入35后树结构:"); 
    tree.printTree();
}
testSplitLogic();
//🧪 测试第4次插入是否会分裂
function testFourthInsertion() {
    console.log("🧪 测试第4次插入是否会分裂");
    const tree = new BPlusTree(4);
    tree.insert(25, "A");
    tree.insert(30, "B");
    tree.insert(35, "C");
    console.log("插入3个key后:");
    tree.printTree();
    tree.insert(40, "D");
    console.log("插入第4个key后:");
    tree.printTree();
}
testFourthInsertion();
```
```
//----范围查询逻辑----//
//查找具体的范围
rangeQuery(startKey, endKey) {
    const results = [];
    // 1. 找到包含startKey的叶子节点
    let currentLeaf = this.findLeaf(startKey);
    // 2. 沿着叶子链表扫描
    rangeQuery(startKey, endKey, options = {}) {
    const { includeStart = true, includeEnd = true } = options;
    const results = [];
    let currentLeaf = this._findLeaf(startKey);
    while (currentLeaf) {
        for (let i = 0; i < currentLeaf.keys.length; i++) {
            const key = currentLeaf.keys[i];
            // 1.定义四种不符合条件的情况
            const excludeForStart = 
                (includeStart && key < startKey) ||     
                (!includeStart && key <= startKey);    
            const excludeForEnd = 
                (includeEnd && key > endKey) ||       
                (!includeEnd && key >= endKey);         
            // 2.如果符合任何一种排除条件，就跳过
            if (excludeForStart || excludeForEnd) {
                continue; // 跳过这个key，继续遍历下一个
            }
            // 3.剩下的就是符合条件的key
            results.push({ key, data: currentLeaf.data[i] });
        }
        currentLeaf = currentLeaf.next;
    }
    return results;
}}
//分页查询
paginatedScan(startKey, pageSize, excludeStartKey = false) {
    const results = [];
    let current = this.findLeaf(startKey);
    let count = 0;
    while (current && count < pageSize) {
        for (let i = 0; i < current.keys.length; i++) {
            if (count >= pageSize) break;
            const key = current.keys[i];
            // 关键判断：是否应该包含这个key
            // 可以遍历的情况大于起始值或者等于起始值且本身包含起始值
            if (key > startKey || (key === startKey && !excludeStartKey)) {
                results.push({ key, data: current.data[i] });
                count++;
            }
        }
        current = current.next;
    }
    return results;
}
```
```
//-----删除逻辑-----//
delete(key) {
    // 1. 精确定位
    const leaf = this.findLeaf(key);
    const keyIndex = leaf.findKey(key);
    //没有关键字的情况
     if (keyIndex === -1 || leaf.keys[keyIndex] !== key) {
        return false; // 键不存在
    }
    // 2. 执行删除
    leaf.keys.splice(keyIndex, 1);//在这个正确的索引位置删除一个元素
    leaf.data.splice(keyIndex, 1);//keys 和 data 是平行数组,必须同时删除
    // 如果根节点为空，让唯一子节点成为新根
    if (this.root.keys.length === 0) { 
    this.root = this.root.children[0];
    this.root.parent = null;
//在B+树中，内部节点的key只是路由信息，不需要因为叶子节点的删除而立即更新；B+树删除的一个重要特性：内部节点存储的是路由边界，不是实际数据的精确副本
    // 3. 检查是否有下溢的问题（下溢=节点的关键字数量少于B+树规定的最小值）
    if (leaf.isUnderflow() && leaf !== this.root) {
        this.handleLeafUnderflow(leaf);// 处理节点的下溢
    }
}
}
//下溢处理过程：
handleLeafUnderflow(leaf) {
    const parent = leaf.parent;
    const leafIndex = parent.children.indexOf(leaf);
    // 1. 尝试获得左子树叶子节点中的关键字
    if (leafIndex > 0) {
        //2.获取左兄弟节点
        const leftSibling = parent.children[leafIndex - 1];
        //3.检查左兄弟关键字是否多余
        if (leftSibling.canLend()) {
            this._borrowFromLeft(leaf, leftSibling);
            return;
        }
    }
    // 2. 尝试获得右子树叶子节点的关键字
    if (leafIndex < parent.children.length - 1) {
        //1.检查是否存在右兄弟节点
        const rightSibling = parent.children[leafIndex + 1];
        if (rightSibling.canLend()) {
            this._borrowFromRight(leaf, rightSibling);
            return;
        }
    }
    // 3. 如果左右子树的叶子节点都无法获得新的关键字，必须删除合并为新的链表结构
    //当无法从左右子树借key时，选择与一个子树合并；优先与左兄弟合并，如果没有左兄弟才与右兄弟合并。
    if (leafIndex > 0) {
        this.mergeLeaves(parent.children[leafIndex - 1], leaf);
        //将当前叶子节点与其左兄弟节点合并：parent.children[leafIndex - 1] = 左兄弟节点；leaf=当前节点（发生下溢的节点）
    } else {
        this._mergeLeaves(leaf, parent.children[leafIndex + 1]);
    }
}
//内部方法
_borrowFromLeft(node, leftSibling, parent, nodeIndex) {
    //node: 当前发生下溢的节点（需要借key的节点）
    //leftSibling: 当前节点的左兄弟节点（可以提供key的节点）
    //parent: 当前节点的父节点（需要更新路由key）
    //nodeIndex: 当前节点在父节点children数组中的索引位置
    if (node.isLeaf) {
        // 1.叶子节点从左兄弟借key：借最后一个key
        const borrowedKey = leftSibling.keys.shift();
        const borrowedData = leftSibling.data.shift();
        // 2.将借来的key插入到当前节点的开头
        node.keys.unshift(borrowedKey);
        node.data.unshift(borrowedData);
        // 3.更新父节点的路由key
        parent.keys[nodeIndex-1] = node.keys[0];//左节点借出去的一个数字是右节点的第一个值同时是它本身被分隔为关键key
    } else {
         // 1.内部节点从左兄弟借key
        const borrowedKey = leftSibling.keys.shift();       // 借左兄弟的最后一个key
        const borrowedChild = leftSibling.children.shift(); // 借对应的child
        // 2.将父节点的分隔key下移到当前节点末尾
        node.keys.push(parent.keys[nodeIndex-1]);
        // 3.将借来的child插入到当前节点开头
        node.children.push(borrowedChild);
        // 4.让内部节点指向已经更新的子节点
        borrowedChild.parent = node;  
        // 5.用借来的key更新父节点的分隔key
        parent.keys[nodeIndex-1] = borrowedKey;
    }
}
_borrowFromRight(node, rightSibling, parent, nodeIndex) {
    if (node.isLeaf) {
        // 1.叶子节点从右兄弟借key：借第一个key
        const borrowedKey = rightSibling.keys.shift();
        const borrowedData = rightSibling.data.shift();
        // 2.将借来的key插入到当前节点的末尾
        node.keys.push(borrowedKey);
        node.data.push(borrowedData);
        // 3.更新父节点的路由key（右兄弟的新第一个key）
        parent.keys[nodeIndex] = rightSibling.keys[0];
    } else {
        // 1.内部节点从右兄弟借key
        const borrowedKey = rightSibling.keys.shift();       // 借右兄弟的第一个key
        const borrowedChild = rightSibling.children.shift(); // 借对应的child
        // 2.将父节点的分隔key下移到当前节点末尾
        node.keys.push(parent.keys[nodeIndex]);
        // 3.将借来的child插入到当前节点末尾
        node.children.push(borrowedChild);
        // 4.让内部节点指向已经更新的子节点
        borrowedChild.parent = node;  
        // 5.用借来的key更新父节点的分隔key
        parent.keys[nodeIndex] = borrowedKey;
    }}

_mergeLeaves(left, right, parent, keyIndex) {
    if (left.isLeaf) {
        // 叶子节点合并逻辑...
    } else {
        // 1.内部节点合并(分别加入加入父节点的分隔key，再加入右节点的keys)
        left.keys.push(parent.keys[keyIndex], ...right.keys);
        // 2.右节点的字节点也要同时push
        left.children.push(...right.children);
        // 3.更新所有右节点children的父指针
        right.children.forEach(child => {
            child.parent = left;
        });
        // 4.从父节点删除对应的key和child
        parent.keys.splice(keyIndex, 1);// 删除父节点位置的key
        parent.children.splice(keyIndex + 1, 1); //删除的是被合并的空的内部节点
    }
}
```
```
//----插入逻辑----//
insert(key, data) {
    // 1. 找到应该插入的叶子节点// 找到关键字所在的位置
    const leaf = this._findLeaf(key);//找到关键字所在的叶子位置
    //概念区分： const keyIndex = leaf.findKey(key);//扎到关键字所在叶子中具体的索引值位置
    // 2. 在叶子节点中插入数据
    leaf.insertKey(key, data);
    // 3. 如果叶子节点溢出
    if (leaf.isOverflow()) {
        //判断是否叶子的关键字是否太多
        //1.惰性平衡策略：不是预防性而是反应性(等真的溢出了再分裂)2.作用：减少不必要的分裂；提高空间利用率；符合"不要过早优化"的原则
        //不预防：允许节点处于半满状态；不优化：不主动合并半空节点；只应对：只在违反约束时采取行动
        const newLeaf = this._splitLeaf(leaf);
        // 明确提取要提升的key
        const promotedKey = newLeaf.keys[0];
        // 1.更新叶子节点链表指针指向
        newLeaf.next = leaf.next; // 新叶子指向原叶子的下一个
        leaf.next =newLeaf; // 原叶子指向新叶子
        //2.只调用一次 insertIntoParent更新父节点
        this.insertIntoParent(leaf,promotedKey, newLeaf);
    // 4. 更新根节点（如果需要）
    //当根节点溢出时，不能像普通节点那样直接分裂，因为根节点没有父节点。需要特殊处理来创建新的根节点。
    //内部节点分裂逻辑已经包含了创建新根的情况根节点分裂本质上就是内部节点分裂 + 父节点为空的特殊情况这样可以减少代码重复
    if (this.root.isOverflow()) {
        const newRoot = this._splitRoot();
        this.root = newRoot;
    }
}}
//--叶子节点分裂：不提升数据关键字，只提升导航关键字
//内部私有方法，不应该被外部直接调用
_splitLeaf(leaf) {//叶子进行分裂
    const midIndex = Math.ceil(leaf.keys.length / 2);//向上取整，确保左节点的数量大于等于右节点的数量减少频繁分裂次数的概率
    const newLeaf = new BPlusTreeNode(this.order, true);//创建新叶子放被分裂出来的节点数据
    // 新叶子获得后半部分
    newLeaf.keys = leaf.keys.slice(midIndex);//从数组的midIndex位置开始，截取到数组的末尾，不包含midindex
    newLeaf.data = leaf.data.slice(midIndex);//从数组索引midIndex开始，截取到末尾位置
    // 原叶子保留前半部分
    leaf.keys = leaf.keys.slice(0, midIndex);//从数组的0位置开始，截取到数组的midIndex
    leaf.data = leaf.data.slice(0, midIndex);//从数组索引0开始，截取到midIndex位置（不包括 midIndex）
    //注意这里除了返回分好段的的区间外还要返回新的父节点的key值，确保上升的key值是新节点是新叶子的第一个关键字
    return {
        newLeaf: newLeaf,
        promotedKey: newLeaf.keys[0]//相当于const promotedKey = newLeaf.keys[0];
    }
}
//--父节点更新逻辑
_insertIntoParent(left, promotedkey, right) {//父节点更新
    const parent = left.parent;
    if (!parent) {//根节点为空：
        // 创建新根节点
        const newRoot = new BPlusTreeNode(this.order, false);
        newRoot.keys.push(promotekey); // 提升的关键字
        newRoot.children.push(left, right);//更新字节点指针
        // 更新父指针
        left.parent = newRoot;
        right.parent = newRoot;
        // 更新树根
        this.root = newRoot;
        return; // 重要：创建新根后直接返回
    }
    else {// 不是根节点：
        const index = parent.findKey(promotekey);
        //1.找到在父节点中插入新关键字的正确位置的索引值；
        parent.keys.splice(index, 0, key);
        //2.在找到的父节点中的正确位置插入新的上升关键字；
        parent.children.splice(index + 1, 0, right);//父节点插入位置索引值为0,它对应的右指针应该在索引1位置；
        //3.在children数组的index+1位置插入right指针；增加从父节点指向子节点的指针；
        right.parent = parent;
        //4.设置新叶子节点的父指针
        if (parent.isOverflow()) {
        //5.检查父节点是否溢出//检查父节点是否需要分裂
            this.splitInternal(parent); //分裂内部节点
        }
    }}
//--内部节点分裂插入逻辑
//内部节点分裂：要提升一个导航关键字；
splitInternal(node) {
    const midIndex = Math.floor(node.keys.length/2);//1.找到向下取整提升中间关键字
    const newInternal = new BPlusTreeNode(this.order, false);//2.创建新的内部节点来存放分裂后的后半部分keys和children它代表了内部节点分裂后产生的新内部节点；promotedKey不属于任何节点，会被插入到祖父节点；
    //3.提升的关键字处理（B+树的精妙之处）
    const promoteKey = node.keys[midindex];
    //4.新内部节点获得后半部分（注意：不包含提升的关键字）
    newInternal.keys = node.keys.slice(midindex+1);//从midindex+1取到末尾
    newInternal.children = node.children.slice(midindex+1);//children的划分完全跟随keys的划分从midindex+1取到末尾；路由规则
    //5.原内部节点保留前半部分
    node.keys = node.keys.slice(0, midIndex);//从0取到midindex,不包含midindex
    node.children = node.children.slice(0, midindex+1);//从0取到midindex+1,不包含midindex+1;
    //6. 更新父指针//
    newInternal.children.forEach(child => child.parent = newInternal);//6.1.更新子节点原本指向内部节点的所有指针
    //6.1.遍历新内部节点的所有子节点，把每个子节点的parent指针指向新内部节点
    //左右子树分类规则：叶子节点的分配是由key的范围决定的：路由规则：每个key都能根据路由规则找到正确的子树
    //当内部节点分裂后，新内部节点newInternal的所有子节点都需要更新父指针，指向这个新父节点
    this._insertIntoParent(node, promoteKey, newInternal);//递归向上插入
    //6.2.让新内部节点 newInternal 被它的父节点（祖父节点）指针指着
    //将分裂产生的提升key和新内部节点插入到祖父节点中，完成分裂的向上传播
}


//splice(start, deleteCount, item1, item2, ...) 三个参数：//
    start：开始位置
    deleteCount：要删除的元素数量
    item1, item2...：要插入的元素
parent.keys.splice(index, 0, key)的意思是：在位置index处，删除0个元素，插入key


//----_splitRoot()逻辑重复的简化方法----//
insert(key, data){
    const leaf = this._findLeaf(key);
    leaf.insertKey(key, data);
    // 只需要这一行！所有分裂都会自动向上传播到根节点//只需要检查一次，分裂会自动传播
    if (leaf.isOverflow()) {
        this._handleOverflow(leaf);
    }
}
_splitLeaf(leaf){//叶子
    const midIndex = Math.ceil(leaf.keys.length/2);
    const newLeaf = new BPlusTreeNode(this.order, true); 
    //先保存再修改
    const allKeys = leaf.keys.slice();
    const allData = leaf.data.slice();
    newLeaf.keys = allKeys.slice(midIndex);
    newLeaf.data = allData.slice(midIndex);
    leaf.keys = allKeys.slice(0, midIndex);
    leaf.data = allData.slice(0, midIndex);
    return {
        newLeaf: newLeaf,
        promotedKey: newLeaf.keys[0]
    };
}
_splitInternal(node) {//内部节点
    const midIndex = Math.floor(node.keys.length/2);
    const promotedKey = node.keys[midIndex];
    const newInternal = new BPlusTreeNode(this.order, false);
    // 关键：先保存原数据！
    const allKeys = node.keys.slice();
    const allChildren = node.children.slice();
    // keys的分裂：midIndex位置的key被提升，所以两边都不包含它
    node.keys = node.keys.slice(0, midIndex);// 原节点保留0到midIndex
    newInternal.keys = node.keys.slice(midIndex + 1); // 新节点获得 [midIndex+1, 结尾]
    // children的分裂：midIndex位置的key对应右边的child，所以需要特殊处理
    node.children = node.children.slice(0, midIndex + 1);// 原节点保留 [0, midIndex+1]
    newInternal.children = node.children.slice(midIndex + 1); // 新节点获得 [midIndex+1, 结尾]
    // 关键：更新新内部节点所有子节点的父指针
    newInternal.children.forEach(child => {
        child.parent = newInternal;
    });
    return { newNode: newInternal, promotedKey };
}
_insertIntoParent(left, promotedKey, right) {
    const parent = left.parent;
    if (!parent) {
        // 创建新根
        const newRoot = new BPlusTreeNode(this.order, false);
        newRoot.keys.push(promotedKey);
        newRoot.children.push(left, right);
        left.parent = right.parent = newRoot;
        this.root = newRoot;
        return;
    }
    // 在父节点中插入
    const index = parent._findInsertIndex(promotedKey);
    parent.keys.splice(index, 0, promotedKey);
    parent.children.splice(index + 1, 0, right);
    right.parent = parent;
    // 关键：递归处理父节点溢出
    if (parent.isOverflow()) {
        this._handleOverflowFromInternal(parent);
    }
}
_handleOverflow(node) {//合并逻辑
    let newNode, promotedKey;
    if (node.isLeaf) {
        // 叶子节点分裂
        const result = this._splitLeaf(node);
        newNode = result.newLeaf;
        promotedKey = result.promotedKey;
        // 叶子节点的特殊逻辑：维护链表
        newNode.next = node.next;
        node.next = newNode;
    } else {
        // 内部节点分裂
        const result = this._splitInternal(node);
        newNode = result.newNode;
        promotedKey = result.promotedKey;
    }
    // 统一向上传播分裂
    this._insertIntoParent(node, promotedKey, newNode);
}
```