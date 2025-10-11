# R*Tree(R-star Tree)
## 基础知识
- **定义**
```
R*树是一种自平衡的树状数据结构，通过优化节点MBR（最小边界矩形）的形状和分布，为多维空间数据提供高效的点查询、范围查询和最近邻查询支持；专门设计用于高效处理多维空间数据（如地理坐标、CAD对象等）；R*树通过在插入过程中引入强制重新插入策略和更智能的分裂算法，显著减少了节点重叠和覆盖面积，从而提升了空间查询性能
```
-  **基本概念解析**

- 节点容量（Node Capacity）

    - 最大容量（maxEntries）：单个节点最多包含的子节点数

    - 最小容量（minEntries）：通常为maxEntries/2

    - 平衡保证：确保树高度一致，查询性能稳定

- 空间关系

    - 分离（Disjoint）：两个MBR没有任何重叠

    - 重叠（Overlap）：两个MBR有共同区域

    - 包含（Contain）：一个MBR完全在另一个内部

    - 被包含（Within）：一个MBR完全在另一个内部

-  **关键特性对比**

|特性|	传统R树|	R*树|	优势|
---|---|---|---
|插入策略	|直接分裂	|强制重新插入 + 分裂	|更优的对象分布|
|分裂算法|	单一维度优化	|多维度+形状优化|	更方正的节点形状|
|成本计算|	仅面积增量|	面积+重叠增量	|更全面的优化目标|
|查询性能|	一般	|提升20-50%|	显著性能改善，**用适度的构建成本换取显著的查询性能提升**|



## 注意事项
1. **混淆点**
- **概念区分**

|混淆点	|概念A	|概念B	|区别说明	|
---|---|---|---
|节点类型	|内部节点	|叶子节点	|内部节点存储子节点引用，叶子节点存储实际数据	|
|MBR计算|	overlaps()|	contains()|	overlaps检查是否有重叠，contains检查是否完全包含	|
|面积 vs 周长|	area|	margin|	area是真实面积，margin是各维度边长和的2倍	|
|分裂目标|	最小化面积|	最小化重叠	|R*树同时优化面积和形状，传统R树只优化面积	|
|重新插入|	强制重新插入|	正常插入	|重新插入是给对象的"第二次机会"，基于当前全局状态|

- **操作环节混淆点**

|操作环节|	容易混淆的做法|	正确做法|	分析|
---|---|---|---
|选择子树|	只考虑面积增量|	面积增量 + 重叠增量	|重叠影响查询性能，必须综合考虑|
|重新插入选择|	选择最近的对象|	选择最远的对象	|最远对象可能是"离群值"，重新分配效果更好|
|分裂轴选择|	只在一个维度分裂|	在所有维度尝试|	不同维度分裂效果不同，需要全局最优|
|分裂点评价|	只考虑面积和|	面积 × 周长	|乘法能放大"面积大且形状差"的坏方案|
|下溢处理|	直接合并|	先尝试重新分配	|重新分配成本低于合并，能保持树结构|


- **流程顺序混淆点**

|流程|	错误顺序|	正确顺序|	逻辑解释|
---|---|---|---
|插入流程|	插入→分裂→重新插入|	插入→重新插入→分裂|	重新插入可能避免分裂，成本更低|
|删除流程|	删除→更新MBR→处理下溢|	删除→处理下溢→更新MBR|	下溢处理可能改变结构，需要最后更新MBR|
|重新插入流程|	重新插入→标记→清理|	标记→重新插入→清理|	必须先标记防止循环，最后清理|
|分裂流程	|分裂→排序→计算成本|	排序→计算成本→分裂|	必须先排序才能找到最佳分裂方案|
|查询流程|	查询所有节点|	空间剪枝→目标节点	|利用MBR重叠快速排除不相关分支|




