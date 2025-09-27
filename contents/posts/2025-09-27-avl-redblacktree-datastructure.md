# Tree
## 基础知识
1. 平衡二叉树AVL Tree：自平衡的BST
2. 红黑树
```
-每个节点是红色或黑色
-根节点是黑色
-叶子节点（NIL）是黑色
-红色节点的子节点都是黑色
-从任一节点到其叶子的所有路径包含相同数目的黑色节点
```

AVL树 vs 红黑树：

|特性	|AVL树|	红黑树|
---|---|---
|平衡严格度	|严格（高度差≤1）|	宽松（最长路径≤2倍最短路径）|
|平衡标准	|高度差≤1	|颜色规则|
|查询速度|	更快（O(log n)）|	稍慢|
|旋转频率|	高	|低|
|查询性能|	更快|	稍慢|
|插入删除|	较慢|	更快|
|插入删除|	需要更多旋转|	需要更少旋转|
|应用场景|	需要频繁查询| 需要频繁插入删除|


## 注意事项
1. AVL混淆点
- 二叉树：每个节点最多两个子节点；二叉搜索树(BST)：有序的二叉树；平衡二叉树(AVL)：自平衡的BST
- 优势
```
AVL树能保证O(log n):保持平衡意味着控制树的高度
O(log n)的意义：数据量翻倍，操作次数只+1//几乎恒定//性能比较稳定
```
- 高度
```
定义：从当前节点到最深叶子节点的路径长度；当前节点本身也占一层高度,所以空树的高度为1,因为它只有一个字节点；
计算：节点高度 = 最高子树高度 + 1
平衡因子： 平衡因子 = 左高 - 右高
AVL树的高度: h ≤ 1.44 × log₂(n)：AVL树通过旋转操作，确保树的高度始终与节点数成对数关系，而不是线性关系；节点数成对数增长；
```
- AVL树通过旋转操作，确保树的高度始终与节点数成对数关系，而不是线性关系
```
- 旋转不是随意转动，而是通过改变指针关系来降低高度-指针关系需要同时考虑方向和值大小
- 旋转必须保持二叉搜索树的性质;旋转前后，中序遍历结果必须相同;
- 关键：要降低高度同时保持二叉搜索树性质
- 关键原则：旋转不能改变中序遍历顺序
- 旋转操作是数学上唯一能同时满足：
1.降低树高度
2.保持二叉搜索树性质
3.不改变元素顺序
```
2. 红黑树混淆点
- 节点
```
-红黑树的叶子节点都指向统一的NIL节点
-黑色节点：数量在路径间必须严格相等（规则5）；提供了树的结构稳定性
-每个数据节点都有两个子节点，新节点总是插入在NIL的位置
```
- 颜色修复
```
-需要parent指针来回溯修复颜色
-需要判断节点是祖父节点的左节点还是右节点
-根据父节点的颜色决定处理策略
-临时违反规则，需要通过向上传递来解决
```
- 修复可能触发新的修复
```
-红黑树保持的是：黑色高度平衡，不是红色数量平衡
-修复局部问题 → 可能影响上层 → 继续修复上层 → 直到根节点
1.发现问题：黑色高度不平衡或连续红色
2.局部修复：通过旋转和染色解决当前三代的问题
3.影响评估：修复可能使祖父节点变红
4.向上传递：如果祖父的父节点也是红，继续修复
5.最终解决：保证根节点为黑
```
- 旋转过程中要防止违反红黑树规则
```
    15(黑)       
   /     \
12(红)   NIL(黑)  
直接右旋违反规则：
    12(红)        
       \
       15(黑)   
         \
         NIL(黑)
```

