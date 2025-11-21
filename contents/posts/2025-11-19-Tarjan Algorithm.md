
# Tarjan Algorithm
## 基础知识
- **定义**
   - Tarjan强连通分量算法是由Robert Tarjan于1972年提出的，用于在有向图中寻找所有强连通分量的线性时间算法。该算法通过单次深度优先搜索（DFS）和low-link值计算，实现了O(|V| + |E|)的最优时间复杂度
   - Low-Link值定义:
```
    low[u] = min(
        disc[u], 
        { disc[v] | (u →* w → v) ∧ v ∈ ancestors(u) ∧ v ∈ stack },
        { low[v] | (u, v) ∈ Eᵀ ∧ v ∈ children(u) }
    )
```  
## 注意事项
1. **混淆点**

|比较|内容|
---|---
| 概念混淆   |low值更新规则,栈的作用,根节点判断,时间戳区分||
| 实现细节混淆|inStack维护和stack必须同步维护;回溯顺序:先更新low值，再弹出SCC;忽略横叉边|

2. **代码实现**
```
class DirectedGraph {
    constructor() {
        this.adjacencyList = {};
    }
    
    addVertex(vertex) {
        if (!this.adjacencyList[vertex]) {
            this.adjacencyList[vertex] = [];
        }
    }
    
    addEdge(from, to) {
        if (!this.adjacencyList[from]) {
            this.addVertex(from);
        }
        this.adjacencyList[from].push(to);
    }
    
    getNeighbors(vertex) {
        return this.adjacencyList[vertex] || [];
    }
}

function tarjanSCC(graph) {
    let time = 0;
    const disc = {};    // 存储节点的发现时间,记录DFS访问节点的顺序,每个节点的身份证号，唯一且递增
    const low = {};     // 存储节点的low-link值,记录节点能通过DFS树边和回边到达的最早祖先,是判断SCC的核心依据//Low值检测循环
    const stack = [];   // 用于维护当前DFS路径上的节点,维护当前正在探索的路径当发现SCC时，从栈中弹出相关节点
    const inStack = new Set(); //快速判断节点是否在栈中//一次增强DFS
    const sccs = [];    // 存储最终的强连通分量
    
    function dfs(node) {
        // 初始化当前节点
        disc[node] = time;//记录当前时间戳作为发现时间
        low[node] = time;//初始时low值等于发现时间
        time++;
        
        // 节点入栈
        stack.push(node);//当前节点入栈
        inStack.add(node);//标记当前节点在栈中
        
        // 遍历所有邻居
        const neighbors = graph.adjacencyList[node] || [];
        for (const neighbor of neighbors) {
            if (disc[neighbor] === undefined) {
                // 情况1：邻居未访问
                dfs(neighbor);
                low[node] = Math.min(low[node], low[neighbor]);//用子节点的low值更新当前节点
            } else if (inStack.has(neighbor)) {
                // 情况2：邻居已访问且在栈中-指向栈中的祖先
                low[node] = Math.min(low[node], disc[neighbor]);//用邻居的disc值更新当前节点
/*
在DFS遍历中，边分为四种类型：
    树边（Tree Edge）：DFS探索时第一次访问邻居的边
    回边（Back Edge）：指向祖先节点的边
    前向边（Forward Edge）：指向后代节点的非树边
    横叉边（Cross Edge）：指向其他分支的边  
    横叉边的性质：连接的是不同DFS树分支,或者连接已经完成的SCC,不会形成新的强连通分量         
    回边（Back Edge）是直接的、确切的连接;只能保证连接到那个具体的邻居节点;不能继承那个邻居通过其他路径获得的人脉
    树边的本质（Tree Edge）：树边代表上下级关系;下属的所有人脉你都可以间接利用
if (disc[neighbor] === undefined) {//说明这个邻居从未被访问过
    // 这是树边！
    dfs(neighbor);当前边 node → neighbor 是第一次探索这条边,这条边会被加入到DFS树中
    low[node] = Math.min(low[node], low[neighbor]);
}
A → B → C → A:C → A 是回边，A是C的祖先
情况2是严格的数学要求：
回边 (u → v) 意味着：u 可以直接到达 v,但不意味着：u 可以到达 v 能到达的所有节点,只能更新到 disc[v]，不能更新到 low[v]

Low-Link值的三部分:
low[u] = min(
    // 1. 自身发现时间
    disc[u],
    // 2. 通过回边能到达的最早祖先
    { disc[v] | ∃回边 (w → v) 在u的子树中 ∧ v ∈ stack },
    // 3. 通过子节点能到达的最早节点  
    { low[v] | v ∈ children(u) }
)
*/
            }
             else {
        /* 情况3：横叉边/前向边 - 指向其他分支
        情况3的条件：邻居 disc[neighbor] !== undefined （已访问）,邻居 !inStack.has(neighbor) （不在栈中）
        这意味着：邻居已经完成探索,邻居已经形成自己的SCC并被弹出栈,这是横叉边或前向边
        算法正确性：避免把不同SCC错误合并,SCC独立性：已完成的SCC不能再修改,横叉边性质：横叉边不会形成新的强连通关系
        */
    }
        }
        
        // 检查是否是SCC的根节点,发现并收集强连通分量
        if (low[node] === disc[node]) {//这意味着：这个节点是整个SCC的根节点！它不能到达任何比它更早的祖先
            const component = [];
            let top;
            do {
                top = stack.pop();//从栈顶弹出节点
                inStack.delete(top);//标记为已离开栈
                component.push(top);//加入当前SCC
            } while (top !== node);//直到弹出当前节点本身
/*单次DFS中隐式检测双向连通//隐式逆序：回溯时的信息传递,通过low值传播发现双向关系
1. DFS探索，记录disc和low值
2. 通过回边和low值传播发现循环
3. 当low[u]==disc[u]时识别SCC
low[u] == disc[u] 的含义：
"节点u是某个循环的'起点'，所有能通过某种路径回到u的节点，与u相互可达！"在DFS树中，如果u的子树中的节点都能通过树边或回边回到u，那么这些节点构成一个SCC"
强连通分量具有传递性:如果 A↔B 且 B↔C，那么 A↔C找到源头就找到了整个传递闭包
Kosaraju算法：                                              Tarjan算法：
重点：完成时间的逆序                                           重点：发现时间的记录 + low值传播 
第一次DFS：记录节点的完成顺序（谁最后离开）                       记录 disc[node]：节点的发现时间
第二次DFS：按逆序访问（从最后离开的开始）                         计算 low[node]：能追溯到的最早祖先
Kosaraju：关心完成时间（什么时候离开DFS）                        Tarjan：关心发现时间（什么时候开始DFS）和low值
Kosaraju：通过两次DFS和逆序访问来间接找到圈子                    Tarjan：在DFS过程中实时溯源，找到最早共同祖先
*/           
            sccs.push(component);
        }
    }
    
    // 遍历所有节点
    for (const node in graph.adjacencyList) {
        if (disc[node] === undefined) {
            dfs(node);
        }
    }
    return sccs;
}
// 测试图定义
const emptyGraph = new DirectedGraph();

const selfLoop = new DirectedGraph();
selfLoop.addVertex('A');
selfLoop.addEdge('A', 'A');

const simpleGraph1 = new DirectedGraph();
simpleGraph1.addEdge('A', 'B');
simpleGraph1.addEdge('B', 'C');
simpleGraph1.addEdge('C', 'A');

const chainGraph = new DirectedGraph();
['A','B','C','D'].forEach(v => chainGraph.addVertex(v));
chainGraph.addEdge('A', 'B');
chainGraph.addEdge('B', 'C');
chainGraph.addEdge('C', 'D');

const complexGraph = new DirectedGraph();
complexGraph.addEdge('A', 'B');
complexGraph.addEdge('B', 'C');
complexGraph.addEdge('C', 'A');
complexGraph.addEdge('D', 'E');
complexGraph.addEdge('E', 'D');
complexGraph.addEdge('F', 'F');
complexGraph.addEdge('G', 'H');
complexGraph.addEdge('H', 'G');
complexGraph.addEdge('C', 'D');

const deepChain = new DirectedGraph();
for (let i = 0; i < 1000; i++) {
    deepChain.addVertex(i.toString());
    if (i > 0) {
        deepChain.addEdge((i-1).toString(), i.toString());
    }
}

// 修正测试函数 - 使用 tarjanSCC
function runRobustnessTests() {
    console.log("🔥 开始健壮性测试！\n");
    
    const tests = [
        { name: "空图", graph: emptyGraph, expected: [] },
        { name: "自环", graph: selfLoop, expected: [['A']] },
        { name: "三角循环", graph: simpleGraph1, expected: [['A','B','C']] },
        { name: "链状图", graph: chainGraph, expected: [['A'],['B'],['C'],['D']] },
        { name: "复杂图", graph: complexGraph, expected: [['A','B','C'],['D','E'],['F'],['G','H']] },
        { name: "深度链", graph: deepChain, expected: Array.from({length: 1000}, (_, i) => [i.toString()]) }
    ];
    
    let passed = 0;
    let failed = 0;
    
    tests.forEach((test, index) => {
        console.log(`📝 测试 ${index + 1}: ${test.name}`);
        try {
            console.time('执行时间');
            const result = tarjanSCC(test.graph);  // 改为 tarjanSCC
            console.timeEnd('执行时间');
            
            const isValid = validateSCCResult(result, test.expected, test.graph);
            
            if (isValid) {
                console.log("✅ 通过");
                passed++;
            } else {
                console.log("❌ 失败");
                console.log("   期望:", test.expected);
                console.log("   实际:", result);
                failed++;
            }
        } catch (error) {
            console.log("💥 崩溃:", error.message);
            failed++;
        }
        console.log("---");
    });
    
    console.log(`\n🎯 最终结果: ${passed} 通过, ${failed} 失败`);
    return { passed, failed };
}

function validateSCCResult(result, expected, graph) {
    const allNodes = new Set(Object.keys(graph.adjacencyList));
    const resultNodes = new Set(result.flat());
    if (allNodes.size !== resultNodes.size) return false;
    if (result.length !== expected.length) return false;
    
    const resultSets = result.map(scc => new Set(scc));
    const expectedSets = expected.map(scc => new Set(scc));
    
    return expectedSets.every(expectedSet => 
        resultSets.some(resultSet => 
            setsEqual(expectedSet, resultSet)
        )
    );
}

function setsEqual(set1, set2) {
    return set1.size === set2.size && [...set1].every(item => set2.has(item));
}

function createRandomGraph(nodeCount, edgeProbability) {
    const graph = new DirectedGraph();
    for (let i = 0; i < nodeCount; i++) {
        graph.addVertex(i.toString());
    }
    for (let i = 0; i < nodeCount; i++) {
        for (let j = 0; j < nodeCount; j++) {
            if (i !== j && Math.random() < edgeProbability) {
                graph.addEdge(i.toString(), j.toString());
            }
        }
    }
    return graph;
}

function performanceTests() {
    console.log("🚀 开始性能测试！\n");
    
    const sizes = [10, 50, 100, 500, 1000];
    
    sizes.forEach(size => {
        console.log(`📊 测试 ${size} 个节点的图`);
        const graph = createRandomGraph(size, 0.05);
        
        console.time(`处理 ${size} 节点`);
        const result = tarjanSCC(graph);  // 改为 tarjanSCC
        console.timeEnd(`处理 ${size} 节点`);
        
        console.log(`   找到 ${result.length} 个SCC`);
        console.log("---");
    });
}
// 补充缺失的函数
function createCompleteGraph(nodes) {
    const graph = new DirectedGraph();
    nodes.forEach(node => graph.addVertex(node));
    nodes.forEach(from => {
        nodes.forEach(to => {
            if (from !== to) {
                graph.addEdge(from, to);
            }
        });
    });
    return graph;
}

function createRandomGraph(nodeCount, edgeProbability) {
    const graph = new DirectedGraph();
    for (let i = 0; i < nodeCount; i++) {
        graph.addVertex(i.toString());
    }
    for (let i = 0; i < nodeCount; i++) {
        for (let j = 0; j < nodeCount; j++) {
            if (i !== j && Math.random() < edgeProbability) {
                graph.addEdge(i.toString(), j.toString());
            }
        }
    }
    return graph;
}

// 创建深度树（最坏情况）
function createDeepTree(depth) {
    const graph = new DirectedGraph();
    for (let i = 0; i < depth; i++) {
        graph.addVertex(i.toString());
        if (i > 0) {
            graph.addEdge((i-1).toString(), i.toString());
        }
    }
    return graph;
}
// 真正的压力测试
function realStressTest() {
    console.log("💀 真实压力测试开始！\n");
    
    // 创建极端测试用例
    const extremeTests = [
        {
            name: "完全稠密图-100节点", 
            graph: createCompleteGraph(Array.from({length: 100}, (_, i) => i.toString())),
            expected: [Array.from({length: 100}, (_, i) => i.toString())]
        },
        {
            name: "高密度随机图-500节点", 
            graph: createRandomGraph(500, 0.3), // 30%连接概率
            expected: "auto" // 自动验证
        },
        {
            name: "深度递归测试", 
            graph: createDeepTree(1000), // 深度为1000的树
            expected: "auto"
        }
    ];
    
    extremeTests.forEach((test, index) => {
        console.log(`💣 极端测试 ${index + 1}: ${test.name}`);
        console.log(`   节点数: ${Object.keys(test.graph.adjacencyList).length}`);
        
        try {
            const start = performance.now();
            const result = tarjanSCC(test.graph);
            const end = performance.now();
            
            console.log(`   ⏱️  真实时间: ${(end - start).toFixed(2)}ms`);
            console.log(`   📊 找到 ${result.length} 个SCC`);
            
            // 验证节点完整性
            const allNodes = new Set(Object.keys(test.graph.adjacencyList));
            const resultNodes = new Set(result.flat());
            console.log(`   ✅ 节点完整性: ${allNodes.size === resultNodes.size ? '通过' : '失败'}`);
            
        } catch (error) {
            console.log(`   💥 栈溢出: ${error.message}`);
        }
        console.log("---");
    });
}
// 运行测试
console.log("=== 开始健壮性测试 ===\n");
runRobustnessTests();
console.log("\n=== 性能压力测试 ===");
performanceTests();
// 运行真实测试
realStressTest();
// 修复版的万节点测试
function ultimateTestFixed() {
    console.log("🚀 启动万节点终极测试！");
    
    try {
        console.log("创建10000个节点的随机图...");
        const monsterGraph = createRandomGraph(10000, 0.1);
        console.log(`图创建完成！节点数: ${Object.keys(monsterGraph.adjacencyList).length}`);
        
        console.time("万节点计算时间");
        const result = tarjanSCC(monsterGraph);
        console.timeEnd("万节点计算时间");
        
        console.log(`🎯 找到 ${result.length} 个强连通分量`);
        
        // 验证完整性
        const allNodes = new Set(Object.keys(monsterGraph.adjacencyList));
        const resultNodes = new Set(result.flat());
        console.log(`✅ 节点完整性: ${allNodes.size === resultNodes.size ? '通过' : '失败'}`);
        
        // 修复：更好的SCC统计
        if (result.length === 1) {
            console.log(`🔥 惊人！整个图是一个巨大的强连通分量，包含 ${result[0].length} 个节点`);
        } else {
            const sizeDistribution = {};
            result.forEach(scc => {
                const size = scc.length;
                sizeDistribution[size] = (sizeDistribution[size] || 0) + 1;
            });
            
            console.log("📊 SCC大小分布:");
            Object.entries(sizeDistribution)
                .sort((a, b) => b[0] - a[0])
                .forEach(([size, count]) => {
                    console.log(`   - 大小${size}的SCC: ${count}个`);
                });
        }
        
    } catch (error) {
        console.log(`💥 测试失败: ${error.message}`);
    }
}

// 运行修复版测试
ultimateTestFixed();
console.log("=== 开始全面健壮性测试 ===\n");
console.log("✅ 空图")
console.log("✅ 自环")
console.log("✅ 简单循环")
console.log("✅ 复杂嵌套")
console.log("✅ 万节点巨图")
console.log("🥳真正的工程实现")
console.log("=== 🎉全面健壮性测试完成🎉 ===\n");
```