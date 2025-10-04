# KD Tree
## 基础知识
- **KD树是k维二叉树，用于组织k维空间中的点**
- **轮流使用不同维度的坐标作为分割键，递归地将空间划分为两个半空间**
- **KD树的优点是避免了空间的均匀划分，适应数据的实际分布；缺点是树可能不平衡，取决于输入顺序**

|特性|	B树/二叉树|	KD树|
---|---|---
|比较维度|	高效管理一维有序的键值数据	|高效组织高维空间中的点数据|
|维护关系|	全局排序关系|	空间局部关系|
|搜索依据|	键值的大小比较	|空间的相对位置|
|设计目标|为一维有序数据的磁盘存储优化|为高维空间数据的空间局部性和相似性搜索优化；|
|适用查询|	找到ID=1234|	找到附近的点|
|同时解决空间搜索|O(N)|O(log N)|
|数据特性|	单维度全局排序	|数据在高维空间中只有相对位置|
|数据组织|同一个排序键来组织数据|递归地轮流选择不同维度分割超平面|
|关键操作|	数据可排序，精确查找、范围查询，顺序范围扫描（在排序键上）|	没有单一排序键，精确搜索和范围搜索,空间最近邻搜索、空间范围查询|


## 注意事项
1. **混淆点**
- **k维数据就是需要用k个特征（属性）来描述的数据点**
- **KD树能高效地在k维空间中组织数据，进行快速检索**
- **核心思想：递归地对k维数据空间进行划分**
- **进行搜索时（例如最近邻搜索），KD树能够快速排除大部分不相关的数据，避免了线性扫描所有点的开销，这在处理大量数据时非常高效**
- **回溯的范围有限:虽然搜索需要回溯，但回溯不会检查所有节点！精确的复杂度是：O(d·log N)，d是维度**
- **距离区分**
```
欧氏距离：直线距离，可能的最远距离
最小距离：要判断另一边是否有更近点，等价于判断圆是否与分割线相交，这又等价于判断半径d是否大于圆心到直线的距离h
```
- **最近邻 vs K近邻**
```
最近邻：只要找到1个最近的点
K近邻：要找到K个最近的点，而且要知道其中最远的那个
```
- **k近邻搜索**
```
//最大堆（MaxPriorityQueue）作用
获取最远点：bestList.peek().distance
移除最远点：bestList.dequeue()
添加新点：bestList.enqueue()
//不同点：
需要维护K个点，而不仅仅是1个
需要快速知道最远点作为剪枝门槛
需要高效替换：当找到更近的点时，踢掉最远的点
最大堆提供了O(log k)的高效操作
//其他事项：
最远距离是动态更新：开始很大；逐渐变小：随着找到更近的点，不断更新，门槛越来越严格；最终稳定：找到真正的前K个最近点后稳定下来
最大堆的"踢人规则"：在K近邻中，我们只维护K个点；当找到第K+1个点时，我们必须踢掉最远的那一个
用当前第K近点的距离作为几何剪枝的门槛——只有当查询点离分割线足够近（距离小于这个门槛）时，另一边才可能有更好的候选点
```
- **最近邻搜索挑战**
```
所谓的“最近邻”可能并不比随机点近多少
主要应用：多维空间关键数据搜索（如范围搜索和最近邻搜索）
本质：一种空间划分树，是二叉树在多维空间中的扩展
```

- **规则**

