# Graph
## 基础知识
- **定义（针对无向图）**

  - 图：由顶点（或称为节点）的集合和连接顶点的边的集合组成
  - 无向图：：边没有方向，即如果顶点A和B之间有一条边，可以从A走到B，也可以从B走到A
  - 非连通图：一个非连通图可以被划分为两个或更多个连通分量
    - 连通分量：一个图中的一个最大连通子图，最大意味着无法再加入另一个顶点而不破坏其连通性
- **定义（针对有向图）**
  - 强连通图：在有向图中，如果对于任意两个顶点u和v，都存在一条从 u 到 v 的路径，同时也存在一条从 v 到 u 的路径，那么这个有向图是强连通的
    - 要求非常严格：任意两点必须“双向可达”
  - 弱连通图：如果一个有向图忽略所有边的方向后，形成的无向图是连通的，那么原图被称为弱连通的
    - 要求宽松：只要求“有连接”，不要求“双向可达”




- **欧拉定理**
  - 欧拉回路的判定定理：一个连通的无向图 GG 存在欧拉回路，当且仅当该图中每个顶点的度（与该顶点相连的边的数目）都是偶数。
  - 欧拉路径（欧拉迹）的判定定理：一个连通的无向图 GG 存在欧拉路径（但不是回路），当且仅当该图中恰好有两个顶点的度是奇数，其余所有顶点的度都是偶数。
  - 连通图：在图论中，一个连通图是指在一个无向图中，任意两个顶点之间都存在一条路径。





## 注意事项
1. **混淆点**
- **顶点重复访问 vs 边重复访问**


|算法类型	|限制条件	|数据结构|	应用场景|
---|---|---|---
|DFS/BFS遍历|	顶点不重复访问|	visited_vertices = set()	|探索图的结构|
|欧拉路径	|边不重复访问|	从邻接表中删除边	|一笔画问题|
|哈密顿路径	|顶点不重复访问|	visited_vertices = set()	|旅行商问题变种|




