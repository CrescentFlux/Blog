# Octree
##  基础知识
- **定义**
```
八叉树是一种用于描述三维空间的树状数据结构，其每个内部节点都恰好有八个子节点。它通过递归地、自适应地将三维空间细分为八个八分体，来高效地表示和管理三维空间中的数据
```
- **核心特性：**
```
层次结构：自顶向下的空间划分
递归细分：每个立方体可继续八等分
空间自适应：根据数据密度动态调整分辨率
稀疏表示：空区域几乎不占用存储空间
```
- **数学表达**
```
对于维度 D，每个节点的子节点数为：2^D
- 1D: 二叉树 (2^1 = 2)
- 2D: 四叉树 (2^2 = 4)  
- 3D: 八叉树 (2^3 = 8)
- nD: 2^n 叉树
```

- **性能特点对比**

|指标	|四叉树	|八叉树|
---|---|---
|内存占用|	相对较低|	相对较高|
|查询复杂度	|O(log₄N)	|O(log₈N)|
|构建时间|	较快|	较慢|
|适用数据	|二维分布数据	|三维空间数据|
|扩展性	|易于扩展到2.5D	|难以扩展到4D+|


## 注意事项
1. **混淆点**
- **节点类型混淆**

|特征|	叶子节点 (Leaf Node)|	内部节点 (Internal Node)|
---|---|---
|存储内容|	直接存储物体对象|	不存储物体，只做路由|
|objects| 数组	|有实际物体	|空数组 []|
|isDivided| 标志	|false|	true|
|children |数组|	全为 null	|有实际的子节点|
|角色	|数据存储层|	空间管理层|

- **对象比较混淆**

|比较方式	|引用比较|	值比较|
---|---|---
|代码	|objects.indexOf(obj)|	手动比较每个属性|
|问题|	必须同一对象引用|	性能较差|
|正确用法	|保存对象引用	|使用唯一ID比较|
|示例	const obj = {...}; tree.insert(obj); tree.remove(obj);|	tree.remove({id: obj.id, ...})|

- **合并条件参数混淆**

|参数	|totalObjects	|occupiedChildren|	mergeThreshold|
---|---|---|---
|含义	|所有子节点的物体总数|	有内容的子节点数量|	合并的物体数量阈值|
|计算方式|	sum(child.objects.length)	|统计 child.objects.length > 0 || child.isDivided|	Math.max(2, 6 - level)|
|作用|	判断物体集中程度	|判断空间利用情况	|控制合并严格度|
|示例值|	3（3个物体）	|1（1个子节点有内容）|	4（层级2的阈值）|

- **查询逻辑混淆**

|概念	|相交查询 (Intersection)|	包含查询 (Containment)|
---|---|---
|判断标准|	边界框有重叠|	物体完全在查询区域内|
|八叉树默认|	 是	| 不是|
|性能|	更快（粗略过滤）|	更慢（精确检查）|
|应用场景|	碰撞检测、视野计算	|精确区域选择|


- **二进制编码规则**

|二进制位	|权重	|方向判断|	条件|
---|---|---|---
|第0位|	1	|X轴方向	|point.x >= centerX|
|第1位|	2	|Y轴方向	|point.y >= centerY|
|第2位|	4	|Z轴方向	|point.z >= centerZ|
|组合规则	|位或运算|	多方向组合|	index = 0 | 1 | 2 | 4|


- **容量管理规则**

|参数|	默认值|	作用|	影响|
---|---|---|---
|maxObjects|	2-4	|单个节点最大物体数|	控制细分频率|
|maxLevel|	4-8	|最大细分深度|	控制树的最大深度|
|mergeThreshold	|动态计算|	合并的物体数量阈值	|控制合并的积极程度|

- **空间划分规则**