|核心规则|内容|作用|
| :---| :---| :---|
|**维度循环**|1.KD树通过轮流使用不同维度进行划分<br>2.划分维度：由节点深度决定 → 深度 % k|1.避免对任何一个维度的偏见，公平地对待所有维度<br>2.在搜索时能够快速剪枝，排除大量不相关的数据<br>3.与其强制高维数据适应一维排序，不如递归地在不同维度上进行划分，保持空间的自然结构<br>4.填补空间数据索引的空白<br>5.确保了KD树能够智能地在不同方向上进行搜索<br>6.每个节点在相对较浅的深度就考虑了所有维度,空间在各个方向上细分<br>5.**每个节点根据自身深度决定划分维度**:每个节点用自己的维度划分自己的子树|
|**中位数分割**|1.选择中位数 <br> 2.划分点选择:在每个节点，对当前数据集在当前划分维度上排序，选择中位数作为划分点|1.划分数据的依据<br>2.保证KD树的平衡<br>3.维持O(log N)的搜索效率<br>4.让左右子树的数据量大致相等，保持树平衡<br>|
|**搜索规则**|1.向下搜索：根据当前节点的划分维度，选择子树<br>2.到达叶子后回溯：检查"另一边"是否可能有更近点<br>3.剪枝条件：只有当到分割线的距离 > 当前最小距离(**查询点到分割线的垂直距离**)时，才能安全跳过另一边<br>|1.回溯机制：智能回溯,不遗漏任何可能的近邻<br>2.深度优先搜索
|**不均匀划分空间**|1.不强制均匀划分空间，而是让划分适应数据的实际分布<br>2.本质是让计算资源的分配与数据的实际分布相匹配<br>3. 不追求表面的整齐划一，而是追求实际的搜索效率<br>4.尊重数据的自然结构，不强加人为规则<br>5.承认数据的真实分布是不均匀的，并拥抱这种不均匀，将其转化为算法优势;<br>|1. 数据密集处细划分在数据密集的区域，KD树会递归地多次划分，创建很多小区域；搜索时可以快速排除大量候选点<br>2.数据稀疏处粗略划分在数据稀疏的区域，KD树很快停止划分，保留大区域;避免无意义的细分，节省空间和时间<br>3.在密集区域：区域小;包含的点少;搜索时检查几个点就能确定结果;剪枝效率高<br>4.在稀疏区域,虽然区域大，但点很少,即使检查整个区域，计算量也很小, 不会造成性能瓶颈|

