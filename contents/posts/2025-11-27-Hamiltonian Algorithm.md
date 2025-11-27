# Hamiltonian Path Cycle Algorithm
## 基础知识

- **定义**
    - 哈密顿路径搜索算法 (Hamiltonian Path Search Algorithm)
    ```
    给定无向图或有向图 G = (V, E)，哈密顿路径算法旨在找到一条经过图中每个顶点恰好一次的路径 P = (v₁, v₂, ..., vₙ)，其中：n = |V|（顶点总数）∀i ≠ j, vᵢ ≠ vⱼ（顶点不重复）∀1 ≤ i < n, (vᵢ, vᵢ₊₁) ∈ E（相邻顶点有边连接）
    ```
    - 哈密顿回路搜索算法 (Hamiltonian Cycle Search Algorithm)
    ```
    给定无向图或有向图 G = (V, E)，哈密顿回路算法旨在找到一个经过图中每个顶点恰好一次的环 C = (v₁, v₂, ..., vₙ, v₁)，其中：n = |V|（顶点总数）∀i ≠ j, vᵢ ≠ vⱼ（顶点不重复，除首尾外）∀1 ≤ i ≤ n, (vᵢ, vᵢ₊₁) ∈ E，其中 vₙ₊₁ = v₁（形成环）首尾顶点相同：v₁ = vₙ₊₁
    ```
## 注意事项
1. **混淆点**

|问题类型|	访问对象	|要求	|判断条件|
---|---|---|---
|哈密顿路径	|顶点|	每个顶点一次	|NP完全|
|哈密顿回路	|顶点|	每个顶点一次+返回起点|	NP完全|
|欧拉路径	|边	|每条边一次|	度数条件|
|欧拉回路	|边	|每条边一次+返回起点	|所有顶点度数为偶|


