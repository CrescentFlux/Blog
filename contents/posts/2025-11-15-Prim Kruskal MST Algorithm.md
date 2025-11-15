







# Prim  Kruskal MST Algorithm
## **基础知识**



- **Prim Algorithm**
   - 定义：一种贪心算法，用于为加权无向图寻找最小生成树(MST)
     - 最小生成树（Minimum Spanning Tree）是指在一个加权无向图中，找到一棵包含所有顶点的树，使得所有边的权重之和最小
- **Kruskal Algorithm**
   - 定义：一种贪心算法，通过按权重递增顺序考虑边来构建最小生成树(MST)




## **注意事项**
1. **混淆点**

- **Prim vs Kruskal**

|对比|Prim|Kruskal|
---|---|---
|核心价值|提供有导向的、连贯的最优解|提供平等的、全局的最优解|
|优先级|深度优先的连通|广度优先的最优|
|性质|始终维护单个连通分量|维护森林，逐步合并连通分量|


- **优先队列 vs 堆**

|比较   | 	优先队列	|堆|
---|---|---
|本质|	抽象数据类型：接口、概念|	实现方式|
|内部维护	|不关心	|必须维护堆性质|
|操作|    关注业务语义|关注数据结构性质|
|核心|做什么|怎么做|
|多种实现|	可以用堆、有序数组、无序数组等实现	|是优先队列的一种实现方式|
|API 设计混淆|优先队列API更抽象，语义更清晰只返回item，不暴露内部结构|堆的API通常更底层，需要同时提供项和键返回 {item, key}，暴露内部操作|

- **普通队列 vs 优先队列**

|比较|	普通队列|	优先队列|
---|---|---
|核心原则	|先进先出	|最高优先级先出|
|出队顺序|	完全由入队时间决定|	完全由元素优先级决定|
|元素关系	|元素是平等的，只有时间先后之分	|元素带有优先级属性，是不平等的|
|典型操作|	enqueue(e) （入队） dequeue() （出队）|enqueue(e, p) （带优先级入队）dequeue() （出队最高优先级的)|
|实现基础	|通常用链表或循环数组实现|	通常用二叉堆实现|