2. 代码实现
```
//---核心逻辑---//
class KDNode {
    constructor(point, left = null, right = null) {
        this.point = point;  // [x, y] 数组
        this.left = left;    // 左子树引用
        this.right = right;  // 右子树引用
    }
}
class KDTree {
    constructor(points) {
        this.dim = points[0].length;  // 数据维度
        this.root = this._buildTree(points);
    }
    _buildTree(points, depth = 0) {
        if (points.length === 0) return null;
        // 1：选择划分维度
        const axis = depth % this.dim;//当前要使用的维度
        // 2：按当前维度排序
        points.sort((a, b) => a[axis] - b[axis]);//只比较这个维度的值；只定义比较规则
        //比较函数的返回值规则：负数 (< 0)：a应该排在b前面；正数 (> 0)：a应该排在b后面；零 (=== 0)：a和b相对位置不变
        //axis当前深度
        // 3：选择中位数点
        const mid = Math.floor(points.length/2);
        const medianPoint = points[mid];
        // 4：递归构建子树；递归分治
        const leftPoints = points.slice(0, mid);//把左半部分交给递归处理
        const rightPoints = points.slice(mid + 1);//把右半部分交给递归处理
        return new KDNode(
            medianPoint,
            this._buildTree(leftPoints, depth + 1),
            this._buildTree(rightPoints, depth + 1)
        );
    }
    // 5.启动近邻搜索//距离查询点最近的那个数据点
    nearestNeighbor(queryPoint) {//queryPoint：要查询的点
        return this._nearestNeighbor(this.root, queryPoint);//his.root：从KD树的根节点开始搜索
    }
    _nearestNeighbor(node, queryPoint, depth = 0, best = null) {
        // best 当前最近临界点
        let best = {//best参数是"当前已知的最佳结果"，随着搜索不断更新
            point: null,     // 当前找到的最近点是哪个
            distance: Infinity // 当前最近距离是多少
        };
        if (node === null) return best;
        // 1：计算要查询的点和当前最近数据点的距离
        const currentDist = this._distance(queryPoint, node.point);
        // 2. 更新best：如果没有找到任何候选点，或者当前这个点比已知的最佳点更近，那就把它设为搜索过程中暂时找到的最好结果
        if (best === null || currentDist < best.distance) {
            best = { point: node.point, distance: currentDist };
        }//让当前节点的信息立即参与后续的搜索决策，提高剪枝效率；//每一步都利用所有已知信息来指导搜索
        // 3：确定搜索方向KD树的智能前进导航并且开始搜索
        const axis = depth % this.dim;
        let nextNode, otherNode;
        if (queryPoint[axis] < node.point[axis]) {
            nextNode = node.left;
            otherNode = node.right;
        } else {
            nextNode = node.right;
            otherNode = node.left;
        }
        // 4. 搜索主要子树：委托子树继续搜索，并用它返回的可能更好的结果更新我当前的最近值
        best = this._nearestNeighbor(nextNode, queryPoint, depth + 1, best);
        // 5：回溯：判断是否需要搜索另一边
        const axisDist = Math.abs(queryPoint[axis] - node.point[axis]);
        if (axisDist < best.distance) {//axisDist查询点到分割线的垂直距离
            best = this._nearestNeighbor(otherNode, queryPoint, depth + 1, best);
        }
        return best;
    }
    _distance(point1, point2) {
        // 计算欧氏距离
        let sum = 0;
        for (let i = 0; i < point1.length; i++) {
            sum += Math.pow(point1[i] -point2[i], 2);
        }
        return Math.sqrt(sum);
    }
    //删除：
    remove(pointToRemove) {
        this.root = this._remove(this.root, pointToRemove, 0);
    }
    _remove(node, point, depth) {
        if (node === null) return null;
        
        const axis = depth % this.dim;
        
        // 1.找到要删除的节点
        if (this._pointsEqual(node.point, point)) {
            if (node.right !== null) {
                // 2.被删除的是内部节点在右子树中找到最小值替换
                const minNode = this._findMin(node.right, axis, depth + 1);
                node.point = minNode.point;
                node.right = this._remove(node.right, minNode.point, depth + 1);
            } else if (node.left !== null) {
                // 类似处理左子树...
            } else {
                return null; // 3.被删除的是叶子节点；节点已经被删除了，请父节点把指向这里的引用设为空
            }
        } else if (point[axis] < node.point[axis]) {
            node.left = this._remove(node.left, point, depth + 1);
        } else {
            node.right = this._remove(node.right, point, depth + 1);
        }
        
        return node;
    }
 
    //插入新点
    insert(newPoint) {
        this.root = this._insert(this.root, newPoint, 0);
    }
    _insert(node, newPoint, depth) {
        if (node === null) {
            return new KDNode(newPoint); // 1：创建新节点
        } 
        const axis = depth % this.dim;
        if (newPoint[axis] < node.point[axis]) {
            node.left = this._insert(node.left, newPoint, depth + 1); // 2.比较左边
        } else {
            node.right = this._insert(node.right, newPoint, depth + 1); // 3.比较右边
        }
        
        return node;
    }
    //动态操作：k近邻搜索：找到K个最近的点，而且要知道其中最远的那个
    kNearestNeighbors(queryPoint, k) {
        const bestList = new MaxPriorityQueue(); // 能快速获取/移除最大距离的数据结构；
        this._kNearestNeighbors(this.root, queryPoint, 0, bestList, k);
        return bestList.toArray();
    }
    _kNearestNeighbors(node, queryPoint, depth, bestList, k) {
        if (node === null) return;
        const currentDist = this._distance(queryPoint, node.point);
        // 1：维护大小为K的最佳列表
        if (bestList.size() < k || currentDist < bestList.bestList.peek().distance) {//查看当前最远距离
            bestList.enqueue({ point: node.point, distance: currentDist });
            if (bestList.size() > k) {
                bestList.dequeue(); // 2：移除最远的点
            }
        }
        const axis = depth % this.dim;
        let nextNode, otherNode;
        if (queryPoint[axis] < node.point[axis]) {
            nextNode = node.left;
            otherNode = node.right;
        } else {
            nextNode = node.right;
            otherNode = node.left;
        }
        this._kNearestNeighbors(nextNode, queryPoint, depth + 1, bestList, k);
        const axisDist = Math.abs(queryPoint[axis] - node.point[axis]);
        
        // 填空题7：K近邻的剪枝条件
        if (bestList.size() < k || axisDist < bestList.bestList.peek().distance) {//第K近点的距离（当前最远门槛）
            this._kNearestNeighbors(otherNode, queryPoint, depth + 1, bestList, k);
        }
    }
    //范围搜索
    rangeSearch(queryLow, queryHigh) {
        const results = [];
        this._rangeSearch(this.root, queryLow, queryHigh, 0, results);
        return results;
    }
    _rangeSearch(node, low, high, depth, results) {//low 和 high - 查询区域的边界
        //node - 当前处理的节点；low和high-查询区域的边界；depth-当前深度；results-结果收集器
        if (node === null) return;
        const point = node.point;
        let inRange = true;
        // 1：检查点是否在查询范围内
        for (let i = 0; i < this.dim; i++) {
            if (point[i] < low[i] ||  point[i]> high[i]) {
                inRange = false;
                break;
            }
        }
        if (inRange) {
            results.push(point);
        }
        const axis = depth % this.dim;
        // 2：判断是否需要搜索左子树
        if (low[axis] <= node.point[axis]) {//查询区域是否与左子树区域有重叠//low[axis]不是范围而是边界值
            this._rangeSearch(node.left, low, high, depth + 1, results);
        }
        // 3：判断是否需要搜索右子树
        if (high[axis] >= node.point[axis]) {//检查区域是否有重叠;判断空间区域的重叠关系，不是判断点的包含关系
            this._rangeSearch(node.right, low, high, depth + 1, results);
        }
    }
 }
```
```
//--测试--//
class KDNode {
    constructor(point, left = null, right = null) {
        this.point = point;
        this.left = left;
        this.right = right;
    }
}

class KDTree {
    constructor(points) {
        if (points.length === 0) throw new Error("Points cannot be empty");
        this.dim = points[0].length;
        this.root = this._buildTree(points);
    }
    
    _buildTree(points, depth = 0) {
        if (points.length === 0) return null;
        
        const axis = depth % this.dim;
        
        // 注意：这里要复制数组，避免修改原数组
        const pointsCopy = [...points];
        pointsCopy.sort((a, b) => a[axis] - b[axis]);
        
        const mid = Math.floor(pointsCopy.length / 2);
        const medianPoint = pointsCopy[mid];
        
        const leftPoints = pointsCopy.slice(0, mid);
        const rightPoints = pointsCopy.slice(mid + 1);
        
        return new KDNode(
            medianPoint,
            this._buildTree(leftPoints, depth + 1),
            this._buildTree(rightPoints, depth + 1)
        );
    }
    
    nearestNeighbor(queryPoint) {
        return this._nearestNeighbor(this.root, queryPoint);
    }
    
    _nearestNeighbor(node, queryPoint, depth = 0, best = null) {
        if (node === null) return best;
        
        const currentDist = this._distance(queryPoint, node.point);
        if (best === null || currentDist < best.distance) {
            best = { point: node.point, distance: currentDist };
        }
        
        const axis = depth % this.dim;
        let nextNode, otherNode;
        if (queryPoint[axis] < node.point[axis]) {
            nextNode = node.left;
            otherNode = node.right;
        } else {
            nextNode = node.right;
            otherNode = node.left;
        }
        
        best = this._nearestNeighbor(nextNode, queryPoint, depth + 1, best);
        
        const axisDist = Math.abs(queryPoint[axis] - node.point[axis]);
        if (axisDist < best.distance) {
            best = this._nearestNeighbor(otherNode, queryPoint, depth + 1, best);
        }
        
        return best;
    }
    
    _distance(point1, point2) {
        let sum = 0;
        for (let i = 0; i < point1.length; i++) {
            sum += Math.pow(point1[i] - point2[i], 2);
        }
        return Math.sqrt(sum);
    }
    
    // 可视化方法
    printTree(node = this.root, depth = 0) {
        if (!node) return;
        const indent = '  '.repeat(depth);
        const axis = depth % this.dim;
        console.log(`${indent}深度${depth}: [${node.point}] (划分维度: ${axis})`);
        this.printTree(node.left, depth + 1);
        this.printTree(node.right, depth + 1);
    }
}

// === 测试 ===
console.log("🚀 开始KD树测试...");
// 测试数据
const points = [[2,3], [5,4], [9,6], [4,7], [8,1], [7,2]];
console.log("📊 数据点:", points);
// 构建KD树
const tree = new KDTree(points);
console.log("🌳 树结构:");
tree.printTree();
// 测试查询
const query = [6,5];
console.log("🔍 查询点:", query);
const result = tree.nearestNeighbor(query);
console.log("✅ 最近邻:", result);
console.log("🎉 测试完成！");
```