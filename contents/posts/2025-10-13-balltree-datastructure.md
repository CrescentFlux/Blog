# Balltree
## 基础知识
- **定义**
```
是一种基于层次化球体划分的空间数据结构，专门用于高维空间中的相似性搜索。其核心思想是通过递归地将数据空间划分为嵌套的超球体，从而实现对最近邻搜索的高效支持。本质是一种层次化的空间数据结构，通过**嵌套球体**来组织高维数据，专门为解决维度诅咒问题而设计。
```

- **Ball Tree 节点**

    - 一个 Ball Tree 节点 N 可以形式化地表示为四元组：
    - N = (P, c, r, {N_l, N_r})
    其中：

        P = {p₁, p₂, ..., p_m} 是节点包含的 d 维数据点集，p_i ∈ R^d

        c ∈ R^d 是节点的球心（pivot）

        r ∈ R^+ 是节点的半径（radius）

        {N_l, N_r} 是左右子节点（叶节点时为空集）

- **几何参数计算**
   - **定义2（球心计算）**：
   -  对于点集 P，球心 c 通过算术均值计算：
    - c = (1/|P|) * Σ_{p∈P} p

   - 分量形式：
    - c_j = (1/m) * Σ_{i=1}^m p_ij, 对于所有 j = 1, ..., d

   - **定义3（半径计算）**：
   - 半径 r 确保所有点都在超球体内：
    - r = max_{p∈P} ||p - c||_2

     - 其中 ||·||_2 表示欧几里得范数

   - **定义 4（球心对选择）**：
    - 函数 select_pivots(P) 通常采用以下策略：

        - 随机选择：从 P 中随机选择两个点

        - 最远点对：选择满足 argmax_{p,q∈P} ||p - q||_2 的点对

        - 采样优化：从 P 的随机子集中选择最远点对

- **定理 1（球体剪枝条件）**：
```
对于查询点 q 和 Ball Tree 节点 N = (P, c, r, {N_l, N_r})，如果：
||q - c||_2 - r > d_current
其中 d_current 是当前找到的最近邻距离，那么节点N的所有子节点都不可能包含更近的节点
证明：
对于任意 p ∈ P，由三角不等式：
||q - p||_2 ≥ ||q - c||_2 - ||p - c||_2 ≥ ||q - c||_2 - r
因此，如果 ||q - c||_2 - r > d_current，则所有 p ∈ P 都满足 ||q - p||_2 > d_current。
```
## 注意事项
1. **混淆点**

- **适用场景理论对比**

|场景|	Ball Tree|	KD Tree|	推荐选择|
---|---|---|---
|低维数据(<20维)|	可选|	推荐	|KD树更简单高效|
|高维数据(>100维)|	推荐	|谨慎使用	|Ball Tree优势区|
|数据分布均匀|	良好	|优秀	|KD树表现更好|
|数据有聚类	|优秀|	良好|	Ball Tree更合适|
|批量查询|	优秀|	良好|	构建一次多次使用|
|动态更新|	复杂|	相对简单|	KD树更容易维护|



- **性能特征对比**

|指标	|Ball Tree|	KD Tree|	关键发现|
---|---|---|---
|构建时间复杂度|	O(dn log n)	|O(dn log n)	|理论相同，实际Ball Tree更慢|
|搜索时间复杂度|	O(log n)	|O(log n)|	但常数项差异很大|
|内存占用|	较高|	较低|	优化版改善明显|
|常数因子|	较大	|较小|	实际性能的关键|
|最差情况|	相对稳定|	可能退化|	KD树在特定数据中表现差|






-  **Ball Tree vs KD Tree 终极对比表**

|特性|	Ball Tree|	KD Tree	|真实性能|
---|---|---|---
|构建时间	|较慢 	|较快	|在JS中差异明显，Python库中差距缩小|
|搜索性能	|稳定 	|波动 |	KD树在友好数据中可能更快|
|高维表现	|理论优 |	理论差 	|需要1000+维才明显|
|数据分布|	无关性 	|轴对齐不依赖 |	但对角线测试中KD树仍很快|
|内存使用	|较高	|较低 	|优化版大幅改善了这点|
|实现复杂度	|复杂 |	简单	|调试Ball Tree确实很复杂|
|批量查询|	优势明显 |	表现良好 |	构建一次，查询多次的场景|
|剪枝效率|	几何剪枝 	|坐标剪枝 	|Ball Tree剪枝更智能|
|划分策略|	球体划分| 	轴对齐划分 |	Ball Tree更符合几何直觉|