3. 代码实现
```
//1.节点高度
class AVLNode {
    constructor(value) {
        this.value = value;
        this.left = null;
        this.right = null;
        this.height = 1;  // 叶子节点高度为1
    }
}

function getHeight(node) {
    if (node === null) return 0;
    
    const leftHeight = getHeight(node.left);
    const rightHeight = getHeight(node.right);
    
    return Math.max(leftHeight, rightHeight) + 1;
}

//2：计算平衡因子
function getBalanceFactor(node) {
    if (node === null) return true;
    
    const leftHeight = getHeight(node.left);
    const rightHeight = getHeight(node.right);
    
    return leftHeight - rightHeight;  // 平衡因子 = 左高 - 右高
}
// 3：判断是否平衡
function isBalanced(node) {
    if (node === null) return true;  // 空树是平衡的（不是0）
    const balanceFactor = getBalanceFactor(node);
    if (Math.abs(balanceFactor) > 1) {  // 平衡因子绝对值不能超过1
        return false;
    }
    return isBalanced(node.left) && isBalanced(node.right);
}

//--AVL插入旋转---//
// 1. 先定义节点类
class AVLNode {
    constructor(value) {
        this.value = value;
        this.left = null;
        this.right = null;
        this.height = 1;
    }
}
// 2. 完整的AVL树实现
class AVLTree {
    constructor() {
        this.root = null;
    }
    // 获取节点高度
    _getHeight(node) {
        if (node === null) return 0;
        return node.height;
    }
    // 获取平衡因子
    _getBalanceFactor(node) {
        if (node === null) return 0;
        return this._getHeight(node.left) - this._getHeight(node.right);
    }
    // 右旋
    _rotateRight(y) {
        const x = y.left;
        const T2 = x.right;
        x.right = y;
        y.left = T2;
        y.height = 1 + Math.max(this._getHeight(y.left), this._getHeight(y.right));
        x.height = 1 + Math.max(this._getHeight(x.left), this._getHeight(x.right));
        return x;
    }
    // 左旋
    _rotateLeft(x) {
        const y = x.right;
        const T2 = y.left;
        y.left = x;
        x.right = T2;
        x.height = 1 + Math.max(this._getHeight(x.left), this._getHeight(x.right));
        y.height = 1 + Math.max(this._getHeight(y.left), this._getHeight(y.right));
        return y;
    }
    insert(value) {
        this.root = this._insert(this.root, value);
    }
    _insert(node, value) {
        if (node === null) {
            return new AVLNode(value);
        }
        if (value < node.value) { // 执行标准的BST插入
            node.left = this._insert(node.left, value);
        } else if (value > node.value) {
            node.right = this._insert(node.right, value);
        } else {
            return node;// 重复值不插入
        }
        node.height = 1 + Math.max(this._getHeight(node.left), this._getHeight(node.right)); //更新当前节点的高度
        const balanceFactor = this._getBalanceFactor(node); //获取平衡因子，检查是否失衡
        return this._balanceNode(node, balanceFactor, value); //根据失衡情况执行旋转
    }
    
    _balanceNode(node, balanceFactor, value) {
        if (balanceFactor > 1 && value < node.left.value) {
            return this._rotateRight(node);
        }
        if (balanceFactor < -1 && value > node.right.value) {
            return this._rotateLeft(node);
        }
        if (balanceFactor > 1 && value > node.left.value) {
            node.left = this._rotateLeft(node.left);
            return this._rotateRight(node);
        }
        if (balanceFactor < -1 && value < node.right.value) {
            node.right = this._rotateRight(node.right);
            return this._rotateLeft(node);
        }
        return node;
    }
    // 打印树结构（辅助方法）
    print() {
        this._print(this.root, "", true);
    }
    _print(node, prefix, isLeft) {
        if (node === null) return;
        console.log(prefix + (isLeft ? "├── " : "└── ") + node.value + `(h:${node.height})`);
        this._print(node.left, prefix + (isLeft ? "│   " : "    "), true);
        this._print(node.right, prefix + (isLeft ? "│   " : "    "), false);
    }
}
// 3. 测试代码
console.log("=== AVL树测试 ===");
const avlTree = new AVLTree();
// 测试插入序列（会触发旋转）
console.log("插入10, 20, 30, 5, 15");
avlTree.insert(10);
avlTree.insert(20);
avlTree.insert(30); // 触发左旋
avlTree.insert(5);
avlTree.insert(15);
console.log("\n最终树结构:");
avlTree.print();
console.log("\n根节点:", avlTree.root.value);
console.log("平衡因子:", avlTree._getBalanceFactor(avlTree.root));
```
```
//红黑树节点定义：
class RedBlackNode {
    constructor(value) {
        this.value = value;
        this.color = 'RED';  // 新节点默认红色
        this.left = null;  // 叶子节点指向NIL
        this.right = null; // 叶子节点指向NIL
        this.parent = null;  // 需要父指针用于旋转
    }
}
//红黑树类框架：
class RedBlackTree {
    constructor() {
        this.NIL = { color: 'BLACK' };  // 统一的叶子节点
        this.root = this.NIL;           // 初始时根指向NIL
    }
    // 插入方法
    insert(value) {
        const newNode = new RedBlackNode(value);
        newNode.left = this.NIL;
        newNode.right = this.NIL;
        this.insert(this.root, newNode);
        this.fixInsert(newNode);  // 红黑树的核心：修复颜色
    }
}

//颜色修复规则//
//符合规则：情况1：解决颜色冲突（视觉问题）情况2+3：解决结构平衡（数学问题）
_fixInsert(node) {
    while (node.parent.color === 'RED') {
        if (node.parent === node.parent.parent.left) {
            // 父节点是祖父节点的左孩子
            const uncle = node.parent.parent.right;
            if (uncle.color === 'RED') {
                // 情况1：叔叔是红色
                node.parent.color = 'BLACK';
                uncle.color = 'BLACK';
                node.parent.parent.color = 'RED';
                node = node.parent.parent;
            } else {
                if (node === node.parent.right) {
                    // 情况2：节点是父节点的右孩子；情况2/3：修复黑色高度（叔叔为黑）
                    node = node.parent;
                    this.leftRotate(node);
                }
                // 情况3：节点是父节点的左孩子
                node.parent.color = 'BLACK';
                node.parent.parent.color = 'RED';
                this.rightRotate(node.parent.parent);
            }
        } else {
            // 对称情况：父节点是祖父节点的右孩子
            // ...（类似逻辑）
        }
    }
    this.root.color = 'BLACK';  // 确保根节点为黑色
}

//红黑树删除操作//
fixDelete(x) {
    while (x !== this.root && x.color === 'BLACK') {
        if (x === x.parent.left) {
            let sibling = x.parent.right;
            //这里sibling永远代表被删除x的兄弟，修改兄弟来符合标准，所以需要实时的知道在树结构变化之后新的兄弟是哪位
            if (sibling.color === 'RED') {
                // 情况1：兄弟为红：注意：情况1只是一个转换步骤，它本身不解决黑高平衡问题
                sibling.color = 'BLACK';//1.把兄弟从红色变成黑色
                x.parent.color = red;//2.把父节点从原本的黑色变成红色
                this._leftRotate(x.parent);//3.对父节点左旋，此时父节点变成原本左子树的一部分，兄弟节点变成父节点
                sibling = x.parent.right;//4.获取新的兄弟节点，然后继续判断
            }
            if (sibling.left.color === 'BLACK' && sibling.right.color === 'BLACK') {
                // 情况2：兄弟的孩子都为黑
                sibling.color = 'RED';//1.先把兄弟变成红色，此时红黑树已经平衡但是总体高度下降了1,所以需要向上传递继续平衡
                x = node.parent;  // 2.向上传递，不平衡位置上升了一层，从下一层的左右孩子不平衡上升成为上一层的左右子树不平衡
            } else {
                if (sibling.right.color === 'BLACK') {
                    // 情况3：兄弟的右孩子为黑==左孩子为红
                    sibling.left.color = 'BLACK';//1.确保兄弟的左孩子为黑
                    sibling.color = 'RED';//2.确保兄弟为红色；//如果直接右旋（不变色）：会违反红黑树性质
                    this._rightRotate(sibling);//情况 3 的旋转是以兄弟节点为支点的右旋，目的是把兄弟的左红孩子提升为新的兄弟。旋转后，原来的左红孩子成为 P 的右孩子（新的兄弟），从而满足情况 4 的条件（新兄弟的右孩子是红色
                    sibling = x.parent.right;//4.获取新的兄弟节点，然后继续判断
                }
                // 情况4：兄弟的右孩子为红
                sibling.color = x.parent.color;//1.兄弟继承父节点的颜色（保持父节点以上的黑高不变）
                x.parent.color = 'BLACK';//2.确保父节点的颜色是黑色
                sibling.right.color = 'BLACK';//3.把兄弟节点的右孩子变成黑色
                this._leftRotate(x.parent);//4.把父节点左旋变成左子树的节点，兄弟节点变成父节点，高度平衡
                x = this.root;//5.目的：强制退出 while 循环；不需要再向上修复
            }
        } else {
            // 对称情况（x是右孩子）
            // ... 类似逻辑
        }
    }
    x.color = 'BLACK';
}

//验证操作//
isValidRedBlackTree() {
    if (this.root.color !== 'BLACK') return false;
    
    // 检查红色节点的子节点必须是黑色
    if (!this._checkRedBlackProperty(this.root)) return false;
    
    // 检查所有路径黑色高度相同
    const blackHeight = this._getBlackHeight(this.root);
    return blackHeight !== -1;
}
_checkRedBlackProperty(node) {
    if (node === this.NIL) return true; 
    if (node.color === 'RED') {
        if (node.left.color === 'RED' || node.right.color === 'RED') {
            return false;  // 红节点不能有红孩子
        }
    }
    return this._checkRedBlackProperty(node.left) && 
           this._checkRedBlackProperty(node.right);
}
_getBlackHeight(node) {//检查是否平衡左子树高度和右子树高度必须一致
    if (node === this.NIL) return 1;  // NIL叶子节点算1个黑色高度
    const leftBlackHeight = this._getBlackHeight(node.left);
    const rightBlackHeight = this._getBlackHeight(node.right);
    if (leftBlackHeight === -1 || rightBlackHeight === -1 || 
        leftBlackHeight !== rightBlackHeight) {
        return -1;//不平衡
    }
    return leftBlackHeight + (node.color === 'BLACK' ? 1 : 0);
}
```