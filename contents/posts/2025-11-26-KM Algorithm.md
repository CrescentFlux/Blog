# Kuhn-Munkres Algorithm
## 基础知识
- **定义**

   - KM算法是一种解决带权完全二分图的最大权完美匹配问题的算法,同时通过权重转换可以完美解决最小权匹配的问题。
     - 给定一个完全二分图G=(X∪Y,E)，其中|X|=|Y|=n，每条边(i,j)∈E具有非负权重wᵢ ⱼ ;通过KM算法找到一个完美匹配M⊆E，使得匹配中所有边的权重之和∑wᵢ ⱼ 达到最大值



## 注意事项
1. **混淆点**
- **KM算法核心机制**

|机制	|数学表示	|作用|常见混淆点|
---|---|---|---
|顶标 (Label)|	lx[i], ly[j]	|	构建可行性条件|顶标调整:只有搜索路径上的节点调整|
|可行性条件|	lx[i] + ly[j] ≥ weight[i][j]		|保证解的最优性|算法终止条件:找到最大权完美匹配才结束,算法保证：在相等子图中找到的完美匹配就是全局最优|
|相等子图	|lx[i] + ly[j] = weight[i][j]	|	缩小搜索范围|相等子图的动态性:相等子图随顶标调整而变化|
|δ调整	|min(lx[i]+ly[j]-weight[i][j])|		扩大匹配可能性|δ计算的范围:只计算特定组合|
|DFS增广路|	在相等子图中搜索		|找到更优匹配|匹配更新的时机:需要重新运行DFS来更新匹配,DFS搜索()才真正改变匹配关系|




