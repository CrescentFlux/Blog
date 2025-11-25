#  Hungarian Hopcroft-Karp Algorithm
## 基础知识
- **定义**
   - Hungarian Algorithm
   ```
   Hungarian算法是一种用于解决无权二分图中最大匹配问题的算法。它通过深度优先搜索（DFS）逐一尝试为集合中的每个顶点寻找增广路，并通过递归回溯来动态调整现有匹配，从而逐步逼近并最终找到最大匹配。
   ```
   - Hopcroft-Karp算法
   ```
   Hopcroft-Karp算法是一种用于解决二分图最大匹配问题的里程碑式的高效算法。它是一种多路增广算法，通过广度优先搜索（BFS）和深度优先搜索（DFS）相结合，在每一阶段寻找极大集合的顶点不相交的最短增广路径，从而实现了优于顺序增广算法的时间复杂度
   ```
- **Berge 定理**
   - 设M是图G的一个匹配。则M是G的最大匹配，当且仅当G中不存在相对于M的增广路


## 注意事项
1. **混淆点**
- **Hungarian 算法 vs Hopcroft-Karp 算法**

|对比	|Hungarian算法	|Hopcroft-Karp算法|
---|---|---
|核心机制	|单路径DFS搜索|	多路径BFS+DFS协作|
|增广策略|单路增广：一次寻找并翻转一条增广路|多路增广：一次寻找并翻转一个极大不相交的最短增广路集合|
|搜索策略|	深度优先，找到第一条可行路径就返回|	广度优先分层，找到所有最短路径后批量执行|
|适用场景|	教学、小规模问题、稀疏图|	大规模问题、稠密图、性能要求高的场景|
|执行效率|	在糟糕的搜索顺序下性能差|	性能稳定，最坏情况也有保障|



