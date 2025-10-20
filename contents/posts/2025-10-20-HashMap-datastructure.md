# Hash Table
## 基础知识
- **定义**
```
哈希表是一种通过键（Key）直接访问值（Value）的数据结构，核心思想：键 → 哈希函数 → 数组索引 → 直接访问
三大核心部件：
1. 哈希函数 (Hash Function)
2. 数组 (Array/Table) 
3. 冲突解决机制 (Collision Resolution)
```
- **冲突解决机制**



    - 链地址法（Separate Chaining）
        - 每个哈希桶维护一个链表结构，所有映射到同一索引的键值对存储在该链表中。
    - 开放地址法（Open Addressing）
        - 当发生冲突时，按照预定探测序列在数组中寻找下一个可用位置，常见变体包括：
            - 线性探测：h(k, i) = (h(k) + i) mod m
            - 二次探测：h(k, i) = (h(k) + c₁i + c₂i²) mod m
            - 双重哈希：h(k, i) = (h₁(k) + i·h₂(k)) mod m
                - 技术特性说明
                - 优势：
                    - 提供基于键的快速数据访问
                    - 支持动态数据集的高效操作
                    - 实现简单，易于理解和应用
                - 局限性：
                    - 内存使用效率相对较低（存在未使用桶）
                    最坏情况下性能退化为线性
                    对哈希函数质量依赖性强
                    迭代操作不保证元素顺序
                应用领域
                    数据库索引构建
                    编译器符号表管理
                    缓存系统实现
                    集合成员快速判断
                    字符串匹配算法优化








## 注意事项
1. **混淆点**

|混淆点	|概念 A	|概念 B	|解析与注意事项|
---|---|---|---
|数据结构类型	|哈希表 (Hash Table)	|哈希集合 (Hash Set)	|哈希表存储键值对 (Key-Value)，如 Map；哈希集合只存储不重复的值，如 Set|
|哈希冲突解决|	链地址法|	开放地址法|	链地址法：冲突时形成链表（Java HashMap）；开放地址法：寻找下一个空桶（Python dict）。链地址法更常见|
|时间复杂度|	平均 O(1)|	最坏 O(n)|	在良好哈希函数和负载因子下是 O(1)；但所有key哈希冲突时退化为链表查询 O(n)|
|键的特性|	不可变性|	可变性|	用作键的对象应为不可变的，如果可变对象作为键且被修改，将无法再次找到该键|
|遍历顺序|	无序性|	有序性|	标准哈希表是无序的；LinkedHashMap 保持插入顺序；TreeMap 保持键的自然顺序|
|空键/空值|	允许 null|	不允许 null	|HashMap 允许一个null键和多个null值；Hashtable 不允许任何null键值；ConcurrentHashMap 不允许null|
|线程安全|	非线程安全	|线程安全|	HashMap 非线程安全；Hashtable 线程安全但性能差；ConcurrentHashMap 线程安全且高性能|
|扩容机制|	负载因子	|初始容量	|负载因子决定何时扩容（默认0.75）；初始容量避免频繁扩容，应根据数据量预估设置|
|相等判断|	hashCode()|	equals()|	先比较 hashCode()，如果相同再比较 equals()。必须同时重写这两个方法且保持一致|
|内存占用	|空间换时间	|时间换空间	|哈希表以更多内存空间换取快速访问，如果内存紧张可能不适合|