2. **代码实现**
```
class KMAlgorithm {
    constructor(weights) {
        // 权重矩阵：weights[i][j] 表示左边第i个节点到右边第j个节点的权重
        this.weights = weights;
        this.n = weights.length;  // 假设是n×n的二分图
        
        // 顶标数组
        this.lx = new Array(this.n).fill(0);  // 左边顶标
        this.ly = new Array(this.n).fill(0);  // 右边顶标
        
        // 匹配关系
        this.matchX = new Array(this.n).fill(-1);  // 左边节点的匹配对象
        this.matchY = new Array(this.n).fill(-1);  // 右边节点的匹配对象
        
        // 访问标记（用于DFS）
        this.visitedX = new Array(this.n).fill(false);
        this.visitedY = new Array(this.n).fill(false);
    }
    
    // 初始化顶标：左边节点顶标 = 最大出边权重
    initLabels() {
        //KM算法要求始终满足：lx[i] + ly[j] ≥ weight[i][j]  (对所有边)初始化策略保证了这一点
        for (let i = 0; i < this.n; i++) {
            this.lx[i] = Math.max(...this.weights[i]);
            this.ly[i] = 0;
        }
        console.log('初始化顶标:', { lx: [...this.lx], ly: [...this.ly] });
    }

//在相等子图中DFS寻找增广路
dfs(x) {
    this.visitedX[x] = true;
    
    for (let y = 0; y < this.n; y++) {
        if (!this.visitedY[y] && this.isFeasibleEdge(x, y)) {
            this.visitedY[y] = true;
            
            // 如果y未被匹配，或者已匹配但可以找到增广路
            if (this.matchY[y] === -1 || this.dfs(this.matchY[y])) {
                this.matchX[x] = y;
                this.matchY[y] = x;
                return true;
            }
        }
    }
    return false;
}
//KM算法的核心判断逻辑
//判断边(x,y)是否在相等子图中
isFeasibleEdge(x, y) {
    return Math.abs(this.lx[x] + this.ly[y] - this.weights[x][y]) < 1e-9;
    //1e-9 = 0.000000001（10的负9次方）就是小数点后面8个0然后一个1//0.000000001
}
/*
①KM在匈牙利基础上维护顶标，用于带权二分图的最大权匹配
②δ就是"最小代价"：用最小的顶标调整，让搜索能够继续下去，找到增广路
δ计算实际上是在确保:用最小代价解决问题,不破坏现有的高价值匹配,找到真正的全局最优
③δ的确定规则:δ调整 = 最小代价的期望调整，让新缘分出现
δ = min{ 所有"访问过的男生i的目标期望值"和"未访问过的女生j的目标期望值"的总和 (lx[i] + ly[j] - weight[i][j]) }当前期望总和比实际心动分数高多少
当这个等式成立时，说明两个人的期望总和正好等于实际感情价值，这样的配对是最"公平"的
weight[i][j] = 男生i对女生j的心动分数
顶标(lx, ly) = 每个人的期望值
④相等子图 = 期望总和正好等于心动分数的缘分边;相等子图边（满足 lx[i] + ly[j] = weight[i][j]）
相等子图就是：在当前期望值下，所有"期望总和等于实际价值"的潜在配对集合//动态的筛选器
完整图:   相等子图:   子图:这是从完整二分图中选出来的一个子集
A-W-X-Y-Z  A-----Y
B-W-X-Y-Z  B---X
C-W-X-Y-Z  C-W
D-W-X-Y-Z  D-----Y
⑤KM算法的局限性:
要求严格：必须是完全二分图（左右节点数相等）,求的是最大权完美匹配
不适合的场景:节点数不相等,只需要最大匹配，不要求完美匹配,权重有负值（需要预处理）
*/
// 调整顶标
adjustLabels() {
    // 找到最小的调整量delta
    let delta = Infinity;
    //计算最小的期望调整量δ,最小要降低多少期望，就能让新的门当户对关系出现
    for (let x = 0; x < this.n; x++) {//外层循环：遍历所有访问过的男生
        if (this.visitedX[x]) {//只考虑参与竞争的男生
            for (let y = 0; y < this.n; y++) {//内层循环：遍历所有未访问的女生
                if (!this.visitedY[y]) { // 只考虑未被追求的女生
                    delta = Math.min(delta, this.lx[x] + this.ly[y] - this.weights[x][y]);
                    //核心计算：期望差值;计算：当前期望总和比实际感情价值高多少➜取最小值,我们要用最小的代价让新的关系出现
                }
            }
        }
    }
    
    console.log(`调整顶标，delta = ${delta}`);
    
    // 调整顶标
    for (let i = 0; i < this.n; i++) {
        if (this.visitedX[i]) this.lx[i] -= delta;
        if (this.visitedY[i]) this.ly[i] += delta;
    }
    //A降低期望的同时Y提高期望//同步调整，既保护现有高质量配对，又为系统重组创造新的可能性
    return delta;
}
// 执行KM算法
solve() {
    //KM算法要找到权重最大的匹配,最大权完美匹配是一个全局优化问题不能只看局部最优,需要不断调整，找到全局最优解,每次调整都可能引发连锁反应
    this.initLabels();
    
    // 为每个左边节点寻找匹配
    for (let x = 0; x < this.n; x++) {//确保每个左边节点都有匹配
        console.log(`\n=== 为左边节点 ${x} 寻找匹配 ===`);
        
        while (true) {//为当前节点x找到匹配（可能需要多次调整）为后面节点找匹配时，可能破坏前面的匹配
            // 重置访问标记
            this.visitedX.fill(false);
            this.visitedY.fill(false);
            
            console.log(`当前匹配状态: X->Y: [${this.matchX}], Y->X: [${this.matchY}]`);
            
            // 在相等子图中寻找增广路
            if (this.dfs(x)) {// 尝试1：在当前相等子图中直接找// 再尝试：在新的相等子图中找
                console.log(`节点 ${x} 匹配成功！`);
                break;
            }
            
            // 如果没有找到增广路，调整顶标
            console.log(`节点 ${x} 未找到匹配，需要调整顶标`);
            const delta = this.adjustLabels();// 尝试失败：调整期望，扩大选择范围// 继续调整...直到成功
            
            console.log(`调整后顶标: lx = [${this.lx}], ly = [${this.ly}]`);
            
            // 如果delta无限大，说明无法找到完美匹配
            if (delta === Infinity) {
                console.log('无法找到完美匹配');
                return null;
            }
        }
    }
    
    return this.getResult();
}

// 获取匹配结果
getResult() {
    const matches = [];
    let totalWeight = 0;
    //1. 收集匹配对,把内部存储的匹配关系转换成人类可读的格式
    for (let x = 0; x < this.n; x++) {
        const y = this.matchX[x];
        if (y !== -1) {
            matches.push({ from: x, to: y, weight: this.weights[x][y] });
            totalWeight += this.weights[x][y];// 计算总权重,累加所有匹配的权重（心动分数总和）

        }
    }
    //返回结果
    return {
        matches: matches,
        totalWeight: totalWeight,
        matchX: [...this.matchX],
        matchY: [...this.matchY]
    };
}
/*
注意:
①在KM算法的DFS中"访问" = 在当前的增广路搜索中实际经过的节点,不是所有节点都会被访问到,只有搜索路径上的节点才会参与顶标调整
开始: D (标记visitedX[D]=true)
    ↓
D找对象 → 找到Y (标记visitedY[Y]=true)
    ↓
Y被A占用 → 递归搜索A (标记visitedX[A]=true)
    ↓
A找新对象 → 没有其他相等边 → 回溯
最终访问集合：visitedX: [A, D] (只有A和D被访问)visitedY: [Y] (只有Y被访问)
DFS从D开始，只沿着相等子图的边搜索,A-Y是相等边从D能走到Y，再从Y走到A,但没有相等边从A连接到B或C，搜索不会到达B和C
②X->Y: [2,1,0,-1] 的含义
这是左边节点匹配右边节点的数组：索引 = 左边节点编号 (0=A, 1=B, 2=C, 3=D),值 = 匹配的右边节点编号 (0=W, 1=X, 2=Y, 3=Z)
具体解读：X[0] = 2 → A匹配Y;X[1] = 1 → B匹配X;X[2] = 0 → C匹配W;X[3] = -1 → D没有匹配
③顶标调整 ≠ 自动重新匹配//虽然顶标调整了，但匹配关系还没有更新//KM算法是逐步试探、逐步优化的过程
调整顶标只是创造了新的可能性，但不会自动改变现有匹配
console.log在调整顶标之后、下一次DFS之前调用，显示的是调整前的匹配状态;在第四次DFS中，算法应该能利用新的相等边（特别是D-Z）找到匹配
*/
}
// 测试我们的算法
function testKM() {
    //使用我们的婚恋市场案例
    const weights = [
        [8, 5, 9, 2],  //列abcd,行wxyz
        [4, 7, 6, 3],  
        [9, 8, 7, 4],  
        [6, 6, 8, 5]  
    ];
    
    console.log('权重矩阵:');
    weights.forEach((row, i) => {
        console.log(`节点${i}: [${row.join(', ')}]`);
    });
    
    const km = new KMAlgorithm(weights);
    const result = km.solve();
    
    console.log('\n🎉 最终匹配结果:');
    result.matches.forEach(match => {
        console.log(`左边${match.from} → 右边${match.to}, 权重: ${match.weight}`);
    });
    console.log(`总权重: ${result.totalWeight}`);
    
    return result;
}

// 运行测试
testKM();

function runRobustnessTests() {
    console.log("🧪 开始KM算法健壮性测试...\n");
    
    const testCases = [
        {
            name: "测试1: 全零矩阵",
            weights: [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        },
        {
            name: "测试2: 包含负值",
            weights: [
                [-1, 2, 3],
                [4, -5, 6],
                [7, 8, -9]
            ]
        },
        {
            name: "测试3: 单一元素",
            weights: [[5]]
        },
        {
            name: "测试4: 完全匹配",
            weights: [
                [10, 0, 0],
                [0, 10, 0],
                [0, 0, 10]
            ]
        },
        {
            name: "测试5: 大数值差异",
            weights: [
                [1, 1000],
                [1000, 1]
            ]
        }
    ];
    
    testCases.forEach((testCase, index) => {
        console.log(`📝 ${testCase.name}`);
        try {
            const km = new KMAlgorithm(testCase.weights);
            const result = km.solve();
            
            if (result && validateResult(result, testCase.weights)) {
                console.log("✅ 测试通过");
                console.log(`   匹配结果: ${JSON.stringify(result.matches)}`);
                console.log(`   总权重: ${result.totalWeight}\n`);
            } else {
                console.log("❌ 结果验证失败\n");
            }
        } catch (error) {
            console.log(`💥 测试异常: ${error.message}\n`);
        }
    });
}

function validateResult(result, weights) {
    // 检查是否完美匹配
    const n = weights.length;
    const matchedX = new Set();
    const matchedY = new Set();
    
    for (const match of result.matches) {
        // 检查匹配是否有效
        if (match.from < 0 || match.from >= n || 
            match.to < 0 || match.to >= n) {
            return false;
        }
        
        // 检查是否有重复匹配
        if (matchedX.has(match.from) || matchedY.has(match.to)) {
            return false;
        }
        
        matchedX.add(match.from);
        matchedY.add(match.to);
    }
    
    return matchedX.size === n && matchedY.size === n;
}

// 运行测试
runRobustnessTests();

class KMStressTester {
    constructor() {
        this.maxSize = 0;
        this.performanceLog = [];
    }

    // 生成随机权重矩阵
    generateRandomMatrix(size) {
        const matrix = [];
        for (let i = 0; i < size; i++) {
            const row = [];
            for (let j = 0; j < size; j++) {
                row.push(Math.floor(Math.random() * 100) + 1); // 1-100的随机权重
            }
            matrix.push(row);
        }
        return matrix;
    }

    // 性能测试
    async performanceTest(maxTestSize = 500, step = 50) {
        console.log('🚀 开始KM算法性能极限测试\n');
        
        for (let size = step; size <= maxTestSize; size += step) {
            try {
                console.log(`测试 ${size} × ${size} 矩阵...`);
                
                const weights = this.generateRandomMatrix(size);
                const km = new KMAlgorithm(weights);
                
                // 测量执行时间
                const startTime = performance.now();
                const result = km.solve();
                const endTime = performance.now();
                const executionTime = (endTime - startTime) / 1000;
                
                if (result && this.validateResult(result, size)) {
                    this.performanceLog.push({
                        size: size,
                        time: executionTime,
                        status: '成功',
                        memory: this.getMemoryUsage()
                    });
                    
                    console.log(`✅ ${size}×${size} - 耗时: ${executionTime.toFixed(2)}秒`);
                    this.maxSize = size;
                    
                    // 如果执行时间超过30秒，停止测试
                    if (executionTime > 30) {
                        console.log('⏰ 执行时间过长，停止测试');
                        break;
                    }
                } else {
                    console.log(`❌ ${size}×${size} - 匹配失败`);
                    break;
                }
                
                // 避免浏览器卡死，添加延迟
                await this.delay(100);
                
            } catch (error) {
                console.log(`💥 ${size}×${size} - 错误: ${error.message}`);
                break;
            }
        }
        
        this.printSummary();
    }


    // 验证结果
    validateResult(result, expectedSize) {
        if (!result.matches || result.matches.length !== expectedSize) {
            return false;
        }
        
        const matchedX = new Set();
        const matchedY = new Set();
        
        for (const match of result.matches) {
            if (matchedX.has(match.from) || matchedY.has(match.to)) {
                return false; // 重复匹配
            }
            matchedX.add(match.from);
            matchedY.add(match.to);
        }
        
        return matchedX.size === expectedSize && matchedY.size === expectedSize;
    }

    getMemoryUsage() {
        // 注意：浏览器中memory usage API有限制
        if (performance.memory) {
            return `${Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)}MB`;
        }
        return 'N/A';
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    printSummary() {
        console.log('\n📊 测试总结');
        console.log('=' .repeat(40));
        console.log(`🏆 目前最大成功矩阵: ${this.maxSize} × ${this.maxSize}`);
        console.log('\n性能记录:');
        this.performanceLog.forEach(log => {
            console.log(`  ${log.size}×${log.size}: ${log.time.toFixed(2)}秒 ${log.memory ? `(${log.memory})` : ''}`);
        });
        
        // 预测更大规模的性能
        if (this.performanceLog.length >= 2) {
            const last = this.performanceLog[this.performanceLog.length - 1];
            const first = this.performanceLog[0];
            const timeComplexity = last.time / first.time;
            const sizeRatio = last.size / first.size;
            
            console.log(`\n📈 时间复杂度趋势: O(n^${(Math.log(timeComplexity) / Math.log(sizeRatio)).toFixed(1)})`);
        }
    }
}

//运行测试
function runStressTest() {
    const tester = new KMStressTester();
    
    // 性能测试
    console.log('===渐进式性能测试 ===');
    tester.performanceTest(200, 50); // 测试到200×200，每次增加50
    
    
}

// 立即运行测试
runStressTest();
```