|方位编码	|二进制	|方向组合|	坐标范围|
---|---|---|---
|0|	000|	左 + 下 + 前|	[x, x+size/2), [y, y+size/2), [z, z+size/2)|
|1|	001|	右 + 下 + 前|	[x+size/2, x+size), [y, y+size/2), [z, z+size/2)|
|2|	010	|左 + 上 + 前|	[x, x+size/2), [y+size/2, y+size), [z, z+size/2)|
|3	|011|	右 + 上 + 前|	[x+size/2, x+size), [y+size/2, y+size), [z, z+size/2)|
|4|	100	|左 + 下 + 后|	[x, x+size/2), [y, y+size/2), [z+size/2, z+size)|
|5|	101|	右 + 下 + 后|	[x+size/2, x+size), [y, y+size/2), [z+size/2, z+size)|
|6|	110|	左 + 上 + 后|	[x, x+size/2), [y+size/2, y+size), [z+size/2, z+size)|
|7	|111|	右 + 上 + 后|	[x+size/2, x+size), [y+size/2, y+size), [z+size/2, z+size)|


2. **代码实现**
```
//--核心逻辑--//
class OctreeNode {
  constructor(bounds, level = 0) {
    this.bounds = bounds;    // {x, y, z, size} 立方体边界//当前立方体的边界信息
    this.level = level;      // 当前节点层级
    this.objects = [];       // 存储在此节点的物体
    this.children =  [null, null, null, null, null, null, null, null]; // 8个子节点; 
    this.isDivided = false;  // 是否已经细分
  }


  //计算点所在的子节点索引 (0-7)//给定一个三维空间中的点，告诉我它属于当前立方体的哪个空间
  getChildIndex(point) {
    const { x, y, z, size } = this.bounds;
    // 当前立方体信息//左下前角的坐标：(x, y, z) = (0, 0, 0)
    
    const halfSize = size / 2;//一半的大小//中心点是划分空间的基准线
    const centerX = x + halfSize;//中心的X坐标
    const centerY = y + halfSize;//中心的Y坐标
    const centerZ = z + halfSize;//中心的Z坐标
    //3位二进制数来表示8个方位二进制位表示的是方向标记，不是坐标值：0=负方向（左/下/前）1=正方向（右/上/后）010："X负，Y正，Z负" 这个方向组合
    let index = 0;//// 初始索引是0（左下前方位）
    if (point.x >= centerX) index |= 1;  // X轴判断//点在中心的右边 → 属于右侧的小立方体//方位编号
    if (point.y >= centerY) index |= 2;  // Y轴判断//点在中心的上边 → 属于上侧的小立方体//方位编号 
    if (point.z >= centerZ) index |= 4;  // Z轴判断//点在中心的后边 → 属于里侧的小立方体//方位编号
    return index;
  }
  // 细分当前节点
  subdivide() {
    //利用方位编号的二进制特性，通过简单的位运算就能计算出8个子立方体的精确位置，无需复杂的if-else判断
    if (this.isDivided) return;//如果已经分过了，就不再分；this.isDivided = true;// 标记为已分裂
    //每个节点只能分裂一次
    const { x, y, z, size } = this.bounds;
    const childSize = size/2;  //子节点尺寸子节点尺寸是父节点的一半
    for (let i = 0; i < 8; i++) {
      //1.计算每个子节点的偏移量//子立方体的大概位置
      const dx = (i & 1) ? childSize : 0;  // 检查最低位：是不是右边
      const dy = (i & 2) ? childSize : 0;  // 检查中间位：是不是上边 
      const dz = (i & 4) ? childSize : 0;  // 检查最高位：是不是后边
      //2.创建子节点//建立空间认知的层次，子立方体的精确位置
      //这实际上定义了一个轴向对齐的边界立方体AABB//
      const childBounds = {
        //从父立方体起点到子立方体起点的距离//为了到达子立方体的起点，需要从父立方体起点出发，在各个方向上移动的距离
        x: x + dx,//子立方体的起始X坐标//Delta变化或差异；在X方向上的变化量
        y: y + dy,// 子立方体的起始Y坐标
        z: z + dz,//子立方体的起始Z坐标
        size: childSize//子立方体的尺寸
      };
      //3.创建一个新的八叉树节点
      this.children[i] = new OctreeNode(childBounds, this.level + 1);//子节点的信息；层级加1；父节点是第0层，子节点就是第1层
    }
    //level（层级）是八叉树的深度控制系统：防止无限递归；控制分辨率；性能优化(通过限制最大层级，防止树变得过深，消耗太多内存)
    this.isDivided = true;
  }

  //--2.插入物体到八叉树--//
  //一旦节点细分，它就不再直接存储物体，只作为索引路由//
  //只有需要时才细分，避免不必要的内存开销;物体密集的区域自动获得更高分辨率;层次管理：每个节点只管理自己区域的物体，职责清晰//
  //根节点在细分后不再存储任何物体;在细分后变成纯粹的路由器//查询高效;内存节约;自适应
  insert(object, maxObjects = 4, maxLevel = 6) {
    // 2.1如果达到最大层级或者物体数量未超限，直接存储
    if (this.level >= maxLevel || //八叉树的双重限制策略:达到最大深度时，强制停止细分;直接存储，不管多拥挤
    //防止无限递归：没有深度限制，八叉树可能无限细分下去//控制内存：每深一层，节点数量×8，深度过大会内存爆炸//精度平衡：在合理深度下平衡精度和性能
        (!this.isDivided && this.objects.length < maxObjects)) {//<= maxObjects;当物体数量达到或小于上限时，直接存储
      this.objects.push(object);
      return true;
    }
    // 2.2如果还没细分，先细分
    if (!this.isDivided) {
      this.subdivide();// 1.调用细分方法:创建8个子节点,设置children数组,不同的空间区域
      // 2.重新插入现有的老物体
      //遍历数组的所有元素；对每个元素执行this.insert；
      for (const obj of this.objects) {
        this.insert(obj, maxObjects, maxLevel);//遍历的是 this.objects，即已经存在的物体 // 重新插入的是老物体obj
      }////现在this.isDivided=true，会路由到子节点
      this.objects = [];//清空根节点实际数据
    }
    //3.这里才处理新物体点
    const index =this.getChildIndex(object); //确定新插入的导致分裂的元素该去的具体位置
    if (this.children[index]) {//分配插入
        // 直接调用
      return this.children[index].insert(object, maxObjects, maxLevel);
    }//同一个insert方法同时处理了：新物体的插入；老物体的重新分配
    
  }

  //--3.查询区域内的所有物体--//
  //层次化搜索：1.粗粒度排除：快速跳过完全不相关的区域；2.中粒度收集：在相关区域内，粗略信任空间划分的合理性；3.可选的细粒度过滤：必要时再进行精确过滤
  //八叉树的默认查询返回的是所有相交的物体；//八叉树存储的是点数据，不是区域数据
  query(range, found = []) {
    //1.检查当前节点是否与查询区域相交//检查这个区域是否相关
    if (!this.intersects(range)) return found;
    //return found：这个区域与查询无关，没有新的发现，但之前找到的结果请继续传递下去//通过参数传递维持状态
    //结果累积：所有相关区域的发现都会汇总；数据安全：不会丢失已找到的结果；递归协作：每个节点只关心自己的贡献，不破坏整体结果
    //2.添加当前节点的物体
    found.push(...this.objects);//收集本区域的物体
    //添加的是节点内所有物体，不管它们是否真的在查询区域内
    //先收集本地，再递归下属
    //3.递归查询子节点
    if (this.isDivided) {
      for (const child of this.children) {//遍历当前节点的所有直接子节点，让它们各自执行相同的查询逻辑
        if (child) child.query(range, found);//继续在更细粒度上重复这个过程
      }//检查子节点是否存在：不是每个节点都有8个子节点；如果子节点一直没有物体插入；且该子节点没有进一步细分；这个子节点可能被垃圾回收或显式设置为null
    }
    return found;
  }

  //--4.检查两个立方体是否相交--//
  //空间碰撞检测:检查两个立方体是否没有分离;如果两个立方体在所有维度上都没有分离，那么它们就相交
  //所有维度都重叠：相交
  //intersects 检查的是节点的边界与查询区域是否相交，不是检查节点内的物体是否在查询区域内
  intersects(other) {
    const a = this.bounds;
    const b = other;
    //快速排除：只要发现一个维度分离，立即返回false//部分维度相同，但关键维度分离还是分离
    //边界包含：如果边界刚好接触，也算相交（因为用的是 < 而不是 <=）
    //高效计算：只有6个比较操作，非常快速
    //快速排除不相关的区域；用最简单的判断排除最多的不可能
    return !(a.x + a.size < b.x || b.x + b.size < a.x ||//如果都不是这两种情况，说明它们相交
             a.y + a.size < b.y || b.y + b.size < a.y ||//分离条件
             a.z + a.size < b.z || b.z + b.size < a.z);//分离条件
  }
//--5.删除逻辑--//
  remove(object) {
    // 1. 在叶子节点查找并删除
    const objectIndex = this.objects.indexOf(object);//// 在当前节点的objects数组中查找要删除的对象的索引位置
    if (objectIndex !== -1) {////如果找到了indexOf返回-1表示找到
      this.objects.splice(objectIndex, 1);////从数组中删除这个对象
      
      //2.删除后检查是否需要合并
      if (this.shouldMerge()) {
        this.merge();
      }
      return true;
    }
    // 2. 内部节点：在子节点中递归删除
    //1.删除
    if (this.isDivided) {
      const index = this.getChildIndex(object);//计算物体应该位于哪个子节点
      if (this.children[index]) {////递归调用子节点的remove方法
        const removed = this.children[index].remove(object);
        ////八叉树是层次结构，物体可能存储在任意深度的叶子节点中
        // 2.如果子节点删除成功，检查是否需要合并
        if (removed && this.shouldMerge()) {
          this.merge();
        }
        return removed;
      }
    }
    //3.都没找到
    return false;
  }
  //--合并逻辑--// 
  //1.判断是否需要合并
  shouldMerge() {
    // 1.只有已细分的节点才需要考虑合并
    if (!this.isDivided) return false;
    let totalObjects = 0;//totalObjects - 物体总数：所有子节点中物体的总和//判断物体的集中程度
    let occupiedChildren = 0;//有效子节点数统计： 有"实际内容"的子节点数量//判断空间的利用情况
    
    // 2.统计所有子节点的物体数量和有效子节点数量
    for (const child of this.children) {
      if (child) {//只处理存在的子节点（非null）
        totalObjects += child.objects.length;
        // 如果子节点有物体或者子节点本身已细分，就算作有效子节点
        if (child.objects.length > 0 || child.isDivided) {
          occupiedChildren++;
        }
      }
    }
    //mergeThreshold 合并阈值：最多允许多少个物体挤在一个节点中；occupiedChildren 统计的是"有业务"的子节点
    //totalObjects元素的总数量；occupiedChildren放了元素的节点的总个数
    // 合并条件：物体总数很少 或者 有效子节点很少
    return totalObjects <= this.mergeThreshold || occupiedChildren <= 1;
    //内存效率的优化：用单个节点代替整个子树，在物体很少时大幅节省内存和查询开销
    //从最深的节点开始，逐层向上合并，直到遇到不符合条件的节点为止
  }
  //2.执行合并操作
  merge() {
    if (!this.isDivided) return;//如果自己都没细分，那就无法合并
    console.log(`合并节点: 层级 ${this.level}`);
    // 1. 收集所有子节点的物体
    const allObjects = [];
    for (const child of this.children) {
      if (child) {
        allObjects.push(...child.objects);
        
        //2.清理子节点的引用，帮助垃圾回收
        child.objects = [];
        child.children = [];
      }
    }
    // 3. 更新当前节点状态
    this.objects = allObjects;//自己直接存储
    this.children = [null, null, null, null, null, null, null, null];//解散所有曾孙节点
    this.isDivided = false;//// 变成叶子节点
    console.log(`合并完成: 将 ${allObjects.length} 个物体提升到层级 ${this.level}`);
  }
  //动态阈值逻辑
  //八叉树能在内存效率和查询精度之间自动找到平衡点
  get mergeThreshold() {
    // 根据层级动态调整阈值，高层级更倾向于合并：浅层宽松，深层严格
    return Math.max(2, 6 - this.level);
    //Math.max(2, ...)：确保阈值至少为2；6 - this.level：基础阈值随着层级加深而减小//管理极小空间，必须非常精细
    //越深的节点越严格，越浅的节点越宽松；深层节点：严格合并，避免树太深；浅层节点：宽松合并，保持较好的空间划分
  }
}

//--5.门面类--//
//八叉树的门面类（Facade），它提供了简洁的对外接口，隐藏了内部复杂的树结构
class Octree {
  constructor(bounds) {
    this.root = new OctreeNode(bounds);;  //创建根节点
  }
  //八叉树必须有一个起点//根节点代表整个三维空间的范围//所有操作都从根节点开始
  insert(object) {
    return this.root.insert(object);// 让根节点处理插入
  }
  query(range) {
    return this.root.query(range);//让根节点处理查询
  }
  remove(){
    return this.root.remove(object)//让根节点处理删除
  }
}
```
```
//----测试----//
class OctreeNode {
  constructor(bounds, level = 0) {
    this.bounds = bounds;
    this.level = level;
    this.objects = [];
    this.children = new Array(8).fill(null);
    this.isDivided = false;
  }

  // 计算子节点索引
  getChildIndex(point) {
    const { x, y, z, size } = this.bounds;
    const halfSize = size / 2;
    const centerX = x + halfSize;
    const centerY = y + halfSize;
    const centerZ = z + halfSize;
    
    let index = 0;
    if (point.x >= centerX) index |= 1;
    if (point.y >= centerY) index |= 2;
    if (point.z >= centerZ) index |= 4;
    return index;
  }

  // 检查边界相交
  intersects(other) {
    const a = this.bounds;
    const b = other;
    return !(a.x + a.size < b.x || b.x + b.size < a.x ||
             a.y + a.size < b.y || b.y + b.size < a.y || 
             a.z + a.size < b.z || b.z + b.size < a.z);
  }

  // 细分节点
  subdivide() {
    if (this.isDivided) return;
    
    const { x, y, z, size } = this.bounds;
    const childSize = size / 2;
    
    for (let i = 0; i < 8; i++) {
      const dx = (i & 1) ? childSize : 0;
      const dy = (i & 2) ? childSize : 0;
      const dz = (i & 4) ? childSize : 0;
      
      const childBounds = {
        x: x + dx,
        y: y + dy,
        z: z + dz,
        size: childSize
      };
      
      this.children[i] = new OctreeNode(childBounds, this.level + 1);
    }
    
    this.isDivided = true;
  }

  // 插入物体
  insert(object, maxObjects = 2, maxLevel = 4) {
    if (this.level >= maxLevel || (!this.isDivided && this.objects.length < maxObjects)) {
      this.objects.push(object);
      return true;
    }
    
    if (!this.isDivided) {
      this.subdivide();
      for (const obj of this.objects) {
        this.insert(obj, maxObjects, maxLevel);
      }
      this.objects = [];
    }
    
    const index = this.getChildIndex(object);
    return this.children[index].insert(object, maxObjects, maxLevel);
  }

  // 查询区域
  query(range, found = []) {
    if (!this.intersects(range)) return found;
    
    found.push(...this.objects);
    
    if (this.isDivided) {
      for (const child of this.children) {
        if (child) child.query(range, found);
      }
    }
    
    return found;
  }

  // 删除物体
  remove(object) {
    const objectIndex = this.objects.indexOf(object);
    if (objectIndex !== -1) {
      this.objects.splice(objectIndex, 1);
      console.log(`🗑️ 在层级${this.level}删除物体: ${object.name}`);
      
      if (this.shouldMerge()) {
        this.merge();
      }
      return true;
    }
    
    if (this.isDivided) {
      const index = this.getChildIndex(object);
      if (this.children[index]) {
        const removed = this.children[index].remove(object);
        if (removed && this.shouldMerge()) {
          this.merge();
        }
        return removed;
      }
    }
    
    return false;
  }

  // 检查是否需要合并
  shouldMerge() {
    if (!this.isDivided) return false;
    
    let totalObjects = 0;
    let occupiedChildren = 0;
    
    for (const child of this.children) {
      if (child) {
        totalObjects += child.objects.length;
        if (child.objects.length > 0 || child.isDivided) {
          occupiedChildren++;
        }
      }
    }
    
    const shouldMerge = totalObjects <= this.mergeThreshold || occupiedChildren <= 1;
    if (shouldMerge) {
      console.log(`🔍 层级${this.level}需要合并: 物体数=${totalObjects}, 有效子节点=${occupiedChildren}, 阈值=${this.mergeThreshold}`);
    }
    return shouldMerge;
  }

  // 执行合并
  merge() {
    if (!this.isDivided) return;
    
    console.log(`🔄 开始合并层级${this.level}节点`);
    
    const allObjects = [];
    for (const child of this.children) {
      if (child) {
        allObjects.push(...child.objects);
        child.objects = [];
        child.children = [];
      }
    }
    
    this.objects = allObjects;
    this.children = new Array(8).fill(null);
    this.isDivided = false;
    
    console.log(`✅ 合并完成: 将${allObjects.length}个物体提升到层级${this.level}`);
  }

  // 动态合并阈值
  get mergeThreshold() {
    return Math.max(2, 6 - this.level);
  }

  // 更新物体位置（改）
  update(oldObject, newObject) {
    if (this.remove(oldObject)) {
      return this.insert(newObject);
    }
    return false;
  }

  // 打印树状态
  printState(prefix = "") {
    const objectNames = this.objects.map(obj => obj.name).join(', ') || '空';
    console.log(prefix + `层级${this.level}: [${objectNames}] ${this.isDivided ? '(已细分)' : '(叶子)'}`);
    if (this.isDivided) {
      for (let i = 0; i < 8; i++) {
        if (this.children[i]) {
          this.children[i].printState(prefix + "  ");
        }
      }
    }
  }

  // 统计信息
  getStats() {
    let nodeCount = 1;
    let objectCount = this.objects.length;
    let maxDepth = this.level;
    
    if (this.isDivided) {
      for (const child of this.children) {
        if (child) {
          const childStats = child.getStats();
          nodeCount += childStats.nodeCount;
          objectCount += childStats.objectCount;
          maxDepth = Math.max(maxDepth, childStats.maxDepth);
        }
      }
    }
    
    return { nodeCount, objectCount, maxDepth };
  }
}

class Octree {
  constructor(bounds) {
    this.root = new OctreeNode(bounds);
    this.maxObjects = 2;
    this.maxLevel = 4;
  }
  
  insert(object) { 
    console.log(`📥 插入物体: ${object.name}`);
    return this.root.insert(object, this.maxObjects, this.maxLevel); 
  }
  
  remove(object) { 
    return this.root.remove(object); 
  }
  
  update(oldObject, newObject) {
    console.log(`✏️ 更新物体: ${oldObject.name} -> ${newObject.name}`);
    return this.root.update(oldObject, newObject);
  }
  
  query(range) { 
    const results = this.root.query(range);
    console.log(`🔍 查询区域 ${JSON.stringify(range)} 找到 ${results.length} 个物体: ${results.map(obj => obj.name).join(', ')}`);
    return results;
  }
  
  printState() { 
    console.log("\n🌳 八叉树当前状态:");
    this.root.printState();
    const stats = this.root.getStats();
    console.log(`📊 统计: ${stats.nodeCount}个节点, ${stats.objectCount}个物体, 最大深度${stats.maxDepth}`);
  }
}

// 测试函数
function testOctree() {
  console.log("=== 🚀 开始八叉树完整测试 ===\n");
  
  const tree = new Octree({ x:0, y:0, z:0, size:100 });

  // 测试数据
  const objects = [
    { x:10, y:10, z:10, name: 'A' },
    { x:15, y:15, z:15, name: 'B' },
    { x:12, y:12, z:12, name: 'C' },
    { x:85, y:85, z:85, name: 'N1' },
    { x:88, y:88, z:88, name: 'N2' },
    { x:82, y:82, z:82, name: 'N3' },
    { x:70, y:20, z:20, name: 'D1' },
    { x:20, y:70, z:20, name: 'D2' }
  ];

  // 阶段1: 插入测试
  console.log("1. 📥 插入测试");
  console.log("=".repeat(40));
  objects.forEach(obj => tree.insert(obj));
  tree.printState();

  // 阶段2: 查询测试
  console.log("\n2. 🔍 查询测试");
  console.log("=".repeat(40));
  tree.query({ x:0, y:0, z:0, size:30 });  // 查询左下前区域
  tree.query({ x:80, y:80, z:80, size:20 }); // 查询右上后区域
  tree.query({ x:0, y:0, z:0, size:100 }); // 查询整个空间

  // 阶段3: 删除测试（触发合并）
  console.log("\n3. 🗑️ 删除测试 - 触发合并");
  console.log("=".repeat(40));
  tree.remove(objects[1]); // 删除B
  tree.printState();

  tree.remove(objects[2]); // 删除C  
  tree.printState();

  tree.remove(objects[0]); // 删除A
  tree.printState();

  // 阶段4: 更新测试
  console.log("\n4. ✏️ 更新测试");
  console.log("=".repeat(40));
  const oldN1 = objects[3];
  const newN1 = { x:75, y:75, z:75, name: 'N1' };
  tree.update(oldN1, newN1);
  tree.printState();

  // 阶段5: 继续删除测试
  console.log("\n5. 🗑️ 继续删除测试");
  console.log("=".repeat(40));
  tree.remove(objects[4]); // 删除N2
  tree.printState();

  tree.remove({ x:88, y:88, z:88, name: 'N2' }); // 删除不存在的物体
  tree.printState();

  // 阶段6: 最终查询
  console.log("\n6. 🔍 最终查询测试");
  console.log("=".repeat(40));
  tree.query({ x:0, y:0, z:0, size:100 }); // 查询所有剩余物体

  console.log("\n=== ✅ 测试完成 ===");
}

// 运行测试
testOctree();

// 额外的边界测试
function additionalTests() {
  console.log("\n\n=== 🧪 额外边界测试 ===");
  
  const tree = new Octree({ x:0, y:0, z:0, size:100 });
  
  // 测试空树查询
  console.log("\n空树查询测试:");
  tree.query({ x:0, y:0, z:0, size:50 });
  
  // 测试删除不存在的物体
  console.log("\n删除不存在物体测试:");
  tree.remove({ x:999, y:999, z:999, name: '不存在的物体' });
  
  // 测试单个物体
  console.log("\n单个物体测试:");
  const singleObj = { x:50, y:50, z:50, name: '单独物体' };
  tree.insert(singleObj);
  tree.printState();
  tree.remove(singleObj);
  tree.printState();
}

// 取消注释运行额外测试
// additionalTests();
```