2. **完整代码实现**
```
class SimpleHashTable {
  constructor(size = 10) {
    this.size = size;
    // 初始化 buckets（桶）。我们使用一个数组，每个元素是另一个空数组，用于实现“链地址法”来解决碰撞。
    // 创建一个长度为 `size` 的数组，并用空数组填充每一个元素。
    this.buckets = new Array(size).fill(null).map(() => []);
/*new Array(size):创建一个指定长度的空位数组。这个数组有长度（length =size)空槽位数组
.fill(null):用一个具体的值这里是null填充数组中的每一个空槽位,
.map(() => []),映射。 对数组中的每一个元素执行一个函数，并用函数的返回值创建一个新数组,通过map操作:备了一个全新的、独立的空数组；这个空数组就是链地址法中的链表（在这里我们用数组来模拟链表的功能）。
不能直接 new Array(size).map(() => [])：
错误示范：JS中的.map()方法会跳过空槽位，new Array(3)创建的是空槽位数组，.map()根本不会对它们进行任何操作，最终得到的还是一个空槽位数组
this.buckets = new Array(3).map(() => []);
console.log(this.buckets); // 输出: [ <3 empty items> ]
this.buckets：一个数组，里面的每个元素都是另一个空数组，等待着被填入因哈希碰撞而来到此地的键值对。
*/
  }

  // 核心：哈希函数。它将一个键（key）映射到一个数组索引。
  _hash(key) {
    let keyStr = key.toString();//统一输入格式，计算字符代码只对字符串有效
    let total = 0;//初始化累加器，total变量将最终承载这个数字指纹的雏形，我们准备开始计算这个字符串的数字指纹，同时需要一个干净的地方来累加结果
    for (let i = 0; i < keyStr.length; i++) {
        //信息摘要算法：循环从第一个字符(i=0)走到最后一个字符(i=keyStr.length-1）
      total += keyStr.charCodeAt(i);//keyStr.charCodeAt(i)：获取字符身份证号的操作。在计算机底层，所有字符（字母、数字、符号）都有一个唯一的数字编号，叫做 Unicode 编码。total += ...： 累加。我们把字符串中每个字符的身份证号都加起来// 对键 "ab" 进行哈希计算：i=0: 字符 'a' → 编码 97。 total = 0 + 97 = 97，i=1: 字符 'b' → 编码 98。total = 97 + 98 = 195最终结果： "ab" 的数字指纹是195。（一个初步的、代表该键的“特征值”）
    }
/*
完成了从任意键到数字的转换，这是哈希映射的第一步
将一个任意的键，通过一个确定的规则（累加字符编码），转化成一个可用于后续取模运算的数值。 这是将“键”翻译成“地址”过程中，最核心的一步计算；
*/
    //使用取模运算，确保返回的索引在 0 到 (this.size - 1) 的范围内。从功能上，它为任何一个键确定了其在底层数组中的最终存放位置（索引）
    return total % this.size;//用total除以this.size，然后返回除不尽的那个余数//完成了从“键”到“地址”的跳跃
/*%是取模运算符，就是计算两个数相除后的余数，total 是我们上一步计算出来的那个（可能很大的）数字指纹，this.size是我们哈希表底层数组的长度，也就是“桶”的总数
限定范围，完成最终映射：% this.size 的作用，就是进行一次“缩放”和“定位”，输入：一个可能无限大的数字空间（所有total的可能值），输出：一个严格限定在 [0, this.size - 1] 范围内的整数
    
    */
}

  //插入键值对
  put(key, value) {
    const index = this._hash(key);//计算坐标：调用hash函数，把这个函数返回的最终数字接住，存到变量index里得到了一个确定的数字，也就是要存的那个数据在底层大数组中的确切位置
    const bucket = this.buckets[index]; //找到对应的桶//这个bucket不是单个位置，而是一个容器（在我们实现里是一个数组）。可能会有哈希碰撞，多个物品（键值对）都被映射到同一个货架上，这个货架本身必须能容纳多个物品。
//完成这两步后，所有后续操作都只在这个bucket上进行，哈希表O(1)时间复杂度：。它通过一次直接计算（_hash）和一次直接访问（buckets[index]），跳过了所有“比较”和“寻找”的过程，瞬间将你带到了数据最可能存在的那个局部区域（桶）//🎯将全局的搜索问题，转化为局部的管理问题
    // 检查桶中是否已存在相同的 key
    for (let i = 0; i < bucket.length; i++) {
      // bucket 中的每个元素都是一个 [key, value] 对。
      // 请写出条件，判断当前遍历到的元素的 key 是否等于我们要插入的 key。
      if (bucket[i][0] === key) {
        // 如果 key 已存在，则更新其 value
        bucket[i][1] = value;
        return;
      }
    }
    // 如果 key 不存在，则将新的键值对放入桶中。
    // 将新的键值对（一个数组）加入到 bucket 中。
    return bucket.push([key, value]);
  }

  //根据键获取值：
  get(key) {
    const index = this._hash(key);
    const bucket = this.buckets[index];
    for (let i = 0; i < bucket.length; i++) {
      //同样，判断当前元素的 key 是否等于我们要查找的 key。
      if (bucket[i][0] === key) {
        // 如果找到，返回对应的 value。
        //返回当前元素的 value（它在数组的第二个位置）。
        return bucket[i][1];
      }
    }
    // 如果遍历完整个桶都没找到，返回 undefined。
    return undefined;
  }

  // 根据键删除键值对
  remove(key) {
    const index = this._hash(key);
    const bucket = this.buckets[index];
    for (let i = 0; i < bucket.length; i++) {
      //找到要删除的 key 所在的元素。
      if (bucket[i][0] === key) {
        //从数组 bucket 中删除索引为 i 的这一个元素。
        bucket.splice(i, 1);
        return true; // 删除成功
      }
    }
    return false; // 未找到，删除失败
  }
}
//🎯用函数计算位置，用链表解决冲突
// 测试哈希表
const myHashTable = new SimpleHashTable(5);
myHashTable.put("name", "Alice");
myHashTable.put("age", 2);
console.log(myHashTable.get("name")); // 应该输出 "Alice"
console.log(myHashTable.get("age"));  // 应该输出 2
myHashTable.remove("age");
console.log(myHashTable.get("age"));  // 应该输出 undefined
//===============工业级哈希表核心实现=============//
/*
🐢简单相加 → 极易碰撞！"ab" 和 "ba" 哈希值相同，攻击者可以轻松制造海量碰撞
🎯哈希函数安全策略：从「简单算法」到「安全工程」
💡核心优化：
随机种子：每次程序启动哈希结果都不同，攻击者无法预判
位扩散：充分利用32位所有位，避免简单相加的信息丢失
非线性变换：乘法、异或、位旋转打乱输入模式
🐢没有扩容！链表会无限变长，最终退化为O(n)
🎯扩容策略：从「固定大小」到「智能扩容」
💡核心优化：
负载因子监控：当 元素数/容量 > 0.75 时触发扩容
几何增长：每次容量翻倍，分摊扩容成本
动态调整：根据实际使用情况自动优化
🐢永远使用链表，最坏情况退化为O(n)
🎯碰撞处理：从「简单链表」到「树化转换」
💡核心优化：
性能保障：链表长度>8时转为红黑树，保证最坏情况O(log n)
内存优化：元素减少时退化回链表，节省内存
自适应：根据实际数据分布动态选择最优结构
🐢简单的数组+链表，内存不连续，缓存不友好
🎯内存布局：从「数组存储」到「缓存友好」
💡核心优化：
数据局部性：相关数据在内存中连续存储
缓存预取：CPU一次缓存行能加载更多相关数据
哈希缓存：存储哈希值避免重复计算
🐢完全没有并发控制
🎯并发安全：从「单线程」到「高并发」
💡核心优化：
锁分段：不同分段可以并发操作，提升吞吐量
细粒度锁：只锁冲突的分段，而不是整个表
无锁读：读操作通常不需要加锁
📚总体核心优化：
安全层面：防DoS攻击的随机化哈希函数
性能层面：动态扩容 + 树化转换保证O(1)平均和O(log n)最坏
内存层面：缓存友好的数据布局 + 智能退化
并发层面：分段锁实现高并发访问
解决能不能在大规模、高并发、恶意环境下稳定高效地用
*/
class IndustrialHashTable {
  constructor(initialCapacity = 16, loadFactor = 0.75) {
    this.capacity = initialCapacity;//底层数组的长度，也就是"桶"的总数，决定了哈希表能有多"宽"，容量越大碰撞越少，随着数据增多会自动扩容（16 → 32 → 64...）
    this.loadFactor = loadFactor;//拥挤度警报线：一个介于0到1之间的比例系数，0.75：经过大量测试得出的时间与空间的最佳平衡点
    this.size = 0;//哈希表中当前存储的键值对总数，put() 新键时size++，remove() 时size--，用于判断是否需要扩容
    this.threshold = Math.floor(this.capacity * this.loadFactor);//扩容阈值，具体的扩容触发点，实际触发扩容的元素数量阈值//计算：容量 × 负载因子
    this.seed = Math.floor(Math.random() * 0xFFFFFFFF); // 随机种子防止攻击//随机安全锁：一个每次启动都不同的随机数
    /*
    自我优化的反馈循环：PUT新数据 → size++ → 检查 size >= threshold? 
                          ↓
                     是 → 执行_resize() → capacity×2 → 重新计算threshold
                          ↓  
                     否 → 继续正常插入
    capacity 和 threshold 是"硬件基础设施"loadFactor 是"管理策略"size 是"实时监控数据"seed 是"安全防护"
    共同确保哈希表在面对海量数据、恶意攻击时，依然能保持高效稳定的性能。
    这已经远远超出了存储数据的范畴，而是构建了一个自适应的、抗攻击的、高性能的数据生态系统
    */
    // 使用Map作为桶，支持树化转换//使用Map/专门的内存布局
    this.buckets = new Array(this.capacity);
    for (let i = 0; i < this.capacity; i++) {
      this.buckets[i] = new Map(); // 初始使用Map而不是数组//🎯智能映射表//查找key时：map.get(key) → 内部优化过的查找
      /*
      Map的优势：快速查找：基于哈希的查找，比数组遍历快
      内置方法：直接有 set(), get(), has(), delete() 等方法
      键类型灵活：键可以是任何类型（对象、函数等），而不仅是字符串
      */
    }
    //树化阈值：防止性能退化的安全网：恶意攻击或极端情况，大量键哈希到同一个桶
    this.TREEIFY_THRESHOLD = 8; // 链表树化阈值// 链表→树阈值
    this.UNTREEIFY_THRESHOLD = 6; // 树退化阈值// 树→链表阈值
/*在良好的哈希函数下，桶长度达到8的概率极小（约0.00000006）
如果真的达到8，说明可能是攻击或极端情况，需要树化保护
6作为退化阈值，提供2个元素的缓冲，避免频繁转换*/
  }

  // 安全哈希函数 - 防止哈希碰撞攻击
  _secureHash(key) {
    const keyStr = JSON.stringify(key);//统一输入格式：把所有类型的键都变成字符串，确保处理一致性
    let hash = this.seed; //🔑关键：随机种子！随机种子：每次程序启动哈希结果都不同，攻击者无法预判
    //核心混战 - 三位一体的信息搅拌：
    for (let i = 0; i < keyStr.length; i++) {
      const char = keyStr.charCodeAt(i);// 获取字符编码
      //1.混合运算：乘法 + 异或 + 位旋转//位扩散：充分利用32位所有位，避免简单相加的信息丢失//非线性变换：乘法、异或、位旋转打乱输入模式
      hash = Math.imul(hash ^ char, 0x9E3779B9);// 黄金比例乘数// 第一重：异或+乘法
      hash = (hash << 5) | (hash >>> 27); // 32位旋转// 位旋转，充分利用所有位// 第二重：位旋转
    /*
    异或操作 hash ^ char：混合但不丢失信息     |     乘法操作 Math.imul(..., 0x9E3779B9)
    hash        :10110101当前状态           |    //0x9E3779B9 = 2654435769 - 黄金比例相关的魔法数字，混合结果 * 2654435769
    XOR char    :11001011新输入字符              //黄金比例乘数，能产生良好的分布，乘法会产生溢出，这种溢出是不可预测的非线性变换
    结果         :01111110完美混合！
      
    hash = (hash << 5) | (hash >>> 27) - 位旋转
    打破局部性：把高位信息移到低位，低位信息移到高位
    充分利用所有位：确保32位中的每一位都参与影响最终结果
    防止模式形成：打乱任何可能被攻击者利用的规律    
    */
    }
    //Avalanche Effect"（雪崩效应）:让输入的微小变化引起输出的巨大改变
    //2.最终混淆，破坏输入模式
    hash ^= keyStr.length;//加入字符串长度的信息:确保不同长度的字符串产生显著不同的哈希值:"a"（长度1）和 "aa"（长度2）会有不同的位模式,防止攻击者用固定长度字符串进行模式攻击
    /* 
    步骤1：提取高位精华 (hash >>> 16)
    步骤2：高位与自身混合 (hash ^ (hash >>> 16))
    步骤3：魔法药剂催化 (× 0x85EBCA6B)让哈希值的高位和低位互相影响，打破内部模式
    */
    hash = Math.imul(hash ^ (hash >>> 16), 0x85EBCA6B);//右移16位
    /* 换一个偏移量（13位），继续混合
    13和16？：使用质数偏移量确保混合更彻底
    */
    hash = Math.imul(hash ^ (hash >>> 13), 0xC2B2AE35);//内外交融
    /* 
    最终hash = hash ^ (hash >>> 16)确保高位的变化能彻底传播到低位
    */
    hash ^= hash >>> 16;
    // 确保非负：去掉符号位// 结果是 0 到 2147483647 之间的正整数//映射到数组范围,% this.capacity: 确保索引在0到capacity-1之间
    return (hash & 0x7FFFFFFF) % this.capacity; // 确保非负
  }

  // 动态扩容
  _resize() {
    const oldBuckets = this.buckets;
    this.capacity *= 2; // 双倍扩容
    this.threshold = Math.floor(this.capacity * this.loadFactor);
    
    this.buckets = new Array(this.capacity);
    for (let i = 0; i < this.capacity; i++) {
      this.buckets[i] = new Map();
    }
    // 重新哈希所有元素// 重新哈希所有元素 - 昂贵但必要！
    for (const bucket of oldBuckets) {
      for (const [key, value] of bucket) {
        const newIndex = this._secureHash(key);//在新容量下重新哈希✅ 正确做法：重新计算地址，可能分配到完全不同区域
        this.buckets[newIndex].set(key, value);
      }
    }
    console.log(`哈希表扩容: ${oldBuckets.length} -> ${this.capacity}`);
  }

                put(key, value) {
                    // 检查是否需要扩容// 检查树化条件
                    if (this.size >= this.threshold) {
                    this._resize();
                    }
                    const index = this._secureHash(key);
                    const bucket = this.buckets[index];
                    if (!bucket.has(key)) {
                    this.size++;
                    }
                    bucket.set(key, value);
                    // 检查是否需要树化（这里简化，实际应该转换为红黑树）
                    if (bucket.size >= this.TREEIFY_THRESHOLD) {
                    this._treeifyBucket(index); // 链表 → 红黑树
                    }
                    return this;
                }
                get(key) {
                    const index = this._secureHash(key);
                    const bucket = this.buckets[index];
                    return bucket.get(key);
                }
                
                remove(key) {
                /*删除元素后：红黑树 → 链表
                树结构内存开销大：每个树节点需要维护父、左、右指针
                小数据量时链表更快：树的操作常数因子更大
                节省资源：元素少了就退化成更轻量的结构
                */
                    const index = this._secureHash(key);
                    const bucket = this.buckets[index];
                    if (bucket.has(key)) {
                    bucket.delete(key);
                    this.size--;
                    // 检查是否需要退化
                    if (bucket.size <= this.UNTREEIFY_THRESHOLD && this._isTreeified(bucket)) {
                        this._untreeifyBucket(index);// 红黑树 → 链表
                    }
                    return true;
                    }
                    return false;
                }

// 简化的树化模拟
_treeifyBucket(index) {//链表转树，将链表演进为红黑树，防止性能退化
    console.log(`桶 ${index} 达到树化阈值，转换为树结构`);
     // 实际实现会在这里将链表转换为红黑树
 }
            /*    _untreeifyBucket(index) {
                    console.log(`桶 ${index} 退化回链表结构`);
                }
                // 在 IndustrialHashTable 类中修复 _isTreeified 方法*/
_isTreeified(bucket) {//检查桶是否已树化：实际工业实现中：会检查桶的实际数据类型，而不仅仅是大小
  // 确保参数名不冲突，使用明确的命名
  if (!bucket || typeof bucket !== 'object') return false;
  
  // 简化实现：如果桶大小曾经达到过树化阈值，就认为是树
  // 在实际实现中，这里会检查桶的实际数据结构类型
  return bucket.size >= this.TREEIFY_THRESHOLD;
}

// 同时修复 _untreeifyBucket 方法
_untreeifyBucket(bucketIndex) {//树转链表将红黑树退化为链表，节省内存，实际效果：小数据量时恢复更节省内存的链表结构
  console.log(`桶 ${bucketIndex} 退化回链表结构`);
  // 在实际实现中，这里会将红黑树转换回链表
}
                /* _isTreeified(bucket) {
                    // 简化实现，实际会检查桶是否为树结构
                    return bucket.size > this.TREEIFY_THRESHOLD;
                }*/

//哈希表健康诊断工具:安全相关方法:让我们能够直观地看到哈希函数的性能和分布质量
  getCollisionDistribution() {//
    const distribution = {};//distribution - 桶分布直方图 //桶大小分布统计
    let maxCollisions = 0;//maxCollisions - 性能瓶颈指标//单个桶的最大元素数
    let totalCollisions = 0; //totalCollisions - 哈希质量指标 //总碰撞元素数量
                                /*
                                maxCollisions → 最坏情况性能保证：直接影响用户体验的上限，触发树化转换的决策依据
                                totalCollisions → 平均性能指标:反映哈希函数的整体质量,影响系统的吞吐量
                                distribution → 分布均匀性分析:检测哈希函数的偏斜程度,识别潜在的攻击模式
                                loadFactor → 空间效率评估:平衡时间与空间的权衡,扩容时机的参考依据
                                诊断函数让开发者能够从"黑盒使用"变为"透明监控"，是生产环境中不可或缺的运维工具
                                */
    //遍历所有桶，统计分布
    for (let i = 0; i < this.capacity; i++) {
      const bucketSize = this.buckets[i].size;//当前桶的元素数量
      distribution[i] = bucketSize;// 记录桶索引 -> 元素数量
      //更新最大桶大小
      if (bucketSize > maxCollisions) {
        maxCollisions = bucketSize;
      }
      //计算总碰撞数：每个桶中超出1个的元素都算作碰撞
      if (bucketSize > 1) {
        totalCollisions += bucketSize - 1;// (桶大小 - 1) = 该桶的碰撞数
      }
    }
    // 返回诊断报告
    return {
      distribution,// 完整的桶分布映射
      maxCollisions,// 最坏情况下的链表/树长度
      totalCollisions,// 经历碰撞的元素总数
      loadFactor: this.size / this.capacity //loadFactor - 空间利用率，计算：总元素数 / 总桶数// 哈希表负载率
    };
  }
}
                                                /* 可选优化：紧凑型存储
                                                class CompactBucket {
                                                constructor() {
                                                    this.keys = [];     // 连续内存
                                                    this.values = [];   // 连续内存  
                                                    this.hashCodes = []; // 缓存哈希值
                                                }
                                                
                                                set(key, value, hashCode) {
                                                    // 保持数据局部性，提高缓存命中率
                                                    this.keys.push(key);
                                                    this.values.push(value);
                                                    this.hashCodes.push(hashCode);
                                                }
                                                }*/

//测试
function performanceTest() {
  const simpleTable = new SimpleHashTable(100);
  const industrialTable = new IndustrialHashTable(100);
  
  const keys = [];
  for (let i = 0; i < 10000; i++) {
    keys.push(`key${i}${Math.random()}`); // 模拟真实数据
  }
  // 测试插入性能
  console.time('简单哈希表插入');
  keys.forEach(key => simpleTable.put(key, 'value'));
  console.timeEnd('简单哈希表插入');
  console.time('工业哈希表插入');  
  keys.forEach(key => industrialTable.put(key, 'value'));
  console.timeEnd('工业哈希表插入');
  //🎯工业版更慢但碰撞更少:工业哈希表触发了9次扩容,每次扩容都需要:创建新数组,重新哈希所有元素,内存分配和数据迁移
  //🎯简单哈希表计算简单快速碰撞率高,工业哈希表分布均匀，碰撞少计算复杂，耗时更长
  //🎯在实际生产环境中，稳定性远比微小的性能差异更重要！
  // 测试碰撞分布
  const simpleStats = simpleTable.getCollisionDistribution?.();
  const industrialStats = industrialTable.getCollisionDistribution();
  console.log('简单版本最大碰撞:', simpleStats?.maxCollisions || 'N/A');
  console.log('工业版本最大碰撞:', industrialStats.maxCollisions);
}
performanceTest();

function demonstrateTreeifyProcess() {
  const table = new IndustrialHashTable();
  console.log("=== 树化过程演示 ===");
  // 阶段1：正常插入，使用链表
  for (let i = 1; i <= 7; i++) {
    table.put(`key${i}`, i);
    console.log(`插入key${i}, 桶大小: ${getBucketSize(table, 'key1')}`);
  }
  // 输出: 桶大小: 1→2→3...→7 (都是链表)
  // 阶段2：触发树化！
  table.put('key8', 8);
  console.log(`插入key8, 触发树化! 桶大小: ${getBucketSize(table, 'key1')}`);
  // 输出: 桶大小: 8 → 转为红黑树
  // 阶段3：树的优势体现
  console.log("现在在树结构中查找，时间复杂度O(log 8)");
  // 阶段4：触发退化
  table.remove('key8');
  table.remove('key7'); 
  table.remove('key6');
  console.log(`删除3个元素, 桶大小: ${getBucketSize(table, 'key1')}`);
  // 还是树结构，因为 5 > UNTREEIFY_THRESHOLD(6)? 等等...
  table.remove('key5');
  console.log(`再删除1个, 触发退化! 桶大小: ${getBucketSize(table, 'key1')}`);
  // 输出: 桶大小: 4 → 退化为链表
}
// 辅助函数：获取某个键所在桶的大小
function getBucketSize(table, key) {
  // 简化实现，实际需要访问内部状态
  return 0;
}
demonstrateTreeifyProcess();


function demonstrateTreeifyProcess() {
  console.log("=== 树化过程演示（修复版）===");
  
  // 方法1：使用小容量哈希表强制碰撞
  const table = new IndustrialHashTable(4); // 只有4个桶！
  
  // 方法2：使用相同前缀的键
  console.log("🎯 故意制造碰撞...");
  
  for (let i = 1; i <= 10; i++) {
    // 使用相同前缀确保哈希碰撞
    const key = `collision_key_${i}`; // 相同前缀
    table.put(key, i);
    
    // 检查第一个键所在的桶大小
    const firstKeyBucketSize = getBucketSize(table, 'collision_key_1');
    console.log(`插入${key}, 桶大小: ${firstKeyBucketSize}`);
    
    if (firstKeyBucketSize >= 8) {
      console.log(`🎉 触发树化！桶大小: ${firstKeyBucketSize}`);
    }
  }
  
  console.log("\n🌳 树化验证:");
  showDistribution(table);
}

// 运行修复版
demonstrateTreeifyProcess();

function superSimpleTreeifyTest() {
  console.log("=== 超简单树化测试 ===");
  // 创建只有2个桶的小哈希表
  const table = new IndustrialHashTable(2);
  // 关闭安全哈希，用简单哈希确保碰撞
  table._secureHash = function(key) {
    return 0; // 所有键都去桶0！
  };
  console.log("🧪 插入8个键到同一个桶...");
  for (let i = 1; i <= 8; i++) {
    table.put(`test${i}`, i);
    console.log(`插入test${i}, 桶0大小: ${table.buckets[0].size}`);
  }
  console.log(" 应该触发树化了！");
  console.log(" 当前分布:");
  showDistribution(table);
}
// 运行超简单版
superSimpleTreeifyTest();


function testUntreeifyProcess() {
  console.log("🔄 === 测试退化过程 ===");
  // 使用刚才成功树化的表
  const table = new IndustrialHashTable(2);
  table._secureHash = function(key) { return 0; };
  // 先触发树化
  for (let i = 1; i <= 8; i++) {
    table.put(`test${i}`, i);
  }
  console.log("✅ 树化完成");
  // 开始删除触发退化
  console.log("\n🗑️ 开始删除元素...");
  table.remove("test8");
  console.log(`删除test8, 桶0大小: ${table.buckets[0].size}`);
  table.remove("test7");
  console.log(`删除test7, 桶0大小: ${table.buckets[0].size}`);
  table.remove("test6"); 
  console.log(`删除test6, 桶0大小: ${table.buckets[0].size}`);
  table.remove("test5");
  console.log(`删除test5, 桶0大小: ${table.buckets[0].size}`);
  
  // 应该触发退化
  table.remove("test4");
  console.log(`删除test4, 桶0大小: ${table.buckets[0].size}`);
  console.log("📊 最终状态:");
  showDistribution(table);
}

// 运行退化测试
testUntreeifyProcess();


function testUntreeifyProcessFixed() {
  console.log("🔄 === 测试退化过程（修复版）===");
  
  const table = new IndustrialHashTable(2);
  table._secureHash = function(key) { return 0; };
  
  // 修改退化阈值为更敏感的值
  table.UNTREEIFY_THRESHOLD = 4;
  
  // 改进树化状态检测
  table._isTreeified = function(bucket) {
    return bucket.size >= 6; // 简化：桶大小曾经达到6就认为是树
  };
  
  // 先触发树化
  for (let i = 1; i <= 8; i++) {
    table.put(`test${i}`, i);
  }
  console.log("✅ 树化完成，桶0大小:", table.buckets[0].size);
  
  // 开始删除触发退化
  console.log("\n🗑️ 开始删除元素...");
  
  const keysToRemove = ["test8", "test7", "test6", "test5", "test4"];
  
  keysToRemove.forEach(key => {
    table.remove(key);
    const currentSize = table.buckets[0].size;
    console.log(`删除${key}, 桶0大小: ${currentSize}`);
    
    if (currentSize <= table.UNTREEIFY_THRESHOLD) {
      console.log("🔔 达到退化条件，应该触发退化！");
    }
  });
  
  console.log("📊 最终状态:");
  showDistribution(table);
}

// 运行修复版
testUntreeifyProcessFixed();

// 添加这个独立函数
function secureHash(key, seed = 123) {
  const keyStr = JSON.stringify(key);
  let hash = seed;
  
  for (let i = 0; i < keyStr.length; i++) {
    const char = keyStr.charCodeAt(i);
    hash = Math.imul(hash ^ char, 0x9E3779B9);
    hash = (hash << 5) | (hash >>> 27);
  }
  
  hash ^= keyStr.length;
  hash = Math.imul(hash ^ (hash >>> 16), 0x85EBCA6B);
  hash ^= hash >>> 15;
  
  return Math.abs(hash & 0x7FFFFFFF);
}
function demonstrateAvalanche() {
  console.log("=== 雪崩效应演示 ===");
  
  const testPairs = [
    ["hello", "hellp"],     // 1个字符不同
    ["color", "colour"],    // 1个字符不同
    ["abc", "acb"],         // 字符顺序不同
    ["", "a"]               // 长度不同
  ];
  
  testPairs.forEach(([str1, str2]) => {
    const hash1 = secureHash(str1, 123);
    const hash2 = secureHash(str2, 123);
    
    console.log(`"${str1}" → ${hash1}`);
    console.log(`"${str2}" → ${hash2}`);
    console.log(`差异: ${Math.abs(hash1 - hash2)}`);
    console.log("---");
  });
}
demonstrateAvalanche();
// 输出示例：
// "hello" → 583
// "hellp" → 924  ← 差异巨大！
// 差异: 341
// 添加缺失的 showDistribution 函数
function showDistribution(table) {
  const stats = table.getCollisionDistribution();
  console.log("📊 哈希表分布情况:");
  
  // 创建可视化图表
  const maxBarLength = 20;
  const maxCollisions = stats.maxCollisions;
  
  for (let i = 0; i < table.capacity; i++) {
    const bucketSize = stats.distribution[i] || 0;
    const barLength = maxCollisions > 0 ? Math.round((bucketSize / maxCollisions) * maxBarLength) : 0;
    const bar = '█'.repeat(barLength) || '│';
    
    console.log(`桶 ${i.toString().padStart(3)}: ${bar} ${bucketSize}个元素`);
  }
  
  console.log("\n📈 统计摘要:");
  console.log(`- 总元素数: ${stats.size || table.size}`);
  console.log(`- 最大碰撞: ${stats.maxCollisions}`);
  console.log(`- 总碰撞数: ${stats.totalCollisions}`);
  console.log(`- 负载因子: ${stats.loadFactor.toFixed(3)}`);
  console.log(`- 桶总数: ${table.capacity}`);
}

// 添加缺失的 getBucketSize 函数
function getBucketSize(table, key) {
  // 简化实现，通过尝试访问内部状态来获取桶大小
  try {
    const index = table._secureHash(key);
    return table.buckets[index].size;
  } catch (e) {
    return 0; // 如果无法访问，返回0
  }
}
function demonstrateResizeMagic() {
  const table = new IndustrialHashTable(4, 0.75); // 小城市测试
  
  // 插入一些数据
  const testData = ["Alice", "Bob", "Charlie", "David", "Eve"];
  testData.forEach(name => table.put(name, `${name}'s data`));
  
  console.log("=== 扩容前的分布 ===");
  console.log("城市大小: 4个区");
  showDistribution(table); // 显示每个区住了几户
  
  // 触发扩容！（插入第4个元素时，4*0.75=3，第4个触发扩容）
  table.put("Frank", "Frank's data");
  
  console.log("=== 扩容后的分布 ===");  
  console.log("城市大小: 8个区");
  showDistribution(table); // 显示重新分布后的情况
}
demonstrateResizeMagic();
// 可能的输出：
// 扩容前: 区0: 2户, 区1: 1户, 区2: 1户, 区3: 0户 ← 拥挤！
// 扩容后: 区0: 1户, 区1: 1户, 区2: 0户, 区3: 1户, 
//         区4: 1户, 区5: 1户, 区6: 1户, 区7: 0户 ← 均匀分布！

