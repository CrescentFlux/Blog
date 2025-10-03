# B Tree
## 基础知识
- B树是一种多叉搜索树，每个节点可以有多个子节点，主要用于数据库存储系统
- 对于m阶B树：B树的"阶数"m表示每个节点最多有m个子节点，最多有m-1个关键字
- B树的所有叶子节点都在最底层，这是保持平衡的关键
- 对比

|特性	|红黑树|	B树|
---|---|---
|设计目标	|内存操作优化	|磁盘IO优化|
|节点大小	|很小（几个指针）|	约4KB（一磁盘页）|
|适用场景	|内存数据结构	|数据库、文件系统|
|子节点数量|二叉树每个节点最多2个|多叉树每个节点可以有多个子节点|



## 注意事项
### **关键字数**
- 关键字数(k)=最大子节点数(m)-1
- 每个节点有"容量限制"
- 关键字数和区间数：k个关键字产生(k+1)个区间，需要(k+1)个子节点；子节点就像不同的区域
- 结构
```
每个关键字分隔两个子树的取值范围
节点：[key1, key2, key3]  ← 3个关键字
子节点：C0   C1   C2   C3  ← 4个子节点
key1分隔：C0 < key1 < C1
key2分隔：C1 < key2 < C2  
key3分隔：C2 < key3 < C3
m子节点数 = 关键字数k + 1
最大子节点数m = 最大关键字数k + 1
最大关键字数k = m - 1
```
- 分隔点动态构建
```
B树通过插入过程中的自动选择来动态确定这些分隔点;
初始状态：不知道哪些是关键点
插入数据：数据自然聚集在节点中
节点饱和：当节点装满时，数据分布本身告诉我们哪里是关键分隔点
分裂提升：中间关键字天然就是好的分隔点:中间关键字能最均衡地分割数据
B树不需要预先知道数据的任何信息，而是通过一种简单的分裂规则，让最优结构从数据中自然涌现出来
```
### **阶数Order**
- 阶数m = 每个节点最多允许的子节点数（设计约束）=最大字节点数
- 本质是把物理限制转换成算法参数
- 每个节点大小 = (关键字大小×关键字数)+(指针大小×子节点数)
- 节点内存布局：每个键占4字节；每个指针占8字节；
- 节点大小可以反向得出关键字的数量；假设有k个关键字，节点大小=k×4+(k+1)×8::每个节点最多容纳340个关键字（k ≤ 340）所以就是341阶b树
- 比较

|特性|	阶数m	|分支因子b|
---|---|---
|含义|	最大允许值|	实际分析值|
|用途|	设计约束|	性能分析|
|数值|	固定值|	b = ⌈m/2⌉（最坏情况）|
|保证|	节点不会超过m个子节点	|树高度不会超过log_b(N)|

