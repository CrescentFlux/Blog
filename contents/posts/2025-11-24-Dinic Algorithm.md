# Dinic Algorithm
## 基础知识
- **定义**
```
Dinic算法是解决网络流问题中最大流问题的一种高效算法,发明者Yefim A. Dinitz (1970)
核心创新：结合了分层图和阻塞流的概念，实现了多路增广
与Edmonds-Karp算法相比，Dinic算法通过更智能的路径搜索策略，在理论上和实践中都显著提升了性能
```

## 注意事项

1. **混淆点**
- **核心机制**

|机制	     |    作用	|
---|---
|分层图 (BFS)	|建立搜索约束：数据只能从层级i流向i+1,创建无环的搜索空间	|
|阻塞流 (DFS)|	在当前约束下饱和运输：充分利用当前分层图，批量处理多条路径，减少BFS调用|
|反向边|	允许流量重新路由，找到全局最优解	|
|当前弧优化|	避免重复检查无效边，提升效率	|
|多轮BFS	|适应网络变化，发现新路径|	

2. **代码实现**
```
class DinicWithoutOptimization {
    constructor(n) {
        this.n = n;
        this.graph = new Array(n).fill(0).map(() => []);
        this.level = new Array(n);
        this.visitCount = new Array(n).fill(0);
        this.edgeCheckCount = 0;
    }

    addEdge(from, to, cap) {
        console.log("Creating edge: " + from + " -> " + to + " (capacity: " + cap + ")");
        const forwardEdge = { to: to, cap: cap, rev: null };
        const backwardEdge = { to: from, cap: 0, rev: null };
        forwardEdge.rev = backwardEdge;
        backwardEdge.rev = forwardEdge;
        this.graph[from].push(forwardEdge);
        this.graph[to].push(backwardEdge);
    }
    // 添加一个方法来打印整个图结构
    printGraph() {
        console.log("=== Graph Structure ===");
        for (let i = 0; i < this.n; i++) {
            console.log("Node " + i + " has edges:");
            for (const edge of this.graph[i]) {
                console.log("  -> " + edge.to + " (cap: " + edge.cap + ")");
            }
        }
        console.log("======================");
    }
    bfs(s, t) {
        this.level.fill(-1);
        const queue = [s];
        this.level[s] = 0;
        
        while (queue.length > 0) {
            const u = queue.shift();
            for (const edge of this.graph[u]) {
                if (edge.cap > 0 && this.level[edge.to] === -1) {
                    this.level[edge.to] = this.level[u] + 1;
                    queue.push(edge.to);
                }
            }
        }
        return this.level[t] !== -1;
    }

    dfs(u, t, f) {
        this.visitCount[u]++;
        
        if (u === t) return f;
        
        let pushed = 0;
        
        console.log("Node " + u + " visit " + this.visitCount[u] + ", check " + this.graph[u].length + " edges");
        
        for (let i = 0; i < this.graph[u].length; i++) {//😵每次都从0开始检查所有边
            const edge = this.graph[u][i];
            this.edgeCheckCount++; // 计数
            if (this.level[edge.to] === this.level[u] + 1 && edge.cap > 0) {
                console.log("  Check edge " + u + "->" + edge.to + ", cap " + edge.cap);
                
                const flow = this.dfs(edge.to, t, Math.min(f - pushed, edge.cap));
                
                if (flow > 0) {
                    console.log("  Success from " + u + "->" + edge.to + " push " + flow);
                    edge.cap -= flow;
                    edge.rev.cap += flow;
                    pushed += flow;
                    
                    if (pushed === f) return pushed;
                }
            }
        }
        
        return pushed;
    }

    maxFlow(s, t) {
        let totalFlow = 0;
        this.visitCount.fill(0);
        this.edgeCheckCount = 0; // 重置计数器
        while (this.bfs(s, t)) {
            console.log('=== New BFS Level ===');
            
            let flow;
            let dfsCallCount = 0;
            
            while ((flow = this.dfs(s, t, Infinity)) > 0) {
                dfsCallCount++;
                totalFlow += flow;
                console.log("*** DFS call " + dfsCallCount + ": push " + flow + ", total " + totalFlow);
            }
            
            console.log("=== Node Visit Stats ===");
            for (let i = 0; i < this.n; i++) {
                if (this.visitCount[i] > 0) {
                    console.log("  Node " + i + ": visited " + this.visitCount[i] + " times");
                }
            }
        }
        
        return totalFlow;
    }
}
// Clean test function
function cleanTest() {
    const dinic = new DinicWithoutOptimization(4);
    
    dinic.addEdge(0, 1, 10);
    dinic.addEdge(0, 2, 5);
    dinic.addEdge(1, 3, 8);
    dinic.addEdge(2, 3, 7);
    // 打印完整的图结构
    dinic.printGraph();
    console.log('=== Clean Test ===');

    const result = dinic.maxFlow(0, 3);
    console.log('Final max flow:', result);
}
//节点0被访问了2次，每次都检查所有2条边，但第二次访问时：0->1 容量只剩2，而且走不通0->2 容量为0第二次访问完全是浪费！
// Run test
cleanTest();
// 创建一个有很多"死胡同"边的网络
function testWithoutOptimization() {
    const dinic = new DinicWithoutOptimization(6);
    
    // 有效路径
    dinic.addEdge(0, 1, 10); // S->A
    dinic.addEdge(1, 5, 10); // A->T
    
    // 很多容量为0的"死胡同"边
    dinic.addEdge(0, 2, 0);  // S->B (死胡同)
    dinic.addEdge(0, 3, 0);  // S->C (死胡同)  
    dinic.addEdge(0, 4, 0);  // S->D (死胡同)
    dinic.addEdge(1, 2, 0);  // A->B (死胡同)
    dinic.addEdge(1, 3, 0);  // A->C (死胡同)
    // 打印完整的图结构
    dinic.printGraph();
   
    console.log('=== 测试没有当前弧优化的版本 ===');
    const result = dinic.maxFlow(0, 5);
    console.log('最终最大流:', result);
}
testWithoutOptimization();

//有多条路径，但有些路径会先被用满的网络
function testRealProblem() {
    const dinic = new DinicWithoutOptimization(5); // 节点: 0,1,2,3,4
    dinic.addEdge(0, 1, 100); // S->A (主要)
    dinic.addEdge(1, 4, 100); // A->T
    dinic.addEdge(0, 2, 10);  // S->B (次要)
    dinic.addEdge(2, 1, 5);   // B->A (瓶颈，先满)
    // 死胡同边
    dinic.addEdge(0, 3, 0);   // S->C (死胡同)
    // 打印完整的图结构
    dinic.printGraph();
    console.log('=== 能展示问题的测试 ===');
    const result = dinic.maxFlow(0, 4);
    //第二次DFS不是bug，而是算法确保找到最大流的必要步骤
    console.log('最终最大流:', result);
}
testRealProblem();
//🛠️节点重复访问是正常的（算法需要尝试多条路径） 边重复检查是浪费的（已知无效的边不应该重复检查）
class DinicWithEdgeCheckCount {
  constructor(n) {
    this.n = n; // 节点数
    // 邻接表：graph[i] 存储从节点i出发的所有边
    this.graph = new Array(n).fill(0).map(() => []); // 邻接表
    this.level = new Array(n); // 层级
    this.ptr = new Array(n); // 当前弧优化指针// 当前弧优化数组
    this.edgeCheckCount = 0; // 统计边检查次数
  }

//边的数据结构
addEdge(from, to, cap) {
    // 添加边界检查
        if (from >= this.n || to >= this.n) {
            throw new Error(`节点编号超出范围: ${from}->${to}`);
        }
    // 我们用一个对象来表示一条边
    const forwardEdge = {
      to: to,          // 边的终点
      cap: cap,        // 剩余容量
      rev: null        // 反向边的引用，稍后设置
    };
    const backwardEdge = {
      to: from,        // 反向边指向原起点
      cap: 0,          // 初始容量为0
      rev: null        // 指向原边
    };
    // 互相设置反向边引用
    forwardEdge.rev = backwardEdge;
    backwardEdge.rev = forwardEdge;
    // 添加到邻接表中
    this.graph[from].push(forwardEdge);   // 正向边
    this.graph[to].push(backwardEdge);    // 反向边
}
     // 打印图结构（用于调试）
    printGraph(){
        for (let i = 0; i < this.n; i++) {
        console.log(`节点 ${i}:`);
        this.graph[i].forEach(edge => {
            console.log(`  -> ${edge.to} (容量: ${edge.cap})`);
        });
        }
    }
  
//BFS构建分层图
bfs(s, t) {
    // 初始化层级为-1（未访问）
    this.level.fill(-1);
    const queue = [s];
    this.level[s] = 0;  // 源点层级为0
    while (queue.length > 0) {
      const u = queue.shift();  // 取出队首节点
      //遍历u的所有出边
      for (const edge of this.graph[u]) {
        // 如果边的容量>0 且 目标节点未访问
        if (edge.cap > 0 && this.level[edge.to] === -1) {
        //🤯这个逻辑已经考虑了所有容量>0的边，包括反向边！
          this.level[edge.to] = this.level[u] + 1;  // 设置层级
          /* 这是经典的"图遍历+状态记录"模式:当前状态+1"的模式在很多算法中出现:动态规划,树的深度计算,层级遍历
          */
          queue.push(edge.to);  // 加入队列
        }
      }
    }
    //如果汇点可达，返回true；否则返回false
    return this.level[t] !== -1;
}
     // 打印层级信息
    printLevels() {
        console.log("节点层级:");
        for (let i = 0; i < this.n; i++) {
        console.log(`  节点 ${i}: 层级 ${this.level[i]}`);
        }
    }
// DFS寻找阻塞流
dfs(u, t, f,path = []) {
    //DFS的目标：在分层图框架下，从当前节点u出发，找一条到汇点t的路径，并推送流量
    // u: 当前节点;t: 汇点;f: 当前可用的流量;返回值: 实际推送的流量
    // 创建新的路径数组，避免引用问题
    const currentPath = [...path, u];

    if (u === t){
        console.log(`🏁 找到路径: ${currentPath.join('->')}, 推送流量 ${f}`);    
        return f;  // 到达汇点，返回可用流量
    } 
            
        let pushed = 0;  // 记录从这个节点推送的总流量
  
        for (let i = this.ptr[u]; i < this.graph[u].length; i++) {//🤯使用ptr[u]而不是从0开始
            const edge = this.graph[u][i];  //获取边对象,这行要放在循环里面！
//this.graph[u] 是节点u的所有出边数组,this.graph[u][i] 获取第i条边,const edge = this.graph[u][i] 把这条边保存到edge变量中
            this.edgeCheckCount++; // 每次检查边就计数！
           // 条件1：目标节点层级 = 当前节点层级 + 1 这确保了数据只能往更高层级流动，不会绕远路或形成循环
           // 条件2：边还有剩余容量
            if (this.level[edge.to] === this.level[u] + 1 && edge.cap > 0) {
                console.log(`  🔍 尝试 ${u}->${edge.to}, 剩余容量 ${edge.cap}`);
                /*
                尝试从edge.to走到汇点t 
                流量控制的核心:取最小值，确保不超过任何限制
                Math.min(f - pushed, edge.cap) 计算实际能推送的流量f - pushed：当前还剩下多少流量可以推送
                edge.cap：这条边还能承载多少流量
                递归DFS调用
                */
                const flow = this.dfs(edge.to, t, Math.min(f - pushed, edge.cap));
                //请从edge.to这个节点开始，尝试往汇点t推送这么多流量，告诉我实际能推多少
                if (flow > 0) {
                    console.log(`  👉成功从 ${u}->${edge.to} 推送 ${flow} 流量`);
                    // 更新边的容量：正向边减少，反向边增加
                    edge.cap -= flow;//减少正向边的剩余容量
                    edge.rev.cap += flow;//增加反向边的容量，允许流量重新路由
                    pushed += flow;// 累计从这个节点推送的总流量

                    //💡当前弧优化：只有成功推送且用完流量时才更新指针
                        if (pushed === f) {
                            this.ptr[u] = i; // 成功推送，记录当前位置
                            return pushed;
                        }
                }
            }
            //💡当前弧优化：这条边不可用，移动到下一条
                 this.ptr[u] = i + 1;
        }
        // 如果循环结束但pushed还是0，说明这个节点所有出路都失败了
        if (pushed === 0) {
        console.log(`  ⚠️ 节点 ${u} 无路可走`);
    }
    return pushed;

  }
   
// 计算最大流
maxFlow(s, t) {
    let totalFlow = 0;
        
        // 只要BFS能找到分层图，就继续
        while (this.bfs(s, t)) {//构建分层图，判断是否还有增广路径,每次找到阻塞流后，网络状态改变，可能出现新的需要走反向边的路径
            //💡重置当前弧指针
            this.ptr.fill(0);// 每轮BFS后重置指针！,每轮BFS构建了全新的分层图// 新的地图版本重置所有书签
            //防御性编程:ptr记录的是在当前分层图内的检查进度,同一张地图内：复用ptr，避免重复检查,换新地图时：重置ptr，重新探索
            this.edgeCheckCount = 0; // 重置计数器
            // 内层循环：在当前分层图中找所有阻塞流
            // 不断调用DFS，直到找不到增广路径
            let flow;
            while ((flow = this.dfs(s, t, Infinity)) > 0) {
                //在当前分层图中找到所有可能的增广路径,dfs(s, t, Infinity)从源点s开始，尽可能多地往汇点t推送流量
                totalFlow += flow;
            }
        }
        
        return totalFlow;
    }
  }
  
function compareOptimization() {
    console.log('=== 对比测试：有优化 vs 无优化 ===');
    
    // 测试网络
     const network = [
        [0, 1, 10],
        [0, 2, 5], 
        [1, 3, 8],
        [2, 3, 7]
    ];
    
    // 有优化的版本
    const dinicWith = new DinicWithEdgeCheckCount(4);
    network.forEach(([from, to, cap]) => dinicWith.addEdge(from, to, cap));
    const resultWith = dinicWith.maxFlow(0, 3);
    
    // 无优化的版本
    const dinicWithout = new DinicWithoutOptimization(4);
    network.forEach(([from, to, cap]) => dinicWithout.addEdge(from, to, cap));
    const resultWithout = dinicWithout.maxFlow(0, 3);

    console.log('有优化 - 最大流:', resultWith, '边检查次数:', dinicWith.edgeCheckCount);
    console.log('无优化 - 最大流:', resultWithout, '边检查次数:', dinicWithout.edgeCheckCount);
    console.log('优化效果:', dinicWithout.edgeCheckCount - dinicWith.edgeCheckCount, '次边检查');
 
 
}

// 运行测试
compareOptimization();
// 优化效率计算函数
function calculateOptimizationEfficiency() {
    console.log('=== 优化效率计算 ===');
    
    const network = [
        [0, 1, 10],
        [0, 2, 5], 
        [1, 3, 8],
        [2, 3, 7]
    ];
    
    // 有优化版本
    const dinicWith = new DinicWithEdgeCheckCount(4);
    network.forEach(([from, to, cap]) => dinicWith.addEdge(from, to, cap));
    const resultWith = dinicWith.maxFlow(0, 3);
    
    // 无优化版本  
    const dinicWithout = new DinicWithoutOptimization(4);
    network.forEach(([from, to, cap]) => dinicWithout.addEdge(from, to, cap));
    const resultWithout = dinicWithout.maxFlow(0, 3);
    
    const savedChecks = dinicWithout.edgeCheckCount - dinicWith.edgeCheckCount;
    const optimizationRate = (savedChecks / dinicWithout.edgeCheckCount * 100).toFixed(1);
    
    console.log('无优化边检查次数:', dinicWithout.edgeCheckCount);
    console.log('有优化边检查次数:', dinicWith.edgeCheckCount);
    console.log('节省的边检查次数:', savedChecks);
    console.log('💫优化效率:', optimizationRate + '%');
    
    return optimizationRate;
}

// 运行计算
const efficiency = calculateOptimizationEfficiency();
console.log('💫当前弧优化效率为', efficiency + '%');

// 测试1：创建一个简单网络
const dinic = new DinicWithEdgeCheckCount(4); // 4个节点：0,1,2,3

// 构建这个网络：
// 0 -> 1 (容量10)
// 0 -> 2 (容量5)  
// 1 -> 3 (容量8)
// 2 -> 3 (容量7)
dinic.addEdge(0, 1, 10);
dinic.addEdge(0, 2, 5);
dinic.addEdge(1, 3, 8);
dinic.addEdge(2, 3, 7);
// 查看图结构
dinic.printGraph();
// 从节点0到节点3进行BFS分层
const reachable = dinic.bfs(0, 3);
console.log("汇点是否可达:", reachable);
dinic.printLevels();
console.log("计算最大流...");
const maxFlow = dinic.maxFlow(0, 3);
console.log("✅最大流:", maxFlow);  // 应该输出13

//========🔄二分图匹配函数  二分图匹配 = 特殊网络的最大流问题=======//
function bipartiteMatching(leftSize, rightSize, edges) {
    // 步骤1: 计算总节点数
    const totalNodes = leftSize + rightSize + 2;//左边节点 + 右边节点 + 源点 + 汇点 
    const dinic = new DinicWithEdgeCheckCount(totalNodes);
    
    const s = 0;// 源点(Source)编号
    const t = totalNodes - 1;// 汇点(Target)编号
    console.log("=== 构建网络 ===");
    console.log(`总节点: ${totalNodes}, 源点: ${s}, 汇点: ${t}`);
    // 步骤2: 源点连接到所有左边节点
    console.log("\n1. 源点 -> 左边节点:");
    for (let i = 1; i <= leftSize; i++) {
        dinic.addEdge(s, i, 1);//容量是可以改变的,这取决于想要解决的具体问题
        console.log(`   边 ${s}->${i} (S->${String.fromCharCode(64 + i)}) 容量1`);
    }
    // 步骤3: 所有右边节点连接到汇点
    for (let i = 1; i <= rightSize; i++) {
        dinic.addEdge(leftSize + i, t, 1);
        console.log(`   边 ${leftSize + i}->${t} (${String.fromCharCode(87 + i)}->T) 容量1`);
    }
    //  步骤4:添加匹配边
    for (const [leftIdx, rightIdx] of edges) {
        const from = leftIdx + 1;// 左边节点编号
        const to = leftSize + rightIdx + 1;// 右边节点编号
        dinic.addEdge(from, to, 1);// 容量为1
        console.log(` 匹配边关系为 ${from}->${to} 容量1`);
    }
    // 步骤5: 计算最大流 = 最大匹配数
    console.log("\n=== 开始计算最大匹配 ===");
    const maxPairs = dinic.maxFlow(s, t);
    return maxPairs;
}
// 简化测试版本
function testSimple() {
    console.log("=== 简化测试 ===");
    const leftSize = 3;
    const rightSize = 3;
    const edges = [
        [0, 0], [0, 1],  // 左边0->右边0, 左边0->右边1
        [1, 0], [1, 2],  // 左边1->右边0, 左边1->右边2
        [2, 1]           // 左边2->右边1
    ];
    
    const result = bipartiteMatching(leftSize, rightSize, edges);
    console.log(`🎯 最大匹配数: ${result}`);
}
// 运行测试
testSimple();
/*
👉Edmonds-Karp算法:每次BFS都是全新的全局搜索
每次推送流量后，边的剩余容量变了，甚至边的方向都反了（产生了反向边），之前可用的路径可能现在不可用了，之前不存在的路径（通过反向边）可能现在出现了。它必须重新进行全局搜索
Edmonds-Karp 它会盲目地探索所有最短路径，包括很多死胡同每次只推送一条路，而且每次推送后都要重新执行全局BFS
每次BFS都在重复探索整个网络，包括那些已经被证明无效的路径
👉Dinic算法:分阶段进行高效复用
先一次全局BFS构建分层图，然后在该图内进行多次局部的DFS。只有当一层耗尽后，才进行下一次全局BFS。
[1]1.分层图：一次BFS服务多次增广;2.当前弧优化：在同一次分层中，避免重复探索无效边
[2]极大地减少了耗时的全局BFS的次数，将主要计算工作量放在了更高效的、基于局部信息的DFS上
[3]一种通过反向边实现的“抵消机制”:利用反向边重新规划，进行一次精妙的流量调度，最终达到了理论上的最大流量;思想:分批次、最大化利用每一层
👉分批次进行DFS”指的是:
一个批次 = 一次构建的分层图 + 在该分层图上进行的所有DFS
在同一个批次内，算法会进行多次DFS来寻找增广路径。这些DFS共享同一个分层图，避免了重复执行昂贵的BFS
每次DFS可能会因为“当前弧优化”而避免重复探索无效的边，从而在同一次分层图内也非常高效
只有当这个批次再也找不到任何路径（找到阻塞流）时，算法才会开启下一个批次：执行一次新的BFS来构建新的分层图
👉核心优势
减少了最昂贵的操作：BFS（全局规划）是昂贵的，因为它需要遍历大量节点。DFS（局部探索）相对廉价
Dinic 用一次BFS的成本，换来了多次DFS的收益
Edmonds-Karp 则是每次增广（送一次货）都要付出一次BFS 的成本
👉BFS规则:在残量网络中，BFS会探索任何容量>0的边，无论它是正向还是反向

分层图:分层图不是简单地把节点分组，而是建立了一个有方向的、无环的“高速公路网络”，在这个网络中，你只能从低层开往高层，绝对不能回头或绕远路
第一步:进行一次BFS，测量每个节点到S的最短距离;现在建立规则：数据包只能从层级i流向层级i+1，绝对不能流向同层级或低层级
层级0: S
层级1: A, B, C      (距离S 1跳)
层级2: D, E, F      (距离S 2跳)  
层级3: G, H, I      (距离S 3跳)
层级4: T            (距离S 4跳)
第二步:在高速公路上批量运输
现在的网络实际上变成了：S(0) -> A,B,C(1) -> D,E,F(2) -> G,H,I(3) -> T(4)
DFS的批量优势体现:局部性,无环保证(只能向高层级走，绝对不会有循环或绕远路),批量处理(在同一分层图内，可以找到多条路径，而不需要重新规划)
从S出发，发现可以同时向A、B、C发送数据;在DFS过程中可以记住每个节点的状态，避免重复探索死胡同可以在同一次分层图的生命周期内，找到多条路径并并行处理
本质是：通过施加只能前进不能后退的约束，将复杂的网络搜索问题分解为一系列简单的、局部的决策问题
分层图的价值在于它约束了搜索空间，而不是分割了工作流程
Dinic的核心优势在于：在同一个分层图的生命周期内，它对每个节点的出口边进行系统性的、无重复的探索。
不是"确保A探索完才探索B"而是"在探索A时，就一次性找出A的所有可能路径，不需要以后重新探索A
通过当前弧优化记录每个节点的探索进度，避免重复检查已经失效的边
*/
class EdmondsKarp {
    constructor(n) {
        this.n = n;
        this.graph = new Array(n).fill(0).map(() => []);
        this.edgeCheckCount = 0;
    }
    addEdge(from, to, cap) {
        const forwardEdge = { to: to, cap: cap, rev: null };
        const backwardEdge = { to: from, cap: 0, rev: null };
        forwardEdge.rev = backwardEdge;
        backwardEdge.rev = forwardEdge;
        this.graph[from].push(forwardEdge);
        this.graph[to].push(backwardEdge);
    }
    bfs(s, t, parent) {
        const visited = new Array(this.n).fill(false);
        const queue = [s];
        visited[s] = true;
        parent[s] = -1;

        while (queue.length > 0) {
            const u = queue.shift();
            for (const edge of this.graph[u]) {
                this.edgeCheckCount++;
                if (!visited[edge.to] && edge.cap > 0) {
                    visited[edge.to] = true;
                    parent[edge.to] = u;
                    queue.push(edge.to);
                    if (edge.to === t) return true;
                }
            }
        }
        return false;
    }
    maxFlow(s, t) {
        let totalFlow = 0;
        this.edgeCheckCount = 0;
        const parent = new Array(this.n);

        while (this.bfs(s, t, parent)) {
            // 找到增广路径的瓶颈容量
            let pathFlow = Infinity;
            for (let v = t; v !== s; v = parent[v]) {
                const u = parent[v];
                const edge = this.graph[u].find(e => e.to === v);
                pathFlow = Math.min(pathFlow, edge.cap);
            }
            // 更新残量网络
            for (let v = t; v !== s; v = parent[v]) {
                const u = parent[v];
                const edge = this.graph[u].find(e => e.to === v);
                edge.cap -= pathFlow;
                edge.rev.cap += pathFlow;
            }

            totalFlow += pathFlow;
        }
        return totalFlow;
    }
}

function robustnessTest() {
    console.log("=== 算法对比测试 ===");
    
    const testCases = [
        {
            name: "简单网络",
            network: [[0,1,10], [0,2,5], [1,3,8], [2,3,7]],
            nodes: 4,
            expected: 13
        },
        {
            name: "完全图", 
            network: [[0,1,5], [0,2,5], [1,2,3], [1,3,4], [2,3,6]],
            nodes: 4,
            expected: 10
        },
        {
            name: "多路径网络",
            network: [[0,1,3], [0,2,3], [1,2,2], [1,3,2], [2,3,3]],
            nodes: 4, 
            expected: 5
        },
        {
            name: "瓶颈网络",
            network: [[0,1,100], [0,2,100], [1,3,50], [2,3,50], [3,4,200]],
            nodes: 5,
            expected: 100
        }
    ];

    testCases.forEach((testCase, index) => {
        console.log(`\n📊 测试 ${index + 1}: ${testCase.name}`);
        
        // 测试Dinic算法
        const dinic = new DinicWithEdgeCheckCount(testCase.nodes);
        testCase.network.forEach(([from, to, cap]) => dinic.addEdge(from, to, cap));
        const dinicResult = dinic.maxFlow(0, testCase.nodes-1);
        
        // 测试Edmonds-Karp算法
        const ek = new EdmondsKarp(testCase.nodes);
        testCase.network.forEach(([from, to, cap]) => ek.addEdge(from, to, cap));
        const ekResult = ek.maxFlow(0, testCase.nodes-1);
        
        console.log(`🌟Dinic:  结果=${dinicResult}, 边检查=${dinic.edgeCheckCount}`);
        console.log(`🌟E-Karp: 结果=${ekResult}, 边检查=${ek.edgeCheckCount}`);
        console.log(`🌟预期结果: ${testCase.expected}`);
        console.log(`🌟Dinic正确: ${dinicResult === testCase.expected}`);
        console.log(`🌟E-Karp正确: ${ekResult === testCase.expected}`);
        console.log(`🌟效率比: ${(ek.edgeCheckCount/dinic.edgeCheckCount).toFixed(2)}x,`);
        console.log(`   🚀 Dinic算法的效率是E-Karp的${(ek.edgeCheckCount/dinic.edgeCheckCount).toFixed(2)} 倍`);
    });
}
robustnessTest();
function testBoundaryCases() {
    console.log("=== Dinic算法边界情况测试 ===");
    
    const testCases = [
        {
            name: "空网络",
            network: [],
            nodes: 2,
            description: "只有源点和汇点，没有边"
        },
        {
            name: "单边网络", 
            network: [[0,1,5]],
            nodes: 2,
            description: "只有一条边"
        },
        {
            name: "无法到达汇点",
            network: [[0,1,10], [2,3,10]],
            nodes: 4,
            description: "源点和汇点不连通"
        },
        {
            name: "超大容量",
            network: [[0,1,1e9], [1,2,1e9]],
            nodes: 3,
            description: "处理极大容量值"
        },
        {
            name: "自环边",
            network: [[0,0,10], [0,1,5]],
            nodes: 2,
            description: "包含自环边"
        },
        {
            name: "完全二分图",
            network: (() => {
                const edges = [];
                for (let i = 0; i < 3; i++) {
                    for (let j = 0; j < 3; j++) {
                        edges.push([i, j + 3, 1]);
                    }
                }
                return edges;
            })(),
            nodes: 7, // 3左 + 3右 + S + T
            description: "完全连接的二分图"
        }
    ];

    testCases.forEach((testCase, index) => {
        console.log(`\n🔬 测试 ${index + 1}: ${testCase.name}`);
        console.log(`   描述: ${testCase.description}`);
        
        try {
            const dinic = new DinicWithEdgeCheckCount(testCase.nodes);
            testCase.network.forEach(([from, to, cap]) => {
                dinic.addEdge(from, to, cap);
            });
            
            const result = dinic.maxFlow(0, testCase.nodes-1);
            console.log(`   ✅ 执行成功 - 最大流: ${result}`);
            console.log(`   📊 边检查次数: ${dinic.edgeCheckCount}`);
            
        } catch (error) {
            console.log(`   ❌ 执行失败 - 错误: ${error.message}`);
        }
    });
}
testBoundaryCases();
```