2. **代码实现**
```
function hamiltonianPathBasic(graph) {
    const vertices = Object.keys(graph);
    
    for (let startVertex of vertices) {//vertices 是所有顶点的数组
        const path = [startVertex];
        const visited = new Set([startVertex]); // 记录当前起始顶点已被访问,startVertex 是循环变量，表示当前尝试的起点
        
        if (backtrackBasic(graph, path, visited, vertices.length)) {//如果从当前起点开始找到了哈密顿路径，就返回这个路径
            return path; //返回找到的路径
        }
    }
    return null;
}

function backtrackBasic(graph, path, visited, totalVertices) {
    // 终止条件：路径包含所有顶点
    if (path.length === totalVertices) { //检查路径长度
        return true; // 找到解
    }
    //已访问集合决定了是否访问过（搜索状态）算法通过遍历当前顶点的邻居，自动处理了能否到达的问题，我们只需要关心是否访问过
    const current = path[path.length - 1];
    
    for (let neighbor of graph[current]) {
        if (!visited.has(neighbor)) { //检查邻居是否未访问
            // 做出选择
            visited.add(neighbor); // 标记为已访问
            path.push(neighbor); // 加入路径
            
            if (backtrackBasic(graph, path, visited, totalVertices)) {
                return true;
            }
            
            // 回溯
            visited.delete(neighbor); // 移除访问标记
            path.pop(); // 移除最后一个顶点
        }
    }
    
    return false;
}
/*
👉同一个图，两种不同的路径
const graph = {
    A: ["B", "C"],
    B: ["A", "C", "D"], 
    C: ["A", "B", "D"],
    D: ["B", "C"]
};

哈密顿路径：访问每个顶点一次
示例：A → B → C → D  (访问了A,B,C,D各一次)
关注：顶点集合的排列
欧拉路径：经过每条边一次  
示例：A → B → D → C → B → C → A
关注：边集合的遍历

哈密顿路径关注去哪些地方，欧拉路径关注走哪些路
哈密顿路径重点：检查顶点访问情况
欧拉路径重点：检查边使用情况
*/
/*
👉软件工程:分离关注点 (Separation of Concerns)
1. 单一职责原则每个方法只做一件事:hamiltonianPathBasic：管理搜索流程,backtrackBasic：执行回溯算法
2. 可复用性:backtrack函数可以在其他地方使用
3. 清晰的接口
4. 易于测试
方法1：hamiltonianPathBasic - 协调者                          方法2：backtrackBasic - 工作者
function hamiltonianPathBasic(graph) {                      function backtrackBasic(graph, path, visited, totalVertices) {
    // 职责：管理整个搜索过程                                         // 职责：执行具体的回溯搜索
    // - 尝试不同的起点                                             // - 深度优先探索
    // - 初始化搜索状态                                             // - 处理选择和撤销
    // - 决定何时停止                                               // - 递归调用自身
    // - 返回最终结果                                                }
}
*/
/*
👉计算/搜索
计算:需要探索多种可能性,涉及决策和回溯,时间复杂度高这个类是一个问题求解器 (Problem Solver)
class HamiltonianSolver {
    // 构造函数：问题建模
    // findPath()：问题求解  
    // dfs()：搜索策略
    // reconstructPath()：结果构建
}
*/
class HamiltonianSolver {
    constructor(graph) {
        this.graph = graph;
        this.vertices = Object.keys(graph);
        this.vertexToIndex = {};
        this.vertices.forEach((v, i) => {
            this.vertexToIndex[v] = i;
        });
    }
    findPath() {
        const parent = new Array(this.vertices.length).fill(-1); //父指针数组
        
        for (let i = 0; i < this.vertices.length; i++) {
            const visited = 1 << i;
            parent[i] = -1; //初始化起点父节点
            
            if (this.dfs(i, visited, parent)) {
                return this.reconstructPath(parent); //重构路径
            }
        }
        return null;
    }
    dfs(current, visited, parent) {
        // 所有顶点都已访问
        if (visited === (1 << this.vertices.length) - 1) { //检查完整访问
            return true;
        }
        
        for (let neighbor of this.graph[this.vertices[current]]) {
            const neighborIndex = this.vertexToIndex[neighbor]; //获取邻居索引
            
            if (visited & (1 << neighborIndex)) {
                continue;
            }
            
            const newVisited = visited | (1 << neighborIndex);
            parent[neighborIndex] =  current; //记录父节点
            
            if (this.dfs(neighborIndex, newVisited, parent)) {
                return true;
            }
        }
        
        return false;
    }
    reconstructPath(parent) {
        // 找到路径的终点（最后一个被访问的顶点）
        let endVertex = -1;
        for (let i = 0; i < parent.length; i++) {
            if (parent[i] !== -1) {
                let count = 0;
                for (let j = 0; j < parent.length; j++) {
                    if (parent[j] !== -1) count++;
                }
                if (count === this.vertices.length) {
                    endVertex = i;
                    break;
                }
            }
        }
        
        // 反向重构路径
        const path = [];//步骤1：找到终点
        let current = endVertex;
        while (current !== -1) { // 重构终止条件,当current不是-1时继续
            path.push(this.vertices[current]);//步骤2：反向追踪
            current = parent[current]; // 向父节点移动
        }
        //不需要再添加起点循环中已经包含了
        return path.reverse();//步骤3：反转路径
    }
}
//验证函数
function isValidHamiltonianPath(graph, path) {
    if (!path || path.length === 0) return false;
    
    // 检查路径长度
    if (path.length !== Object.keys(graph).length) { // 检查顶点数量
        return false;
    }
    
    // 检查是否有重复顶点
    const uniqueVertices = new Set(path); //去重检查
    if (uniqueVertices.size !== path.length) {
        return false;
    }
    
    // 检查路径连通性
    for (let i = 0; i < path.length - 1; i++) {
        const current = path[i];
        const next = path[i + 1];
        
        if (!graph[current].includes(next)) { //检查边是否存在
            return false;
        }
    }
    
    return true;
}
// 测试图
const testGraph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
};

// 测试你的实现
const path = hamiltonianPathBasic(testGraph);
console.log("找到的路径:", path);
console.log("路径是否有效:", isValidHamiltonianPath(testGraph, path));

class HamiltonianStabilityTester {
    constructor() {
        this.testCases = this.createTestCases();
        this.results = [];
    }
    
    createTestCases() {
        return {
            // 测试1：简单完全图（一定有哈密顿路径）
            completeGraph: {
                name: "完全图 K4",
                graph: {
                    'A': ['B', 'C', 'D'],
                    'B': ['A', 'C', 'D'],
                    'C': ['A', 'B', 'D'],
                    'D': ['A', 'B', 'C']
                },
                expected: true
            },
            
            // 测试2：链状图（一定有哈密顿路径）
            chainGraph: {
                name: "链状图",
                graph: {
                    'A': ['B'],
                    'B': ['A', 'C'],
                    'C': ['B', 'D'],
                    'D': ['C', 'E'],
                    'E': ['D']
                },
                expected: true
            },
            
            // 测试3：星形图（没有哈密顿路径）
            starGraph: {
                name: "星形图（无解）",
                graph: {
                    'A': ['B', 'C', 'D'],
                    'B': ['A'],
                    'C': ['A'],
                    'D': ['A']
                },
                expected: false
            },
            
            // 测试4：复杂连通图
            complexGraph: {
                name: "复杂连通图",
                graph: {
                    'A': ['B', 'C', 'D'],
                    'B': ['A', 'D', 'E'],
                    'C': ['A', 'D', 'F'],
                    'D': ['A', 'B', 'C', 'E', 'F', 'G'],
                    'E': ['B', 'D', 'G'],
                    'F': ['C', 'D', 'G'],
                    'G': ['D', 'E', 'F']
                },
                expected: true
            },
            
            // 测试5：不连通图（无解）
            disconnectedGraph: {
                name: "不连通图（无解）",
                graph: {
                    'A': ['B'],
                    'B': ['A'],
                    'C': ['D'],
                    'D': ['C'],
                    'E': ['F'],
                    'F': ['E']
                },
                expected: false
            },
            
            // 测试6：大型图测试
            largeGraph: {
                name: "8顶点复杂图",
                graph: {
                    'A': ['B', 'C', 'D'],
                    'B': ['A', 'D', 'E', 'F'],
                    'C': ['A', 'D', 'G'],
                    'D': ['A', 'B', 'C', 'E', 'H'],
                    'E': ['B', 'D', 'F', 'H'],
                    'F': ['B', 'E', 'G', 'H'],
                    'G': ['C', 'F', 'H'],
                    'H': ['D', 'E', 'F', 'G']
                },
                expected: true
            },
            
            // 测试7：有孤立顶点的图
            isolatedVertexGraph: {
                name: "有孤立顶点的图",
                graph: {
                    'A': ['B', 'C'],
                    'B': ['A', 'C'],
                    'C': ['A', 'B'],
                    'D': []  // 孤立顶点
                },
                expected: false
            }
        };
    }
    
    runAllTests() {
        console.log("🚀 开始哈密顿路径稳定性测试\n");
        console.log("=" .repeat(50));
        
        let passed = 0;
        let failed = 0;
        
        for (const [testKey, testCase] of Object.entries(this.testCases)) {
            console.log(`\n📋 测试: ${testCase.name}`);
            console.log(`图结构:`, Object.keys(testCase.graph).map(v => `${v}: [${testCase.graph[v].join(', ')}]`).join(', '));
            
            try {
                const startTime = performance.now();
                const path = hamiltonianPathBasic(testCase.graph);
                const endTime = performance.now();
                const executionTime = (endTime - startTime).toFixed(2);
                
                const isValid = path ? isValidHamiltonianPath(testCase.graph, path) : false;
                const foundPath = path !== null;
                const testPassed = foundPath === testCase.expected;
                
                // 记录结果
                const result = {
                    testName: testCase.name,
                    expected: testCase.expected,
                    found: foundPath,
                    path: path,
                    executionTime: executionTime + 'ms',
                    valid: isValid,
                    passed: testPassed
                };
                
                this.results.push(result);
                
                // 输出结果
                if (testPassed) {
                    console.log(`✅ 通过 | 耗时: ${executionTime}ms`);
                    passed++;
                } else {
                    console.log(`❌ 失败 | 耗时: ${executionTime}ms`);
                    failed++;
                }
                
                if (path) {
                    console.log(`  找到路径: ${path.join(' → ')}`);
                    console.log(`  路径验证: ${isValid ? '有效' : '无效'}`);
                } else {
                    console.log(`  未找到哈密顿路径`);
                }
                
            } catch (error) {
                console.log(`💥 错误: ${error.message}`);
                failed++;
            }
        }
        
        this.printSummary(passed, failed);
        return this.results;
    }
    
    printSummary(passed, failed) {
        console.log("\n" + "=" .repeat(50));
        console.log("📊 哈密顿路径算法测试总结");
        console.log("=" .repeat(50));
        console.log(`✅ 通过: ${passed} 个测试`);
        console.log(`❌ 失败: ${failed} 个测试`);
        console.log(`📈 成功率: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
        
        console.log("\n🔍 详细结果:");
        this.results.forEach((result, index) => {
            console.log(`  ${index + 1}. ${result.testName}: ${result.passed ? '✅' : '❌'} (${result.executionTime})`);
        });
    }
    
    
    
    generateRandomGraph(size, connectivity = 0.5) {
        const graph = {};
        const vertices = Array.from({length: size}, (_, i) => `V${i + 1}`);
        
        // 初始化图
        vertices.forEach(vertex => {
            graph[vertex] = [];
        });
        
        // 随机添加边
        for (let i = 0; i < vertices.length; i++) {
            for (let j = i + 1; j < vertices.length; j++) {
                if (Math.random() < connectivity) {
                    graph[vertices[i]].push(vertices[j]);
                    graph[vertices[j]].push(vertices[i]);
                }
            }
        }
        
        return graph;
    }
}