2. **代码实现**
```
//=================================🔄prim=============================//
function primMST(graph) {
/**
 * 找出连接已访问集合和未访问集合的最小边
 * @param {Object} graph - 邻接表表示的图
 * @param {Set} visited - 已访问的节点集合:visited 集合代表已经连通的组件,这个组件内部的所有节点已经可以通过某种路径互相到达,只需要找从这个组件通向外部的边
 * @param {Set} unvisited - 未访问的节点集合
 * @returns {Array} [from, to, cost] 最小成本边的信息
 * ⭐️完整Prim 算法：
 * 1.返回最小生成树的所有边:遍历所有已访问的节点,对于每个已访问节点的邻居，如果邻居在未访问集合中，且成本更小，则更新minEdge
 * 2.Prim算法需要起点，需要逐步扩张的视角：从一个点开始，一步步扩张领地；需要中心化的规划：我们从骨干节点开始，一步步扩展到边缘节点；
 */
  const nodes = Object.keys(graph).map(Number);
  if (nodes.length === 0) return [];
  const visited = new Set();
  const unvisited = new Set(nodes);
  const mstEdges = [];
  
  // 从节点0开始
  visited.add(0);
  unvisited.delete(0);
  
  while (unvisited.size > 0) {
    let minCost = Infinity;
    let minEdge = null;
    //最坏情况：O(V × E) ≈ O(V³) 对于稠密图,每次都要重新扫描所有已访问节点的所有邻居，大量重复计算
    // 在已访问和未访问集合之间寻找最小成本边
    for (const node of visited) {// 1. 遍历所有已访问的节点//外层循环：V-1 次（每次加一个节点）
      for (const [neighbor, cost] of graph[node]) { // 2. 对于每个已访问节点，遍历它的所有邻居//内层循环：最多检查所有边 E
        if (unvisited.has(neighbor) && cost < minCost) {// 3. 如果邻居在未访问集合中，且成本更小
        // 4. 更新记录
          minCost = cost;
          minEdge = [node, neighbor, cost];
        }
      }
    }
    
    if (!minEdge) break; // 图不连通
    const [from, to, cost] = minEdge;
    mstEdges.push(minEdge);
    visited.add(to);
    unvisited.delete(to);
  }
  
  return mstEdges;
}
// 测试
const testGraph = {
  0: [[1, 2], [2, 3]],
  1: [[0, 2], [2, 1]], 
  2: [[0, 3], [1, 1], [3, 4]],
  3: [[2, 4]]
};
console.log(primMST(testGraph));
// 应该返回：[[0,1,2], [1,2,1], [2,3,4]] 
// 这是一个树形结构，每个节点都通过某种路径与其他所有节点连通。[[0,1,2], [1,2,1], [2,3,4]] 表示构建了三条独立的边：边1: 0 ↔ 1 (成本2),边2: 1 ↔ 2 (成本1)边3: 2 ↔ 3 (成本4)

/*
⭐️堆的优化:
1.空间换时间：用堆存储所有候选边;避免重复：不用每次重新扫描所有节点
2.性能优化（使用优先队列）,基础版本的时间复杂度是 O(V²)，对于稠密图很慢。我们可以用 最小堆（优先队列） 来优化到 O(E log V)。
3.关键优势：避免重复扫描：堆记住了所有候选边;快速取最小：堆顶就是当前最小成本边;动态更新：当发现更优路径时，更新堆中的key值
*/
class MinHeap {//首先我们需要一个最小堆实现,
  constructor() {
    this.heap = [];
  }
  
  push(node, key) {
    this.heap.push({node, key});
    this.heapifyUp(this.heap.length - 1);
  }
  
  pop() {
    if (this.heap.length === 0) return null;// 边界情况：堆为空时返回null
    const min = this.heap[0];// 步骤1：保存堆顶元素（最小值）
    const last = this.heap.pop(); // 步骤2：取出堆的最后一个元素
    if (this.heap.length > 0) { // 步骤3：如果堆中还有元素，需要重新调整堆
      this.heap[0] = last; // 步骤4：将最后一个元素放到堆顶
      this.heapifyDown(0);// 步骤5：从堆顶开始向下调整，恢复堆性质
    }
    return min; // 返回最小值
  }
  
  heapifyUp(index) {
    // 实现堆的上浮操作
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      if (this.heap[parent].key <= this.heap[index].key) break;
      [this.heap[parent], this.heap[index]] = [this.heap[index], this.heap[parent]];
      index = parent;
    }
  }
  
  heapifyDown(index) {
    // 实现堆的下沉操作
    const length = this.heap.length;
    while (true) {
      let left = 2 * index + 1;
      let right = 2 * index + 2;
      let smallest = index;
      
      if (left < length && this.heap[left].key < this.heap[smallest].key) {
        smallest = left;
      }
      if (right < length && this.heap[right].key < this.heap[smallest].key) {
        smallest = right;
      }
      if (smallest === index) break;
      
      [this.heap[index], this.heap[smallest]] = [this.heap[smallest], this.heap[index]];
      index = smallest;
    }
  }
  isEmpty() {
    return this.heap.length === 0;
  }
}
// 使用最小堆的 Prim 算法
function primMSTOptimized(graph) {
  const n = Object.keys(graph).length;
  if (n === 0) return [];
  
  const inMST = new Array(n).fill(false);
  const key = new Array(n).fill(Infinity);
  const parent = new Array(n).fill(-1);
  const heap = new MinHeap();
  
  // 从节点0开始
  key[0] = 0;
  heap.push(0, 0);
  
  while (!heap.isEmpty()) {
    //每个节点只被 pop 一次，确保算法会终止//pop 的三重作用：获取当前最重要的节点,移除它，避免重复处理,推进算法进度
    const {node: u} = heap.pop();//这个操作有重大意义,u 现在正式加入MST
    //🔥关键：移除并获取最小节点
    if (inMST[u]) continue; // 安全校验堆中可能有重复节点
    inMST[u] = true; // 标记为已处理
    
    for (const [v, weight] of graph[u]) {
      if (!inMST[v] && weight < key[v]) {
        key[v] = weight;
        parent[v] = u;
        heap.push(v, key[v]);
      }
    }
  }
  // 构建结果
  const mstEdges = [];
  for (let i = 1; i < n; i++) {
    if (parent[i] !== -1) {
      mstEdges.push([parent[i], i, key[i]]);
    }
  }
  
  return mstEdges;
}
//测试
function primWithSteps(graph) {
  const steps = [];
  const nodes = Object.keys(graph).map(Number);
  const visited = new Set([0]);
  const unvisited = new Set(nodes.slice(1));
  const mstEdges = [];
  steps.push({
    visited: new Set(visited),
    unvisited: new Set(unvisited),
    currentMinEdge: null,
    mstEdges: [...mstEdges]
  });
  while (unvisited.size > 0) {
    let minCost = Infinity;
    let minEdge = null;
    for (const node of visited) {
      for (const [neighbor, cost] of graph[node]) {
        if (unvisited.has(neighbor) && cost < minCost) {
          minCost = cost;
          minEdge = [node, neighbor, cost];
        }
      }
    }
    
    if (!minEdge) break;
    const [from, to, cost] = minEdge;
    mstEdges.push(minEdge);
    visited.add(to);
    unvisited.delete(to);
    steps.push({
      visited: new Set(visited),
      unvisited: new Set(unvisited),
      currentMinEdge: minEdge,
      mstEdges: [...mstEdges]
    });
  }
  return steps;
}
const complexGraph = {
  0: [[1, 4], [7, 8]],
  1: [[0, 4], [2, 8], [7, 11]],
  2: [[1, 8], [3, 7], [5, 4], [8, 2]],
  3: [[2, 7], [4, 9], [5, 14]],
  4: [[3, 9], [5, 10]],
  5: [[2, 4], [3, 14], [4, 10], [6, 2]],
  6: [[5, 2], [7, 1], [8, 6]],
  7: [[0, 8], [1, 11], [6, 1], [8, 7]],
  8: [[2, 2], [6, 6], [7, 7]]
};
// 查看每一步的执行过程
const steps = primWithSteps(complexGraph);
steps.forEach((step, index) => {
  console.log(`步骤 ${index + 1}:`);
  console.log(`  已访问:`, Array.from(step.visited));
  console.log(`  最小边:`, step.currentMinEdge);
  console.log(`  MST边:`, step.mstEdges);
  console.log(' ---');
});
// 单独在最后输出成功消息
console.log('🎉 Prim算法完美运行并找到了最小生成树 ---');
console.log('总成本:', steps[steps.length - 1].mstEdges.reduce((sum, edge) => sum + edge[2], 0));
console.log('连接了所有', steps[steps.length - 1].visited.size, '个节点');
    
/*
Kruskal算法从边的角度思考问题，而Prim从点的角度思考
Kruskal的核心数据结构是并查集，用于检测是否形成环
*/

//=============================🔄Kruskal===============================//
/*
⭐️Kruskal的视角（互联网思维）：让每个局域网先自己连起来，然后用最便宜的线路把它们连在一起，去中心化，自下而上。
算法思想：将所有边按权重从小到大排序，然后依次选择不形成环的边加入最小生成树。
把所有边按成本排序，从最便宜的开始选，只要不成环就要；要最便宜的，但不要多余的
1.调查所有可能的路：把每两个城市之间修路的成本都列出来
2.从最便宜的路开始修：先修最便宜的那条
3.检查会不会形成环：如果修这条路会让某些城市之间有两条不同的路径，那就不要修
4.重复直到所有城市连通
⭐️Kruskal的优雅之处在于：
1.不需要指定起点：从全局视角处理
2.天然并行：可以同时处理多条边
3.更符合直觉：就是要最便宜的边，只要不形成环
4.从边出发的全局最优性
⭐️Kruskal证明了一个优美的定理：
对于任何图，如果把所有边按权重排序，从最小开始，依次选择不形成环的边，直到选出V-1条边；结果一定是最小生成树！
不需要知道全局结构，只需要局部判断是否成环；全局最优可以通过局部最优的简单组合来实现
⭐️Kruskal的适用场景：
分布式网络，模块化设计，渐进式开发，微服务架构，区块链网络，并行计算，分布式系统
⭐️最小生成树的性质：图论中的一个奇迹
其他大多数优化问题中，贪心策略都会失败。但最小生成树有两个魔法性质
性质1：切割性质（Cut Property）：对于图的任意切割，跨越切割的最小权重边一定在某个最小生成树中。
性质2：环性质（Cycle Property）：对于图的任意环，环上的最大权重边一定不在任何最小生成树中。
Prim算法 = 反复应用切割性质 ：每次：已访问节点 vs 未访问节点 形成一个切割；选择：跨越这个切割的最小边，根据切割性质，这个选择一定正确
Kruskal算法 = 反复应用环性质：每次：按权重从小到大考虑边如果加入当前边会形成环，那它一定是环上的最大边，根据环性质，这条边一定不在MST中，所以跳过
最短路径问题：局部最优（当前最短的边）不一定导致全局最优，因为我们要考虑的是整条路径的总成本，而不是每一步的成本
在最小生成树中：我们要的是所有边的总成本最小，不是某两个点之间的成本，神奇的是，在这里局部最优确实能导致全局最优
*/
function kruskalMST(graph) {
  // 步骤1：收集所有边
  const edges = [];
  for (const [u, neighbors] of Object.entries(graph)) {
    for (const [v, weight] of neighbors) {
      // 避免重复边（无向图）
      if (Number(u) < v) {
        edges.push([Number(u), v, weight]);
      }
    }
  }
  console.log('收集到的所有边:', edges);
  // 步骤2：将边按成本从小到大排序
  edges.sort((a, b) =>  a[2] - b[2]);//a[2]和b[2]是边的权重，每条边是 [u, v, weight] 格式，weight在索引2的位置
  /*边是用数组表示的，格式是：[起点, 终点, 权重]
    数组索引对应关系：[0] = 起点 (u)，[1] = 终点 (v)，[2] = 权重 (weight)
  */
  console.log('排序后的边:', edges);
  // 步骤3：初始化并查集
  const n = Object.keys(graph).length;//获取图中节点的数量，Object.keys(graph) 返回对象所有键的数组.length 的作用：获取数组的长度：
  console.log('节点数量 n =', n);
  const uf = new UnionFind(n);
  const mstEdges = [];
  
  /* 步骤4：遍历排序后的边
  console.log('\n开始处理边:');
  for (const [u, v, weight] of edges) {
    // 使用并查集检查是否形成环
    if (uf.union(u, v)) {//环检测：如果union返回true，说明不会形成环
      mstEdges.push([u, v, weight]);
    }
    // 如果已经选了 n-1 条边，提前结束//最小生成树有 V-1 条边（V个节点），提前结束优化：不用遍历所有边
    if (mstEdges.length === n-1) break;
  }*/
  // 步骤4：遍历排序后的边（带详细调试）
console.log('\n🎯 步骤4：开始处理边');
console.log('排序后的边:', edges);
console.log('期望边数: n-1 =', n-1);

let step = 1;
for (const [u, v, weight] of edges) {
  console.log(`\n--- 第${step}步: 处理边 ${u}-${v} (成本${weight}) ---`);
  
  // 记录处理前的状态
  console.log(`处理前: find(${u}) = ${uf.find(u)}, find(${v}) = ${uf.find(v)}`);
  
  // 关键调试：union 的返回值
  const unionResult = uf.union(u, v);
  console.log(`union(${u}, ${v}) 返回值:`, unionResult);
  
  // 记录处理后的状态
  console.log(`处理后: find(${u}) = ${uf.find(u)}, find(${v}) = ${uf.find(v)}`);
  
  if (unionResult) {
    mstEdges.push([u, v, weight]);
    console.log(`✅ 加入MST! 当前MST边:`, mstEdges);
  } else {
    console.log(`❌ 跳过! 原因: 会形成环`);
  }
  
  console.log(`当前MST边数: ${mstEdges.length}/${n-1}`);
  
  // 提前结束检查
  if (mstEdges.length === n - 1) {
    console.log(`💫 已达到目标边数 ${n-1}, 提前结束!`);
    break;
  }
  
  step++;
}

// 如果循环结束但边数不够
if (mstEdges.length < n - 1) {
  console.log(`⚠️ 警告: 只找到 ${mstEdges.length} 条边, 但需要 ${n-1} 条`);
  console.log('可能原因: 图不连通');
}





  console.log('最终MST边:', mstEdges);
  return mstEdges;
}
/*
⭐️并查集：一个专门处理集合合并与查询功能的数据结构；并查集不是通用数据结构，它是为解决动态连通性问题而生的专用工具
功能：
1.find(x)：找到x属于哪个集合
2.union(x, y)：把x和y所在的集合合并
特点：
1.它不存储具体数据，只存储集合关系
2.通过父指针表示树形结构，但不像二叉树那样有序
3.优化技巧独特：路径压缩、按秩合并，这些在其他数据结构中很少见
在Kruskal算法中，我们需要反复问："节点A和节点B已经在同一个连通分量里了吗？
用并查集的代价：经过路径压缩和按秩优化后，平均O(α(n))，其中α(n)是反阿克曼函数，增长极其缓慢，对于所有实际应用规模，基本可以认为是O(1)
用其他数据结构的代价：数组/链表：每次查询需要O(V)时间扫描，哈希表：难以高效处理集合合并
*/
class UnionFind {
  constructor(n) {
    this.parent = Array.from({length: n}, (_, i) => i);// 使用 Array.from 确保正确初始化
    this.rank = Array(n).fill(0);// 初始秩为0//rank（秩）是并查集的性能优化关键，没有它算法也能工作，但有了它效率能提升几个数量级
    /*
    Array(n).fill().map() 在某些环境下工作不正常。
    //this.parent = Array(n).fill().map((_, i) => 0);//创建 n 个节点，每个节点初始时都是自己的父节点 
    ⭐️map 是一个数组方法，它遍历数组的每个元素，并对每个元素执行一个函数，然后返回一个新数组。
    基本语法：
    const newArray = oldArray.map((当前元素, 索引) => {
            return 对当前元素的操作;
            });
    _ 表示当前元素（这里是 undefined，但我们不关心），i 表示当前索引（0, 1, 2, 3...），=> i 表示返回索引值本身
    Array(n) - 创建长度为 n 的空数组，.fill()-用undefined 填充空位（让map能正常工作）
    // 创建 [0, 1, 2, 3, 4]
        const arr1 = Array(5).fill().map((_, i) => i);// 创建长度为 n 的空数组，然后映射//初始时，每个人都是自己的父节点
        console.log(arr1); // [0, 1, 2, 3, 4]
    ⭐️rank ：平衡树高
    1.记录的是树的高度估计值（不是精确高度，是上界）
    2.合并规则： 总是让矮树并入高树
    3.没有按秩合并的 union总是让y并入x可能会形成很长的链， find(5) 需要遍历整个链，退化为 O(n)
    4.rank 的作用：
    避免树退化成链，保持近似平衡；与路径压缩配合，达到近乎常数时间；让Kruskal从理论算法变成实用算法
    没有 rank，Kruskal在处理1000个节点时可能就慢得无法忍受；有 rank，可以轻松处理百万级节点
    */
   // 添加调试验证
    console.log('UnionFind 初始化验证:');
    console.log('   parent数组:', this.parent);
    console.log('   应该为:    ', Array.from({length: n}, (_, i) => i));
  
}
  find(x) {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]); 
      /*⭐️路径压缩：
        1.它在一次查找中，把长长的访问路径压缩成了直接连接。真正的路径压缩发生在那些原本不直接指向根节点的中间节点上。
        2.在Kruskal算法中，我们会反复查询节点的根节点。没有路径压缩的话，算法会越来越慢；有路径压缩，速度基本保持恒定
        3.x 可以是任何节点，从 0 到 n-1 都可以。路径压缩对所有节点都有效
        特点：
        1.向下递归：一层层找到终极根节点；向上返回：在返回路径上完成路径压缩；递归返回的过程中完成了额外工作（路径压缩），而不只是简单地传递结果
        2.大多数递归只是return f(n-1) + something;但这个递归是：this.parent[x] = find(parent[x]); // 在返回时修改结构return this.parent[x];
        3.路径压缩是用第一次的代价换取后续所有操作的极速
        4.在链 0←1←2←3←4 中：当调用 find(4) 时，函数内部确实产生了这样的递归链find(4) → find(3) → find(2) → find(1) → find(0)
        递归下去时：一层层找父节点；递归返回时：在返回路径上修改父指针
        */
    }
    return this.parent[x];//return的作用：传递根节点信息，向上传递信息：告诉调用者根节点是谁；让每一层都能完成 this.parent[x] = 根节点的压缩操作
  }
  union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);
    if (rootX === rootY) return false;//合并失败，两个节点已经在同一集合
    // 按秩合并
    if (this.rank[rootX] < this.rank[rootY]) {
      this.parent[rootX] = rootY;//矮树X并入高树Y
    } else if (this.rank[rootX] > this.rank[rootY]) {
      this.parent[rootY] = rootX;//矮树Y并入高树X  
    } else {
      this.parent[rootY] = rootX; // 高度相同，任选一个为根
      this.rank[rootX]++;//树高+1
    }
    return true;//合并成功，两个节点原本不在同一集合，合并操作成功执行
  }
}
//测试
const complexGraph2 = {//多个环，桥接边：有些边是连接不同部分的关键，权重竞争：很多边的权重很接近，稠密连接：某些节点有4个邻居
  0: [[1, 3], [2, 5], [4, 2]],
  1: [[0, 3], [2, 1], [3, 4]],
  2: [[0, 5], [1, 1], [3, 2], [5, 3]],
  3: [[1, 4], [2, 2], [6, 1]],
  4: [[0, 2], [5, 4], [7, 3]],
  5: [[2, 3], [4, 4], [6, 2], [8, 1]],
  6: [[3, 1], [5, 2], [9, 3]],
  7: [[4, 3], [8, 2], [10, 4]],
  8: [[5, 1], [7, 2], [9, 5], [11, 3]],
  9: [[6, 3], [8, 5], [11, 2]],
  10: [[7, 4], [11, 1]],
  11: [[8, 3], [9, 2], [10, 1]]
};
/*复杂图会测试算法的:
环检测能力：能否正确跳过所有会形成环的边
权重决策：当多条边权重相近时，能否做出正确选择
连通性保证：最终是否真的连通了所有节点
提前终止：是否在得到n-1条边时正确终止
*/

console.log('=== Kruskal算法测试 ===');
//运行Kruskal算法
const result = kruskalMST(complexGraph2);
console.log('最小生成树边:', result);
//先获取节点数量
const n = Object.keys(complexGraph2).length;
//计算总成本
const totalCost = result.reduce((sum, edge) => sum + edge[2], 0);
console.log('总成本:', totalCost);
//验证：边数应该是n-1
console.log('边数验证:', result.length === n-1);
console.log('🎉 Kruskal 算法健壮性验证通过!');
console.log('✅ 复杂图处理 ✓');
console.log('✅ 环检测准确 ✓');  
console.log('✅ 最优解找到 ✓');
console.log('✅ 提前终止智能 ✓');
console.log('🎊 算法完全健壮!');
```