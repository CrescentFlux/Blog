

## 基础知识
- **定义**
```
A*搜索算法是一种在图形或网格中用于寻找从起始节点到目标节点的最低成本路径的启发式搜索算法。它通过结合两个成本函数来保证其完备性和最优性（在满足特定条件下）
```
- **定义**
```
并查集是一种树型的数据结构，用于处理一些不交集合的合并及查询问题
```
- **反阿克曼函数**
```
反阿克曼函数 α(n):α(n)是使得A(k, 1)超过n所需的最小k; 对于一个规模 n (宇宙原子总数)的输入，它的输出值也不会超过 5。
阿克曼函数: A(m, n) 是一个有两个变量的递归函数,阿克曼函数 A(m, n) 的增长速度，远远快于指数函数、阶乘函数
```



## 注意事项
1. **混淆点**
- **A*搜索 vs 并查集**

| 对比 | A*搜索算法 | 并查集(Union-Find) |
|------|------------|-------------------|
| 问题类型 | 路径规划、寻路 | 动态连通性、集合管理 |
| 核心操作 | search() + 启发式搜索 | find() + union() |
| 数据结构 | Map + Set + Array | Array |
| 主要优化 | 启发函数h(n) | 路径压缩 + 按秩合并 |
| 输出结果 | 具体路径 | 连通关系(true/false) |
| 关键思想 | 智能的方向选择 | 高效的集合合并与查询 |
| 应用场景 | 机器人路径规划、游戏AI、GPS导航、网络路由 | Kruskal算法、动态连通性问题、网络连接 |





