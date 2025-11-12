# Heap
## 基础知识
- **定义**：堆是一种特殊的完全二叉树，它满足堆属性：在最小堆中：父节点的值 ≤ 所有子节点的值；在最大堆中：父节点的值 ≥ 所有子节点的值
    - 三大特征：完全二叉树结构，堆序性质，数组存储方式
    - 完全二叉树：除了最后一层，其他层都是满的，并且最后一层的节点都尽量靠左排列；完全二叉树可以用数组完美表示，没有空洞
      - 完全二叉树判断规则：从根节点开始，按层级从左到右编号如果编号出现跳号，就不是完全二叉树；从左到右、逐层填充、没有空洞
- **堆的类别**：
    - 按堆性质分：最小堆：根节点是最小值；最大堆：根节点是最大值
    - 按实现方式分：二叉堆：每个节点最多两个子节点；二项堆：更复杂的合并操作；斐波那契堆：理论最优但实现复杂

- **堆的优势**：用数组而不用树节点的优势：内存连续，缓存友好；不需要指针，节省空间；通过数学计算快速定位父子节点
- **核心能力**：快速访问最值，应用：当需要频繁访问最值，同时数据动态变化时


## **注意事项**
1. **混淆点**

|完全二叉树 vs 满二叉树|内容|其他混淆性质|
---|---|---
|满二叉树 (Full Binary Tree)：|每个节点都有0个或2个子节点，所有叶子都在同一层|所有满二叉树都是完全二叉树，但反过来不成立|
|完全二叉树 (Complete Binary Tree)：|除了最后一层，其他层都是满的，最后一层节点尽量靠左|1.在堆中，唯一的要求是：父节点 ≤ 子节点（最小堆）2.左右子树的大小是随机的，不需要遵守特定规则;3.堆的目标：快速访问最值，而不是完全排序|



