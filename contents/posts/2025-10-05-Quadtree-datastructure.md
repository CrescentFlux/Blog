# Quardtree
## 基础知识
- **四叉树是一种树形数据结构，其中每个内部节点恰好有四个子节点**
- **四叉树通常用于对二维空间进行递归细分，通过将空间区域递归地划分为四个等大的象限（quadrants）来实现空间分区**
- 给定一个二维空间区域R，四叉树定义为：
```
如果R满足停止条件(如点数 ≤ 容量阈值)，则作为叶子节点
否则，将 RR 划分为四个不相交的子区域：
R=R_NW U R_NE U R_SW U R_SE
R=R_NW U R_NE U R_SW U R_SE​
其中每个R∗是R的四分之一，然后递归构建子树
```
## 注意事项
1. **混淆点**
- **中心点定义:Rectangle是用中心点(x, y)和宽度(w)、高度(h)来定义：达到四叉树分裂时的计算简洁性**
- **工程中的权衡：为了更复杂的操作分裂的简洁性，接受简单操作包含判断的稍微复杂性**
- **userData 属性**
```
分离空间管理和业务数据；四叉树只管理空间，业务数据通过userData关联
1. 关注点分离:四叉树只负责：空间索引;userData负责：业务逻辑
2. 可重用性
3. 灵活性:业务数据可以是任何类型
4. 性能优化:四叉树在内部进行空间分割时，只需要拷贝轻量的Point对象，而不需要拷贝沉重的业务数据;两者通过清晰的接口协作。
```
- **删除复杂性**
```
1. 点匹配问题
2. 性能权衡
立即合并：删除时立即检查合并，保持树紧凑
延迟合并：定期或批量合并，提高删除性能
永不合并：简单但可能导致树过于稀疏
3.四叉树的删除流程包含两个主要部分：
点删除：递归找到点并从叶子节点中删除
节点合并：删除后检查是否可以将四个子节点合并回父节点
```
- **核心优势**

|核心优势|内容|
---|---
|空间划分|专门为二维空间数据设计|
|递归结构|自顶向下的递归细分|
|均匀分割|每次划分产生四个等大的矩形区域|
|自适应|根据数据密度自动调整划分粒度|
|高效|查询时利用四叉树的空间结构快速跳过无关区域|
|单一职责|1.叶子节点：负责存储数据;<br>2.内部节点：负责四个子节点;<br>3.通过divided标志和points数组的状态，立即判断节点类型<br>|
|性能优势|用不相交来判断：<br>1.正面判断相交需要检查多种重叠情况<br>2.反面判断不相交只需要检查4种简单情况<br>3.一旦发现任何一种不相交情况，就可以立即返回，不需要检查其他条件<br>4.用极低的成本（一次矩形比较），排除掉大片肯定不相关的区域，让我们只需要在极小的相关区域内进行精细搜索<br>|

- **四叉树节点**

|名称|用途|注意事项|
---|---|---
|根节点|区域划分|根节点的边界要足够大，确保能容纳所有数据|
|内部节点|空间导航|内部节点合并的特点:<br>1.递归性：合并可能触发连锁反应<br>2.条件严格：必须所有直接子节点都是叶子节点<br>3.点数限制：总点数必须 ≤ capacity<br>4.可能停止：合并可能在任何层级停止，不一定会传播到根节点<br>|
|叶子节点|存储数据|注意容量限制|
|共同点|分裂后的节点：<br>1.物理上：不再直接存储数据（points = []）<br>2.逻辑上：仍然存在于树结构中，作为父节点<br>3.管理上：通过四个子区域来间接管理原来的区域<br>|1. 保持结构完整性<br>2. 空间关系的保持:根节点仍然知道整个区域的边界，可以快速进行大范围的空间剪枝<br>3. 递归处理的便利性:每个节点都有统一的接口，不管是叶子节点还是内部节点，都响应同样的insert、query等方法<br>

- **四叉树**