/*首先，我们需要一个简单的互斥锁实现
互斥锁的核心特性：
互斥性（Mutual Exclusion），     原子性（Atomicity），                      内存可见性（Memory Visibility）
同一时间只有一个线程能持有锁      // 锁的操作是原子的，不会被打断               //锁确保所有线程看到一致的内存状态
锁状态 = {                       锁操作 = {                                内存保证 = {
可用: "线程可以获取锁",            获取锁: "要么完全成功，要么完全失败",         加锁时: "强制刷新内存，让其他线程看到最新数据",
已锁定: "其他线程必须等待"         释放锁: "不会卡在中间状态"                   解锁时: "确保修改对其他线程可见"
};                                };                                            };
在哈希表中的互斥锁：分段锁的设计，🔒每个分段有自己的锁，每个分段有独立哈希表
在并发编程中，互斥锁确保：✅数据一致性-不会出现中间状态，✅操作原子性-要么完全成功，要么完全失败，✅执行顺序-避免竞争条件，✅内存可见性-所有线程看到一致的数据
互斥锁让多线程操作变得安全有序🔒
*/
class Mutex {
  constructor() {
    this._locked = false;
    this._waiting = [];
  }
  acquire() {//🔒获取锁
    return new Promise((resolve) => {
      if (!this._locked) {
        this._locked = true;
        resolve();
      } else {
        this._waiting.push(resolve);
      }
    });
  }