// 🚀 运行稳定性测试
async function runStabilityTest() {
    const tester = new HamiltonianStabilityTester();
    
    // 运行基础测试
    console.log("🎯 第一阶段：基础功能测试");
    tester.runAllTests();
    
    return tester.results;
}

// 立即运行测试
runStabilityTest().then(results => {
    console.log("\n🎊 基础测试完成！");
});

/*
👉NP完全
NP完全 = 验证容易 + 求解极难 + 是所有难题的代表
NP完全的判断条件:个问题是NP完全的，需要满足：
条件1：属于NP类
// 能在多项式时间内验证解
function verifySolution(problem, solution) {
     例如验证哈密顿回路：
    1. 检查是否访问所有顶点  O(n)
    2. 检查是否回到起点  O(1)  
    3. 检查边是否存在 O(n)
    总时间: O(n) - 多项式时间！
}
                 
条件2：所有NP问题都能归约到它
如果问题A能"转化"为问题B，且：
- A是NP完全的
- 转化过程是多项式的
那么B也是NP完全的！
哈密顿路径/回路:验证：给你路径，容易检查;求解：可能要尝试n!种排列

遇到NP完全问题，就知道：
if (problem.isNPComplete()) {
// 不要寻找完美的最优解
// 考虑：近似算法、启发式方法、限制问题规模
}
*/


