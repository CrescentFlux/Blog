# LSH局部敏感哈希
## **基础知识**
- **定义**
```
局部敏感哈希是一种特殊的哈希技术，核心思想是相似的输入在概率上会产生相似的哈希值,与传统哈希的"微小变化导致完全不同的哈希值"不同;LSH故意设计成：相似向量 → 高概率产生相同/相似的哈希值;不相似向量 → 低概率产生相同/相似的哈希值;通过概率性保证来换取搜索效率的指数级提升,核心价值：将高维空间中的相似性搜索问题，转化为低维空间中的哈希表查找问题，实现从O(N)到近似O(1)的跨越
```
- **LSH 查询：给定查询向量 q ∈ R^d 和局部敏感哈希索引 L，相似性搜索过程：**
```
执行步骤
    候选集初始化
        创建空候选集 C = ∅
    多哈希表并行查询
        对于每个哈希表 Ti ∈ {T1, T2, ..., TL}：
        a. 计算查询向量的哈希值：hi = Hi(q)
        b. 检索对应哈希桶：Bi = Ti[hi]
        c. 将桶中所有向量ID加入候选集：C = C ∪ Bi
    结果后处理
        对候选集 C 进行去重
        可选：按精确相似度对候选排序
        返回前 k 个最相似的候选向量
数学表达：C = ∪_{i=1}^{L} Ti[Hi(q)]
时间复杂度分析
    哈希计算：O(L·d) - 与哈希表数量 L 和维度 d 相关
    桶检索：O(L) - 常数时间哈希表查找
    总体复杂度：O(L·d) - 与数据库大小无关
关键特性
    概率完备性：通过多个独立哈希表提高召回率
    P(找到最近邻) = 1 - (1 - P1)^L
    其中 P1 是单个哈希表的命中概率
    近似保证：返回 (1+ε)-近似最近邻
    亚线性查询：查询时间与数据库规模呈亚线性关系
```

- **LSH vs 传统树结构索引**

|维度	|LSH索引|	树结构索引 (B树/K-D树)|
---|---|---
|高维表现	|性能稳定，专为高维优化	|维度灾难，性能退化|
|搜索类型|	近似最近邻搜索	|精确最近邻搜索|
|查询速度|	O(1) 哈希查找	|O(log N) 树遍历|
|数据更新|	批量重建更高效	|支持动态更新|
|结果保证|	概率性保证召回率	|确定性保证精度|


- **LSH vs 传统哈希**

|特性|	局部敏感哈希 (LSH)	|传统哈希 (如MD5, SHA)|
---|---|---
|设计目标	|相似输入 → 相似输出|	相似输入 → 完全不同输出|
|冲突处理	|利用冲突来检测相似性	|极力避免冲突|
|应用场景|	相似性搜索、推荐系统|	数据完整性校验、加密|
|输出稳定性|	概率性稳定（随机超平面）	|确定性稳定|
|核心价值|	搜索效率	|数据安全|


## **注意事项**
1. **混淆点**

- **重建 vs 批量插入的区别**

|操作|	目的|	改变什么	|不改变什么|解决的问题|
---|---|---|---|---
|批量插入|	添加新数据，使用原有的超平面标准，只是增加更多数据到现有桶中	|索引内容|	评估标准(超平面)|高效地添加数据到现有架构|
|重建索引	|优化性能，重新设计整个架构，生成全新的超平面标准，用新标准重新组织所有数据  |	评估标准 + 索引结构|原始数据|优化架构本身以适应数据变化|



- **静态方法 vs 实例方法的区别**

|特性	|静态方法|	实例方法|
---|---|---
|调用方式	|类名.方法名()	|实例.方法名()|
|访问数据|	|不能访问this	|可以访问this.属性|
|存储状态|	无状态	|有状态（存储数据）|
|使用场景|	工具函数、计算|	实际操作、数据处理|