2. 代码实现
```
/-----------调试版本---------//
class MBR {
    //==========================MBR类=============================//
    // 空间计算（重叠判断、面积、扩展等）//MBR遍历的是自己的边界数据；//负责空间几何计算（遍历自己的维度数据）
  constructor(min, max) {
    // 情况1：无参数，默认创建2维空MBR
    if (min === undefined && max === undefined) {
      this.min = [Infinity, Infinity];
      this.max = [-Infinity, -Infinity];
    }
    // 情况2：情况2：用数字创建（空MBR）
    //创建一个长度为min的数组，用Infinity/-Infinity填充
    //情况2可以创建任意维度的空MBR：
    else if (typeof min === 'number' && max === undefined) {//检查min参数是不是数字类型；检查max参数是不是未提供//如果用户传了一个数字给min，并且没有传max参数
      this.min = new Array(min).fill(Infinity);////创建一个长度为n的空数组；n个空位置；用Infinity填充所有空位置
      this.max = new Array(min).fill(-Infinity);//快速创建指定维度的空MBR//知道要处理3维数据，但还没有具体数据//之后插入数据时，MBR会自动扩展
    }
    ////new MBR(2)是创建2维空MBR//
    // 情况3：提供min/max数组////用数组创建（有具体边界）
    else if (Array.isArray(min) && Array.isArray(max)) {////检查min参数是不是数组，检查max参数是不是数组//如果用户传了两个数组给min和max
      //维度检查//检查min和max的长度是否相同
      if (min.length !== max.length) {////min数组的长度（维度数）
        throw new Error("min和max维度必须相同");////如果两个数组的长度不一样，就报错
      }
      //创建副本//复制用户传入的数组，避免外部修改影响内部数据
      this.min = min.slice();
      this.max = max.slice();
    }
    //new MBR([2])// 意思是"创建1维MBR，边界是[2]到..."////const mbr3D = new MBR([1, 2, 3], [4, 5, 6]);
    ////维度一致性：min和max必须是相同维度//数据安全：内部数据不受外部修改影响//明确边界：用户清楚地知道MBR的具体范围
    // 情况4：参数不合法
    else {
      throw new Error("参数不合法：请提供维度数字或min/max数组");
    }
    
    this.dimension = this.min.length;
  }
   //constructor(min = [Infinity, Infinity], max = [-Infinity, -Infinity]) {
    //如果使用空数组，会出现维度不匹配的问题，不知道维度时无法正确初始化：必须使用固定维度的无穷大
    //假设最小值"无限大"，这样第一个点肯定比它小；假设最大值"无限小"，这样第一个点肯定比它大
    //this.min = min.slice(); // 矩形左下角坐标//创建数组的副本//新的内存地址，避免外部修改影响内部数据
    //this.max = max.slice(); // 矩形右上角坐标
    //封装性原则：类的内部数据应该受到保护，不受外部意外修改的影响；slice() 确保了MBR对象对自己数据的完全控制权
    //两个点定义的是矩形的对角//R*树需要表示空间区域，而不仅仅是点或线段//2D空间平面所以用矩形来表示
    //维度数由min数组的长度决定//数据的维度决定了MBR的维度//数据的结构决定了空间的维度
    //this.dimension = min.length//MBR的维度完全由输入数据决定，不需要预先硬编码
  //🎯添加缺失的方法
  clone() {
    return new MBR(this.min.slice(), this.max.slice());
  }

  getCenter() {
    const center = [];
    for (let i = 0; i < this.min.length; i++) {
      center.push((this.min[i] + this.max[i]) / 2);
    }
    return center;
  }
  extend(other) {//遍历所有维度，维度数来自this.min.length
    if (this.dimension !== other.dimension) {
      throw new Error(`维度不匹配: ${this.dimension}D vs ${other.dimension}D`);
    }
    for (let i = 0; i < this.dimension; i++) {
      this.min[i] = Math.min(this.min[i], other.min[i]);
      this.max[i] = Math.max(this.max[i], other.max[i]);
    }
    return this;
  }
  toString() {//将对象转换成可读的字符串表示形式//返回对象的字符串描述//适合调试和测试
    return `MBR(${this.dimension}D): [${this.min}] -> [${this.max}]`;
  }
  //计算MBR的面积（在2D）或体积（在3D+）：
   get area() {//area getter实际上计算的是MBR的超体积——在任意维度下，各维度边长的乘积
    let area = 1;
    for (let i = 0; i < this.min.length; i++) {
      area *= (this.max[i] - this.min[i]); // 遍历所有维度//通过循环 this.min.length（维度数）次，自动适应任意维度
    }
    //通过 mbr.area 直接访问面积，而不需要调用函数
    return area;
  }
  //R*树论文中，这个方法计算的不是几何周长，而是各维度边长总和的两倍
  //R*树使用这个"周长"来偏好更方正的形状//在2D时计算正确的周长：计算MBR的周长（R*树的核心优化指标之一）
  get margin() {//计算MBR的周长（2D）或表面积（3D+）
  let sumOfSides = 0;
  for (let i = 0; i < this.dimension; i++) {
    sumOfSides += (this.max[i] - this.min[i]);// 把所有维度的边长相加
  }
  return 2 * sumOfSides;// 在nD时计算各维度边长和的2倍
}
//=======r*树查询逻辑========//
  // 判断两个MBR是否重叠//MBR只负责空间计算，不负责树遍历
  overlaps(other) {
    // 遍历每个维度// 如果在任一维度上不重叠，则整体不重叠//自动适应任意维度，因为它在所有维度上都检查
    //高效剪枝，减少不必要的搜索//基于"任一维度分离则整体分离"的原理
    for (let i = 0; i < this.min.length; i++) {
      if (this.max[i] < other.min[i] || this.min[i] > other.max[i]) {
        return false;
      }
    }
    return true; // 所有维度都重叠，则整体重叠
  }
  contains(other) {//判断当前MBR是否完全包含另一个MBR//检查当前矩形是否完全包围另一个矩形
    for (let i = 0; i < this.min.length; i++) {
        //查询优化：快速判断查询区域是否完全包含在某个节点内；空间关系：确定对象之间的包含关系；分裂决策：在分裂时判断对象分组
      if (this.min[i] > other.min[i] || this.max[i] < other.max[i]) {
        return false;
      }
    }
    return true;
  }

}}
////R*树核心概念
//第一部分：核心目标
//R*树的设计目标是，在继承R树所有能力的基础上，尤其致力于优化以下两个关键指标：
    //最小化节点面积 （一个衡量节点覆盖范围的指标）
    //最小化节点重叠 （一个衡量节点间低效搜索的指标）
//第二部分：插入流程的革新
//当向一个已满的叶子节点插入新数据时，传统R树会立即执行分裂。而R*树则引入了一个革命性的步骤：它首先会尝试执行强制重新插入
//第三部分：秘密武器——“强制重新插入”
   // 触发条件：当节点已满，且深度 （或层级）未达到一个预设的阈值时，优先触发此操作。
      //R树通常只对树的底层（叶子节点及其父节点）进行重新插入，避免在高层次进行代价高昂的全局重组；
   // 操作对象：从已满节点中，选择距离节点中心远的约30% 的对象；
      //优先驱逐那些离群的、可能本就不属于这个节点的对象。30%这个值是大量实验得出的一个平衡点。
   // 执行动作：将这些被选中的对象从原节点中删除，然后在树中重新插入；这些对象被当作新的插入对象，从根节点开始，重新走一遍插入流程
   // 设计理念：这个操作给予了一部分对象第二次选择的机会，让它们能够基于当前全局的树结构，做出更优的位置选择。
//第四部分：更聪明的“分裂”算法
//当“强制重新插入”无法解决问题，必须分裂时，R*树的分裂算法也比传统R树更精细。
    //选择分裂轴：它会在所有维度上进行尝试，并选择一个能使分裂后两个新节点的周长之和最小的轴作为分裂轴；最小化周长之和，能直接促使产生更方正的矩形，而非狭长的条形，这大大提升了查询效率
    //选择分裂点：沿选定的轴，它不再只找一个分裂点，而是会尝试多种不同的分布方案；实践中常为 2 * M-2种，M为节点容量
    //评价标准：在评价一个分裂方案的好坏时，它除了考虑覆盖面积，还会额外考虑周长（或形状质量），因为更“方正”的矩形通常意味着更少的死空间和更高的查询效率。
//创建一个初始为空的边界矩形
class RStarTreeNode {
    //=======================节点类==============================//
    // 节点只存储数据，不负责搜索逻辑//
  constructor(isLeaf = false, mbr = new MBR()) {
    this.isLeaf = isLeaf;
    this.mbr = mbr;       // 该节点所覆盖的整个区域
    this.children = [];   // 子节点（如果是内部节点）或数据项（如果是叶子节点）
    this.parent = null;
    this.data = null; // 仅叶子节点使用
  }
  // 计算节点的MBR（基于其子节点或数据项）
  computeMBR() {
    this.mbr = new MBR();
    for (let child of this.children) {
      this.mbr.extend(child.mbr);
    }
    return this.mbr;
  }
}
class RStarTree {
    //===============================RStarTree类================================//
    //管理整棵树（插入、删除、搜索-实现搜索算法-协调节点间的操作//遍历的是树节点结构//遍历树结构：节点 → 子节点 → 孙子节点//
  constructor(maxEntries = 4) {
    this.root = new RStarTreeNode(true);
    this.maxEntries = maxEntries;
    this.minEntries = Math.floor(maxEntries / 2);
    this.reinsertInProgress = false;//🎯 R*树稳定性的重要保障：是一个防止重新插入无限循环的标志：这是一个"锁"机制，用来标记当前是否正在进行重新插入操作。
  }
  //=======r*树查询逻辑========//
  // search方法在这里
  search(queryMBR) {
    const results = [];
    this._searchRecursive(this.root, queryMBR, results);//搜索树从根节点开始查询区域，queryMBR要搜索的矩形范围，results结果数组，用于收集找到的数据
    //this: 当前RStarTree实例//_searchRecursive: 一个私有递归方法（_前缀表示内部方法）//这个方法负责实际的树遍历逻辑
    return results;
  }
//分离轴定理：两个n维矩形重叠，当且仅当在所有维度上都重叠//在任一维度上分离，则整体分离
  _searchRecursive(node, queryMBR, results) {
    // 使用MBR的overlaps方法进行空间判断
    if (!node.mbr.overlaps(queryMBR)) {//// 1. 空间剪枝：如果不重叠，跳过整个子树
      return;
    }
    if (node.isLeaf) {// 2. 如果是叶子节点：检查实际数据
      for (let child of node.children) {
        if (child.mbr.overlaps(queryMBR)) {
          results.push(child.data);// 找到匹配，加入结果
        }
      }
    } else {// 3. 如果是内部节点：递归搜索子节点
      for (let child of node.children) {
        this._searchRecursive(child, queryMBR, results);// 递归调用
      }
    }
  }
  //==============插入+分裂逻辑================//
  // 插入数据的主入口
  insert(data, coordinates) {
    // 1：为数据创建叶子节点
    const dataNode = new RStarTreeNode(true);// true表示这是叶子节点
    dataNode.mbr = new MBR(coordinates, coordinates); //点的MBR就是自己//coordinates空间坐标
    dataNode.data =data;// 存储实际的数据内容
    // 2：从根节点开始插入
    this._insert(dataNode, this.root, 0);
    //R*树需要统一处理：叶子节点：存储实际数据//内部节点：存储子节点的引用
  }
  //---插入方法---//
  _insert(dataNode, currentNode, depth) {
     console.log(`📥 _insert 开始: 插入 ${dataNode.data}, 深度=${depth}, 节点类型=${currentNode.isLeaf ? '叶子' : '内部'}`);
    if (currentNode.isLeaf) {
        console.log(`  叶子节点: 插入前有 ${currentNode.children.length} 个子节点`);
      //1.叶子节点直接添加数据
      currentNode.children.push(dataNode);
      dataNode.parent = currentNode;
      console.log(`  调用 _updateMBR (第一次)`);
      this._updateMBR(currentNode,0, "insert_after_push");

      //2.如果节点已满，需要处理溢出
      if (currentNode.children.length > this.maxEntries) {
        console.log(`  🚨 节点溢出! 调用 _handleOverflow`);
        this._handleOverflow(currentNode, depth);
      }
    } else {
      //3.内部节点需要选择子树
      console.log(`  内部节点: 选择子树`);
      const chosenChild = this._chooseSubtree(dataNode, currentNode);
      this._insert(dataNode, chosenChild, depth + 1);
    }
    //4.插入后更新节点的mbr
    console.log(`  调用 _updateMBR (第二次)`);
    this._updateMBR(currentNode);
    console.log(`📤 _insert 结束: ${dataNode.data}`);
  }
  //---4.1选择正确的子树---//
  _chooseSubtree(dataNode, node) {
    console.log(`=== 为 ${dataNode.data} 选择子树 ===`);
    let bestChild = null;
    let bestCost = Infinity;
    //R*树用这个成本来选择"最优"的插入位置
    for (let child of node.children) {
      // 1：计算MBR扩展后的面积增量
      const enlargedMBR = child.mbr.clone();//克隆当前MBR
      enlargedMBR.extend(dataNode.mbr);//扩展MBR以包含新数据
      //选择那个为了容纳新数据，需要扩展面积最小的节点
      const areaIncrease = enlargedMBR.area - child.mbr.area;//计算面积增量
      // 2：R*树还考虑重叠增量
      const overlapIncrease = this._computeOverlapIncrease(node, child, dataNode);//计算重叠增量的具体实现
      //重叠 = 节点之间MBR的重叠区域；重叠增量 = 插入新数据后，与其他兄弟节点重叠区域的变化量
      //有重叠时：两个都要搜索！效率低//无重叠时：只有一个盒子需要搜索
      //减少查询时的多路径搜索：重叠越少，查询时需要遍历的分支越少；提高查询性能：这是R*树比传统R树性能更好的关键原因；保持树结构健康：避免产生高度重叠的节点
      // 3.总成本 = 面积代价 + 重叠代价
      //综合考虑了"扩展代价"和"邻里影响"//根据重叠信息来做出智能的插入决策//进行高效剪枝-跳过不相关的搜索路径//维持树结构健康-避免产生高度重叠的节点
      //预见性地避免问题，而不仅仅是事后处理//
      const cost = areaIncrease + overlapIncrease;
    console.log(`  候选 ${child.mbr.toString()}: 成本=${cost}`);
    console.log(`候选 ${child.mbr.toString()}:`);
    console.log(`  面积增量: ${areaIncrease}, 重叠增量: ${overlapIncrease}, 总成本: ${cost}`);
      // 4.选择成本最低的子节点
      if (cost < bestCost) {
        bestCost = cost;
        bestChild = child; //选择当前这个子节点作为最佳候选
        console.log(` 🎯 成为最佳选择`);
    }
      }
      return bestChild;//5.返回最佳插入位置
    //---❌注意----//
    //🎯 1.修改重新插入策略，确保对象被分配到不同的节点
    }
//---4.1.1计算重叠增量---//
  _computeOverlapIncrease(parent, child, newEntry) {
     console.log(`计算重叠增量: ${child.mbr.toString()} + ${newEntry.mbr.toString()}`);
     // 计算：如果向currentChild插入newData，与所有兄弟节点的重叠面积会增加多少
     //parentNode: 当前父节点（包含所有兄弟节点//currentChild: 我们正在考虑插入的子节点//newData: 要插入的新数据
    let overlapIncrease = 0;
    // 第一步：模拟扩展当前子节点的MBR
    const enlargedMBR = child.mbr.clone();
    enlargedMBR.extend(newEntry.mbr);
    // 第二步：遍历所有兄弟节点（除了自己）
    for (let sibling of parent.children) {
      if (sibling !== child) {// 跳过自己
        // 计算当前的重叠面积
        const currentOverlap = this._computeOverlap(child.mbr, sibling.mbr);
        // 计算扩展后的重叠面积  
        const newOverlap = this._computeOverlap(enlargedMBR, sibling.mbr);
        //重叠增量 = 新重叠 - 旧重叠
        const increase = newOverlap - currentOverlap;
        console.log(`  与兄弟 ${sibling.mbr.toString()}: 旧重叠=${currentOverlap}, 新重叠=${newOverlap}, 增量=${increase}`);
        
        //---❌注意----//
        //🎯总重叠增量:重叠增量计算问题
        overlapIncrease += increase;
      }
    }
     console.log(`总重叠增量: ${overlapIncrease}`);
    return overlapIncrease;
  }
  //---4.1.2计算mbr1和mbr2重叠部分的面积（2D）或体积（3D+）---//
  _computeOverlap(mbr1, mbr2) {
    if (!mbr1.overlaps(mbr2)) return 0;//第1步：检查是否重叠// 如果不重叠，直接返回0
    //第2步：计算每个维度的重叠长度
    let overlap = 1;// 初始值
    //遍历每个维度//在当前重叠值的基础上，乘上这个维度的重叠长度，来构建完整的多维重叠区域
    for (let i = 0; i < mbr1.min.length; i++) {
      const minOverlap = Math.max(mbr1.min[i], mbr2.min[i]);
      const maxOverlap = Math.min(mbr1.max[i], mbr2.max[i]);
      overlap *= Math.max(0, maxOverlap - minOverlap);
      //累乘每个维度的重叠长度来计算总的重叠面积/体积//// 确保重叠长度不为负数（防止边界情况）// 将当前维度的重叠长度乘到总重叠值上
      //// 计算在当前维度上的重叠长度；const overlapLength = maxOverlap - minOverlap;
      //// 确保重叠长度不为负数（防止边界情况）const safeOverlapLength = Math.max(0, overlapLength);
      //// 将当前维度的重叠长度乘到总重叠值上overlap = overlap × safeOverlapLength;

    }
    return overlap;    
    }
  
  //---5.处理溢出---//
  _handleOverflow(node, depth) {
  console.log(`🛠️ 处理溢出，深度=${depth}`);
  
  //🎯关键修复：添加重新插入次数限制
  if (depth < 2 && (!node.reinsertCount || node.reinsertCount < 2)) {
    console.log("第一次尝试重新插入");
    node.reinsertCount = (node.reinsertCount || 0) + 1; // 🎯记录重新插入次数
    
    const removedEntries = this._selectReinsertEntries(node);
    this._reinsert(removedEntries, depth);
    // 1.1如果重新插入后仍然溢出，则分裂
    if (node.children.length > this.maxEntries) {
      console.log("重新插入后仍然溢出，执行分裂");
      this._splitNode(node);
    }
  } else {
    console.log(`🛠️ 节点溢出，直接分裂，深度=${depth}`);
    // 2：高层节点直接分裂
    console.log("已尝试过重新插入或深度过大，直接分裂");
    this._splitNode(node);
  }
}
  //---5.1选择哪些对象应该重新插入---//
  _selectReinsertEntries(node) {  //选择要驱逐的对象
     console.log(`🎯 选择重新插入对象，当前节点: ${node.mbr.toString()}`);
    //从节点的所有子对象中，选择一部分进行"强制重新插入"
    const entries = node.children;
    // 1：选择约30%的对象重新插入
    const p = Math.max(1, Math.floor(entries.length * 0.3));
    console.log(`选择 ${p} 个对象重新插入`);
    //---❌注意----//
    // 🎯const p = Math.floor(entries.length * 0.3);当 entries.length = 3 时，p = Math.floor(3 * 0.3) = Math.floor(0.9) = 0//这就是显示"选择 0 个对象重新插入"的原因
    // 🎯在 _selectReinsertEntries 方法中，确保至少选择1个对象
    // 2：计算节点中心
    const center = node.mbr.getCenter();
    console.log(`节点中心: [${center}]`);
    // 3：按到中心的距离排序，选择最远的对象
    entries.sort((a, b) => {
      const distA = this._distanceToPoint(center, a.mbr);
      const distB = this._distanceToPoint(center, b.mbr);
      return distB - distA; //实际上是从大到小排序//从远到近//排序比较函数
    });
    // 4：移除最远的p个对象
    const removed = entries.splice(0, p);// 然后应该从开头取最远的！取前p个最远的
    console.log(`移除的对象: [${removed.map(r => r.data).join(', ')}]`);
    this._updateMBR(node);
    return removed;
    //---❌注意----//
    //🎯需要避免重复选择相同的对象进行重新插入:限制重新插入次数,标记已重新插入的对象,直接分裂
  }
//---5.2重新插入操作---//
_reinsert(entries, depth) {//R*树的动态自我优化
  console.log(`🔄 _reinsert 开始: 重新插入 ${entries.length} 个对象`);
  console.log(`🔄 _reinsert 调用: 深度=${depth}, 对象数=${entries.length}, 调用者=${new Error().stack.split('\n')[2]?.trim()}`);
  //🎯防循环保护：记录本次重新插入的对象
  if (!this.currentReinsertSet) this.currentReinsertSet = new Set();
  //🎯关键修复1：在循环开始前创建唯一的重新插入标识
  const reinsertSessionId = `reinsert-${depth}-${Date.now()}`;
  for (let entry of entries) {
    //const entryKey = `${entry.data}-${Date.now()}`; // 使用时间戳确保唯一性
    const entryKey = `${entry.data}-${reinsertSessionId}`; // 🎯修复：使用会话ID而不是深度
    if (this.currentReinsertSet.has(entryKey)) {
      console.log(`⚠️ 检测到循环，跳过 ${entry.data}`);
      continue;
    }
    this.currentReinsertSet.add(entryKey);
    console.log(`  重新插入: ${entry.data} 在深度 ${depth}`);
    //重新插入的本质是让对象重新选择位置//重新插入 = 第二次机会
    //1.基于当前全局状态 第一次插入时，树可能很空；重新插入时，树结构已经变化，可能找到更优位置
    //2.自我修复能力：如果早期插入决策不好，重新插入可以纠正；树具备"学习"和"优化"能力  
    //3.低成本优化：只重新插入30%的对象；用较小代价获得较大优化
    //🎯关键修复2：清除父节点引用，让对象真正重新选择位置
    entry.parent = null;
    this._insert(entry, this.root, 0);//entry: 要重新插入的对象；this.root: 从根节点开始（全局重新选择）；深度从0开始（完整遍历）
  }
  //🎯关键修复3：将清理逻辑移到循环外部，只执行一次
  //🎯使用防抖，避免重复清理
  if (this.cleanupTimeout) clearTimeout(this.cleanupTimeout);
  this.cleanupTimeout = setTimeout(() => {
    console.log(`🧹 清理重新插入记录 (深度=${depth})`);
    this.currentReinsertSet.clear();
  }, 100); // 稍微延迟清理
  
  console.log(`🔄 _reinsert 结束`);
  //---❌注意----//
  //🎯setTimeout 在循环内部被调用，导致创建了很多定时器：⚠️ 重复清理:清理重新插入记录出现了很多次;可能的内存泄漏：多个setTimeout在运行
  //🎯如果 setTimeout 确实在外面，但还是有很多清理记录，那说明 _reinsert 方法被调用了很多次
  //多个节点同时溢出，每个节点都调用了 _reinsert;分裂操作触发连锁反应，导致多次重新插入;重新插入的对象又触发了新的溢出
}
//=====5.3分裂逻辑=====//
  //精细化分裂策略：选择那个既节约空间又形状方正的分裂方案//
  _splitNode(node) {
    let bestAxis = 0;//记录最佳分裂维度（X轴、Y轴等）//分裂点定位器 // 默认在第一个位置分裂
    let bestSplitIndex = 0; // 记录最佳分裂位置（在排序后的第几个对象后分裂）// 默认选择第0个维度（X轴）
    let bestCost = Infinity;// 记录最低成本（越小越好）//初始化为无限大// 这样第一个候选方案无论多差，都会成为"当前最佳"
    //共同记录了到目前为止找到的最佳分裂方案
    // 1：在所有维度上尝试分裂
    for (let axis = 0; axis < node.mbr.min.length; axis++) {
      //2.按当前维度对子节点排序
      node.children.sort((a, b) => {//按指定维度对对象进行排序
        const centerA = (a.mbr.min[axis] + a.mbr.max[axis]) / 2;//对于每个对象（MBR），计算它在当前维度上的中心位置
        const centerB = (b.mbr.min[axis] + b.mbr.max[axis]) / 2;// 考虑对象的整体位置// 既考虑起点也考虑大小，更合理！//自动适应任意维度
    //计算中心：找到每个对象在当前维度上的中心位置；比较排序：按中心位置对对象进行排序；为分裂做准备：有序的对象列表便于寻找最佳分裂点
        return centerA - centerB;// 比较逻辑：返回负数：a应该排在b前面；返回正数：a应该排在b后面；返回0：a和b位置不变
        //让中心位置较小的对象排在前面，实现按中心坐标的升序排列"
     });
      // 3：尝试所有可能的分裂点//枚举所有合法的分裂方式
      //确保分裂后两个新节点都至少有minEntries个对象
      for (let i = this.minEntries; i <= node.children.length - this.minEntries; i++) {//确保分裂后两个新节点都至少有minEntries个对象
        // 临时排序，只是为了计算成本
        //这个循环：寻找最优平衡：通过循环尝试所有可能，找到最佳平衡点
        //确保：考虑所有合法分裂方案；避免产生过小的节点（少于minEntries）；系统性地寻找最优解
        const group1 = node.children.slice(0, i);// 第一组：前i个对象
        const group2 = node.children.slice(i);// 第二组：剩余对象
        //分裂必须满足最小容量要求//this.minEntries：节点最少要包含的对象数//node.children.length：当前节点的对象总数
        const mbr1 = this._computeGroupMBR(group1); // 计算第一组的边界
        const mbr2 = this._computeGroupMBR(group2);// 计算第二组的边界
        //穷举搜索最优分裂方案：循环：尝试所有可能的分裂位置；分组：将对象分成两个合法组别；计算：为每组计算空间边界；评估：后续代码会基于这些MBR计算成本
        // 4：R*树同时优化面积和形状
        //评估分裂方案质量的评分系统//
        //完整的优化目标：总面积小（空间紧凑）；形状方正（周长小，查询效率高）；平衡（两个节点大小相近）
        const areaSum = mbr1.area + mbr2.area; // 总面积成本//让两个新节点的覆盖总面积最小//衡量"空间利用率"（越小越好）
        const marginSum = mbr1.margin + mbr2.margin;// 总形状成本 //让两个新节点的形状尽量方正（周长小）//衡量"形状质量"（越小越好）
        const cost = areaSum * marginSum;// 综合成本//同时优化面积和形状，找到最佳平衡//综合评分（越小代表分裂方案越优秀）
        //用乘法（更好）：放大问题：面积大 × 形状差 = 成本很高！；面积小 × 形状好 = 成本很低 
        // 面积小 × 周长小 = 总成本小 
        if (cost < bestCost) {
            //5.找到更好的方案，更新记录
          bestCost = cost;
          bestAxis = axis;
          bestSplitIndex = i;
        }
        //循环结束后，node.children的排序状态是不确定的！排序状态丢失
        //在多个维度上循环尝试，最后一次排序可能是任意维度的排序，不一定是最终选中的最佳维度      
      }
    }
    //----6.执行实际分裂----//
    this._performSplit(node, bestAxis, bestSplitIndex);
  }//分裂执行引擎：
  //1.准备：排序并分组对象；2.分裂：创建新节点，分配对象；3.连接：建立正确的父子关系；4.特殊处理：根节点分裂需要创建新根；5.连锁检查：确保父节点不会因此溢出
  _performSplit(node, axis, splitIndex) {//splitIndex是基于特定排序顺序：按照最佳轴的方向把对象排好队
    //1.按最佳轴排序
    //最佳轴 = 在哪个方向上切割效果最好//最佳轴"的选择过程：会计算两种切法的成本：水平切（Y轴）的成本；垂直切（X轴）的成本；
    //重新排序是为了确保一致性：虽然已经找到了最佳分裂方案，但在实际执行分裂时，我们需要重新确保对象按照那个方案排序
    //分裂位置（splitIndex）依赖于排序顺序
    node.children.sort((a, b) => {
      const centerA = (a.mbr.min[axis] + a.mbr.max[axis]) / 2;
      const centerB = (b.mbr.min[axis] + b.mbr.max[axis]) / 2;
      return centerA - centerB;
    });
    const group1 = node.children.slice(0, splitIndex);
    const group2 = node.children.slice(splitIndex);
    //2：创建新节点
    const newNode = new RStarTreeNode(node.isLeaf);
    newNode.children = group2;
    newNode.parent = node.parent;//新节点的父节点 = 原节点的父节点
    //建立新节点的父子关系//建立向上链接：完成双向关系
    node.children = group1;
    
    //3.更新两个节点的MBR
    this._updateMBR(node);
    this._updateMBR(newNode);
    
    if (node === this.root) {
      // 4：分裂根节点时需要创建新的根节点
      const newRoot = new RStarTreeNode(false);
      newRoot.children = [node, newNode];
      node.parent = newRoot;
      newNode.parent = newRoot;
      this._updateMBR(newRoot);
      this.root = newRoot;
    } else {
      //5：将新节点添加到父节点
      node.parent.children.push(newNode);
      //6.检查父节点是否溢出
      if (node.parent.children.length > this.maxEntries) {
        //处理分裂的连锁反应：分裂的"多米诺骨牌效应"；如果不检查：树结构可能变得不平衡；某些节点会过度拥挤；查询性能下降
        //分裂的自动传播//
        this._handleOverflow(node.parent, this._getDepth(node.parent));
      }
    }
  }
  //-----6.1更新mbr------//
  _updateMBR(node) {
    if (node.children.length === 0) return;
    //重新计算：确保节点MBR精确包含所有子节点；递归传播：将MBR变化向上传播到整个祖先链；保持一致性：维护整棵树的空間索引正确性
    // node.mbr = node.children[0].mbr.clone(); 
    // 注意1：🎯确保创建新的 MBR 实例
    if (node.children[0].mbr instanceof MBR) {
        node.mbr = node.children[0].mbr.clone();//1：重新计算节点的MBR，包含所有子节点;;// 从第一个子节点开始
    } else {
        // 如果是数据节点，使用数据节点的 MBR
        node.mbr = new MBR(node.children[0].mbr.min, node.children[0].mbr.max);
    }
    
    for (let i = 1; i < node.children.length; i++) {
      node.mbr.extend(node.children[i].mbr);// 逐个扩展包含其他子节点；确保节点的MBR精确包围所有子节点
    }
    //2：递归更新父节点的MBR
    if (node.parent) {
      this._updateMBR(node.parent);//当前节点MBR变了，父节点的MBR也需要相应更新//MBR变化会向上传播：需要递归更新
    }
  }
  //---❌注意----//
  //🎯1.Uncaught TypeError: node.children[0].mbr.clone is not a function:在 _updateMBR 方法中，node.children[0].mbr 可能不是 MBR 实例
  //🎯2.Uncaught TypeError: node.mbr.getCenter is not a function：MBR 对象缺少 clone 和 getCenter
  //🎯3._updateMBR 错误: InternalError: too much recursion：
  //无限递归问题：1.当更新父节点时，如果父节点的 MBR 没有实际变化，但仍然递归调用，就会形成无限循环2.//即使 MBR 内容相同，递归调用仍然发生了(浮点数精度问题；对象创建时机问题)
  //调试版本1_updateMBR：
_updateMBR(node) {
  console.log("🔄 更新 MBR, 节点类型:", node.isLeaf ? "叶子" : "内部");
  console.log("子节点数量:", node.children.length);
  if (node.children.length === 0) {
    console.log("没有子节点，跳过更新");
    return;
  }
  try {
     //🎯保存旧的 MBR 用于比较
    const oldMBR = new MBR(node.mbr.min, node.mbr.max);
    // 调试第一个子节点//计算新的 MBR
    const firstChild = node.children[0];
    console.log("第一个子节点:", firstChild);
    console.log("第一个子节点的 mbr:", firstChild.mbr);
    console.log("mbr 类型:", typeof firstChild.mbr);
    console.log("是否有 clone 方法:", firstChild.mbr && firstChild.mbr.clone);
    if (firstChild.mbr && firstChild.mbr.clone) {
      node.mbr = firstChild.mbr.clone();
    } else {
      // 创建新的 MBR
      console.log("创建新的 MBR");
      node.mbr = new MBR();
    }
    for (let i = 1; i < node.children.length; i++) {
      node.mbr.extend(node.children[i].mbr);
    }
    console.log("更新后的 MBR:", node.mbr.toString());

    //🎯关键修复：只有 MBR 实际发生变化时才递归更新父节点
  if (node.parent && !this._mbrEquals(node.mbr, oldMBR)) {//如果有父节点并且MBR不相同；更新父节点
    this._updateMBR(node.parent);
  }
    if (node.parent) {
      this._updateMBR(node.parent);
    }
  } catch (error) {
    console.log("❌ _updateMBR 错误:", error);
    throw error;
  }
}
// 🎯添加MBR比较方法
_mbrEquals(mbr1, mbr2) {
  return mbr1.min.every((val, i) => val === mbr2.min[i]) &&//检查 mbr1.min 数组的每个元素是否都等于 mbr2.min 数组对应位置的元素
         mbr1.max.every((val, i) => val === mbr2.max[i]);//同样检查 max 数组
}
//---调试2---//
//---❌注意----//
//🎯1.MBR比较逻辑是正确的 - 每次都返回 true（相同）；递归保护是有效的 - 没有无限递归，每次都正确停止
//🎯_updateMBR 被重复调用了很多次，但每次 MBR 都相同；这说明问题不在 _updateMBR 本身，而在于谁在重复调用它
//在 _insert 中调用了两次 _updateMBR;;重新插入导致重复调用;;某个地方有循环调用
//重新插入 A → 节点溢出 → 重新插入 B → 节点溢出 → 重新插入 C → 节点溢出 → 重新插入 D → ...=>每次重新插入的对象又被重新选择进行重新插入=>形成了无限循环：重新插入 → 溢出 → 重新插入 → 溢出 → 
//🎯在 _selectReinsertEntries 中，我们选择了对象进行重新插入，但这些对象重新插入后又回到了同一个节点，然后又被重新选择:重新插入的对象会回到同一个节点
//🎯在 _chooseSubtree 方法中:1.当所有子节点的成本相同时，系统可能会总是选择同一个节点2.重新插入的对象位置没变 → 成本计算相同3.节点结构没有变化 → 相同的选择逻辑
//🎯每次重新插入后，节点的MBR都是 [1,1] -> [3,3]，说明：重新插入的对象又回到了同一个节点;节点的内容没有真正变化;形成了无限循环//所有子节点成本相同 → 总是选择同一个;重新插入的对象位置没变 → 相同的成本计算;节点结构单一 → 没有其他选择
//🎯Uncaught TypeError: can't access property "mbr", node is null：node 为 null 但代码试图访问 node.mbr。问题出现在删除逻辑
//删除操作：检查 leafNode.parent 是否为 null；合并操作：修复变量名错误（leafNode → parent）
_updateMBR(node, depth = 0) {
  console.log(`=== _updateMBR 调用，深度=${depth} ===`);
  if (depth > 5) {
    console.error("💥 递归过深！");
    return;
  }
  const oldMBR = new MBR(node.mbr.min, node.mbr.max);
  console.log("保存的旧MBR:", oldMBR.toString());
  // 计算新 MBR
  const newMBR = new MBR(node.children[0].mbr.min, node.children[0].mbr.max);
  for (let i = 1; i < node.children.length; i++) {
    newMBR.extend(node.children[i].mbr);
  }
  console.log("计算的新MBR:", newMBR.toString());
  console.log("节点当前MBR:", node.mbr.toString());
  const isEqual = this._mbrEquals(newMBR, oldMBR);
  console.log("MBR是否相等?", isEqual);
  if (!isEqual) {
    node.mbr = newMBR;
    console.log("✅ 更新了节点MBR");
    if (node.parent) {
      console.log("🔄 准备递归父节点...");
      this._updateMBR(node.parent, depth + 1);
    }
  } else {
    console.log("⏸️ MBR相同，不更新不递归");//重新插入的对象又回到了同一个节点
  }
}
//===========R*树的工具方法=========//
//-----5.3.1计算组的边界-----//空间计算//
_computeGroupMBR(entries) {
  if (entries.length === 0) return new MBR(); // 空组返回空MBR
  
  const mbr = entries[0].mbr.clone(); // 从第一个对象开始
  for (let i = 1; i < entries.length; i++) {
    mbr.extend(entries[i].mbr);// 逐个扩展包含其他对象
  }
  return mbr;
}

//-------5.1.1计算点到MBR的距离-----//距离测量//
_distanceToPoint(point, mbr) {
  let dist = 0;
  for (let i = 0; i < point.length; i++) {
    const p = point[i];
    if (p < mbr.min[i]) {//点在MBR左边/下面
      dist += (mbr.min[i] - p) ** 2;//mbr.min[i] - p = 点到MBR边界的距离
    } else if (p > mbr.max[i]) {// 点在MBR右边/上面
      dist += (p - mbr.max[i]) ** 2;
    }
    // 如果点在MBR内部，该维度距离为0如果 min[i] <= p <= max[i]，不执行任何操作//该维度的距离贡献为0
  }
  return Math.sqrt(dist);//欧几里得距离:√(Δx² + Δy² + Δz² + ...)累加各维度距离的平方，最后再开方
}

//----6.2获取节点深度----//结构分析//
_getDepth(node) {
  let depth = 0;
  while (node && !node.isLeaf) {
    depth++;
    node = node.children[0];//从任何内部节点出发，沿着第一个子节点一直向下，最终都会到达叶子节点，这样可以准确计算深度
  }
  return depth;
}
//这些方法放在 _updateMBR 方法之后，delete 方法之前

//=======删除逻辑========//
  delete(data, coordinates) {
    console.log(`🗑️ 开始删除: ${data} 在 [${coordinates}]`);
    const targetMBR = new MBR(coordinates, coordinates);
    const leafNode = this._findLeaf(this.root, data, targetMBR);
    if (!leafNode) {
      console.log(`❌ 未找到要删除的数据: ${data}`);
      return false;
    }
    //1.从叶子节点中删除数据
    const index = leafNode.children.findIndex(child => 
      child.data === data && this._mbrEquals(child.mbr, targetMBR)
    );
    if (index === -1) {
      console.log(`❌ 在叶子节点中未找到数据: ${data}`);
      return false;
    }
    //2：从children数组中移除找到的数据节点
    leafNode.children.splice(index, 1);
    console.log(`✅ 从叶子节点删除数据: ${data}`);
    //3：更新叶子节点的MBR
    this._updateMBR(leafNode); 
    //4：处理下溢（节点对象数过少）
    if (leafNode.children.length < this.minEntries && leafNode !== this.root) {
      console.log(`⚠️ 检测到下溢，节点对象数: ${leafNode.children.length}`);
      this._handleUnderflow(leafNode);
    } else if(leafNode.parent) {
      // 5：如果没有下溢，只需要更新MBR
      this._updateMBR(leafNode.parent); // ❌ 这里 leafNode.parent 可能为 null
    }
    return true;
    //---❌注意----//
    //🎯Uncaught TypeError: can't access property "mbr", node is null
  }

  // ============ 查找包含数据的叶子节点 ============
  _findLeaf(node, data, targetMBR) {
    if (!node.mbr.overlaps(targetMBR)) {
      return null;
    } 
    if (node.isLeaf) {
      // 1：在叶子节点中查找匹配的数据
      const found = node.children.some(child => 
        child.data === data && this._mbrEquals(child.mbr, targetMBR) 
      );
      return found ? node : null;
    } else {
      // 2：在内部节点中递归查找
      for (let child of node.children) {
        const result = this._findLeaf(child, data, targetMBR);
        if (result) return result;
      }
    }
    return null;
  }
  // ============ 处理下溢 ============
  _handleUnderflow(node) {
    console.log(`🔄 处理下溢: ${node.mbr.toString()}`);
    
    // 1：尝试重新分配（从兄弟节点借对象）
    if (this._tryRedistribute(node)) {
      console.log(`✅ 通过重新分配解决下溢`);
      return;
    }
    // 2：如果重新分配失败，执行节点合并
    console.log(`🔄 重新分配失败，执行节点合并`);
    this._mergeNodes(node); 
  }
  // ============ 尝试重新分配 ============
  _tryRedistribute(node) {
    const parent = node.parent;
    if (!parent) return false;
    // 1：找到所有兄弟节点
    const siblings = parent.children.filter(sibling =>sibling !== node);
    for (let sibling of siblings) {
      // 2：检查兄弟节点是否可以借出对象而不导致自己下溢
      if (sibling.children.length > this.minEntries) {
        console.log(`🔄 从兄弟节点借对象`);
        // 3：选择要转移的对象（通常选择距离最远的）
        const objectsToTransfer = this._selectObjectsForTransfer(sibling, node);
        // 4：将对象转移到下溢节点
        node.children.push(...objectsToTransfer); 
        // 5：更新两个节点的MBR
        this._updateMBR(sibling);  
        this._updateMBR(node);   
        return true;
      }
    }
    return false;
  }
  // ============ 选择要转移的对象 ============
  _selectObjectsForTransfer(fromNode, toNode) {
    // 1：按到目标节点中心的距离排序，选择最远的对象
    const center = toNode.mbr.getCenter(); // 1. 计算目标节点的中心
    //2. 计算每个对象到中心[1,1]的距离：
    //3. 排序：从远到近
    fromNode.children.sort((a, b) => {
      const distA = this._distanceToPoint(center, a.mbr);
      const distB = this._distanceToPoint(center, b.mbr);
      return  distB - distA; // 填空：排序顺序
    });
    // 4：选择要转移的对象数量（通常1个）
    const count = 1;
    // 5. 取出最远的1个对象//优化空间布局，让两个节点的MBR更加分离
    //对借出节点：失去最远的对象 → MBR收缩更明显:对借入节点;获得最远的对象 → 但这是临时的重新分配，后续可能再次调整;整体效果：让两个节点的空间覆盖更加分离
    //优化空间布局，而不是直觉上的"把合适的对象放到合适的位置";这是R*树为了长期性能做的权衡
    return fromNode.children.splice(0, count);
  }
  // ============ 节点合并 ============
  _mergeNodes(node) {
    const parent = node.parent;
    if (!parent) return;
    console.log(`🔀 合并节点: ${node.mbr.toString()}`);
    // 1：找到最适合合并的兄弟节点
    const bestSibling = this._findBestSiblingForMerge(node);
    if (bestSibling) {
      // 2：将下溢节点的所有对象转移到兄弟节点
       bestSibling.children.push(...node.children);//使用展开运算符 ... 转移所有对象
      // 3：从父节点中移除下溢节点
      const nodeIndex = parent.children.indexOf(node);
      parent.children.splice(nodeIndex, 1); 
      // 4：更新兄弟节点的MBR
      this._updateMBR(bestSibling);
      // 5：检查父节点是否因此下溢
      if (parent.children.length < this.minEntries && parent !== this.root) {
        console.log(`⚠️ 父节点下溢，递归处理`);
        this._handleUnderflow(parent);
      } else {
        // 6：更新父节点的MBR
         //this._updateMBR(parent);  // ❌ 如果leafNode.parent为null会出错
         if (leafNode.parent) {
            this._updateMBR(leafNode.parent);  // ✅ 安全访问
            }
      }
    }
  }
  // ============ 查找最适合合并的兄弟节点 ============
  _findBestSiblingForMerge(node) {
    const parent = node.parent;
    let bestSibling = null;
    let bestCost = Infinity;
    for (let sibling of parent.children) {
      if (sibling === node) continue;
      // 1：计算合并后的MBR
      const mergedMBR = sibling.mbr.clone();
      mergedMBR.extend(node.mbr);
      // 2：计算合并成本（通常使用面积增量）
      const cost =  mergedMBR.area - sibling.mbr.area;;
      if (cost < bestCost) {
        bestCost = cost;
        bestSibling = sibling;
      }
    }
    return bestSibling;
  }
  // ============ 工具方法 ============
  _mbrEquals(mbr1, mbr2) {//判断两个MBR（最小边界矩形）是否相等的工具方法//min数组完全相等且max数组完全相等
    //这个方法确保了基于值的深度比较，而不是基于引用的浅比较
    //删除时精确匹配数据和位置;//既要数据标识相同，又要空间位置相同
    return mbr1.min.every((val, i) => val === mbr2.min[i]) &&//判断两个MBR（最小边界矩形）是否相等的工具方法//val: mbr1.min数组的当前元素值
           mbr1.max.every((val, i) => val === mbr2.max[i]);//i: 当前索引位置//val === mbr2.min[i]: 比较mbr1和mbr2在相同位置的min值
  }
  }
  
// ============ 完整测试验证 ============//
function comprehensiveTest() {
  console.log("🚀 开始完整R*树测试");
  const tree = new RStarTree(4);
  // 测试1: 插入测试
  console.log("\n📥 测试1: 插入操作");
  const testData = [
    ["A", [1, 1]], ["B", [2, 2]], ["C", [3, 3]], ["D", [4, 4]],
    ["E", [5, 5]], ["F", [6, 6]], ["G", [7, 7]], ["H", [8, 8]]
  ];
  testData.forEach(([name, coords]) => {
    tree.insert(name, coords);
    console.log(`插入 ${name} 完成`);
  });
  // 测试2: 查询测试
  console.log("\n🔍 测试2: 查询操作");
  const query1 = tree.search(new MBR([2, 2], [5, 5]));
  console.log(`查询区域 [2,2]-[5,5]: [${query1.join(", ")}]`);
  
  const query2 = tree.search(new MBR([0, 0], [10, 10]));
  console.log(`查询所有数据: [${query2.join(", ")}]`);
  // 测试3: 删除测试
  console.log("\n🗑️ 测试3: 删除操作");
  console.log("删除 B(2,2):", tree.delete("B", [2, 2]) ? "成功" : "失败");
  console.log("删除 F(6,6):", tree.delete("F", [6, 6]) ? "成功" : "失败");
  
  // 验证删除后的查询
  const query3 = tree.search(new MBR([0, 0], [10, 10]));
  console.log(`删除后剩余数据: [${query3.join(", ")}]`);
  
  // 测试4: 边界测试
  console.log("\n⚠️ 测试4: 边界情况");
  console.log("删除不存在的数据:", tree.delete("XXX", [99, 99]) ? "错误" : "正确");
  console.log("查询空区域:", tree.search(new MBR([100, 100], [101, 101])));
  
  // 测试5: 性能测试
  console.log("\n⚡ 测试5: 批量操作");
  for (let i = 0; i < 10; i++) {
    tree.insert(`X${i}`, [Math.random() * 10, Math.random() * 10]);
  }
  console.log("批量插入完成");
  
  const finalQuery = tree.search(new MBR([0, 0], [10, 10]));
  console.log(`最终数据量: ${finalQuery.length}`);
  
  console.log("\n✅ 所有测试完成!");
  return tree;
}

// 运行完整测试
// 🎯 添加这行：调用测试函数
console.log("=== 开始执行完整测试 ===");
const finalTree = comprehensiveTest();
// 树结构可视化
function visualizeTree(tree) {
  console.log("\n🌳 树结构可视化:");
  function printNode(node, depth = 0) {
    const indent = "  ".repeat(depth);
    const type = node.isLeaf ? "叶子" : "内部";
    console.log(`${indent}${type}节点: ${node.mbr.toString()}`);
    
    if (node.isLeaf) {
      console.log(`${indent}  数据: [${node.children.map(c => c.data).join(", ")}]`);
    } else {
      console.log(`${indent}  子节点数: ${node.children.length}`);
      node.children.forEach(child => printNode(child, depth + 1));
    }
  }
  printNode(tree.root);
}

// 可视化最终树结构
visualizeTree(finalTree);
```
```
//-------优化版本--------//
// 完整的R*树实现
class MBR {
  constructor(min, max) {
    if (min === undefined && max === undefined) {
      this.min = [Infinity, Infinity];
      this.max = [-Infinity, -Infinity];
    } else if (typeof min === 'number' && max === undefined) {
      this.min = new Array(min).fill(Infinity);
      this.max = new Array(min).fill(-Infinity);
    } else if (Array.isArray(min) && Array.isArray(max)) {
      if (min.length !== max.length) {
        throw new Error("min和max维度必须相同");
      }
      this.min = min.slice();
      this.max = max.slice();
    } else {
      throw new Error("参数不合法：请提供维度数字或min/max数组");
    }
    this.dimension = this.min.length;
  }

  clone() {
    return new MBR(this.min.slice(), this.max.slice());
  }

  getCenter() {
    const center = [];
    for (let i = 0; i < this.min.length; i++) {
      center.push((this.min[i] + this.max[i]) / 2);
    }
    return center;
  }

  extend(other) {
    if (this.dimension !== other.dimension) {
      throw new Error(`维度不匹配: ${this.dimension}D vs ${other.dimension}D`);
    }
    for (let i = 0; i < this.dimension; i++) {
      this.min[i] = Math.min(this.min[i], other.min[i]);
      this.max[i] = Math.max(this.max[i], other.max[i]);
    }
    return this;
  }

  toString() {
    return `MBR(${this.dimension}D): [${this.min}] -> [${this.max}]`;
  }

  get area() {
    let area = 1;
    for (let i = 0; i < this.min.length; i++) {
      const side = this.max[i] - this.min[i];
      area *= side;
    }
    return area;
  }

  get margin() {
    let sumOfSides = 0;
    for (let i = 0; i < this.dimension; i++) {
      sumOfSides += (this.max[i] - this.min[i]);
    }
    return 2 * sumOfSides;
  }

  overlaps(other) {
    for (let i = 0; i < this.min.length; i++) {
      if (this.max[i] < other.min[i] || this.min[i] > other.max[i]) {
        return false;
      }
    }
    return true;
  }

  contains(other) {
    for (let i = 0; i < this.min.length; i++) {
      if (this.min[i] > other.min[i] || this.max[i] < other.max[i]) {
        return false;
      }
    }
    return true;
  }
}

class RStarTreeNode {
  constructor(isLeaf = false, mbr = new MBR(2)) {
    this.isLeaf = isLeaf;
    this.mbr = mbr;
    this.children = [];
    this.parent = null;
    this.data = null; // 仅叶子节点使用
  }
}

class RStarTree {
  constructor(maxEntries = 4) {
    this.root = new RStarTreeNode(true);
    this.maxEntries = maxEntries;
    this.minEntries = Math.floor(maxEntries / 2);
    this.reinsertInProgress = false;
  }

  // ============ 插入操作 ============
  insert(data, coordinates) {
    const dataNode = new RStarTreeNode(true);
    dataNode.mbr = new MBR(coordinates, coordinates);
    dataNode.data = data;
    this._insert(dataNode, this.root, 0);
  }

  _insert(dataNode, currentNode, depth) {
    if (currentNode.isLeaf) {
      currentNode.children.push(dataNode);
      dataNode.parent = currentNode;
      this._updateMBR(currentNode);

      if (currentNode.children.length > this.maxEntries) {
        this._handleOverflow(currentNode, depth);
      }
    } else {
      const chosenChild = this._chooseSubtree(dataNode, currentNode);
      this._insert(dataNode, chosenChild, depth + 1);
    }
    this._updateMBR(currentNode);
  }

  _chooseSubtree(dataNode, node) {
    let bestChild = null;
    let bestCost = Infinity;

    for (let child of node.children) {
      const enlargedMBR = child.mbr.clone();
      enlargedMBR.extend(dataNode.mbr);
      
      const areaIncrease = enlargedMBR.area - child.mbr.area;
      const overlapIncrease = this._computeOverlapIncrease(node, child, dataNode);
      const cost = areaIncrease + overlapIncrease;

      if (cost < bestCost) {
        bestCost = cost;
        bestChild = child;
      }
    }
    return bestChild;
  }

  _computeOverlapIncrease(parent, child, newEntry) {
    let overlapIncrease = 0;
    const enlargedMBR = child.mbr.clone();
    enlargedMBR.extend(newEntry.mbr);

    for (let sibling of parent.children) {
      if (sibling !== child) {
        const currentOverlap = this._computeOverlap(child.mbr, sibling.mbr);
        const newOverlap = this._computeOverlap(enlargedMBR, sibling.mbr);
        overlapIncrease += Math.max(0, newOverlap - currentOverlap);
      }
    }
    return overlapIncrease;
  }

  _computeOverlap(mbr1, mbr2) {
    if (!mbr1.overlaps(mbr2)) return 0;
    
    let overlap = 1;
    for (let i = 0; i < mbr1.min.length; i++) {
      const minOverlap = Math.max(mbr1.min[i], mbr2.min[i]);
      const maxOverlap = Math.min(mbr1.max[i], mbr2.max[i]);
      overlap *= Math.max(0, maxOverlap - minOverlap);
    }
    return overlap;
  }

  _handleOverflow(node, depth) {
    if (depth < 2 && !this.reinsertInProgress) {
      const removedEntries = this._selectReinsertEntries(node);
      if (removedEntries.length > 0) {
        this.reinsertInProgress = true;
        this._reinsert(removedEntries, depth);
        this.reinsertInProgress = false;
      }
      
      if (node.children.length > this.maxEntries) {
        this._splitNode(node);
      }
    } else {
      this._splitNode(node);
    }
  }

  _selectReinsertEntries(node) {
    const entries = node.children;
    let p = Math.floor(entries.length * 0.3);
    p = Math.max(1, p);
    p = Math.min(p, entries.length - this.minEntries);

    const center = node.mbr.getCenter();
    entries.sort((a, b) => {
      const distA = this._distanceToPoint(center, a.mbr);
      const distB = this._distanceToPoint(center, b.mbr);
      return distB - distA;
    });

    const removed = entries.splice(0, p);
    this._updateMBR(node);
    return removed;
  }

  _reinsert(entries, depth) {
    for (let entry of entries) {
      entry.parent = null;
      this._insert(entry, this.root, 0);
    }
  }

  _splitNode(node) {
    let bestAxis = 0;
    let bestSplitIndex = 0;
    let bestCost = Infinity;

    for (let axis = 0; axis < node.mbr.min.length; axis++) {
      node.children.sort((a, b) => {
        const centerA = (a.mbr.min[axis] + a.mbr.max[axis]) / 2;
        const centerB = (b.mbr.min[axis] + b.mbr.max[axis]) / 2;
        return centerA - centerB;
      });

      for (let i = this.minEntries; i <= node.children.length - this.minEntries; i++) {
        const group1 = node.children.slice(0, i);
        const group2 = node.children.slice(i);
        
        const mbr1 = this._computeGroupMBR(group1);
        const mbr2 = this._computeGroupMBR(group2);
        
        const areaSum = mbr1.area + mbr2.area;
        const marginSum = mbr1.margin + mbr2.margin;
        const cost = areaSum * marginSum;

        if (cost < bestCost) {
          bestCost = cost;
          bestAxis = axis;
          bestSplitIndex = i;
        }
      }
    }

    this._performSplit(node, bestAxis, bestSplitIndex);
  }

  _performSplit(node, axis, splitIndex) {
    node.children.sort((a, b) => {
      const centerA = (a.mbr.min[axis] + a.mbr.max[axis]) / 2;
      const centerB = (b.mbr.min[axis] + b.mbr.max[axis]) / 2;
      return centerA - centerB;
    });

    const group1 = node.children.slice(0, splitIndex);
    const group2 = node.children.slice(splitIndex);
    
    const newNode = new RStarTreeNode(node.isLeaf);
    newNode.children = group2;
    newNode.parent = node.parent;
    
    node.children = group1;

    this._updateMBR(node);
    this._updateMBR(newNode);

    if (node === this.root) {
      const newRoot = new RStarTreeNode(false);
      newRoot.children = [node, newNode];
      node.parent = newRoot;
      newNode.parent = newRoot;
      this._updateMBR(newRoot);
      this.root = newRoot;
    } else {
      node.parent.children.push(newNode);
      if (node.parent.children.length > this.maxEntries) {
        this._handleOverflow(node.parent, this._getDepth(node.parent));
      }
    }
  }

  // ============ 查询操作 ============
  search(queryMBR) {
    const results = [];
    this._searchRecursive(this.root, queryMBR, results);
    return results;
  }

  _searchRecursive(node, queryMBR, results) {
    if (!node.mbr.overlaps(queryMBR)) {
      return;
    }

    if (node.isLeaf) {
      for (let child of node.children) {
        if (child.mbr.overlaps(queryMBR)) {
          results.push(child.data);
        }
      }
    } else {
      for (let child of node.children) {
        this._searchRecursive(child, queryMBR, results);
      }
    }
  }

  // ============ 删除操作 ============
  delete(data, coordinates) {
    const targetMBR = new MBR(coordinates, coordinates);
    const leafNode = this._findLeaf(this.root, data, targetMBR);
    
    if (!leafNode) {
      return false;
    }

    const index = leafNode.children.findIndex(child => 
      child.data === data && this._mbrEquals(child.mbr, targetMBR)
    );

    if (index === -1) {
      return false;
    }

    leafNode.children.splice(index, 1);
    this._updateMBR(leafNode);

    if (leafNode.children.length < this.minEntries && leafNode !== this.root) {
      this._handleUnderflow(leafNode);
    } else if (leafNode.parent) {
      this._updateMBR(leafNode.parent);
    }

    return true;
  }

  _findLeaf(node, data, targetMBR) {
    if (!node.mbr.overlaps(targetMBR)) {
      return null;
    }

    if (node.isLeaf) {
      const found = node.children.some(child => 
        child.data === data && this._mbrEquals(child.mbr, targetMBR)
      );
      return found ? node : null;
    } else {
      for (let child of node.children) {
        const result = this._findLeaf(child, data, targetMBR);
        if (result) return result;
      }
    }
    return null;
  }

  _handleUnderflow(node) {
    if (this._tryRedistribute(node)) {
      return;
    }
    this._mergeNodes(node);
  }

  _tryRedistribute(node) {
    const parent = node.parent;
    if (!parent) return false;

    const siblings = parent.children.filter(sibling => sibling !== node);

    for (let sibling of siblings) {
      if (sibling.children.length > this.minEntries) {
        const objectsToTransfer = this._selectObjectsForTransfer(sibling, node);
        node.children.push(...objectsToTransfer);
        
        this._updateMBR(sibling);
        this._updateMBR(node);
        return true;
      }
    }
    return false;
  }

  _selectObjectsForTransfer(fromNode, toNode) {
    const center = toNode.mbr.getCenter();
    fromNode.children.sort((a, b) => {
      const distA = this._distanceToPoint(center, a.mbr);
      const distB = this._distanceToPoint(center, b.mbr);
      return distB - distA;
    });

    const count = 1;
    return fromNode.children.splice(0, count);
  }

  _mergeNodes(node) {
    const parent = node.parent;
    if (!parent) return;

    const bestSibling = this._findBestSiblingForMerge(node);
    if (!bestSibling) return;

    bestSibling.children.push(...node.children);
    
    const nodeIndex = parent.children.indexOf(node);
    parent.children.splice(nodeIndex, 1);
    
    this._updateMBR(bestSibling);

    if (parent.children.length < this.minEntries && parent !== this.root) {
      this._handleUnderflow(parent);
    } else {
      this._updateMBR(parent);
    }
  }

  _findBestSiblingForMerge(node) {
    const parent = node.parent;
    let bestSibling = null;
    let bestCost = Infinity;

    for (let sibling of parent.children) {
      if (sibling === node) continue;

      const mergedMBR = sibling.mbr.clone();
      mergedMBR.extend(node.mbr);
      const cost = mergedMBR.area - sibling.mbr.area;

      if (cost < bestCost) {
        bestCost = cost;
        bestSibling = sibling;
      }
    }
    return bestSibling;
  }

  // ============ 工具方法 ============
  _updateMBR(node) {
    if (!node || node.children.length === 0) return;

    const firstChild = node.children[0];
    node.mbr = firstChild.mbr.clone();

    for (let i = 1; i < node.children.length; i++) {
      node.mbr.extend(node.children[i].mbr);
    }

    if (node.parent) {
      this._updateMBR(node.parent);
    }
  }

  _computeGroupMBR(entries) {
    if (entries.length === 0) return new MBR(2);
    
    const mbr = entries[0].mbr.clone();
    for (let i = 1; i < entries.length; i++) {
      mbr.extend(entries[i].mbr);
    }
    return mbr;
  }

  _distanceToPoint(point, mbr) {
    let dist = 0;
    for (let i = 0; i < point.length; i++) {
      const p = point[i];
      if (p < mbr.min[i]) {
        dist += (mbr.min[i] - p) ** 2;
      } else if (p > mbr.max[i]) {
        dist += (p - mbr.max[i]) ** 2;
      }
    }
    return Math.sqrt(dist);
  }

  _getDepth(node) {
    let depth = 0;
    while (node && !node.isLeaf) {
      depth++;
      node = node.children[0];
    }
    return depth;
  }

  _mbrEquals(mbr1, mbr2) {
    return mbr1.min.every((val, i) => val === mbr2.min[i]) &&
           mbr1.max.every((val, i) => val === mbr2.max[i]);
  }
}

// ============ 完整测试验证 ============
function comprehensiveTest() {
  console.log("🚀 开始完整R*树测试");
  
  const tree = new RStarTree(4);
  
  // 测试1: 插入测试
  console.log("\n📥 测试1: 插入操作");
  const testData = [
    ["A", [1, 1]], ["B", [2, 2]], ["C", [3, 3]], ["D", [4, 4]],
    ["E", [5, 5]], ["F", [6, 6]], ["G", [7, 7]], ["H", [8, 8]]
  ];
  
  testData.forEach(([name, coords]) => {
    tree.insert(name, coords);
    console.log(`插入 ${name} 完成`);
  });
  
  // 测试2: 查询测试
  console.log("\n🔍 测试2: 查询操作");
  const query1 = tree.search(new MBR([2, 2], [5, 5]));
  console.log(`查询区域 [2,2]-[5,5]: [${query1.join(", ")}]`);
  
  const query2 = tree.search(new MBR([0, 0], [10, 10]));
  console.log(`查询所有数据: [${query2.join(", ")}]`);
  
  // 测试3: 删除测试
  console.log("\n🗑️ 测试3: 删除操作");
  console.log("删除 B(2,2):", tree.delete("B", [2, 2]) ? "成功" : "失败");
  console.log("删除 F(6,6):", tree.delete("F", [6, 6]) ? "成功" : "失败");
  
  // 验证删除后的查询
  const query3 = tree.search(new MBR([0, 0], [10, 10]));
  console.log(`删除后剩余数据: [${query3.join(", ")}]`);
  
  // 测试4: 边界测试
  console.log("\n⚠️ 测试4: 边界情况");
  console.log("删除不存在的数据:", tree.delete("XXX", [99, 99]) ? "错误" : "正确");
  console.log("查询空区域:", tree.search(new MBR([100, 100], [101, 101])));
  
  // 测试5: 性能测试
  console.log("\n⚡ 测试5: 批量操作");
  for (let i = 0; i < 10; i++) {
    tree.insert(`X${i}`, [Math.random() * 10, Math.random() * 10]);
  }
  console.log("批量插入完成");
  
  const finalQuery = tree.search(new MBR([0, 0], [10, 10]));
  console.log(`最终数据量: ${finalQuery.length}`);
  
  console.log("\n✅ 所有测试完成!");
  return tree;
}

// 运行完整测试
const finalTree = comprehensiveTest();

// 树结构可视化
function visualizeTree(tree) {
  console.log("\n🌳 树结构可视化:");
  function printNode(node, depth = 0) {
    const indent = "  ".repeat(depth);
    const type = node.isLeaf ? "叶子" : "内部";
    console.log(`${indent}${type}节点: ${node.mbr.toString()}`);
    
    if (node.isLeaf) {
      console.log(`${indent}  数据: [${node.children.map(c => c.data).join(", ")}]`);
    } else {
      console.log(`${indent}  子节点数: ${node.children.length}`);
      node.children.forEach(child => printNode(child, depth + 1));
    }
  }
  printNode(tree.root);
}

// 可视化最终树结构
visualizeTree(finalTree);
```