  release() { //🔓释放锁
    if (this._waiting.length > 0) {
      const next = this._waiting.shift();
      next();
    } else {
      this._locked = false;
    }
  }
}
/*
🔍一个线程在工作时，其他所有线程都必须等待
🎯线程需要锁：
1.保证原子性：一个操作要么完全完成，要么完全没开始，不会停留在中间状态
2.保证可见性：一个线程修改后，其他线程能立即看到最新结果
3.保证有序性：防止指令重排导致意外行为
4.防止数据损坏：避免并发修改导致数据结构破坏
🎯并发编程中一个核心的优化思想：大幅减少多线程环境下的锁竞争，从而提升并发性能。
🎯Segmented Locking. 分段锁：分段锁将底层的数据结构（这里是哈希表）分成多个逻辑段（Segment），在Java 7的 ConcurrentHashMap 中，每个Segment本质
上就是一个独立的小哈希表，它拥有自己的一把锁；
1.当线程要操作一个Key时，首先根据Key的哈希值计算出它属于哪个段
2.然后，线程只去获取那个特定段的锁
3.只要两个线程操作的Key落在不同的段，它们就可以真正地并行执行
🎯分段锁带来的好处：
1.高并发性：这是最主要的好处。默认情况下，支持16个线程并发写入（如果它们分布在不同的段上），极大地提高了吞吐量。
2.细粒度锁：锁的粒度从“整个表”缩小到了“段”，竞争的概率大大降低。
🔍从分段锁到CAS（Compare-And-Swap）：Java 8的 ConcurrentHashMap 又取消了分段锁
🎯为了更极致的并发性能；
🎯分段锁的粒度还是不够细；如果一个段非常热门（有很多操作），所有操作这个段的线程仍然要排队
🎯硬件和JDK的进步：Java 8利用了 sun.misc.Unsafe 提供的 CAS（Compare-And-Swap）原子操作CAS是一种乐观锁，它不需要真正的加锁。
在Java 8的 ConcurrentHashMap 中：
1.它完全摒弃了Segment的概念。
2.它的同步粒度是每个哈希桶的链表头节点（或红黑树根节点）。
3.对于put操作，如果桶是空的，就用CAS无锁地插入头节点；如果桶非空，则只锁住那个桶的头节点。
4.对于读操作（get），则完全不需要锁，因为使用了 volatile 关键字保证可见性。
🎯哈希表需要分段，是为了在多线程环境下，通过减小锁的粒度来减少竞争，从而提升性能。 这是一种在锁机制下非常有效的并发控制策略。随着技术的发展，它又被更先进的、基于CAS的无锁/细粒度锁技术所取代
*/
// 🔒 并发安全的哈希表
class ConcurrentHashTable {
  constructor(segmentsCount = 16) {
    this.segmentsCount = segmentsCount;
    this.segments = [];
    // 初始化所有分段
    for (let i = 0; i < segmentsCount; i++) {
      this.segments[i] = {
        lock: new Mutex(),  // 每个分段有自己的锁
        table: new IndustrialHashTable() // 每个分段有独立的哈希表
      };
    }
  }
  // 计算键属于哪个分段
  _segmentFor(key) {
    // 使用哈希函数确定分段，确保相同键总是到同一分段
    const hash = this._simpleHash(key);
    return hash % this.segmentsCount;
  }
  // 简单的哈希函数用于分段
  _simpleHash(key) {
    let hash = 0;
    const keyStr = key.toString();
    for (let i = 0; i < keyStr.length; i++) {
      hash = (hash << 5) - hash + keyStr.charCodeAt(i);
      hash |= 0; // 转换为32位整数
    }
    return Math.abs(hash);
  }
  //🔒并发安全的插入
  async put(key, value) {
    const segmentIndex = this._segmentFor(key);
    const segment = this.segments[segmentIndex];
    await segment.lock.acquire();  // 只锁这个分段
    try {
      return segment.table.put(key, value);
    } finally {
      segment.lock.release();  // 确保锁被释放
    }
  }
  // 🔒 并发安全的获取
  async get(key) {
    const segmentIndex = this._segmentFor(key);
    const segment = this.segments[segmentIndex];
    await segment.lock.acquire();
    try {
      return segment.table.get(key);
    } finally {
      segment.lock.release();
    }
  }