|核心规则|内容|作用|
---|---|---
|递归分裂|1.按需分裂：不预先划分，等到真的需要时才分裂<br>2.递归分裂：分裂会一直向下进行，直到每个叶子节点的点数≤capacity<br>3.角色转变：节点分裂后从"数据存储者"变为"数据路由者"<br>4.容量控制：最终确保每个叶子节点最多有capacity个点<br>|自动在数据密集的区域进行更细的划分，在稀疏的区域保持粗粒度，实现了完美的自适应空间管理|
|容量规则|1.每个叶子节点最多存储capacity个点<br>2.一旦超过capacity，叶子节点就转变为内部节点，不再直接存储点，而是把存储责任交给子节点<br>3.递归分配：分裂后，所有点重新插入到合适的子节点<br>|1.容量触发分裂：当叶子节点的点数超过capacity时自动分裂：<br>- 点被充分分散<br>- 每个子区域点数 ≤ capacity达到最小粒度：有些实现会设置最小区域尺寸<br>- 所有点坐标相同（极端情况） <br>2.动态生长：四叉树根据数据分布自动调整结构<br>3.空间局部性：相近的点会被分到同一个深层节点|

- **关注点对比**

|名称|关注点|内容|
---|---|---
|二叉树|数值关系|主要用于排序和搜索：左子树 < 当前节点 < 右子树|
|四叉树|空间关系|1.用于空间管理和分割：西北区域 ∪ 东北区域 ∪ 西南区域 ∪ 东南区域 = 父区域<br>2.使用相对坐标系<br>3.空间完整性：四个子节点完整覆盖父区域，没有"未分配"的空间<br>4.递归分裂：分裂会向下传递，直到所有叶子节点都满足容量要求<br>5.可能创建空节点：即使某些象限没有点，也会创建对应的空节点<br>6.重新分配后点不一定均匀分布，点的分布完全取决于它们的坐标位置<br>|


- **五种树结构的核心对比**

|特性|	四叉树|	二叉树|	B树|	B+树|	KD树|
---|---|---|---|---|---
|维度|	2D空间|	1D线性|	1D键值|	1D键值|	k维空间|
|子节点数|	4	|2|	m (m≥2)|	m (m≥2)|	2|
|划分方式|	空间四等分|	值比较|	键范围|	键范围	|维度交替划分|
|数据结构|	空间区域|	有序值|	平衡多路|	索引+数据分离|	超平面划分|
|查询类型|	范围查询、空间查询|	精确查找、范围查询	|精确查找|	范围查询、顺序访问	|k近邻、范围查询|
|叶子节点|	存储数据点|	存储数据|	存储数据	|链表连接存储所有数据|	存储数据点|
|内部节点|	空间导航|	比较路由|	存储数据和指针|	纯索引，不存数据	|划分超平面|
|典型应用|	图像处理、空间索引、碰撞检测|	排序、搜索、表达式树|	文件系统、数据库索引|	关系数据库索引|	机器学习、多维搜索|