### **分支因子Branching Factor**
- 分支因子b = 实际有效子节点数（分析参数）=> 用于计算树高度
- b = ⌈m/2⌉
- 注意这里是向上取整有效防止了最坏情况链表的发生确保了性能正常;即使在最坏情况下，也不会超过log_m(N)次IO
- 当数学的连续性遇到物理的离散性时，工程要做出有利于系统稳定性的选择分支因子
- m ≈ B / (K + P) {页大小：B bytes；关键字大小：K bytes指针大小：P bytes}
- 树高度:
```
磁盘页大小 → 决定最大m值 → 影响树高度
阶数m（越大越好，但受磁盘页限制）
节点容量越大，树高度越矮
数据总量N:b = 分支因子=每个节点的子节点数
要存储N个数据：b^h ≥ N → h ≥ log_b(N)
```
- 二分查找
```
-二分查找：逻辑上的二叉树，每次比较需要计算中间位置
-对于一个有序数组，二分查找的时间复杂度应该是o(logn);无序数组顺序扫描O(n)
-直接把这种树结构显式地存储起来，并优化为多叉树来适应磁盘特性：减少树高度，减少IO次数
-二分查找比较的次数 = 隐形二叉树的高度
-二分查找的决策逻辑：遍历一棵隐式的二叉树
-显式二叉树：节点之间有明确的指针连接;隐式二叉树：没有实际的节点对象，但逻辑上存在树结构
-二叉树高度 = log₂(n)；二分查找最多需要比较次数 = 树高度；所以时间复杂度 = O(log n)
```
### 其他
1. 优势
- 保持平衡：自动平衡机制：中间关键字提升后，左右子树大小基本相等
```
-所有叶子节点都在同一层；节点太满时会分裂；太小时会合并
-高效处理海量随机数据
-平衡性保证最坏情况下的IO次数可控
```
- 保持有序：左子树 < 中间关键字 < 右子树
- 效率最优：每次分裂都能最大程度利用节点空间
- 控制节点大小(节点不会越来越大)
- 磁盘IO优化（B树的核心目标是减少磁盘IO）
```
-磁盘IO：从硬盘读取数据到内存的操作
-节点大小≈磁盘页：一次IO读取整个节点;磁盘的物理属性决定了节点的大小和数量
-内存访问：约100纳秒
-磁盘访问：约10毫秒 = 10,000,000纳秒
-磁盘读取的单位是"页"（通常4KB）
-无论读取1个字节还是4KB，磁盘IO时间几乎相同所以一次IO应该读取尽量多的有用数据
-节点A（5.2KB） → 第一次IO读4KB不完整;第二次IO读剩下的1.2KB（效率低下）
-对于N个关键字，如何设计树结构，使得最坏情况下的磁盘IO次数最少：假设有k各关键字---得到关键字的取值范围
```
```
数据库系统的可靠性要求：
-原子性：每次IO必须完整读取一个节点
-一致性：节点数据必须完整无误
-性能：避免多次IO读取同一个节点
如果节点超过页大小，会破坏所有这些保证
节点大小 ≤ 磁盘页大小
```
- 节点大小固定≈磁盘页大小，确保每次读取效率一致
- 无论插入顺序如何，B树都能自动保持平衡B树都会自动调整成平衡结构
- 多路分支（直接把这种树结构显式地存储起来，并优化为多叉树来适应磁盘特性）
```
二分查找 vs 多路查找
B树通过插入时的分裂规则，自动把"二分查找过程中会访问的中间点"提前提取出来，组织成显式的索引结构
```
- B树：物理存储的树结构，直接存储分隔点，一次读取多个比较信息(局部性原理：相关数据在同一个节点，一次IO读取多个关键字)

2. B树关键字排序：关键字有序分隔
```
节点结构：[key1, key2]  
子节点：   C0   C1   C2
C0中的关键字 < key1
C1中的关键字在 key1 和 key2 之间  
C2中的关键字 > key2
```
3. 分裂规则
```
第1步：找中间位置
第2步：根据索引的位置找到中间关键字然后提升中间关键字(注意中间关键索引位置floor(index/2)(数组的中间索引)的规则是向下取整)
第3步：分裂成两个子节点
关键规则：总是提升中间索引的关键字到父节点，剩下的平分给两个子节点
```
4. 四大核心定理
```
定理1：多路平衡定理
"通过适当选择分支因子m，可以在常数层数内存储任意大规模数据集"
定理2：IO复杂度定理
"B树的搜索、插入、删除操作的时间复杂度为O(log_m N)，其中磁盘IO次数为O(log_m N)"
定理3：自平衡定理
"通过节点分裂与合并操作，B树能在动态更新中自动保持平衡"
定理4：空间利用率定理
"B树的空间利用率始终保持在50%以上
数据结构应该适应底层硬件特性
不同的存储层次需要不同的优化策略
```

5. b树本身
- 层次结构
```
根节点（level 0）
    |
内部节点（level 1）← 这里的子节点可能还有子节点！// 只有内部节点才有子节点
    |
叶子节点（level 2）
```
- 处理子节点
```
-B树分裂的核心原则：保持关键字与子节点的对应关系；每个关键字都充当"分隔符"的角色；
-因为B树的分裂必须是完整的子树分裂，而不仅仅是关键字的分裂
当分裂一个内部节点时，我们需要：
    分裂关键字
    重新分配子节点（关键！）
    保持树结构的完整性
如果不处理子节点，分裂后的节点就无法正确指向下一层，树结构就断裂
-原节点的子节点公平分配给两个新节点，保持树的连通性
```
```
通用的分配公式：保证平衡分配，无论k是奇数还是偶数
midIndex = floor(k/2)
左节点:
- 关键字数 = midIndex
- 子节点数 = midIndex + 1
右节点:  
- 关键字数 = k - midIndex - 1
- 子节点数 = k - midIndex
```

