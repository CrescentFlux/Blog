# 树（Tree）
## 基础特性
- 树：每个节点有多个next指针（层次结构）
- 基础对比

|概念|	链表	|二叉树|	
---|---|---
|起点|	head	|root|	
|指针数量	|1个(next)	|2个(left, right)|	
|结构	|线性	|层次|	
|遍历方式|	顺序遍历	|前序、中序、后序|


## 注意事项
1. **混淆点**
- 树的结构
```
        A (根节点)
       / \
      B   C (子节点)
     / \   \
    D   E   F (叶子节点)
```
- 叶子节点和字节点
```
叶子节点示例：最底层的节点
    5
   / \
  3   7   ← 3和7都是叶子节点（没有子节点）
    5 根节点（最顶层的节点）
   / \
  3   7   ← 3和7都是5的子节点（既有上级又有下属的节点）
```
- 特殊情况：最小值/最大值不是叶子节点
```
      5
     / \
    3   7
   /   / \
  2   6   8
   \
    4    ← 在2的右边添加一个节点
如果最小值是叶子节点 → 情况1（直接删除）
如果最小值有一个右子节点 → 情况2（用右子节点替代）
最小值不可能有左子节点（否则就不是最小值）
```
- 树的遍历
```
前序遍历（Pre-order）：根 → 左 → 右(A → B → D → E → C → F)
中序遍历（In-order）：左 → 根 → 右(D → B → E → A → C → F)
后序遍历（Post-order）：左 → 右 → 根(D → E → B → F → C → A)
```
- 递归
```
- 树的结构是"分支"的，不是"线性"的，循环无法优雅地处理这种"深入再返回"的路径
- 递归的核心理念：分而治之；递归思维："要解决大问题，先假设小问题已经解决"
- 问题具有"树形结构"，而递归是处理树形结构的自然方式 
- 递归的核心特征：函数调用自身：任何函数自我调用（直接或间接）
- 树的插入是深度优先:沿着一条路径走到头 → 在第一个空位插入
```
- 卡特兰数
```
1.卡特兰数Catalan Number:有效括号组合的数量遵循卡特兰数
C(n) = (2n)! / ((n+1)! * n!)
2.逻辑判断
是否涉及平衡/配对概念？
是否需要避免某种"越界"？
是否与二叉树、栈操作相关
3.适用领域【C(n)】
网格路径不穿越对角线：在n×n网格中，从左下到右上不穿越对角线的路径数
二叉树的形态：n个节点可以组成多少种不同形状的二叉树
栈的出入序列：1,2,3,...,n通过栈产生的所有输出序列数
多边形三角划分：n+2边形的三角划分方案数
n对括号的有效组合数 
```
- 组合排列的选择
```
排列：考虑顺序 → 排队问题（张三李四排队 vs 李四张三排队是两种）
组合：不考虑顺序 → 选人问题（选张三李四 vs 选李四张三是同一种）
公式：
排列 A(n,k) = n!/(n-k)!
组合 C(n,k) = n!/(k!×(n-k)!)
```
- 查询修改方法
```
1.查询方法：查找节点；计算深度/高度；检查平衡性
2. 修改方法：插入节点；删除节点；修改节点
```
- 二叉树实现基本过程(Binary Tree)
```
1：定义树节点
2：创建简单的二叉树Binary Tree
- 初始时树为空，没有根节点
```
- 二叉搜索树的性质：
```
左子树所有节点 < 当前节点 < 右子树所有节点
根节点的替代值必须满足：
大于左子树所有节点
小于右子树所有节点
```
- 标准二叉搜索树通常不允许重复值
```
重复值会破坏排序性质
查找时无法确定返回哪个节点
通常用其他方式处理重复（如计数器）
遇到相等值通常不插入，或者特殊处理。
```
- 二叉搜索树 vs 平衡二叉树
```
它们不是对立关系，而是层次关系：
二叉搜索树（BST）：基础要求
    左子树所有节点 < 当前节点 < 右子树所有节点
    保证元素有序，但不保证效率
平衡二叉树：高级要求
    首先是二叉搜索树（满足排序性质）
    额外要求：左右子树高度差 ≤ 1
    保证操作效率（O(log n)）
```