2. **代码实现**
```
//-----核心逻辑-----//
// 定义四叉树节点的边界
class Rectangle {
  constructor(x, y, w, h) {
    this.x = x; // 边界中心的x坐标
    this.y = y; // 边界中心的y坐标
    this.w = w; // 边界的宽度
    this.h = h; // 边界的高度
  }
  // 关键方法：判断一个点是否在这个矩形边界内
  contains(point) {//同时满足四个条件：点的x坐标在左右边界之间，点的y坐标在上下边界之间
    return (point.x >= this.x - this.w / 2 &&  //矩形的左边界
            point.x <= this.x + this.w / 2 &&  //矩形的右边界
            point.y >= this.y - this.h / 2 &&  //矩形的上边界
            point.y <= this.y + this.h / 2);   //矩形的下边界
  }

  // 关键方法：判断这个矩形是否与另一个矩形相交
  intersects(range) {//通过检查四种简单的不相交情况，来反推两个矩形是否相交。这种方法在计算上更高效，让四叉树能够快速裁剪掉无关的区域
    return !(range.x - range.w / 2 > this.x + this.w / 2 ||//!取反，得到最终结果
             range.x + range.w / 2 < this.x - this.w / 2 ||//必须所有4个条件都为false，两个矩形才相交！
             range.y - range.h / 2 > this.y + this.h / 2 ||//这4个条件是「或」的关系，只要任何一个条件成立，就说明不相交
             range.y + range.h / 2 < this.y - this.h / 2);
  }
}
// 定义一个简单的点类
class Point {
  constructor(x, y, data = null) {
    this.x = x;
    this.y = y;
    this.userData = data; // 可以携带一些自定义数据
  }
}
//定义四叉树节点类
class QuadTree {
  constructor(boundary, capacity) {
    // 1. 这个节点所负责的空间区域
    this.boundary = boundary;
    // 2. 在分裂之前，这个节点最多能容纳多少个点
    this.capacity = capacity;
    // 3. 当前节点中存储的数据点集合;只有叶子节点才会真正在这个数组里存储点;一旦节点分裂，points数组会被清空，数据被"下放"到子节点；
    this.points = [];
    // 4. 节点是否已经分裂
    this.divided = false;
    // 5. 如果分裂，四个子节点指针情况
    this.northwest = null;//null表示还没有分裂
    this.northeast = null;
    this.southwest = null;
    this.southeast = null;
  }
  //--插入--//
  // 1.向四叉树中插入一个点;2.插入顺序只影响何时触发分裂;不影响分裂后点的最终位置3.递归思想:如果当前节点满了就分裂，然后把任务交给更专业的子节点去处理4.分裂后，所有点都按照它们当前的坐标位置和新区域的边界重新分配，与插入顺序完全无关;5.分配只依赖于：点的绝对坐标和当前区域的边界
  insert(point) {
    // 1. 首先检查点是否在本节点的边界内
    if (!this.boundary.contains(point)) {
      return false; // 点不在本节点范围内，插入失败
    }

    // 2. 如果本节点还有容量，并且尚未分裂
    if (this.points.length < this.capacity && !this.divided) {
      this.points.push(point);
      return true;
    }

    // 3. 如果已经达到容量，需要分裂
    if (!this.divided) {
      this.subdivide(); // 分裂当前节点
    }

    // 4. 将新点插入到合适的子节点中
    // 注意：分裂后，当前节点的points不会清空，但新点只会加入到子节点
    if (this.northwest.insert(point)) return true;
    if (this.northeast.insert(point)) return true;
    if (this.southwest.insert(point)) return true;
    if (this.southeast.insert(point)) return true;

    // 理论上不应该执行到这里
    return false;
  }
  //--分裂--//
  //分裂不会无限进行：区域每次分裂变小一半；点会逐渐被分散到不同子区域；最终每个叶子节点的点数都会 ≤ capacity
  // 分裂当前节点
  subdivide() {
    const x = this.boundary.x;
    const y = this.boundary.y;
    const w = this.boundary.w / 2;
    const h = this.boundary.h / 2;

    // 创建四个子区域
    const nw = new Rectangle(x - w/2, y - h/2, w, h);
    const ne = new Rectangle(x + w/2, y - h/2, w, h);
    const sw = new Rectangle(x - w/2, y + h/2, w, h);
    const se = new Rectangle(x + w/2, y + h/2, w, h);

    // 创建四个子节点
    this.northwest = new QuadTree(nw, this.capacity);
    this.northeast = new QuadTree(ne, this.capacity);
    this.southwest = new QuadTree(sw, this.capacity);
    this.southeast = new QuadTree(se, this.capacity);

    this.divided = true;
    
    // 将当前节点中的点重新分配到子节点中
    for (let point of this.points) {
      this.northwest.insert(point);
      this.northeast.insert(point);
      this.southwest.insert(point);
      this.southeast.insert(point);
    }
    
    // 清空当前节点的点列表（因为点已经下放到子节点了）
    this.points = [];
  }
  //--查询--//
  //1.快速剪枝：通过矩形相交检查，跳过整个不相关的子树；2.局部搜索：只在可能与查询范围相交的区域进行精细搜索3.层次优化：从大范围到小范围，逐步缩小搜索范围4.查询需要深入到所有层级
  // 查询在给定范围内的所有点
  query(range, found = []) {
    // 1. 如果查询范围与当前节点边界不相交，直接返回
    if (!this.boundary.intersects(range)) {//在递归早期就跳过整棵子树，避免不必要的计算
      return found;
    }
    // 2. 检查当前节点存储的点（如果是叶子节点）
    for (let point of this.points) {
      if (range.contains(point)) {
        found.push(point);
      }
    }
    // 3. 如果当前节点已经分裂，递归检查所有子节点
    if (this.divided) {//让查询能够从根节点开始，沿着树的层级结构一直深入到最底层的叶子节点，确保不遗漏任何可能包含在查询范围内的点
      this.northwest.query(range, found);
      this.northeast.query(range, found);
      this.southwest.query(range, found);
      this.southeast.query(range, found);
    }
    return found;
  }
  //--删除--//
  //内部节点的删除和合并过程：1.删除叶子节点中的点2.父节点检查合并条件3.如果满足条件，内部节点变回叶子节点4.合并可能继续向上传播，也可能在某一层停止
  remove(point) {
  if (!this.boundary.contains(point)) return false;
  let removed = false;
  if (!this.divided) {
    // 叶子节点：直接删除点
    const index = this.points.findIndex(p => p.x === point.x && p.y === point.y);
    if (index > -1) {
      this.points.splice(index, 1);
      removed = true;
    }
  } else {
    // 内部节点：递归删除
    if (this.northwest.remove(point)) removed = true;
    else if (this.northeast.remove(point)) removed = true;
    else if (this.southwest.remove(point)) removed = true;
    else if (this.southeast.remove(point)) removed = true;
    
    //🎯关键：检查是否需要合并
    if (removed) {
      this.tryMerge();
    }
  }
  
  return removed;
}

tryMerge(){
    //检查过程：总点数 <= capacity
    if (this.divided &&//检查1：当前节点必须是内部节点（已经分裂过）divided = true → 我是内部节点，有四个子节点；divided = false → 我是叶子节点，没有子节点，不需要合并
      //2.四个子节点都必须是叶子节点
    !this.northwest.divided &&!this.northeast.divided &&!this.southwest.divided &&!this.southeast.divided) {//只能合并"扁平"的结构;确保合并的安全性
      //3.计算总点数
    const totalPoints =this.northwest.points.length +this.northeast.points.length +this.southwest.points.length +this.southeast.points.length;
    //4.释放过程
    if (totalPoints <= this.capacity) {
      //4.1. 先收集所有子节点的数据
      this.points = [
        ...this.northwest.points,//扩展运算符:数组展开语法，用于合并多个数组
        ...this.northeast.points,
        ...this.southwest.points,
        ...this.southeast.points
      ];
      //4.2. 释放子节点//避免内存泄漏和保持数据结构一致性
      this.northwest = null;
      this.northeast = null;
      this.southwest = null;
      this.southeast = null;
      this.divided = false;
      //4.3. 更新状态标志
      this.divided = false; 
    }
  }
}
}
```
```
//-----测试------//
// ==================== 四叉树核心类定义 ====================
class Rectangle {
    constructor(x, y, w, h) {
        this.x = x; this.y = y; this.w = w; this.h = h;
    }
    contains(point) {
        return point.x >= this.x - this.w/2 &&
               point.x <= this.x + this.w/2 &&
               point.y >= this.y - this.h/2 &&
               point.y <= this.y + this.h/2;
    }
    
    intersects(range) {
        return !(range.x - range.w/2 > this.x + this.w/2 ||
                 range.x + range.w/2 < this.x - this.w/2 ||
                 range.y - range.h/2 > this.y + this.h/2 ||
                 range.y + range.h/2 < this.y - this.h/2);
    }
    
    toString() {
        return `Rectangle(center:(${this.x},${this.y}), size:${this.w}x${this.h})`;
    }
}

class Point {
    constructor(x, y, data = null) {
        this.x = x; this.y = y; this.userData = data;
    }
    
    toString() {
        return `Point(${this.x},${this.y})`;
    }
}

class QuadTree {
    constructor(boundary, capacity) {
        this.boundary = boundary;
        this.capacity = capacity;
        this.points = [];
        this.divided = false;
        this.northwest = null;
        this.northeast = null;
        this.southwest = null;
        this.southeast = null;
    }

    insert(point) {
        if (!this.boundary.contains(point)) {
            console.log(`❌ 点 ${point} 不在边界 ${this.boundary} 内`);
            return false;
        }
        
        if (!this.divided && this.points.length < this.capacity) {
            this.points.push(point);
            console.log(`✅ 插入 ${point} 到叶子节点，当前点数: ${this.points.length}`);
            return true;
        }
        
        if (!this.divided) {
            console.log(`🔄 节点已满 (${this.points.length}/${this.capacity})，开始分裂...`);
            this.subdivide();
        }
        
        console.log(`🔍 将 ${point} 路由到子节点`);
        if (this.northwest.insert(point)) return true;
        if (this.northeast.insert(point)) return true;
        if (this.southwest.insert(point)) return true;
        if (this.southeast.insert(point)) return true;
        
        return false;
    }

    subdivide() {
        const x = this.boundary.x;
        const y = this.boundary.y;
        const w = this.boundary.w / 2;
        const h = this.boundary.h / 2;
        
        const nw = new Rectangle(x - w/2, y - h/2, w, h);
        const ne = new Rectangle(x + w/2, y - h/2, w, h);
        const sw = new Rectangle(x - w/2, y + h/2, w, h);
        const se = new Rectangle(x + w/2, y + h/2, w, h);
        
        this.northwest = new QuadTree(nw, this.capacity);
        this.northeast = new QuadTree(ne, this.capacity);
        this.southwest = new QuadTree(sw, this.capacity);
        this.southeast = new QuadTree(se, this.capacity);
        this.divided = true;
        
        console.log(`🎯 分裂完成，创建4个子节点`);
        
        // 重新分配现有点到子节点
        for (let point of this.points) {
            this.northwest.insert(point);
            this.northeast.insert(point);
            this.southwest.insert(point);
            this.southeast.insert(point);
        }
        this.points = [];
    }

    query(range, found = []) {
        if (!this.boundary.intersects(range)) {
            console.log(`🚫 跳过节点 ${this.boundary}，与查询范围不相交`);
            return found;
        }
        
        console.log(`🔍 检查节点 ${this.boundary}`);
        
        if (!this.divided) {
            for (let point of this.points) {
                if (range.contains(point)) {
                    found.push(point);
                    console.log(`✅ 找到点 ${point}`);
                }
            }
        } else {
            console.log(`↘️ 递归查询子节点...`);
            this.northwest.query(range, found);
            this.northeast.query(range, found);
            this.southwest.query(range, found);
            this.southeast.query(range, found);
        }
        
        return found;
    }

    remove(point) {
        if (!this.boundary.contains(point)) {
            console.log(`❌ 点 ${point} 不在边界内`);
            return false;
        }
        
        let removed = false;
        
        if (!this.divided) {
            const index = this.points.findIndex(p => 
                p.x === point.x && p.y === point.y);
            if (index > -1) {
                this.points.splice(index, 1);
                removed = true;
                console.log(`🗑️ 从叶子节点删除 ${point}，剩余点数: ${this.points.length}`);
            }
        } else {
            console.log(`🔍 在子节点中查找要删除的点 ${point}`);
            if (this.northwest.remove(point)) removed = true;
            else if (this.northeast.remove(point)) removed = true;
            else if (this.southwest.remove(point)) removed = true;
            else if (this.southeast.remove(point)) removed = true;
            
            if (removed) {
                console.log(`🔄 删除成功，检查合并条件...`);
                this.tryMerge();
            }
        }
        
        return removed;
    }

    tryMerge() {
        if (this.divided &&
            !this.northwest.divided &&
            !this.northeast.divided &&
            !this.southwest.divided &&
            !this.southeast.divided) {
            
            const totalPoints = 
                this.northwest.points.length +
                this.northeast.points.length +
                this.southwest.points.length +
                this.southeast.points.length;
            
            console.log(`📊 合并检查: 总点数=${totalPoints}, 容量=${this.capacity}`);
            
            if (totalPoints <= this.capacity) {
                this.points = [
                    ...this.northwest.points,
                    ...this.northeast.points,
                    ...this.southwest.points,
                    ...this.southeast.points
                ];
                
                this.northwest = null;
                this.northeast = null;
                this.southwest = null;
                this.southeast = null;
                this.divided = false;
                
                console.log(`🎉 合并完成！节点变为叶子节点，点数: ${this.points.length}`);
            }
        }
    }

    // 工具方法：获取所有点
    getAllPoints() {
        let allPoints = [...this.points];
        if (this.divided) {
            allPoints = allPoints.concat(this.northwest.getAllPoints());
            allPoints = allPoints.concat(this.northeast.getAllPoints());
            allPoints = allPoints.concat(this.southwest.getAllPoints());
            allPoints = allPoints.concat(this.southeast.getAllPoints());
        }
        return allPoints;
    }

    // 工具方法：打印树结构
    printTree(level = 0) {
        const indent = '  '.repeat(level);
        const nodeType = this.divided ? '内部节点' : '叶子节点';
        console.log(`${indent}${nodeType} ${this.boundary} - 点数: ${this.points.length}`);
        
        if (this.divided) {
            this.northwest.printTree(level + 1);
            this.northeast.printTree(level + 1);
            this.southwest.printTree(level + 1);
            this.southeast.printTree(level + 1);
        }
    }
}

// ==================== 测试代码 ====================
console.log('🚀 开始四叉树测试...\n');

// 1. 创建四叉树
const boundary = new Rectangle(50, 50, 100, 100); // 中心(50,50), 100x100区域
const quadtree = new QuadTree(boundary, 3); // 容量为3
console.log('✅ 创建四叉树:', quadtree.boundary.toString(), '容量: 3\n');

// 2. 插入测试
console.log('📥 插入点测试:');
const points = [
    new Point(10, 10),  // A - NW
    new Point(20, 20),  // B - NW  
    new Point(30, 30),  // C - NW
    new Point(80, 10),  // D - NE
    new Point(10, 80),  // E - SW
    new Point(80, 80)   // F - SE
];

points.forEach(point => {
    console.log(`\n--- 插入 ${point} ---`);
    quadtree.insert(point);
});

// 3. 打印当前树结构
console.log('\n🌳 当前四叉树结构:');
quadtree.printTree();

// 4. 查询测试
console.log('\n🔍 查询测试:');
const queryRange = new Rectangle(40, 40, 60, 60); // 查询中心区域
console.log('查询范围:', queryRange.toString());
const foundPoints = quadtree.query(queryRange);
console.log('查询结果:', foundPoints.map(p => p.toString()).join(', '));

// 5. 删除测试
console.log('\n🗑️ 删除测试:');
console.log('删除点 C(30,30):');
quadtree.remove(new Point(30, 30));

console.log('\n🌳 删除后的树结构:');
quadtree.printTree();

// 6. 再次查询
console.log('\n🔍 再次查询相同范围:');
const foundPoints2 = quadtree.query(queryRange);
console.log('查询结果:', foundPoints2.map(p => p.toString()).join(', '));

// 7. 获取所有点验证
console.log('\n📋 当前所有点:');
const allPoints = quadtree.getAllPoints();
console.log('所有点:', allPoints.map(p => p.toString()).join(', '));

console.log('\n🎉 测试完成！');
// 手动插入点
quadtree.insert(new Point(15, 15));
// 手动查询
const myQuery = new Rectangle(30, 30, 40, 40);
quadtree.query(myQuery);
// 手动删除
quadtree.remove(new Point(20, 20));
// 查看当前结构
quadtree.printTree();
// 获取所有点
quadtree.getAllPoints();
```