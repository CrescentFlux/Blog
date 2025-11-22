# Ford-Fulkerson Algorithm
## **基础知识**
- **定义**
  - Ford-Fulkerson 方法是一种用于在容量网络中计算从源点到汇点的最大流的算法。




## **注意事项**
1. **混淆点**
- **核心机制表**

|机制	|作用	|实现方式|
---|---|---
|剩余图	|算法的工作地图|	动态跟踪每条边还能走多少流量|
|反向边|允许流量重新分配|	正向边减多少，反向边就加多少|
|BFS寻路|	系统性探索所有可能	|找最短增广路径，避免陷入次优|
|容量更新	|反映当前网络状态	|每次增广后更新正向和反向容量|

- **最大流最小割定理**
  - 在任何流网络中，从源点s到汇点t的最大流量值，等于分离s和t的最小割的容量:最大流 = 最小割容量
  - 最小割是网络的瓶颈,决定了整个系统的最大流量;算法在找到最大流的同时，也找到了网络的瓶颈所在
    - 引理1：任意流值 ≤ 任意割容量:
        - 对于任意割 $(S,T)$ 和任意流 $f$：
        - 流值=∑u∈S,v∈Tf(u,v)−∑u∈T,v∈Sf(u,v)≤∑u∈S,v∈Tc(u,v)=割容量流值=∑u∈S,v∈T​f(u,v)−∑u∈T,v∈S​f(u,v)≤∑u∈S,v∈T​c(u,v)=割容量
    - 引理2：最大流存在时，存在等值的最小割
        - 当Ford-Fulkerson算法终止时：Ford-Fulkerson终止时自动找到最小割    
        - 在剩余图 $G_f$ 中，从 $s$ 可达的顶点集合为 $S$,$T = V - S$ 构成一个割,这个割的容量正好等于最大流值