  // 🔒 并发安全的删除
  async remove(key) {
    const segmentIndex = this._segmentFor(key);
    const segment = this.segments[segmentIndex];
    await segment.lock.acquire();
    try {
      return segment.table.remove(key);
    } finally {
      segment.lock.release();
    }
  }
  // 统计信息（需要锁所有分段）
  async getStats() {
    // 按顺序锁住所有分段，避免死锁
    const locks = [];
    try {
      // 第一阶段：获取所有锁
      for (const segment of this.segments) {
        locks.push(await segment.lock.acquire());
      }
      // 第二阶段：统计信息
      let totalSize = 0;
      let maxBucketSize = 0;
      const segmentStats = [];
      for (let i = 0; i < this.segments.length; i++) {
        const segment = this.segments[i];
        // 这里需要 IndustrialHashTable 有获取内部状态的方法
        segmentStats.push({
          segmentIndex: i,
          size: segment.table.size,
          // 可以添加更多统计信息
        });
        totalSize += segment.table.size;
      }
      return {
        totalSize,
        segmentsCount: this.segmentsCount,
        segmentStats
      };
    } finally {
      // 第三阶段：释放所有锁
      for (const segment of this.segments) {
        segment.lock.release();
      }
    }
  }
}
//可视化演示：分段锁如何工作
// 演示并发场景
async function demonstrateConcurrentAccess() {
  console.log("=== 并发哈希表演示 ===");
  const concurrentTable = new ConcurrentHashTable(4); // 4个分段
  // 模拟多个客户端同时操作
  const promises = [];
  // 客户端1：操作键 "user1" (可能到分段1)
  promises.push((async () => {
    await concurrentTable.put("user1", "Alice");
    console.log("客户端1: 写入 user1");
  })());
  // 客户端2：操作键 "user2" (可能到分段3) 
  promises.push((async () => {
    await concurrentTable.put("user2", "Bob");
    console.log("客户端2: 写入 user2");
  })());
  // 客户端3：操作键 "product1" (可能到分段1)
  promises.push((async () => {
    await concurrentTable.put("product1", "Laptop");
    console.log("客户端3: 写入 product1");
  })());
  // 等待所有操作完成
  await Promise.all(promises);
  console.log("所有操作完成!");
  
  // 查看统计信息
  const stats = await concurrentTable.getStats();
  console.log("最终统计:", stats);
}
/*
分段锁的设计体现了空间换时间和细粒度控制的工程智慧
并发性：不同分段的操作可以真正并行
锁粒度：从"表级锁"细化到"分段锁"
可伸缩性：分段数可以根据CPU核心数调整
复杂性：实现更复杂，但换来性能的巨大提升
现代高并发系统（如数据库、缓存）都采用类似架构
// 优化1：读操作不加锁（读多写少场景）
async get(key) {
  const segmentIndex = this._segmentFor(key);
  const segment = this.segments[segmentIndex];
  
  // 尝试无锁读取（可能读到旧数据，但最终一致）
  const value = segment.table.get(key);
  if (value !== undefined) {
    return value;
  }
  
  // 如果没找到，加锁再试一次（防止正在写入的情况）
  await segment.lock.acquire();
  try {
    return segment.table.get(key);
  } finally {
    segment.lock.release();
  }
}

// 优化2：分段数动态调整
resizeSegments(newSegmentsCount) {
  // 根据并发度动态调整分段数量
}
*/