- 向上生长规律
```
B树是递归结构：
根节点有子节点（第一层子节点）
子节点可能还有自己的子节点（第二层，即"孩子的孩子"）
```
- 切片原理
```
左节点 = keys[0 到 midIndex-1]      // 中间关键字之前的部分
提升关键字 = keys[midIndex]          // 正中间的关键字  
右节点 = keys[midIndex+1 到 最后]    // 中间关键字之后的部分
```
- 合并子节点引用
```
    保持树结构完整
    维持B树性质：内部节点的子节点数量必须等于键数量+1
    避免内存泄漏：右子节点将被删除，必须转移其所有子节点
如果我们要合并的节点是内部节点（不是叶子节点），那么它们有子节点引用需要一起合并，否则会破坏树的结构
B树删除操作中的预防性加强，确保在递归删除前子节点有足够的键
```
- 对比
```
B树：预防性策略（防止变空）
// B树的逻辑：在变空之前预防
if (node.children[i].keys.length <= this.MIN_KEYS) {  // 快要变空了！
    this._fillChild(node, i);  // 赶紧加强
}
return this.delete(key, node.children[i]);  // 现在安全了
```

```
B+树：修复性策略(变空后修复)
// B+树的典型逻辑：先删除，如果变空了再修复
let deleted = this._deleteFromNode(node, key);
if (node.keys.length < this.MIN_KEYS) {  // 已经变空了！
    this._handleUnderflow(node);  // 赶紧修复
}
```
### 代码实现
```
class BTreeNode {
    constructor(order) {
        this.order = order;        // B树的阶数
        this.keys = [];           // 存储关键字的数组
        this.children = [];       // 存储子节点的数组
        this.isLeaf = true;       // 是否是叶子节点
    }
    
    // 判断节点是否已满
    isFull() {
        return this.keys.length >= this.order - 1;
    }
    
    // 关键字查找
    findKey(key) {
        let i = 0;
        while (i < this.keys.length && key > this.keys[i]) {
            i++;
        }
        return i;
    }
}

class BTree {
    constructor(order = 3) {
        this.order = order;
        this.MIN_KEYS = Math.ceil(order / 2) - 1;  // 最小键数
        this.root = new BTreeNode(order);
    }

    // ==================== 公共接口 ====================
    
    /**
     * 插入关键字
     * @param {number} key - 要插入的关键字
     */
    insert(key) {
        this._insert(key);
    }
    
    /**
     * 删除关键字
     * @param {number} key - 要删除的关键字
     * @returns {boolean} 是否删除成功
     */
    delete(key) {
        return this._delete(key);
    }
    
    /**
     * 查找关键字
     * @param {number} key - 要查找的关键字
     * @returns {boolean} 是否存在
     */
    search(key) {
        return this._search(key, this.root);
    }
    
    /**
     * 获取B树的高度
     * @returns {number} 树的高度
     */
    getHeight() {
        return this._getHeight(this.root);
    }
    
    /**
     * 打印B树结构（用于调试）
     */
    print() {
        this._printTree(this.root, 0);
    }
    // 在BTree类中添加调试方法
debugInsert(key) {
    console.log(`\n=== 插入 ${key} ===`);
    this.insert(key);
    this.print();
}

debugDelete(key) {
    console.log(`\n=== 删除 ${key} ===`);
    const result = this.delete(key);
    console.log(`删除结果: ${result}`);
    this.print();
    return result;
}
// 在BTree类中添加深度调试方法
debugDetailedInsert(key) {
    console.log(`\n🔍 === 详细插入 ${key} ===`);
    console.log("插入前树结构:");
    this._printTree(this.root, 0);
    
    this._insert(key);
    
    console.log("插入后树结构:");
    this._printTree(this.root, 0);
    console.log("=== 插入完成 ===\n");
}

// 修改验证方法，提供更多信息
_validateNode(node, level = 0, path = "root") {
    console.log(`验证: ${path} [${node.keys}] isLeaf:${node.isLeaf} children:${node.children.length}`);
    
    if (node.isLeaf && node.children.length > 0) {
        throw new Error(`叶子节点 ${path} 有子节点: [${node.keys}]`);
    }
    if (!node.isLeaf && node.children.length === 0) {
        throw new Error(`内部节点 ${path} 没有子节点: [${node.keys}]`);
    }
    if (node.keys.length > this.order - 1) {
        throw new Error(`节点 ${path} 键数超出限制: [${node.keys}]`);
    }
    if (node !== this.root && node.keys.length < this.MIN_KEYS) {
        throw new Error(`🚨 节点 ${path} 键数过少: [${node.keys}] level:${level}`);
    }
    
    // 内部节点的子节点数量应该是 keys.length + 1
    if (!node.isLeaf && node.children.length !== node.keys.length + 1) {
        throw new Error(`内部节点 ${path} 子节点数量错误: keys=${node.keys.length} children=${node.children.length}`);
    }
    
    // 递归验证子节点
    if (!node.isLeaf) {
        for (let i = 0; i < node.children.length; i++) {
            this._validateNode(node.children[i], level + 1, `${path}.children[${i}]`);
        }
    }
}

    // ==================== 内部方法 ====================

    /**
     * 内部插入方法
     */
    _insert(key) {
    if (this._search(key, this.root)) {
        console.log(`⚠️ 键 ${key} 已存在，跳过插入`);
        return;
    }
    
    this._insertRecursive(this.root, key);
    
    // 检查根节点是否需要分裂
    if (this.root.keys.length > this.order - 1) {
        const newRoot = new BTreeNode(this.order);
        newRoot.isLeaf = false;
        newRoot.children.push(this.root);
        this._splitChild(newRoot, 0, this.root);
        this.root = newRoot;
    }
}

_insertRecursive(node, key) {
    let i = node.findKey(key);
    
    if (node.isLeaf) {
        node.keys.splice(i, 0, key);
    } else {
        this._insertRecursive(node.children[i], key);
        
        // 插入后检查子节点是否需要分裂
        if (node.children[i].keys.length > this.order - 1) {
            this._splitChild(node, i, node.children[i]);
        }
    }
}

    /**
     * 分裂子节点
     */
   _splitChild(parent, index, child) {
    console.log(`🔧 开始分裂: child=[${child.keys}], length=${child.keys.length}`);
    
    if (child.keys.length < 2) {
        throw new Error(`无法分裂节点: 键数不足 ${child.keys.length}`);
    }
    
    const midIndex = Math.floor(child.keys.length / 2);
    const midKey = child.keys[midIndex];
    
    console.log(`midIndex=${midIndex}, midKey=${midKey}`);
    
    const rightNode = new BTreeNode(this.order);
    rightNode.keys = child.keys.slice(midIndex + 1);
    
    console.log(`右节点 keys: slice(${midIndex + 1}) = [${rightNode.keys}]`);
    
    if (!child.isLeaf) {
        rightNode.children = child.children.slice(midIndex + 1);
        rightNode.isLeaf = false;
    } else {
        rightNode.isLeaf = true;
    }
    
    // 更新左节点
    const leftKeysBefore = child.keys.slice(0, midIndex);
    console.log(`左节点 keys: slice(0, ${midIndex}) = [${leftKeysBefore}]`);
    child.keys = leftKeysBefore;
    
    if (!child.isLeaf) {
        child.children = child.children.slice(0, midIndex + 1);
    }
    
    // 插入到父节点
    parent.keys.splice(index, 0, midKey);
    parent.children.splice(index + 1, 0, rightNode);
    parent.isLeaf = false;
    
    console.log(`分裂完成: 中间键=${midKey}, 左节点=[${child.keys}], 右节点=[${rightNode.keys}]`);
}

    /**
     * 内部删除方法
     */
    _delete(key, node = this.root) {
        let i = node.findKey(key);
        
        if (i < node.keys.length && node.keys[i] === key) {
            if (node.isLeaf) {
                return this._deleteFromLeaf(node, i);
            } else {
                return this._deleteFromInternal(node, i);
            }
        } else {
            if (node.isLeaf) {
                return false;
            }
            
            if (node.children[i].keys.length <= this.MIN_KEYS) {
                this._fillChild(node, i);
                // 加强后可能需要调整索引
                if (i > 0 && node.children[i].keys.length <= this.MIN_KEYS) {
                    i--;
                }
            }
            
            return this._delete(key, node.children[i]);
        }
    }

    /**
     * 从叶子节点删除
     */
    _deleteFromLeaf(node, index) {
        node.keys.splice(index, 1);
        return true;
    }

    /**
     * 从内部节点删除
     */
    _deleteFromInternal(node, index) {
        const key = node.keys[index];
        
        if (node.children[index].keys.length > this.MIN_KEYS) {
            const predecessor = this._getPredecessor(node.children[index]);
            node.keys[index] = predecessor;
            return this._delete(predecessor, node.children[index]);
        } else if (node.children[index + 1].keys.length > this.MIN_KEYS) {
            const successor = this._getSuccessor(node.children[index + 1]);
            node.keys[index] = successor;
            return this._delete(successor, node.children[index + 1]);
        } else {
            this._mergeChildren(node, index);
            return this._delete(key, node.children[index]);
        }
    }

    /**
     * 获取前驱节点
     */
    _getPredecessor(node) {
        while (!node.isLeaf) {
            node = node.children[node.children.length - 1];
        }
        return node.keys[node.keys.length - 1];
    }

    /**
     * 获取后继节点
     */
    _getSuccessor(node) {
        while (!node.isLeaf) {
            node = node.children[0];
        }
        return node.keys[0];
    }

    /**
     * 合并子节点
     */
    _mergeChildren(node, index) {
        const leftChild = node.children[index];
        const rightChild = node.children[index + 1];
        const keyToMoveDown = node.keys[index];
        // 添加空节点检查
    if (rightChild.keys.length === 0) {
        // 如果右子节点为空，特殊处理
        node.keys.splice(index, 1);
        node.children.splice(index + 1, 1);
        
        if (node === this.root && node.keys.length === 0) {
            this.root = leftChild;
        }
        return;
    }
        leftChild.keys.push(keyToMoveDown);
        leftChild.keys.push(...rightChild.keys);
        
        if (!leftChild.isLeaf) {
            leftChild.children.push(...rightChild.children);
        }
        
        node.keys.splice(index, 1);
        node.children.splice(index + 1, 1);
        
        if (node === this.root && node.keys.length === 0) {
            this.root = leftChild;
        }
    }

    /**
     * 加强子节点
     */
    _fillChild(node, childIndex) {
        const child = node.children[childIndex];
        
        if (childIndex > 0 && node.children[childIndex - 1].keys.length > this.MIN_KEYS) {
            this._borrowFromLeft(node, childIndex);
        } else if (childIndex < node.children.length - 1 && 
                  node.children[childIndex + 1].keys.length > this.MIN_KEYS) {
            this._borrowFromRight(node, childIndex);
        } else {
            if (childIndex > 0) {
                this._mergeChildren(node, childIndex - 1);
            } else {
                this._mergeChildren(node, childIndex);
            }
        }
    }

    /**
     * 从左兄弟借用
     */
    _borrowFromLeft(node, childIndex) {
        const child = node.children[childIndex];
        const leftSibling = node.children[childIndex - 1];
        
        child.keys.unshift(node.keys[childIndex - 1]);
        node.keys[childIndex - 1] = leftSibling.keys.pop();
        
        if (!child.isLeaf) {
            child.children.unshift(leftSibling.children.pop());
        }
    }

    /**
     * 从右兄弟借用
     */
    _borrowFromRight(node, childIndex) {
        const child = node.children[childIndex];
        const rightSibling = node.children[childIndex + 1];
        
        child.keys.push(node.keys[childIndex]);
        node.keys[childIndex] = rightSibling.keys.shift();
        
        if (!child.isLeaf) {
            child.children.push(rightSibling.children.shift());
        }
    }

    /**
     * 内部查找方法
     */
    _search(key, node) {
        const i = node.findKey(key);
        
        if (i < node.keys.length && node.keys[i] === key) {
            return true;
        }
        
        if (node.isLeaf) {
            return false;
        }
        
        return this._search(key, node.children[i]);
    }

    /**
     * 获取树的高度
     */
    _getHeight(node) {
        if (node.isLeaf) {
            return 1;
        }
        return 1 + this._getHeight(node.children[0]);
    }

    /**
     * 打印树结构
     */
    _printTree(node, level) {
        let result = "  ".repeat(level) + `Level ${level}: [${node.keys.join(', ')}]`;
        console.log(result);
        
        if (!node.isLeaf) {
            for (const child of node.children) {
                this._printTree(child, level + 1);
            }
        }
    }
    // 添加验证方法
_validateNode(node, level = 0) {
    if (node.isLeaf && node.children.length > 0) {
        throw new Error(`叶子节点 ${level} 级有子节点: [${node.keys}]`);
    }
    if (!node.isLeaf && node.children.length === 0) {
        throw new Error(`内部节点 ${level} 级没有子节点: [${node.keys}]`);
    }
    if (node.keys.length > this.order - 1) {
        throw new Error(`节点键数超出限制: [${node.keys}]`);
    }
    if (node !== this.root && node.keys.length < this.MIN_KEYS) {
        throw new Error(`节点键数过少: [${node.keys}]`);
    }
    
    // 递归验证子节点
    if (!node.isLeaf) {
        for (const child of node.children) {
            this._validateNode(child, level + 1);
        }
    }
}

// 在插入和删除后调用验证
insert(key) {
    this._insert(key);
    this._validateNode(this.root);  // 添加验证
}
}
const bTree = new BTree(3);

console.log("=== 初始插入 ===");
bTree.debugInsert(10);
bTree.debugInsert(20);
bTree.debugInsert(5);
bTree.debugInsert(15);

console.log("\n=== 删除测试 ===");
bTree.debugDelete(10);

console.log("\n=== 最终状态 ===");
console.log("搜索10:", bTree.search(10));
console.log("搜索15:", bTree.search(15));
console.log("树高:", bTree.getHeight());
const bTree = new BTree(3);

console.log("=== 逐步插入测试 ===");
bTree.debugInsert(10);
bTree.debugInsert(20); 
bTree.debugInsert(5);
bTree.debugInsert(15);

console.log("\n=== 验证最终结构 ===");
// 期望的正确结构应该是：
//     [10,15]    或者    [15]
//    /   |   \         /    \
//  [5]  [ ]  [20]    [5,10] [20]
const bTree = new BTree(3);

console.log("=== 逐步详细测试 ===");
bTree.debugDetailedInsert(10);
bTree.debugDetailedInsert(20);
bTree.debugDetailedInsert(5);
// 在插入15之前检查状态
console.log("准备插入15前的状态:");
bTree._validateNode(bTree.root);
// 先暂时关闭验证，测试基本功能
const bTree = new BTree(3);

console.log("=== 测试修复后的插入 ===");
const testKeys = [10, 20, 5, 15, 25, 30];

for (const key of testKeys) {
    console.log(`插入 ${key}`);
    bTree.insert(key);
    bTree.print();
    console.log('---');
}

// 最后再验证
console.log("最终验证:");
try {
    bTree._validateNode(bTree.root);
    console.log("✅ 验证通过！");
} catch (e) {
    console.log("❌ 验证失败:", e.message);
}
const bTree = new BTree(3);

// 逐步插入并详细观察
console.log("=== 详细调试插入过程 ===");

console.log("\n1. 插入 10");
bTree.insert(10);
bTree.print();

console.log("\n2. 插入 20");
bTree.insert(20);
bTree.print();

console.log("\n3. 插入 5");
bTree.insert(5);
bTree.print();

console.log("\n4. 插入 15");
bTree.insert(15);
bTree.print();

console.log("\n=== 验证最终结果 ===");
try {
    bTree._validateNode(bTree.root);
    console.log("🎉 所有验证通过！B树结构正确");
} catch (e) {
    console.log("💥 验证失败:", e.message);
}

console.log("\n=== 搜索测试 ===");
[10, 15, 20, 5, 25].forEach(key => {
    console.log(`搜索 ${key}: ${bTree.search(key)}`);
});
// 删除测试函数
function testDeleteOperations() {
    const bTree = new BTree(3);
    
    console.log("=== B树删除功能全面测试 ===\n");

    // 阶段1：准备测试数据
    console.log("📝 阶段1：准备测试数据");
    const testKeys = [10, 20, 5, 15, 25, 3, 8, 12, 18, 30];
    testKeys.forEach(key => bTree.insert(key));
    
    console.log("初始B树结构:");
    bTree.print();
    console.log("初始验证:", bTree._validateNode(bTree.root) ? "通过" : "失败");
    console.log("---\n");

    // 阶段2：测试各种删除情况
    console.log("🗑️ 阶段2：删除操作测试");

    // 情况1：删除叶子节点中的键（节点仍有足够键）
    console.log("1. 删除叶子节点键（节点仍健康）");
    console.log("删除 3:");
    bTree.delete(3);
    bTree.print();
    console.log("搜索3:", bTree.search(3));
    console.log("---");

    // 情况2：删除叶子节点中的键（需要从兄弟借）
    console.log("2. 删除叶子节点键（需要借用）");
    console.log("删除 8:");
    bTree.delete(8);
    bTree.print();
    console.log("搜索8:", bTree.search(8));
    console.log("---");

    // 情况3：删除内部节点中的键（用后继替换）
    console.log("3. 删除内部节点键（后继替换）");
    console.log("删除 15:");
    bTree.delete(15);
    bTree.print();
    console.log("搜索15:", bTree.search(15));
    console.log("---");

    // 情况4：删除内部节点中的键（用前驱替换）
    console.log("4. 删除内部节点键（前驱替换）");
    console.log("删除 20:");
    bTree.delete(20);
    bTree.print();
    console.log("搜索20:", bTree.search(20));
    console.log("---");

    // 情况5：删除导致节点合并
    console.log("5. 删除导致节点合并");
    console.log("删除 12:");
    bTree.delete(12);
    bTree.print();
    console.log("搜索12:", bTree.search(12));
    console.log("---");

    // 情况6：删除根节点
    console.log("6. 删除根节点");
    console.log("删除 18:");
    bTree.delete(18);
    bTree.print();
    console.log("搜索18:", bTree.search(18));
    console.log("---");

    // 最终验证
    console.log("✅ 最终验证:");
    try {
        bTree._validateNode(bTree.root);
        console.log("🎉 所有删除操作后B树仍然正确！");
    } catch (e) {
        console.log("❌ 验证失败:", e.message);
    }

    // 剩余键检查
    console.log("\n🔍 剩余键检查:");
    testKeys.forEach(key => {
        const exists = bTree.search(key);
        console.log(`搜索 ${key}: ${exists ? "存在" : "不存在"}`);
    });
}

// 运行测试
testDeleteOperations();
```
```
//----插入逻辑----//
insert(key) {
    if (this.root.isFull()) {  // 检查根节点是否已满
        //分裂根节点，创建新根
        const newRoot = new BTreeNode(this.order);
        newRoot.children.push(this.root);  // 原根成为子节点
        this._splitChild(newRoot, 0, this.root);  // 分裂原根
        this.root = newRoot; //更新根指针
    }
    this._insertNonFull(this.root, key);
}

//分裂逻辑：B树的生长是向上生长
_splitChild(parent, index, child) {
    // parent: 要分裂的节点的父节点
    // index: child在parent.children中的位置  
    // child: 实际要分裂的节点
    const midIndex = Math.floor(child.keys.length / 2);
    const midKey = child.keys[midIndex];  // 找出中间值 
    
    // 创建右节点
    const rightNode = new BTreeNode(this.order);
    
    // === 右边部分 ===
    rightNode.keys = child.keys.slice(midIndex + 1);  // 右节点获得中间关键字之后的所有关键字 
    if (!child.isLeaf) {
        // 如果原节点有子节点，右节点也需要继承对应的子节点
        rightNode.children = child.children.slice(midIndex + 1);  //从mid+1开始取到最后
        rightNode.isLeaf = false;  // 标记右节点为内部节点 
    }
    // === 左边部分 ===  
    // 更新左节点（原来的child变成左节点）
    child.keys = child.keys.slice(0, midIndex);  // 左节点保留中间关键字之前的所有关键字 
    if (!child.isLeaf) {
        // 左节点保留对应的子节点
        child.children = child.children.slice(0, midIndex + 1);  // 从索引0开始取到mid+1
    }
    // === 更新父节点 ===
    parent.keys.splice(index, 0, midKey);  // 在父节点的index位置插入中间关键字 
    parent.children.splice(index + 1, 0, rightNode);  // 在父节点的index+1位置插入右节点 
}


```
```
//----删除逻辑----//
delete(key, node = this.root) {
    let i = node.findKey(key);
    // 情况1：关键字在当前节点中
    if (i < node.keys.length && node.keys[i] === key) {
        if (node.isLeaf) {
            // 情况1A：要删除的键在当前节点中，且当前节点是叶子节点
            return this._deleteFromLeaf(node, i);
        } else {
            // 情况1B：要删除的键在当前节点中，但当前节点是内部节点
            return this._deleteFromInternal(node, i);
        }
    } else {
        // 情况2：要删除的键不在当前节点中
        if (node.isLeaf) {
            return false; // 关键字不存在
        }
        // 检查子节点是否需要加强
        if (node.children[i].keys.length <= this.MIN_KEYS) {
            this._fillChild(node, i);
        }
        // 递归删除
        return this.delete(key, node.children[i]);
    }
}
//内部方法：
//删除叶子节点时的后继替换策略
_deleteFromLeaf(node, index) {
    // 直接从叶子节点中删除关键值
    node.keys.splice(index, 1);
    return true;
}
//删除内部节点时的后继替换策略
_deleteFromInternal(node, index) {
    const key = node.keys[index];
    // 情况1B-a：左子节点足够
    if (node.children[index].keys.length > this.MIN_KEYS) {//1.node.children[index]是要删除键的左边子节点
        const predecessor = this._getPredecessor(node.children[index]);//2._getPredecessor()函数找到右子节点中的最大值
        node.keys[index] = predecessor;//3.用找到的后继键替换要删除的键
        return this.delete(predecessor, node.children[index]);// 4.递归删除原本左边子节点中的最大值
    }
    // 情况1B-b：右子节点足够
    else if (node.children[index + 1].keys.length > this.MIN_KEYS) {//1.node.children[index + 1]是要删除键的右子节点
        const successor = this._getSuccessor(node.children[index + 1]);//2._getSuccessor()函数找到右子节点中的最小键
        node.keys[index] = successor;//3.用找到的后继键替换要删除的键
        return this.delete(successor, node.children[index + 1]); // 4.递归删除后继节点；现在需要从右子树中删除原来的最小值
    }
    // 情况1B-c：两个子节点都不够，需要合并
    else {
        this._mergeChildren(node, index);//1.合并子节点：将左子节点、要删除的键、右子节点合并成一个节点
        return this.delete(key, node.children[index]);
    }
}
_mergeChildren(node, index) {
    /**
     * 合并节点的两个子节点
     * @param {BTreeNode} node - 父节点
     * @param {number} index - 要删除的键的索引位置
     */
    // 1. 获取要合并的两个子节点
    const leftChild = node.children[index];      // 左子节点
    const rightChild = node.children[index + 1]; // 右子节点
    const keyToMoveDown = node.keys[index];      // 要从父节点下移的键
    // 2. 将父节点的键下移到左子节点
    leftChild.keys.push(keyToMoveDown);
    // 3. 将右子节点的所有键合并到左子节点
    // 注意：这里使用扩展运算符将右子节点的键数组展开并添加到左子节点
    leftChild.keys.push(...rightChild.keys);//不需要合并子节点引用，因为叶子节点本来就没有子节点。
    // 4. 如果子节点不是叶子节点，还需要合并子节点的子节点引用
    if (!leftChild.isLeaf) {
        // 将右子节点的所有子节点引用合并到左子节点
        leftChild.children.push(...rightChild.children);
    }
    // 5. 从父节点中删除下移的键和右子节点引用
    node.keys.splice(index, 1);           // 删除下移的键
    node.children.splice(index + 1, 1);   // 删除右子节点引用
    // 6. 特殊情况：如果合并后父节点是根节点且变空，需要更新根节点
    if (node === this.root && node.keys.length === 0) {
        this.root = leftChild;  // 左子节点成为新的根节点
    }
}
//加强子节点：确保子节点有足够的键
_fillChild(node, childIndex) {
    /**
     * 加强子节点：确保子节点有足够的键
     * 策略优先级：
     * 1. 从左兄弟节点借一个键
     * 2. 从右兄弟节点借一个键  
     * 3. 合并子节点
     */
    const child = node.children[childIndex];
    // 策略1：尝试从左兄弟节点借用
    if (childIndex > 0 && node.children[childIndex - 1].keys.length > this.MIN_KEYS) {
        this._borrowFromLeft(node, childIndex);
    }
    // 策略2：尝试从右兄弟节点借用
    else if (childIndex < node.children.length - 1 && 
             node.children[childIndex + 1].keys.length > this.MIN_KEYS) {
        this._borrowFromRight(node, childIndex);
    }
    // 策略3：左右兄弟都没有富余，只能合并
    else {
        // 选择与左兄弟合并（如果存在），否则与右兄弟合并
        if (childIndex > 0) {
            this._mergeChildren(node, childIndex - 1);
        } else {
            this._mergeChildren(node, childIndex);
        }
    }
}
_borrowFromLeft(node, childIndex) {
    const child = node.children[childIndex];        // 需要加强的子节点
    const leftSibling = node.children[childIndex - 1]; // 左兄弟节点
    // 1. 将父节点的键下移到子节点（在开头插入）
    child.keys.unshift(node.keys[childIndex - 1]);
    // 2. 将左兄弟节点的最大键上移到父节点
    node.keys[childIndex - 1] = leftSibling.keys.pop();
    // 3. 如果子节点不是叶子节点，还需要移动子节点引用
    if (!child.isLeaf) {
        // 将左兄弟节点的最后一个子节点移动到子节点的开头
        child.children.unshift(leftSibling.children.pop());
    }
}
_borrowFromRight(node, childIndex) {
    const child = node.children[childIndex];        // 需要加强的子节点
    const rightSibling = node.children[childIndex + 1]; // 右兄弟节点
    // 1. 将父节点的键下移到子节点（在末尾添加）
    child.keys.push(node.keys[childIndex]);
    // 2. 将右兄弟节点的最小键上移到父节点
    node.keys[childIndex] = rightSibling.keys.shift();
    // 3. 如果子节点不是叶子节点，还需要移动子节点引用
    if (!child.isLeaf) {
        // 将右兄弟节点的第一个子节点移动到子节点的末尾
        child.children.push(rightSibling.children.shift());
    }
}
```