2. 代码实现
```
//---实现基础二叉树---//
class TreeNode {
    constructor(data) {
        this.data = data;
        this.left = null;   // 左指针
        this.right = null;  // 右指针 ← 新增
    }
}
class BinaryTree {
    constructor() {
        this.root = null;  // 树的根节点（相当于链表的head）初始值树为空没有根节点
    }
    
    // 手动构建方法
    createSimpleTree() {
        this.root = new TreeNode('A');
        this.root.left = new TreeNode('B');
        this.root.right = new TreeNode('C');
        this.root.left.left = new TreeNode('D');
        this.root.left.right = new TreeNode('E');
        this.root.right.right = new TreeNode('F');
    }
}

//----树的遍历----//
//前序遍历的实现
class BinaryTree {
    // ... 之前的代码
    
    preOrderTraversal(node = this.root) {
        if (node === null) return;
        
        console.log(node.data);    // 1. 访问根节点
        this.preOrderTraversal(node.left);  // 2. 遍历左子树
        this.preOrderTraversal(node.right); // 3. 遍历右子树
    }
}

//----递归基础------//
// 1. 计算树的节点总数（递归）递归是处理层次结构和分支问题的自然工具，而树正是这类问题的典型代表
function countNodes(node) {
    if (node === null) return 0;  // 空树有0个节点
    
    // 当前节点(1) + 左子树节点数 + 右子树节点数
    return 1 + countNodes(node.left) + countNodes(node.right);
}
//2. 列出文件夹下所有文件（包括子文件夹）
function listFiles(folderPath) {
    let files = [];
    for (let item of readDirectory(folderPath)) {
        if (isFile(item)) {
            files.push(item);  // 如果是文件，直接加入结果
        } else {
            // 如果是文件夹，递归遍历它
            files = files.concat(listFiles(item));
        }
    }
    return files;
}
//计算公司组织架构的总人数
function countEmployees(node) {
    if (node === null) return 0;
    return 1 + countEmployees(node.left) + countEmployees(node.right);
}
// 用递归解决复杂问题：查找树中所有路径
function findAllPaths(node, currentPath = [], allPaths = []) {
    if (node === null) return;
    currentPath.push(node.data);  // 添加当前节点到路径
    if (node.left === null && node.right === null) {
        // 到达叶子节点，保存完整路径
        allPaths.push([...currentPath]);
    } else {
        // 继续探索左右分支
        findAllPaths(node.left, currentPath, allPaths);
        findAllPaths(node.right, currentPath, allPaths);
    }// 对于树：A-B-D, A-B-E, A-C-F
        // 递归自动找出所有路径    复杂问题（遍历文件系统）：递归的优势爆炸式增长//
    currentPath.pop();  // 回溯，准备探索其他分支
    return allPaths;
}

//---递归进阶---//
//生成n对括号，并且输出所有可能的括号组合---//--回溯递归--探索决策树---//
//递归思路：决策树思维；有条件+递归（高效）：
//理解卡特兰条件：条件1：确保始终 open >= close（卡特兰条件1）条件2：最终 open = close = n（卡特兰条件2）
1.从左到右扫描时，右括号数量永远不能超过左括号数量
2.最终左括号数量 = 右括号数量 = n
3.平衡性必须在每一步都保持："())(()"为什么无效  
-只能向前走或向后走（左括号=前进，右括号=后退）
-不能退到起点后面（右括号不能超过左括号）
-最终要回到起点（左右括号数量相等）
//递归负责：
1.自动回溯：尝试一条路→返回→尝试下一条路；尝试所有可能路径，自动放弃无效路径
2.路径记录：保持当前路径状态- 避免重复：通过参数控制，不生成明显无效的组合
3.完整搜索：确保不遗漏任何可能解
//条件负责：
1.剪枝：提前终止无效路径
2.导向：只引导递归走向有希望的方向
3.效率：减少不必要的计算

function backtrack(current, open, close) {//有效性的核心规则是：在任何时刻，close ≤ open；如果没有close参数，无法实时判断有效性
    // 条件1：不能退到起点后面！
    if (close > open) return; // 立即终止无效路径
    // 条件2：最终要回到起点
    if (open === n && close === n) {
        result.push(current);
        return;
    }
    // 选择1：向前走一步（如果还有前进空间）
    if (open < n) {
        backtrack(current + '(', open + 1, close);
    }
    // 选择2：向后退一步（如果不会退到起点后面）
    if (close < open) {  // 注意这里是close < open，不是close < n
        backtrack(current + ')', open, close + 1);
    }
}

//数学递归--斐波那契数列
function fib(n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2); // 明显的分解
}

//间接递归，函数互相调用
function D() {
    E();
}
function E() {
    D(); // 互相调用（间接递归）
}

//八皇后问题



//----二叉树创建和测试-----//
// 1. 定义树节点
class TreeNode {//TreeNode：管理单个节点
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
    }
}

// 2. 定义二叉树
class BinaryTree {// BinaryTree：管理整棵树
    constructor() {
        this.root = null;
    }
    
    // 先手动创建一棵测试树
    createTestTree() {
        /* 创建这样一棵树：
              10
            /    \
           5      15
          / \    /  \
         3   7  12  18
        */
        this.root = new TreeNode(10);
        this.root.left = new TreeNode(5);
        this.root.right = new TreeNode(15);
        this.root.left.left = new TreeNode(3);
        this.root.left.right = new TreeNode(7);
        this.root.right.left = new TreeNode(12);
        this.root.right.right = new TreeNode(18);
    }
    
    // 1：查找节点
    find(value, node = this.root) {
        if (node === null) return null;
        if (value === node.data) return node;
        
        if (value < node.data) {//在二叉搜索树中，小值往左找，大值往右找
            return this.find(value, node.left);
        } else {
            return this.find(value, node.right);
        }
    }
    
    // 2：计算树的高度
    getHeight(node = this.root) {
        if (node === null) return 0;  // null是"无值"，空树高度 = 0；只有根节点的树高度 = 1；根节点+一个子节点高度 = 2
        const leftHeight = this.getHeight(node.left);
        const rightHeight = this.getHeight(node.right);
        return Math.max(leftHeight, rightHeight) + 1;// 当前节点贡献1层高度
    }
    
    // 3：检查平衡性；平衡二叉树的定义：每个节点的左右子树高度差不超过1
    isBalanced(node = this.root) {
        if (node === null) return true;//空树是平衡的
        
        const leftHeight = this.getHeight(node.left);
        const rightHeight = this.getHeight(node.right);
        
        if (Math.abs(leftHeight - rightHeight) > 1) {
            return false;
        }
        
        return this.isBalanced(node.left) && this.isBalanced(node.right);
    }
    
    // 辅助方法：打印树结构（方便调试）
    printTree(node = this.root, prefix = "", isLeft = true) {
        if (node === null) return;
        
        console.log(prefix + (isLeft ? "├── " : "└── ") + node.data);
        this.printTree(node.left, prefix + (isLeft ? "│   " : "    "), true);
        this.printTree(node.right, prefix + (isLeft ? "│   " : "    "), false);
    }
}
// 3. 测试代码
console.log("=== 二叉树测试 ===");
// 创建树实例
const tree = new BinaryTree();
tree.createTestTree();
// 打印树结构
console.log("树结构:");
tree.printTree();
// 测试查找功能
console.log("\n=== 查找测试 ===");
console.log("查找7:", tree.find(7) ? "找到" : "未找到");
console.log("查找20:", tree.find(20) ? "找到" : "未找到");
// 测试高度计算
console.log("\n=== 高度测试 ===");
console.log("树的高度:", tree.getHeight());
// 测试平衡性
console.log("\n=== 平衡性测试 ===");
console.log("树是否平衡:", tree.isBalanced());
// 创建一个不平衡的树测试
console.log("\n=== 不平衡树测试 ===");
const unbalancedTree = new BinaryTree();
unbalancedTree.root = new TreeNode(10);
unbalancedTree.root.left = new TreeNode(5);
unbalancedTree.root.left.left = new TreeNode(3);
unbalancedTree.root.left.left.left = new TreeNode(1); // 故意制造不平衡
console.log("不平衡树的高度:", unbalancedTree.getHeight());
console.log("不平衡树是否平衡:", unbalancedTree.isBalanced());


//--查询修改操作--//
insert(value) {
    const newNode = new TreeNode(value);
    
    if (this.root === null) {
        this.root = newNode;  // 第一个节点成为根节点
        return;
    }
    //插入位置是由值的大小关系自动确定；插入操作不是在"替换"，而是在"扩展"树的结构，同时维护二叉搜索树的排序性质，这样才能保证高效的查找性能
    function insertNode(node, newNode) {//node是指"当前正在检查的节点"；
        if (newNode.value < node.value) {
            if (node.left === null) {
                node.left = newNode;  // 左位置空着，直接放新节点
            } else {
                insertNode(node.left, newNode);  // 继续在左子树中找位置
            }
        } else if (newNode.value > node.value) {
            if (node.right === null) {
                node.right = newNode;  // 右位置空着，直接放新节点
            } else {
                insertNode(node.right, newNode);  // 继续在右子树中找位置
            }
        } else {
            // 值相等的情况：可以选择不插入，或特殊处理
            console.log("值已存在，不插入重复值");
        }
    }
    
    insertNode(this.root, newNode);
}

//查找最小值：移动节点指针，不是比较值
findMin(node = this.root) {
    if (node === null) return null;
    while (node.left !== null) {  // 只要还有左节点，就继续向左
        node = node.left;         // 移动到左节点
    }
    return node.value;            // 返回最左节点的值
}

//删除不同位置的节点
remove(value, node = this.root) {
    if (node === null) return null;
    if (value < node.value) {
        node.left = this.remove(value, node.left);  // 
        return node;
    } else if (value > node.value) {
        node.right = this.remove(value, node.right);  //
        return node;
    } else {
        // 找到要删除的节点
        
        // 情况1：叶子节点： 直接移除，父节点指针设为null；不影响其他节点
        if (node.left === null && node.right === null) {
            return null;  //  返回null，不是node
        }
        // 情况2：只有一个子节点：用子节点替代自己；需要更新父节点的指针
        if (node.left === null) {
            return node.right;  // 
        }
        if (node.right === null) {
            return node.left;   //
        }
        // 情况3：有两个子节点 需要找替代值（右子树最小值或左子树最大值）；还要删除原来的替代节点
        const minValue = this.findMin(node.right);  //  在右子树找最小值
        node.value = minValue;                      // 用最小值替代当前值
        node.right = this.remove(minValue, node.right);  // 删除右子树中的最小值节点，避免重复
        return node;
        
    }
}

//验证二叉搜索树：每个节点必须在(min, max)范围内；左子树的最大值是当前节点值；右子树的最小值是当前节点值
isValidBST(node = this.root, min = -Infinity, max = Infinity) {
    if (node === null) return true;  // 空树是有效的
    if (node.value <= min || node.value >= max) {
        return false;  // 超出范围
    }
    return this.isValidBST(node.left, min, node.value) && 
           this.isValidBST(node.right, node.value, max);
}

//层级遍历：广度优先；使用队列（先进先出）；根节点 → 第二层 → 第三层...;层级遍历的队列就是当前层级的所有待访问节点
levelOrder() {
    if (this.root === null) return [];
    const result = [];
    const queue = [this.root];  // 队列初始包含根节点
    while (queue.length > 0) {
        const node = queue.shift();  // 从队列开头取出
        result.push(node.value);
        if (node.left !== null) {
            queue.push(node.left);
        }
        if (node.right !== null) {
            queue.push(node.right);
        }
    }
    return result;
}

//查找最小值：中序遍历二叉搜索树得到升序数组；第k小就是数组第k-1个元素；中序遍历(从小到大报数)自然得到有序序列
findKthSmallest(k, node = this.root) {
    const result = [];
    function inOrderTraversal(node) {
        if (node === null) return;
        inOrderTraversal(node.left);   // 遍历左子树
        result.push(node.value);       // 访问当前节点
        inOrderTraversal(node.right);  // 遍历右子树
    }
    inOrderTraversal(node);
    return result[k - 1];  // 第k小对应索引k-1
}


```