2. **代码实现**
```
class Graph {
    //===========基础临接表的实现===========//
    constructor() {
        //1: 初始化一个邻接表来存储图
        this.adjacencyList = {};
        /*邻接表就是：为每个顶点维护一个列表，记录它直接连接的所有点。省空间：只存实际存在的边,高效遍历：找某个顶点的所有邻居很快；符合现实。
        基础的邻接表确实只记录了连接关系，但丢失了边的其他信息。我们可以轻松地扩展它来记录所有需要的信息。
        */

    }

    addVertex(vertex) {
        //2: 如果顶点不存在于邻接表中，则初始化它的邻居列表
         if (!this.adjacencyList[vertex]) {
            this.adjacencyList[vertex] = [];
        }
    }

    addEdge(vertex1, vertex2) {
         //3: 使用push方法互相添加邻居
        this.adjacencyList[vertex1].push(vertex2);
        this.adjacencyList[vertex2].push(vertex1);
    }

    getDegree(vertex) {
         //4: 数组的length就是度数
        return this.adjacencyList[vertex].length;
    }
3
    hasEulerianPath() {
        let oddDegreeCount = 0;
        
        //5: 遍历所有顶点，统计奇度顶点的数量
        for (let vertex in this.adjacencyList) {
            if (this.getDegree(vertex) % 2 !== 0) {
                oddDegreeCount++;
            }
        }
        
        //6: 欧拉路径存在的条件当奇度顶点数为0或2
        return oddDegreeCount === 0 || oddDegreeCount === 2;
    }

    // 进阶挑战：找到一条欧拉路径的起点
    findEulerPathStart() {
        let oddVertices = [];
        
        for (let vertex in this.adjacencyList) {
            if (this.getDegree(vertex) % 2 !== 0) {
                oddVertices.push(vertex);
            }
        }
        
        //7: 如果有两个奇度顶点，返回其中一个；否则返回任意顶点
        if (oddVertices.length === 2) {
            return oddVertices[0];
        } else {
            return Object.keys(this.adjacencyList)[0]; // 返回第一个顶点
        }
    }
}

// 测试代码
/*👉基础邻接表实现无法正确处理平行边，问题根源：平行边的重复计数
A的邻居列表：['B', 'C', 'C'] → 长度=3；C的邻居列表：['A', 'A', 'B', 'D', 'D'] → 长度=5
*/
const graph01 = new Graph();

//添加顶点 A, B, C, D
['A', 'B', 'C', 'D'].forEach(vertex => {
    graph.addVertex(vertex);
});

//添加边创建我们的"南极北极"模型
// A(度3) -- B(度3) 和 C(度4) -- D(度2)
graph.addEdge('A', 'B');
graph.addEdge('A', 'C');
graph.addEdge('A', 'C'); // 平行边让A的度变为3
graph.addEdge('B', 'C');
graph.addEdge('B', 'D');
graph.addEdge('C', 'D');
graph.addEdge('C', 'D'); // 平行边让C的度变为4

console.log("顶点度数:");
//打印每个顶点的度数
for (let vertex in graph.adjacencyList) {
    console.log(`顶点 ${vertex}: 度 = ${graph.getDegree(vertex)}`);
}

console.log(`是否存在欧拉路径: ${graph.hasEulerianPath()}`);
console.log(`欧拉路径起点: ${graph.findEulerPathStart()}`);


 
 //========边类：存储边的完整信息-"边对象邻接表"=========//
class Edge {
    constructor(id, from, to, weight = 1, attributes = {}) {
        this.id = id;// 核心1: 唯一标识 ✅精确操作：可以单独删除、更新某条边跟踪变化✅记录边的创建、修改历史数据关系✅在数据库中作为主键
        this.from = from;// 核心2: 起点引用✅from/to: 顶点引用，用对象引用可以直接访问用户数据
        this.to = to;// 核心3: 终点引用
        this.weight = weight;// 核心4: 权重数值✅不只是"距离"，而是"关系强度"的量化
        this.attributes = {// 扩展: 业务属性容器✅可扩展的业务数据✅复杂的边信息：社交网络分析，物流路径规划✅attributes 的设计体现了 "开闭原则"：对扩展开放，对修改关闭。
            type: 'default',
            created: new Date(),
            ...attributes
        };
        
    }
}

// 邻接项类：管理到一个邻居的所有边
class AdjacencyItem {
    constructor(neighbor) {
        this.neighbor = neighbor;
        this.edges = [];
    }
    
    addEdge(edge) {
        this.edges.push(edge);
    }
    
    getEdgeCount() {
        return this.edges.length;
    }
}

// 主图类
class ProfessionalGraph {
    constructor() {
        this.adjacencyList = {};
        this.edges = new Map();//边仓库
        this.vertices = new Map();//专业顶点仓库
        /*Map优势
        优势1：键可以是任何类型，Map的键可以是任意类型优势2：保持插入顺序优势3：性能优化，大量数据时，Map的增删改查性能更好优势4：安全的键名
        */
    }
    
    addVertex(vertex, data = {}) {
        if (!this.adjacencyList[vertex]) {
            this.adjacencyList[vertex] = [];
        }
        this.vertices.set(vertex, data);//set() 的三大特性特性1：键值对存储，特性2：自动更新（幂等性），特性3：链式调用
    }
    
    addEdge(edgeId, from, to, weight = 1, attributes = {}) {
        const edge = new Edge(edgeId, from, to, weight, attributes);
        this.edges.set(edgeId, edge);
        //保证起点和终点都存在！//防御性编程" 和 "数据一致性保证" 的专业思想
        this.addVertex(from);// 如果from不存在，就创建它
        this.addVertex(to);// 如果to不存在，就创建它
        // 现在可以安全地添加边了// ... 添加边的逻辑
        let fromItem = this.adjacencyList[from].find(item => item.neighbor === to);
        if (!fromItem) {
            fromItem = new AdjacencyItem(to);
            this.adjacencyList[from].push(fromItem);
        }
        fromItem.addEdge(edge);
        //"智能连接管理" 的设计思想：问题：平行边的管理，如果没有这个设计，处理平行边会很混乱
        //✨为每对顶点之间的连接建立一个专门的管理单元（AdjacencyItem），在这个单元内精细管理所有的边"
        let toItem = this.adjacencyList[to].find(item => item.neighbor === from);
        if (!toItem) {
            toItem = new AdjacencyItem(from);
            this.adjacencyList[to].push(toItem);
        }
        toItem.addEdge(edge);
        
        return edge;
    }
    //精确统计一个顶点连接的所有边的数量
    getDegree(vertex) {
        let totalEdges = 0; // 从0开始计数
        for (let item of this.adjacencyList[vertex]) {// 遍历这个顶点的所有"邻居关系档案"
            totalEdges += item.getEdgeCount();// 每个档案里可能有多个边（平行边）
        }
        return totalEdges;// 返回总边数
    }
    
    hasEulerianPath() {
        let oddDegreeCount = 0;
        for (let vertex in this.adjacencyList) {
            if (this.getDegree(vertex) % 2 !== 0) {
                oddDegreeCount++;
            }
        }
        return oddDegreeCount === 0 || oddDegreeCount === 2;
    }
    
    // 打印所有顶点信息
    printAllVerticesInfo() {
        console.log("=== 所有顶点详细信息 ===");
        for (let vertex in this.adjacencyList) {
            const degree = this.getDegree(vertex);
            const parity = degree % 2 === 0 ? '偶数' : '奇数';
            
            console.log(`\n顶点 "${vertex}": 度=${degree} (${parity})`);
            
            for (let item of this.adjacencyList[vertex]) {
                console.log(`  → 到 "${item.neighbor}": ${item.getEdgeCount()} 条边`);
                item.edges.forEach(edge => {
                    console.log(`    边 ${edge.id}: ${edge.from} ↔ ${edge.to}`);
                });
            }
        }
    }
    
    printGraph() {
        this.printAllVerticesInfo();
        
        console.log(`\n=== 图统计信息 ===`);
        console.log(`总边数: ${this.edges.size}`);
        console.log(`总顶点数: ${Object.keys(this.adjacencyList).length}`);
        console.log(`是否存在欧拉路径: ${this.hasEulerianPath()}`);
        
        // 分析度数分布
        const degrees = {};
        for (let vertex in this.adjacencyList) {
            degrees[vertex] = this.getDegree(vertex);
        }
        console.log(`度数分布:`, degrees);
    }
}

// ========== 执行部分 - 创建2-3-3-4度数分布 ==========
console.log("开始创建2-3-3-4度数分布的图...");

// 创建图实例
const graph02 = new ProfessionalGraph();

// 添加四个顶点：A, B, C, D
graph.addVertex('A', {type: '北岸'});
graph.addVertex('B', {type: '左岛'});  
graph.addVertex('C', {type: '右岛'});
graph.addVertex('D', {type: '南岸'});

console.log("顶点添加完成");

// 创建 2-3-3-4 的度数分布：
// A度=2, B度=3, C度=3, D度=4

// 添加边来实现目标度数：
graph.addEdge('e1', 'A', 'B', 1, {type: '桥'});  // A:1, B:1
console.log("添加边 e1: A-B");

graph.addEdge('e2', 'A', 'C', 1, {type: '桥'});  // A:2, B:1, C:1
console.log("添加边 e2: A-C");

graph.addEdge('e3', 'B', 'C', 1, {type: '桥'});  // A:2, B:2, C:2
console.log("添加边 e3: B-C");

graph.addEdge('e4', 'B', 'D', 1, {type: '桥'});  // A:2, B:3, C:2, D:1
console.log("添加边 e4: B-D");

graph.addEdge('e5', 'C', 'D', 1, {type: '桥'});  // A:2, B:3, C:3, D:2
console.log("添加边 e5: C-D");

// 现在度数是2-3-3-2，需要让D变成4
// 添加D的自环（自环在度数计算中算作2度）👉自环就是一条边连接同一个顶点，自环对度数的贡献是2自环改变了度数分布，从而影响欧拉路径的存在性
graph.addEdge('e6', 'D', 'D', 1, {type: '自环'});  // A:2, B:3, C:3, D:4
console.log("添加自环边 e6: D-D");

// 打印完整的图信息
console.log("\n生成图结构...");
graph.printGraph();

// 验证度数
console.log("\n=== 度数验证 ===");
console.log(`A的度数: ${graph.getDegree('A')} (目标: 2)`);
console.log(`B的度数: ${graph.getDegree('B')} (目标: 3)`);  
console.log(`C的度数: ${graph.getDegree('C')} (目标: 3)`);
console.log(`D的度数: ${graph.getDegree('D')} (目标: 4)`);

// 分析欧拉路径条件
console.log("\n=== 欧拉路径分析 ===");
let oddDegreeCount = 0;
let oddVertices = [];
for (let vertex in graph.adjacencyList) {
    const degree = graph.getDegree(vertex);
    if (degree % 2 !== 0) {
        oddDegreeCount++;
        oddVertices.push(vertex);
    }
}
console.log(`奇度顶点数: ${oddDegreeCount}`);
console.log(`奇度顶点: ${oddVertices.join(', ')}`);
console.log(`存在欧拉路径: ${oddDegreeCount === 0 || oddDegreeCount === 2}`);

if (oddDegreeCount === 2) {
    console.log(`✓ 欧拉路径必须从 ${oddVertices[0]} 开始，在 ${oddVertices[1]} 结束`);
} else {
    console.log(`✗ 无法形成欧拉路径，奇度顶点数不是2`);
}

console.log("\n=== 最终结果 ===");
const degrees = {
    'A': graph.getDegree('A'),
    'B': graph.getDegree('B'),
    'C': graph.getDegree('C'),
    'D': graph.getDegree('D')
};
console.log(`实现的度数分布: ${degrees.A}-${degrees.B}-${degrees.C}-${degrees.D}`);
console.log(`目标度数分布: 2-3-3-4`);
console.log(`匹配结果: ${degrees.A === 2 && degrees.B === 3 && degrees.C === 3 && degrees.D === 4 ? '✓ 成功' : '✗ 失败'}`);
//==================🔄欧拉回路和连通图===================//
//📜欧拉回路：一条经过图中每条边恰好一次，并最终回到起点的回路；欧拉路径：一条经过图中每条边恰好一次，但不一定回到起点的路径
类型	    必要条件	                    起点与终点
欧拉回路	图连通，且所有顶点的度为偶数	    起点 = 终点
欧拉路径	图连通，且恰好两个顶点的度为奇数	 起点和终点是那两个奇度顶点
//📜欧拉路径问题，我们需要的是：每条边只访问一次，但顶点可以多次访问
// 边类：存储边的完整信息
class Edge {
    constructor(id, from, to, weight = 1, attributes = {}) {
        this.id = id;
        this.from = from;
        this.to = to;
        this.weight = weight;
        this.attributes = {
            type: 'default',
            created: new Date(),
            ...attributes
        };
    }
}

// 邻接项类：管理到一个邻居的所有边
class AdjacencyItem {
    constructor(neighbor) {
        this.neighbor = neighbor;
        this.edges = [];
    }
    
    addEdge(edge) {
        this.edges.push(edge);
    }
    
    getEdgeCount() {
        return this.edges.length;
    }
}

// 主图类
class ProfessionalGraph {
    constructor() {
        this.adjacencyList = {};
        this.edges = new Map();
        this.vertices = new Map();
    }
    
    addVertex(vertex, data = {}) {
        if (!this.adjacencyList[vertex]) {
            this.adjacencyList[vertex] = [];
        }
        this.vertices.set(vertex, {
            id: vertex,
            data: data,
            createdAt: new Date()
        });
    }
    
    addEdge(edgeId, from, to, weight = 1, attributes = {}) {
        // 确保顶点存在
        this.addVertex(from);
        this.addVertex(to);
        
        const edge = new Edge(edgeId, from, to, weight, attributes);
        this.edges.set(edgeId, edge);
        
        // 添加到from的邻接表
        let fromItem = this.adjacencyList[from].find(item => item.neighbor === to);
        if (!fromItem) {
            fromItem = new AdjacencyItem(to);
            this.adjacencyList[from].push(fromItem);
        }
        fromItem.addEdge(edge);
        
        // 添加到to的邻接表（无向图）
        let toItem = this.adjacencyList[to].find(item => item.neighbor === from);
        if (!toItem) {
            toItem = new AdjacencyItem(from);
            this.adjacencyList[to].push(toItem);
        }
        toItem.addEdge(edge);
        
        return edge;
    }
    
    getDegree(vertex) {
        let totalEdges = 0;
        for (let item of this.adjacencyList[vertex]) {
            if (item.neighbor === vertex) {
                // 自环：每条边贡献2度
                totalEdges += item.getEdgeCount() * 2;
            } else {
                // 普通边：每条边贡献1度
                totalEdges += item.getEdgeCount();
            }
        }
        return totalEdges;
    }
    
    // 检查图是否连通
    isConnected() {//深度优先搜索(DFS) 来检查图是否连通
        const vertices = Object.keys(this.adjacencyList);// 第一行：获取图中所有顶点的列表
        if (vertices.length === 0) return true;// 第二行：如果图是空的，默认算连通（边界情况）
        const visited = new Set();// 第三行：创建"已访问标记"集合，记录走过哪些地方
        this._dfs(vertices[0], visited);//第四行：从第一个顶点开始"探路"（深度优先搜索）
        return visited.size === vertices.length; // 第五行：如果访问过的顶点数 = 总顶点数，说明整个图是连通的
    }
    //连通图的定义： 图中任意两个顶点之间都存在路径。💡从任意一个顶点出发，如果能通过DFS访问到所有顶点，说明所有顶点都是连通的
    _dfs(vertex, visited) {
        visited.add(vertex);// 标记当前顶点为已访问
        console.log(`访问: ${vertex}`);
        for (let item of this.adjacencyList[vertex]) {// 遍历当前顶点的所有邻居
            if (!visited.has(item.neighbor)) {//如果邻居还没访问过，就去访问它
                console.log(`从 ${vertex} 探索到 ${item.neighbor}`);
                this._dfs(item.neighbor, visited);
            }
        }
    }
    // 获取所有连通分量，深入理解图的内部结构
    getConnectedComponents() {
        const visited = new Set();// 第一行：记录哪些顶点已经"被发现"了
        const components = [];// 第二行：存储找到的所有连通分量（岛屿群）
        // 第三行：遍历图中的每一个顶点
        for (let vertex in this.adjacencyList) {
            if (!visited.has(vertex)) {// 第四行：如果这个顶点还没被探索过
                const component = new Set();// 第五行：创建一个新的"岛屿群"容器
                this._dfs(vertex, component);// 第六行：从这个顶点开始DFS，探索整个连通分量
                components.push(Array.from(component));// 第七行：把这个连通分量转换成数组，加入到结果中
                // 第八行：把这个连通分量里的所有顶点标记为已访问
                for (let v of component) {
                    visited.add(v);
                }
            }
        }
        // 第九行：返回所有找到的连通分量
        return components;
    }
/*isConnected() {
    const vertices = Object.keys(this.adjacencyList);  // O(V)
    if (vertices.length === 0) return true;
    const visited = new Set();
    this._dfs(vertices[0], visited);  // O(V + E) - 遍历所有顶点和边
    return visited.size === vertices.length;  // O(1)
}
总时间复杂度：O(V + E)//
方法	                           目的	       返回值	          应用场景
isConnected()	            检查整个图是否连通	boolean      	快速判断连通性
getConnectedComponents()	找出所有连通分量	Array<Array>	详细分析图结构
*/
    // 完整的欧拉路径检查
    hasEulerianPath() {
        if (!this.isConnected()) {
            console.log("❌ 图不连通，不存在欧拉路径");
            return false;
        }
        
        let oddDegreeCount = 0;
        for (let vertex in this.adjacencyList) {
            const degree = this.getDegree(vertex);
            if (degree % 2 !== 0) {
                oddDegreeCount++;
            }
        }
        
        const result = oddDegreeCount === 0 || oddDegreeCount === 2;
        if (result) {
            console.log(`✓ 存在欧拉路径（奇度顶点数: ${oddDegreeCount}）`);
        } else {
            console.log(`❌ 不存在欧拉路径（奇度顶点数: ${oddDegreeCount}，需要0或2）`);
        }
        return result;
    }
    
    // 检查欧拉回路
    hasEulerianCircuit() {
         // 必须先检查连通性！
        if (!this.isConnected()) {
            console.log("❌ 图不连通，不存在欧拉回路");
            return false;
        }
        // 再检查度数条件
        for (let vertex in this.adjacencyList) {
            if (this.getDegree(vertex) % 2 !== 0) {
                console.log(`❌ 顶点 ${vertex} 的度数为奇数，不存在欧拉回路`);
                return false;
            }
        }
        
        console.log("✓ 存在欧拉回路（所有顶点度数为偶数且图连通）");
        return true;
    }
    
    // 打印图信息
    printGraphInfo() {
        console.log("\n" + "=".repeat(50));
        console.log("图结构分析");
        console.log("=".repeat(50));
        
        // 打印所有顶点度数
        console.log("\n顶点度数分布:");
        const degrees = {};
        for (let vertex in this.adjacencyList) {
            degrees[vertex] = this.getDegree(vertex);
            console.log(`  顶点 ${vertex}: 度 = ${degrees[vertex]}`);
        }
        
        // 连通性分析
        console.log("\n连通性分析:");
        console.log(`  是否连通: ${this.isConnected()}`);
        const components = this.getConnectedComponents();
        console.log(`  连通分量: ${JSON.stringify(components)}`);
        
        // 边信息
        console.log(`\n图统计:`);
        console.log(`  总顶点数: ${Object.keys(this.adjacencyList).length}`);
        console.log(`  总边数: ${this.edges.size}`);
        
        // 欧拉性质判断
        console.log("\n欧拉性质判断:");
        this.hasEulerianPath();
        this.hasEulerianCircuit();
        
        console.log("=".repeat(50));
    }
}

// ========== 测试用例 ==========

console.log("🏁 开始图论测试...");

// 测试1：经典的4个顶点全连通，每个顶点度数为6（欧拉回路）
console.log("\n🧪 测试1: 4顶点全连通，每个度数为6（欧拉回路）");
const graph1 = new ProfessionalGraph();

// 创建4个顶点：A, B, C, D 全连通
// 每个顶点到其他3个顶点都有2条边 → 度数 = 3 × 2 = 6

// A的连接
graph1.addEdge('e1', 'A', 'B', 1);
graph1.addEdge('e2', 'A', 'B', 1); // 平行边
graph1.addEdge('e3', 'A', 'C', 1);
graph1.addEdge('e4', 'A', 'C', 1); // 平行边
graph1.addEdge('e5', 'A', 'D', 1);
graph1.addEdge('e6', 'A', 'D', 1); // 平行边

// B的连接（除了A-B已经建立，还需要B-C, B-D）
graph1.addEdge('e7', 'B', 'C', 1);
graph1.addEdge('e8', 'B', 'C', 1); // 平行边
graph1.addEdge('e9', 'B', 'D', 1);
graph1.addEdge('e10', 'B', 'D', 1); // 平行边

// C的连接（除了A-C, B-C已经建立，还需要C-D）
graph1.addEdge('e11', 'C', 'D', 1);
graph1.addEdge('e12', 'C', 'D', 1); // 平行边

graph1.printGraphInfo();

// 测试2：非连通图
console.log("\n🧪 测试2: 非连通图");
const graph2 = new ProfessionalGraph();

// 分量1: 三角形
graph2.addEdge('e1', 'A', 'B', 1);
graph2.addEdge('e2', 'B', 'C', 1);
graph2.addEdge('e3', 'C', 'A', 1);

// 分量2: 线段
graph2.addEdge('e4', 'D', 'E', 1);

// 孤立点
graph2.addVertex('F');

graph2.printGraphInfo();

// 测试3：欧拉路径（2个奇度顶点）
console.log("\n🧪 测试3: 欧拉路径（2个奇度顶点）");
const graph3 = new ProfessionalGraph();

// 创建一条路径：A-B-C-D，A和D度数为1（奇数），B和C度数为2（偶数）
graph3.addEdge('e1', 'A', 'B', 1);
graph3.addEdge('e2', 'B', 'C', 1);
graph3.addEdge('e3', 'C', 'D', 1);

graph3.printGraphInfo();

// 测试4：验证我们的"2-3-3-4"例子
console.log("\n🧪 测试4: 2-3-3-4度数分布");
const graph4 = new ProfessionalGraph();

// 创建2-3-3-4度数分布
graph4.addEdge('e1', 'A', 'B', 1);
graph4.addEdge('e2', 'A', 'C', 1);      // A:度2

graph4.addEdge('e3', 'B', 'C', 1);
graph4.addEdge('e4', 'B', 'D', 1);      // B:度3

graph4.addEdge('e5', 'C', 'D', 1);      // C:度3

// 让D度数为4：添加自环（自环算2度）
graph4.addEdge('e6', 'D', 'D', 1);      // D:度4

graph4.printGraphInfo();

// 验证度数
console.log("\n✅ 度数验证:");
console.log(`A的度数: ${graph4.getDegree('A')} (目标: 2)`);
console.log(`B的度数: ${graph4.getDegree('B')} (目标: 3)`);
console.log(`C的度数: ${graph4.getDegree('C')} (目标: 3)`);
console.log(`D的度数: ${graph4.getDegree('D')} (目标: 4)`);

console.log("\n🎉 所有测试完成！");
```