// ==================== 🔄哈密顿回路算法 ==================== //

function hamiltonianCycle(graph) {
    const vertices = Object.keys(graph);
    console.log("🔍 开始寻找哈密顿回路...");
    console.log("图顶点:", vertices);
    
    for (let startVertex of vertices) {
        console.log(`\n🚀 尝试从 ${startVertex} 开始寻找回路...`);
        const path = [startVertex];
        const visited = new Set([startVertex]);
        //👉返回包含起点的闭合回路
        if (backtrackCycle(graph, path, visited, vertices.length, startVertex)) {
            console.log("🎉 找到哈密顿回路!");
            return path;
        } else {
            console.log(`❌ 从 ${startVertex} 出发未找到回路`);
        }
    }
    
    console.log("💥 图中不存在哈密顿回路");
    return null;
}

function backtrackCycle(graph, path, visited, totalVertices, startVertex) {
    const current = path[path.length - 1];
    console.log(`  当前路径: [${path}], 在顶点 ${current}`);
    
    // 终止条件：路径包含所有顶点
    if (path.length === totalVertices) {
        console.log(`  📍 已访问所有顶点，检查能否回到起点 ${startVertex}...`);
        
        //👉关键区别：检查能否回到起点
        if (graph[current].includes(startVertex)) {
            path.push(startVertex); // 闭合回路
            console.log(`  ✅ 可以回到起点！形成回路: [${path}]`);
            return true;
        } else {
            console.log(`  ❌ 无法从 ${current} 回到起点 ${startVertex}`);
            return false;
        }
    }
    
    // 尝试所有未访问的邻居
    for (let neighbor of graph[current]) {
        if (!visited.has(neighbor)) {
            console.log(`  → 尝试 ${current} → ${neighbor}`);
            
            visited.add(neighbor);
            path.push(neighbor);
            
            if (backtrackCycle(graph, path, visited, totalVertices, startVertex)) {
                return true;
            }
            
            // 回溯
            console.log(`  ← 回溯: 移除 ${neighbor}`);
            visited.delete(neighbor);
            path.pop();
        } else {
            console.log(`  ⏭️  跳过 ${neighbor} (已访问)`);
        }
    }
    
    console.log(`  💥 ${current} 的所有选项都尝试完了`);
    return false;
}
//验证函数
function isValidHamiltonianCycle(graph, cycle) {
    if (!cycle || cycle.length === 0) {
        console.log("❌ 回路为空");
        return false;
    }
    
    const vertices = Object.keys(graph);
    console.log(`🔍 验证回路: [${cycle}]`);
    
    // 检查1: 长度应该是顶点数 + 1
    if (cycle.length !== vertices.length + 1) {
        console.log(`❌ 长度错误: 期望 ${vertices.length + 1}, 实际 ${cycle.length}`);
        return false;
    }
    
    // 检查2: 首尾必须相同
    if (cycle[0] !== cycle[cycle.length - 1]) {
        console.log(`❌ 首尾不同: 开始=${cycle[0]}, 结束=${cycle[cycle.length - 1]}`);
        return false;
    }
    
    // 检查3: 中间顶点不能重复
    const middleVertices = cycle.slice(0, -1); // 排除最后一个（与第一个相同）
    const uniqueVertices = new Set(middleVertices);
    if (uniqueVertices.size !== middleVertices.length) {
        console.log(`❌ 中间顶点有重复: [${middleVertices}]`);
        return false;
    }
    
    // 检查4: 必须包含所有顶点
    if (uniqueVertices.size !== vertices.length) {
        console.log(`❌ 未包含所有顶点: 缺少 ${vertices.filter(v => !uniqueVertices.has(v))}`);
        return false;
    }
    
    // 检查5: 所有边必须存在
    for (let i = 0; i < cycle.length - 1; i++) {
        const current = cycle[i];
        const next = cycle[i + 1];
        
        if (!graph[current].includes(next)) {
            console.log(`❌ 边不存在: ${current} → ${next}`);
            return false;
        }
    }
    
    console.log("✅ 哈密顿回路验证通过!");
    return true;
}
// 测试图1: 有哈密顿回路
const graphWithCycle = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
};
/*
👉注意:
回溯的起点是C，不是D;D只是回溯的第一个被移除的顶点
哈密顿回路的要求是：访问所有顶点各一次,最后回到起点
回溯流程:
第1阶段：第一次尝试（失败）     第2阶段：开始回溯                            第3阶段：重新选择
路径: [A]                   从 [A,B,C,D] 开始回溯：                      在 [A,B] 时：
→ A → B → [A,B]             1. 移除 D → [A,B,C]   （撤销 C→D 的选择）    B的邻居：[A(已访问), C(试过了), D(未尝试)]
→ B → C → [A,B,C]           2. 在C：还有其他选择吗？没有！                 → 尝试 B → D → [A,B,D]
→ C → D → [A,B,C,D]         3. 移除 C → [A,B]     （撤销 B→C 的选择）    C:已尝试（刚才走过B→C→D但失败了）D: 未尝试（B→D这个分支还没探索过）
检查：D 能直接回 A 吗？        在C所有未访问的邻居都尝试过了，但都走不通C只有
结果：这条路走不通！           一个未访问邻居：D;尝试了 C→D，但最终失败       
                            C这个分支是死路

第4阶段：新的探索                            第5阶段：成功！
在 [A,B,D] 时：                            在 [A,B,D,C] 时：已访问所有顶点 A,B,D,C检查 C → A：✅ 可以！形成回路：[A,B,D,C,A]
D的邻居：[B(已访问), C(未访问)]
→ 跳过 B，选择 D → C → [A,B,D,C] 
*/
// 测试图2: 无哈密顿回路
const graphWithoutCycle = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B'],
    'D': ['E'],
    'E': ['D']
};


console.log("🧪 ========== 测试1: 有回路的图 ==========");
const cycle1 = hamiltonianCycle(graphWithCycle);
console.log("最终结果:", cycle1);
if (cycle1) {
    console.log("验证结果:", isValidHamiltonianCycle(graphWithCycle, cycle1));
}

console.log("\n🧪 ========== 测试2: 无回路的图 ==========");
const cycle2 = hamiltonianCycle(graphWithoutCycle);
console.log("最终结果:", cycle2);
if (cycle2) {
    console.log("验证结果:", isValidHamiltonianCycle(graphWithoutCycle, cycle2));
}

// ==================== 性能测试 ====================

console.log("\n⚡ ========== 性能测试 ==========");
const performanceGraph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'D', 'E'],
    'C': ['A', 'B', 'D', 'F'],
    'D': ['A', 'B', 'C', 'E', 'F', 'G'],
    'E': ['B', 'D', 'F', 'G'],
    'F': ['C', 'D', 'E', 'G'],
    'G': ['D', 'E', 'F']
};

console.time("哈密顿回路搜索");
const performanceCycle = hamiltonianCycle(performanceGraph);
console.timeEnd("哈密顿回路搜索");
console.log("性能测试结果:", performanceCycle);
```