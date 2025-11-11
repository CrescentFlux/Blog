# BFS DFS Algorithm
## **基础知识**
- **深度优先搜索 (DFS)**
  - 定义：一种用于遍历或搜索树或图的算法，它沿着每个分支尽可能深地探索，直到无法继续前进，然后回溯到上一个分支点。
  - 关键特性：使用栈（LIFO）；

- **广度优先搜索 (BFS)**
  - 定义：一种按层次遍历树或图的算法，先访问起始顶点的所有邻接点，然后再访问这些邻接点的邻接点，依此类推。
  - 关键特性：使用队列（FIFO）；

## 注意事项
1. **混淆点**
- **算法对比**

| 特性 | DFS (深度优先) | BFS (广度优先) |
|------|----------------|----------------|
| 数据结构 | 栈 | 队列 |
| 适用场景 | 拓扑排序、连通分量 | 最短路径、层级遍历 |
| 空间复杂度 | O(h) | O(w) |







2. **代码实现**
```
//============================BFS==========================//
class GraphWithBFS {
    constructor() {
        this.adjacencyList = {};
    }
    
    addVertex(vertex) {
        if (!this.adjacencyList[vertex]) {
            // 1: 初始化空数组作为邻居列表
            this.adjacencyList[vertex] = [];
        }
    }
    
    addEdge(vertex1, vertex2) {
        //  2: 确保两个顶点都存在
        this.addVertex(vertex1);
        this.addVertex(vertex2);
        
        //  3: 互相添加邻居
        this.adjacencyList[vertex1].push(vertex2);
        this.adjacencyList[vertex2].push(vertex1);
    }
    
    bfs(startVertex) {
        //📜整个BFS最短路径算法的核心思想：从起点开始，一层层往外探索，记录每条路径//最短路径问题可以转化为层次遍历问题，不需要复杂计算，只需要正确记录
        //👉选择队列：先进先出保证广度优先//👉选择数组：简单直接记录路径//👉选择Set：快速去重防循环
        //  1: 如果起点不存在，直接返回
        if (!this.adjacencyList[startVertex]) {
            console.log("起点不存在");
            return;
        }
        //  2: 创建已访问集合和队列
        const visited = new Set();
        /*👉使用Set更语义化,使用Map功能过剩,我们只需要记录"谁被访问过"，不需要关联值, Set的API更简洁直观,内存使用更高效（不存储无用的值）
        const visited = new Set();                const visited = new Map();  使用 Map - 功能过剩
        visited.add('A'); // "A被访问了"           visited.set('A', true); // 我们其实不需要这个true值！
        visited.has('A'); // "A被访问过吗？"        visited.has('A'); // 只需要键，值没用上                                                  
        */
        const queue = [startVertex];
        
        //  3: 标记起点为已访问
        visited.add(startVertex);
        
        console.log(`开始BFS遍历，从顶点 ${startVertex} 出发`);
        let step = 0;
        
        while (queue.length > 0) {  //  4: 队列不为空时循环,检查队列长度
            //  5: 从队列头部取出当前顶点,先进先出
            const current = queue.shift();
            step++;
            
            console.log(`第${step}步: 访问 ${current}`);
            
            // 6.遍历当前顶点的所有邻居
            for (let neighbor of this.adjacencyList[current]) {//for...of 循环，for (let item of collection) 对每个item执行操作
                //  7. 如果邻居未被访问
                if (!visited.has(neighbor)) {
                    //  8. 标记为已访问并加入队列
                    visited.add(neighbor);
                    queue.push(neighbor);
                    console.log(`  发现新顶点: ${neighbor}，加入队列`);
                }
            }
            
            console.log(`  当前队列: [${queue.join(', ')}]`);
        }
        
        console.log(`BFS完成！共访问 ${visited.size} 个顶点`);  // 
        return Array.from(visited);
    }
    
    // BFS查找最短路径
    bfsShortestPath(startVertex, targetVertex) {
        if (!this.adjacencyList[startVertex] || !this.adjacencyList[targetVertex]) {
            return null;
        }
        //👉BFS按层次遍历：当第一次到达目标顶点时，路径一定是最短的；队列始终按路径长度排序：短路径先处理，长路径后处理
        const visited = new Set();
        //1. 队列存储[当前顶点, 路径数组]
        const queue = [[startVertex, [startVertex]]];
        visited.add(startVertex);
        
        console.log(`寻找从 ${startVertex} 到 ${targetVertex} 的最短路径`);
        
        while (queue.length > 0) {
            // 2. 取出当前顶点和路径
            const [current, path] = queue.shift(); //当前顶点 + 到达当前顶点的路径
            
            console.log(`  检查: ${current}，当前路径: [${path.join(' → ')}]`);
            
            // 3. 如果找到目标顶点
            if (current === targetVertex) {
                console.log(`✅ 找到最短路径: [${path.join(' → ')}]`);
                return path;
            }
            // 4.遍历邻居
            for (let neighbor of this.adjacencyList[current]) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    //5: 将新路径加入队列
                    queue.push([neighbor, [...path,neighbor]]);
                    // 展开运算符（简洁）...path 把原路径展开，然后添加新的邻居✅创建副本
    //👉路径不可变：每次创建新数组，不修改原路径；完整记录：队列中保存的是从起点到当前点的完整路径；最短保证：BFS按路径长度顺序处理，保证找到最短路径
                }
            }
        }
        
        console.log("❌ 路径不存在");
        return null;
    }
}

// 测试代码
function testBFS() {
    const graph = new GraphWithBFS();
    //添加测试图的顶点和边
    ['A', 'B', 'C', 'D', 'E'].forEach(vertex => {
        graph.addVertex(vertex);
    });
    graph.addEdge('A', 'B');
    graph.addEdge('A', 'C');
    graph.addEdge('B', 'D');
    graph.addEdge('C', 'E');
    graph.addEdge('D', 'E');
    console.log("=== BFS遍历测试 ===");
    //从A开始BFS遍历
    graph.bfs('A');
    console.log("\n=== 最短路径测试 ===");
    //查找A到E的最短路径
    graph.bfsShortestPath('A', 'E');
}
// 执行测试
testBFS();


//===================================DFS================================//
class GraphWithDFS {
    constructor() {
        this.adjacencyList = {};
    }
    addVertex(vertex) {
        if (!this.adjacencyList[vertex]) {
            // 1: 初始化顶点的邻居列表,初始化空数组
            this.adjacencyList[vertex] = [];
        }
    }
    
    addEdge(vertex1, vertex2) {
        this.addVertex(vertex1);
        this.addVertex(vertex2);
        this.adjacencyList[vertex1].push(vertex2);
        this.adjacencyList[vertex2].push(vertex1);
    }
/*👉两种不同的DFS目标：
目标1：访问记录，记录所有访问过的顶点；特点：✅包含死胡同（D是死胡同，但确实访问过）✅记录完整探索历史✅不需要pop-历史不应该被删除
目标2：路径跟踪（需要pop）维护当前有效路径//特点：✅排除死胡同（D被移除了）✅只保留正确路线✅需要pop - 错误路线要删除！
*/   
    //DFS递归实现 - 分析遍历顺序 - 隐式栈
    dfsRecursive(startVertex) {
        //  2: 创建已访问集合和结果数组
        const visited = new Set();
        const result = []; //🎯分析DFS的遍历行为
        console.log(`开始DFS递归遍历，从顶点 ${startVertex} 出发`);
        const dfs = (vertex) => {
            //  3: 如果顶点已访问，直接返回.检查是否已访问
            if (visited.has(vertex)) return;
            // 4: 标记为已访问并记录结果
            visited.add(vertex);
            result.push(vertex);//📝记录：这个顶点被访问了
            console.log(` 访问: ${vertex}`);
            const neighbors = this.adjacencyList[vertex];
            // 5: 对邻居排序让遍历更可预测
            neighbors.sort();
            //👉让遍历结果可预测,便于调试和理解,问题复现
            for (let neighbor of neighbors) {
                if (!visited.has(neighbor)) {
                    console.log(`从 ${vertex} 深入探索 ${neighbor}`);
                    // 6: 递归调用DFS
                    dfs(neighbor);
                    console.log(`从 ${neighbor} 回溯到 ${vertex}`);
                }
            }
        };
        // 7: 从起点开始DFS
        dfs(startVertex);
        console.log(` DFS递归完成！访问顺序: [${result.join(' → ')}]`);
        return result; //返回：完整的访问历史
    }
    
    //DFS迭代实现 - 使用栈 - 显式栈
    dfsIterative(startVertex) {
        //👉递归调用栈本身就在自动处理回溯，但我们手动管理path数组时还需要额外的回溯
        //👉函数调用时：压栈，保存执行上下文函数返回时：弹栈，恢复执行上下文,这是语言层面的自动回溯
        if (!this.adjacencyList[startVertex]) {
            console.log("起点不存在");
            return;
        }
        //1: 创建已访问集合和栈
        const visited = new Set();
        const stack = [startVertex];
        const result = [];
        visited.add(startVertex);
        console.log(`开始DFS迭代遍历，从顶点 ${startVertex} 出发`);
        let step = 0;
        while (stack.length > 0) {  // 2: 栈不为空时循环
            //  3: 从栈顶取出当前顶点（后进先出）
            const current = stack.pop();//👉BFS: queue.shift()队列,DFS: stack.pop()栈//✅显式出栈
            step++;
            
            console.log(`第${step}步: 访问 ${current}`);
            result.push(current);//✅显式入栈
            
            const neighbors = this.adjacencyList[current];
            //4: 反向排序以保证与递归结果一致
            neighbors.sort().reverse();
            for (let neighbor of neighbors) {
                if (!visited.has(neighbor)) {
                    //5: 标记并压入栈顶
                    visited.add(neighbor);
                    stack.push(neighbor);
                    console.log(`  发现新顶点: ${neighbor}，压入栈顶`);
                }
            }
            console.log(`  当前栈: [${stack.join(', ')}]`);
        }
        
        console.log(`🏁 DFS迭代完成！访问顺序: [${result.join(' → ')}]`);
        return result;
    }
    
    // DFS查找路径（不一定最短）
    dfsFindPath(startVertex, targetVertex) {
        const visited = new Set();
        const path = [];//👉手动回溯
        console.log(`🎯 DFS寻找从 ${startVertex} 到 ${targetVertex} 的路径`);
        const dfs = (vertex) => {
            //1: 如果已访问，返回false
            if (visited.has(vertex)) return false;
            visited.add(vertex);
            path.push(vertex);
            console.log(`   尝试路径: [${path.join(' → ')}]`);
            
            //2: 如果找到目标顶点
            if (vertex === targetVertex) {
                console.log(` 找到路径: [${path.join(' → ')}]`);
                return true;
            }
            const neighbors = this.adjacencyList[vertex];
            neighbors.sort();
            for (let neighbor of neighbors) {
                //3: 如果递归找到路径，返回true
                if (dfs(neighbor)) {
                    return true;
                }
            }
            
            //4: 回溯 - 从路径中移除当前顶点
            path.pop();//👉回溯(Backtracking):走错路时，退回到上一个岔路口保持;承认当前选择是错误的，退回到上一个决策点，尝试其他可能性
            //👉路径纯净,path只包含当前有效路径;节省内存;有回溯：path长度 ≈ 当前探索深度;正确性保证:返回的路径是真实的有效路径
            console.log(`  回溯，移除 ${vertex}`);
            return false;
        };
        if (dfs(startVertex)) {
            return path;
        } else {
            console.log("❌ 路径不存在");
            return null;
        }
    }
}

// 测试代码
function testDFS() {
    const graph = new GraphWithDFS();
    
    //构建测试图
    ['A', 'B', 'C', 'D', 'E', 'F'].forEach(vertex => {
        graph.addVertex(vertex);
    });
    
    graph.addEdge('A', 'B');
    graph.addEdge('A', 'C');
    graph.addEdge('B', 'D');
    graph.addEdge('C', 'E');
    graph.addEdge('C', 'F');
    graph.addEdge('D', 'E');
    
    console.log("=== DFS递归遍历测试 ===");
    //测试递归DFS
    graph.dfsRecursive('A');
    
    console.log("\n=== DFS迭代遍历测试 ===");
    //测试迭代DFS  
    graph.dfsIterative('A');
    
    console.log("\n=== DFS路径查找测试 ===");
    //测试DFS路径查找
    graph.dfsFindPath('A', 'F');
}

// 执行测试
testDFS();
```