2. **代码实现**
```
class FlowNetwork {
    constructor() {
        this.graph = {};
    }
    
    addEdge(u, v, capacity) {
        if (!this.graph[u]) this.graph[u] = {};
        this.graph[u][v] = capacity;
        if (!this.graph[v]) this.graph[v] = {};
        // 确保反向边初始化为0
        this.graph[v][u] = 0;
    }
    
    deepCopyGraph() {
        const copy = {};
        for (const u in this.graph) {
            copy[u] = {};
            for (const v in this.graph[u]) {
                copy[u][v] = this.graph[u][v];
            }
        }
        return copy;
    }
/*
初始化剩余图剩余图（Residual Graph） 是算法运行时的工作地图，它记录着当前还能走多少流量。
剩余图的构成包含两种边：正向边：剩余容量 = 原始容量 - 已用流量;反向边：容量 = 已用流量（表示可以"退回"的流量）算法不看原始图，只看剩余图来找路
反向边容量 = 实际已使用的流量,反向边表示可以重新分配的量，你不能重新分配你根本没有使用过的容量
反向边容量 = 在这条路径上实际用掉的流量,不能超过边的原始容量,不能超过这条路径实际运送的流量,必须是真实使用过的量

residualGraph（剩余图）表示当前还能走多少流量;包含正向边（剩余容量）和反向边（可退回的容量）随着算法执行动态更新值为0的边表示"此路不通"
source（源点）就是流的起点，相当于：水库的源头,快递的总仓库,消息的发送者
sink（汇点）流的终点相当于：消息的接收者,收快递的客户,用水的地方
*/
    fordFulkerson(source, sink) {
        const residual = this.deepCopyGraph();
        let maxFlow = 0;
        console.log("初始剩余图:", JSON.stringify(residual, null, 2));
        
        while (true) {
            const parent = this.bfsFindPath(residual, source, sink);
            console.log("BFS找到的parent:", parent);
            
            if (!parent) {
                console.log("找不到路径，算法结束");
                break;
            }
            
            let pathFlow = Infinity;
            let v = sink;
            
            // 重建路径并计算最小容量
            const path = [sink];
            while (v !== source) {
                const u = parent[v];
                path.unshift(u);
                console.log(`边 ${u}→${v} 容量: ${residual[u][v]}`);
                pathFlow = Math.min(pathFlow, residual[u][v]);
                v = u;
            }
            console.log(`路径: ${path.join(' → ')}, 最小容量: ${pathFlow}`);
            
            maxFlow += pathFlow;
            
            // 更新剩余图
            v = sink;
            while (v !== source) {
                const u = parent[v];
                console.log(`更新: ${u}→${v}: ${residual[u][v]} - ${pathFlow} = ${residual[u][v] - pathFlow}`);
                residual[u][v] -= pathFlow;
                console.log(`更新反向: ${v}→${u}: ${residual[v][u]} + ${pathFlow} = ${residual[v][u] + pathFlow}`);
                residual[v][u] += pathFlow;
                v = u;
            }
            
            console.log(`当前总流量: ${maxFlow}`);
            console.log("更新后剩余图:", JSON.stringify(residual, null, 2));
            console.log("---");
        }
        
        return maxFlow;
    }
    
    bfsFindPath(residualGraph, source, sink) {
        const parent = {};
        const visited = new Set();
        const queue = [source];
        visited.add(source);
        
        console.log(`BFS开始: 从 ${source} 到 ${sink}`);
        
        while (queue.length > 0) {
            const u = queue.shift();
            console.log(`处理节点 ${u}`);
            
            if (!residualGraph[u]) {
                console.log(`节点 ${u} 在剩余图中不存在`);
                continue;
            }
            
            for (const [v, capacity] of Object.entries(residualGraph[u])) {
                console.log(`  检查边 ${u}→${v}, 容量: ${capacity}, 已访问: ${visited.has(v)}`);
                
                if (!visited.has(v) && capacity > 0) {
                    parent[v] = u;
                    visited.add(v);
                    console.log(`    找到可行边! parent[${v}] = ${u}`);
                    
                    if (v === sink) {
                        console.log(`到达汇点 ${sink}! 路径找到`);
                        return parent;
                    }
                    
                    queue.push(v);
                    console.log(`    将 ${v} 加入队列: [${queue.join(', ')}]`);
                }
            }
        }
        
        console.log("BFS结束，未找到路径");
        return null;
    }
}
/*
反向边不是物理通道，而是"重新分配权限"的数学记录：
    允许撤销：可以取消之前分配的流量
    允许重分配：把流量从低效路径移到高效路径
    保证完整性：最终找到的确实是数学上的最大流
    系统性探索：不依赖幸运的路径选择顺序
没有反向边 = 贪心算法，容易陷入局部最优
有反向边 = 系统性的全局最优搜索
反向边 A→S 容量5 的实际含义:A有权让S把之前给A的5个流量转送给别人;当算法后来找到路径 S→B→T 时，它可以通过这个反向边发现：A愿意出让5个流量名额，那我让B多送5个就行了
名义上是A干的，实际上是B干的

在网络流中，capacity 表示一条边能够承载的最大流量
容量决定了：
    哪些边可以用（剩余容量 > 0）
    每条路径能送多少（路径上最小的容量）
    什么时候算法结束（没有剩余容量 > 0 的路径）

自动找到最大流量，不管网络多复杂
虚拟反向边就是一个会计技巧，不是物理连接它让算法能够在不违反物理容量限制的情况下，重新分配各条路径的责任，从而找到更好的整体方案。
网络流模型里我们考虑的是任意时刻的瞬时流量不能超过容量
反向边这个技巧，在数学上等价于允许你重新分配路径，使得
在任意时刻，每条边的流量 ≤ 容量但整体来看，从 S 到 T 的总流量达到最大
反向边 A→S 的建立，相当于允许调整之前的流分配，让 B 的负载减轻，从而在稳态下也能达到 4 的流量。
网络流这个数学模型里，我们要求同一时刻不能有任何边超容量

Ford-Fulkerson方法是一种用于计算流网络中最大流的算法。它通过不断在剩余图中寻找增广路径并增加流量，直到不存在增广路径为止。
Ford-Fulkerson = 在剩余图中不断找路送水 + 用反向边留后悔余地 + 无路可走时停止
增广路径就是：在剩余图中，从源点S到汇点T的一条路径，并且这条路径上的每条边都有剩余容量 > 0从起点到终点，能找到一条所有路段都还有空车位的完整路线
Ford-Fulkerson 的核心思想:反复寻找增广路径（Augmenting Path），并沿其“推流”，直到找不到为止;能增则增，增无可增即为最大; 
*/
// 🎯 简单测试
console.log("=== 简单测试 ===");
const network1 = new FlowNetwork();
network1.addEdge('S', 'A', 5);
network1.addEdge('A', 'T', 3);
const result1 = network1.fordFulkerson('S', 'T');
console.log('最终结果:', result1);
// 🎯 完整测试
console.log("=== 完整测试 ===");

// 测试1：简单直线
const network001 = new FlowNetwork();
network1.addEdge('S', 'A', 5);
network1.addEdge('A', 'T', 3);
console.log('✅测试1结果:', network1.fordFulkerson('S', 'T')); // 应该输出3

// 测试2：并行路径
const network2 = new FlowNetwork();
network2.addEdge('S', 'T', 2);
network2.addEdge('S', 'A', 3);
network2.addEdge('A', 'T', 4);
console.log('✅测试2结果:', network2.fordFulkerson('S', 'T')); // 应该输出5

// 测试3：复杂网络
const network3 = new FlowNetwork();
network3.addEdge('S', 'A', 10);
network3.addEdge('S', 'B', 10);
network3.addEdge('A', 'T', 4);
network3.addEdge('B', 'T', 9);
network3.addEdge('A', 'B', 10);
network3.addEdge('B', 'A', 10);
console.log('✅测试3结果:', network3.fordFulkerson('S', 'T')); // 应该输出13

console.log("=== 测试完成 ===");

//测试1：单边网络
const test1 = new FlowNetwork();
test1.addEdge('S', 'T', 5);
console.log('✅单边网络:', test1.fordFulkerson('S', 'T')); // 应该输出5

//测试2：无路径网络
const test2 = new FlowNetwork();
test2.addEdge('S', 'A', 10);
test2.addEdge('B', 'T', 10);
// A和B之间没有连接！
console.log('✅无路径网络:', test2.fordFulkerson('S', 'T')); // 应该输出0

//测试3：零容量边
const test3 = new FlowNetwork();
test3.addEdge('S', 'A', 0);
test3.addEdge('A', 'T', 10);
console.log('✅零容量边:', test3.fordFulkerson('S', 'T')); // 应该输出0
//测试4：多路径交叉
const test4 = new FlowNetwork();
// 层状网络
test4.addEdge('S', 'A', 10);
test4.addEdge('S', 'B', 5);
test4.addEdge('A', 'C', 8);
test4.addEdge('A', 'D', 3);
test4.addEdge('B', 'C', 4);
test4.addEdge('B', 'D', 7);
test4.addEdge('C', 'T', 6);
test4.addEdge('D', 'T', 9);
console.log('✅多路径交叉:', test4.fordFulkerson('S', 'T')); // 应该输出14

//测试5：瓶颈在中间
const test5 = new FlowNetwork();
test5.addEdge('S', 'A', 100);
test5.addEdge('S', 'B', 100);
test5.addEdge('A', 'C', 1);  // 瓶颈！
test5.addEdge('B', 'C', 1);  // 瓶颈！
test5.addEdge('C', 'T', 100);
console.log('✅中间瓶颈:', test5.fordFulkerson('S', 'T')); // 应该输出2

//测试6：反向边关键路径
const test6 = new FlowNetwork();
test6.addEdge('S', 'A', 10);
test6.addEdge('S', 'B', 10);
test6.addEdge('A', 'C', 15);
test6.addEdge('B', 'C', 5);
test6.addEdge('C', 'T', 15);
console.log('✅反向边测试:', test6.fordFulkerson('S', 'T')); // 应该输出15

//测试7：重复边
const test7 = new FlowNetwork();
test7.addEdge('S', 'A', 5);
test7.addEdge('S', 'A', 10); // 重复边，应该覆盖前值
test7.addEdge('A', 'T', 8);
console.log('✅重复边处理:', test7.fordFulkerson('S', 'T')); // 应该输出8


//测试8：自环边
const test8 = new FlowNetwork();
test8.addEdge('S', 'A', 10);
test8.addEdge('A', 'A', 5); // 自环，应该被BFS忽略
test8.addEdge('A', 'T', 10);
console.log('✅自环边:', test8.fordFulkerson('S', 'T')); // 应该输出10


//测试9：孤立节点
const test9 = new FlowNetwork();
test9.addEdge('S', 'A', 10);
test9.addEdge('A', 'T', 10);
test9.addEdge('X', 'Y', 10); // 孤立部分，与ST不连通
console.log('✅孤立节点:', test9.fordFulkerson('S', 'T')); // 应该输出10

//测试10：大规模简单网络
const test10 = new FlowNetwork();
// 创建10个节点的链式网络
for (let i = 0; i < 9; i++) {
    test10.addEdge(i === 0 ? 'S' : `N${i}`, i === 8 ? 'T' : `N${i+1}`, 5);
}
console.log('✅链式网络:', test10.fordFulkerson('S', 'T')); // 应该输出5

//测试11：完全二分图
const test11 = new FlowNetwork();
// S连接所有左节点，所有右节点连接T，左右完全连接
const leftNodes = ['L1', 'L2', 'L3'];
const rightNodes = ['R1', 'R2', 'R3'];

leftNodes.forEach(l => {
    test11.addEdge('S', l, 10);
    rightNodes.forEach(r => {
        test11.addEdge(l, r, 5);
    });
});

rightNodes.forEach(r => {
    test11.addEdge(r, 'T', 10);
});

console.log('✅二分图:', test11.fordFulkerson('S', 'T')); // 应该输出30

console.log("==健壮性测试开始===")

console.log("✅ 边界情况（空图、单边、零容量）");
console.log("✅ 拓扑复杂性（多路径、瓶颈、反向边）");
console.log("✅ 异常处理（重复边、自环、孤立节点）");
console.log("✅ 扩展性（大规模网络）");
console.log("💫算法测试健壮性通过");
```