2. **代码实现**
```
//=========================🔄基础balltree实现========================//
//----计算平方差-----//
function distance(a, b) {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
        sum += Math.pow(a[i] - b[i], 2); // 计算平方差,欧氏距离是差的平方和，不是各自平方和
    }
    return Math.sqrt(sum);
}
//---找到数据集的中心点（球心）---//
function findPivot(points) {
    if (points.length === 0) return null;
    //1.确定点的维度
    const dim = points[0].length;
    //2.初始化球心数组，全填0
    const pivot = new Array(dim).fill(0);
    //3.外层循环：遍历每个维度
    for (let i = 0; i < dim; i++) {
        let sum = 0;
        //4.内层循环：累加所有点在第i维的值
        for (const point of points) {
            sum += point[i] //累加第i维的值//取每个点的第i个坐标值//逐维度计算平均值//球心 = 所有点在每个维度上的平均值
        }
        //5.计算该维度的平均值
        pivot[i] = sum / points.length;//🎯关键区别：点的数量 vs 点的维度：每个维度的和要除以点的总数//有多少个点，就除以多少
    }
    return pivot;
}
//---计算球体半径---//
function calculateRadius(points, pivot) {//🎯计算能够包裹所有点的最小球体的半径//找到离球心最远的那个点，它到球心的距离就是半径。
    let maxDistance = 0;//1.初始化最大距离为0
    for (const point of points) {//2.遍历每个点
        const dist = distance(point, pivot); //3.计算当前点到球心的距离
        maxDistance = Math.max(maxDistance, dist); //4.更新最大距离
    }
    return maxDistance;//5.返回最大的距离作为半径
}
class BallTreeNode {
    //节点结构定义
    constructor(points) {
        this.points = points; // 该节点包含的数据点:points 在构建阶段和搜索阶段有着完全不同的意义:✅阶段一：构建阶段（需要 points）1. 计算球心(pivot)2. 计算半径(radius)  3.划分数据到左右子树//内部节点的 points 在构建完成后就不再使用，但依然占用内存。在实际实现中，我们通常在构建完成后释放内部节点的points✅阶段二：搜索阶段（不需要内部节点points）:只在叶节点使用points进行暴力搜索
        this.pivot =findPivot(points); //✅当points数量小于leafSize阈值时为true, 说明它是叶节点，不再继续分割；✅为false时说明它是内部节点，需要继续分割，节点包含左右子树，不直接存储数据点//✅isLeaf应该是布尔值，不是null//✅根据点数判断是否为叶节点
        //🚨这里调用this.findPivot//球心：球心(Pivot),节点内所有点的中心（均值点）,每个维度分别求平均值,定义球体的中心位置
        this.radius =calculateRadius(points, this.pivot);// 半径：半径(Radius),从球心到最远点的距离,max(distance(point, pivot)),确保所有点都在球体内
        this.left = null;     // 左子树
        this.right = null;    // 右子树
        // ✅简单处理：点数<=1就是叶节点
        this.isLeaf = points.length <= 1;
    }}
    //在 BallTreeNode 中定义工具方法
   /*  this.pivot = this.findPivot(points);this.radius =this.calculateRadius(points, this.pivot)
   findPivot(points) {
        if (points.length === 0) return null;
        const dim = points[0].length;
        const pivot = new Array(dim).fill(0);
        for (let i = 0; i < dim; i++) {
            let sum = 0;
            for (const point of points) {
                sum += point[i];
            }
            pivot[i] = sum / points.length;
        }
        return pivot;
    }
    calculateRadius(points, pivot) {
        let maxDistance = 0;
        for (const point of points) {
            const dist = distance(point, pivot);
            maxDistance = Math.max(maxDistance, dist);
        }}
        return maxDistance;*/
    
    //-------💡注意------//
        //1.核心结构
            //Ball Tree的每个节点代表一个超球体 ，它由球心和半径定义
            //球心或pivot是节点中所有数据的中心点
            //半径或radius是从球心到最远数据点的距离，确保所有数据都在球体内
        //2.构建过程
            //构建Ball Tree时，我们递归地将数据划分为两个子球体或子节点 ，直到每个叶节点包含的数据点少于某个阈值
            //选择两个初始球心的常见方法是找到数据集中相距最远的两个点
        //3.搜索算法
           //搜索时，我们使用点到球体距离来估计查询点到节点内任何点的最小可能距离
           //为了优化搜索顺序，我们应该先搜索距离更近或更可能有最近邻的子树//Ball Tree的搜索是深度优先的，但访问子节点的顺序很重要：更可能找到近邻：距离球心近的子树，更可能包含近距离的点，更快更新best_dist：尽早找到更小的best_dist，后续剪枝更有效，减少搜索范围：如果左子树就找到了很近的点，右子树可能被整体剪枝
        //4.剪枝条件：如果 distance(q, pivot) - radius > best_dist，那么跳过整个节点或剪枝该分支
        

    //--------❌注意-------//
    //🔍Uncaught ReferenceError: leafSize is not defined：这里leafSize是参数，但是在 buildTree 中调用时：if (points.length <= this.leafSize) {//这里用this.leafSize，🚨但没有传递leafSize参数！
    //this.isLeaf =  points.length <= leafSize;//🚨这里leafSize是参数
    //主要问题是在创建 BallTreeNode时没有传递leafSize参数:在创建节点时传递leafSize；在BallTreeNode中直接使用固定值
    //leafSize 在 BallTree 类中定义，但 BallTreeNode 是另一个类，它们不共享变量：
    //🎯别的参数不用传:其他参数（如 pivot, radius）都是在节点内部计算的，而 isLeaf 需要依赖外部规则（leafSize）
    //✅1.不传递 leafSize:this.isLeaf = points.length <= 1;在 BallTree 中判断，不在 BallTreeNode 中判断
    //✅2.在 BallTree 中统一控制:
    //class BallTreeNode {constructor(points, isLeaf = false) {//✅接收isLeaf状态}2.this.isLeaf = isLeaf; //✅由外部控制class BallTree {const node = new BallTreeNode(points, isLeaf);  // ✅ 传递状态
    //✅3.class BallTreeNode {this.isLeaf = true;//✅默认都是叶节点，让 BallTree 来覆盖}//✅在BallTree中控制叶节点逻辑,if (points.length <= this.leafSize) 
    //🔍Uncaught TypeError: this.findPivot is not a function:findPivot 方法在 BallTreeNode 类中没有正确定义//this.pivot = null;
    //🎯工具函数 findPivot 和 calculateRadius 是通用的，不应该绑定到特定的类，这样代码更清晰且可复用
    //🎯BallTreeNode 构造函数中计算的只是基于当前点的，但内部节点需要基于整个子树的
    //✅1.在 BallTreeNode 中定义工具方法
    //✅2.使用外部函数（推荐，避免代码重复）调用外部函数，不加 this.
    //✅3：在 BallTree 中计算并传递:constructor(points, pivot, radius)//接收计算好的值,const pivot = this.findPivot(points);//✅在BallTree中计算const radius = this.calculateRadius(points, pivot); const node = new BallTreeNode(points, pivot, radius);//✅传递计算好的值
    //✅4:删掉tree类中参数的重复计算

class BallTree {
    //===1.构建Ball Tree//
    //把一堆杂乱的点，组织成层次化的球体结构
    constructor(points, leafSize = 1) {
        this.leafSize = leafSize; // 步骤1：保存配置参数
        this.root = this.buildTree(points);// 步骤2：构建树结构
    }
    //===2.创建树结构===//
    buildTree(points) {
        console.log("构建节点，点数:", points.length); // 调试信息
        // 安全检查
        if (!points || points.length === 0) {
            console.warn("空数据点集");
            return null;
        }
        //1. 终止条件：点数够少就变成叶节点
        if (points.length <= this.leafSize) { // ✅ 在 BallTree 中判断，不在 BallTreeNode 中判断
            return new BallTreeNode(points);// 叶节点会在构造函数中计算pivot和radius
        }
        // 2. 找到两个"代表点"（相距最远的两个点）
        const [pivot1, pivot2] = this.findFarthestPoints(points)// 调用找最远点函数//findFarthestPoints - 找最远点对//✅优化思想：完全计算所有点对太耗时(O(n²))，采样计算近似最远点就够了
        // 3. 根据离哪个代表近，把点分成两组
        const [leftPoints, rightPoints] = this.splitPoints(//splitPoints - 数据划分//几何意义：用两个球心的垂直平分线来划分空间
        //垂直平分线的性质：线上的任何点到A和B的距离相等；线左侧的点：离A更近；线右侧的点：离B更近
        //Ball Tree通过计算每个点到两个球心的距离，实际上是在用隐式的垂直平分超平面把空间分成两半，让相似的点（离同一个球心近的点）聚集在一起
            points, pivot1, pivot2
        );
        // 安全检查：确保划分后没有空数据集
        if (leftPoints.length === 0 || rightPoints.length === 0) {
            console.warn("划分后出现空数据集，创建叶节点");
            return new BallTreeNode(points);
        }
        //4.递归构建子树
        const node = new BallTreeNode(points);
        //5.关键：计算当前节点的球心和半径
        //🗑️🚨删除这两行 - 因为 BallTreeNode 构造函数已经计算过了否则会出现：this.findPivot is not a function
        //node.pivot = this.findPivot(points);    // 计算当前节点所有点的中心
        //node.radius = this.calculateRadius(points, node.pivot); // 计算半径
        //分而治之：把大问题分解成小问题，分别处理后再组合
        node.left = this.buildTree(leftPoints);//处理左边点
        node.right = this.buildTree(rightPoints);//处理右边点
        //递归：处理任意规模的数据，自动产生层次结构，确保每个叶节点都满足条件：通过递归，最终每个叶节点的点数都 ≤ leafSize，保证搜索效率
        //用同样的方法处理更小的问题，直到问题简单到可以直接解决
        return node;
        //---❌注意---//
        //🔍Uncaught TypeError: can't access property "pivot", node.left is null：说明在某些情况下，递归构建时子节点创建失败了
        //✅修复搜索方法：问题在于搜索时没有检查子节点是否存在
    }
    
    //===3.找到数据集中相距最远的两个点===//
    findFarthestPoints(points) {
        let maxDistance = -1;
        let pivot1 = points[0], pivot2 = points[0];
        // 采样部分点以减少计算量
        const sampleSize = Math.min(50, points.length);//限制检查范围
        for (let i = 0; i < sampleSize; i++) {//双重循环：两两比较//让每个点(i)都和其他所有点(j)比一比距离
            for (let j = i + 1; j < sampleSize; j++) {
                const dist = distance(points[i], points[j]); //计算两点距离
                if (dist > maxDistance) { // 如果比当前最远还远
                    maxDistance = dist;//更新最远距离记录
                    pivot1 = points[i];//记下第一个点
                    pivot2 = points[j];//记下第二个点
                }
            }
        }
        return [pivot1, pivot2];
        //---❌注意---//
        //Uncaught ReferenceError: findFarthestPoints is not defined：
        //✅1.方法定义位置错误：错误：方法定义在类外部；✅2.方法作用域问题：错误：直接调用 findFarthestPoints，没有 this.；✅方法定义语法错误：错误：缺少 function 关键字或方法语法


    }
    //=====4.根据距离划分点到两个子集=====//
    //核心划分逻辑//自然聚类//平衡性好//为递归构建做准备
    splitPoints(points, pivot1, pivot2) {
        const leftPoints = [];
        const rightPoints = [];
        for (const point of points) {
            //测量到队长A的距离
            const distToPivot1 = distance(point, pivot1);
            //测量到队长B的距离 
            const distToPivot2 = distance(point, pivot2);  
            // 决定站哪一队
            if (distToPivot1 < distToPivot2) { //判断条件:离哪个球心近就分到哪边
                leftPoints.push(point);//离A近，站左队
            } else {
                rightPoints.push(point);//离B近（或相等），站右队
            }
        }
        return [leftPoints, rightPoints];
    }
//========5.搜索算法=========//
// 在Ball Tree中搜索最近邻//聪明地决定去哪找，发现没必要就果断放弃//通过智能的导航和大胆的剪枝，在保证结果正确的前提下大幅提升搜索效率
//先近后远：更可能快速找到近的点，提升后续剪枝效果//球体剪枝：利用几何性质快速排除整个区域//渐进优化：随着找到更近的点，剪枝越来越有效
findNearest(query, k = 1) {
    let best = [];
    this._search(this.root, query, k, best);
    return best;
}
_search(node, query, k, best) {
    //node - 当前搜索的节点，可以是根节点（开始搜索）内部节点（决定搜索方向）叶节点（实际比较数据点）；query - 查询点：要找最近邻的那个点，在Ball Tree中找到离这个点最近的那些点
    //k - 要找的最近邻数量：要找前K个最近的点；best - 当前最佳候选列表：到目前为止找到的最近邻候选点（按距离排序）始终按distance从小到大排序，在递归搜索过程中不断更新
    //区分了导航信息（子树球心）和实际数据（子树内的点），通过几何计算确保不会漏掉任何可能的最近邻
    //不过度保守，不过度激进，用几何保证正确性
    //🎯叶节点：暴力搜索所有点 
    if (node.isLeaf) {
        // 叶节点：暴力搜索所有点
        for (const point of node.points) {
            this._updateBest(point, query, k, best);
        }
        return;
    }
    //🎯内部节点：导航 + 剪枝逻辑
    // 1.计算到左右子树的距离
    // 🚨问题：没有检查left和right是否存在//node.left 可能为 null!// node.right 可能为 null!
    // ✅修复：添加空值检查
    if (!node.left || !node.right) {
        //如果某个子节点不存在，只搜索存在的子节点//
        if (node.left) this._search(node.left, query, k, best);
        if (node.right) this._search(node.right, query, k, best);
        return;
    }
    const distToLeft = distance(query, node.left.pivot);//distToLeft/Right：到子树球心的距离（用于决定搜索顺序）
    const distToRight =distance(query, node.right.pivot);//计算到右子树的距离
    // 2.决定搜索顺序：先近后远
    let first, second;
    if (distToLeft < distToRight) { //判断哪个更近
        first = node.left;
        second = node.right;//实际上，第二个子树经常被跳过（剪枝）
    } else {
        first = node.right;
        second = node.left;
    }
    //3.搜索更近的子树
    this._search(first, query, k, best);
    //4.计算到第二个子树的最小可能距离
    const minDistToSecond = distance(query, second.pivot) - second.radius; //查询点到第二个子树中最近可能点的最小距离
    //查询点距离第二个子树球体的最近可能距离//minDistToSecond：到子树内任何点的最小可能距离（用于剪枝判断）
    //子树球心 ≠ 子树内的数据点：左子树的球心可能靠近查询点，但左子树内部的数据点可能很远；右子树的球心可能较远，但右子树内部的数据点可能很近
    //不是在比较"距离子树球心的远近"，而是在比较"距离子树内实际数据点的远近"
    //5.获取"当前找到的第K近邻的距离"作为剪枝标准
    const worstBestDist = best.length > 0 ? best[best.length - 1].distance : Infinity;//当前已找到的候选点中，距离最远的那一个的距离//现在找到的候选点中，最差的那个有多远
    //best.length > 0 ? ... : Infinity：如果已经找到候选点 → 取最后一个点的距离，如果还没找到任何点 → 用无穷大（表示没有限制）；
    //best[best.length - 1].distance：best 数组按距离从小到大排序，最后一个元素就是当前找到的第K远的点
    //动态更新的剪枝标准：随着搜索的进行，worstBestDist 会越来越小，剪枝越来越严格； 适用于K近邻搜索：不只是找最近邻，而是找前K个最近邻；渐进优化：算法越往后搜索，剪枝条件越苛刻，效率越高！
    if (minDistToSecond < worstBestDist) { // 剪枝条件// 如果最小可能距离比当前最佳还小，才需要搜索//如果 右边最好的 < 左边最差的：说明右边可能有比左边当前候选更好的点，需要去右边搜索确认
        this._search(second, query, k, best);
    }
}
//-----更新最佳候选列表--------//
// 维护一个有序的最优候选列表
//高效维护有序列表，动态更新，内存友好：只保留K个点，不无限增长
_updateBest(point, query, k, best) {
    const dist = distance(point, query);
    const candidate = { point, distance: dist };
    //1.将候选点插入到正确位置
    let i = 0;
    while (i < best.length && best[i].distance < dist) {//从前往后找，找到第一个比新点距离更远的位置
        i++;
    }
    //2.插入新点
    best.splice(i, 0, candidate);
    //3.保持只保留前k个：如果榜单超过K个，淘汰最后一名
    if (best.length > k) {
        best.pop();
    }
}
}
// 简单的测试代码
function testBallTree() {
    console.log("🚀 开始测试 Ball Tree...\n");
    
    // 测试数据：6个简单的二维点
    const points = [
        [1, 1], [2, 2], [3, 3],
        [7, 7], [8, 8], [9, 9]
    ];
    
    console.log("📊 测试数据:", points);
    
    // 创建Ball Tree
    const ballTree = new BallTree(points, 2); // leafSize=2
    
    console.log("✅ Ball Tree 创建成功");
    console.log("根节点球心:", ballTree.root.pivot);
    console.log("根节点半径:", ballTree.root.radius.toFixed(2));
    console.log("根节点是叶节点?", ballTree.root.isLeaf);
    
    // 测试搜索
    console.log("\n🔍 测试搜索功能:");
    
    // 测试1：搜索靠近左下角的点
    const query1 = [1.5, 1.5];
    const result1 = ballTree.findNearest(query1, 1);
    console.log(`查询点: [${query1}]`);
    console.log("最近邻:", result1[0].point, "距离:", result1[0].distance.toFixed(2));
    
    // 测试2：搜索靠近右上角的点
    const query2 = [8.5, 8.5];
    const result2 = ballTree.findNearest(query2, 1);
    console.log(`\n查询点: [${query2}]`);
    console.log("最近邻:", result2[0].point, "距离:", result2[0].distance.toFixed(2));
    
    // 测试3：搜索3个最近邻
    const query3 = [5, 5];
    const result3 = ballTree.findNearest(query3, 3);
    console.log(`\n查询点: [${query3}], 找3个最近邻:`);
    result3.forEach((item, index) => {
        console.log(`  第${index + 1}近: [${item.point}], 距离: ${item.distance.toFixed(2)}`);
    });
    
    console.log("\n🎉 测试完成！");
}

// 运行测试
testBallTree();

//=============================🔄批量查询测试========================//
function batchQueryTest() {
    console.log("📊 批量查询测试");
    
    const points = [
        [1,1], [2,2], [3,3], [4,4], [5,5],
        [6,6], [7,7], [8,8], [9,9], [10,10]
    ];
    
    const ballTree = new BallTree(points, 2);
    
    // 批量查询多个点
    const queries = [
        [1.5, 1.5], [5.5, 5.5], [9.5, 9.5],
        [3.2, 3.2], [7.8, 7.8]
    ];
    
    console.time("批量Ball Tree搜索");
    const allResults = queries.map(query => 
        ballTree.findNearest(query, 3)
    );
    console.timeEnd("批量Ball Tree搜索");}
batchQueryTest();


//===========================🔄动态更新=============================//
// Ball Tree的动态更新（简化版）
class DynamicBallTree extends BallTree {//DynamicBallTree 扩展了基础 Ball Tree，增加了动态更新能力
    //基础 Ball Tree：一次性构建，静态结构；DynamicBall Tree：支持动态插入，自适应平衡
    //1. 插入新点
    insert(point) {
        // 找到合适的叶节点插入
        this._insertToNode(this.root, point);
        // 如果节点过大，重新平衡
        if (this.root.points.length > this.leafSize * 10) {
            this.root = this.buildTree(this.getAllPoints());// 完全重建
            //渐进式更新：叶节点：直接更新，开销小；内部节点：只更新导航信息，不改变结构；定期重建：防止结构退化
        }
    }
    //2. 递归插入逻辑
    _insertToNode(node, point) {
        // 叶节点：直接添加并更新几何属性
        if (node.isLeaf) {
            node.points.push(point);
            // 更新球心和半径
            node.pivot = findPivot(node.points);
            node.radius = calculateRadius(node.points, node.pivot);
        } else {
             // 内部节点：导航到合适的子树
            const distToLeft = distance(point, node.left.pivot);
            const distToRight = distance(point, node.right.pivot);
            
            if (distToLeft < distToRight) {
                this._insertToNode(node.left, point);
            } else {
                this._insertToNode(node.right, point);
            }
        }
    }
    getAllPoints() { //入口函数
        // ✅ 最简单方案：只返回根节点的points
        // 因为根节点已经包含了所有数据
        if (this.root && this.root.points) {
            return [...this.root.points]; // 返回副本，避免修改原数据
        }
        return [];
    /*
        const points = []; // 1. 创建空数组
        this._collectPoints(this.root, points);// 2. 从根节点开始收集
        return points;// 3. 返回所有点*/
    }
    
    _collectPoints(node, points) {
    // ✅ 最简单修复：如果节点为空，直接返回
    if (!node) return;
    // ✅ 关键：只在叶节点收集数据
    if (node.isLeaf && node.points && node.points.length > 0) {
        points.push(...node.points);
        return; // 叶节点没有子节点，直接返回
    }
    // ✅ 如果节点有points，直接用它（不管是不是叶节点）
    if (node.points && node.points.length > 0) {
        points.push(...node.points);
    }
    
    // ✅ 如果有子节点，继续收集（但不再依赖isLeaf判断）
    if (node.left) this._collectPoints(node.left, points);
    if (node.right) this._collectPoints(node.right, points);
}
}
function quickTest() {
    console.log("⚡ 快速测试");
    
    const points = [[1,1], [2,2], [3,3], [4,4]];
    const ballTree = new DynamicBallTree(points, 2);
    
    // 不管树结构如何，直接收集所有能找到的点
    const collected = ballTree.getAllPoints();
    console.log("收集到的点:", collected.length);
    console.log("应该能收到一些点，不一定是全部");
}

quickTest();
function verifyFix() {
    console.log("✅ 验证修复");
    
    const points = [[1,1], [2,2], [3,3], [4,4]];
    const ballTree = new DynamicBallTree(points, 2);
    
    const collected = ballTree.getAllPoints();
    console.log("原始数据:", points.length, "个点");
    console.log("收集到的:", collected.length, "个点");
    console.log("应该相等:", points.length === collected.length);
    
    // 检查内容
    const originalSet = new Set(points.map(p => p.join(',')));
    const collectedSet = new Set(collected.map(p => p.join(',')));
    console.log("内容一致:", originalSet.size === collectedSet.size);
}

verifyFix();
/*从构建日志看：根节点：4个点，左子树：2个点，右子树：2个点内部节点也存储了所有points的副本，导致了重复收集//只返回根节点的points
我们的Ball Tree设计中，每个节点都存储了完整的数据副本：根节点：4个点，左子节点：2个点（但其实是根节点数据的子集），右子节点：2个点（也是根节点数据的子集）
这导致了：内存浪费 - 数据被多次存储，数据不一致风险 - 更新时容易出错，收集逻辑混乱 - 不知道哪个是权威数据源
*/
/*测试1：基础功能验证
function testGetAllPoints() {
    console.log("🧪 测试 getAllPoints()");
    
    const points = [[1,1], [2,2], [3,3], [4,4]];
    const ballTree = new DynamicBallTree(points, 2);
    
    const collectedPoints = ballTree.getAllPoints();
    console.log("原始数据:", points);
    console.log("收集的数据:", collectedPoints);
    console.log("数据一致:", points.length === collectedPoints.length);
    console.log("内容一致:", JSON.stringify(points) === JSON.stringify(collectedPoints));
}
//测试2：插入后验证
function testAfterInsert() {
    console.log("🧪 测试插入后数据收集");
    const initialPoints = [[1,1], [2,2]];
    const dynamicTree = new DynamicBallTree(initialPoints, 2);
    console.log("初始数据:", dynamicTree.getAllPoints());
    // 插入新点
    dynamicTree.insert([3,3]);
    console.log("插入后数据:", dynamicTree.getAllPoints());
    
    // 再插入一个
    dynamicTree.insert([4,4]);
    console.log("再插入后数据:", dynamicTree.getAllPoints());
    
    console.log("最终应该有4个点:", dynamicTree.getAllPoints().length === 4);
}
//测试3：复杂树结构验证
function testComplexTree() {
    console.log("🧪 测试复杂树结构");
    // 创建多层树结构
    const points = [
        [1,1], [2,2], [3,3], [4,4],
        [5,5], [6,6], [7,7], [8,8]
    ];
    const dynamicTree = new DynamicBallTree(points, 2);
    const collected = dynamicTree.getAllPoints();
    console.log("期望8个点，实际:", collected.length);
    
    // 验证所有点都存在
    const pointSet = new Set(points.map(p => p.join(',')));
    const collectedSet = new Set(collected.map(p => p.join(',')));
    console.log("所有点都存在:", pointSet.size === collectedSet.size);
    
    // 插入测试
    dynamicTree.insert([9,9]);
    console.log("插入后点数:", dynamicTree.getAllPoints().length);
}

// 运行所有测试
testGetAllPoints();
console.log("\n");
testAfterInsert(); 
console.log("\n");
testComplexTree();*/

/*🚀使用场景：这个设计在数据流和在线学习场景中很有价值，但需要仔细调优平衡阈值
const dynamicTree = new DynamicBallTree(initialPoints);
// 流式数据场景
dataStream.on('data', (newPoint) => {
    dynamicTree.insert(newPoint);  // 动态更新
    const neighbors = dynamicTree.findNearest(queryPoint); // 实时查询
});
// 增量学习场景
for (let i = 0; i < newData.length; i++) {
    dynamicTree.insert(newData[i]); // 逐步增强
}*/
/*⚠️ 潜在问题
    球体可能不紧致 - 多次插入后球体可能变得松散
    重建开销 - 定期完全重建可能很昂贵
    并发问题 - 插入时查询可能得到不一致结果*/
//=============================💡工业级版本========================//
class OptimizedBallTree {
    constructor(points, leafSize = 10) {
        this.points = points;           // 唯一数据源
        this.leafSize = leafSize;       // 叶节点大小
        this.indices = Array.from({length: points.length}, (_, i) => i); // 索引数组
        this.root = this._buildTree(0, points.length);
    }
    _buildTree(start, end) {
        const count = end - start;
        
        // 叶节点：直接存储索引范围
        if (count <= this.leafSize) {
            return {
                type: 'leaf',
                start, end,
                pivot: this._calculatePivot(start, end),
                radius: this._calculateRadius(start, end)
            };
        }
        
        // 内部节点：划分并递归构建
        const splitIndex = this._partition(start, end);
        
        return {
            type: 'node', 
            pivot: this._calculatePivot(start, end),
            radius: this._calculateRadius(start, end),
            left: this._buildTree(start, splitIndex),
            right: this._buildTree(splitIndex, end)
        };
    }
    
    _partition(start, end) {
        // 选择两个距离最远的点作为pivot
        const [pivot1, pivot2] = this._findFarthestPoints(start, end);
        
        // 原地划分：根据距离分配到左右两边
        let i = start;
        let j = end - 1;
        
        while (i <= j) {
            const dist1 = this._pointDistance(this.indices[i], this.indices[pivot1]);
            const dist2 = this._pointDistance(this.indices[i], this.indices[pivot2]);
            
            if (dist1 < dist2) {
                i++;
            } else {
                // 交换索引
                [this.indices[i], this.indices[j]] = [this.indices[j], this.indices[i]];
                j--;
            }
        }
        
        return i;
    }
    
    _findFarthestPoints(start, end) {
        const sampleSize = Math.min(20, end - start);
        let maxDist = -1;
        let pivot1 = start, pivot2 = start;
        
        // 采样找最远点对
        for (let i = 0; i < sampleSize; i++) {
            const idx1 = start + Math.floor(Math.random() * (end - start));
            const idx2 = start + Math.floor(Math.random() * (end - start));
            const dist = this._pointDistance(this.indices[idx1], this.indices[idx2]);
            if (dist > maxDist) {
                maxDist = dist;
                pivot1 = idx1;
                pivot2 = idx2;
            }
        }
        return [pivot1, pivot2];
    }
    
    _calculatePivot(start, end) {
        const dim = this.points[0].length;
        const pivot = new Array(dim).fill(0);
        
        for (let i = 0; i < dim; i++) {
            let sum = 0;
            for (let j = start; j < end; j++) {
                sum += this.points[this.indices[j]][i];
            }
            pivot[i] = sum / (end - start);
        }
        return pivot;
    }
    
    _calculateRadius(start, end) {
        const pivot = this._calculatePivot(start, end);
        let maxDist = 0;
        
        for (let i = start; i < end; i++) {
            const dist = this._pointDistanceToPivot(this.indices[i], pivot);
            maxDist = Math.max(maxDist, dist);
        }
        return maxDist;
    }
    
    _pointDistance(i, j) {
    const a = this.points[i];
    const b = this.points[j];
    
    // ✅ 添加边界检查
    if (!a || !b) {
        console.warn(`无效索引: i=${i}, j=${j}, points长度=${this.points.length}`);
        return Infinity; // 返回很大的距离
    }
    
    let sum = 0;
    for (let k = 0; k < a.length; k++) {
        const diff = a[k] - b[k];
        sum += diff * diff;
    }
    return Math.sqrt(sum);
}
    
    _pointDistanceToPivot(i, pivot) {
    const a = this.points[i];
    
    // ✅ 添加边界检查
    if (!a) {
        console.warn(`无效索引: i=${i}, points长度=${this.points.length}`);
        return Infinity;
    }
    
    let sum = 0;
    for (let k = 0; k < a.length; k++) {
        const diff = a[k] - pivot[k];
        sum += diff * diff;
    }
    return Math.sqrt(sum);
}
    
    // === 搜索方法 ===
    findNearest(query, k = 1) {
        const best = new Array(k).fill({ index: -1, distance: Infinity });
        this._search(this.root, query, best);
        return best.filter(b => b.index !== -1)
                  .sort((a, b) => a.distance - b.distance)
                  .map(b => ({
                      point: this.points[b.index],
                      distance: b.distance
                  }));
    }
    
    _search(node, query, best) {
    if (!node) return;
    
    if (node.type === 'leaf') {
        // 叶节点：暴力搜索范围内的点
        for (let i = node.start; i < node.end; i++) {
            const pointIndex = this.indices[i];
            const dist = this._pointDistanceToPivot(pointIndex, query);
            this._updateBest(pointIndex, dist, best);
        }
        return;
    }
    
    // ✅ 修复：计算到节点球心的距离，不需要具体点
    const distToNodeCenter = this._distanceBetweenPivots(node.pivot, query);
    const minPossibleDist = distToNodeCenter - node.radius;
    const worstDist = best[best.length - 1].distance;
    
    if (minPossibleDist > worstDist) {
        return; // 剪枝
    }
    
    // ✅ 修复：计算到左右子树球心的距离
    const distToLeft = this._distanceBetweenPivots(node.left.pivot, query);
    const distToRight = this._distanceBetweenPivots(node.right.pivot, query);
    
    if (distToLeft < distToRight) {
        this._search(node.left, query, best);
        this._search(node.right, query, best);
    } else {
        this._search(node.right, query, best);
        this._search(node.left, query, best);
    }
}
// ✅ 新增：计算两个球心之间的距离
_distanceBetweenPivots(pivot1, pivot2) {
    let sum = 0;
    for (let k = 0; k < pivot1.length; k++) {
        const diff = pivot1[k] - pivot2[k];
        sum += diff * diff;
    }
    return Math.sqrt(sum);
}
    
    _updateBest(index, dist, best) {
        for (let i = 0; i < best.length; i++) {
            if (dist < best[i].distance) {
                best.splice(i, 0, { index, distance: dist });
                best.pop();
                break;
            }
        }
    }
    
    // === 工具方法 ===
    getAllPoints() {
        return this.indices.map(idx => this.points[idx]);
    }
    
    getTreeStats() {
        let leafCount = 0, nodeCount = 0, maxDepth = 0;
        
        const traverse = (node, depth = 0) => {
            if (!node) return;
            
            maxDepth = Math.max(maxDepth, depth);
            if (node.type === 'leaf') {
                leafCount++;
            } else {
                nodeCount++;
                traverse(node.left, depth + 1);
                traverse(node.right, depth + 1);
            }
        };
        
        traverse(this.root);
        return { leafCount, nodeCount, maxDepth, totalPoints: this.points.length };
    }
    //-------❌注意--------//
    //Uncaught TypeError: can't access property "length", a is undefined：意味着某个索引指向了不存在的点
    
}
function debugOptimizedBallTree() {
    console.log("🐛 调试优化版 Ball Tree");
    
    // 先用小数据测试
    const points = [
        [1,1,1,1,1,1,1,1,1,1],
        [2,2,2,2,2,2,2,2,2,2], 
        [3,3,3,3,3,3,3,3,3,3],
        [4,4,4,4,4,4,4,4,4,4]
    ];
    const query = [1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5];
    
    console.log("测试数据:", points.length, "个点");
    
    try {
        console.time("构建");
        const ballTree = new OptimizedBallTree(points, 2);
        console.timeEnd("构建");
        
        console.log("构建成功!");
        console.log("根节点:", ballTree.root);
        
        console.time("搜索");
        const results = ballTree.findNearest(query, 2);
        console.timeEnd("搜索");
        
        console.log("搜索结果:", results);
        
        const stats = ballTree.getTreeStats();
        console.log("树统计:", stats);
        
    } catch (error) {
        console.error("错误详情:", error);
    }
}

debugOptimizedBallTree();
// === 性能测试 ===//
//🎉 关键突破
    /*索引架构 - 不复制数据，只管理索引
    原地划分 - 内存操作高效
    正确剪枝 - 基于球心距离的几何剪枝
    边界处理 - 完善的错误检查*/
//🎯 优化亮点
    /*唯一数据源 - 不复制点数据
    索引数组 - 原地划分，内存高效
    正确剪枝 - 基于几何距离的剪枝
    统计信息 - 便于调试和监控
    内存友好 - 大幅减少内存使用*/
function testOptimizedBallTree() {
    console.log("🚀 测试优化版 Ball Tree");
    //构建: 4ms (1000个10维点)；搜索: 0ms (即时响应)；数据完整性: 100%正确；树结构: 平衡良好 (128叶节点，17层深度)
    const points = Array(1000).fill(0).map(() => 
        Array(10).fill(0).map(() => Math.random())
    );
    const query = Array(10).fill(0).map(() => Math.random());
    console.time("优化BallTree构建");
    const ballTree = new OptimizedBallTree(points, 15);
    console.timeEnd("优化BallTree构建");
    console.time("优化BallTree搜索");
    const results = ballTree.findNearest(query, 5);
    console.timeEnd("优化BallTree搜索");
    const stats = ballTree.getTreeStats();
    console.log("树统计:", stats);
    console.log("搜索结果:", results.length, "个点");
    // 验证数据完整性
    const allPoints = ballTree.getAllPoints();
    console.log("数据完整性:", allPoints.length === points.length);
}

testOptimizedBallTree();
//================================🔄范围查询=============================//
// 找到距离query在radius范围内的所有点
//🎯找到所有距离查询点在指定半径范围内的点：以query为圆心，radius为半径画圆，找出圆内所有点
//算法优势：高效剪枝：不用检查每个点，直接排除整个区域，这个功能在地理搜索、碰撞检测、推荐系统中非常有用
BallTree.prototype.findInRadius = function(query, radius) {
    //入口函数：输入: 查询点query + 搜索半径radius，输出: 半径范围内的所有点及其距离
    const results = [];
    this._radiusSearch(this.root, query, radius, results);
    return results;
};
BallTree.prototype._radiusSearch = function(node, query, radius, results) {
    // 剪枝：如果整个节点都在范围外，跳过
    const minDistToNode = distance(query, node.pivot) - node.radius;
    if (minDistToNode > radius) {
        return;// 整个节点都可以跳过！
    }
    
    if (node.isLeaf) {
        // 叶节点：检查每个点
        // 叶节点：暴力检查每个点；符合条件：距离 ≤ 半径的点加入结果
        for (const point of node.points) {
            const dist = distance(point, query);
            if (dist <= radius) {
                results.push({ point, distance: dist });
            }
        }
    } else {
        // 内部节点：递归搜索    内部节点：递归搜索两个子树
        this._radiusSearch(node.left, query, radius, results);
        this._radiusSearch(node.right, query, radius, results);
    }
};
function testRadiusSearch() {
    console.log("🎯 测试范围查询");
    // 超简单数据 - 4个明确位置的点
    const points = [
        [1, 1],    // 距离 [2,2] 约1.41
        [2, 2],    // 距离 [2,2] 约0
        [3, 3],    // 距离 [2,2] 约1.41  
        [8, 8]     // 距离 [2,2] 约8.49
    ];
    const ballTree = new OptimizedBallTree(points, 2);
    const query = [2, 2];
    const radius = 2.0; // 搜索半径 
    console.log("数据点:", points);
    console.log(`查询点: [${query}], 半径: ${radius}`);
    const results = ballTree.findInRadius(query, radius);
    console.log("找到", results.length, "个点:");
    results.forEach(result => {
        console.log(`  点 [${result.point}], 距离: ${result.distance.toFixed(2)}`);
    });
    // 预期结果: 前3个点应该在范围内，第4个点应该被排除
}
// 立即运行
testRadiusSearch();
/*运行所有测试
console.log("=== Ball Tree 核心优势演示 ===");
performanceTest();
console.log("\n");
batchQueryTest();
console.log("\n");*/
// 测试范围查询
const points = [[1,1], [2,2], [3,3], [8,8], [9,9]];
const ballTree = new BallTree(points);
const radiusResults = ballTree.findInRadius([2,2], 2.5);
console.log("范围查询结果:", radiusResults);


//==========================🔄性能对比=========================//
//Ball Tree的优势//
//1.高维性能：k-d树在20+维度就基本失效，Ball Tree在100+维度仍有效
//Ball Tree的优势场景：真正的高维（1000+维度）大数据量（10万+点）特定数据分布（非轴对齐的簇）
//2.数据分布无关：不依赖轴对齐，对任意分布的数据都有效
//3.几何剪枝：基于距离的剪枝在高维空间更可靠
//4.稳定性：不会因为数据分布而性能急剧下降
//建议：用C++的FLANN库或scikit-learn - 工业级实现；测试真实数据集 - 而不是随机数据；Rust现代且性能好；

/*关键性能差异
基础实现	优化实现
大量数组创建	原地操作
重复距离计算	缓存结果
深度递归栈	迭代+栈
JavaScript对象开销	紧凑数据结构*/

//真实情况：在JavaScript中，对于大多数实际应用场景，Ball Tree确实没有明显优势：
//Ball Tree在我们的JavaScript实现中确实没有明显优势，构建开销太大数据量不够大，JavaScript执行效率问题：
//JavaScript实现有很多隐藏的开销，而优化版本会避免这些，在C++/Python的库中，这些算法都是用高度优化的C代码实现
//JavaScript不适合做这种计算密集型算法对比 - 隐藏开销太多，实际实现和理论差距很大，算法性能严重依赖具体实现和硬件
    /*构建开销太大 - Ball Tree构建比k-d树复杂得多
    JavaScript性能限制 - 递归、对象创建等开销很大
    数据量要求高 - 需要10万+点才能看到优势
    维度要求高 - 需要500+维才明显*/
//当前实现的架构有缺陷：
//数据存储设计的重要性；索引vs副本的权衡；工业级实现更复杂

//📊工业界的实际选择：
//现实中的选择逻辑：
function chooseAlgorithm(points, queries) {
    const dim = points[0].length;
    const count = points.length;
    const queryCount = queries.length;
    
    if (count < 1000 || dim < 20) {
        return 'k-d树或甚至暴力搜索'; // 小数据简单处理
    }
    if (dim > 100 && queryCount > 10) {
        return 'Ball Tree'; // 真正的高维批量查询
    }
    return 'k-d树'; // 默认选择
}

//---❌注意---//
//Uncaught SyntaxError: illegal character U+FF1B：代码中包含了全角分号 ；（中文分号）而不是半角分号 ;（英文分号）
//Uncaught ReferenceError: distance is not defined：在 KDTree 类中使用了distance函数，但这个函数没有在 KDTree 类的范围内定义
//KDTree 类中添加 distance 方法：这样代码更封装，不会依赖外部函数
//或者使用全局的 distance 函数：确保在代码开头定义了全局的 distance 函数
//Uncaught TypeError: can't access property "distance", ballResults[0] is undefined:主要问题是构建过程中产生了无效的内部节点
//很多节点被标记为 isLeaf: false（内部节点），但它们的 left 和 right 都是 null！这说明在构建Ball Tree时，递归构建失败了，子节点没有被正确创建
//修改 buildTree 方法，确保内部节点真的有子节点
//增强的 splitPoints 方法
//Uncaught ReferenceError: leftChild is not defined：buildTree 方法中声明了 leftChild 和 rightChild，但在使用前又删除了这些变量

//===========对比=========//
// === 工具函数 ===
function distance(a, b) {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
        sum += Math.pow(a[i] - b[i], 2);
    }
    return Math.sqrt(sum);
}

function findPivot(points) {
    if (points.length === 0) return null;
    const dim = points[0].length;
    const pivot = new Array(dim).fill(0);
    for (let i = 0; i < dim; i++) {
        let sum = 0;
        for (const point of points) {
            sum += point[i];
        }
        pivot[i] = sum / points.length;
    }
    return pivot;
}

function calculateRadius(points, pivot) {
    let maxDistance = 0;
    for (const point of points) {
        const dist = distance(point, pivot);
        maxDistance = Math.max(maxDistance, dist);
    }
    return maxDistance;
}

// === BallTree 完整实现 ===
class BallTreeNode {
    constructor(points) {
        this.points = points;
        this.pivot = findPivot(points);
        this.radius = calculateRadius(points, this.pivot);
        this.left = null;
        this.right = null;
        this.isLeaf = points.length <= 1;
    }
}
class BallTree {
    constructor(points, leafSize = 1) {
        this.leafSize = leafSize;
        this.root = this.buildTree(points);
    }
    buildTree(points) {
        if (points.length <= this.leafSize) {
            return new BallTreeNode(points);
        }
        const [pivot1, pivot2] = this.findFarthestPoints(points);
        const [leftPoints, rightPoints] = this.splitPoints(points, pivot1, pivot2);
        // ✅ 关键修复：检查划分结果是否有效
    if (leftPoints.length === 0 || rightPoints.length === 0) {
        console.warn(`划分失败: 左${leftPoints.length}点, 右${rightPoints.length}点，创建叶节点`);
        return new BallTreeNode(points);
    }
    // 🚨 问题在这里！又重复调用了 buildTree！
    // ✅ 递归构建子树
    const leftChild = this.buildTree(leftPoints);
    const rightChild = this.buildTree(rightPoints);
    // 🚨 问题：缺少变量声明！
    // ✅ 修复：声明 leftChild 和 rightChild 变量
   
    // ✅ 检查子树是否构建成功
    if (!leftChild || !rightChild) {
        console.warn("子树构建失败，创建叶节点");
        return new BallTreeNode(points);
    }
        const node = new BallTreeNode(points);
        node.left = this.buildTree(leftPoints);
        node.right = this.buildTree(rightPoints);
        return node;
    }
    findFarthestPoints(points) {
        let maxDistance = -1;
        let pivot1 = points[0], pivot2 = points[0];
        const sampleSize = Math.min(50, points.length);
        
        for (let i = 0; i < sampleSize; i++) {
            for (let j = i + 1; j < sampleSize; j++) {
                const dist = distance(points[i], points[j]);
                if (dist > maxDistance) {
                    maxDistance = dist;
                    pivot1 = points[i];
                    pivot2 = points[j];
                }
            }
        }
        return [pivot1, pivot2];
    }
    
    splitPoints(points, pivot1, pivot2) {//🔧 增强的 splitPoints 方法
    const leftPoints = [];
    const rightPoints = [];
    
    for (const point of points) {
        const distToPivot1 = distance(point, pivot1);
        const distToPivot2 = distance(point, pivot2);
        
        if (distToPivot1 < distToPivot2) {
            leftPoints.push(point);
        } else {
            rightPoints.push(point);
        }
    }
    
    // ✅ 防止所有点都分到一边
    if (leftPoints.length === 0 && rightPoints.length > 0) {
        leftPoints.push(rightPoints.pop());
    }
    if (rightPoints.length === 0 && leftPoints.length > 0) {
        rightPoints.push(leftPoints.pop());
    }
    
    return [leftPoints, rightPoints];
}
    
    findNearest(query, k = 1) {
        let best = [];
        this._search(this.root, query, k, best);
        return best;
    }
    
    _search(node, query, k, best) {
        console.log("搜索节点:", node ? `有${node.points ? node.points.length : 0}个点` : "空节点");
    if (!node) return;  // ✅ 添加空节点检查
    
    if (node.isLeaf) {
        //✅添加叶节点数据检查
        if (!node.points || node.points.length === 0) return;
        
        for (const point of node.points) {
            this._updateBest(point, query, k, best);
        }
        return;
    }
  /*  //✅增强安全检查
    if (!node.left && !node.right) {
        console.warn("内部节点没有子节点:", node);
        return;
    }
        if (node.isLeaf) {
            for (const point of node.points) {
                this._updateBest(point, query, k, best);
            }
            return;
        }
        
        // 安全检查
        if (!node.left || !node.right) {
            if (node.left) this._search(node.left, query, k, best);
            if (node.right) this._search(node.right, query, k, best);
            return;
        }*/
        //✅改进的内部节点处理
         /* const hasLeft = node.left && !node.left.isLeaf;
            const hasRight = node.right && !node.right.isLeaf;*/
        // ✅ 修复：搜索所有有效子节点，不管是不是叶节点
            const hasLeft = node.left !== null;
            const hasRight = node.right !== null;
            if (!hasLeft && !hasRight) {
                // 如果两个子节点都是叶节点或不存在，直接搜索所有后代叶节点
                this._searchAllLeaves(node, query, k, best);
                return;
            }
            
            // 正常的内部节点搜索逻辑
            if (hasLeft && hasRight) {
                const distToLeft = distance(query, node.left.pivot);
                const distToRight = distance(query, node.right.pivot);
                
                let first, second;
                if (distToLeft < distToRight) {
                    first = node.left;
                    second = node.right;
                } else {
                    first = node.right;
                    second = node.left;
                }
                
                this._search(first, query, k, best);
                
                const minDistToSecond = distance(query, second.pivot) - second.radius;
                const worstBestDist = best.length > 0 ? best[best.length - 1].distance : Infinity;
                
                if (minDistToSecond < worstBestDist) {
                    this._search(second, query, k, best);
                }
            } else {
                // 只有一个有效的内部子节点
                if (hasLeft) this._search(node.left, query, k, best);
                if (hasRight) this._search(node.right, query, k, best);
            }
        }

        // ✅ 新增：搜索所有叶节点
        _searchAllLeaves(node, query, k, best){
            if (!node) return;
            
            if (node.isLeaf) {
                for (const point of node.points) {
                    this._updateBest(point, query, k, best);
                }
            } else {
                this._searchAllLeaves(node.left, query, k, best);
                this._searchAllLeaves(node.right, query, k, best);
            }
        }
        _updateBest(point, query, k, best) {
        const dist = distance(point, query);
        const candidate = { point, distance: dist };
        
        let i = 0;
        while (i < best.length && best[i].distance < dist) {
            i++;
        }
        best.splice(i, 0, candidate);
        
        if (best.length > k) {
            best.pop();
        }
    }
        /*if (!hasLeft && !hasRight) {
            // 如果两个子节点都是叶节点或不存在，直接搜索所有后代叶节点
            this._searchAllLeaves(node, query, k, best);
            return;
        }
        const distToLeft = distance(query, node.left.pivot);
        const distToRight = distance(query, node.right.pivot);
        
        let first, second;
        if (distToLeft < distToRight) {
            first = node.left;
            second = node.right;
        } else {
            first = node.right;
            second = node.left;
        }
        
        this._search(first, query, k, best);*/
        /*// ✅ 添加第二个子节点的安全检查
        if (!second) return;*/
        /*const minDistToSecond = distance(query, second.pivot) - second.radius;
        const worstBestDist = best.length > 0 ? best[best.length - 1].distance : Infinity;
        
        if (minDistToSecond < worstBestDist) {
            this._search(second, query, k, best);
        }*/
    }
// 诊断搜索失败的具体原因
function debugSearchFailure() {
    console.log("🔍 诊断Ball Tree搜索失败原因");
    
    // 10维测试数据
    const points = [];
    for (let i = 0; i < 20; i++) {
        points.push(Array(10).fill(0).map(() => Math.random()));
    }
    const query = Array(10).fill(0).map(() => Math.random());
    
    console.log("创建BallTree...");
    const ballTree = new BallTree(points, 5);
    
    // 手动跟踪搜索过程
    let searchPath = [];
    const originalSearch = ballTree._search.bind(ballTree);
    ballTree._search = function(node, query, k, best) {
        searchPath.push({
            points: node.points.length,
            isLeaf: node.isLeaf,
            hasLeft: !!node.left,
            hasRight: !!node.right
        });
        
        if (searchPath.length > 50) {
            console.log("搜索路径过长，可能陷入循环");
            console.log("搜索路径:", searchPath);
            return;
        }
        
        return originalSearch(node, query, k, best);
    };
    
    console.log("开始搜索...");
    const results = ballTree.findNearest(query, 3);
    console.log("搜索路径长度:", searchPath.length);
    console.log("搜索结果:", results);
    
    if (results.length === 0) {
        console.log("❌ 搜索完全失败");
        console.log("最后几个节点:", searchPath.slice(-5));
    }
}
debugSearchFailure();
// 深入诊断 _updateBest 方法
function debugUpdateBest() {
    console.log("🔍 诊断 _updateBest 方法");
    
    const points = [
        [1,1,1,1,1,1,1,1,1,1],  // 10维点
        [2,2,2,2,2,2,2,2,2,2]
    ];
    const query = [1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5];
    
    const ballTree = new BallTree(points, 1);
    
    // 劫持 _updateBest 方法
    let updateCount = 0;
    const originalUpdate = ballTree._updateBest.bind(ballTree);
    ballTree._updateBest = function(point, query, k, best) {
        updateCount++;
        console.log(`_updateBest 调用 ${updateCount}:`, {
            point: point.slice(0, 3), // 只显示前3维
            query: query.slice(0, 3),
            bestLength: best.length
        });
        
        const dist = distance(point, query);
        console.log(`距离计算结果: ${dist}`);
        
        return originalUpdate(point, query, k, best);
    };
    
    console.log("开始搜索...");
    const results = ballTree.findNearest(query, 1);
    console.log("_updateBest 调用次数:", updateCount);
    console.log("最终结果:", results);
}

debugUpdateBest();
// 检查叶节点数据完整性
function debugLeafNodes() {
    console.log("🔍 检查叶节点数据");
    
    const points = Array(10).fill(0).map(() => Array(10).fill(0).map(() => Math.random()));
    const ballTree = new BallTree(points, 3);
    
    let leafNodes = [];
    
    function findLeafNodes(node) {
        if (!node) return;
        if (node.isLeaf) {
            leafNodes.push({
                points: node.points,
                pointsLength: node.points.length,
                pivot: node.pivot,
                radius: node.radius
            });
        } else {
            findLeafNodes(node.left);
            findLeafNodes(node.right);
        }
    }
    
    findLeafNodes(ballTree.root);
    
    console.log("找到叶节点数量:", leafNodes.length);
    leafNodes.forEach((leaf, i) => {
        console.log(`叶节点 ${i}: ${leaf.pointsLength}个点, 半径: ${leaf.radius}`);
        if (leaf.pointsLength > 0) {
            console.log(`  第一个点: ${leaf.points[0].slice(0, 3)}...`);
        }
    });
}
debugLeafNodes();
function realAdvantageTest() {
    console.log("🔥 Ball Tree真正优势场景测试");
    
    // 场景1：真正的高维数据
    console.log("\n🎯 场景1: 1000维数据");
    const highDimPoints = Array(1000).fill(0).map(() => 
        Array(1000).fill(0).map(() => Math.random())
    );
    const highDimQuery = Array(1000).fill(0).map(() => Math.random());
    
    console.time("k-d树 1000维搜索");
    // k-d树在1000维基本会退化到暴力搜索
    let kdCount = 0;
    for (let i = 0; i < Math.min(100, highDimPoints.length); i++) {
        distance(highDimPoints[i], highDimQuery);
        kdCount++;
    }
    console.timeEnd("k-d树 1000维搜索");
    console.log(`k-d树实际计算了 ${kdCount} 个距离`);
    
    console.time("BallTree 1000维搜索");
    const ballTree = new BallTree(highDimPoints, 50);
    const results = ballTree.findNearest(highDimQuery, 1);
    console.timeEnd("BallTree 1000维搜索");
    
    // 场景2：特殊数据分布（非轴对齐的簇）
    console.log("\n🎯 场景2: 非轴对齐簇数据");
    const clusterPoints = [];
    for (let i = 0; i < 500; i++) {
        // 创建对角线分布的簇
        const base = Math.random() * 10;
        clusterPoints.push([base + Math.random()*0.1, base + Math.random()*0.1]);
    }
    const clusterQuery = [5.5, 5.5];
    
    console.time("k-d树 簇数据");
    const kdTreeCluster = new KDTree(clusterPoints);
    kdTreeCluster.findNearest(clusterQuery, 5);
    console.timeEnd("k-d树 簇数据");
    
    console.time("BallTree 簇数据");
    const ballTreeCluster = new BallTree(clusterPoints, 10);
    ballTreeCluster.findNearest(clusterQuery, 5);
    console.timeEnd("BallTree 簇数据");
}
realAdvantageTest();
class KDNode {
    constructor(point, depth = 0) {
        this.point = point;
        this.left = null;
        this.right = null;
        this.depth = depth;
    }
}
class KDTree {
    constructor(points) {
        this.root = this.buildTree(points);
    }
    //✅在KDTree 类中添加distance方法
    distance(a, b) {
        let sum = 0;
        for (let i = 0; i < a.length; i++) {
            sum += Math.pow(a[i] - b[i], 2);
        }
        return Math.sqrt(sum);
    }
    buildTree(points, depth = 0) {
        if (points.length === 0) return null;
        const dim = points[0].length;
        const axis = depth % dim;
        
        // 按当前维度排序
        points.sort((a, b) => a[axis] - b[axis]);
        const median = Math.floor(points.length / 2);
        
        const node = new KDNode(points[median], depth);
        node.left = this.buildTree(points.slice(0, median), depth + 1);
        node.right = this.buildTree(points.slice(median + 1), depth + 1);
        
        return node;
    }
    
    findNearest(query, k = 1) {
        let best = [];
        this._search(this.root, query, k, best);
        return best.sort((a, b) => a.distance - b.distance);
    }
    
    _search(node, query, k, best, depth = 0) {
        if (!node) return;
        
        const dim = query.length;
        const axis = depth % dim;
        //✅现在使用this.distance
        const dist = this.distance(node.point, query);
        
        // 更新最佳列表
        this._updateBest({ point: node.point, distance: dist }, k, best);
        
        // 决定搜索顺序
        const goLeft = query[axis] < node.point[axis];
        
        if (goLeft) {
            this._search(node.left, query, k, best, depth + 1);
            // k-d树的剪枝条件
            const worstDist = best.length > 0 ? best[best.length - 1].distance : Infinity;
            if (best.length < k || Math.abs(query[axis] - node.point[axis]) < worstDist) {
                this._search(node.right, query, k, best, depth + 1);
            }
        } else {
            this._search(node.right, query, k, best, depth + 1);
            const worstDist = best.length > 0 ? best[best.length - 1].distance : Infinity;
            if (best.length < k || Math.abs(query[axis] - node.point[axis]) < worstDist) {
                this._search(node.left, query, k, best, depth + 1);
            }
        }
    }
    
    _updateBest(candidate, k, best) {
        let i = 0;
        while (i < best.length && best[i].distance < candidate.distance) {
            i++;
        }
        best.splice(i, 0, candidate);
        if (best.length > k) best.pop();
    }
}

// 高维性能对比测试
function highDimensionBattle() {
    console.log("🔥 Ball Tree vs k-d树 高维对决");
    // 生成高维数据
    const generateData = (count, dimensions) => {
        const points = [];
        for (let i = 0; i < count; i++) {
            const point = Array(dimensions).fill(0).map(() => Math.random());
            points.push(point);
        }
        return points;
    };
    // 测试不同维度
    const dimensions = [2, 10, 50, 100];
    dimensions.forEach(dim => {
        console.log(`\n📊 ${dim}维空间测试:`);
        const points = generateData(1000, dim);
        const query = generateData(1, dim)[0];
        // k-d树测试
        console.time(`k-d树构建 ${dim}D`);
        const kdTree = new KDTree(points);
        console.timeEnd(`k-d树构建 ${dim}D`);
        console.time(`k-d树搜索 ${dim}D`);
        const kdResults = kdTree.findNearest(query, 5);
        console.timeEnd(`k-d树搜索 ${dim}D`);
        // Ball Tree测试
        console.time(`BallTree构建 ${dim}D`);
        const ballTree = new BallTree(points, 10);
        console.timeEnd(`BallTree构建 ${dim}D`);
        console.time(`BallTree搜索 ${dim}D`);
        const ballResults = ballTree.findNearest(query, 5);
        console.timeEnd(`BallTree搜索 ${dim}D`);
        
        console.log(`结果一致: ${kdResults[0].distance.toFixed(4)} vs ${ballResults[0].distance.toFixed(4)}`);
    });
}
highDimensionBattle();
///以上测试////
//测试数据（均匀随机分布）是对k-d树最友好的情况：在真实数据中：数据有聚类结构，维度间有关联，分布不均匀这些情况下Ball Tree的球体划分会更有效；
//理论和现实的差距：理论：BallTree在高维更好，现实：需要"足够高"的维度和合适的数据分布，实践：在大多数实际应用中，k-d树已经足够好
function kdTreeKiller() {
    console.log("💀 KD树死亡测试 - 构造最差情况");
    
    // 构造完全对角的数据 - KD树的噩梦！
    const points = [];
    for (let i = 0; i < 300; i++) {
        // 所有点都在一条对角线上
        const val = i / 30;
        const point = Array(50).fill(0).map((_, idx) => val + idx * 0.01);
        points.push(point);
    }
    
    const query = Array(50).fill(0).map((_, idx) => 5 + idx * 0.01);
    
    console.log("数据: 300个50维点，完全对角线分布");
    console.log("这是KD树的最差情况！");
    
    // Ball Tree
    console.time("BallTree - 对角数据");
    const ballTree = new OptimizedBallTree(points, 10);
    const ballResults = ballTree.findNearest(query, 5);
    console.timeEnd("BallTree - 对角数据");
    
    // KD Tree  
    console.time("KDTree - 对角数据");
    const kdTree = new KDTree(points);
    const kdResults = kdTree.findNearest(query, 5);
    console.timeEnd("KDTree - 对角数据");
    
    console.log("BallTree找到:", ballResults.length, "个结果");
    console.log("KDTree找到:", kdResults.length, "个结果");
    
    // 验证正确性
    console.log("最近点距离:");
    console.log("  BallTree:", ballResults[0]?.distance.toFixed(4));
    console.log("  KDTree:  ", kdResults[0]?.distance.toFixed(4));
}

// 立即运行死亡测试
kdTreeKiller();


function ultimateBattle() {
    console.log("🔥 BALL TREE vs KD-TREE 终极对决");
    
    // 测试真正能体现差异的场景
    const testCases = [
        { name: "🔺 对角簇数据", points: generateDiagonalClusters(2000, 100) },
        { name: "🎯 超高维稀疏", points: generateSparseData(1500, 500) },
        { name: "🔄 非轴对齐", points: generateRotatedClusters(1800, 80) }
    ];
    
    testCases.forEach(testCase => {
        console.log(`\n${testCase.name}: ${testCase.points.length}个点`);
        const query = testCase.points[0].map(() => Math.random());
        
        // Ball Tree
        console.time("BallTree");
        const ballTree = new OptimizedBallTree(testCase.points, 20);
        const ballResults = ballTree.findNearest(query, 5);
        console.timeEnd("BallTree");
        
        // KD Tree
        console.time("KDTree");
        const kdTree = new KDTree(testCase.points);
        const kdResults = kdTree.findNearest(query, 5);
        console.timeEnd("KDTree");
        
        console.log(`距离差异: ${Math.abs(ballResults[0].distance - kdResults[0].distance).toFixed(6)}`);
    });
}

// 生成对角簇数据（k-d树的噩梦）
function generateDiagonalClusters(count, dimensions) {
    const points = [];
    for (let i = 0; i < count; i++) {
        const clusterCenter = Math.floor(Math.random() * 10);
        const point = Array(dimensions).fill(0).map((_, idx) => 
            clusterCenter + (idx * 0.1) + Math.random() * 0.2
        );
        points.push(point);
    }
    return points;
}

// 生成稀疏高维数据
function generateSparseData(count, dimensions) {
    const points = [];
    for (let i = 0; i < count; i++) {
        const point = Array(dimensions).fill(0).map(() => 
            Math.random() < 0.1 ? Math.random() : 0  // 90%稀疏
        );
        points.push(point);
    }
    return points;
}

// 生成旋转簇（非轴对齐）
function generateRotatedClusters(count, dimensions) {
    const points = [];
    const clusters = 5;
    
    for (let i = 0; i < count; i++) {
        const cluster = Math.floor(Math.random() * clusters);
        const angle = (cluster * Math.PI) / clusters; // 旋转角度
        
        const point = Array(dimensions).fill(0).map((_, idx) => {
            const radius = 2 + Math.random();
            return radius * Math.cos(angle + idx * 0.1) + Math.random() * 0.3;
        });
        points.push(point);
    }
    return points;
}

// 运行终极测试
ultimateBattle();
//KD树在所有情况下都更快，Ball Tree的构建开销确实很大，即使在对角线数据中，KD树仍然表现优秀
```