// 运行演示
demonstrateConcurrentAccess();
//分段锁的优势分析
// 对比演示：分段锁 vs 全局锁
class GlobalLockTable {
  constructor() {
    this.lock = new Mutex();
    this.table = new IndustrialHashTable();
  }
  
  async put(key, value) {
    await this.lock.acquire();  // 🔒 锁整个表
    try {
      return this.table.put(key, value);
    } finally {
      this.lock.release();
    }
  }
}
// 性能对比测试
async function performanceComparison() {
  const concurrentTable = new ConcurrentHashTable(16);
  const globalLockTable = new GlobalLockTable();
  const testKeys = Array.from({length: 100}, (_, i) => `key${i}`);
  // 测试并发表
  console.time('分段锁并发表');
  await Promise.all(testKeys.map(key => 
    concurrentTable.put(key, `value${key}`)
  ));
  console.timeEnd('分段锁并发表');
  // 测试全局锁表
  console.time('全局锁表');
  await Promise.all(testKeys.map(key =>
    globalLockTable.put(key, `value${key}`)  
  ));
  console.timeEnd('全局锁表');
}
```
3. **😎StealthDine System-隐蔽用餐编码系统完整实现**
```
//精简安全哈希器（保留所有核心运算）
class SecureHasher {
  constructor(secretKey = Math.random().toString(36).slice(2)) {//1.生成一个随机的私钥
    /*Math.random() → 生成 0.123456789 (随机小数),.toString(36) → 转为36进制："0.4fzyo82mvyr",.slice(2) → 去掉 "0."，得到 "4fzyo82mvyr"结果： 一个随机的字母数字字符串，如 "4fzyo82mvyr"
    */
    this.secretKey = secretKey;//2.私钥🔴这只是固定字符串，不是随机种子
    this.counter = 0;//3.添加计数器确保唯一性
    this.randomSeed = Math.floor(Math.random() * 0xFFFFFFFF); //🔑4.真正的随机种子
    console.log(" 私钥:", this.secretKey);
    console.log(" 随机种子:", this.randomSeed);
  }