2. 代码实现
```
class LSH {
    constructor(dimensions, numTables = 10, hashLength = 10) {
        this.dimensions = dimensions;//向量的维度数
        this.numTables = numTables;//哈希表的数量//多个哈希表：概率提升，参数选择的经验法则
        this.hashLength = hashLength;//每个哈希值的位数（划分的精细程度//生成多少个判断标准//每个标准当中随机哈希值的个数//一个标准 = 一个问题 = 哈希值的一个位//多个标准 = 多个问题 = 完整的哈希值//✅ 可调节的精细度：通过hashLength控制，✅ 概率相似性：相似向量回答相似，哈希值相似，✅ 高效比较：比较二进制串比比较浮点向量快得多
        this.tables = []; //长度为numTables的数组，每个元素是一个哈希表
        this.planesList = []; //长度为numTables的数组，每个元素是一组超平面法向量
        //法向量定义方向 → 点积符号判断在哪侧 → 0/1记录位置 → 多个超平面组成哈希值
        //空间换时间,批处理优化,预处理//接受某些操作的复杂性（避免删除）,接受预处理开销（先构建后查询）,换取查询时的极致性能
        this.vectorMap = new Map();  // ✅必须初始化 vectorMap！

        // 1.初始化哈希表
        for (let i = 0; i < numTables; i++) {
            this.tables.push({});
            // 1: 生成随机超平面法向量
            this.planesList.push(this.generateRandomPlanes(dimensions, hashLength));
        }
    }
    // 2:生成随机超平面法向量
    generateRandomPlanes(dim, numPlanes) {//从各个随机方向来观察向量的相似性
        const planes = [];
        for (let i = 0; i < numPlanes; i++) {//生成numPlanes个随机问题
            const plane = [];
            for (let j = 0; j < dim; j++) {// 每个问题是dim维的
                // 3: 生成随机数，通常使用正态分布
                //均匀分布生成的点：偏向立方体角落，向量长度变化很大，方向分布不均匀；正态分布生成的点：在所有方向上均匀分布// 正态分布向量更关注方向而不是长度
                //在生成能够均匀覆盖所有可能方向的测试问题，这样才能公平地检测向量的相似性
                plane.push(this.generateRandomNumber());// 随机生成问题的方向角度
            }
            planes.push(plane);
        }
        return planes;
    }
    // 3.生成随机数（标准正态分布）
    generateRandomNumber() {
        //使用Box-Muller变换生成正态分布随机数// Box-Muller变换：将均匀分布转为正态分布//利用极坐标变换把均匀分布加工成正态分布
        //在二维正态分布中，点离原点的距离平方恰好服从指数分布//二维正态分布在极坐标下有简单形式
        //Math.random()生成 [0,1) 的均匀分布：均值 = 0，标准差 = 1，形状是完美的钟形曲线
        let u = 0, v = 0;//v：来自 Math.random()，范围是 [0, 1)；给出一个"比例"，表示"占整个圆的多少"；v从0到1，均匀地扫过整个圆周
        while(u === 0) u = Math.random();
        while(v === 0) v = Math.random();
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
        //Math.log(u)把均匀分布变成"指数分布"的形状，-2.0 * Math.log(u)调整参数，为下一步做准备，Math.sqrt(-2.0 * Math.log(u))开平方根，这会产生径向距离的效果
        //Math.cos(2.0 * Math.PI * v)生成随机角度（余弦函数在0到2π间均匀分布），相乘：距离 × 角度 = 极坐标到直角坐标的转换
        //距离 = Math.sqrt(-2.0 * Math.log(u))；角度 = 2.0 * Math.PI * v；
        // x = 距离 * cos(角度)  //正态分布随机数；y = 距离 * sin(角度)//实际上我们得到两个正态分布数
        //极坐标(𝑟,𝜃)来表示点：角度𝜃应该是[0,2π]的均匀分布，半径𝑟需要满足特定的分布才能得到正态分布；
        //要使(x,y)成为标准正态分布，半径𝑟必须满足：P(半径 < R) = 1 - e^(-R²/2)//半径的平方(𝑟²)服从指数分布
        //-log(u)就是指数分布；-2.0 * Math.log(u)，生成的是均值为2的指数分布，标准正态分布的半径平方恰好是均值为2的指数分布；对半径平方开方，得到真正的半径𝑟
        //在二维平面上，一个完整的圆是360度 = 2π 弧度；Math.PI：π ≈ 3.14159，半个圆的弧度；2.0 * Math.PI：完整的圆 = 2π ≈ 6.28318 弧度
        //v 是均匀分布在 [0,1) 的；乘以 2π 后，角度均匀分布在 [0, 2π)；每个角度出现的概率相等//把一个均匀分布的随机数 v 转换成在圆周上均匀分布的角度，确保我们的随机方向没有偏见，覆盖所有可能的方向
        //概率论变量变换公式：𝑢, 𝑣 是独立的均匀分布：𝑟 = √(-2ln𝑢)；𝜃 = 2π𝑣 ：𝑥 = 𝑟cos𝜃 和 𝑦 = 𝑟sin𝜃 是独立的标准正态分布
        //二维标准正态分布的联合概率密度：f(x,y) = (1/2π) * e^(-(x²+y²)/2)；在极坐标下，𝑥²+𝑦² = 𝑟²：f(𝑟,𝜃) = (1/2π) * 𝑟 * e^(-𝑟²/2)：半径𝑟的分布确实包含指数项 e^(-𝑟²/2)
    }
    
    // 4: 计算单个哈希表的哈希值//随机投影 + 二值化//
    //把复杂的向量相似性转化为简单的二进制串比较//
    //进行一场方向比较：让多个随机超平面从不同方向检测向量的朝向，根据向量的位置回答'1'或'0'，最终组合成一个二进制签名；相似向量会给出相似的答案序列
    computeHash(vector, planes) {
        //vector 是特征空间中的一个点：vector = [v₁, v₂, v₃, ..., vₙ]；每个维度代表一个特征：// 每个 plane 定义一个超平面的法向量：plane = [p₁, p₂, p₃, ..., pₙ]：p₁*x₁ + p₂*x₂ + ... + pₙ*xₙ = 0
        //vector 就是一个数据的数学表示，vector可以是一个点或者一个箭头，// planes 是一组随机方向，用来划分空间
        let hash = '';
           // 计算向量在平面法向量方向上的投影分量
           // 投影分量 > 0：在法向量指向的那侧；投影分量 < 0：在相反侧；投影分量 = 0：正好在超平面上//点积的几何意义：某个向量在法向量方向上的影子长度；
        for (const plane of planes) {
            // 5: 计算点积
            const dotProduct = this.dotProduct(vector, plane);
            // 6: 根据点积符号决定哈希位//判断向量在超平面的哪一侧//投影程度 >= 0) {hash += '1';// 在正面hash += '0';//在负面}
            hash += dotProduct >= 0 ? '1' : '0';
        }
        return hash;//相似向量：会有相似的哈希签名；哈希组合：多个二进制位组成最终签名；0/1决策：根据点积符号给出二进制结果；多个超平面：每个从随机方向评估向量
    }
    
    // 4.1: 计算点积
    dotProduct(v1, v2) {
        let result = 0;
        for (let i = 0; i < v1.length; i++) {
            // 1: 点积计算公式
            result += v1[i] * v2[i]; // 对应维度相乘；对应维度相乘后累加求和//v1ₙ×v2ₙ = v1₁×v2₁ + v1₂×v2₂ + v1₃×v2₃ + ... + v1ₙ×v2ₙ
        }
        return result;
    }
    // 5.插入向量到LSH索引//概率分桶//阶段1：构建索引（预处理）
    //LSH的插入是概率性分桶，不是确定性排序//为搜索优化，而不是为频繁更新优化
    //多重备份，概率保证
    // 只是计算哈希值，放入对应的桶//各个桶之间完全独立//优势：桶之间相互独立，无全局约束//并行处理多个插入操作:而传统树结构需要维护全局有序性，每次插入都可能影响整个结构，难以批量优化
    insert(vector, id) {
        //✅存储向量到vectorMap
        this.vectorMap.set(id, vector);
        // LSH：插入的是向量到哈希桶的映射，传统B树：插入单个记录
        for (let i = 0; i < this.numTables; i++) {//遍历所有超平面；每个新的向量需要在所有超平面位置处都登记
            const planes = this.planesList[i];
            // 1: 计算哈希值
            const hash = this.computeHash(vector, planes);
            if (!this.tables[i][hash]) {
                this.tables[i][hash] = [];// 创建新的档案袋
            }
            // 2: 将ID添加到对应的哈希桶
            this.tables[i][hash].push(id);// 放进对应档案袋
            //为每个向量建立多重身份档案：让它在多个不同的评分体系中都留下记录，这样查询时只要在任何一个体系中匹配成功，就能找到相似的候选//多维度比较：多维度发现隐藏的相似性，避免"维度偏见"，均衡的多维度覆盖//不断变换观察角度，多角度拼出完整画面//多个哈希表 = 多个观察维度 = 多角度全面评估
        }
    }
    //6.快速查询相似向量// 桶查找 // 阶段2：执行查询（快速检索）
    //亚线性时间搜索//O(N)的搜索问题变成了O(1)的哈希表查找//LSH：相似性搜索（近似匹配）
    query(vector, maxResults = 10) {
        const candidates = new Set();//1.准备一个向量收集器
        
        for (let i = 0; i < this.numTables; i++) {
            const planes = this.planesList[i]; // 2.找到第i个超平面
            const hash = this.computeHash(vector, planes);// 3.进行比较得到当前向量在这个超平面的哈希值
            
            //4.获取向量收集器里哈希值相同的所有向量并且收集id
            const bucket = this.tables[i][hash] || [];
            //5.把获取到的所有相似向量放到收集器里
            for (const id of bucket) {
                candidates.add(id);
            }
        }
         // 6. 精确重排序（计算真实相似度）
        const sortedCandidates = Array.from(candidates)
            .map(id => ({
                id: id,
                similarity: this.exactSimilarity(vector, this.getVector(id))
            }))
            .sort((a, b) => b.similarity - a.similarity); // 按相似度降序
        
        // 7: 返回前N个相似向量数据集（实际应用中会进一步精确排序）//LSH返回的候选集是"近似相似"的，需要进一步筛选
        return Array.from(candidates).slice(0, maxResults);//结果限制和优化：从候选集中取出前 maxResults 个结果//性能考虑，用户体验，资源节约
    }
    // 新增：获取向量方法
    getVector(id) {
        return this.vectorMap.get(id);
    }
    // 新增：精确相似度计算
    exactSimilarity(v1, v2) {
        // 余弦相似度
        const dot = this.dotProduct(v1, v2);
        const norm1 = Math.sqrt(this.dotProduct(v1, v1));
        const norm2 = Math.sqrt(this.dotProduct(v2, v2));
        return dot / (norm1 * norm2);
    }
    //----基础理论---//
        //LSH 概念//
    //第一部分：基本概念
        //传统哈希函数的设计目标是：相似的输入产生精确的哈希值
        //LSH的设计目标是：相似的输入产生相似的哈希值
        //LSH通过牺牲精确来换取查询效率的大幅提升
        //在512维空间中，直接计算所有向量的相似度需要100万 × 512 = 5.12亿次运算次运算（对于100万数据）
    //第二部分：核心机制
        //LSH使用随机超平面来划分高维空间
        //每个随机超平面由一个法向量定义
        //对于向量v和超平面法向量r，计算点积 r·v（不是夹角，夹角是结果）判断v在超平面的哪一侧
        //如果r·v ≥ 0，则哈希位为r·v ≥ 0 → 1；如果r·v < 0，则哈希位为r·v < 0 → 0
    //第三部分：概率基础
        //两个向量夹角越小，它们在随机超平面同侧的概率越大
        //数学上，P(同侧) = P(同侧) = 1 - θ/π
        //当两个向量夹角为90度时，同侧概率为50%
        //当两个向量完全同向时，同侧概率为100%
    //第四部分：工程实现
        //使用多个随机超平面可以生成一个生成二进制位的哈希签名位的哈希签名
        //构建多个哈希表可以提高召回率
        // 查询时只需要搜索哈希桶中的向量
        //LSH把O(N)的搜索问题变成了O(1)的查找问题
    //第五部分：应用场景
        //LSH特别适合高维数据的相似性搜索
        //在图片搜索中，LSH比较的是图片的特征相似性而非像素相似性
        //LSH能够有效避免查询效率低问题
        //与K-D树相比，LSH在高维空间中的效率更高
    //----🎯注意----//
    //Uncaught TypeError: can't access property "get", this.vectorMap is undefined：this.vectorMap 没有在构造函数中初始化//在构造函数中初始化 this.vectorMap = new Map()
}
//--测试--//
const lsh = new LSH(512, 10, 12); // 512维，10个哈希表，每个12位哈希
//1.创建LSH实例
const vectors = [
    {id: 'img1', vector: [0.1, 0.2, /*...512个值*/]},
    {id: 'img2', vector: [0.15, 0.18, /*...*/]},
    // ...更多数据
];
//2.构建索引
console.log('插入数据...');
for (const item of vectors) {
    lsh.insert(item.vector, item.id);
    console.log(`插入: ${item.id}`, item.vector);
}
//3.查询
console.log('\n查询相似向量...');
const queryVector = [0.12, 0.19, /*...*/];
const results = lsh.query(queryVector, 5);
console.log('找到相似图片:', results);
//4.查看哈希表结构
console.log('\n哈希表结构:');
console.log(lsh.tables);
console.log('查询向量:', queryVector);
console.log('找到的相似向量:', results);

//============================批处理实现===========================//
class SmartLSH {
    constructor(dimensions, numTables = 10, hashLength = 10) {
        this.dimensions = dimensions;
        this.numTables = numTables;
        this.hashLength = hashLength;
        this.tables = [];
        this.planesList = [];
        this.vectorMap = new Map();
        this.dataCount = 0; //跟踪数据量用于重建判断
        //放弃精确的全局有序性，换来批量处理的高效性
        //✅智能重建所需参数：
        this.lastRebuildCount = 0;      // 上次重建时的数据量，记录上一次重建索引时的数据总量，用来计算自上次重建后新增了多少数据
        this.rebuildThreshold = 1000;   // 重建阈值：触发重建的数据增长量阈值，当新增数据超过这个数量时，自动重建索引  
        this.maxQueryTime = 20;         // 最大允许查询时间：查询操作的性能红线：如果平均查询时间超过这个值，说明索引性能下降，需要重建
        this.queryTimes = [];           // 查询时间记录：存储最近查询的耗时记录，用于计算平均查询时间，监控性能趋势，避免内存无限增长
        this.initializeTables();
    }
    
    initializeTables() {
        //LSH的多角度评估系统:多个哈希表/多个独立评估框架，每个表的随机超平面/每个团队的评估标准，初始化空表/准备空白记录板
        for (let i = 0; i < this.numTables; i++) {
            this.tables.push({});//数组存储多个哈希表，而不是单个变量//this.tables 本身就是一个数组，里面的每个元素 this.tables[i] 就是一个独立的哈希表！//✅这就是哈希表的初始化！在JS中，空对象 {} 就是一个功能完整的哈希表，不需要额外的初始化步骤。
            this.planesList.push(this.generateRandomPlanes(this.dimensions, this.hashLength));  // 生成i个随机方向（i个超平面）
        }
    }
    // ✅ 1. 生成随机超平面
    generateRandomPlanes(dim, numPlanes) {
        const planes = [];
        for (let i = 0; i < numPlanes; i++) {
            const plane = [];
            for (let j = 0; j < dim; j++) {
                // 生成随机数，范围: [-1, 1]
                plane.push((Math.random() - 0.5) * 2);
            }
            planes.push(plane);
        }
        return planes;
    }
    // ✅ 2. 计算点积
    dotProduct(v1, v2) {
        let result = 0;
        for (let i = 0; i < v1.length; i++) {
            result += v1[i] * v2[i];
        }
        return result;
    }
    // ✅ 3. 计算哈希值
    computeHash(vector, planes) {
        let hash = '';
        for (const plane of planes) {
            const dotProduct = this.dotProduct(vector, plane);
            hash += dotProduct >= 0 ? '1' : '0';
        }
        return hash;
    }
    // ✅ 4. 初始化表
    initializeTables() {
        for (let i = 0; i < this.numTables; i++) {
            this.tables.push({});
            this.planesList.push(this.generateRandomPlanes(this.dimensions, this.hashLength));
        }
    }
    //✅ 5. 单个插入
    insert(vector, id) {
        this.vectorMap.set(id, vector);
        
        for (let i = 0; i < this.numTables; i++) {
            const planes = this.planesList[i];
            const hash = this.computeHash(vector, planes); // 
            
            if (!this.tables[i][hash]) {
                this.tables[i][hash] = [];
            }
            this.tables[i][hash].push(id);
        }
        //---动态维护策略---//
        this.dataCount++;// 跟踪数据总量
        this.checkRebuild();  // 检查是否需要重建索引
        //重建索引：随着数据增加，随机超平面可能不再最优，导致某些桶过大，某些桶过小；查询性能下降：大桶：需要精确比较的候选太多；小桶：召回率降低
        //重建的成本：重建成本 = O(N × L × d) ；N个数据，L个哈希表，d维度//不重建的成本：//查询成本增长 = O(桶大小)；桶会越来越大//智能策略：在适当的时候付出重建成本，换取长期查询性能
        //前瞻性：不是等到系统变慢才处理，而是主动预防性能退化
    }
    //✅ 6. 批量插入
    //===批处理插入===//
    //🎯计算与存储分离，映射关系层层传递//先计算所有映射关系，再批量构建索引//
    //一次性构建完整的索引结构：计算哈希值确定索引位置//索引位置 = 哈希值，索引结构 = 哈希表（哈希值到向量的映射），批处理 = 一次性构建完整的索引结构，查询 = 根据索引位置快速定位相似数据
    batchInsertOptimized(vectors) {
        //按表批量处理"：先集中为表0计算所有向量的哈希值，再为表1计算所有向量的哈希值
        console.log("🔄 真正的批处理预处理...");
        // 阶段1: 批量计算所有哈希值（一次性）//哈希表 ⇄ 哈希值对应//（计算逻辑）
        //✅计算模式优化；✅缓存友好：连续处理同一表的标准，更好的CPU缓存利用率，批量计算，可能触发编译器的向量化优化
        const allHashes = [];
        for (let tableIdx = 0; tableIdx < this.numTables; tableIdx++) {//外层循环：遍历所有哈希表，为每个哈希表准备数据
            const tableHashes = [];//初始化当前表的哈希值数组
            const planes = this.planesList[tableIdx];//拿到当前哈希表的"面试官标准"
            // 先分组，再批量操作//内层循环：为所有向量计算哈希值
            for (const {vector} of vectors) {
                const hash = this.computeHash(vector, planes);
                tableHashes.push(hash);//一次性为所有向量在当前表中计算哈希值
            }
            allHashes.push(tableHashes);//存储当前表的所有哈希值，把当前表的所有哈希值保存到总数组中
            
        }
        // 阶段2: 批量构建索引（一次性）//数据 ⇄ 桶对应//（存储逻辑）
        //把之前计算好的哈希值批量写入到实际的索引结构中
        // 对每个哈希表..
        for (let tableIdx = 0; tableIdx < this.numTables; tableIdx++) {
            // 对每个向量..// 一次性写入哈希表
            for (let i = 0; i < vectors.length; i++) {
                const hash = allHashes[tableIdx][i];
                const id = vectors[i].id;
                // 构建索引结构
                if (!this.tables[tableIdx][hash]) {
                    this.tables[tableIdx][hash] = [];// 创建新桶
                }
                this.tables[tableIdx][hash].push(id);// 把ID放入对应桶
            }
        }
        this.dataCount += vectors.length;
        console.log(`✅ 批处理完成，新增 ${vectors.length} 个向量`);
}
    // ✅ 7. 重建检查
    //====重建检查====//
    checkRebuild() {
        const growth = this.dataCount - this.lastRebuildCount;  // 计算数据增长量//✅智能触发//
        // 策略1：数据量增长触发
        if (growth >= this.rebuildThreshold) {//growth - 数据增长量，rebuildThreshold - 重建阈值
            console.log(`数据增长 ${growth}，触发重建`);
            this.rebuildIndex();
            return;
        }
        // 策略1：定期重建（每rebuildInterval次插入后）
        //if (this.dataCount % this.rebuildInterval === 0) {
            //this.rebuildIndex();
            //return;
        //}
        // 策略2：性能触发重建
        const stats = this.getPerformanceStats();
        if (stats.avgBucketSize > this.maxBucketSize) {
            console.log('检测到桶过大，触发重建...');
            this.rebuildIndex();
        }
    }
    //✅记录查询时间的方法
    recordQueryTime(time) {
        this.queryTimes.push(time);
        // 只保留最近100次查询时间
        if (this.queryTimes.length > 100) {
            this.queryTimes.shift();
        }
    }
    //✅计算平均查询时间
    getAverageQueryTime() {
        if (this.queryTimes.length === 0) return 0;
        const sum = this.queryTimes.reduce((a, b) => a + b, 0);
        return sum / this.queryTimes.length;
    }
    // ✅ 8. 重建索引
    //---重建索引---//
    rebuildIndex() {
        //避免哈希碰撞累积，数据特征变化，重新分桶，减少误匹配
        console.log('开始重建索引...');
        const allVectors = Array.from(this.vectorMap.entries());
        
        // 清空现有索引
        this.tables = [];
        // 关键步骤：重新生成随机标准！
        this.initializeTables(); //重新初始化表// ← 这里会生成新的随机超平面
        
        // 重新插入所有数据// 然后用新标准重新分桶
        for (const [id, vector] of allVectors) {
            for (let i = 0; i < this.numTables; i++) {
                const hash = this.computeHash(vector, this.planesList[i]); // 新标准！
                if (!this.tables[i][hash]) {
                    this.tables[i][hash] = [];
                }
                this.tables[i][hash].push(id);
            }
        }
        //✅更新重建计数器
        this.lastRebuildCount = this.dataCount;
        console.log('索引重建完成');
        console.log('索引重建完成');
    }
     //✅添加 query 方法
    query(vector, maxResults = 10) {
        const candidates = new Set();
        
        for (let i = 0; i < this.numTables; i++) {
            const planes = this.planesList[i];
            const hash = this.computeHash(vector, planes);
            const bucket = this.tables[i][hash] || [];
            
            for (const id of bucket) {
                candidates.add(id);
            }
        }
        
        const candidateArray = Array.from(candidates);
        return candidateArray.slice(0, maxResults);
    }
    // ✅ 9. 性能统计
    getStats() {
        let totalBuckets = 0;
        let maxBucketSize = 0;
        let emptyBuckets = 0;
        
        for (const table of this.tables) {
            const buckets = Object.values(table);
            totalBuckets += buckets.length;
            emptyBuckets += (Math.pow(2, this.hashLength) - buckets.length);
            
            for (const bucket of buckets) {
                maxBucketSize = Math.max(maxBucketSize, bucket.length);
            }
        }
        
        const avgBucketSize = this.dataCount / totalBuckets;
        const totalPossibleBuckets = Math.pow(2, this.hashLength) * this.numTables;
        
        return {
            数据总量: this.dataCount,
            哈希表数量: this.numTables,
            总桶数: totalBuckets,
            平均桶大小: Number(avgBucketSize.toFixed(2)),
            最大桶大小: maxBucketSize,
            空桶率: Number((emptyBuckets / totalPossibleBuckets).toFixed(2))
        };
    }
    
    // ✅ 10. 查询方法
    query(vector, maxResults = 10) {
        const candidates = new Set();
        
        for (let i = 0; i < this.numTables; i++) {
            const planes = this.planesList[i];
            const hash = this.computeHash(vector, planes);
            const bucket = this.tables[i][hash] || [];
            
            for (const id of bucket) {
                candidates.add(id);
            }
        }
        
        const candidateArray = Array.from(candidates);
        return candidateArray.slice(0, maxResults);
    }
    
    // ✅ 11. 自适应调整
    adaptiveAdjust() {
        const stats = this.getStats();
        
        if (stats.平均桶大小 > 100) {
            this.hashLength = Math.min(20, this.hashLength + 1);
            console.log(`检测到桶过大，增加哈希长度至: ${this.hashLength}`);
            this.rebuildIndex();
        } else if (stats.空桶率 > 0.8) {
            this.hashLength = Math.max(8, this.hashLength - 1);
            console.log(`检测到空桶过多，减少哈希长度至: ${this.hashLength}`);
            this.rebuildIndex();
        }
    }
}
//--完成测试--//
// 测试数据
const vectors1 = [
    { id: '猫图片1', vector: [0.8, 0.6, 0.1, 0.9] },
    { id: '猫图片2', vector: [0.7, 0.5, 0.2, 0.8] },
    { id: '狗图片1', vector: [0.2, 0.9, 0.8, 0.1] }
];
// 创建实例
const lsh1 = new SmartLSH(4, 2, 3);
console.log('=== 开始测试 ===');
// 批量插入
lsh1.batchInsertOptimized(vectors1);
// 查看性能统计
const stats = lsh1.getStats();
console.log('性能统计:', stats);
// 测试查询
const results1 = lsh1.query([0.78, 0.58, 0.12, 0.88], 3);
console.log('查询结果:', results1);
console.log('=== 测试完成 ===');
// OptimizedLSH 只关心：如何计算最优参数
// 输入：维度、数据量、召回率要求
// 输出：最优参数
// smartLSH 只关心：如何执行LSH操作
// 输入：数据向量
// 输出：相似结果
//研究战略，制定方案（静态方法）
//根据方案，实际作战（实例方法）

//============================参数优化============================//
class OptimizedLSH {//参数顾问（静态类）
    //static表示这是一个类方法，而不是实例方法：静态方法通过类直接调用//实例方法：通过实例调用//参数推荐器//
    //✅只负责计算参数，不存储状态//
    static recommendParams(dimensions, expectedDataSize, baseRecall=null,desiredRecall = 0.95) { //自动调参方法
        // 基于理论和经验的参数选择:
        // 🎯注意不要重复声明变量：Uncaught SyntaxError: redeclaration of formal parameter baseRecall
        // 根据数据规模调整基础召回率:
            /*let baseRecall;// ❌ 这里重复声明了！直接使用传入的 baseRecall 参数
            if (expectedDataSize < 1000) {
                baseRecall = 0.7; // 小数据集
            } else if (expectedDataSize < 100000) {
                baseRecall = 0.5; // 中等数据集
            } else {
                baseRecall = 0.3; // 大数据集
            }*/

        //如果没传 baseRecall，才自动推断
        //✅智能推断：如果没提供 baseRecall，才自动计算
            if (baseRecall === null) {
                if (expectedDataSize < 1000) {
                    baseRecall = 0.7;
                } else if (expectedDataSize < 100000) {
                    baseRecall = 0.5;
                } else {
                    baseRecall = 0.3;
                }
            }
        //期望召回率 desiredRecall,单个表召回率 baseRecall 
        const numTables = Math.ceil(Math.log(1 - desiredRecall)/Math.log(1 - baseRecall)); //哈希表数量的计算
        const hashLength = Math.max(8, Math.ceil(Math.sqrt(dimensions) * 2)); //哈希长度的计算
        // 部分1：基于维度的基础计算，Math.ceil(Math.sqrt(dimensions) * 2)//含义：哈希长度与维度平方根成正比
        // 部分2：最低保障值Math.max(8, ...)//含义：无论如何，哈希长度至少8位
        console.log(`推荐参数: ${numTables}个哈希表, ${hashLength}位哈希长度`);
        return { numTables, hashLength };//
        //numTables 的计算基于召回率公式：P(找到最近邻) = 1 - (1 - P₁)^L，P₁是单个表的命中概率，L是表数量，推导出：L = ceil( log(1 - 期望召回率) / log(1 - P₁) )
        // 回忆率公式：P(找到) = 1 - (1 - P₁)^L
                // 其中：P₁是单个表的命中概率，L是表数量:
                //  L：// 1 - (1 - P₁)^L = desiredRecall
                // (1 - P₁)^L = 1 - desiredRecall
                // L = log(1 - desiredRecall) / log(1 - P₁)
        //基于维度计算哈希长度: hashLength 影响划分的精细度:维度越高，需要更长的哈希来充分划分空间;经验公式：hashLength ∝ sqrt(维度数)//✅哈希长度应该与维度的平方根成正比//在高维空间中，需要更多的位来充分划分空间
        //平方根：维度d → 空间有2^d个"角落"//但实际数据通常分布在低维流形上//有效划分需要的位数增长比维度慢// √d 是一个很好的近似
        //乘以2：// 提供一些安全边际，确保充分划分// 实际测试发现 √d × 2 在各种场景下效果良好
    }
    constructor(dimensions, expectedDataSize = 10000, desiredRecall = 0.95) {//✅实际存储数据和执行操作//使用顾问的建议来创建实际可用的LSH实例
        this.dimensions = dimensions;
        //1.调用静态方法获取优化参数// 自动优化参数
        //✅要把参数包装成对象：自文档化；顺序无关：对象属性顺序不重要；易于扩展：未来想返回更多参数，很容易！//返回对象而不是多个值
        //✅数据传输对象（DTO）模式；参数对象模式；把相关的多个数据打包成一个有语义的对象，让代码：更易读，更易维护，更易扩展，更少bug
        //✅调用时不需要传 baseRecall，让方法自动推断
        const optimizedParams = OptimizedLSH.recommendParams( 
            //LSH系统的工作环境
            dimensions, //向量维度：每个数据向量的特征数量，维度越高，需要更复杂的索引结构，直接影响哈希长度的计算
            expectedDataSize, //预期数据量，预计要处理的数据总量，数据量影响单个哈希表的召回率，大数据集需要更频繁的重建
            desiredRecall//期望召回率，召回率 = 找到的相似项 / 所有的相似项
        );
        this.numTables = optimizedParams.numTables;// 实例属性
        this.hashLength = optimizedParams.hashLength;// 实例属性
        this.rebuildThreshold = Math.max(1000, Math.floor(expectedDataSize / 10)); // 初始化重建阈值（基于数据规模）
        //部分1：基于数据量的重建频率，Math.floor(expectedDataSize/10)//含义：每增加"数据总量的10%"就考虑重建
        //部分2：最低保障值Math.max(1000, ...)//含义：无论如何，至少每1000次插入检查一次重建
        this.dataCount = 0;
        this.tables = [];
        this.planesList = [];
        this.vectorMap = new Map();
        this.initializeTables();
    }
    
    // 性能监控//
    //没有这些方法：LSH只是一个静态工具，需要人工监控和调整；有了这些方法：🔍自我诊断：发现性能问题；🛠️ 自我修复：自动调整参数；📈 自我优化：持续保持最佳性能
    //没有监控的LSH：不知道性能如何，可能很慢；有监控的LSH：系统自动优化
    getStats(){ //监控方法名
        //1.初始化统计变量
        let totalBuckets = 0;// 统计实际有数据的桶数量
        let maxBucketSize = 0;// 记录最大的桶里有多少个向量
        let emptyBuckets = 0;// 统计空桶的数量
        //2. 遍历所有哈希表
        for (const table of this.tables) {
            const buckets = Object.values(table); // 获取当前表的所有桶//Object.values(实际使用的桶); 
            totalBuckets += buckets.length; // 累加有数据的桶数量
            //计算空桶数量
            emptyBuckets += (Math.pow(2, this.hashLength) - buckets.length);
            // 解释：每个表最多有 2^hashLength 个桶//// 空桶数量 = 总桶位数 - 有数据的桶数//Math.pow(2, this.hashLength) 计算的是哈希系统的"最大容量"（所有可能的桶位），而实际使用的桶位通常远小于这个数量。空桶率告诉我们系统的"空间利用率"如何
            // 2的幂次：每个位有2种可能（0或1）//对性能的影响：即使很多桶是空的，内存中也要保留这些"空槽位"
            // 遍历每个桶，找到最大的桶
            for (const bucket of buckets) {
                maxBucketSize = Math.max(maxBucketSize, bucket.length);
            }
        }
        //3.计算关键指标
        const avgBucketSize = this.dataCount / totalBuckets;// 平均每个桶有多少向量
        //4. 返回健康报告
        return {
            数据总量: this.dataCount,
            哈希表数量: this.numTables,
            总桶数: totalBuckets,// 实际被使用的桶数量
            平均桶大小:  Number(avgBucketSize.toFixed(2)), //平均每个桶的向量数//浮点数的精度问题：toFixed(2) 保留2位小数，但返回的是字符串，步骤2：Number() 转回数字类型//JavaScript的数值精度处理
            最大桶大小: maxBucketSize, // 最大的桶里有多少向量
            空桶率: Number((emptyBuckets / (Math.pow(2, this.hashLength) * this.numTables)).toFixed(2)) //数据美化 + 精度控制//JavaScript的数值精度处理
        };
    }
    // 自适应调整//自动调节哈希长度
    //智能调节
    adaptiveAdjust() { //自适应调整方法
        const stats = this.getStats();// 获取系统健康报告
        if (stats.平均桶大小 > 100) {//平均桶大小阈值//平均桶大小 < 50 → 查询很快，但可能漏掉相似向量//平均桶大小 50-100 → 良好平衡//平均桶大小 > 100 → 查询明显变慢
            //情况1：桶太大 → 增加哈希长度（更细的划分）
            //防止哈希长度无限增长//20以上再大就内存爆炸了，而且收益很小
            this.hashLength = Math.min(20, this.hashLength + 1);//边界保护：Math.min(20, ...) 和 Math.max(8, ...)
            console.log(`检测到桶过大，增加哈希长度至: ${this.hashLength}`);
            this.rebuildIndex();
        } else if (stats.空桶率 > 0.8) {//0.8（空桶率阈值）// 0.8意味着80%的内存被空桶占用！//内存效率考虑：空桶率 < 0.6 → 内存使用高效，空桶率 0.6-0.8 → 可接受范围，空桶率 > 0.8 → 明显内存浪费
            //情况2：空桶太多 → 减少哈希长度（更粗的划分）  
            this.hashLength = Math.max(8, this.hashLength - 1);//边界保护：Math.min(20, ...) 和 Math.max(8, ...)2⁸ = 256个桶// 最少要有256个桶位，// 再小就划分太粗糙，性能很差
            console.log(`检测到空桶过多，减少哈希长度至: ${this.hashLength}`);
            this.rebuildIndex();
        }
    }
}
// 测试代码
// 使用 SmartLSH 而不是 OptimizedLSH
// ✅ 先定义测试数据
/*const vectors1 = [
    { id: 'img1', vector: [0.8, 0.6, 0.1, 0.9] },
    { id: 'img2', vector: [0.7, 0.5, 0.2, 0.8] },
    { id: 'img3', vector: [0.75, 0.55, 0.15, 0.85] },
    { id: 'img4', vector: [0.2, 0.9, 0.8, 0.1] }
];
// 创建实例
const lsh1 = new SmartLSH(4, 1000, 0.9);  // ✅ 使用完整的类
console.log('开始批处理测试...');
// 批量插入
lsh1.batchInsertOptimized(vectors1);// ❌ vectors 未定义！

// 查看性能统计
const stats = lsh1.getStats();
console.log('性能统计:', stats);
// ✅ 测试查询（需要先添加 query 方法）
const results1 = lsh.query([0.75, 0.55, 0.15, 0.85], 3);
console.log('查询结果:', results1);*/



//-- 哈希表测试---//
class OptimizedLSH {
    static recommendParams(dimensions, expectedDataSize, desiredRecall = 0.95) {
        // 根据数据规模调整基础召回率
        let baseRecall;
        if (expectedDataSize < 1000) {
            baseRecall = 0.7; // 小数据集
        } else if (expectedDataSize < 100000) {
            baseRecall = 0.5; // 中等数据集
        } else {
            baseRecall = 0.3; // 大数据集
        }
        
        // 填空题11: 计算哈希表数量
        const numTables = Math.ceil(
            Math.log(1 - desiredRecall) / Math.log(1 - baseRecall)
        );
        
        // 填空题12: 计算哈希长度  
        const hashLength = Math.max(8, Math.ceil(Math.sqrt(dimensions) * 2));
        
        return { numTables, hashLength };
    }
}
// 输入：维度=256, 数据量=50000, 期望召回率=0.9
const dimensions = 256;
const expectedDataSize = 50000; 
const desiredRecall = 0.9;
// 步骤1：确定baseRecall（中等数据集 → 0.5）
const baseRecall = 0.5;
// 步骤2：计算numTables
const numTables = Math.ceil(Math.log(1 - 0.9) / Math.log(1 - 0.5));
// = Math.ceil(Math.log(0.1) / Math.log(0.5))
// = Math.ceil(-2.3026 / -0.6931) 
// = Math.ceil(3.32) = 4
// 步骤3：计算hashLength
const hashLength = Math.max(8, Math.ceil(Math.sqrt(256) * 2));
// = Math.max(8, Math.ceil(16 * 2))
// = Math.max(8, 32) = 32
console.log(`推荐: ${numTables}个表, ${hashLength}位哈希`);
// 输出: 推荐: 4个表, 32位哈希
//--实际测试--//
// 测试不同的场景
console.log("=== 参数推荐测试 ===");
const testCases = [
    { dim: 64, size: 1000, recall: 0.9 },
    { dim: 512, size: 100000, recall: 0.95 },
    { dim: 1024, size: 1000000, recall: 0.99 }
];
testCases.forEach((test, i) => {
    const params = OptimizedLSH.recommendParams(test.dim, test.size, test.recall);
    console.log(`场景${i+1}: 维度=${test.dim}, 数据量=${test.size.toLocaleString()}`);
    console.log(`  推荐: ${params.numTables}表, ${params.hashLength}位哈希\n`);
});

//--LSH插入过程可视化--//
class VisualLSH {
    constructor(dimensions = 2, numTables = 2, hashLength = 3) {
        this.dimensions = dimensions;
        this.numTables = numTables;
        this.hashLength = hashLength;
        this.tables = [];
        this.planesList = [];
        this.vectorMap = new Map();
        this.dataCount = 0;
        
        this.initializeTables();
        this.visualizeState("初始化完成");
    }
    
    initializeTables() {
        console.log("🎯 初始化哈希表结构...");
        for (let i = 0; i < this.numTables; i++) {
            this.tables.push({});
            this.planesList.push(this.generateRandomPlanes(this.dimensions, this.hashLength));
        }
    }
    
    generateRandomPlanes(dim, numPlanes) {
        const planes = [];
        for (let i = 0; i < numPlanes; i++) {
            const plane = [];
            for (let j = 0; j < dim; j++) {
                plane.push((Math.random() - 0.5) * 2);
            }
            planes.push(plane);
        }
        return planes;
    }
    
    computeHash(vector, planes) {
        let hash = '';
        for (const plane of planes) {
            const dotProduct = this.dotProduct(vector, plane);
            hash += dotProduct >= 0 ? '1' : '0';
        }
        return hash;
    }
    
    dotProduct(v1, v2) {
        return v1.reduce((sum, val, i) => sum + val * v2[i], 0);
    }
    
    insert(vector, id) {
        console.log(`\n🚀 开始插入向量: ${id} = [${vector}]`);
        this.vectorMap.set(id, vector);
        
        for (let i = 0; i < this.numTables; i++) {
            console.log(`\n📊 在哈希表 ${i} 中处理...`);
            
            const planes = this.planesList[i];
            console.log(`   面试官标准: ${planes.map(p => `[${p.map(n => n.toFixed(2))}]`).join(', ')}`);
            
            const hash = this.computeHash(vector, planes);
            console.log(`   📝 计算哈希值: ${hash}`);
            
            // 可视化哈希计算过程
            this.visualizeHashCalculation(vector, planes, hash);
            
            if (!this.tables[i][hash]) {
                this.tables[i][hash] = [];
                console.log(`   🆕 创建新桶: ${hash}`);
            } else {
                console.log(`   🔍 找到现有桶: ${hash} (已有 ${this.tables[i][hash].length} 个元素)`);
            }
            
            this.tables[i][hash].push(id);
            console.log(`   ✅ 将 ${id} 添加到桶 ${hash}`);
        }
        
        this.dataCount++;
        this.visualizeState(`插入 ${id} 完成`);
    }
    
    visualizeHashCalculation(vector, planes, finalHash) {
        console.log(`   🧮 哈希计算详情:`);
        planes.forEach((plane, index) => {
            const dot = this.dotProduct(vector, plane);
            const bit = dot >= 0 ? '1' : '0';
            console.log(`     位${index}: [${vector}] · [${plane.map(n => n.toFixed(2))}] = ${dot.toFixed(2)} → ${bit}`);
        });
        console.log(`   🎯 最终哈希: ${finalHash}`);
    }
    
    visualizeState(message) {
        console.log(`\n🌈 ${message}`);
        console.log("📋 当前LSH状态:");
        console.log(`   数据总量: ${this.dataCount}`);
        
        this.tables.forEach((table, tableIndex) => {
            console.log(`\n   🏷️  哈希表 ${tableIndex}:`);
            const buckets = Object.keys(table);
            if (buckets.length === 0) {
                console.log(`      暂无数据`);
            } else {
                buckets.forEach(bucket => {
                    console.log(`      桶 ${bucket}: [${table[bucket].join(', ')}]`);
                });
            }
        });
        
        console.log("\n" + "=".repeat(50));
    }
    
    // 批量插入演示
    demoBatchInsert() {
        console.log("🎬 开始LSH插入过程演示...");
        
        const testVectors = [
            { id: '猫图片1', vector: [0.8, 0.6] },
            { id: '猫图片2', vector: [0.7, 0.5] },
            { id: '狗图片1', vector: [0.2, 0.9] },
            { id: '猫图片3', vector: [0.75, 0.55] }
        ];
        
        testVectors.forEach(item => {
            this.insert(item.vector, item.id);
        });
        
        this.demoQuery();
    }
    
    demoQuery() {
        console.log("\n🔍 开始查询演示...");
        const queryVector = [0.78, 0.58]; // 与猫图片相似的向量
        
        console.log(`查询向量: [${queryVector}]`);
        
        const candidates = new Set();
        for (let i = 0; i < this.numTables; i++) {
            const planes = this.planesList[i];
            const hash = this.computeHash(queryVector, planes);
            console.log(`在表${i}中查询哈希: ${hash}`);
            
            const bucket = this.tables[i][hash] || [];
            console.log(`  找到候选: [${bucket.join(', ')}]`);
            
            bucket.forEach(id => candidates.add(id));
        }
        
        console.log(`\n🎯 最终相似结果: [${Array.from(candidates).join(', ')}]`);
    }}
   /* 一个标准对应哈希值的一个位
   visualizeHashCalculation(vector, planes, finalHash) {
        console.log(`   🧮 哈希计算详情:`);
        planes.forEach((plane, index) => {
            const dot = this.dotProduct(vector, plane);
            const bit = dot >= 0 ? '1' : '0';
            console.log(`     🎯 标准${index}: [${plane.map(n => n.toFixed(2))}]`);
            console.log(`       计算: [${vector}] · 标准${index} = ${dot.toFixed(2)}`);
            console.log(`       结果: ${dot.toFixed(2)} >= 0 ? → 位${index} = ${bit}`);
        });
        console.log(`   🎯 组合所有位 → 最终哈希: ${finalHash}`);*/
}

// 运行演示
const visualLSH = new VisualLSH(2, 2, 3);
visualLSH.demoBatchInsert();
```

