2. **代码实现**
```
//===============================🔄Union-Find==============================//
class UnionFind {
    constructor(n) {
        this.parent = Array(n).fill().map((_, i) => i);//每个元素初始时都是自己的父节点
        // 初始化每个元素的父节点
    }
    
    find(x) {
        while (this.parent[x] !== x) {
            x = this.parent[x];
        }
        return x;
        // 查找根节点,一直向上找，直到找到根节点
    }
    
    union(x, y) {
        const rootX = this.find(x);
        const rootY = this.find(y);
        
        if (rootX === rootY) return;
        
        this.parent[rootX] = rootY;
        // 合并两个集合,把X的根节点指向Y的根节点
    }
    
    connected(x, y) {
        return this.find(x) === this.find(y);
        // 检查连通性
    }
    getState() {
        const groups = {};
        for (let i = 0; i < this.parent.length; i++) {
            const root = this.find(i);
            if (!groups[root]) groups[root] = [];
            groups[root].push(i);
        }
        return {
            parent: [...this.parent],
            groups: groups
        };
    }
}
/*
🎯核心区别：动态 vs 静态
连通分量算法（静态分析）
一次性分析整个图的连通分量
function findConnectedComponents(graph) {
    使用DFS/BFS遍历整个图
    返回所有连通分量
    图结构一旦改变，需要重新计算整个图！
}
并查集（动态维护）
支持动态添加边并实时查询
class UnionFind {
    constructor(n) {
        this.parent = Array(n).fill().map((_, i) => i);
    }
find(x)  实时查找根 
union(x, y)  动态合并集合 
connected(x, y)  实时查询连通性
图结构变化时，只需要局部更新！
*/
class OptimizedUnionFind {//在查找的过程中，顺便把路径压平;不预先优化，等到真正需要时才优化
    constructor(n) {
        this.parent = Array(n).fill().map((_, i) => i);
        this.rank = Array(n).fill(0);
        // 初始化秩数组,初始时每棵树的高度都是0（每个节点单独成树）,秩表示的是树的高度上界，而不是精确高度
        /*秩(rank)的本质：秩是合并时的高度估计值,路径压缩会降低实际高度，但秩保持不变,秩保证了我们合并决策的合理性
        即使有路径压缩，按秩合并仍然能减少路径压缩的工作量;如果没有按秩合并，可能形成很长的链 路径压缩需要处理很长的路径
        如果有按秩合并，链的长度得到控制;
        按秩合并的核心是：通过让矮树挂在高树下，避免不必要的高度增加
        🎯核心洞察：连通性 = 集合关系  ;"动态连通性" = "动态集合管理"
        传统思维：图论节点A和节点B之间有没有路径？  并查集思维：集合论,节点A和节点B是否在同一个集合中
        🎯动态连通性（并查集）支持边建图边查询;并查集的威力在于：它用集合操作隐藏了复杂的图遍历
        没有并查集：每次查询都要DFS/BFS,需要遍历整个连通分量，O(n)时间如果图经常变化，每次都要重新遍历！
        有并查集：查询接近O(1),它把各种连通性查询问题，都转化为了统一的集合归属查询问题
        */
    }
    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
            // 路径压缩,递归调用find进行路径压缩
        }
        return this.parent[x];
    }
    union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);
    if (rootX === rootY) return;
    
    //按秩合并,根据树的高度来决定合并方向
    //🎯核心目标：控制树的高度;树的高度直接影响查找操作的性能;树越高，遍历的步数越多每一步都是时间消耗;矮树挂在高树下（控制高度）
    // 这里比较的rank是路径压缩前的高度上界
    if (this.rank[rootX] < this.rank[rootY]) {//高度不同：合并后高度 = 较高的树的高度;高度相同：合并后高度 = 原高度 + 1
        this.parent[rootX] = rootY;//把X的整个集合合并到Y的集合,rootX 成为 rootY 的子节点
    } else if (this.rank[rootX] > this.rank[rootY]) {//如果rootX的树更高，就让rootY挂在rootX下
        this.parent[rootY] = rootX;// 把Y的整个集合合并到X的集合,rootY 成为 rootX 的子节点
    } else {
        this.parent[rootY] = rootX;
        this.rank[rootX] += 1;
        //两棵树高度相同时，合并后高度+1
    }
    }
    // 添加缺失的 connected 方法
    connected(x, y) {
        return this.find(x) === this.find(y);
    }
    getState() {
        const groups = {};
        for (let i = 0; i < this.parent.length; i++) {
            const root = this.find(i);
            if (!groups[root]) groups[root] = [];
            groups[root].push(i);
        }
        return {
            parent: [...this.parent],
            rank: [...this.rank],
            groups: groups
        };
    }
}
class DebugUnionFind extends OptimizedUnionFind {
    find(x, depth = 0) {
        const indent = "  ".repeat(depth);
        console.log(`${indent}find(${x})开始: parent[${x}] = ${this.parent[x]}`);
        
        if (this.parent[x] !== x) {
            console.log(`${indent}递归调用 find(${this.parent[x]})`);
            this.parent[x] = this.find(this.parent[x], depth + 1);
            console.log(`${indent}回溯: parent[${x}] = ${this.parent[x]}`);
        }
        
        console.log(`${indent}find(${x})返回: ${this.parent[x]}`);
        return this.parent[x];
    }
}

// 测试
console.log("=== 深度调试 ===");
const debugUF = new DebugUnionFind(5);
debugUF.union(0, 1);
debugUF.union(1, 2);
debugUF.union(2, 3);
debugUF.union(3, 4);

console.log("最终parent:", debugUF.parent);

console.log("\n=== 正确测试路径压缩效果 ===");
const uf1 = new OptimizedUnionFind(5);
// 创建长链：0→1→2→3→4
uf1.union(0, 1);
uf1.union(1, 2); 
uf1.union(2, 3);
uf1.union(3, 4);
console.log("创建长链后的parent:", uf1.parent);//🎯路径压缩在创建链的过程中就完成了，而不是等到我们单独调用 find 时才发生
//如果想看到压缩过程，需要避免在union中压缩
// 测试链末端的节点（会触发递归）
console.log("执行 find(0):", uf1.find(0));  // 这会触发深度递归！
console.log("路径压缩后的parent:", uf1.parent);

// 测试修复
console.log("=== 测试基础版UnionFind ===");//基础版没有路径压缩和按秩合并可能形成长链,合并方向随意,效率较低：查找操作需要遍历整个链
const uf = new UnionFind(5);
console.log("初始:", uf.getState());
uf.union(0, 1);
console.log("union(0,1)后:", uf.getState());
uf.union(1, 2);
console.log("union(1,2)后:", uf.getState());
console.log("connected(0,2):", uf.connected(0, 2));
console.log("connected(0,3):", uf.connected(0, 3));

console.log("\n=== 测试优化版UnionFind ===");//可以随时查询任意两个节点是否连通返回 true/false,可以随时建立新的连接动态合并集合,高效性能
const optimizedUF = new OptimizedUnionFind(5);
console.log("初始:", optimizedUF.getState());
optimizedUF.union(0, 1);
console.log("union(0,1)后:", optimizedUF.getState());
optimizedUF.union(1, 2);
console.log("union(1,2)后:", optimizedUF.getState());

//热身测试
function warmUpTest() {
    console.log("🔥 热身测试：10万节点");
    const size = 100000;
    const uf = new OptimizedUnionFind(size);
    
    for (let i = 0; i < 10000; i++) {
        uf.union(
            Math.floor(Math.random() * size),
            Math.floor(Math.random() * size)
        );
    }
    
    console.log("✅ 热身完成，准备上强度！\n");
}

function testMillionNodes() {
    console.log("🔥 准备挑战100万节点...");
    
    const size = 1000000; // 100万！
    console.log(`创建 ${size.toLocaleString()} 个节点的并查集...`);
    
    const startTime = Date.now();
    const uf = new OptimizedUnionFind(size);
    const initTime = Date.now() - startTime;
    console.log(`✅ 初始化完成，耗时: ${initTime}ms`);
    
    // 阶段1：创建链式结构
    console.log("\n🔗 阶段1: 创建链式结构...");
    const chainStart = Date.now();
    for (let i = 0; i < size - 1; i++) {
        uf.union(i, i + 1);
        if (i % 100000 === 0 && i > 0) {
            console.log(`   已完成 ${i.toLocaleString()} 次union...`);
        }
    }
    const chainTime = Date.now() - chainStart;
    console.log(`✅ 链式结构完成，耗时: ${chainTime}ms`);
    
    // 阶段2：随机连接测试
    console.log("\n🎲 阶段2: 随机连接测试...");
    const randomStart = Date.now();
    const randomOps = 10000;
    for (let i = 0; i < randomOps; i++) {
        const a = Math.floor(Math.random() * size);
        const b = Math.floor(Math.random() * size);
        uf.union(a, b);
    }
    const randomTime = Date.now() - randomStart;
    console.log(`✅ 随机连接完成，耗时: ${randomTime}ms`);
    
    // 阶段3：性能查询测试
    console.log("\n⚡ 阶段3: 查询性能测试...");
    const queryStart = Date.now();
    const queryCount = 1000;
    let connectedCount = 0;
    
    for (let i = 0; i < queryCount; i++) {
        const a = Math.floor(Math.random() * size);
        const b = Math.floor(Math.random() * size);
        if (uf.connected(a, b)) {
            connectedCount++;
        }
    }
    const queryTime = Date.now() - queryStart;
    
    // 结果统计
    console.log("\n📊 === 100万节点测试结果 ===");
    console.log(`总节点数: ${size.toLocaleString()}`);
    console.log(`总union操作: ${(size - 1 + randomOps).toLocaleString()}`);
    console.log(`总查询操作: ${queryCount}`);
    console.log(`连通率: ${((connectedCount / queryCount) * 100).toFixed(1)}%`);
    console.log(`总耗时: ${(Date.now() - startTime)}ms`);
    console.log(`平均查询时间: ${(queryTime / queryCount).toFixed(3)}ms`);
    // 内存使用估算
    const memoryUsage = (size * 8 * 2) / (1024 * 1024); // 2个数组，每个8字节
    console.log(`预估内存: ${memoryUsage.toFixed(2)}MB`);
    // 验证最终状态
    const state = uf.getState();
    const groupCount = Object.keys(state.groups).length;
    console.log(`最终连通分量: ${groupCount} 个`);
    console.log("🎉 100万节点挑战完成！");
}
// 执行测试
warmUpTest();
testMillionNodes();

//===============================🔄A* Search==============================//

class AStar {
    constructor() {
        // 需要维护的数据结构
        this.openSet = [];       // 待探索节点（优先队列）//决定下一步探索哪里
        this.closedSet = new Set(); // 已探索节点//"已探索地图" - 避免重复探索
        this.gScore = new Map();    //记录从起点到每个节点的实际最短距离,判断是否找到了更短的路径//"里程记录表" - 记录实际走了多远
        this.fScore = new Map();    //评估节点的综合潜力 (实际 + 预估),决定探索的优先级//"智能导航" - 综合评估哪里最有希望
        this.cameFrom = new Map();  // 记录路径,记录每个节点是从哪个节点过来的,最后能重构出完整路径//"路径记忆" - 记住怎么走到每个地方的
        //this.heuristicType = heuristicType;  // 🆕存储启发函数类型
    }

    // 启发函数 - 估计从当前点到终点的代价//A*的核心：启发函数 h(n) 可以自定义
 
    heuristic(node, goal) {
       // if (this.heuristicType === 'euclidean') {
    //🆕欧几里得距离
    return Math.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2);
        // 🎯 直接硬编码为欧几里得距离
        //return Math.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2);
        /*}else{
        // 曼哈顿距离 = 网格城市中的行走距离|x1-x2| + |y1-y2|//网格中直角行走的总步数
        // 曼哈顿距离是可采纳的启发函数,它不会高估实际距离,在实际网格中，你至少要走这么多步;给算法一个乐观但不离谱的估计
        return Math.abs(node.x - goal.x) + (node.y - goal.y);
        }
        */
   // 
   }

    //在openSet中找到f值最小的节点，这是A*算法的核心贪心选择
    getLowestFScore() {
        //找到f值最小的节点
        let lowestNode = this.openSet[0];//先假设第一个节点最小
        // 检查第i个节点：openSet[i]/ 获取它的f值：this.fScore.get(openSet[i])与当前最小节点的f值比较：this.fScore.get(lowestNode)
        for (let i = 1; i < this.openSet.length; i++) {
            if (this.fScore.get(this.openSet[i]) < this.fScore.get(lowestNode)) {
                lowestNode = this.openSet[i];// 找到更小的，更新
            }
        }
        return lowestNode;
/*
A*的贪心选择核心:不是选离起点最近的（g值最小）不是选离终点最近的（h值最小）而是选综合估计最好的（f值最小）
            f(n) = g(n) + h(n) f值会随着探索更新
            ↓  
        "已走距离" + "预估剩余距离" = "总预估代价"
//选项1：只选g值最小的（Dijkstra）
f(n) = g(n)  
"我已经走了多远？选走得最少的继续;问题：会盲目探索所有方向，效率低
// 选项2：只选h值最小的（贪心最佳优先）
f(n) = h(n)
"离终点多近？选离终点最近的"问题：可能陷入死胡同，不保证最优
// 选项3：A*的智慧选择
f(n) = g(n) + h(n)
"综合考虑已走距离 + 预估剩余距离"平衡了效率和最优性！
*/
    }
/*  
A* = Dijkstra的保证最优 + 贪心的搜索效率
三大关键变量:
每个节点有三个值：
g(n) = 从起点到n的实际代价
h(n) = 从n到终点的估计代价（启发函数）
f(n) = g(n) + h(n) = 总估计代价
// 决策原则：总是扩展f(n)最小的节点！
*/
    //重构最终路径//从终点反向追溯，重构完整路径
    reconstructPath(current) {
        const path = [current];
        while (this.cameFrom.has(current)) {
            current = this.cameFrom.get(current);  //向前追溯路径//// 找当前节点的"父节点"
            path.unshift(current);// 添加到路径开头
        }
        return path;
    }

    // 获取节点的邻居,负责探索当前节点的周围环境//输入：当前节点 + 地图信息//输出：所有可以走的相邻节点
    getNeighbors(node, grid) {
        const neighbors = [];
        //1. 定义移动方向,这表示只能上下左右4方向移动（曼哈顿距离对应的移动方式）
        const directions = [//在计算机中，坐标系的y轴是向下的：在这个坐标系中，y值增加表示向下移动
            {dx: 0, dy: -1},  // 上
            {dx: 1, dy: 0},   // 右
            {dx: 0, dy: 1},   // 下
            {dx: -1, dy: 0}   // 左
        ];
        //2. 计算邻居坐标,对每个方向，计算相邻格子的坐标
        for (const dir of directions) {
            const newX = node.x + dir.dx;
            const newY = node.y + dir.dy;
            //3. 有效性检查
            // 检查邻居是否有效（在网格内且不是障碍）
            if (newX >= 0 && newX < grid.width && 
                newY >= 0 && newY < grid.height && 
                !grid.isObstacle(newX, newY)) {
                neighbors.push({x: newX, y: newY});
            }
        }
        return neighbors;
    }

    // 主搜索函数
/*A*的智慧在于：
前瞻性：用f(n)=g(n)+h(n)评估节点潜力
系统性：不放过任何可能的好路径
高效性：优先探索最有希望的方向
总是扩展f值最小的节点（最有希望的）;gScore保证记录的是实际最短距离;启发函数h(n)乐观估计，不会错过好路径;closedSet避免重复计算
f值 = 全局视野的智慧
*/
    search(start, goal, grid) {
        console.log(`🔍 开始寻路: (${start.x},${start.y}) -> (${goal.x},${goal.y})`);
        console.log(`障碍物:`, grid.obstacles);
         // 🎯 重置所有状态
        this.openSet = [];
        this.closedSet = new Set();
        this.gScore = new Map();
        this.fScore = new Map();
        this.cameFrom = new Map();
        //阶段1：初始化
        this.openSet.push(start);// 起点加入待探索
        this.gScore.set(start, 0); // 起点到自己的代价=0
        this.fScore.set(start, this.heuristic(start, goal));//起点总估计代价
        //阶段2：主循环 - 每次处理一个节点
        // 🎯 声明count变量
         let count = 0;
        while (this.openSet.length > 0) {
            // 获取当前要处理的节点
            const current = this.getLowestFScore();//选f值最小的节点
        if (count === 1) { // 只显示第一次选择
            console.log(`首次选择: (${current.x},${current.y}), f=${this.fScore.get(current).toFixed(2)}`);
        }
        
        if (current.x === goal.x && current.y === goal.y) {
            console.log(`总探索次数: ${count}`);
            return this.reconstructPath(current);
        }
        //阶段3：目标检查    
            // 找到目标！
            if (current.x === goal.x && current.y === goal.y) {
                return this.reconstructPath(current);// 找到路径！
            }
        //阶段4：标记当前节点已探索
            //从openSet移除，加入closedSet
            this.openSet = this.openSet.filter(n => !(n.x === current.x && n.y === current.y));
            this.closedSet.add(`${current.x},${current.y}`);// 加入已探索集合
        //阶段5：探索邻居
        /*
        这些邻居就是你当前能做的所有选择,每个选择都会影响后续的整个路线
        探索邻居的必要性：
            路径是连续的：不能跳过中间步骤直接到终点
            决策需要选项：没有邻居就没有选择，没有选择就无法决策
            搜索需要扩展：算法通过不断扩展邻居来"蔓延"到整个地图
            最优路径存在：但必须通过一步步探索才能发现它
        */
            // 检查所有邻居
            const neighbors = this.getNeighbors(current, grid);// 获取可走的邻居
            for (const neighbor of neighbors) {
                const neighborKey = `${neighbor.x},${neighbor.y}`;
                
                // 跳过已探索的邻居
                if (this.closedSet.has(neighborKey)) continue; // 跳过已探索的
        //阶段6：计算新路径代价
                // 计算经过current到neighbor的代价
                const tentativeGScore = this.gScore.get(current) + 1;//网格中相邻节点距离为1
        //阶段7：判断是否找到更好路径        
                // 如果找到更好路径
                if (!this.gScore.has(neighbor) || tentativeGScore < this.gScore.get(neighbor)) {
                    this.cameFrom.set(neighbor, current); // 记录路径
                    this.gScore.set(neighbor, tentativeGScore);// 更新实际代价
                    this.fScore.set(neighbor, tentativeGScore + this.heuristic(neighbor, goal));
                   
                    // 如果邻居不在openSet中，加入
                    if (!this.openSet.some(n => n.x === neighbor.x && n.y === neighbor.y)) {
                        this.openSet.push(neighbor);// 新发现的节点加入待探索
                    }
                }
            }
        }

        return null; // 没有找到路径
    }
}

//A*算法的地图管理器;它负责管理整个寻路环境
class Grid {
    constructor(width, height, obstacles) {
        this.width = width;// 地图宽度
        this.height = height;// 地图高度
        this.obstacles = obstacles;// 障碍物位置数组
    }
/* 相当于一个"智能地图"：
- 知道地图有多大（width, height）
- 知道哪里不能走（obstacles）  
- 能回答"这个位置能走吗？"（isObstacle）
定义寻路空间的边界,标记不可通行的区域, 提供统一的位置查询接口,让算法专注于核心的寻路逻辑
*/
    isObstacle(x, y) {// 检查坐标(x,y)是否在障碍物列表中
        return this.obstacles.some(obs => obs.x === x && obs.y === y);
    }
    //可视化方法
    visualize(path = []) {
        let gridStr = '';
        
        for (let y = 0; y < this.height; y++) {
            let row = '';
            for (let x = 0; x < this.width; x++) {
                const pos = {x, y};
                
                // 🎯 优先显示起点和终点
                if (start && x === start.x && y === start.y) {
                    row += '🟢 ';
                } else if (goal && x === goal.x && y === goal.y) {
                    row += '🎯 ';
                } else if (path.some(p => p.x === x && p.y === y)) {
                    row += '🟦 ';
                } else if (this.isObstacle(x, y)) {
                    row += '🚧 ';
                } else {
                    row += '⬜ ';
                }
            }
            gridStr += row + '\n';
        }
        return gridStr;
    }
}
// 明确创建两个不同的地图
const grid1 = new Grid(5, 5, [
    {x: 1, y: 1}, {x: 2, y: 2}, {x: 3, y: 1}  // 简单地图：分散障碍
]);

const grid2 = new Grid(5, 5, [
    {x: 1, y: 0}, {x: 1, y: 1}, {x: 1, y: 2},  // 挑战地图：垂直墙
    {x: 3, y: 2}, {x: 3, y: 3}, {x: 3, y: 4}   // 另一堵墙
]);

// 明确的起点终点
const start = {x: 0, y: 0};
const goal = {x: 4, y: 4};

console.log("=== 第一步：验证地图数据 ===");
console.log("grid1障碍物:", grid1.obstacles);
console.log("grid2障碍物:", grid2.obstacles);
console.log("是同一个实例吗?", grid1 === grid2);

// 测试障碍物检测
console.log("\n=== 第二步：测试障碍物检测 ===");
console.log("grid1 (1,1)是障碍?", grid1.isObstacle(1,1)); // 应该true
console.log("grid1 (1,0)是障碍?", grid1.isObstacle(1,0)); // 应该false
console.log("grid2 (1,0)是障碍?", grid2.isObstacle(1,0)); // 应该true
console.log("grid2 (2,0)是障碍?", grid2.isObstacle(2,0)); // 应该false

console.log("\n=== 第三步：测试寻路 ===");

console.log("--- 测试grid1（简单地图）---");
const aStar1 = new AStar();
const path1 = aStar1.search(start, goal, grid1);
console.log("grid1路径长度:", path1?.length);
console.log("grid1路径可视化:");
console.log(grid1.visualize(path1, start, goal));

console.log("\n--- 测试grid2（挑战地图）---");
const aStar2 = new AStar();
const path2 = aStar2.search(start, goal, grid2);
console.log("grid2路径长度:", path2?.length);
console.log("grid2路径可视化:");
console.log(grid2.visualize(path2, start, goal));

console.log("\n=== 第四步：比较结果 ===");
if (path1 && path2) {
    const samePath = JSON.stringify(path1) === JSON.stringify(path2);
    console.log("两个路径相同吗?", samePath);
    
    if (samePath) {
        console.log("❌ 问题：两个不同地图找到了相同路径！");
        console.log("共同路径:", path1);
    } else {
        console.log("✅ 正常：两个地图找到了不同路径");
    }
}

// 首先定义测试用的网格
const testGrid = new Grid(5, 5, [
    {x: 1, y: 1}, {x: 2, y: 2}, {x: 3, y: 1}
]);

console.log("=== 开始健壮性测试 ===");

// 测试1: 边界情况
console.log("--- 测试1: 边界情况 ---");

// 1.1 起点即终点
console.log("1.1 起点即终点:");
const aStar01 = new AStar();
const path01 = aStar1.search({x:0,y:0}, {x:0,y:0}, testGrid);
console.log("路径长度:", path01?.length, "期望: 1");
console.log("路径:", path01);

// 1.2 相邻节点
console.log("\n1.2 相邻节点:");
const path02 = aStar01.search({x:0,y:0}, {x:0,y:1}, testGrid);
console.log("路径长度:", path02?.length, "期望: 2");
console.log("路径:", path02);

// 测试2: 无解情况
console.log("\n--- 测试2: 无解情况 ---");

// 2.1 被障碍物包围
const trappedGrid = new Grid(3, 3, [
    {x:0,y:1}, {x:1,y:0}, {x:1,y:2}, {x:2,y:1}  // 十字包围
]);
const path3 = aStar1.search({x:1,y:1}, {x:0,y:0}, trappedGrid);
console.log("被包围时能找到路径吗?", path3 ? "是" : "否", "期望: 否");

// 2.2 完全障碍物网格
const fullObstacleGrid = new Grid(3, 3, [
    {x:0,y:0}, {x:0,y:1}, {x:0,y:2},
    {x:1,y:0}, {x:1,y:1}, {x:1,y:2},
    {x:2,y:0}, {x:2,y:1}, {x:2,y:2}
]);
const path4 = aStar1.search({x:0,y:0}, {x:2,y:2}, fullObstacleGrid);
console.log("全障碍网格能找到路径吗?", path4 ? "是" : "否", "期望: 否");

// 测试3: 正常情况验证
console.log("\n--- 测试3: 正常情况验证 ---");

// 3.1 简单路径
const path5 = aStar1.search({x:0,y:0}, {x:4,y:4}, testGrid);
console.log("正常寻路路径长度:", path5?.length);
console.log("路径是否连续:", checkPathContinuity(path5));

// 测试4: 性能测试
console.log("\n--- 测试4: 性能测试 ---");

// 4.1 空网格性能
const emptyGrid = new Grid(10, 10, []);
console.time("空网格寻路");
const path6 = aStar1.search({x:0,y:0}, {x:9,y:9}, emptyGrid);
console.timeEnd("空网格寻路");
console.log("空网格路径长度:", path6?.length);

// 辅助函数：检查路径连续性
function checkPathContinuity(path) {
    if (!path || path.length < 2) return true;
    
    for (let i = 1; i < path.length; i++) {
        const dx = Math.abs(path[i].x - path[i-1].x);
        const dy = Math.abs(path[i].y - path[i-1].y);
        if (dx + dy !== 1) {
            console.log(`❌ 路径不连续: [${path[i-1].x},${path[i-1].y}] -> [${path[i].x},${path[i].y}]`);
            return false;
        }
    }
    return true;
}

// 测试5: 多次运行稳定性
console.log("\n--- 测试5: 稳定性测试 ---");
let successCount = 0;
for (let i = 0; i < 10; i++) {
    const tempAStar = new AStar();
    const tempPath = tempAStar.search({x:0,y:0}, {x:4,y:4}, testGrid);
    if (tempPath && tempPath.length > 0) {
        successCount++;
    }
}
console.log(`稳定性: ${successCount}/10 次成功`);

console.log("\n🎉 健壮性测试完成！");
```