  encode(number) {//number 的作用：编码真实选择//计数器的作用：确保唯一性
    /*
    核心用途——它把您简单的数字选择变成别人看不懂的随机代码：输入一个数字 → 输出一个防窥屏的随机代码
    encode(5) {
    // 1. 准备原料
    私钥指纹 = 1705260166      //    //来自_stringToHash，_stringToHash 只是准备工作，而encode是实际加密
    时间戳 = 1700000000000     |   //这样不安全：_stringToHash("5") → 固定结果（容易被破解）
    随机数 = 0.123456789       |   //这样安全：encode(5) = _stringToHash(私钥) + 时间戳 + 随机数 → 每次不同  
    // 2. 混合所有信息                               
    混合信息 = "5|mySuperSecretKey|1700000000000|0|0.123456789"
    // 3. 用同样的"搅拌方法"加密
    最终哈希 = 搅拌(混合信息)
    // 4. 转为友好格式
    return 最终哈希转36进制 = "4UL51Z"
}
    */
    //1.初始化哈希状态：设置哈希计算的"初始状态"// 阶段1：设置加密环境（只做一次）
    let hash = this.randomSeed ^ this._stringToHash(this.secretKey);
    /*
    //设置一个加密机器的初始配置                         特点：🔄每次会话不同（随机种子变化）
    随机种子 = 485760617        // 当前会话的临时密钥         🔐 身份绑定（私钥固定）
    私钥哈希 = -40005293        // 您的身份指纹              🎯 一次性：只在哈希计算开始时设置一次
    初始状态 = 485760617 ^ (-40005293) = 新的唯一值
    */
    //随机种子方式 提供了会话级别的安全性,私钥哈希方式提供了身份验证，但缺乏会话随机性,最佳实践：两者结合
    /*
    方式1：let hash = this.randomSeed//真正随机：每次程序重启都完全不同，会话隔离：不同运行会话产生不同序列，防预测：攻击者无法建立长期映射表                     
    // 每次程序启动时生成新的随机种子let hash = this.randomSeed;  // 用随机种子初始化，而不是固定值// 每次程序启动时生成新的随机种子
    this.randomSeed = 123456789  // 每次启动都不同
    encode(5) {
    let hash = 123456789;  // 直接从随机种子开始
    // 后续处理...
    }
    方式2：let hash = this._stringToHash(this.secretKey)//确定性：相同私钥总是产生相同的初始值，可重现：只要私钥相同，结果序列就相同，可能被分析：长期使用可能暴露模式
    // 基于固定私钥计算初始值
    this.secretKey = "mySecret"  // 固定不变
    encode(5) {
    let hash = this._stringToHash("mySecret");  // 总是得到相同的数字
    // 后续处理...
    //工业级安全哈希的设计思想
    会话随机性：相同输入在不同时间产生不同输出
    身份验证：只有知道私钥的人能参与系统
    防长期分析：重启后完全刷新序列
    双重保护：需要同时知道私钥和当前随机种子
    //我们的原理: 双重依赖,防单点失效,时间敏感性, 编码基于时间戳，每次不同
    function encode(number) {
    const timeWindow = Date.now(); // 更细的时间粒度
    return hash(随机种子 + 私钥 + number + timeWindow + 计数器);
    }
    number 的作用：编码真实选择
    计数器的作用：确保唯一性// 同一毫秒内连续调用,即使时间相同，计数器确保每次输入都不同
    // 问题：在同一个毫秒内快速调用
    encode(5) // 时间戳相同，可能产生相同结果
    encode(5) // 时间戳相同，可能产生相同结果
    // 解决方案：加入计数器
    encode(5) // counter=0 → 输入包含 "|0|"
    encode(5) // counter=1 → 输入包含 "|1|" → 确保不同！
    }
    function encode(5) {
        // 准备所有原料
        const 原料 = {
            随机种子: 485760617,     // 会话安全
            私钥: "sameSecret",      // 身份验证  
            真实选择: 5,             //  意图 👈 number
            时间戳: 1700000000000,   // 时间保护
            计数器: 3,               // 唯一性保证 👈 计数器
            随机数: 0.123456789      // 额外随机性
        };
        // 混合所有原料
        const 混合信息 = "5|sameSecret|1700000000000|3|0.123456789";
        // 哈希计算
        return 哈希(混合信息) → "GRAIVK";
        }
    */
    //🔐 用私钥初始化//用您的私钥来初始化哈希值,取出您的私钥 this.secretKey,通过_stringToHash方法将私钥转换成一个数字,用这个数字作为哈希计算的初始状态,返回一个基于私钥的数字
    //2.构建输入数据：准备要被哈希的"原始数据"// 阶段2：准备要加密的内容（每次不同）
    const input = `${number}|${this.secretKey}|${Date.now()}|${this.counter++}|${Math.random()}`;//每次调用 counter 都会增加
    /*
    把信息放入加密机器处理                                    特点：📝每次调用都构建新的数据
    输入数据 = "5|sameSecret|1700000000000|3|0.123456789"        🔄计数器自动递增确保唯一性
        ↓                                                      🕒包含实时信息（时间戳、随机数）
        ↓ 数字5   私钥     时间戳    计数器   随机数
        ↓ (选择)(身份验证)(时间保护)(唯一性)(随机性)
        */
        //核心：混合数字、私钥、时间戳
    //const input = `${number}|${this.secretKey}|${Date.now()}`;//后续的哈希计算都基于这个初始状态
    //阶段3：核心加密计算
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      //保留所有核心位运算
      hash = Math.imul(hash ^ char, 0x9E3779B9);  // 异或 + 黄金比例乘法
      hash = (hash << 7) | (hash >>> 25);         // 位旋转
    }
    //阶段4：最终处理//阶段4 = 格式化和输出
    hash ^= input.length;
    hash = Math.imul(hash ^ (hash >>> 16), 0x85EBCA6B);
    hash ^= hash >>> 15;
    return Math.abs(hash & 0x7FFFFFFF).toString(36).toUpperCase();
  }
  /*
  哈希函数的灵魂，它确保了✅均匀分布，✅碰撞抵抗，✅雪崩效应，✅不可预测性
  */
  // 辅助函数：将字符串转为初始哈希值
  /*
  _stringToHash("mySuperSecretKey") {
  let hash = 0;  // 从0开始
  // 对私钥的每个字符进行"搅拌"
  for (每个字符 in "mySuperSecretKey") {
    // 两步搅拌：
    hash = (当前hash 异或 字符编码) × 黄金比例数
    hash = 左转7位 | 右转25位  // 像拧魔方一样旋转
  }
  return hash; // 得到最终的数字指纹: 1705260166//这个"数字指纹" 1705260166 
  //数字指纹会成为后续编码的基础：只有知道私钥的人能生成相同的编码序列，不同私钥的人会得到完全不同的结果，先把私钥变成数字，再用这个数字去加密选择
}
  */
  _stringToHash(str) {
    let hash = 0;
    console.log(`开始处理私钥: "${str}"`);
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      const before = hash;
      hash = Math.imul(hash ^ char, 0x9E3779B9);
      hash = (hash << 7) | (hash >>> 25);
      console.log(`  字符 '${str[i]}' (${char}): ${before} → ${hash}`);
    }
    console.log(`私钥处理完成: ${hash}`);
    return hash;
  }
  // 批量生成（用于测试）// 验证同一个数字在不同时间编码会产生不同结果"
  testEncode(number, times = 5) { //默认测试5次
    console.log(`=== 测试编码数字 ${number} ===`);
    for (let i = 0; i < times; i++) {
      console.log(`结果 ${i+1}:`, this.encode(number));
    }
  }
}
/* 初始化
const hasher = new SecureHasher("mySuperSecretKey");
// 测试不同数字
console.log("=== 安全哈希演示 ===");
hasher.testEncode(5);   //testEncode(5) 的作用：对数字5进行5次编码测试,每次都会生成不同的随机字符串,用来演示即使选择同一家店，不同时间也会生成不同代码"
hasher.testEncode(8);   // 
hasher.testEncode(12);  
// 结果：三个测试几乎同时开始，互相干扰！testEncode() 方法被设计为异步的（有 await），但是用同步的方式调用了它。
/*async function runDemo() {
  console.log("=== 安全哈希演示 ===");
  await hasher.testEncode(5);   // 等待完成
  await hasher.testEncode(8);   // 再执行下一个//testEncode(8) 只显示5个结果是因为 testEncode 方法本身就是设计为测试5次的
  await hasher.testEncode(12);  // 再执行下一个
  runDemo();
}*/
/* 演示不同私钥的效果
console.log("=== 不同私钥的初始化演示 ===");
const hasher1 = new SecureHasher("abc");
const hasher2 = new SecureHasher("xyz");
console.log("编码数字5:");
console.log("私钥abc结果:", hasher1.encode(5));
console.log("私钥xyz结果:", hasher2.encode(5));*/
function compareInitialization() {
  console.log("=== 初始化方式对比 ===");
  // 测试方式1：随机种子
  const hasher1 = new SecureHasher("sameSecret");
  console.log("随机种子方式:");
  console.log("会话1 - 选择5:", hasher1.encode(5));
  console.log("会话1 - 再选5:", hasher1.encode(5));
  // 模拟重启
  const hasher2 = new SecureHasher("sameSecret"); 
  console.log("会话2 - 选择5:", hasher2.encode(5)); // 🔥 完全不同！
  console.log("\n------------------------");
  // 测试方式2：私钥哈希
  class OldHasher {
    constructor(secret) {
      this.secretKey = secret;
      this.counter = 0;
    }
    encode(number) {
      let hash = this._stringToHash(this.secretKey);  // 固定初始值
      const input = `${number}|${Date.now()}|${this.counter++}|${Math.random()}`;
      // ... 后续处理相同
      return "模拟结果";
    }
    _stringToHash(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = Math.imul(hash ^ str.charCodeAt(i), 0x9E3779B9);
      }
      return hash;  // 总是返回相同值
    }
  }
  const old1 = new OldHasher("sameSecret");
  const old2 = new OldHasher("sameSecret");
  console.log("私钥哈希方式:");
  console.log("实例1 初始值:", old1._stringToHash("sameSecret"));
  console.log("实例2 初始值:", old2._stringToHash("sameSecret")); // 🔥 相同！
}
compareInitialization();