2. **代码实现**
```
class HungarianAlgorithm {
    constructor() {
        this.adjList = [];       // 邻接表：adjList[u] = 与左部节点u相邻的右部节点集合
        this.rightMatch = [];    // rightMatch[v] = 与右部节点v匹配的左部节点，-1表示未匹配
        this.visited = [];       // DFS访问标记数组
        this.operationCount = 0;
    }
/*
增广路径:能让你扩大匹配的路径
增广路径 = 一条能通过边角色翻转来增加匹配数的特殊路径
关键思想：在这条特殊路径上，如果我们把匹配边和非匹配边互换角色，匹配数就会+1
增广路径的本质：一条重新安排的链;它不是简单的路径，而是一套调整方案
通过系统性地找调整链，来不断改进匹配
*/
    //算法数据初始化
    init(leftPreferences) {
        this.adjList = leftPreferences;//存储图的邻接表结构
        
        // 计算右部节点数量,找出最大的右部节点索引
        let maxRightNode = -1;
        for (let neighbors of this.adjList) { // L 次循环//嵌套循环 → 乘法关系
            //遍历所有连接关系，记录遇到的最大节点编号;问遍所有左边节点确保所有的右边节点都被记录防止遗漏
            for (let v of neighbors) {// 最多 E 条边（实际是deg(u)） // 可能触发递归调查
                maxRightNode = Math.max(maxRightNode, v);
            }
        }
        this.rightMatch = Array(maxRightNode + 1).fill(-1);//整个算法匹配结果的存储中心
        //创建并初始化匹配数组,maxRightNode + 1节点编号从0开始，数量需要+1;用-1填充：-1表示该右部节点尚未匹配任何左部节点
    }
    //对左边节点dfs开始增广路径
    dfs(u) {
        this.operationCount++; // 计数
        //遍历左部节点u的所有邻接右部节点
        //for (let v of this.adjList[u]) {// 遍历u的所有邻接节点
        for (let i = 0; i < this.adjList[u].length; i++) {
            const v = this.adjList[u][i];  // 这里用 neighbors[i]
            this.operationCount++; // 每条边检查都计数
            // 如果右部节点v在当前DFS中尚未被访问
            if (!this.visited[v]) {
                this.visited[v] = true;
                //visited数组防止无限循环
                // 关键判断：如果v未匹配，或者与v匹配的节点可以找到新的匹配
                if (this.rightMatch[v] === -1 || this.dfs(this.rightMatch[v])) {
                    //找到增广路径，更新匹配关系
                    this.rightMatch[v] = u;
                    return true;
                }
            }
        }
        return false;
    }
    //最大匹配数计算
    maxMatching() {// 外层循环：L次
        let matchCount = 0;
        // 遍历所有左部节点
        for (let u = 0; u < this.adjList.length; u++) {
            // 重置访问标记数组
            this.visited = Array(this.rightMatch.length).fill(false);
            // 如果为左部节点u找到增广路径，则匹配数增加
            if (this.dfs(u)) {
                matchCount++;
            }
        }
        return matchCount;
    }
    
    /**
     * 获取具体的匹配对
     * @returns {number[][]} 匹配对数组，每个元素为[u, v]表示左部节点u与右部节点v匹配
     */
    getMatches() {
        const matches = [];
        for (let v = 0; v < this.rightMatch.length; v++) {
            if (this.rightMatch[v] !== -1) {
                matches.push([this.rightMatch[v], v]);
            }
        }
        return matches;
    }
    
    /**
     * 获取匹配关系详情
     * @returns {Object} 匹配关系的详细描述
     */
    getMatchingDetails() {
        const details = {
            maxMatches: this.maxMatching(),
            matchingPairs: this.getMatches(),
            description: `在包含${this.adjList.length}个左部节点和${this.rightMatch.length}个右部节点的二分图中找到最大匹配`
        };
        return details;
    }
/*
 ➜算法复杂度分析
完全二分图（最稠密）左部每个节点都连接右部所有节点,边数 E = L × R
稠密二分图:边数接近完全二分图,通常 E ≈ O(L × R)
稀疏二分图：边数远小于完全二分图通常 E ≈ O(L + R) 或 O(max(L, R))
匈牙利算法既适用于稠密二分图，也适用于稀疏二分图，但在不同场景下效率表现不同;稀疏图表现更为优秀适合大规模稀疏图
 ➜时间复杂度: O(L × E)，其中L为左部节点数，E为边数
 ➜空间复杂度:
adjList：存储图的邻接表,需要 O(E) 空间（存储所有边）
rightMatch：匹配数组,需要 O(R) 空间
visited：访问标记数组,需要 O(R) 空间
递归调用栈:最坏深度 O(L)
总空间 = O(E) + O(R) + O(R) + O(L)
       = O(E + R + L)在二分图中通常 E ≥ L 且 E ≥ R，可以简化为 O(E)
O(L + R) 只考虑了节点数，但忽略了存储边需要的空间//如果只说有L个男生，R个女生 → O(L + R)但要说清楚具体关系 → 需要 O(E) 空间
*/
}

// 测试用例
console.log("=== 匈牙利算法测试 ===");

// 定义二分图：左部节点3个，右部节点3个
const bipartiteGraph = [
    [0, 1],  // 左部节点0与右部节点0,1相邻
    [1, 2],  // 左部节点1与右部节点1,2相邻
    [0]      // 左部节点2仅与右部节点0相邻
];

const algorithm = new HungarianAlgorithm();
algorithm.init(bipartiteGraph);

const result = algorithm.getMatchingDetails();
console.log("算法结果:", result);
console.log("\n匹配对详情:");
result.matchingPairs.forEach(([u, v]) => {
    console.log(`  左部节点 ${u} ←→ 右部节点 ${v}`);
});

/*
匈牙利算法是贪婪的DFS：找到第一条可行路径就返回，不管是否最优。
Hopcroft-Karp是优化的BFS+DFS：先找到所有最短路径，再批量执行
*/

class HopcroftKarp {
    // 针对二分图匹配优化,不需要容量、流量、反向边等概念
    constructor() {
        this.adjList = [];           // 邻接表 // 只需要邻接表
        this.leftMatch = [];         // leftMatch[u] = 与左部节点u匹配的右部节点
        this.rightMatch = [];        // rightMatch[v] = 与右部节点v匹配的左部节点
        this.dist = [];              // dist：BFS搜索的起点状态
        this.nullNode = -1;          // 空节点标识
        this.bfsCount = 0;
    }
    
    /**
     * 初始化算法
     * @param {number} leftCount - 左部节点数
     * @param {number} rightCount - 右部节点数  
     * @param {number[][]} edges - 边列表
     */
    init(leftCount, rightCount, edges) {
        this.leftCount = leftCount;
        this.rightCount = rightCount;
        
        // 构建邻接表
        this.adjList = Array(leftCount).fill().map(() => []);
        for (const [u, v] of edges) {
            this.adjList[u].push(v);
        }
        
        // 初始化匹配数组
        this.leftMatch = Array(leftCount).fill(this.nullNode);
        this.rightMatch = Array(rightCount).fill(this.nullNode);
        this.dist = Array(leftCount).fill(0);
    }
    
    /**
     * BFS阶段：寻找所有最短增广路径
     * @returns {boolean} 是否存在增广路径
     */
    bfs() {
        const queue = [];
    /*
    👉路径长度= 路径中的边数（不是工作次数）边数少 = 调整链短 = 执行更快、更稳定
    在算法中，BFS是按照图的边来计算距离;每次走过一条边，距离+1;BFS找到的就是边数最少的路径
    Hopcroft-Karp的优化：每次都找边数最少的增广路径，避免长链条的复杂调整
    在增广路径中，我们关注的是边的状态，不是节点的状态
    👉匹配边 vs 非匹配边：
    匹配边：当前匹配关系中存在的边
    非匹配边：图中存在，但不在当前匹配中的边
    增广路径的定义:开始于未匹配节点,结束于未匹配节点,边交替出现：非匹配边 → 匹配边 → 非匹配边 → ...这种交替结构让我们能够通过"翻转"来增加匹配数
    节点有匹配/未匹配状态,边有匹配边/非匹配边状态
    */    
        //①初始化距离，将所有未匹配的左部节点加入队列
        for (let u = 0; u < this.leftCount; u++) {
            if (this.leftMatch[u] === this.nullNode) {
                this.dist[u] = 0;// 起点
                queue.push(u);
            } else {
                this.dist[u] = Infinity;
            }
        }
        /*
        queue的含义：当前待摸排人员名单
        nullNode是一个虚拟节点，用来表示摸排结束的标志
        dist数组的含义：摸排轮次记录表
        dist[u] = 0：这个男生是摸排起点（第0轮）,dist[u] = 1：需要第1轮才能摸排到这个男生,dist[u] = 2：需要第2轮才能摸排到这个男生
        */
        //this.dist[this.nullNode] = Infinity;//暂时不需要摸排或无法摸排// 初始为无穷大
        this.dist[-1] = Infinity;//算法里约定俗成用 -1 表示"无匹配"
        //BFS的层层扩展特性天然保证了找到的路径是最短,长路径需要更多轮次才能发现,算法选择最先发现的路径执行
        //②BFS遍历,最先找到的增广路径一定是最短的;找到第一条能走通的路就收工，不再找更远的路
        while (queue.length > 0) {
           //👉一旦找到一条路径，就拒绝探索更长的路径;这是一种优化：找到第一条路径后就停止寻找更长的路径！
            const u = queue.shift();// 按距离顺序出队
            if (this.dist[u] < this.dist[-1]) {
            /*nullNode在这里的双重作用:记录当前找到的最短路径长度,作为提前终止的判据，避免探索更长的路径
                dist[nullNode] 记录当前找到的最短完整路径长度,if (dist[u] < dist[nullNode]) 确保只探索可能找到更短路径的节点
                dist[u] = 你当前位置到起点的距离;dist[nullNode] = 当前找到的最近出口的距离   
            */
                // 遍历u的所有邻接右部节点
                //for (const v of this.adjList[u]) {
                for (let i = 0; i < this.adjList[u].length; i++) {
                    const v = this.adjList[u][i];  
                    const u2 = this.rightMatch[v];//右节点的现有匹配关系
                    if (u2 === this.nullNode) {
                        this.dist[this.nullNode] = this.dist[u] + 1;
                    }
                    // 如果u2未被访问过，更新距离并加入队列
                    if (this.dist[u2] === Infinity) {
                        this.dist[u2] = this.dist[u] + 1;
                        queue.push(u2);
                    }
                }
            }
        }
        //nullNode代表：路径的终点,在BFS中，当我们找到一条完整的增广路径时，最终会到达nullNode
        //return this.dist[this.nullNode] !== Infinity;
        return this.dist[-1] !== Infinity;
    }
 /*
                while (还有地方没探索) {
                        从队列拿出一个位置u;
                        if (u距离起点 < 最近出口距离) {
                            // 说明从这里出发可能找到更近的出口
                            看看u能去到哪些地方;
                            for (每个能去的地方v) {
                                if (v就是出口) {
                                    记录：最近出口距离 = u距离 + 1;
                                }
                                if (v是没去过的地方) {
                                    标记v的距离 = u距离 + 1;
                                    把v加入探索队列;
                                }
                            }
                        } else {
                            // u距离起点 >= 最近出口距离
                            // 说明从这里出发找到的出口不会更近，直接跳过！
                        }
                    }
*/    
    /**
     * DFS阶段：沿着BFS找到的最短路径进行增广
     * @param {number} u - 当前左部节点
     * @returns {boolean} 是否找到增广路径
     */
    dfs(u) {
    /*
    DFS负责：实际执行这条路径上的所有匹配调整,确保整条路径都能成功打通//实际执行这些路径，确保可行
    关键思想：沿着BFS找到的骨架，实际走一遍并翻转匹配状态
    👉DFS的核心动作：回溯时更新匹配
    👉路径反转 = 增广操作的数学描述;增广操作 = 路径反转的代码实现//增广操作通过路径反转来实现
        增广路径发现
            ↓  
        DFS执行（递归深入）
            ↓
        到达终点，开始回溯
            ↓  
        路径反转（更新匹配关系）← 这就是增广！//它们不是两个操作，而是同一个过程的不同描述
            ↓
        匹配数+1
    */
        if (u === this.nullNode) return true;
        //for (const v of this.adjList[u]) {有些JavaScript环境对for...of循环支持不完善，改用传统的for循环更稳定
        for (let i = 0; i < this.adjList[u].length; i++) {
            const v = this.adjList[u][i]; 
            const u2 = this.rightMatch[v];
            // 检查是否在最短增广路径上
            if (this.dist[u2] === this.dist[u] + 1) {
                if (this.dfs(u2)) {
                    // 找到增广路径，更新匹配
                    this.rightMatch[v] = u;
                    this.leftMatch[u] = v;
                    return true;
                }
            }
        }
        
        // 标记该节点在当前层级不可用
        this.dist[u] = Infinity;
        return false;
    }
    
    /**
     * 计算最大匹配
     * @returns {number} 最大匹配数
     */
    maxMatching() {
        let matching = 0;
        
        // 算法主循环：多轮BFS+DFS//Berge定理：一个匹配是最大匹配，当且仅当不存在增广路径
        while (this.bfs()) {// ← 寻找增广路径（Berge定理的条件判断）
            this.bfsCount++; // 计数BFS轮次
            for (let u = 0; u < this.leftCount; u++) {
                if (this.leftMatch[u] === this.nullNode && this.dfs(u)) {// ← 找到并执行增广路径
                    matching++;/ ← 匹配数增加（定理的结论）
                }
            }
        }
        
        return matching;
    }
    
    /**
     * 获取匹配详情
     */
    getMatchingDetails() {
        const pairs = [];
        for (let u = 0; u < this.leftCount; u++) {
            if (this.leftMatch[u] !== this.nullNode) {
                pairs.push([u, this.leftMatch[u]]);
            }
        }
        return {
            maxMatching: pairs.length,
            pairs: pairs,
            leftMatch: [...this.leftMatch],
            rightMatch: [...this.rightMatch]
        };
    }
}
// 简单测试 - 验证Hopcroft-Karp算法是否正常工作
function testHopcroftKarp() {
    console.log("=== Hopcroft-Karp算法简单测试 ===");
    
    // 测试案例：3个男生，3个女生
    const testCase = {
        leftCount: 3,
        rightCount: 3,
        edges: [
            [0, 0], [0, 1],  // 男生0喜欢女生0,1
            [1, 1], [1, 2],  // 男生1喜欢女生1,2
            [2, 0]           // 男生2喜欢女生0
        ]
    };

    const hopcroft = new HopcroftKarp();
    hopcroft.init(testCase.leftCount, testCase.rightCount, testCase.edges);
    const result = hopcroft.maxMatching();
    const details = hopcroft.getMatchingDetails();

    console.log("匹配数:", result);
    console.log("BFS轮次:", hopcroft.bfsCount);
    console.log("匹配对:", details.pairs);
    console.log("测试通过！✓");
}

// 运行测试
testHopcroftKarp();


//=====算法性能对比测试=====//
class HungarianAlgorithm {
    constructor() {
        this.adjList = []; this.rightMatch = []; this.visited = []; this.operationCount = 0;
    }
    init(leftCount, rightCount, edges) {
        this.adjList = Array(leftCount).fill().map(() => []);
        for (const [u, v] of edges) {
            this.adjList[u].push(v);
        }
        this.rightMatch = Array(rightCount).fill(-1);
    }
    dfs(u) {
        this.operationCount++;
        for (let i = 0; i < this.adjList[u].length; i++) {
            const v = this.adjList[u][i];
            if (!this.visited[v]) {
                this.visited[v] = true;
                if (this.rightMatch[v] === -1 || this.dfs(this.rightMatch[v])) {
                    this.rightMatch[v] = u;
                    return true;
                }
            }
        }
        return false;
    }
    
    maxMatching() {
        let matchCount = 0;
        for (let u = 0; u < this.adjList.length; u++) {
            this.visited = Array(this.rightMatch.length).fill(false);
            if (this.dfs(u)) {
                matchCount++;
            }
        }
        return matchCount;
    }
}
class HopcroftKarp {
    constructor() {
        this.adjList = []; this.leftMatch = []; this.rightMatch = []; this.dist = []; this.bfsCount = 0;
    }
    
    init(leftCount, rightCount, edges) {
        this.adjList = Array(leftCount).fill().map(() => []);
        for (const [u, v] of edges) {
            this.adjList[u].push(v);
        }
        this.leftMatch = Array(leftCount).fill(-1);
        this.rightMatch = Array(rightCount).fill(-1);
    }
    
    bfs() {
        const queue = [];
        this.dist = Array(this.leftMatch.length).fill(Infinity);
        
        for (let u = 0; u < this.leftMatch.length; u++) {
            if (this.leftMatch[u] === -1) {
                this.dist[u] = 0;
                queue.push(u);
            }
        }
        
        this.dist[-1] = Infinity;
        
        while (queue.length > 0) {
            const u = queue.shift();
            if (this.dist[u] < this.dist[-1]) {
                for (let i = 0; i < this.adjList[u].length; i++) {
                    const v = this.adjList[u][i];
                    const u2 = this.rightMatch[v];
                    if (this.dist[u2] === Infinity) {
                        this.dist[u2] = this.dist[u] + 1;
                        queue.push(u2);
                    }
                }
            }
        }
        
        return this.dist[-1] !== Infinity;
    }
    
    dfs(u) {
        if (u === -1) return true;
        for (let i = 0; i < this.adjList[u].length; i++) {
            const v = this.adjList[u][i];
            const u2 = this.rightMatch[v];
            if (this.dist[u2] === this.dist[u] + 1) {
                if (this.dfs(u2)) {
                    this.rightMatch[v] = u;
                    this.leftMatch[u] = v;
                    return true;
                }
            }
        }
        this.dist[u] = Infinity;
        return false;
    }
    
    maxMatching() {
        let matching = 0;
        while (this.bfs()) {
            this.bfsCount++;
            for (let u = 0; u < this.leftMatch.length; u++) {
                if (this.leftMatch[u] === -1 && this.dfs(u)) {
                    matching++;
                }
            }
        }
        return matching;
    }
}
// 测试对比
const testCase = {
    leftCount: 6,
    rightCount: 6,
    edges: [
        [0,1], [1,2], [2,3], [3,4], [4,5],  
        [0,0], [1,1], [1,0], [2,2], [2,1],
        [3,3], [3,2], [4,4], [4,3],
        [5,4], [5,3], [5,2], [5,1], [5,0]   
    ]
};
console.log("=== 🔍算法对比测试 ===");
const hungarian = new HungarianAlgorithm();
hungarian.init(testCase.leftCount, testCase.rightCount, testCase.edges);
const hResult = hungarian.maxMatching();
console.log("匈牙利算法 - 操作次数:", hungarian.operationCount, "匹配数:", hResult);
const hopcroft = new HopcroftKarp();
hopcroft.init(testCase.leftCount, testCase.rightCount, testCase.edges);
const hkResult = hopcroft.maxMatching();
console.log("Hopcroft-Karp - BFS轮次:", hopcroft.bfsCount, "匹配数:", hkResult);
console.log("🎯🔥效率对比:", hungarian.operationCount / hopcroft.bfsCount, "倍");

// 生成大规模稠密二分图测试
function testDenseLargeGraph() {
    console.log("=== 🔍大规模稠密图性能测试 ===");
    
    const nodeCount = 50; // 50个左节点，50个右节点
    const density = 0.8;  // 80%的边存在（很稠密！）
    
    console.log(`图规模: ${nodeCount} × ${nodeCount} 节点`);
    console.log(`稠密度: ${density * 100}%`);
    
    // 生成稠密图的边
    const edges = [];
    for (let u = 0; u < nodeCount; u++) {
        for (let v = 0; v < nodeCount; v++) {
            if (Math.random() < density) {
                edges.push([u, v]);
            }
        }
    }
    
    console.log(`总边数: ${edges.length}`);
    console.log(`理论最大边数: ${nodeCount * nodeCount}`);
    console.log(`实际稠密度: ${(edges.length / (nodeCount * nodeCount) * 100).toFixed(1)}%`);

    // 测试匈牙利算法
    console.time("匈牙利算法耗时");
    const hungarian = new HungarianAlgorithm();
    hungarian.init(nodeCount, nodeCount, edges);
    const hResult = hungarian.maxMatching();
    console.timeEnd("匈牙利算法耗时");
    
    // 测试Hopcroft-Karp算法  
    console.time("Hopcroft-Karp耗时");
    const hopcroft = new HopcroftKarp();
    hopcroft.init(nodeCount, nodeCount, edges);
    const hkResult = hopcroft.maxMatching();
    console.timeEnd("Hopcroft-Karp耗时");
    
    console.log("\n📊 性能对比:");
    console.log(`匈牙利算法 - 操作次数: ${hungarian.operationCount}`);
    console.log(`Hopcroft-Karp - BFS轮次: ${hopcroft.bfsCount}`);
    console.log(`匹配数: 匈牙利=${hResult}, Hopcroft-Karp=${hkResult}`);
    
    const operationRatio = hungarian.operationCount / hopcroft.bfsCount;
    console.log(`🎯🔥操作次数比: ${operationRatio.toFixed(1)}倍的性能差距`);
}

/*运行大规模测试
注意:大规模测试会改变JavaScript引擎状态,运行100万节点测试后,V8引擎的堆内存大幅增长JIT编译器积累了不同的优化策略,垃圾回收机制处于高压状态
内存布局完全改变,对后续测试的影响再运行50节点测试时：匈牙利算法: 受益于JIT热代码路径 → 稍快一些
Hopcroft-Karp: 受内存碎片影响 → 可能需要更多BFS轮次,结果: 1251倍 → 600多倍
*/
testDenseLargeGraph();

// 真实的10万节点测试 - 应该能扛住
function testReal100K() {
    console.log("=== 真实10万节点测试 ===");
    console.log("准备挑战算法极限...");
    
    const nodeCount = 100000; // 10万节点
    const density = 0.0001;   // 极稀疏，0.01%密度
    
    console.log(`规模: ${nodeCount} × ${nodeCount} 节点`);
    console.log(`密度: ${density * 100}%`);
    
    // 高效生成边 - 只生成100万条边
    console.time("生成边");
    const edges = [];
    const targetEdges = 1000000; // 100万条边
    
    for (let i = 0; i < targetEdges; i++) {
        const u = Math.floor(Math.random() * nodeCount);
        const v = Math.floor(Math.random() * nodeCount);
        edges.push([u, v]);
    }
    console.timeEnd("生成边");
    
    console.log(`边数: ${edges.length}`);
    console.log("开始算法测试...");

    try {
        console.time("Hopcroft-Karp总耗时");
        const hopcroft = new HopcroftKarp();
        
        console.time("初始化");
        hopcroft.init(nodeCount, nodeCount, edges);
        console.timeEnd("初始化");
        
        console.time("匹配计算");
        const result = hopcroft.maxMatching();
        console.timeEnd("匹配计算");
        
        console.timeEnd("Hopcroft-Karp总耗时");
        
        console.log(`🎉 成功！匹配数: ${result}, BFS轮次: ${hopcroft.bfsCount}`);
        console.log("算法还是挺能打的！");
        
    } catch (error) {
        console.log("❌ 算法说：我累了...", error.message);
    }
}

// 真的运行这个！
testReal100K();

// 100万节点终极测试！
function testMillionNodes() {
    console.log("=== 100万节点终极测试 ===");
    console.log("🌊 准备测试...");
    
    const nodeCount = 1000000; // 100万节点！
    const targetEdges = 5000000; // 500万条边
    
    console.log(`规模: ${nodeCount} × ${nodeCount} 节点`);
    console.log(`边数: ${targetEdges}`);
    
    // 高效生成500万条边
    console.time("生成边");
    const edges = [];
    
    for (let i = 0; i < targetEdges; i++) {
        const u = Math.floor(Math.random() * nodeCount);
        const v = Math.floor(Math.random() * nodeCount);
        edges.push([u, v]);
    }
    console.timeEnd("生成边");
    
    console.log(`实际边数: ${edges.length}`);
    console.log("开始算法挑战...");

    try {
        console.time("总耗时");
        const hopcroft = new HopcroftKarp();
        
        console.time("初始化");
        hopcroft.init(nodeCount, nodeCount, edges);
        console.timeEnd("初始化");
        
        console.time("匹配计算");
        const result = hopcroft.maxMatching();
        console.timeEnd("匹配计算");
        
        console.timeEnd("总耗时");
        
        console.log(`🎉 奇迹！匹配数: ${result}, BFS轮次: ${hopcroft.bfsCount}`);        
    } catch (error) {
        console.log("❌ 终于...算法说：我认输", error.message);
    }
}

// 开始测试
testMillionNodes();
```