2. **代码实现**
```
//=========================================🔄堆=============================================//
class MinHeap {
    constructor() {
        this.heap = []; //堆的存储结构
    }
    //💡堆的导航系统：核心思想：数组当做树来操作虽然堆在内存中是个普通数组但这些导航方法让我们能够像操作树一样操作数组：通过数学计算就能找到父子关系
    // 获取父节点索引
    _parentIndex(index) {
        return Math.floor((index - 1) / 2);
    }
    /*第k层的特性：第k层有 2^k 个节点，第k层的第一个节点索引是：2^k - 1，第k层的最后一个节点索引是：2^(k+1) - 2
    在完全二叉树中，如果根节点在第0层，那么第k层的第一个节点索引是 2^k - 1"
    已知：第k层有 2^k 个节点，第k层的节点索引范围是：[2^k - 1, 2^(k+1) - 2]
    对于索引为i的节点：它位于第k层，其中 k = floor(log₂(i+1))，在该层中的位置是：pos = i - (2^k - 1)
    父节点在第k-1层，在该层中的位置是：floor(pos / 2)，所以父节点索引 = (2^(k-1) - 1) + floor(pos / 2)
    parent = floor((i-1)/2)
    2.子节点索引：对于索引为i的节点在第k层：在该层中的位置：pos = i - (2^k - 1)，左孩子在下一层的第 2*pos 个位置，
    左孩子索引 = (2^(k+1) - 1) + 2*pos得到：leftChild = 2*i + 1
    */
    // 获取左孩子索引
    _leftChildIndex(index) {
        return 2 * index + 1; 
    }
    
    // 获取右孩子索引
    _rightChildIndex(index) {
        return 2 * index + 2;
    }
    
    // 交换两个元素
    _swap(i, j) {
        [this.heap[i], this.heap[j]] = [this.heap[j], this.heap[i]];
    }
    
    // 插入元素
    insert(value) {
        this.heap.push(value); // 将新值添加到数组末尾
        this._bubbleUp(this.heap.length - 1); //从最后一个位置开始上浮
    }
    
    // 上浮操作
    _bubbleUp(index) {
        while (index > 0) {
            const parentIndex = this._parentIndex(index);
            // 如果父节点已经 <= 当前节点，满足堆性质，退出
            if (this.heap[parentIndex] <= this.heap[index]) break; //比较父节点和当前节点
            
            // 否则交换并继续上浮
            this._swap(index, parentIndex); //与父节点交换
            index = parentIndex; // 更新当前位置为父节点位置
        }
    }
    
    // 查看最小值（不删除）
    peek() {
        return this.heap.length > 0 ? this.heap[0] : null; //最小值总是在根节点（索引0）
    }
    
    // 获取堆大小
    size() {
        return this.heap[0].length; //返回堆数组的长度
    }
    
    // 判断堆是否为空
    isEmpty() {
        return this.heap.length === 0; //检查数组是否为空
    }
    // 删除并返回最小值
    extractMin() {
        if (this.heap.length === 0) return null; //堆为空返回null
        if (this.heap.length === 1) return this.heap.this.heap.pop(); //只有一个元素直接弹出
        
        const min = this.heap[0];
        // 用最后一个元素替换根节点
        this.heap[0] = this.heap.pop();//弹出最后一个元素并放到根位置,这里一次性完成两个操作:返回数组的最后一个元素,从数组中删除这个元素
        // 下沉调整
        this._sinkDown(0); //从根节点开始下沉
        
        return min;
    }
    // 下沉操作
    _sinkDown(index) {
        const length = this.heap.length;
        
        while (true) {
            const leftChildIndex = this._leftChildIndex(index);
            const rightChildIndex = this._rightChildIndex(index);
            let smallest = index; //先假设当前节点是最小的
            
            // 找三个节点中最小的//堆的性质要求
            if (leftChildIndex < length && 
                this.heap[leftChildIndex] < this.heap[smallest]) {
                smallest = leftChildIndex; 
            }
            
            if (rightChildIndex < length && 
                this.heap[rightChildIndex] < this.heap[smallest]) {
                smallest = rightChildIndex;
            }
            
            // 如果当前节点已经是最小的，退出循环
            if (smallest === index) break; //堆性质已满足
            
            // 交换并继续下沉
            this._swap(index, smallest); 
            index = smallest; //更新当前位置
        }
    }
    // 从数组构建堆
    heapify(array) {
        this.heap = [...array]; //复制传入的数组
        // 从最后一个非叶子节点开始，向前遍历进行下沉
        for (let i = Math.floor(this.heap.length / 2); i >= 0; i--) {
            //从 length/2 开始叶子节点不需要下沉,最后一个非叶子节点索引 = floor(长度/2),从后往前处理，保证处理父节点时，子树已经是堆
            this._sinkDown(i); //对每个非叶子节点进行下沉
        }
    }
    printAndValidate() {
        console.log('=== 堆状态 ===');
        console.log('堆数组:', this.heap);
        console.log('大小:', this.size());
        console.log('是否为空:', this.isEmpty());
        console.log('最小值:', this.peek());
        
        // 验证堆性质
        const isValid = this._validateHeap();
        console.log('堆性质验证:', isValid ? '✅ 通过' : '❌ 失败');
        
        // 打印树结构
        this.printTree();
        
        return isValid;
    }
    
    _validateHeap() {
        for (let i = 0; i < this.heap.length; i++) {
            const left = this._leftChildIndex(i);
            const right = this._rightChildIndex(i);
            
            if (left < this.heap.length && this.heap[i] > this.heap[left]) {
                console.log(`❌ 违反堆性质: 父节点[${i}]=${this.heap[i]} > 左孩子[${left}]=${this.heap[left]}`);
                return false;
            }
            
            if (right < this.heap.length && this.heap[i] > this.heap[right]) {
                console.log(`❌ 违反堆性质: 父节点[${i}]=${this.heap[i]} > 右孩子[${right}]=${this.heap[right]}`);
                return false;
            }
        }
        return true;
    }
    // 打印堆（调试用）
    print() {
        console.log('MinHeap:', this.heap); //打印堆数组}
       // 打印树结构
    }
    printTree() {
        if (this.heap.length === 0) {
            console.log('堆为空');
            return;
        }
        
        let result = '';
        const levels = Math.floor(Math.log2(this.heap.length)) + 1;
        
        for (let i = 0; i < levels; i++) {
            const start = Math.pow(2, i) - 1;
            const end = Math.min(Math.pow(2, i + 1) - 1, this.heap.length);
            const levelNodes = this.heap.slice(start, end);
            
            // 添加缩进
            const indent = ' '.repeat(Math.pow(2, levels - i - 1) - 1);
            result += indent + levelNodes.join(' ') + '\n';
            
            // 添加连接线（除了最后一层）
            if (i < levels - 1) {
                const lineIndent = ' '.repeat(Math.pow(2, levels - i - 2) - 1);
                const lines = '/\\ '.repeat(levelNodes.length).trim();
                result += lineIndent + lines + '\n';
            }
        }
        
        console.log('堆的树结构:');
        console.log(result);
    }
    printTreeDetailed() {
        if (this.heap.length === 0) {
            console.log('堆为空');
            return;
        }
        
        console.log('堆的树结构:');
        this._printNode(0, '', true);
    }
    
    _printNode(index, prefix, isLeft) {
        if (index >= this.heap.length) return;
        
        // 打印当前节点
        console.log(prefix + (isLeft ? '├── ' : '└── ') + this.heap[index]);
        
        // 准备新的前缀
        const newPrefix = prefix + (isLeft ? '│   ' : '    ');
        
        // 递归打印左右子树
        const leftIndex = this._leftChildIndex(index);
        const rightIndex = this._rightChildIndex(index);
        
        if (leftIndex < this.heap.length) {
            this._printNode(leftIndex, newPrefix, true);
        }
        if (rightIndex < this.heap.length) {
            this._printNode(rightIndex, newPrefix, false);
        }
    }}
    


// 测试堆的功能
function testMinHeap() {
    const heap = new MinHeap();
    
    // 测试插入
    heap.insert(5);
    heap.insert(3);
    heap.insert(8);
    heap.insert(1);
    heap.insert(10);
    heap.printTree();
    heap.printTreeDetailed();
    console.log('插入后堆:', heap.heap);
    console.log('最小值:', heap.peek()); //应该输出1但不删除
    
    // 测试删除
    console.log('删除的值:', heap.extractMin()); //应该输出1
    console.log('删除后堆:', heap.heap);
    
    // 测试堆化
    const heap2 = new MinHeap();
    heap2.heapify([15, 10, 20, 5, 8, 25]);
    console.log('堆化后:', heap2.heap);
    console.log('大小:', heap2.size());
    heap2.printTree();
    heap2.printTreeDetailed();
}
// 增强的测试函数，每一步都打印堆状态
function testMinHeapWithVisualization() {
    console.log('=== 开始堆测试 ===\n');
    
    const heap = new MinHeap();
    
    // 测试插入操作
    console.log('1. 插入元素 5');
    heap.insert(5);
    heap.printAndValidate();
    heap.printTreeDetailed();
    console.log('\n2. 插入元素 3');
    heap.insert(3);
    heap.printAndValidate();
    heap.printTreeDetailed();
    console.log('\n3. 插入元素 8');
    heap.insert(8);
    heap.printAndValidate();
    heap.printTreeDetailed();
    console.log('\n4. 插入元素 1');
    heap.insert(1);
    heap.printAndValidate();
    heap.printTreeDetailed();
    console.log('\n5. 插入元素 10');
    heap.insert(10);
    heap.printAndValidate();
    heap.printTreeDetailed();
    // 测试查看最小值（不删除）
    console.log('\n6. 查看最小值（不删除）');
    console.log('当前最小值:', heap.peek());
    heap.printAndValidate(); // 堆应该保持不变
    heap.printTreeDetailed();
    // 测试删除操作
    console.log('\n7. 第一次删除最小值');
    const removed1 = heap.extractMin();
    console.log('删除的值:', removed1);
    heap.printAndValidate();
    heap.printTreeDetailed();
    console.log('\n8. 第二次删除最小值');
    const removed2 = heap.extractMin();
    console.log('删除的值:', removed2);
    heap.printAndValidate();
    heap.printTreeDetailed();
    console.log('\n9. 第三次删除最小值');
    const removed3 = heap.extractMin();
    console.log('删除的值:', removed3);
    heap.printAndValidate();
    heap.printTreeDetailed();
    // 测试堆化
    console.log('\n=== 测试堆化功能 ===');
    const heap2 = new MinHeap();
    console.log('堆化数组: [15, 10, 20, 5, 8, 25]');
    heap2.heapify([15, 10, 20, 5, 8, 25]);
    heap2.printAndValidate();
    heap2.printTreeDetailed();
    console.log('\n堆化后删除最小值');
    const removedFromHeap2 = heap2.extractMin();
    console.log('删除的值:', removedFromHeap2);
    heap2.printAndValidate();
    heap2.printTreeDetailed();
}
// 运行测试
testMinHeap();
// 运行增强测试
testMinHeapWithVisualization();
//=======================================🔄dijkstra======================================//
function dijkstraBasic(graph, start) {
    // 初始化距离表，记录从起点到每个节点的最短距离
    const distances = {};
    // 初始化已访问集合，记录已经确定最短路径的节点
    const visited = new Set();
    // 初始化前驱节点表，用于回溯路径
    const previous = {};
    // 获取所有节点
    const nodes = Object.keys(graph);
    // 步骤1: 初始化所有节点的距离为无穷大
    for (const node of nodes) {
        distances[node] = Infinity; 
        previous[node] = null;
    }
    // 起点的距离设为0
    distances[start] = 0; 
    // 主循环：当还有节点未访问时继续
    while (visited.size < nodes.length) {
        // 步骤2: 从未访问节点中找到距离最近的节点
        let currentNode = null;
        let minDistance = Infinity;
        
        for (const node in distances) {
            if (!visited.has(node) && distances[node] < minDistance) {
                minDistance = distances[node];
                currentNode = node;
            }
        }
        if (currentNode === null) break;
        // 标记当前节点为已访问
        visited.add(currentNode);
        // 步骤3: 更新所有邻居的距离
        for (const [neighbor, weight] of graph[currentNode]) {
            if (!visited.has(neighbor)) {
                // 计算经过当前节点到达邻居的新距离
                const newDistance = distances[currentNode] + weight; 
                // 如果新距离更短，则更新
                if (newDistance < distances[neighbor]) {
                    distances[neighbor] = newDistance;
                    previous[neighbor] = currentNode; 
                }
            }
        }
    }
    return { distances, previous };
}
class PriorityQueue {
    constructor() {
        this.nodes = []; // 存储节点和它们的优先级（距离）
    }
    
    enqueue(node, priority) {
        this.nodes.push({ node, priority });
        this.nodes.sort((a, b) =>  a.priority - b.priority); //按优先级升序排序，让最小的在最前面
    }
    
    dequeue() {
        return this.nodes.shift().node;// 取出优先级最高的（第一个元素）
    }
    
    isEmpty() {
        return this.nodes.length === 0; //检查队列是否为空
    }
}
function dijkstraWithPQ(graph, start) {
    //👉使用优先队列优化版的 Dijkstra 算法，用更高效的方式找到从起点到所有其他节点的最短路径,用优先队列的数据结构替代了耗时的线性搜索，让算法在大型图中运行得更快
    // 初始化数据结构
    const distances = {}; // 记录到每个节点的最短距离
    const previous = {}; // 记录路径回溯信息
    const pq = new PriorityQueue(); // 优先队列，帮我们快速找到最近节点
    
    // 初始化所有节点
    for (const node in graph) {
        distances[node] = node === start ? 0 : Infinity;// 起点距离为0，其他无穷大
        previous[node] = null; //还没有前驱节点
        if (node === start) {
            pq.enqueue(node, 0); //起点入队，优先级为0
        }
    }
    //主循环阶段
    while (!pq.isEmpty()) {
        const currentNode = pq.dequeue();
        
        for (const [neighbor, weight] of graph[currentNode]) {
            const newDistance = distances[currentNode] + weight;
            
            // 核心逻辑：如果找到更短路径
            if (newDistance < distances[neighbor]) { //新距离比已知距离更短
                distances[neighbor] = newDistance;
                previous[neighbor] = currentNode;
                // 将邻居加入优先队列
                pq.enqueue(neighbor, newDistance); // 邻居入队，优先级为新距离
            }
        }
    }
    
    return { distances, previous };
}
function getShortestPath(previous, endNode) {//从结果中重构出完整路径的工具,把 Dijkstra 算法生成的"前驱节点表"转换成人类能看懂的完整路径
    const path = [];// 用来存储最终的路径
    let currentNode = endNode;// 从终点开始回溯
    
    // 从终点回溯到起点
    while (currentNode !== null) { // 当前节点不为空时继续
        path.unshift(currentNode); // 将当前节点添加到路径开头
        currentNode = previous[currentNode]; // 移动到前一个节点
    }
    
    return path;
}
/*
👉加权图就是在普通的图基础上，给每条边都赋予一个"权重"（数值）的图，Dijkstra算法为加权图设计。
普通图（无权重）：只记录连接关系；加权图：记录连接关系和权重；
加权图的三种类型：距离/成本权重（正数）收益/容量权重（正数）混合权重（可能有负数）
Dijkstra 算法不能处理负权重的边，负权边会破坏"一旦确认就是最短路径"的前提  
算法的时间复杂度：基础版本：O(V²)，优先队列版本：O((V+E) log V)
算法的核心思想是贪心算法，每次都是选择最近的节点   
该算法保证找到的是单源最短路径，它从单个起点出发，找到到所有其他节点的最短路径
👉同样的逻辑适用于：地图导航，网络路由，任务调度，游戏AI寻路
*/

// 使用示例
const graph = {
    'A': [['B', 4], ['C', 2]],
    'B': [['A', 4], ['C', 1], ['D', 5]],
    'C': [['A', 2], ['B', 1], ['D', 8], ['E', 10]],
    'D': [['B', 5], ['C', 8], ['E', 2]],
    'E': [['C', 10], ['D', 2]]
};

const result = dijkstraBasic(graph, 'A');
const pathToE = getShortestPath(result.previous, 'E');

console.log('最短路径:', pathToE.join(' -> ')); // 应该输出: A -> C -> B -> D -> E
console.log('总距离:', result.distances['E']); // 应该输出: 10
// 测试
const testGraph = {//定义图的邻接表表示法，表示一个图结构，每个节点都记录它能直接到达的邻居和距离//优势：节省空间，只存储实际存在的连接
    'S': [['A', 7], ['B', 2], ['C', 3]],
    'A': [['S', 7], ['B', 3], ['D', 4]],
    'B': [['S', 2], ['A', 3], ['D', 4], ['H', 1]],
    'C': [['S', 3], ['L', 2]],
    'D': [['A', 4], ['B', 4], ['F', 5]],
    'H': [['B', 1], ['F', 3], ['G', 2]],
    'F': [['D', 5], ['H', 3]],
    'G': [['H', 2], ['E', 2]],
    'L': [['C', 2], ['I', 4], ['J', 4]],
    'I': [['L', 4], ['J', 6], ['K', 4]],
    'J': [['L', 4], ['I', 6], ['K', 4]],
    'K': [['I', 4], ['J', 4], ['E', 5]],
    'E': [['G', 2], ['K', 5]]
};

const testResult = dijkstraBasic(testGraph, 'S');
console.log('S到E的最短路径:', getShortestPath(testResult.previous, 'E').join(' -> '));
console.log('距离:', testResult.distances['E']);
//=======================================🔄优化Dijkstra====================================//
class PriorityQueue {
    //📜没有堆：每次找最小值需要检查所有节点，有堆：直接获取堆顶就是最小值
    constructor() {
        this.heap = [];
    }
    //修改堆，使其能存储节点和距离
    // 插入节点和距离
    enqueue(node, distance) {
        this.heap.push({ node, distance });
        this._bubbleUp(this.heap.length - 1);
        /*堆插入操作的核心，从堆的最后一个位置开始上浮调整，请从新插入的元素位置开始，向上检查并调整，直到堆性质恢复
        this.heap.length - 1新元素1的索引
        this._bubbleUp(3)：从索引3（新元素1）开始，不断与父节点比较，如果违反堆性质就交换，直到满足堆性质
        */
    }
    
    // 删除并返回距离最小的节点
    dequeue() {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop();
        
        const min = this.heap[0];
        this.heap[0] = this.heap.pop();
        this._sinkDown(0);
        return min;
    }
    
    // 查看最小距离节点（不删除）
    peek() {
        return this.heap[0] || null;
    }
    
    isEmpty() {
        return this.heap.length === 0;
    }
    
    // 堆调整方法（需要修改比较逻辑）
    _bubbleUp(index) {
        while (index > 0) {
            const parentIndex = Math.floor((index - 1) / 2);
            // 比较distance而不是直接比较值
            if (this.heap[parentIndex].distance <= this.heap[index].distance) break;
            
            [this.heap[parentIndex], this.heap[index]] = 
            [this.heap[index], this.heap[parentIndex]];
            index = parentIndex;
        }
    }
    
    _sinkDown(index) {
        const length = this.heap.length;
        while (true) {
            const leftChildIndex = 2 * index + 1;
            const rightChildIndex = 2 * index + 2;
            let smallest = index;
            if (leftChildIndex < length && 
                this.heap[leftChildIndex].distance < this.heap[smallest].distance) {
                smallest = leftChildIndex;
            }
            
            if (rightChildIndex < length && 
                this.heap[rightChildIndex].distance < this.heap[smallest].distance) {
                smallest = rightChildIndex;
            }
            
            if (smallest === index) break;
            // 这里！没有调用 _swap 方法，而是直接写交换逻辑
            [this.heap[index], this.heap[smallest]] = 
            [this.heap[smallest], this.heap[index]];
            index = smallest;
        }
    }
}
//用优先队列实现Dijkstra
function dijkstraWithHeap(graph, start) {
    // 初始化数据结构// 初始化: O(V)
    const distances = {};
    const previous = {};
    const pq = new PriorityQueue();
    
    // 1. 初始化所有节点的距离
    for (const node in graph) {
        distances[node] = node === start ? 0 : Infinity;
        previous[node] = null;
    }
    // 2. 起点入队
    pq.enqueue(start, 0);
    // 3. 主循环
    while (!pq.isEmpty()) {// 循环 V 次
        // 获取当前距离最小的节点
        const { node: currentNode, distance: currentDistance } = pq.dequeue();// O(log V)
        // 如果当前距离大于已知最短距离，跳过（懒删除）
        if (currentDistance > distances[currentNode]) continue;
        // 4. 遍历所有邻居
        for (const [neighbor, weight] of graph[currentNode]) {// 总共 E 次循环
            const newDistance = distances[currentNode] + weight;
            // 5. 如果找到更短路径
            if (newDistance < distances[neighbor]) {
                distances[neighbor] = newDistance;
                previous[neighbor] = currentNode;
                // 将邻居加入优先队列// 更新和入队: O(log V)
                pq.enqueue(neighbor, newDistance);
            }
        }
    }
    return { distances, previous };
/*
每个节点最多出队一次
while (!pq.isEmpty()) {           // 循环 V 次
    const current = pq.dequeue(); // O(log V) × V = O(V log V)
}
每条边检查一次 → E 次邻居遍历
for (const [neighbor, weight] of graph[currentNode]) {
    // 可能执行 enqueue: O(log V) × E = O(E log V)
    pq.enqueue(neighbor, newDistance);
}
合并时间复杂度
总时间 = V次dequeue + E次enqueue
       = O(V log V) + O(E log V)
       = O((V + E) log V)
堆的高度是 log V，每个堆操作（插入、删除）都需要从根到叶子的路径//V：每个节点处理一次，E：每条边检查一次
懒删除的影响：这确保每个节点最多出队一次，即使它被多次入队if (currentDistance > distances[currentNode]) continue;
基础版本（没有堆）：每次找最小值需要遍历所有节点，总时间: V次循环 × V次查找 = O(V²)
*/
}
// 测试图
const graph2 = {
    'A': [['B', 4], ['C', 2]],
    'B': [['A', 4], ['C', 1], ['D', 5]],
    'C': [['A', 2], ['B', 1], ['D', 8], ['E', 10]],
    'D': [['B', 5], ['C', 8], ['E', 2]],
    'E': [['C', 10], ['D', 2]]
};
// 路径重构函数
function getShortestPath(previous, endNode) {
    const path = [];
    let currentNode = endNode;
    
    while (currentNode !== null) {
        path.unshift(currentNode);
        currentNode = previous[currentNode];
    }
    
    return path;
}

// 测试优化后的Dijkstra
function testDijkstraWithHeap() {
    console.log('=== 使用堆优化的Dijkstra算法 ===\n');
    
    const startNode = 'A';
    const { distances, previous } = dijkstraWithHeap(graph2, startNode);
    
    console.log('从起点', startNode, '到各节点的最短距离:');
    for (const node in distances) {
        console.log(`  到 ${node}: ${distances[node]}`);
    }
    
    console.log('\n最短路径详情:');
    for (const node in distances) {
        if (node !== startNode) {
            const path = getShortestPath(previous, node);
            console.log(`  ${startNode} -> ${node}: ${path.join(' → ')} (距离: ${distances[node]})`);
        }
    }
    
    // 性能对比
    console.log('\n=== 💫性能优势 ===');
    console.log('没有堆: 需要 V² 次比较');
    console.log('有堆: 只需要 (V+E) log V 次操作');
    console.log('对于大型图，性能提升显著！');
}

// 运行测试
testDijkstraWithHeap();
```