function comprehensiveSecurityTest() {
  console.log("🔒 === 全面安全测试 ===");
  const hasher = new SecureHasher("myTestSecret");
  // 🧪 测试1：相同输入的时间敏感性
  console.log("\n1. 时间敏感性测试");
  console.log("同时刻两次编码同一数字:");
  const sameTime1 = hasher.encode(5);
  const sameTime2 = hasher.encode(5);
  console.log("结果1:", sameTime1);
  console.log("结果2:", sameTime2);
  console.log("是否不同?", sameTime1 !== sameTime2 ? "✅" : "❌");
  // 🧪 测试2：雪崩效应
  console.log("\n2. 雪崩效应测试");
  console.log("微小数字变化:");
  const results = [];
  for (let i = 495; i <= 505; i++) {
    const code = hasher.encode(i);
    results.push(code);
    console.log(`数字 ${i} → ${code}`);
  }
  // 检查所有结果是否唯一
  const uniqueResults = new Set(results);
  console.log(`生成了 ${results.length} 个编码，其中 ${uniqueResults.size} 个唯一`);
  console.log("雪崩效应:", uniqueResults.size === results.length ? "✅" : "❌");
  // 🧪 测试3：模式分析抵抗
  console.log("\n3. 模式分析抵抗测试");
  console.log("连续选择同一数字10次:");
  const patternTest = [];
  for (let i = 0; i < 10; i++) {
    patternTest.push(hasher.encode(8));
  }
  // 检查是否有重复模式
  const hasPattern = patternTest.some((code, index) => 
    index > 0 && code === patternTest[index - 1]
  );
  console.log("模式测试结果:", patternTest);
  console.log("抵抗模式分析:", !hasPattern ? "✅" : "❌");
  // 🧪 测试4：私钥依赖性
  console.log("\n4. 私钥依赖性测试");
  const hasherA = new SecureHasher("secretA");
  const hasherB = new SecureHasher("secretB");
  const codeA = hasherA.encode(5);
  const codeB = hasherB.encode(5);
  console.log("相同输入5，不同私钥:");
  console.log("私钥A结果:", codeA);
  console.log("私钥B结果:", codeB);
  console.log("私钥保护:", codeA !== codeB ? "✅" : "❌");
  // 🧪 测试5：会话隔离性
  console.log("\n5. 会话隔离性测试");
  const session1 = new SecureHasher("sameSecret");
  const session2 = new SecureHasher("sameSecret");
  const session1Code = session1.encode(5);
  const session2Code = session2.encode(5);
  console.log("相同私钥，不同会话:");
  console.log("会话1:", session1Code);
  console.log("会话2:", session2Code);
  console.log("会话隔离:", session1Code !== session2Code ? "✅" : "❌");
}
// 运行全面测试
comprehensiveSecurityTest();

function antiPeepingTest() {
  console.log("👀 === 防窥屏专项测试 ===");
  const hasher = new SecureHasher("diningSecret");
  // 模拟真实用餐选择场景// 步骤A：查找餐厅名称
  const restaurantChoices = [
    { number: 1, name: "McDonald's" },
    { number: 2, name: "KFC" },
    { number: 3, name: "Starbucks" },
    { number: 4, name: "Pizza Hut" },
    { number: 5, name: "Haidilao" },

  ];
  console.log("\n📊餐厅选择编码表:");
  restaurantChoices.forEach(restaurant => {
    const code = hasher.encode(restaurant.number);// 步骤B：生成防窥屏代码
    console.log(`${restaurant.number}. ${restaurant.name} → ${code}`);
  });
  // 模拟窥屏者视角
  console.log("\n🎭 窥屏者视角模拟:");
  console.log("窥屏者看到以下代码，但不知道含义:");
  const observedCodes = [];
  for (let i = 0; i < 5; i++) {
    const randomChoice = Math.floor(Math.random() * 5) + 1;
    const code = hasher.encode(randomChoice);
    observedCodes.push(code);
    console.log(`观察到代码: ${code} (实际选择: ${randomChoice}号店)`);
  }
  // 分析窥屏效果
  console.log("\n🔍 防窥屏效果分析:");
  const uniqueCodes = new Set(observedCodes);
  console.log(`观察到 ${observedCodes.length} 个代码，其中 ${uniqueCodes.size} 个唯一`);
  console.log("防窥屏效果:", uniqueCodes.size === observedCodes.length ? "✅ 优秀" : "❌ 有风险");
  // 测试重复选择
  console.log("\n🔄 重复选择测试:");
  console.log("连续3次选择同一家店:");
  const repeatedChoice = 3; // 星巴克
  for (let i = 0; i < 3; i++) {
    const code = hasher.encode(repeatedChoice);
    console.log(`第${i+1}次选择星巴克 → ${code}`);
  }
}
// 运行防窥屏测试
antiPeepingTest();

/*使用
// 1. 创建哈希器（只需要做一次）
const hasher = new SecureHasher("myKey");
// 2. 直接生成代码并打印
console.log("我的订餐代码:", hasher.encode(1)); 传入数字就行*/ 

/*性能与碰撞测试
function performanceAndCollisionTest() {
  console.log("⚡ === 性能与碰撞测试 ===");
  const hasher = new SecureHasher("performanceTest");
  const testSize = 1000;
  const results = new Map();
  let collisions = 0;
  
  console.log(`生成 ${testSize} 个随机编码...`);
  console.time("生成时间");
  
  for (let i = 0; i < testSize; i++) {
    const randomNumber = Math.floor(Math.random() * 1000);
    const code = hasher.encode(randomNumber);
    
    if (results.has(code)) {
      collisions++;
      console.warn(`🚨 碰撞发现: ${code} 对应 ${results.get(code)} 和 ${randomNumber}`);
    } else {
      results.set(code, randomNumber);
    }
  }
  console.timeEnd("生成时间");
  console.log("\n📈 测试结果统计:");
  console.log(`总生成数: ${testSize}`);
  console.log(`唯一编码数: ${results.size}`);
  console.log(`碰撞次数: ${collisions}`);
  console.log(`碰撞率: ${((collisions / testSize) * 100).toFixed(4)}%`);
  console.log("碰撞抵抗:", collisions === 0 ? "✅ 完美" : collisions < 5 ? "⚠️ 良好" : "❌ 需优化");
}

// 运行性能测试
performanceAndCollisionTest();
*/
```