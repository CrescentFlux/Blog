#  Compressed Suffix Tree
## 基础知识
- 定义
```
后缀树是一种压缩的字典树，它存储了一个字符串的所有后缀，并通过巧妙的压缩技术将空间复杂度优化到线性级别。核心价值：一次预处理，终身快速查询。
```

- 结构特性分析

    - 树形结构特征：后缀树呈现出一棵有根树的形态，从根节点到每个叶节点的路径唯一对应一个完整的后缀。内部节点代表多个后缀共享的公共前缀，叶节点则标识各个后缀的起始位置。

    - 边的标签特性：边的标签可能是单个字符，也可能是较长的子串，这取决于路径压缩的程度。标签内容通过起始和结束索引引用原始文本，实现数据的零复制共享。
      


    - 空间优化机制：通过路径压缩和索引存储双重技术，后缀树将理论上的平方级空间复杂度优化到线性级别，使其能够处理大规模文本数据。


|方向	|核心要点|	详细说明|
---|---|---
|本质定义|	有向文本载体|	连接两节点的有向链接，承载文本片段信息，通过索引引用原始文本|
|物理特性|	索引存储	|不存实际文本，用(start,end)索引标识文本位置，所有边共享原始文本|
|	|长度可变	|长度从1字符到多字符不等，取决于路径压缩程度|
|	|方向明确|	从父节点指向子节点，体现匹配的先后顺序|
|逻辑作用|	文本承载|	路径上所有边标签连接形成完整后缀|
|	|匹配导航|	首字符决定搜索分支选择，指导匹配方向|
|	|结构连接|	连接独立节点形成完整树形骨架|
|分类特征|	按位置分|	根边(连根节点)、内部边(连内部节点)、叶边(通叶节点)|
|	|按长度分|	单字符边、多字符边、空边(应避免)|
|节点关系|	父子体现|	定义节点间父子关系，形成层次结构|
|	|信息互补|	节点管结构，边管文本承载，共同完成信息存储|
|	|动态调整|	分裂时边与节点同步重组，维护结构正确性|
|操作特性|	创建时机|	插入新后缀时创建根边，分裂时创建新叶边|
|	|标签更新|	路径压缩时合并相邻边，形成更长标签|
|	|结构调整|	重平衡时连接关系变化，保持文本完整性|
|实际意义	|空间优化|	可变长度标签实现极致空间压缩|
|	|查询效率|	智能设计支持快速跳过字符，提升匹配速度|
|	|结构清晰|	明确标签和方向使结构易于理解维护|
|特殊现象|	共享标签|	不同边可指向文本相同区域，索引存储的自然结果|
|	|重叠引用|	复杂结构中以不同方式引用文本，形成精妙索引网络|
|	|动态演化|	构建过程中标签和连接关系不断演化至最优状态|







## 注意事项
1. **混淆点**

- 关键概念

|概念	|关键理解|
---|---
|后缀	|从文本的某个位置开始直到结束的整个子串，不是任意片段|
|后缀树	|所有后缀的压缩字典树，包含文本全部后缀信息|
|路径压缩|	将没有分支的连续路径合并为单一边，边上存储子串而非单字符|
|边的标签|	可能包含多个字符，通过start和end索引指向原始文本|
|节点|	不存储实际字符串，只存储文本中的起始和结束位置索引|
|内部节点|	代表多个后缀共享的公共前缀|
|叶子节点|	每个叶子唯一对应一个后缀的起始位置|
|分裂操作|	在字符匹配结束的位置创建新节点，提取公共前缀|
|完全匹配|	当前边上所有字符都匹配成功，继续处理后缀剩余部分|
|部分匹配|	在第一个不匹配字符处分裂节点，创建新分支|
|后缀链接|	优化构建过程的指针，用于快速跳转（Ukkonen算法）|
|时间复杂度|	构建O(n)，查询O(m)，与文本大小无关|
|空间复杂度|	O(n)，通过路径压缩优化|
|查询原理|	从根开始逐字符匹配，完全匹配后收集所有叶子位置|



- 构建过程关键点

|阶段	|核心操作|
---|---
|初始化	|创建根节点，文本添加终止符$|
|插入后缀	|逐个处理后缀，从首字符开始匹配|
|匹配决策|	完全匹配继续向下，部分匹配分裂节点|
|分裂重组	|创建内部节点代表公共前缀，调整原子节点关系|
|路径压缩|	自动合并无分支路径，优化空间效率|




- 查询特性

|特性	|说明|
---|---
|精确匹配|	返回模式串所有出现位置，不只是存在性|
|前缀搜索|	自然支持，找到所有以某前缀开头的后缀|
|多模式匹配|	一次预处理，支持多次不同模式查询|
|空间效率|	所有节点共享原始文本，避免重复存储|






2. 代码实现调试版
```
//----------调试版本15-----------//
//节点定义与树结构
class SuffixTreeNode {//后缀树节点
    constructor() {
        //🟢节点不存储实际的字符串值，只存储 start 和 end 索引。实际的文本需要通过 T.substring(start, end+1) 计算得到。
        //🟢children 表建立了字符到子节点内存地址的映射；叶子节点的 children 通常为空对象 {}。
        //🟢节省了大量内存，所有节点都共享原始字符串 T，不需要重复存储字符串内容
        this.children = {};
        //子节点映射表；键：边的起始字符；值：子节点对象//节点不代表一个字符，而是代表一条边，这条边上可能存储着一个子串
        //children对象记录了从这个节点出发的所有出边。每条出边由一个起始字符（Key）和对应的子节点（Value）定义
        this.start = -1;//start 和 end 定义了这条边的文本内容；实际文本通过原始字符串.substring(start, end+1) 获得
        this.end = -1;//该节点代表的边，其文本在原始字符串中的结束索引
        this.suffixLink = null;//用于优化构建过程的指针（在Ukkonen算法中使用）
        //不直接存储字符串，而是存储索引：节省内存（所有边共享同一个字符串），快速子串提取（通过 text.substring(start, end+1) 获取实际文本）
    }
}
class SuffixTree {//后缀树的构造函数：把字符串的每一个后缀，一个一个地塞进树里
    constructor(text) {//它确保了每个后缀都被处理
        this.text = text;// 把原始字符串存起来
        this.root = new SuffixTreeNode();// 创建一棵空树，只有一个根节点
        //this.build(); //🚨开始建树//构造函数中不能直接调用build
    }
    build() {//把字符串从头到尾的每一个后缀，按顺序一个一个添加到树里//后缀树的定义就是：包含这个字符串所有后缀的一棵树
        const n = this.text.length;
        for (let i = 0; i < n; i++) {
            // 逐个添加后缀
            this._addSuffix(i);//构建方法：找到所有后缀（通过改变起始位置 i），把这些后缀一个一个插入树中，插入时树会自动处理共享前缀和路径压缩
        }
    }
     //简单的调试方法
    debugStepByStep() {
        const n = this.text.length;
        console.log(`=== 构建后缀树: "${this.text}" ===`);
        for (let i = 0; i < n; i++) {
            console.log(`\n🎯 步骤 ${i}: 插入后缀 "${this.text.substring(i)}"`);
            console.log("插入前:");
            this._printSimple();
            this._addSuffix(i);
            console.log("插入后:");
            this._printSimple();
            console.log("-------------------");
        }
    }
    _printSimple(node = this.root, indent = 0) {
        let space = "  ".repeat(indent);
        if (node === this.root) {
            console.log(space + "根");
        } else {
            let edgeText = this.text.substring(node.start, node.end + 1);
            let type = Object.keys(node.children).length === 0 ? "叶" : "内";
            console.log(space + `[${edgeText}] (${type}, start=${node.start})`);
        }
        for (let [char, child] of Object.entries(node.children)) {
            this._printSimple(child, indent + 1);
        }
    }
    //后缀的基础逻辑：找到后缀的起始位置
    
_addSuffix(suffixIndex) {//🎯创建新的分支
    //suffixIndex参数本身就是后缀的起始位置//处理一个后缀的第一个字符//把相同的前缀提取出来变成内部节点
    //🟢每次插入的都是一个独立的后缀字符串；树在每次插入后都保持完整状态；下一次插入是在当前树的基础上，插入另一个独立的后缀
    let currentNode = this.root;
    let currentChar = this.text[suffixIndex];//suffixIndex要插入的后缀的起始位置
    //这个后缀的第一个字符在根节点还没有出现过，直接创建一个新边来存储整个后缀
    if (!currentNode.children[currentChar]) {//currentChar 是这个后缀的第一个字符
        //1.创建新的叶子节点
        let leaf = new SuffixTreeNode();
        leaf.start = suffixIndex;// 后缀从这里开始
        leaf.end = this.text.length - 1;//一直到文本结束
        currentNode.children[currentChar] = leaf;//存储的是字符串，不是节点对象//🟢在父节点的children表中创建一条新边，这条边指向新创建的叶子节点//节点=部门，边=部门名称牌+部门职责范围
    } else {
        // 处理已有分支的情况//这个后缀的第一个字符在根节点已经有对应的边了，需要沿着这条边继续走下去，看看能匹配多少
        this._walkDown(suffixIndex, currentNode.children[currentChar]);//currentNode.children[currentChar]：父部门门口挂的牌子指向的那个具体部门
    }
}

_walkDown(suffixIndex, node) {//🎯分支已经被创建的话就进行比较找到分歧点
    //共享前缀的后缀会共享树的一部分路径:如果多个后缀开头几个字符相同，那么在后缀树中它们从根节点开始会走同一条边（或同几条边），直到第一个不同的字符才分开
    //🟢在普通字典树中，每条边只代表1个字符，但在后缀树中，一条边可以代表多个字符//边的长度就是边上存储的字符个数
    //🟢后缀树不实际重复存储字符，而是通过 start 和 end 索引指向原始字符串的同一份数据
    //🟢1.计算当前边的长度
     console.log(`🔍 _walkDown: 后缀="${this.text.substring(suffixIndex)}", 边="${this.text.substring(node.start, node.end + 1)}"`);
    let edgeLength = node.end - node.start + 1;
    //其实可以直接比较，但算长度是为了效率优化//批量操作效率高：一次取子串比逐个字符比较快，利用底层优化：JavaScript引擎的字符串比较是高度优化的代码清晰
    //子串操作是左闭右开[start, end)为了包含结束索引位置的字符，需要在 end 后面 +1
    //在后缀树中，一条边可能代表多个字符，而不仅仅是单个字符;这次匹配消费了多少个字符,还剩下多少个字符需要继续处理,从哪个位置开始继续匹配剩余部分
    //🟢2.从要插入的后缀中，截取一段文本，准备与树上的边进行比较//准备比较材料——从后缀中取出与边等长的文本片段，准备进行匹配比较
    let textToMatch = this.text.substring(suffixIndex, suffixIndex + edgeLength);
    //🟢3.获取树上当前边上存储的实际文本内容
    let edgeText = this.text.substring(node.start, node.end + 1);
    console.log(`   textToMatch="${textToMatch}", edgeText="${edgeText}"`);
    //🚨详细比较每个字符:
    let matchLength = 0;
    for (let i = 0; i < Math.min(textToMatch.length, edgeText.length); i++) {
        let char1 = textToMatch[i];
        let char2 = edgeText[i];
        console.log(`   比较 位置${i}: '${char1}' vs '${char2}' = ${char1 === char2}`);
        
        if (textToMatch[i] === edgeText[i]) {
            matchLength++;
        } else {
            break;
        }
    }
    
    console.log(`  匹配长度: ${matchLength}`);
    //🟢4.后缀树构建的决策核心：
    if (textToMatch === edgeText) {//textToMatch要插入的后缀片段，edgeText边上存储的文本
        //这条边上的所有字符都匹配成功了！现在去处理这个后缀还剩下的部分//要插入的后缀片段与边上存储的文本完全一致
        //如果还有剩余字符，继续处理，否则什么都不做//🔧修复：检查是否还有剩余字符
                let nextIndex = suffixIndex + edgeLength;//
//suffixIndex要匹配的当前字符串在原文本中的索引位置，edgeLength是匹配到共享前缀时共享前缀边边 "a" 的长度，nextindex表示匹配完共享前缀之后要处理的下一个字母在原文本中的索引位置
                if (nextIndex < this.text.length) {
                // ✅ 安全地访问this.text[nextIndex]
                let nextChar = this.text[nextIndex];//🔧修复：先定义 nextChar // this.text[10] = 'u'//🔴这里nextIndex可能超出范围！：应该先检查 nextIndex 是否有效，再访问 this.text[nextIndex]
                //🔴：在if块内定义nextChar：变量作用域：else这里nextChar不可用；把 nextChar 的定义移到if语句外面；
                //🔴：Uncaught TypeError: can't access property "start", node is undefined：说明 node.children[nextChar] 是 undefined，但代码试图访问它的 start 属性：需要确保 node.children[nextChar] 存在才调用 _walkDown：
                //this._addSuffix(nextIndex);//🔧完全匹配后错误地从根节点重新开始处理剩余部分，而不是在当前匹配的节点下继续处理。
                // 如果 nextIndex >= text.length，说明这个后缀已经处理完了
                if (node.children[nextChar]) {// 检查是否存在对应的子节点：关键就是：先检查索引有效性，再访问数组
                this._walkDown(nextIndex, node.children[nextChar]);}//🚨修复：在当前节点下继续，而不是从根节点开始
                //🎯继续在当前分支下匹配剩余部分，不要回到根节点重新开始；
                // node.children[nextChar] - "沿着哪条路走"作用：下一个要比较的分支节点：从na开始而不是直接创建新的节点存储us
            }else {
            // 创建新叶子节点作为当前节点的子节点
            //🔧当完全匹配后，还有剩余字符，但当前节点也就是na共享前缀下面没有以剩余字符开头的子分支时，这时候就需要创建新叶子；确保每个后缀的剩余部分都能在正确的位置被存储
            let leaf = new SuffixTreeNode();
            leaf.start = nextIndex;
            leaf.end = this.text.length - 1;
            node.children[nextChar] = leaf;//🔧ReferenceError!
           //🔧nextIndex = 10，对应字符u：// 第一轮：比较 "anaus" 和 "a"suffixIndex = 7edgeLength = 1  // 边 "a" 的长度nextIndex = 7 + 1 = 8
           //第二轮：比较 "naus" 和 "na"  suffixIndex = 8，edgeLength = 2  // 边 "na" 的长度，nextIndex = 8 + 2 = 10
        }
        //this._addSuffix(suffixIndex + edgeLength);//🔧无限递归，需要改用迭代方式沿着树向下走，避免在相同节点上重复调用 _addSuffix
        //🟢完全匹配时只是递归调用，但递归的终点可能什么都不做；完全匹配 = 这个后缀已经存在于树中，不需要重复添加；完全匹配时不会创建新节点
        //实际上，如果这条边已经匹配完了整个后缀，那么 suffixIndex + edgeLength 就会超出文本范围，什么都不做；
    } else {
        //🚨修复：添加 matchLength 的计算
        let matchLength = 0;
        for (let i = 0; i < Math.min(textToMatch.length, edgeText.length); i++) {
            if (textToMatch[i] === edgeText[i]) {
                matchLength++;
            } else {
                break;
            }
        }
        //只有前面一部分字符匹配，后面出现分歧了！需要在这里分裂节点
        this._splitNode(node,suffixIndex, matchLength);
    }
}

_splitNode(node, suffixIndex, matchLength) {
    //在分裂操作中，node 参数指的是当前正在比较的那个节点，也就是需要被分裂的节点；suffixIndex 是当前要插入的后缀在原始文本中的起始位置
    // 创建新的内部节点，代表公共前缀
    let internalNode = new SuffixTreeNode();
    internalNode.start = node.start; // 创建代表"共享前缀"的内部节点；（从原节点开始位置开始）
    internalNode.end = node.start + matchLength - 1; //到匹配结束的位置//matchLength 是实际匹配的字符数量//-1 是索引计算和子串操作的特性
    // 1.调整原节点代表未匹配的剩余部分
    //🎯原来的 "anana" 信息没有丢失：只是从：一个节点存储完整字符串变成了：两个节点通过路径连接来表达同一个字符串//原来的 "anana" 还在，只是存储方式从"整块"变成了"分块"！
    node.start = node.start + matchLength; 
    // 2.创建新的叶子节点
    let newLeaf = new SuffixTreeNode();
    newLeaf.start = suffixIndex + matchLength;//完整后缀：从 suffixIndex 开始到文本结束；//newLeaf.start不是完整后缀的起始位置，而是匹配完成后剩余部分的起始位置
    newLeaf.end = this.text.length - 1;//新叶子节点代表的边，从它的 start 位置开始，一直到文本的最后一个字符  
    // 检查是否有剩余字符//🚨关键修复：只在有剩余字符时创建新叶子
    if (newLeaf.start < this.text.length) {
        newLeaf.end = this.text.length - 1;
    } else {
        //没有剩余字符，标记为叶子但边为空//空叶子虽然不理想，但至少不会崩溃，它表示从这里开始没有更多字符了
        //给文本添加终止符 $，这样所有后缀都有明确的结束，就不会出现空边了
        newLeaf.end = newLeaf.start;
    }
   
   
    // 3.重新组织父子关系
    let parent = this._findParent(node);//找到父节点
    let firstChar = this.text[internalNode.start];//确定新部门的标识
    parent.children[firstChar] = internalNode;//让父节点重新指向子节点
    internalNode.children[this.text[node.start]] = node;//让原节点变成新内部节点的子节点
    internalNode.children[this.text[newLeaf.start]] = newLeaf;//让新叶子也变成新的内部节点的子节点
    //当新后缀有剩余字符时：原节点：代表剩余部分；新叶子：代表新后缀的剩余部分
    //即使路径中"隐含"了某个后缀，仍然需要显式插入：
}

_findParent(node) {
    // 实现查找父节点的逻辑
    let queue = [this.root];
    while (queue.length > 0) {
        let current = queue.shift();
        for (let child of Object.values(current.children)) {
            if (child === node) {//找到这个节点的直接上级在树中查找某个节点的父节点
                return current;
            }
            queue.push(child);
        }
    }
    return null;
    
}
//-------💡注意----------//

    /*后缀树旨在解决的核心字符串问题是：在给定的文本T中，高效地查找任意模式P的所有出现位置
    该数据结构建立在一个关键之上：任何模式P在T中的出现，必然是T的某个后缀的前缀。
    构建后缀树的第一步是枚举文本T的所有后缀
    一种朴素的构建方法是将所有后缀存入一棵Trie或后缀Trie树中。然而，该方法的空间复杂度为O(n²)，在实践中难以承受。
    为优化空间效率，引入了路径压缩技术，将树中不存在分支的连续路径合并为单一边，边标签由单个字符扩展为子串
    经优化后，所得数据结构的空间复杂度降至O(n)，该结构被正式称为后缀树
    在该结构中，从根节点到任意叶子节点的路径唯一对应于原文本的一个后缀
    其查询操作的效率极高，对于长度为m的模式P，时间复杂度为O(m)，与文本T的长度无关
    后缀树不仅能用于子串查询，还能高效解决最长重复子串、最长公共子串，最大回文子串，数据压缩等一系列复杂的字符串问题。
    构建后缀树的经典算法是Ukkonen算法，其在线性时间内完成构建。
    通过对文本的一次深度预处理，构建一个万能索引，从而为所有基于“子串”和“重复模式”的查询与分析提供近乎即时的回答*/
//---------❌注意--------//
//Uncaught InternalError: too much recursion：说明代码中有无限递归：原来的代码在完全匹配时，即使后缀已经处理完了（比如整个后缀都匹配了），还是会调用_addSuffix导致
//Uncaught ReferenceError: matchLength is not defined：在 _walkDown 的 else 分支中使用了 matchLength 变量，但没有定义它。需要添加计算匹配长度的代码
//构造函数中不能直接调用build()
}
// 测试1: 例子
console.log("=== 测试1: abc ===");
let tree1 = new SuffixTree("abc");
tree1.debugStepByStep();
// 测试2: 例子
console.log("\n\n=== 测试2: banana ===");
let tree2 = new SuffixTree("banana");
tree2.debugStepByStep();
// 测试3: 例子
console.log("\n\n=== 测试3:bananasanaus===");
let tree3 = new SuffixTree("bananasanaus");
tree2.debugStepByStep();
//---优化---//
console.log("=== 诊断步骤7 ===");
let tree = new SuffixTree("bananasanaus");
// 只执行到步骤7
for (let i = 0; i <= 7; i++) {
    console.log(`\n步骤 ${i}: 插入后缀 "${tree.text.substring(i)}"`);
    tree._addSuffix(i);
    if (i === 6) {
        console.log("步骤6后的树状态:");
        tree._printSimple();
    }
}
// 测试3: 空字符串
console.log("\n\n=== 测试3: 空字符串 ===");
let tree4 = new SuffixTree("");
tree3.debugStepByStep();
```
```
//--------优化-调试版本15----------//
class SuffixTreeNode {
    constructor() {
        this.children = {};
        this.start = -1;
        this.end = -1;
        this.suffixLink = null;
    }
}

class SuffixTree {
    constructor(text) {
        this.text = text;
        this.root = new SuffixTreeNode();
    }

    debugStepByStep() {
        const n = this.text.length;
        console.log(`=== 构建后缀树: "${this.text}" ===`);
        
        for (let i = 0; i < n; i++) {
            console.log(`\n🎯 步骤 ${i}: 插入后缀 "${this.text.substring(i)}"`);
            console.log("插入前:");
            this._printSimple();
            
            this._addSuffix(i);
            
            console.log("插入后:");
            this._printSimple();
            console.log("-------------------");
        }
    }

    _printSimple(node = this.root, indent = 0) {
        let space = "  ".repeat(indent);
        
        if (node === this.root) {
            console.log(space + "根");
        } else {
            let edgeText = this.text.substring(node.start, node.end + 1);
            let type = Object.keys(node.children).length === 0 ? "叶" : "内";
            console.log(space + `[${edgeText}] (${type}, start=${node.start})`);
        }
        
        for (let [char, child] of Object.entries(node.children)) {
            this._printSimple(child, indent + 1);
        }
    }

    _addSuffix(suffixIndex) {
        let currentNode = this.root;
        let currentChar = this.text[suffixIndex];
        
        if (!currentNode.children[currentChar]) {
            let leaf = new SuffixTreeNode();
            leaf.start = suffixIndex;
            leaf.end = this.text.length - 1;
            currentNode.children[currentChar] = leaf;
        } else {
            this._walkDown(suffixIndex, currentNode.children[currentChar]);
        }
    }

    _walkDown(suffixIndex, node) {
        let current = suffixIndex;
        let edgePos = node.start;
        
        // 直接比较字符
        while (current < this.text.length && edgePos <= node.end) {
            if (this.text[current] !== this.text[edgePos]) {
                break;
            }
            current++;
            edgePos++;
        }
        
        let matchLength = current - suffixIndex;
        let edgeLength = node.end - node.start + 1;
        
        if (matchLength === edgeLength) {
            // 完全匹配当前边
            if (current < this.text.length) {
                let nextChar = this.text[current];
                if (node.children[nextChar]) {
                    this._walkDown(current, node.children[nextChar]);
                } else {
                    let leaf = new SuffixTreeNode();
                    leaf.start = current;
                    leaf.end = this.text.length - 1;
                    node.children[nextChar] = leaf;
                }
            }
        } else if (matchLength > 0) {
            // 部分匹配，分裂节点
            this._splitNode(node, suffixIndex, matchLength);
        }
    }

    _splitNode(node, suffixIndex, matchLength) {
        let internalNode = new SuffixTreeNode();
        internalNode.start = node.start;
        internalNode.end = node.start + matchLength - 1;
        
        node.start = node.start + matchLength;
        
        let newLeaf = new SuffixTreeNode();
        newLeaf.start = suffixIndex + matchLength;
        newLeaf.end = this.text.length - 1;
        
        let parent = this._findParent(node);
        let firstChar = this.text[internalNode.start];
        if (parent) {
            parent.children[firstChar] = internalNode;
        }
        
        internalNode.children[this.text[node.start]] = node;
        internalNode.children[this.text[newLeaf.start]] = newLeaf;
    }

    _findParent(node) {
        let queue = [this.root];
        while (queue.length > 0) {
            let current = queue.shift();
            for (let child of Object.values(current.children)) {
                if (child === node) {
                    return current;
                }
                queue.push(child);
            }
        }
        return null;
    }
}

// 测试
console.log("=== 测试 ===");
let tree = new SuffixTree("bananasanaus");
tree.debugStepByStep();
/*🐢树形结构基本正确 - 分裂的层级关系是对的
  🐢匹配逻辑正确 - 字符比较和分裂点的选择是对的
  🐢路径压缩有效 - 空间优化机制在工作
  🐢搜索框架正确 - 查询的基本流程是对的
*/
```
```
//-------调试版本16-------//
class SuffixTreeNode {
    constructor() {
        this.children = {};
        this.start = -1;//🔥永远代表原始后缀身份
        this.end = -1;//
        this.edgeStart = -1;  // 🔥新增：边标签起始位置
        this.edgeEnd = -1;    // 🔥新增：边标签结束位置
        //this.suffixId = -1;//🔧原始后缀身份标识（仅叶子需要）
/*节点P (父节点)
  |
    children: {
        根
    ├── [bananasanaus] (叶, start=0,end=11)  ← 后缀0
    ├── a (内, start=1,end=1)← ← 边标签:"a"
    │   ├── [na] (叶, start=2,end=3)← ← 边标签:"na" 
    │         └── [sanaus](叶, start=3,end=11)  ← 后缀3 ←边标签: "sanaus"：这是从父节点到子节点的路径标签
    │         └── [nasanaus](叶, start=1,end=11) ← 后缀1
    │         └── [us](叶,start=7,end=11)  ← 后缀7
    |   └── [us](叶,start=9,end=11)  ← 后缀9
    |   └── [sanaus](叶, start=5,end=11)←后缀5
    ├── na (内, start=4,end=5)← 内部节点
    │   └── [sanaus] (叶, start=4,end=11) ← 后缀4
    │   └── [us] (叶, start=8,end=11)    ← 后缀8
    │   └── [nasanaus] (叶, start=2,end=11)← 后缀2
    ├── s (内, start=6,end=6)← 内部节点
    │   └── [s] (叶, start=11,end=11) ← 后缀11
    │   └── [anaus] (叶, start=6,end=11) ← 后缀6 
    ├── [us] (叶, start=10,end=11)    ← 后缀10
  }
🎯边：总是通过父节点的children[key]隐式定义
🔗边被"溶解"在了父子关系中；边的标签被"拆分"存储：首字符在父节点的children键中，完整内容在子节点的(start, end)中；没有独立的边对象让你直接操作
🔗不仅是结构连接的桥梁，更是智能文本载体： 通过索引存储实现空间优化；通过可变长度支持快速匹配；通过方向导航维护结构清晰
🔗节点A (子节点)
  start: 0, end: 6 // 计算得边标签="banana$"
🎉🔥start和end就像身份证一样，每个节点都有唯一的文本区间
    内部节点的 start/end：标识这条边在原文中的位置
    叶子节点的 start/end：标识这个后缀在原文中的位置
    整个路径的拼接：重构出完整后缀  
🎉🔥唯一性约束：
    所有叶子节点的start必须唯一（0到n-1）
    内部节点的start可以与其他节点重复
🎯边标签 (Edge Label)：边上显示的文本片段，描述从父节点到子节点的路径上的字符串，可能只是完整后缀的一部分
🎯后缀标识 (Suffix Identifier)：叶子节点代表的完整后缀的起始位置，唯一标识这个叶子对应哪个后缀，总是指向完整后缀的开始位置：[sanaus] (start=6, end=11) ← 后缀标识: 6（代表后缀6:"sanaus"）
🔗关键区别：边标签 = 路径上的路标（指引方向）后缀标识 = 目的地的地址（最终位置）
范围不同：边标签：可以是任意长度的子串（"a", "na", "san"等），后缀标识：总是标识完整的后缀（从start到文本末尾）
用途不同：边标签：用于导航和匹配（搜索时比较字符），后缀标识：用于结果定位（找到后知道是哪个后缀）
唯一性不同：边标签：可以重复（多个边可以有相同标签）后缀标识：必须唯一（每个后缀有唯一起始位置）
*/
        this.suffixLink = null;
    }

/*-------⚠️注意---------/
🔧节点数据损坏: start=1, end=-1：后缀0、1、2 创建时正常，但从后缀3开始，找到的节点就是损坏的 (start=1, end=-1)
//创建叶子节点时，end 值没有被正确设置，确保：_addSuffix(suffixIndex)， leaf.end = this.text.length - 1;
🔧只有 'u' 和 'b' 开头的节点正常，其他都被改成了 start=-1：步骤 0: 插入后缀 "bananasanaus" debugger eval目标节点数据: start=0,end=11；但是步骤 1: 插入后缀 "ananasanaus"，目标节点数据: start=-1, end=11， 所有的后缀节点start都变成了-1开始
分裂逻辑普遍错误：不是个别节点的问题，内部节点转换逻辑错误：把所有节点都转成了 start=-1 的内部节点，只有没被分裂的节点幸存：'u' 和 'b' 节点没有被分裂过
//在分裂时过早地把节点标记为内部节点（设置 start=-1）身份信息要在整个计算过程中保持可用，直到不再需要为止。
🔧Uncaught ReferenceError: can't access lexical declaration 'remainingNode' before initialization：remainingNode 在初始化之前被访问
    let remainingNode = new SuffixTreeNode();  // 🚨声明了，但还没赋值完成
    node.children = {
        [this.text[remainingNode.edgeStart]]: remainingNode,  //🚨这里！
                ↑                          ↑
        访问属性edgeStart           访问变量remainingNode
        但remainingNode还在初始化过程中！
    JavaScript 的执行顺序
        声明阶段：let remainingNode（变量存在，但值为undefined）
        执行阶段：
            开始计算 this.text[remainingNode.edgeStart]
            但 remainingNode 还是 undefined，访问 undefined.edgeStart 就报错
            然后才执行 remainingNode = new SuffixTreeNode()
};
🔧在步骤0（第一次插入）时，根节点的children就已经有5个节点了：在第一次调用 _addSuffix 之前，节点已经被创建了
1.肯定是在构造函数或测试代码的某个地方提前创建了这些节点
2.部分匹配，需要分裂 debugger eval code:307:17
3.警告: 正在修改根节点的 'a' 节点! debugger eval code:331:17当前: start=1, 正在改为: -1：就是在分裂过程中，根节点的 'a' 节点被错误地修改了！
在 _splitNode 中，我们正在把根节点下的 'a' 节点（代表后缀1）转变成内部节点，设置 start=-1。但这是错误的！根节点下的直接子节点不应该变成内部节点！
🔥在正常的后缀树中，根节点的直接子节点确实可以变成内部节点：问题可能在于：原节点的身份没有正确保存和传递。
*/
}
class SuffixTree {
    constructor(text) {
        this.text = text;
        this.root = new SuffixTreeNode();
        console.log("🚨 构造函数完成时根节点children:", Object.keys(this.root.children));
    }
build() {
    const n = this.text.length;
    for (let i = 0; i < n; i++) {
        console.log(` 插入后缀 ${i}: "${this.text.substring(i)}"`);
        this._addSuffix(i);
    }
}
/*
🎯build()方法：
分离「构造」与「查询」： 没有build()的糟糕设计：每次查询都要重新建树！
有 build() 的良好设计：一次性构建，直接查询，无需重新构建
🔗预处理思想：后缀树的核心价值就是：一次构建（可能较慢）多次查询（非常快速）
🔗清晰的生命周期：初始化 →  构建   → 查询/使用
                ↓        ↓         ↓
              new()    build()   search()
🔗设计模式的体现：典型的Builder模式：构造过程复杂 → 封装在build()中，使用接口简单 → 暴露简单的 search()
*/
    debugStepByStep() {
        const n = this.text.length;
        console.log(`=== 构建后缀树: "${this.text}" ===`);
        for (let i = 0; i < n; i++) {
            console.log(`\n 步骤 ${i}: 插入后缀 "${this.text.substring(i)}"`);
            console.log("插入前:");
            this._printSimple();
            this._addSuffix(i);
            console.log("插入后:");
            this._printSimple();
            console.log("-------------------");
        }
    }
    _printSimple(node = this.root, indent = 0) {
    let space = "  ".repeat(indent);
    if (node === this.root) {
        console.log(space + "根");
    } else {
        let edgeText = this.text.substring(node.start, node.end + 1);
        let type = Object.keys(node.children).length === 0 ? "叶" : "内";
        // 显示start和end，如果是叶子还显示对应的后缀
        let suffixInfo = "";
        if (type === "叶") {
            let actualSuffix = this.text.substring(node.start);
            suffixInfo = ` → 后缀${node.start}:"${actualSuffix}"`;
        }
        console.log(space + `[${edgeText}] (${type}, start=${node.start}, end=${node.end})${suffixInfo}`);
    }
    
    // 按字符排序子节点以便阅读
    let sortedChildren = Object.entries(node.children)
        .sort(([a], [b]) => a.localeCompare(b));
    for (let [char, child] of sortedChildren) {
        this._printSimple(child, indent + 1);
    }
}
_addSuffix(suffixIndex) {
    //🔥朴素后缀树构建算法的核心：将文本中从位置suffixIndex开始的后缀插入到后缀树中//后缀树的构建引擎，它负责把每个后缀正确地加入到树结构中，并在需要时进行节点分裂来共享公共前缀
    //对于文本 "bananasanaus"：_addSuffix(0) → 插入后缀 "bananasanaus"，_addSuffix(1) → 插入后缀 "ananasanaus"
    //🎯每个后缀独立插入：这是朴素算法的特点；🎯从根节点开始：每次插入都从根节点重新开始；
    //🎯按首字符分组：相同首字符的后缀会在同一个分支下可能触发分裂🎯当新后缀与现有边部分匹配时，会调用 _walkDown 和 _splitNode
    console.log(`\n🔹 插入后缀 ${suffixIndex}: "${this.text.substring(suffixIndex)}"`);
    // 1. 从根节点开始
    let currentNode = this.root;
    // 2. 获取后缀的首字符
    let currentChar = this.text[suffixIndex]; 
    console.log(`   根节点的children:`, Object.keys(currentNode.children)); 
    // 3. 检查根节点是否有以这个字符开头的子节点
    if (!currentNode.children[currentChar]) {
        console.log(`   创建新叶子，字符: ${currentChar}`);
        // 3.1 如果没有：直接创建新叶子
        let leaf = new SuffixTreeNode();
        leaf.start = suffixIndex;
        leaf.end = this.text.length - 1;  //🚨必须设置！
        leaf.uniqueId = Math.random();  // 🎯 添加唯一标识
        console.log(`   创建新节点:`, leaf);
        console.log(`    节点内存地址:`, leaf.uniqueId);
        leaf.edgeStart = suffixIndex;
        leaf.edgeEnd = this.text.length - 1;
        currentNode.children[currentChar] = leaf;
    } else {// 3.2 如果有：沿着匹配的边继续深入
        console.log(`   找到匹配边，字符: ${currentChar}`);
        let targetNode = currentNode.children[currentChar];
        console.log(`   🎯 找到现有节点:`, targetNode);
        console.log(`   🎯 节点内存地址:`, targetNode.uniqueId);
        console.log(`   🎯 目标节点数据: start=${targetNode.start}, end=${targetNode.end}`);//🚨检查找到的节点
        this._walkDown(suffixIndex, currentNode.children[currentChar]);
    }
}
_walkDown(suffixIndex, node) {//suffixIndex: 正在插入的后缀的起始位置，node: 当前要匹配的节点（边）
    //🔥沿着树的边逐字符比较，找到新后缀的插入位置：后缀树匹配和分裂的核心逻辑
    // 🚨先检查节点数据是否有效
    if (node.start > node.end) {
        console.error(`❌ 节点数据损坏: start=${node.start}, end=${node.end}`);
        return;
    }
    let current = suffixIndex;//🎯新后缀的光标
    let edgePos = node.start;// 🎯当前边的光标
/*
🔥current跟踪新后缀当前比较到了哪个位置：current 就是新后缀的进度指示器，告诉我们已经匹配了多少，还剩下多少要处理
🎯current的完整生命周期：初始：current = suffixIndex（新后缀开始位置）比较中：current+（逐个字符前进）结束后：current 指向新后缀剩余部分的开始位置
新后缀: a n a s a n a u s
         ↑
       current=3 (开始)
        比较过程:
        a n a s a n a u s
      ✅✅✅ ❌
        ↑ ↑ ↑ ↑
        3 4 5 6 ← current 的位置变化
结束:
a n a s a n a u s
        ↑
      current=6 (剩余部分"sanaus"的开始)
🔥edgePos的作用：这个变量是当前边的"光标"，它与current配对工作
//在分裂时的关键作用：分裂时需要知道在边的哪个位置分裂，edgePos最终值告诉我们在边的哪个位置分裂：重复计算：node.start + matchLength重新计算了edgePos 的值，精度损失：如果计算有舍入误差，可能不一致，语义不清晰：edgePos 直接表示"边的匹配结束位置"，更直观
文本: "bananasanaus"
新后缀: "anasanaus" (从位置3开始)
当前边: "ananasanaus" (从位置1开始)
_walkDown(3, node) {
    let current = 3; 🎯新后缀光标：从位置3开始
    let edgePos = 1; 🎯当前边光标：从位置1开始//如果没有edgePos，我们无法知道当前边比较到了哪里，特别是在边很长的情况下：
    第1轮比较:
    text[current=3]='a' vs text[edgePos=1]='a'✅
    current = 4, edgePos = 2  // 两个光标都前进
    第2轮比较:  
    text[current=4]='n' vs text[edgePos=2]='n'✅
    current = 5, edgePos = 3  // 两个光标都前进
    第3轮比较:
    text[current=5]='a' vs text[edgePos=3]='a'✅  
    current = 6, edgePos = 4  // 两个光标都前进
    第4轮比较:
    text[current=6]='s' vs text[edgePos=4]='n' ❌
    跳出循环
}
*/
    console.log(`   _walkDown: 后缀${suffixIndex}="${this.text.substring(suffixIndex)}", 边="${this.text.substring(node.start, node.end + 1)}"`);
    // 🎯完整的字符比较逻辑
    //第1步：字符比较：逐个字符比较新后缀和当前边的标签
    //字符比较是后缀树的核心精髓！它解决了后缀树最关键的问题：如何发现和利用重复模式。1. 发现共享前缀2. 支持高效搜索3. 构建压缩树结构：字符比较让后缀树从朴素Trie变成压缩Trie
    //空间效率：共享前缀只存储一次，时间效率：搜索时快速定位，结构清晰：自然形成层次结构
    //字符比较不是可选的，而是后缀树存在的理由！它让后缀树从O(n²)的朴素结构变成了O(n)的压缩结构🎯
    while (current < this.text.length && edgePos <= node.end) {
        if (this.text[current] !== this.text[edgePos]) {
            console.log(`    不匹配: 位置${current}('${this.text[current]}') ≠ 位置${edgePos}('${this.text[edgePos]}')`);
            break;
        }
        console.log(`    匹配: 位置${current}('${this.text[current]}') = 位置${edgePos}('${this.text[edgePos]}')`);
        current++;
        edgePos++;
    }
    //第2步：计算匹配结果
    //决策的关键！它计算了两个重要长度，用来决定接下来该做什么
    let matchLength = current - suffixIndex;//matchLength - 已匹配的长度
    let edgeLength = node.end - node.start + 1;//edgeLength - 当前边的总长度
    console.log(`  匹配结果: matchLength=${matchLength}, edgeLength=${edgeLength}`);
/*
🔥当前边 = 从父节点到当前节点的路径上的文本标签
插入后缀3: "anasanaus"
假设当前有边: "ananasanaus" (start=1, end=11)
_walkDown(3, node) {
    node.start=1, node.end=11
    当前边 = text[1..11] = "ananasanaus"
    比较:
    新后缀: a n a s a n a u s  (从位置3开始)
    当前边: a n a n a s a n a u s  (从位置1开始)//当前边就是从父节点到当前节点的路径上显示的那个文本标签
         ✅✅✅ ❌
        current = 6   匹配结束位置（不匹配发生在位置6）
        suffixIndex = 3
        matchLength = 6 - 3 = 3  匹配了3个字符"ana"
        node.start=1, node.end=11  
        edgeLength = 11 - 1 + 1 = 11当前边总长度11个字符
        决策: 3 < 11 → 部分匹配，需要分裂
}
🔥当前节点：node（树中已存在的节点，我们正在与它比较），比较过程：把新后缀与当前节点的边标签逐个字符比较，新的后缀：text[suffixIndex..]（我们正在尝试插入的内容）
*/
    //第3步：三种情况处理
    if (matchLength === edgeLength) {
        // 情况1: 完全匹配当前边，继续向下
/*
🔥完全匹配 = 新后缀与当前边的标签完全匹配，但新后缀还有剩余字符：
在 "anana" 匹配 "ana" 的情况下：current =3开始：比较结束后:current = 6，this.text.length = 6，if (current < this.text.length) → 6 < 6 → false，所以不会进入 if 分支，直接结束
文本：banana：当前边: "ana" (node.start=3, end=5)  新后缀: "ana" (suffixIndex=3)//部分匹配，不是完全匹配
🔥"完全匹配"有两种情况：
情况1：真正完全匹配（结束）：
当前边: "ana"
新后缀: "ana"
结果: 完全匹配，没有剩余，结束
情况2：前缀匹配（继续向下）：
当前边: "ana" (内部节点)
新后缀: "anana" 
结果: 完全匹配当前边，但还有剩余"na"，继续向下
🎯"完全匹配+继续向下"只发生在：🎯当前节点是内部节点（有子节点），🎯新后缀比当前边长（有剩余字符）
叶子节点的情况（无法继续向下）：
[anana] (叶子)
↑
完全匹配，结束！
内部节点的情况（可以继续向下）：结构要求：只有内部节点才有子节点可以"继续向下"，逻辑要求：如果当前节点是叶子，完全匹配就意味着后缀已存在，应该结束
[ana] (内部节点)//算法要求：后缀树的压缩特性要求共享前缀必须是内部节点//天然地要求当前节点必须是内部节点
├── [na] (叶子)
└── [s]  (叶子)
↑
完全匹配"ana"，继续在子节点中匹配剩余"na"
 */
        console.log(`完全匹配，继续向下`);
        if (current < this.text.length) {
            let nextChar = this.text[current];
            if (node.children[nextChar]) {
                this._walkDown(current, node.children[nextChar]);
            } else {
                console.log(` 添加新叶子，字符: ${nextChar}`);
                let leaf = new SuffixTreeNode();
                leaf.start = current;
                leaf.end = this.text.length - 1;
                node.children[nextChar] = leaf;
            }
        }
    } 
    else if (matchLength > 0) {
        // 情况2: 部分匹配，需要分裂
        console.log(`部分匹配，需要分裂`);
        this._splitNode(node, suffixIndex, matchLength);
    } else {
        // 情况3: 首字符匹配但matchLength=0（不应该发生）
        console.error(`    错误: 首字符匹配但matchLength=0`);
        console.error(`     后缀: "${this.text.substring(suffixIndex)}"`);
        console.error(`     边: "${this.text.substring(node.start, node.end + 1)}"`);
    }
}

debugSplit(node, suffixIndex, matchLength) {
    console.log(`🔧 分裂调试:`);
    console.log(`   插入后缀: "${this.text.substring(suffixIndex)}" (start=${suffixIndex})`);
    console.log(`   匹配节点: "${this.text.substring(node.start, node.end + 1)}" (start=${node.start}, end=${node.end})`);
    console.log(`   匹配长度: ${matchLength}`);
    console.log(`   分裂位置: ${node.start + matchLength}`);
    
    // 检查分裂前的父节点
    let parentBefore = this._findParent(node);
    console.log(`   分裂前父节点:`, parentBefore ? this.text.substring(parentBefore.start, parentBefore.end + 1) : '无');
}
_splitNode(node, suffixIndex, matchLength) {
    // 🎯 确保这里有这行：
    let originalIdentity = node.start;  // 🚨 这行必须存在！
    // 🎯 删除这个干扰性检查！
    // 🎯 特别监控对根节点下 'a' 节点的修改
    /*if (node === this.root.children['a']) {
        console.error(`🚨 警告: 正在修改根节点的 'a' 节点!`);
        console.error(`   当前: start=${node.start}, 正在改为: -1`);
        console.trace();  // 打印调用栈
        }*/
    this.debugSplit(node, suffixIndex, matchLength);
    //node - 当前需要分裂的节点（匹配发生在这个节点上）/matchLength 就是共同前缀的长度，它决定了在哪里分裂节点
    //🔥suffixIndex -后缀的原始身份标识，正在插入的后缀的起始位置：这个值在整个插入过程中保持不变//suffixIndex就是后缀的身份证号码，永远不变
    console.log(` _splitNode: 分裂节点[${this.text.substring(node.start, node.end + 1)}], suffixIndex=${suffixIndex}, matchLength=${matchLength}`);
    /*node定义：
    // - 这是一个现有的节点，我们正在尝试将新后缀插入到它的路径下
    // - 它可能是叶子节点或内部节点
    // - 它的 start/end 定义了这条边的文本范围
    // - 新后缀与这个节点的边部分匹配（匹配了matchLength个字符）：
    比如文本: "bananasanaus"
    正在插入: "anasanaus" (suffixIndex=3)
    node: 代表 "ananasanaus" (start=1, end=11)
    matchLength: 3 (匹配了 "ana")*/


    /*1.创建内部节点
    let internalNode = new SuffixTreeNode();
    internalNode.start = -1;
    🚨内部节点无身份：内部节点不应该有具体的后缀身份，内部节点代表共享前缀，不属于任何一个具体的后缀，如果内部节点有身份，会造成语义混乱
    internalNode.edgeStart = node.edgeStart;     
    internalNode.edgeEnd = node.edgeStart + matchLength - 1;
    */
    //🎯matchLength当前插入的后缀与现有边已经匹配的字符数量的作用：确定内部节点的范围，确定原节点的调整，🟢确定新叶子的位置：新叶子代表我们正在插入的后缀的剩余部分
    //🎯但注意：新叶子的 start 是原始后缀位置，不是匹配后的位置！
    /* 
    🚨原节点保持原来的 start！但边的标签应该同时被改变!
    ⏹️node.start 保持不变！仍然是start=1:原节点如果不改变直接作为字节点的话，它的start确实保持了初始值，但是它的内容还是start标志的位置开始，内容没有变！
    原节点现在在内部节点下面，应该代表的是后缀的剩余部分
    ⏹️调整原节点的位置，但保持其标识
    ana (内, start=1, end=3)        ← 新建的内部节点
        └── [ananasanaus] (start=1, end=11)←🚨原节点保持不变！但这样边标签还是 "ananasanaus"，不对！
    原节点保持 start=1（身份不变），但显示为 "nasanaus"（内容改变）：这实际上是不可能的，因为在一个节点中，start 既表示身份又决定边标签
    🔧1.需要创建新节点，而不是修改原节点：⚠️根本矛盾：一个节点无法同时满足：start 值作为永恒的身份标识，start/end 准确描述边的文本内容
    🔧2.此时引入新的变量用来记录原始文本的start值，内容依旧加上长度计算防止矛盾，记录原始的start和内容改变分开⚠️但这样start可读性非常差   
    🔥3.完全放弃用start作为边标签，让start永远代表身份：让打印出来的 start 值就是初始的 start，让人能直观理解。用新的变量来表示内容的起始位置。
    🔧4.创建新的内部节点，创建新的叶子节点，创建新的剩余节点，直接丢弃原节点：⚠️原节点还存在于树中，如果丢弃会造成内存泄漏和结构混乱
    🔥5.重用原节点（实际做法）：我们不创建新的内部节点，而是直接把原节点改造成内部节点。
    */
    console.log(`🔧 分裂调试:`);
    console.log(`   插入后缀: "${this.text.substring(suffixIndex)}" (身份=${suffixIndex})`);
    console.log(`   匹配节点: "${this.text.substring(node.edgeStart, node.edgeEnd + 1)}" (身份=${node.start})`);
    console.log(`   匹配长度: ${matchLength}`);
    //1.🔥第一步：直接改造原节点为内部节点：保存原节点的信息（在修改前）
    let originalStart = node.start;// 保存原身份（后面要用）
    let originalEnd = node.end;// 保存原边标签结束
    let originalEdgeStart = node.edgeStart;  //保存原边标签起始
    let originalChildren = {...node.children};// 保存原子节点
    // 🚨不创建新的内部节点！直接改造原节点
    // 原节点现在变成共享前缀的内部节点
    /*🔥立即改造原节点：在分裂时过早地把节点标记为内部节点（设置 start=-1），
    /但这时候原节点可能还不是内部节点（可能还是叶子）设置start=-1 后，就丢失了原始身份信息；后续操作都基于这个错误的-1值
    解决方案：推迟身份清除：不要在分裂开始时就把 start 设为 -1，而是最后一步才设置 -1
    */
    // 🎯 第二步：创建两个新节点
    //2.1🔥创建代表原节点剩余部分的新节点（代表原节点的剩余部分）使用保存的原始值计算：总是使用保存的原始值来计算，避免依赖可能被修改的节点属性
    
    let remainingNode = new SuffixTreeNode();
    remainingNode.start = node.start;//1.🚨继承原身份
    //remainingNode.edgeStart = node.edgeStart + matchLength;//剩余节点内容的起始值 
    remainingNode.edgeStart = originalStart + matchLength;//2.需要原结束位置，originalStart时机安全：使用保存的原始值，不受后续修改影响，语义清晰：明确表示"基于原始起始位置计算"，避免混淆：不依赖可能被修改的 node.edgeStart
    remainingNode.edgeEnd = originalEnd;//3.直接使用保存的值 
    remainingNode.children = originalChildren;//🎯4.如果原内部节点有子节点，分裂后，这些子节点应该转移到剩余节点下面//继承原子节点
   

    //2.2🔥新叶子必须记录原始后缀位置，创建新叶子（代表正在插入的后缀）
    let newLeaf = new SuffixTreeNode();
    newLeaf.start = suffixIndex;//很重要🎯
    console.log(`   创建新叶子前: start=${newLeaf.start}`);
    newLeaf.edgeStart = suffixIndex + matchLength;
    newLeaf.edgeEnd = this.text.length - 1;
    console.log(`   创建新叶子后: start=${newLeaf.start}`);
    //newLeaf.end = this.text.length - 1;//叶子节点总是延伸到文本末尾文本："bananasanaus" (长度=12)

                                 
    
    //🎯先完全初始化节点，再使用它们🚀在对象字面量中使用变量前，确保该变量已经完全初始化！
    let remainingChar = this.text[remainingNode.edgeStart];  // ✅ 安全
    let newLeafChar = this.text[newLeaf.edgeStart];         // ✅ 安全
    //🎯添加身份传递检查
    console.log(`   🎯 身份传递: 原节点身份=${originalIdentity} → 剩余节点身份=${remainingNode.start}`);  
    //🎯第三步：最后才设置原节点为内部节点
    node.start = -1;//内部节点无身份🚨最后一步！//
    node.edgeStart = originalStart;                   // 边标签起始：1
    node.edgeEnd = originalStart + matchLength - 1;   // 边标签结束：3
    //node.children = {};// 先清空，稍后添加子节点 
    node.children = {
        [remainingChar]: remainingNode,
        [newLeafChar]: newLeaf
    }; 


    //🎯修正后的调试输出
    console.log(`   改造结果:`);
    console.log(`     - 原节点 → [${this.text.substring(node.edgeStart, node.edgeEnd + 1)}] (内部节点, start=${node.start})`);
    console.log(`     - 剩余节点 → [${this.text.substring(remainingNode.edgeStart, remainingNode.edgeEnd + 1)}] (身份=${remainingNode.start})`);
    console.log(`     - 新叶子 → [${this.text.substring(newLeaf.edgeStart, newLeaf.edgeEnd + 1)}] (身份=${newLeaf.start})`);
    console.log(`   子节点键: '${this.text[remainingNode.edgeStart]}' → 剩余节点, '${this.text[newLeaf.edgeStart]}' → 新叶子`);



    /*console.log(`   内部节点: [${this.text.substring(internalNode.start, internalNode.end + 1)}]`);
    console.log(`   原节点调整: [${this.text.substring(node.start, node.end + 1)}]`);
    console.log(`   新叶子: start=${newLeaf.start}, 代表 "${this.text.substring(newLeaf.start)}"`);*/
    //3.更新节点间的父子关系/重新连接节点关系
        /*
        之前：父节点
        └── node (原节点)
        之后：父节点
        └── internalNode (新建的内部节点)
            ├── node (调整后的原节点)
            └── newLeaf (新叶子)
        
    🔥：重用原节点的最大优势：不需要更新任何父节点引用
    如果直接改变原节点为内部节点就不需要重新维护指针关系，我们只是改变了原节点里面的状态：
    原节点对象没变：还是同一个内存对象//父节点的引用没变：父节点仍然指向同一个对象
           */
    /* 1. 找到原节点的父节点
    let parent = this._findParent(node);//可能 _findParent没有找到正确的父节点，导致节点关系混乱！
    // 2. 获取内部节点的首字符（用于在父节点的children中定位）
    let firstChar = this.text[internalNode.start];
    // 3. 将父节点指向原节点的链接改为指向新内部节点// 现在：parent → internalNode（而不是原来的 node）
    if (parent) {
        parent.children[firstChar] = internalNode;
    }
    // 4. 将原节点和新叶子作为内部节点的子节点
    internalNode.children[this.text[node.start]] = node;
    internalNode.children[this.text[newLeaf.start]] = newLeaf;*/

    console.log(`   重组完成`);
}

    _findParent(node) {
    //使用广度优先搜索 (BFS) 来寻找父节点
    console.log(`  寻找节点 [${this.text.substring(node.start, node.end + 1)}] 的父节点`);
    let queue = [this.root];//1.从根节点开始
    //🚨这里不是"根节点是队列"，而是创建一个队列，初始时包含根节点
    /*广度优先BFS 确保：先检查高层级节点（更可能是父节点），不会错过任何节点，找到的父节点是最近的：根 → 子节点A → 子节点B → 子节点C → 孙节点A1...
    深度优先 (DFS)：根 → 子节点A → 孙节点A1 → 曾孙节点A1a...
    */
    while (queue.length > 0) {
        let current = queue.shift();// 取出队列第一个节点//从队列的头部取出第一个元素，确保我们按"层级顺序"遍历树
        // 检查current的所有子节点
        for (let [char, child] of Object.entries(current.children)) {
            //Object.entries() 的作用：将对象转换为键值对数组；
            /*{'a': { start:1, end:3,children: {...} 
               'char':{child}
            },  子节点A*/
            console.log(`    检查: ${char} -> [${this.text.substring(child.start, child.end + 1)}]`);
            if (child === node) {// 找到目标节点的父节点
                console.log(` 找到父节点`);
                return current;
            }
            queue.push(child);// 将子节点加入队列继续搜索
        }
    }
    console.log(`  未找到父节点`);
    return null;
}
search(pattern) {
    //✅后缀树搜索:是否存在，所有出现位置，精确匹配（不是模糊匹配）
    //✅关键特性：找所有位置：不只是第一个出现的位置；精确子串：必须是连续字符序列；O(m)速度：搜索时间只与模式串长度有关，与文本大小无关
    //✅在后缀树中搜索模式串，会返回该模式串在文本中所有出现的起始位置列表"；不仅仅是"显示内容"，而是精确定位所有出现位置！
    let currentNode = this.root;
    let patternIndex = 0;
    //1.外层循环 - 控制模式串进度
    while (patternIndex < pattern.length) {//只要模式串还有字符没匹配完，就继续
        //2. 选择分支
        let currentChar = pattern[patternIndex];
        if (!currentNode.children[currentChar]) return [];//根据当前要匹配的字符，选择树上的对应分支。如果没有这个分支，说明模式串不存在"
        //3. 获取边上文本
        let child = currentNode.children[currentChar];
        let edgeText = this.text.substring(child.start, child.end + 1);
        //4. 内层循环 - 匹配边上字符
        for (let i = 0; i < edgeText.length && patternIndex < pattern.length; i++) {
            if (edgeText[i] !== pattern[patternIndex]) return [];//逐个字符比较边上文本与模式串的剩余部分。如果发现不匹配，立即返回失败
            patternIndex++;
        }
        currentNode = child;//5.移动到下一节点
    }
    
    return this._collectLeafIndices(currentNode);

/*-------⚠️注意--------
🔧在文本 "bananasanaus" 中："ana" 应该出现在位置1,3但结果出现了位置8，这说明在分裂操作或叶子节点收集时：某些叶子节点的start值设置错误，或者搜索时匹配过度，包含了不应该匹配的路径
🔧叶子节点标识错误 - start 值设置逻辑有系统性偏差🔧导致重复和缺失 - 但不影响树的结构正确性
🔗 新叶子节点应该代表"正在插入的完整后缀"：插入后缀8 "naus"
理解1：代表"匹配后的剩余部分"：后缀8:n a u s：❌错误方式：后缀8和后缀10都创建 start=10 的叶子
                                | | | |
                                匹配 剩余
                               "na" "us"
                        新叶子代表："us" → start=10
理解2：代表"正在插入的完整后缀"：✅正确方式：后缀8创建 start=8，后缀10创建 start=10
后缀8: "n a u s"
        ↑
        完整后缀开始位置
新叶子代表："naus" → start=8
🔗新叶子节点永远代表：当前正在插入的完整后缀；不是剩余部分，不是片段，而是完整的原始后缀！
🔗搜索"ana":
1. 根节点 → 找键'a' → 找到内部节点
2. 内部节点边标签="ana" → 匹配成功!
3. 继续在内部节点下处理剩余部分
搜索"an":
1. 根节点 → 找键'a' → 找到内部节点  
2. 内部节点边标签="ana" → 匹配前2个字符"an"
3. 部分匹配，需要分裂 
共享前缀 "ana" 的完整边标签就是 "ana"，在父节点的children中只用首字符 'a' 作为查找键，这是为了搜索效率，不是边被截断了 



*/}
}

_collectLeafIndices(node) {//递归收集所有叶子节点的起始位置：找到某个节点下的所有叶子节点，并收集它们的start值
    let results = [];
    if (Object.keys(node.children).length === 0) {//1. 基本情况 - 叶子节点
        results.push(node.start);
    } else {//2. 递归情况 - 内部节点：如果这个节点有子节点，就递归处理每个子节点，把结果合并
        for (let child of Object.values(node.children)) {
            results = results.concat(this._collectLeafIndices(child));
        }
    }
    return results;
}
// 添加调试方法
debugLeafStarts() {
    console.log("=== 检查所有叶子节点的start值 ===");
    this._debugLeafStarts(this.root);
}

_debugLeafStarts(node, path = "") {
    if (Object.keys(node.children).length === 0) {
        let suffix = this.text.substring(node.start);
        console.log(`叶子: 路径=${path}, start=${node.start}, 后缀="${suffix}"`);
    } else {
        for (let [char, child] of Object.entries(node.children)) {
            let edgeText = this.text.substring(child.start, child.end + 1);
            this._debugLeafStarts(child, path + " → [" + edgeText + "]");
        }
    }
}
// 检查是否所有后缀都有对应的叶子节点
checkAllSuffixes() {
    console.log("=== 检查所有后缀是否都有叶子节点 ===");
    const n = this.text.length;
    let missing = [];
    
    for (let i = 0; i < n; i++) {
        let found = false;
        // 遍历所有叶子节点，检查是否有start=i的
        let queue = [this.root];
        while (queue.length > 0) {
            let node = queue.shift();
            if (Object.keys(node.children).length === 0) {
                if (node.start === i) {
                    found = true;
                    break;
                }
            } else {
                for (let child of Object.values(node.children)) {
                    queue.push(child);
                }
            }
        }
        
        if (!found) {
            missing.push(i);
            console.log(`缺失: start=${i}, 后缀="${this.text.substring(i)}"`);
        }
    }
    
    if (missing.length === 0) {
        console.log(" 所有后缀都有对应的叶子节点");
    } else {
        console.log(`总计缺失 ${missing.length} 个后缀`);
    }
}

}

/*测试
console.log("=== 测试 ===");
let tree = new SuffixTree("bananasanaus");
tree.debugStepByStep();*/

// 测试搜索功能
function testSearch() {
    let tree = new SuffixTree("bananasanaus");
    
    // 构建树
    for (let i = 0; i < tree.text.length; i++) {
        tree._addSuffix(i);
    }
    console.log("=== 搜索测试 ===");
    // 基本测试
    console.log("'ana' 位置:", tree.search("ana"));    // 应该返回 [1, 3]
    console.log("'na' 位置:", tree.search("na"));      // 应该返回 [2, 4]  
    console.log("'us' 位置:", tree.search("us"));      // 应该返回 [10]
    console.log("'ban' 位置:", tree.search("ban"));    // 应该返回 [0]
    // 边界测试
    console.log("'xyz' 位置:", tree.search("xyz"));    // 应该返回 []
    console.log("'' 位置:", tree.search(""));          // 应该返回所有位置
    // 单个字符
    console.log("'a' 位置:", tree.search("a"));        // 应该返回 [1, 3, 7, 9]
    console.log("'n' 位置:", tree.search("n"));        // 应该返回 [2, 4, 8]
}

testSearch();

let tree = new SuffixTree("bananasanaus");
for (let i = 0; i < tree.text.length; i++) {
    tree._addSuffix(i);
}

tree.debugLeafStarts();

console.log("=== 详细构建过程 ===");
let tree2 = new SuffixTree("bananasanaus");
for (let i = 0; i < tree.text.length; i++) {
    console.log(`\n 步骤 ${i}: 插入后缀 "${tree2.text.substring(i)}"`);
    tree._addSuffix(i);
    // 每步后检查叶子节点
    if (i < 5) { // 只看前几步，避免输出太多
        console.log("当前叶子节点:");
        tree._debugLeafStarts(tree2.root);
    }
}
let tree3 = new SuffixTree("bananasanaus");
for (let i = 0; i < tree3.text.length; i++) {
    tree._addSuffix(i);
}
tree.checkAllSuffixes();
tree.debugLeafStarts();

// 测试代码
let tree4 = new SuffixTree("bananasanaus");
console.log("创建树后根节点children:", Object.keys(tree.root.children));  //🎯这里检查
// 如果这里就已经有节点，说明构造函数有问题
// 如果这里是空的，但 debugStepByStep 开始时就有节点，说明 debugStepByStep 内部有问题
tree4.debugStepByStep();
```
```
//-------调试版本17------//
class SuffixTreeNode {
    constructor() {
        this.children = {};
       
        this.root.start = -1;
        this.root.end = -1;
        this.root.edgeStart = 0;      // 🎯 立即设置！
        this.root.edgeEnd = 0;        // 🎯 立即设置！
        //🎯每次创建 new SuffixTreeNode() 后，必须立即设置 start, end, edgeStart, edgeEnd 四个值！

/*      this.start = -1;//🔥永远代表原始后缀身份
        this.end = -1;//
        this.edgeStart = -1;  // 🔥新增：边标签起始位置
        this.edgeEnd = -1;    // 🔥新增：边标签结束位置
*/
/*💥💥💥💥
创建新节点: 
Object { children: {}, start: 1, end: 11, edgeStart: -1, edgeEnd: -1, ... }
1.不要在构造函数中设置默认的-1，让调用者明确设置所有值：
2.创建后立即设置边界，在你的所有节点创建处，确保创建后立即设置所有四个边界：
can't access property "start", this.root is undefined:这个错误说明根节点this.root 没有正确初始化！
*/


        //this.suffixId = -1;//🔧原始后缀身份标识（仅叶子需要）
/*节点P (父节点)
  |
    children: {
        根
    ├── [bananasanaus] (叶, start=0,end=11)  ← 后缀0
    ├── a (内, start=1,end=1)← ← 边标签:"a"
    │   ├── [na] (叶, start=2,end=3)← ← 边标签:"na" 
    │         └── [sanaus](叶, start=3,end=11)  ← 后缀3 ←边标签: "sanaus"：这是从父节点到子节点的路径标签
    │         └── [nasanaus](叶, start=1,end=11) ← 后缀1
    │         └── [us](叶,start=7,end=11)  ← 后缀7
    |   └── [us](叶,start=9,end=11)  ← 后缀9
    |   └── [sanaus](叶, start=5,end=11)←后缀5
    ├── na (内, start=4,end=5)← 内部节点
    │   └── [sanaus] (叶, start=4,end=11) ← 后缀4
    │   └── [us] (叶, start=8,end=11)    ← 后缀8
    │   └── [nasanaus] (叶, start=2,end=11)← 后缀2
    ├── s (内, start=6,end=6)← 内部节点
    │   └── [s] (叶, start=11,end=11) ← 后缀11
    │   └── [anaus] (叶, start=6,end=11) ← 后缀6 
    ├── [us] (叶, start=10,end=11)    ← 后缀10
  }
🎯边：总是通过父节点的children[key]隐式定义
🔗边被"溶解"在了父子关系中；边的标签被"拆分"存储：首字符在父节点的children键中，完整内容在子节点的(start, end)中；没有独立的边对象让你直接操作
🔗不仅是结构连接的桥梁，更是智能文本载体： 通过索引存储实现空间优化；通过可变长度支持快速匹配；通过方向导航维护结构清晰
🔗节点A (子节点)
  start: 0, end: 6 // 计算得边标签="banana$"
🎉🔥start和end就像身份证一样，每个节点都有唯一的文本区间
    内部节点的 start/end：标识这条边在原文中的位置
    叶子节点的 start/end：标识这个后缀在原文中的位置
    整个路径的拼接：重构出完整后缀  
🎉🔥唯一性约束：
    所有叶子节点的start必须唯一（0到n-1）
    内部节点的start可以与其他节点重复
🎯边标签 (Edge Label)：边上显示的文本片段，描述从父节点到子节点的路径上的字符串，可能只是完整后缀的一部分
🎯后缀标识 (Suffix Identifier)：叶子节点代表的完整后缀的起始位置，唯一标识这个叶子对应哪个后缀，总是指向完整后缀的开始位置：[sanaus] (start=6, end=11) ← 后缀标识: 6（代表后缀6:"sanaus"）
🔗关键区别：边标签 = 路径上的路标（指引方向）后缀标识 = 目的地的地址（最终位置）
范围不同：边标签：可以是任意长度的子串（"a", "na", "san"等），后缀标识：总是标识完整的后缀（从start到文本末尾）
用途不同：边标签：用于导航和匹配（搜索时比较字符），后缀标识：用于结果定位（找到后知道是哪个后缀）
唯一性不同：边标签：可以重复（多个边可以有相同标签）后缀标识：必须唯一（每个后缀有唯一起始位置）
*/
        this.suffixLink = null;
    }

/*-------⚠️注意---------/
🔧节点数据损坏: start=1, end=-1：后缀0、1、2 创建时正常，但从后缀3开始，找到的节点就是损坏的 (start=1, end=-1)
//创建叶子节点时，end 值没有被正确设置，确保：_addSuffix(suffixIndex)， leaf.end = this.text.length - 1;
🔧只有 'u' 和 'b' 开头的节点正常，其他都被改成了 start=-1：步骤 0: 插入后缀 "bananasanaus" debugger eval目标节点数据: start=0,end=11；但是步骤 1: 插入后缀 "ananasanaus"，目标节点数据: start=-1, end=11， 所有的后缀节点start都变成了-1开始
分裂逻辑普遍错误：不是个别节点的问题，内部节点转换逻辑错误：把所有节点都转成了 start=-1 的内部节点，只有没被分裂的节点幸存：'u' 和 'b' 节点没有被分裂过
//在分裂时过早地把节点标记为内部节点（设置 start=-1）身份信息要在整个计算过程中保持可用，直到不再需要为止。
🔧Uncaught ReferenceError: can't access lexical declaration 'remainingNode' before initialization：remainingNode 在初始化之前被访问
    let remainingNode = new SuffixTreeNode();  // 🚨声明了，但还没赋值完成
    node.children = {
        [this.text[remainingNode.edgeStart]]: remainingNode,  //🚨这里！
                ↑                          ↑
        访问属性edgeStart           访问变量remainingNode
        但remainingNode还在初始化过程中！
    JavaScript 的执行顺序
        声明阶段：let remainingNode（变量存在，但值为undefined）
        执行阶段：
            开始计算 this.text[remainingNode.edgeStart]
            但 remainingNode 还是 undefined，访问 undefined.edgeStart 就报错
            然后才执行 remainingNode = new SuffixTreeNode()
};
🔧在步骤0（第一次插入）时，根节点的children就已经有5个节点了：在第一次调用 _addSuffix 之前，节点已经被创建了
1.肯定是在构造函数或测试代码的某个地方提前创建了这些节点
2.部分匹配，需要分裂 debugger eval code:307:17
3.警告: 正在修改根节点的 'a' 节点! debugger eval code:331:17当前: start=1, 正在改为: -1：就是在分裂过程中，根节点的 'a' 节点被错误地修改了！
在 _splitNode 中，我们正在把根节点下的 'a' 节点（代表后缀1）转变成内部节点，设置 start=-1。但这是错误的！根节点下的直接子节点不应该变成内部节点！
🔥在正常的后缀树中，根节点的直接子节点确实可以变成内部节点：问题可能在于：原节点的身份没有正确保存和传递。
🔧剩余节点和新叶子在创建时 end 值就是 -1，这说明问题在节点构造函数中：确保每个新创建的节点都完整设置所有字段
1.在创建节点时立即设置所有值：remainingNode.end = originalEnd; 必须设置！newLeaf.end = this.text.length - 1; 必须设置！
2.构造函数不设置默认值：不设置默认值，让调用者负责设置//this.start = undefined;//this.end = undefined;
class SuffixTreeNode {
    constructor() {
        this.children = {};
        // 不设置默认值，让调用者负责设置
        // this.start = undefined;
        // this.end = undefined;
        this.edgeStart = -1;
        this.edgeEnd = -1;
        this.suffixLink = null;
        this.uniqueId = Math.random();
    }
}
🔧分裂创建了正确的节点，但打印函数显示的是错误的内容！
🔧严重错误：在插入后缀5 "asanaus" 时：找到的节点身份已经是 =-1（内部节点），但匹配结果显示 matchLength=1（部分匹配），这说明内部节点也参与了匹配和分裂
🔧内部节点不应该参与字符匹配和分裂！内部节点只是结构节点，它的边标签是固定的，不应该与新的后缀进行字符比较。
🔥在 _walkDown 中，如果当前节点是内部节点（start=-1），应该：直接根据首字符选择子节点，不应该进行字符比较，不应该触发分裂：在walkdown中添加触发条件，
🔧没有把共享前缀 "a" 提取出来：分裂不够彻底，内部节点创建层级错误：应该在 'a' 处就创建内部节点，而不是在 'ana' 处
当插入后缀5 "asanaus" 时：找到 [ana] 内部节点查找子节点 'a'，但没有找到（只有 'n' 和 's'）直接添加了新叶子 [asanaus]
在内部节点路由时，我们没有进行字符比较，只是简单根据首字符路由。
🔧在内部节点路由时，如果找到匹配的子节点，应该继续比较剩余字符：关键修复：继续在子节点中进行字符比较；内部节点路由不能只看首字符，还需要检查是否与现有子节点共享更长的前缀！
🔧问题就是我们没有把 [na] 从 [ana] 中分离出来；我们创建了子节点 'a'，但没有重新组织现有的 'n' 和 's' ‘an’子节点！
🔁当创建新的 'a' 子节点时，我们应该：1.把[ana]节点拆分成[a]+[na]2.把原来的'n'和's'子节点移动到[na]下面，让[a]指向[na]和新的 [sanaus]
🔍子节点键 vs 节点内容：子节点键：是字符，用于在哈希表中查找（'a', 'n', 's'），节点内容：是 SuffixTreeNode 对象，包含实际的边标签
[ana] (内部节点)   +a                     //之后[ana] (内部节点)--->现在确实有 'a' 这个子节点键
  子节点键: {//之前                        子节点键: {
    'n': → [nasanaus] (叶子节点)            'a': → [sanaus] (新叶子, start=5)  ← 刚刚添加的
    's': → [sanaus] (叶子节点)              'n': → [nasanaus] (叶子节点) 
}                                          's': → [sanaus] (叶子节点)}
🔥正确的为后缀与内部节点的匹配设置不同的三种边界条件 
🔧Uncaught ReferenceError: can't access lexical declaration 'matchLength' before initialization ：必须先定义                                            
🔥🔥🔥路由、比较、分裂是三件不同的事情！
比较 (Comparison)：作用：逐个字符对比，找出共享前缀长度，比较：找出匹配了多少个字符，"asanaus" vs "ana" → 匹配了1个字符 'a'
分裂 (Splitting)：作用：根据比较结果重组节点结构//分裂：把[ana]拆成[a]+[na]，[ana] → [a] + [na]                                                                           
路由 (Routing)：作用：根据首字符快速导航到子节点//路由：根据首字符跳转，在 [a] 节点中，根据 's' 找到子节点 [sanaus]
正确顺序：比较 → [判断] → 分裂或路由   
1. 比较 "asanaus" vs "ana" → 匹配1个字符
2. 判断：1 < 3 → 部分匹配
3. 分裂：把 [ana] 拆成 [a] + [na]  
4. 路由：在新区结构中继续处理   
🔥🔥🔥 💥内部节点数据结构设计问题：
1.内部节点边标签不准确：内部节点 [ana] 实际上应该代表从根节点到该节点的路径标签
2.子节点键设计问题：子节点键应该是下一个字符，但你的比较逻辑没有正确执行
3.缺少字符比较：内部节点路由时直接看首字符，没有进行必要的字符比较来确定是否匹配
💥问题不是代码顺序，而是执行路径。内部节点路由分支可能有一个 return 语句，导致代码提前退出，没有执行后面的比较逻辑
❌_walkDown: 后缀5="asanaus", 边="ananasanaus" debugger eval code:252:13
   _walkDown 开始: 节点类型=叶子节点 
比较结果: matchLength=undefined, current=undefined 
插入后: debugger eval code:159:21
根 debugger eval code:167:17
  [ananasanaus] (叶, start=1, end=11) → 后缀1:"ananasanaus" 
  [bananasanaus] (叶, start=0, end=11) → 后缀0:"bananasanaus" 
  [nanasanaus] (叶, start=2, end=11) → 后缀2:"nanasanaus"
🔧比较方法返回 undefined，导致：matchLength和current都是undefined，所有决策逻辑都无法正常工作，算法退回到最简单的添加叶子节点模式
🔧比较方法返回 undefined：关键：在同一个作用域内不要用 let 重复声明同一个变量！
*/
}

class SuffixTree {
    constructor(text) {
        this.text = text;
        this.root = new SuffixTreeNode();
        console.log("🚨 构造函数完成时根节点children:", Object.keys(this.root.children));
    }}
build() {
    const n = this.text.length;
    for (let i = 0; i < n; i++) {
        console.log(` 插入后缀 ${i}: "${this.text.substring(i)}"`);
        this._addSuffix(i);
    }
}
/*
🎯build()方法：
分离「构造」与「查询」： 没有build()的糟糕设计：每次查询都要重新建树！
有 build() 的良好设计：一次性构建，直接查询，无需重新构建
🔗预处理思想：后缀树的核心价值就是：一次构建（可能较慢）多次查询（非常快速）
🔗清晰的生命周期：初始化 →  构建   → 查询/使用
                ↓        ↓         ↓
              new()    build()   search()
🔗设计模式的体现：典型的Builder模式：构造过程复杂 → 封装在build()中，使用接口简单 → 暴露简单的 search()
*/
    debugStepByStep() {
        const n = this.text.length;
        console.log(`=== 构建后缀树: "${this.text}" ===`);
        for (let i = 0; i < n; i++) {
            console.log(`\n 步骤 ${i}: 插入后缀 "${this.text.substring(i)}"`);
            console.log("插入前:");
            this._printSimple();
            this._addSuffix(i);
            console.log("插入后:");
            this._printSimple();
            console.log("-------------------");
        }
    }
    _printSimple(node = this.root, indent = 0) {
    let space = "  ".repeat(indent);
    if (node === this.root) {
        console.log(space + "根");
    } else {
         //🎯修复：内部节点用 edgeStart/edgeEnd，叶子节点用 start/end
        let edgeStart = node.start === -1 ? node.edgeStart : node.start;
        let edgeEnd = node.start === -1 ? node.edgeEnd : node.end;
        let edgeText = this.text.substring(edgeStart, edgeEnd + 1);
        let type = Object.keys(node.children).length === 0 ? "叶" : "内";
        // 显示start和end，如果是叶子还显示对应的后缀
        let suffixInfo = "";
        if (type === "叶") {
            let actualSuffix = this.text.substring(node.start);
            suffixInfo = ` → 后缀${node.start}:"${actualSuffix}"`;
        }
        console.log(space + `[${edgeText}] (${type}, start=${node.start}, end=${node.end})${suffixInfo}`);
    }
    
    // 按字符排序子节点以便阅读
    let sortedChildren = Object.entries(node.children)
        .sort(([a], [b]) => a.localeCompare(b));
    for (let [char, child] of sortedChildren) {
        this._printSimple(child, indent + 1);
    }
}
_addSuffix(suffixIndex) {
    //🔥朴素后缀树构建算法的核心：将文本中从位置suffixIndex开始的后缀插入到后缀树中//后缀树的构建引擎，它负责把每个后缀正确地加入到树结构中，并在需要时进行节点分裂来共享公共前缀
    //对于文本 "bananasanaus"：_addSuffix(0) → 插入后缀 "bananasanaus"，_addSuffix(1) → 插入后缀 "ananasanaus"
    //🎯每个后缀独立插入：这是朴素算法的特点；🎯从根节点开始：每次插入都从根节点重新开始；
    //🎯按首字符分组：相同首字符的后缀会在同一个分支下可能触发分裂🎯当新后缀与现有边部分匹配时，会调用 _walkDown 和 _splitNode
    console.log(`\n🔹 插入后缀 ${suffixIndex}: "${this.text.substring(suffixIndex)}"`);
    // 1. 从根节点开始
    let currentNode = this.root;
    // 2. 获取后缀的首字符
    let currentChar = this.text[suffixIndex]; 
    console.log(`   根节点的children:`, Object.keys(currentNode.children)); 
    // 3. 检查根节点是否有以这个字符开头的子节点
    if (!currentNode.children[currentChar]) {
        console.log(`   创建新叶子，字符: ${currentChar}`);
        // 3.1 如果没有：直接创建新叶子
        let leaf = new SuffixTreeNode();
        leaf.start = suffixIndex;
        leaf.end = this.text.length - 1;  //🚨必须设置！
        leaf.uniqueId = Math.random();  // 🎯 添加唯一标识
        console.log(`   创建新节点:`, leaf);
        console.log(`    节点内存地址:`, leaf.uniqueId);
        leaf.edgeStart = suffixIndex;
        leaf.edgeEnd = this.text.length - 1;
        currentNode.children[currentChar] = leaf;
        console.log(`    新节点内存地址:`, leaf.uniqueId);
    } else {// 3.2 如果有：沿着匹配的边继续深入
        
        let targetNode = currentNode.children[currentChar];
        console.log(`    找到现有节点:`, targetNode);
        console.log(`    现有节点内存地址:`, targetNode.uniqueId);
        console.log(`    现有节点数据:`, targetNode);
        this._walkDown(suffixIndex, currentNode.children[currentChar]);
    }
}
_compareSuffixWithEdge(suffixIndex, node) {
    console.log('🎯 _compareSuffixWithEdge 方法开始执行!');
    console.log('参数:', { suffixIndex, node });

    let current = suffixIndex;
    let edgePos = node.edgeStart;
    let matchLength = 0;

    console.log('变量初始化完成:', { current, edgePos, matchLength });
    
    // 🎯 情况1: 完全匹配整个边
    // 🎯 情况2: 部分匹配（匹配了前N个字符）  
    // 🎯 情况3: 完全不匹配（首字符就不匹配）
    console.log(` 比较: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
    while (current < this.text.length && edgePos <= node.edgeEnd) {
        console.log(`   位置${current}("${this.text[current]}") vs 位置${edgePos}("${this.text[edgePos]}")`);
        if (this.text[current] !== this.text[edgePos]) break;
        current++;
        edgePos++;
        matchLength++;
    }
    //第2步：计算匹配结果
    //决策的关键！它计算了两个重要长度，用来决定接下来该做什么
    //let matchLength = current - suffixIndex;//matchLength - 已匹配的长度
    let edgeLength = node.edgeEnd - node.edgeStart + 1;//✅使用edgeStart/edgeEnd//edgeLength-当前边的总长度
    console.log(`  匹配结果: matchLength=${matchLength}, edgeLength=${edgeLength}`);
    //第三步：现在添加三种情况的判断
    if (matchLength === edgeLength) {
        console.log(` 情况1: 完全匹配整个边`);
        if (current < this.text.length) {
            let nextChar = this.text[current];
            if (node.children[nextChar]) {
                this._walkDown(current, node.children[nextChar]);
            } else {
                console.log(` 添加新叶子，字符: ${nextChar}`);
                this._addLeaf(node, current);
            }}
    } else if (matchLength > 0) {
        console.log(` 情况2: 部分匹配 ${matchLength} 个字符`);
        this._splitNode(node, suffixIndex, matchLength);
    } else {
        console.log(` 情况3: 完全不匹配`);
        // 🎯 情况3: 完全不匹配 → 创建新分支（正常情况！）
        console.log(`创建新分支: ${this.text.substring(suffixIndex)}`);
        this._addNewBranch(node, suffixIndex);
    }
    console.log(`   比较完成: matchLength=${matchLength}, current=${current}`);
    return { current, matchLength, matchType: matchLength === edgeLength ? 'full' : matchLength > 0 ? 'partial' : 'none' };
    
    // 🎯 确保有这行！
    //return { current, matchLength };
    

}


_walkDown(suffixIndex, node) {//suffixIndex: 正在插入的后缀的起始位置，node: 当前要匹配的节点（边） 
    // 先声明变量
    //let current, matchLength, edgeLength;
    //🔥声明并初始化默认值
    let current = suffixIndex;
    let matchLength = 0;
    let edgeLength = 0;
    console.log('=== _walkDown 开始 ===');
    console.log('参数:', { suffixIndex, node });
    console.log('node.start:', node.start);

    //1.🚨先检查节点数据是否有效
    if (node.start > node.end) {
        console.error(`❌ 节点数据损坏: start=${node.start}, end=${node.end}`);
        return;
    } 
    console.log(`   _walkDown: 后缀${suffixIndex}="${this.text.substring(suffixIndex)}", 边="${this.text.substring(node.start, node.end + 1)}"`);
    console.log(`   _walkDown 开始: 节点类型=${node.start === -1 ? '内部节点' : '叶子节点'}`);
    /*2.🎯变量声明：
    let current = suffixIndex;//🎯新后缀的光标
    let edgePos = node.edgeStart;//✅使用 edgeStart//🎯当前边的光标
/*
🔥current跟踪新后缀当前比较到了哪个位置：current 就是新后缀的进度指示器，告诉我们已经匹配了多少，还剩下多少要处理
🎯current的完整生命周期：初始：current = suffixIndex（新后缀开始位置）比较中：current+（逐个字符前进）结束后：current 指向新后缀剩余部分的开始位置
新后缀: a n a s a n a u s
         ↑
       current=3 (开始)
        比较过程:
        a n a s a n a u s
      ✅✅✅ ❌
        ↑ ↑ ↑ ↑
        3 4 5 6 ← current 的位置变化
结束:
a n a s a n a u s
        ↑
      current=6 (剩余部分"sanaus"的开始)
🔥edgePos的作用：这个变量是当前边的"光标"，它与current配对工作
//在分裂时的关键作用：分裂时需要知道在边的哪个位置分裂，edgePos最终值告诉我们在边的哪个位置分裂：重复计算：node.start + matchLength重新计算了edgePos 的值，精度损失：如果计算有舍入误差，可能不一致，语义不清晰：edgePos 直接表示"边的匹配结束位置"，更直观
文本: "bananasanaus"
新后缀: "anasanaus" (从位置3开始)
当前边: "ananasanaus" (从位置1开始)
_walkDown(3, node) {
    let current = 3; 🎯新后缀光标：从位置3开始
    let edgePos = 1; 🎯当前边光标：从位置1开始//如果没有edgePos，我们无法知道当前边比较到了哪里，特别是在边很长的情况下：
    第1轮比较:
    text[current=3]='a' vs text[edgePos=1]='a'✅
    current = 4, edgePos = 2  // 两个光标都前进
    第2轮比较:  
    text[current=4]='n' vs text[edgePos=2]='n'✅
    current = 5, edgePos = 3  // 两个光标都前进
    第3轮比较:
    text[current=5]='a' vs text[edgePos=3]='a'✅  
    current = 6, edgePos = 4  // 两个光标都前进
    第4轮比较:
    text[current=6]='s' vs text[edgePos=4]='n' ❌
    跳出循环
}
*/
//3.🔁⚠️内部节点的路由逻辑
/*内部节点路由的三种情况：
正确的逻辑应该是:先检查新后缀与内部节点边标签的匹配情况,✅如果部分匹配 → 分裂内部节点,✅如果完全匹配 → 路由到子节点,✅如果完全不匹配 → 添加新叶子
应该把"字符匹配情况"作为判断条件*/
    if (node.start === -1) {//💥💥💥💥💥 处理内部节点的子节点查找和路由
        //🔥内部节点：重新赋值
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        console.log(`   内部节点: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
        
        console.log(' 准备调用 _compareSuffixWithEdge');
        
        // 先检查方法是否存在
        console.log('_compareSuffixWithEdge 方法类型:', typeof this._compareSuffixWithEdge);
        
        console.log('🎯 _compareSuffixWithEdge 返回结果:', result);
        
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        
        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);


        //let matchLength = this._compareSuffixWithEdge(suffixIndex, node);
        //显示当前内部节点的边标签
        console.log(`   内部节点: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`); 
        console.log(`   内部节点路由: 边="${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
        let nextChar = this.text[suffixIndex];// 使用原始位置的首字符
/*
💥nextChar 是下一个要用于路由的字符，它取决于当前匹配后的位置；在完全匹配当前边后，下一个用于选择子节点的字符，基于比较后的当前位置 current
文本: "bananasanaus"//nextChar 必须在字符比较之后，基于新的current位置计算
后缀5: "asanaus"
当前边: "ana" (内部节点边标签)
比较过程:
"asanaus" vs "ana"
   "a" = "a" → current=6
   "s" ≠ "n" → 停止比较
结果: 
matchLength=1, current=6
nextChar = this.text[6] = "s"
*/
        console.log(`   查找子节点: ${nextChar}`);
        console.log(`   可用子节点:`, Object.keys(node.children));
        // 🎯 调用封装的比较方法
        // 🎯 先比较字符！
        //let { current, matchLength } = this._compareSuffixWithEdge(suffixIndex, node);// 🚨 错误：重复声明
         /* ✅ 正确：赋值给已声明的变量
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);*/
        ({ current, matchLength } = this._compareSuffixWithEdge(suffixIndex, node));
        /*✅1.正确：解构但不声明（去掉 let）
💥关键：({ current, matchLength } = result) 这种语法表示"赋值给已存在的变量"，而不是声明新变量。这样既能在开头声明变量供后面使用，又能在内部节点中正确赋值！
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        let edgeLength = node.edgeEnd - node.edgeStart + 1;
        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);*/
        /*
        ES6的解构赋值语法：相当于：一个方法调用同时返回两个相关的计算结果：代码更清晰简洁
        // 先调用方法获取结果对象
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        // 然后从对象中提取属性
        let current = result.current;
        let matchLength = result.matchLength;
        */
        if (matchLength > 0 && matchLength < edgeLength) {
                    //部分匹配 → 分裂//分裂：用于"共享前缀但后续分叉"的情况
                    //分裂操作内部处理了新叶子的创建，但需要为其他两种情况定义对应的添加方法！
                    this._splitNode(node, suffixIndex, matchLength);
        } else if (matchLength === edgeLength) {
                    // 完全匹配 → 继续路由
                    let nextChar = this.text[current];// 获取匹配后的下一个字符
                    if (node.children[nextChar]) {
                        // 🎯 情况A：有对应的子节点 → 继续递归
                        this._walkDown(current, node.children[nextChar]);
                    } else {
                        // 🎯 这里才是真正添加叶子的地方！
                        //完全匹配但无子节点 → 直接添加叶子 (_addLeaf)，不需要走分裂流程就不会有叶子
                        this._addLeaf(node, current);
                    }
                } 
        else {
               //🎯理论上不会发生，但作为错误检查：可以去掉，因为正常的算法流程不会进入这个分支，作为调试工具，发现算法错误，提高代码的健壮性
                console.error(`❌ 内部节点完全不匹配: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
                this._addNewBranch(node, suffixIndex);
            }
                return;
            }
         else {
        // 💥💥💥💥💥 叶子节点逻辑
        //🔥叶子节点：重新赋值
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.end - node.start + 1;
        
        console.log(`叶子节点比较结果: matchLength=${matchLength}, current=${current}`);
        
        // 叶子节点决策逻辑...
        // 🎯 直接调用，不需要额外决策
        this._compareSuffixWithEdge(suffixIndex, node);
        // 比较方法内部会处理分裂或创建新分支
    }
/*edgeLength 是当前边的文本标签的长度：
情况1：完全匹配：完全匹配应该发生在后缀与边标签完全一致且没有剩余字符时
后缀11: "s"
遇到内部节点 [s] (边标签="s")
比较:
"s" vs "s"
完全匹配1个字符
matchLength = 1
edgeLength = 1  
current = 12 (text.length)→没有剩余字符
matchLength = edgeLength → 完全匹配
情况2：部分匹配
新后缀: "asanaus" (从位置5开始) 
边标签: "ana" (位置1-3)
比较:
"a"sanaus vs "a"na
只匹配1个字符
matchLength = 1  
edgeLength = 3（ana的长度）
matchLength < edgeLength → 部分匹配
内部节点的路由机制：根节点根据首字符路由到不同分支，如果首字符不匹配，根本不会进入这个内部节点；完全不匹配"更多发生在：根节点级别或者算法错误时
*/

        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);
    /*    if (node.children[nextChar]) {
            console.log(` 路由到子节点: ${nextChar}`);
            let childNode = node.children[nextChar];
            // 🚨 关键：继续在子节点中进行字符比较，可能触发进一步分裂
            this._walkDown(current, childNode);//suffixIndex（原始后缀起始位置）*/
/*
💥注意参数的正确传递，如果递归调用比较方法，传入current而不是index
如果传入原始其实后缀位置会发生：                                            
处理后缀5: "asanaus"                                                    
遇到内部节点 [ana] (边标签="ana")                                        
当前逻辑：                                             正确逻辑：                 
1. 看到首字符'a'                                     //先比较 "asanaus" vs "ana"                 
2. 找到子节点键'a'存在                                //发现匹配1个字符 ("a")                 
3. 递归调用_walkDown(5,childNode) ←还是从位置5开始！   //当前指针走到位置6 (剩余 "sanaus")         
4. 在子节点中重新比较asanausvs子节点的边标签            //递归调用 _walkDown(6, childNode) ← 从已匹配位置继续！
关键原则：在 JavaScript 中，let 和 const 声明的变量有"暂时性死区"，在声明之前不能使用。把所有声明放在函数开头可以避免这个问题
_walkDown(suffixIndex, node) {
    if (某个条件) {
        this._walkDown(current, childNode) //🚨在声明之前使用//🚨问题：这里直接使用 current，但 current 还没有计算！
    } 
    let current = suffixIndex;
💥缺少了字符比较来计算current,要把current算出来就必须把比较的方法放在路由之前,如果比较放在路由之前就会爆红，所以需要用一个新的变量来点出比较方法，把比较方法封装到内部方法里面
[a] (内部节点)
  ├── [na] (内部节点) 
  │     ├── [nasanaus] (叶子)  // 后缀1: "ananasanaus" 的部分
  │     └── [sanaus] (叶子)  // 后缀3: "anasanaus" 的部分
  └── [s] anaus (叶子)        // 后缀5: "asanaus"
}
*/
       //🔁与内部节点边标签比较
        //let matchLength = this._compareWithEdge(suffixIndex, node);
        //🎯避免重复代码：比较逻辑只写一次;解决死循环：方法调用不会造成循环依赖,调试清晰：比较过程有详细的日志,可复用：其他地方也可以使用这个比较方法
     /*   if (matchLength > 0 && matchLength < (node.edgeEnd - node.edgeStart + 1)) {
            //matchLength > 0，说明至少匹配了1个字符；node.edgeEnd - node.edgeStart + 1计算当前边的总长度；matchLength < 边长度：匹配的字符数 < 边的总长度，说明没有完全匹配整条边
            //如果匹配了至少1个字符，但没有匹配整条边
            //🔁情况一：如果部分匹配 → 分裂内部节点
            console.log(`   部分匹配 ${matchLength} 个字符，分裂内部节点`);
            this._splitNode(node, suffixIndex, matchLength);
            //分裂后不需要重新写指针关系：分裂逻辑 _splitNode 内部已经处理了指针关系
            return;
        } else if (matchLength === (node.edgeEnd - node.edgeStart + 1)) {
            //情况二：如果完全匹配 → 路由到子节点
            console.log(`   完全匹配，路由到子节点`);
            let nextChar = this.text[suffixIndex + matchLength];
            if (node.children[nextChar]) {
                this._walkDown(suffixIndex + matchLength, node.children[nextChar]);
            } */
           //=======================
        /*  if (node.children[nextChar]) {
             //直接路由
            }else {
                /*
                它假设：在内部节点中，如果根据首字符找不到子节点，就直接添加新叶子
                let nextChar = this.text[suffixIndex]; // 使用原始位置的首字符
                    if (node.children[nextChar]) {   
                        // 路由到子节点
                    } else {
                        // 🚨错误：直接添加新叶子
                        // 这跳过了必要的字符比较！
                    }
                        1. 取首字符 'a'
                        2. 查找 node.children['a'] 
                        3. 没找到 → 直接添加叶子 [asanaus]
                        4. 🚨 跳过了比较和分裂！
                */
          /*  console.log(`   叶子节点处理...`);
               //情况三：如果完全不匹配 → 添加新叶子
               console.log(`    添加新叶子到内部节点: ${nextChar}`);
                // 创建新叶子节点
                    let leaf = new SuffixTreeNode();
                    leaf.start = suffixIndex;
                    leaf.end = this.text.length - 1;
                    leaf.edgeStart = suffixIndex;
                    leaf.edgeEnd = this.text.length - 1;
                    // 添加到内部节点的子节点中
                    node.children[nextChar] = leaf;
                }
                return;
            }
            */
/*
💥叶子节点没有进入这个路由分支！叶子节点直接执行后面的通用比较逻辑，所以能正常分裂  
💥架构设计：
内部节点：走路由逻辑（快速查找）
合理的性能优化！内部节点通过路由快速定位到可能匹配的分支，叶子节点再进行详细的字符比较和分裂。叶子节点：走比较分裂逻辑（精细处理）
问题不在于架构设计，而在于内部节点路由逻辑中的索引计算错误
💥后缀树需要更精细的字符比较模型
💥内部节点应该先比较，再决策，而不是基于首字符直接路由

*/
//===========比较逻辑==========//
// 在通用比较逻辑开始前添加：
/*console.log(`🔍 通用比较调试:`);
console.log(`   节点类型: ${node.start === -1 ? '内部节点' : '叶子节点'}`);
console.log(`   节点edgeStart: ${node.edgeStart}, edgeEnd: ${node.edgeEnd}`);
console.log(`   边标签: "${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
console.log(`   后缀: "${this.text.substring(suffixIndex)}"`);
console.log(`   比较范围: 后缀位置${suffixIndex} vs 边位置${node.edgeStart}到${node.edgeEnd}`);
//🔥沿着树的边逐字符比较，找到新后缀的插入位置：后缀树匹配和分裂的核心逻辑
//1.字符比较
while (current < this.text.length && edgePos <= node.end) {
        if (this.text[current] !== this.text[edgePos]) {
            console.log(`    不匹配: 位置${current}('${this.text[current]}') ≠ 位置${edgePos}('${this.text[edgePos]}')`);
            break;
        }
        console.log(`    匹配: 位置${current}('${this.text[current]}') = 位置${edgePos}('${this.text[edgePos]}')`);
        current++;
        edgePos++;
    }
//第2步：计算匹配结果
//决策的关键！它计算了两个重要长度，用来决定接下来该做什么
let matchLength = current - suffixIndex;//matchLength - 已匹配的长度
let edgeLength = node.edgeEnd - node.edgeStart + 1;//✅使用edgeStart/edgeEnd//edgeLength-当前边的总长度
console.log(`  匹配结果: matchLength=${matchLength}, edgeLength=${edgeLength}`);
/*
🔥当前边 = 从父节点到当前节点的路径上的文本标签
插入后缀3: "anasanaus"
假设当前有边: "ananasanaus" (start=1, end=11)
_walkDown(3, node) {
    node.start=1, node.end=11
    当前边 = text[1..11] = "ananasanaus"
    比较:
    新后缀: a n a s a n a u s  (从位置3开始)
    当前边: a n a n a s a n a u s  (从位置1开始)//当前边就是从父节点到当前节点的路径上显示的那个文本标签
         ✅✅✅ ❌
        current = 6   匹配结束位置（不匹配发生在位置6）
        suffixIndex = 3
        matchLength = 6 - 3 = 3  匹配了3个字符"ana"
        node.start=1, node.end=11  
        edgeLength = 11 - 1 + 1 = 11当前边总长度11个字符
        决策: 3 < 11 → 部分匹配，需要分裂
}
🔥当前节点：node（树中已存在的节点，我们正在与它比较），比较过程：把新后缀与当前节点的边标签逐个字符比较，新的后缀：text[suffixIndex..]（我们正在尝试插入的内容）
*/
//第3步：三种情况处理
/*if (matchLength === edgeLength) {
        // 情况1: 完全匹配当前边，继续向下
/*
🔥完全匹配 = 新后缀与当前边的标签完全匹配，但新后缀还有剩余字符：
在 "anana" 匹配 "ana" 的情况下：current =3开始：比较结束后:current = 6，this.text.length = 6，if (current < this.text.length) → 6 < 6 → false，所以不会进入 if 分支，直接结束
文本：banana：当前边: "ana" (node.start=3, end=5)  新后缀: "ana" (suffixIndex=3)//部分匹配，不是完全匹配
🔥"完全匹配"有两种情况：
情况1：真正完全匹配（结束）：
当前边: "ana"
新后缀: "ana"
结果: 完全匹配，没有剩余，结束
情况2：前缀匹配（继续向下）：
当前边: "ana" (内部节点)
新后缀: "anana" 
结果: 完全匹配当前边，但还有剩余"na"，继续向下
🎯"完全匹配+继续向下"只发生在：🎯当前节点是内部节点（有子节点），🎯新后缀比当前边长（有剩余字符）
叶子节点的情况（无法继续向下）：
[anana] (叶子)
↑
完全匹配，结束！
内部节点的情况（可以继续向下）：结构要求：只有内部节点才有子节点可以"继续向下"，逻辑要求：如果当前节点是叶子，完全匹配就意味着后缀已存在，应该结束
[ana] (内部节点)//算法要求：后缀树的压缩特性要求共享前缀必须是内部节点//天然地要求当前节点必须是内部节点
├── [na] (叶子)
└── [s]  (叶子)
↑
完全匹配"ana"，继续在子节点中匹配剩余"na"
 */
/*      console.log(`完全匹配，继续向下`);
        if (current < this.text.length) {
            let nextChar = this.text[current];
            if (node.children[nextChar]) {
                this._walkDown(current, node.children[nextChar]);
            } else {
                console.log(` 添加新叶子，字符: ${nextChar}`);
                let leaf = new SuffixTreeNode();
                leaf.start = current;
                leaf.end = this.text.length - 1;
                node.children[nextChar] = leaf;
            }
        }
    } 
else if (matchLength > 0) {
        // 情况2: 部分匹配，需要分裂
        console.log(`部分匹配，需要分裂`);
        this._splitNode(node, suffixIndex, matchLength);
} else {
        // 情况3: 首字符匹配但matchLength=0（不应该发生）
        console.error(`    错误: 首字符匹配但matchLength=0`);
        console.error(`     后缀: "${this.text.substring(suffixIndex)}"`);
        console.error(`     边: "${this.text.substring(node.start, node.end + 1)}"`);
    }
    //🎯只有叶子节点才进行字符比较和分裂
    console.log(`   _walkDown: 后缀${suffixIndex}="${this.text.substring(suffixIndex)}", 边="${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
*/}
// 需要添加这个方法，在已有路径完全匹配后添加叶子
_addLeaf(parentNode, startPos) {
    let leaf = new SuffixTreeNode();
    leaf.start = startPos;// 叶子节点在文本中的起始位置
    leaf.end = this.text.length - 1;// 叶子节点在文本中的结束位置
    leaf.edgeStart = startPos; // 边的起始位置（与start相同）//🎯
    leaf.edgeEnd = this.text.length - 1;// 边的结束位置//🎯
    
    let nextChar = this.text[startPos]; // 获取用于路由的字符
    if (!parentNode.children) parentNode.children = {};// 确保children对象存在
    parentNode.children[nextChar] = leaf; // 将叶子挂载到父节点
    
    console.log(` 添加新叶子: ${this.text.substring(startPos)}`);
}
_addNewBranch(parentNode, suffixIndex) {//在完全不匹配时创建全新分支
    console.log(` 创建新分支: ${this.text.substring(suffixIndex)}`);
    let leaf = new SuffixTreeNode();
    leaf.start = suffixIndex;
    leaf.end = this.text.length - 1;//🎯
    leaf.edgeStart = suffixIndex;//🎯
    leaf.edgeEnd = this.text.length - 1;
    let nextChar = this.text[suffixIndex];
    if (!parentNode.children) parentNode.children = {};
    parentNode.children[nextChar] = leaf;
    
    console.log(` 新分支创建完成: ${nextChar} -> ${this.text.substring(suffixIndex)}`);
}

debugSplit(node, suffixIndex, matchLength) {
    console.log(`🔧 分裂调试:`);
    console.log(`   插入后缀: "${this.text.substring(suffixIndex)}" (start=${suffixIndex})`);
    console.log(`   匹配节点: "${this.text.substring(node.start, node.end + 1)}" (start=${node.start}, end=${node.end})`);
    console.log(`   匹配长度: ${matchLength}`);
    console.log(`   分裂位置: ${node.start + matchLength}`);
    
    // 检查分裂前的父节点
    let parentBefore = this._findParent(node);
    console.log(`   分裂前父节点:`, parentBefore ? this.text.substring(parentBefore.start, parentBefore.end + 1) : '无');
        
     //3.🎯完整的字符比较逻辑
    //第1步：字符比较：逐个字符比较新后缀和当前边的标签
    //字符比较是后缀树的核心精髓！它解决了后缀树最关键的问题：如何发现和利用重复模式。1. 发现共享前缀2. 支持高效搜索3. 构建压缩树结构：字符比较让后缀树从朴素Trie变成压缩Trie
    //空间效率：共享前缀只存储一次，时间效率：搜索时快速定位，结构清晰：自然形成层次结构
    //字符比较不是可选的，而是后缀树存在的理由！它让后缀树从O(n²)的朴素结构变成了O(n)的压缩结构🎯
    
}
//比较逻辑：
/*_compareSuffixWithEdge(suffixIndex, node){
    
    // 🎯 确定比较的起始位置
    let current = suffixIndex;
    let edgePos;
    if (node.start === -1) {
        // 内部节点：用 edgeStart
        edgePos = node.edgeStart;
        console.log(`   比较: 后缀"${this.text.substring(suffixIndex)}" vs 内部节点边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
    } else {
        // 叶子节点：用 start  
        edgePos = node.start;
        console.log(`   比较: 后缀"${this.text.substring(suffixIndex)}" vs 叶子节点边"${this.text.substring(node.start, node.end + 1)}"`);
    }
    
    let matchLength = 0;
    
    // 🎯 确定比较的边界
    let edgeEnd;
    if (node.start === -1) {
        edgeEnd = node.edgeEnd;
    } else {
        edgeEnd = node.end;
    }
    
    // 字符比较
    while (current < this.text.length && edgePos <= edgeEnd) {
        if (this.text[current] !== this.text[edgePos]) {
            console.log(`    不匹配: 位置${current}('${this.text[current]}') ≠ 位置${edgePos}('${this.text[edgePos]}')`);
            break;
        }
        console.log(`    匹配: 位置${current}('${this.text[current]}') = 位置${edgePos}('${this.text[edgePos]}')`);
        current++;
        edgePos++;
        matchLength++;
    }
    
    console.log(`   匹配长度: ${matchLength}`);
    return matchLength;
}*/
//==============分裂逻辑============//
_splitNode(node, suffixIndex, matchLength) {
     //🚨严格检查：如果原节点身份已经是 -1，说明之前就有问题
    if (node.start === -1) {
        console.error(`❌ 严重错误: 分裂的节点身份已经是 -1!`);
        console.error(`   节点: ${this.text.substring(node.edgeStart, node.edgeEnd + 1)}`);
        console.error(`   正在插入: ${suffixIndex}`);
        console.trace();
        return; // 或者尝试修复
        }
    // 🎯 确保这里有这行：
    let originalIdentity = node.start;  // 🚨 这行必须存在！
    // 🎯 删除这个干扰性检查！
    // 🎯 特别监控对根节点下 'a' 节点的修改
    if (node === this.root.children['a']) {
        console.error(`🚨 警告: 正在修改根节点的 'a' 节点!`);
        console.error(`   当前: start=${node.start}, 正在改为: -1`);
        console.trace();  // 打印调用栈
        }
  /*  this.debugSplit(node, suffixIndex, matchLength);
    //node - 当前需要分裂的节点（匹配发生在这个节点上）/matchLength 就是共同前缀的长度，它决定了在哪里分裂节点
    //🔥suffixIndex -后缀的原始身份标识，正在插入的后缀的起始位置：这个值在整个插入过程中保持不变//suffixIndex就是后缀的身份证号码，永远不变
    console.log(` _splitNode: 分裂节点[${this.text.substring(node.start, node.end + 1)}], suffixIndex=${suffixIndex}, matchLength=${matchLength}`);
    /*node定义：
    // - 这是一个现有的节点，我们正在尝试将新后缀插入到它的路径下
    // - 它可能是叶子节点或内部节点
    // - 它的 start/end 定义了这条边的文本范围
    // - 新后缀与这个节点的边部分匹配（匹配了matchLength个字符）：
    比如文本: "bananasanaus"
    正在插入: "anasanaus" (suffixIndex=3)
    node: 代表 "ananasanaus" (start=1, end=11)
    matchLength: 3 (匹配了 "ana")*/


    /*1.创建内部节点
    let internalNode = new SuffixTreeNode();
    internalNode.start = -1;
    🚨内部节点无身份：内部节点不应该有具体的后缀身份，内部节点代表共享前缀，不属于任何一个具体的后缀，如果内部节点有身份，会造成语义混乱
    internalNode.edgeStart = node.edgeStart;     
    internalNode.edgeEnd = node.edgeStart + matchLength - 1;
    */
    //🎯matchLength当前插入的后缀与现有边已经匹配的字符数量的作用：确定内部节点的范围，确定原节点的调整，🟢确定新叶子的位置：新叶子代表我们正在插入的后缀的剩余部分
    //🎯但注意：新叶子的 start 是原始后缀位置，不是匹配后的位置！
    /* 
    🚨原节点保持原来的 start！但边的标签应该同时被改变!
    ⏹️node.start 保持不变！仍然是start=1:原节点如果不改变直接作为字节点的话，它的start确实保持了初始值，但是它的内容还是start标志的位置开始，内容没有变！
    原节点现在在内部节点下面，应该代表的是后缀的剩余部分
    ⏹️调整原节点的位置，但保持其标识
    ana (内, start=1, end=3)        ← 新建的内部节点
        └── [ananasanaus] (start=1, end=11)←🚨原节点保持不变！但这样边标签还是 "ananasanaus"，不对！
    原节点保持 start=1（身份不变），但显示为 "nasanaus"（内容改变）：这实际上是不可能的，因为在一个节点中，start 既表示身份又决定边标签
    🔧1.需要创建新节点，而不是修改原节点：⚠️根本矛盾：一个节点无法同时满足：start 值作为永恒的身份标识，start/end 准确描述边的文本内容
    🔧2.此时引入新的变量用来记录原始文本的start值，内容依旧加上长度计算防止矛盾，记录原始的start和内容改变分开⚠️但这样start可读性非常差   
    🔥3.完全放弃用start作为边标签，让start永远代表身份：让打印出来的 start 值就是初始的 start，让人能直观理解。用新的变量来表示内容的起始位置。
    🔧4.创建新的内部节点，创建新的叶子节点，创建新的剩余节点，直接丢弃原节点：⚠️原节点还存在于树中，如果丢弃会造成内存泄漏和结构混乱
    🔥5.重用原节点（实际做法）：我们不创建新的内部节点，而是直接把原节点改造成内部节点。
    */
   
    console.log(`🔧 分裂调试:`);
    console.log(`   插入后缀: "${this.text.substring(suffixIndex)}" (身份=${suffixIndex})`);
    console.log(`   匹配节点: "${this.text.substring(node.edgeStart, node.edgeEnd + 1)}" (身份=${node.start})`);
    console.log(`   匹配长度: ${matchLength}`);
    console.log('=== 分裂节点 ===');
    console.log('原节点:', {
        start: node.start, 
        end: node.end,
        edgeStart: node.edgeStart, 
        edgeEnd: node.edgeEnd,
        edgeLabel: this.text.substring(node.edgeStart, node.edgeEnd + 1)
    });
    console.log('🔥 === 分裂终极调试 ===');
    console.log('🔥 节点身份:', node.start, node.end, node.edgeStart, node.edgeEnd);
    console.log('🔥 节点类型:', node.start === -1 ? '内部节点' : '叶子节点');
    console.log('🔥 边标签:', this.text.substring(node.edgeStart, node.edgeEnd + 1));
    console.log('🔥 匹配长度:', matchLength);
    console.log('🔥 正在插入的后缀:', this.text.substring(suffixIndex));
    //1.🔥第一步：直接改造原节点为内部节点：保存原节点的信息（在修改前）
    //💥💥💥💥💥你把叶子节点改造成了内部节点，但忘记调整它的边标签边界！
    let originalStart = node.start;// 保存原身份（后面要用）
    let originalEnd = node.end;// 保存原边标签结束
    let originalEdgeStart = node.edgeStart;  //保存原边标签起始


    let originalChildren = {...node.children};// 保存原子节点
    console.log(`   end值跟踪: 原节点end=${originalEnd}`);
    // 🚨不创建新的内部节点！直接改造原节点
    // 原节点现在变成共享前缀的内部节点
    /*🔥立即改造原节点：在分裂时过早地把节点标记为内部节点（设置 start=-1），
    /但这时候原节点可能还不是内部节点（可能还是叶子）设置start=-1 后，就丢失了原始身份信息；后续操作都基于这个错误的-1值
    解决方案：推迟身份清除：不要在分裂开始时就把 start 设为 -1，而是最后一步才设置 -1
    */
    // 🎯 第二步：创建两个新节点
    //2.1🔥创建代表原节点剩余部分的新节点（代表原节点的剩余部分）使用保存的原始值计算：总是使用保存的原始值来计算，避免依赖可能被修改的节点属性
    
    let remainingNode = new SuffixTreeNode();
    remainingNode.start = node.start;//1.🚨继承原身份
    remainingNode.end = originalEnd;// 🚨 必须设置
    //remainingNode.edgeStart = node.edgeStart + matchLength;//剩余节点内容的起始值 
    remainingNode.edgeStart = originalStart + matchLength;//2.需要原结束位置，originalStart时机安全：使用保存的原始值，不受后续修改影响，语义清晰：明确表示"基于原始起始位置计算"，避免混淆：不依赖可能被修改的 node.edgeStart
    remainingNode.edgeEnd = originalEnd;//3.直接使用保存的值 
    remainingNode.children = originalChildren;//🎯4.如果原内部节点有子节点，分裂后，这些子节点应该转移到剩余节点下面//继承原子节点
    

    console.log(`  end值跟踪: 剩余节点end=${remainingNode.end}`);

    //2.2🔥新叶子必须记录原始后缀位置，创建新叶子（代表正在插入的后缀）
    let newLeaf = new SuffixTreeNode();
    newLeaf.start = suffixIndex;//很重要🎯
    newLeaf.end = this.text.length - 1;  // 🚨 必须设置！
    console.log(`   创建新叶子前: start=${newLeaf.start}`);
    newLeaf.edgeStart = suffixIndex + matchLength;
    newLeaf.edgeEnd = this.text.length - 1;


    console.log(`   创建新叶子后: start=${newLeaf.start}`);
    console.log(`    end值跟踪: 新叶子end=${newLeaf.end}`);
    //newLeaf.end = this.text.length - 1;//叶子节点总是延伸到文本末尾文本："bananasanaus" (长度=12)

                                 
    
    //🎯先完全初始化节点，再使用它们🚀在对象字面量中使用变量前，确保该变量已经完全初始化！
    let remainingChar = this.text[remainingNode.edgeStart];  // ✅ 安全
    let newLeafChar = this.text[newLeaf.edgeStart];         // ✅ 安全
    //🎯添加身份传递检查
    console.log(`   🎯 身份传递: 原节点身份=${originalIdentity} → 剩余节点身份=${remainingNode.start}`);  
    //🎯第三步：最后才设置原节点为内部节点
    node.start = -1;//内部节点无身份🚨最后一步！//
    node.edgeStart = originalEdgeStart;                   // 边标签起始：1
    node.edgeEnd = originalEdgeStart + matchLength - 1;       // 边标签结束：3  
    //💥originalEdgeStart：🎯 虽然结果相同，但逻辑意义不同！originalEdgeStart：明确表示边的起始位置，originalStart：节点的身份标识，可能在其他情况下不同
    //node.children = {};// 先清空，稍后添加子节点 
    node.children = {
        [remainingChar]: remainingNode,
        [newLeafChar]: newLeaf
    }; 


    //🎯修正后的调试输出
    console.log(`   改造结果:`);
    console.log(`     - 原节点 → [${this.text.substring(node.edgeStart, node.edgeEnd + 1)}] (内部节点, start=${node.start})`);
    console.log(`     - 剩余节点 → [${this.text.substring(remainingNode.edgeStart, remainingNode.edgeEnd + 1)}] (身份=${remainingNode.start})`);
    console.log(`     - 新叶子 → [${this.text.substring(newLeaf.edgeStart, newLeaf.edgeEnd + 1)}] (身份=${newLeaf.start})`);
    console.log(`   子节点键: '${this.text[remainingNode.edgeStart]}' → 剩余节点, '${this.text[newLeaf.edgeStart]}' → 新叶子`);

    // 在 _splitNode 最后添加
    console.log(`    分裂后验证:`);
    console.log(`      原节点: [${this.text.substring(node.edgeStart, node.edgeEnd + 1)}] (start=${node.start}, end=${node.end})`);
    console.log(`      剩余节点: [${this.text.substring(remainingNode.edgeStart, remainingNode.edgeEnd + 1)}] (start=${remainingNode.start}, end=${remainingNode.end})`);
    console.log(`      新叶子: [${this.text.substring(newLeaf.edgeStart, newLeaf.edgeEnd + 1)}] (start=${newLeaf.start}, end=${newLeaf.end})`);

    /*console.log(`   内部节点: [${this.text.substring(internalNode.start, internalNode.end + 1)}]`);
    console.log(`   原节点调整: [${this.text.substring(node.start, node.end + 1)}]`);
    console.log(`   新叶子: start=${newLeaf.start}, 代表 "${this.text.substring(newLeaf.start)}"`);*/
    //3.更新节点间的父子关系/重新连接节点关系
        /*
        之前：父节点
        └── node (原节点)
        之后：父节点
        └── internalNode (新建的内部节点)
            ├── node (调整后的原节点)
            └── newLeaf (新叶子)
        
    🔥：重用原节点的最大优势：不需要更新任何父节点引用
    如果直接改变原节点为内部节点就不需要重新维护指针关系，我们只是改变了原节点里面的状态：
    原节点对象没变：还是同一个内存对象//父节点的引用没变：父节点仍然指向同一个对象
           */
    /* 1. 找到原节点的父节点
    let parent = this._findParent(node);//可能 _findParent没有找到正确的父节点，导致节点关系混乱！
    // 2. 获取内部节点的首字符（用于在父节点的children中定位）
    let firstChar = this.text[internalNode.start];
    // 3. 将父节点指向原节点的链接改为指向新内部节点// 现在：parent → internalNode（而不是原来的 node）
    if (parent) {
        parent.children[firstChar] = internalNode;
    }
    // 4. 将原节点和新叶子作为内部节点的子节点
    internalNode.children[this.text[node.start]] = node;
    internalNode.children[this.text[newLeaf.start]] = newLeaf;*/
    console.log(`   分裂位置分析:`);
    console.log(`     匹配长度: ${matchLength}`);
    console.log(`     应该分裂在: 共享前缀 "${this.text.substring(node.edgeStart, node.edgeStart + matchLength)}"`);
    console.log(`   重组完成`);


}
_findParent(node){
    //使用广度优先搜索 (BFS) 来寻找父节点
    console.log(`  寻找节点 [${this.text.substring(node.start, node.end + 1)}] 的父节点`);
    let queue = [this.root];//1.从根节点开始
    //🚨这里不是"根节点是队列"，而是创建一个队列，初始时包含根节点
    /*广度优先BFS 确保：先检查高层级节点（更可能是父节点），不会错过任何节点，找到的父节点是最近的：根 → 子节点A → 子节点B → 子节点C → 孙节点A1...
    深度优先 (DFS)：根 → 子节点A → 孙节点A1 → 曾孙节点A1a...
    */
    while (queue.length > 0) {
        let current = queue.shift();// 取出队列第一个节点//从队列的头部取出第一个元素，确保我们按"层级顺序"遍历树
        // 检查current的所有子节点
        for (let [char, child] of Object.entries(current.children)) {
            //Object.entries() 的作用：将对象转换为键值对数组；
            /*{'a': { start:1, end:3,children: {...} 
               'char':{child}
            },  子节点A*/
            console.log(`    检查: ${char} -> [${this.text.substring(child.start, child.end + 1)}]`);
            if (child === node) {// 找到目标节点的父节点
                console.log(` 找到父节点`);
                return current;
            }
            queue.push(child);// 将子节点加入队列继续搜索
        }
    }
    console.log(`  未找到父节点`);
    return null;
}

search(pattern) {
    //✅后缀树搜索:是否存在，所有出现位置，精确匹配（不是模糊匹配）
    //✅关键特性：找所有位置：不只是第一个出现的位置；精确子串：必须是连续字符序列；O(m)速度：搜索时间只与模式串长度有关，与文本大小无关
    //✅在后缀树中搜索模式串，会返回该模式串在文本中所有出现的起始位置列表"；不仅仅是"显示内容"，而是精确定位所有出现位置！
    let currentNode = this.root;
    let patternIndex = 0;
    //1.外层循环 - 控制模式串进度
    while (patternIndex < pattern.length) {//只要模式串还有字符没匹配完，就继续
        //2. 选择分支
        let currentChar = pattern[patternIndex];
        if (!currentNode.children[currentChar]) return [];//根据当前要匹配的字符，选择树上的对应分支。如果没有这个分支，说明模式串不存在"
        //3. 获取边上文本
        let child = currentNode.children[currentChar];
        let edgeText = this.text.substring(child.start, child.end + 1);
        //4. 内层循环 - 匹配边上字符
        for (let i = 0; i < edgeText.length && patternIndex < pattern.length; i++) {
            if (edgeText[i] !== pattern[patternIndex]) return [];//逐个字符比较边上文本与模式串的剩余部分。如果发现不匹配，立即返回失败
            patternIndex++;
        }
        currentNode = child;//5.移动到下一节点
    }
    
    return this._collectLeafIndices(currentNode);

/*-------⚠️注意--------
🔧在文本 "bananasanaus" 中："ana" 应该出现在位置1,3但结果出现了位置8，这说明在分裂操作或叶子节点收集时：某些叶子节点的start值设置错误，或者搜索时匹配过度，包含了不应该匹配的路径
🔧叶子节点标识错误 - start 值设置逻辑有系统性偏差🔧导致重复和缺失 - 但不影响树的结构正确性
🔗 新叶子节点应该代表"正在插入的完整后缀"：插入后缀8 "naus"
理解1：代表"匹配后的剩余部分"：后缀8:n a u s：❌错误方式：后缀8和后缀10都创建 start=10 的叶子
                                | | | |
                                匹配 剩余
                               "na" "us"
                        新叶子代表："us" → start=10
理解2：代表"正在插入的完整后缀"：✅正确方式：后缀8创建 start=8，后缀10创建 start=10
后缀8: "n a u s"
        ↑
        完整后缀开始位置
新叶子代表："naus" → start=8
🔗新叶子节点永远代表：当前正在插入的完整后缀；不是剩余部分，不是片段，而是完整的原始后缀！
🔗搜索"ana":
1. 根节点 → 找键'a' → 找到内部节点
2. 内部节点边标签="ana" → 匹配成功!
3. 继续在内部节点下处理剩余部分
搜索"an":
1. 根节点 → 找键'a' → 找到内部节点  
2. 内部节点边标签="ana" → 匹配前2个字符"an"
3. 部分匹配，需要分裂 
共享前缀 "ana" 的完整边标签就是 "ana"，在父节点的children中只用首字符 'a' 作为查找键，这是为了搜索效率，不是边被截断了 
*/
}
_collectLeafIndices(node) {//递归收集所有叶子节点的起始位置：找到某个节点下的所有叶子节点，并收集它们的start值
    let results = [];
    if (Object.keys(node.children).length === 0) {//1. 基本情况 - 叶子节点
        results.push(node.start);
    } else {//2. 递归情况 - 内部节点：如果这个节点有子节点，就递归处理每个子节点，把结果合并
        for (let child of Object.values(node.children)) {
            results = results.concat(this._collectLeafIndices(child));
        }
    }
    return results;
}
// 添加调试方法
debugLeafStarts() {
    console.log("=== 检查所有叶子节点的start值 ===");
    this._debugLeafStarts(this.root);
}

_debugLeafStarts(node, path = "") {
    if (Object.keys(node.children).length === 0) {
        let suffix = this.text.substring(node.start);
        console.log(`叶子: 路径=${path}, start=${node.start}, 后缀="${suffix}"`);
    } else {
        for (let [char, child] of Object.entries(node.children)) {
            let edgeText = this.text.substring(child.start, child.end + 1);
            this._debugLeafStarts(child, path + " → [" + edgeText + "]");
        }
    }
}
// 检查是否所有后缀都有对应的叶子节点
checkAllSuffixes() {
    console.log("=== 检查所有后缀是否都有叶子节点 ===");
    const n = this.text.length;
    let missing = [];
    
    for (let i = 0; i < n; i++) {
        let found = false;
        // 遍历所有叶子节点，检查是否有start=i的
        let queue = [this.root];
        while (queue.length > 0) {
            let node = queue.shift();
            if (Object.keys(node.children).length === 0) {
                if (node.start === i) {
                    found = true;
                    break;
                }
            } else {
                for (let child of Object.values(node.children)) {
                    queue.push(child);
                }
            }
        }
        
        if (!found) {
            missing.push(i);
            console.log(`缺失: start=${i}, 后缀="${this.text.substring(i)}"`);
        }
    }
    
    if (missing.length === 0) {
        console.log(" 所有后缀都有对应的叶子节点");
    } else {
        console.log(`总计缺失 ${missing.length} 个后缀`);
    }
}
}




/*测试
console.log("=== 测试 ===");
let tree = new SuffixTree("bananasanaus");
tree.debugStepByStep();*/

/* 测试搜索功能
function testSearch() {
    let tree = new SuffixTree("bananasanaus");
    
    // 构建树
    for (let i = 0; i < tree.text.length; i++) {
        tree._addSuffix(i);
    }
    console.log("=== 搜索测试 ===");
    // 基本测试
    console.log("'ana' 位置:", tree.search("ana"));    // 应该返回 [1, 3]
    console.log("'na' 位置:", tree.search("na"));      // 应该返回 [2, 4]  
    console.log("'us' 位置:", tree.search("us"));      // 应该返回 [10]
    console.log("'ban' 位置:", tree.search("ban"));    // 应该返回 [0]
    // 边界测试
    console.log("'xyz' 位置:", tree.search("xyz"));    // 应该返回 []
    console.log("'' 位置:", tree.search(""));          // 应该返回所有位置
    // 单个字符
    console.log("'a' 位置:", tree.search("a"));        // 应该返回 [1, 3, 7, 9]
    console.log("'n' 位置:", tree.search("n"));        // 应该返回 [2, 4, 8]
}

testSearch();

let tree = new SuffixTree("bananasanaus");
for (let i = 0; i < tree.text.length; i++) {
    tree._addSuffix(i);
}

tree.debugLeafStarts();
*/
console.log("=== 详细构建过程 ===");
console.log('=== 启动调试 ===');
console.log('SuffixTree 类:', typeof SuffixTree);
console.log('准备创建实例...');
let tree = new SuffixTree("bananasanaus");
console.log('实例:', tree);
console.log('根节点:', tree.root);
console.log('根节点start:', tree.root.start);
for (let i = 0; i < tree.text.length; i++) {
    console.log(`\n 步骤 ${i}: 插入后缀 "${tree2.text.substring(i)}"`);
    tree._addSuffix(i);
    // 每步后检查叶子节点
    if (i < 5) { // 只看前几步，避免输出太多
        console.log("当前叶子节点:");
        tree._debugLeafStarts(tree2.root);
    }
}
let tree1 = new SuffixTree("bananasanaus");
console.log('实例:', tree);
console.log('根节点:', tree.root);
console.log('根节点start:', tree.root.start);
for (let i = 0; i < tree3.text.length; i++) {
    tree._addSuffix(i);
}
tree1.checkAllSuffixes();
tree1.debugLeafStarts();

// 测试代码
let tree2 = new SuffixTree("bananasanaus");
console.log("创建树后根节点children:", Object.keys(tree.root.children));  //🎯这里检查
// 如果这里就已经有节点，说明构造函数有问题
// 如果这里是空的，但 debugStepByStep 开始时就有节点，说明 debugStepByStep 内部有问题
tree2.debugStepByStep();
```
- **🎊✨完整后缀压缩树朴素算法实现版本🎊✨**
```
//==========🎉🎉🎉🎉🎉🎉🎉🎉🎉朴素算法后缀树完整实现🎉🎉🎉🎉🎉🎉🎉🎉🎉==================//
class SuffixTreeNode {
    constructor() {
        this.children = {};
        this.start = -1;
        this.end = -1;
        this.edgeStart = 0;      // 🎯 在节点构造函数中错误地使用了 this.root 而不是 this！
        this.edgeEnd = 0;        // 🎯 立即设置！
        this.suffixLink = null;
        this.parent = null;  // 🎯 新增父指针：第一步：修改节点类，添加父指针
    }}
        //🎯每次创建 new SuffixTreeNode() 后，必须立即设置 start, end, edgeStart, edgeEnd 四个值！

/*      this.start = -1;//🔥永远代表原始后缀身份
        this.end = -1;//
        this.edgeStart = -1;  // 🔥新增：边标签起始位置
        this.edgeEnd = -1;    // 🔥新增：边标签结束位置
*/
/*💥💥💥💥
创建新节点: 
Object { children: {}, start: 1, end: 11, edgeStart: -1, edgeEnd: -1, ... }
1.不要在构造函数中设置默认的-1，让调用者明确设置所有值：
2.创建后立即设置边界，在你的所有节点创建处，确保创建后立即设置所有四个边界：
can't access property "start", this.root is undefined:这个错误说明根节点this.root 没有正确初始化！
*/


        //this.suffixId = -1;//🔧原始后缀身份标识（仅叶子需要）
/*节点P (父节点)
  |
    children: {
        根
    ├── [bananasanaus] (叶, start=0,end=11)  ← 后缀0
    ├── a (内, start=1,end=1)← ← 边标签:"a"
    │   ├── [na] (叶, start=2,end=3)← ← 边标签:"na" 
    │         └── [sanaus](叶, start=3,end=11)  ← 后缀3 ←边标签: "sanaus"：这是从父节点到子节点的路径标签
    │         └── [nasanaus](叶, start=1,end=11) ← 后缀1
    │         └── [us](叶,start=7,end=11)  ← 后缀7
    |   └── [us](叶,start=9,end=11)  ← 后缀9
    |   └── [sanaus](叶, start=5,end=11)←后缀5
    ├── na (内, start=4,end=5)← 内部节点
    │   └── [sanaus] (叶, start=4,end=11) ← 后缀4
    │   └── [us] (叶, start=8,end=11)    ← 后缀8
    │   └── [nasanaus] (叶, start=2,end=11)← 后缀2
    ├── s (内, start=6,end=6)← 内部节点
    │   └── [s] (叶, start=11,end=11) ← 后缀11
    │   └── [anaus] (叶, start=6,end=11) ← 后缀6 
    ├── [us] (叶, start=10,end=11)    ← 后缀10
  }
🎯边：总是通过父节点的children[key]隐式定义
🔗边被"溶解"在了父子关系中；边的标签被"拆分"存储：首字符在父节点的children键中，完整内容在子节点的(start, end)中；没有独立的边对象让你直接操作
🔗不仅是结构连接的桥梁，更是智能文本载体： 通过索引存储实现空间优化；通过可变长度支持快速匹配；通过方向导航维护结构清晰
🔗节点A (子节点)
  start: 0, end: 6 // 计算得边标签="banana$"
🎉🔥start和end就像身份证一样，每个节点都有唯一的文本区间
    内部节点的 start/end：标识这条边在原文中的位置
    叶子节点的 start/end：标识这个后缀在原文中的位置
    整个路径的拼接：重构出完整后缀  
🎉🔥唯一性约束：
    所有叶子节点的start必须唯一（0到n-1）
    内部节点的start可以与其他节点重复
🎯边标签 (Edge Label)：边上显示的文本片段，描述从父节点到子节点的路径上的字符串，可能只是完整后缀的一部分
🎯后缀标识 (Suffix Identifier)：叶子节点代表的完整后缀的起始位置，唯一标识这个叶子对应哪个后缀，总是指向完整后缀的开始位置：[sanaus] (start=6, end=11) ← 后缀标识: 6（代表后缀6:"sanaus"）
🔗关键区别：边标签 = 路径上的路标（指引方向）后缀标识 = 目的地的地址（最终位置）
范围不同：边标签：可以是任意长度的子串（"a", "na", "san"等），后缀标识：总是标识完整的后缀（从start到文本末尾）
用途不同：边标签：用于导航和匹配（搜索时比较字符），后缀标识：用于结果定位（找到后知道是哪个后缀）
唯一性不同：边标签：可以重复（多个边可以有相同标签）后缀标识：必须唯一（每个后缀有唯一起始位置）
*/
       

/*-------⚠️注意---------/
🔧节点数据损坏: start=1, end=-1：后缀0、1、2 创建时正常，但从后缀3开始，找到的节点就是损坏的 (start=1, end=-1)
//创建叶子节点时，end 值没有被正确设置，确保：_addSuffix(suffixIndex)， leaf.end = this.text.length - 1;
🔧只有 'u' 和 'b' 开头的节点正常，其他都被改成了 start=-1：步骤 0: 插入后缀 "bananasanaus" debugger eval目标节点数据: start=0,end=11；但是步骤 1: 插入后缀 "ananasanaus"，目标节点数据: start=-1, end=11， 所有的后缀节点start都变成了-1开始
分裂逻辑普遍错误：不是个别节点的问题，内部节点转换逻辑错误：把所有节点都转成了 start=-1 的内部节点，只有没被分裂的节点幸存：'u' 和 'b' 节点没有被分裂过
//在分裂时过早地把节点标记为内部节点（设置 start=-1）身份信息要在整个计算过程中保持可用，直到不再需要为止。
🔧Uncaught ReferenceError: can't access lexical declaration 'remainingNode' before initialization：remainingNode 在初始化之前被访问
    let remainingNode = new SuffixTreeNode();  // 🚨声明了，但还没赋值完成
    node.children = {
        [this.text[remainingNode.edgeStart]]: remainingNode,  //🚨这里！
                ↑                          ↑
        访问属性edgeStart           访问变量remainingNode
        但remainingNode还在初始化过程中！
    JavaScript 的执行顺序
        声明阶段：let remainingNode（变量存在，但值为undefined）
        执行阶段：
            开始计算 this.text[remainingNode.edgeStart]
            但 remainingNode 还是 undefined，访问 undefined.edgeStart 就报错
            然后才执行 remainingNode = new SuffixTreeNode()
};
🔧在步骤0（第一次插入）时，根节点的children就已经有5个节点了：在第一次调用 _addSuffix 之前，节点已经被创建了
1.肯定是在构造函数或测试代码的某个地方提前创建了这些节点
2.部分匹配，需要分裂 debugger eval code:307:17
3.警告: 正在修改根节点的 'a' 节点! debugger eval code:331:17当前: start=1, 正在改为: -1：就是在分裂过程中，根节点的 'a' 节点被错误地修改了！
在 _splitNode 中，我们正在把根节点下的 'a' 节点（代表后缀1）转变成内部节点，设置 start=-1。但这是错误的！根节点下的直接子节点不应该变成内部节点！
🔥在正常的后缀树中，根节点的直接子节点确实可以变成内部节点：问题可能在于：原节点的身份没有正确保存和传递。
🔧剩余节点和新叶子在创建时 end 值就是 -1，这说明问题在节点构造函数中：确保每个新创建的节点都完整设置所有字段
1.在创建节点时立即设置所有值：remainingNode.end = originalEnd; 必须设置！newLeaf.end = this.text.length - 1; 必须设置！
2.构造函数不设置默认值：不设置默认值，让调用者负责设置//this.start = undefined;//this.end = undefined;
class SuffixTreeNode {
    constructor() {
        this.children = {};
        // 不设置默认值，让调用者负责设置
        // this.start = undefined;
        // this.end = undefined;
        this.edgeStart = -1;
        this.edgeEnd = -1;
        this.suffixLink = null;
        this.uniqueId = Math.random();
    }
}
🔧分裂创建了正确的节点，但打印函数显示的是错误的内容！
🔧严重错误：在插入后缀5 "asanaus" 时：找到的节点身份已经是 =-1（内部节点），但匹配结果显示 matchLength=1（部分匹配），这说明内部节点也参与了匹配和分裂
🔧内部节点不应该参与字符匹配和分裂！内部节点只是结构节点，它的边标签是固定的，不应该与新的后缀进行字符比较。
🔥在 _walkDown 中，如果当前节点是内部节点（start=-1），应该：直接根据首字符选择子节点，不应该进行字符比较，不应该触发分裂：在walkdown中添加触发条件，
🔧没有把共享前缀 "a" 提取出来：分裂不够彻底，内部节点创建层级错误：应该在 'a' 处就创建内部节点，而不是在 'ana' 处
当插入后缀5 "asanaus" 时：找到 [ana] 内部节点查找子节点 'a'，但没有找到（只有 'n' 和 's'）直接添加了新叶子 [asanaus]
在内部节点路由时，我们没有进行字符比较，只是简单根据首字符路由。
🔧在内部节点路由时，如果找到匹配的子节点，应该继续比较剩余字符：关键修复：继续在子节点中进行字符比较；内部节点路由不能只看首字符，还需要检查是否与现有子节点共享更长的前缀！
🔧问题就是我们没有把 [na] 从 [ana] 中分离出来；我们创建了子节点 'a'，但没有重新组织现有的 'n' 和 's' ‘an’子节点！
🔁当创建新的 'a' 子节点时，我们应该：1.把[ana]节点拆分成[a]+[na]2.把原来的'n'和's'子节点移动到[na]下面，让[a]指向[na]和新的 [sanaus]
🔍子节点键 vs 节点内容：子节点键：是字符，用于在哈希表中查找（'a', 'n', 's'），节点内容：是 SuffixTreeNode 对象，包含实际的边标签
[ana] (内部节点)   +a                     //之后[ana] (内部节点)--->现在确实有 'a' 这个子节点键
  子节点键: {//之前                        子节点键: {
    'n': → [nasanaus] (叶子节点)            'a': → [sanaus] (新叶子, start=5)  ← 刚刚添加的
    's': → [sanaus] (叶子节点)              'n': → [nasanaus] (叶子节点) 
}                                          's': → [sanaus] (叶子节点)}
🔥正确的为后缀与内部节点的匹配设置不同的三种边界条件 
🔧Uncaught ReferenceError: can't access lexical declaration 'matchLength' before initialization ：必须先定义                                            
🔥🔥🔥路由、比较、分裂是三件不同的事情！
比较 (Comparison)：作用：逐个字符对比，找出共享前缀长度，比较：找出匹配了多少个字符，"asanaus" vs "ana" → 匹配了1个字符 'a'
分裂 (Splitting)：作用：根据比较结果重组节点结构//分裂：把[ana]拆成[a]+[na]，[ana] → [a] + [na]                                                                           
路由 (Routing)：作用：根据首字符快速导航到子节点//路由：根据首字符跳转，在 [a] 节点中，根据 's' 找到子节点 [sanaus]
正确顺序：比较 → [判断] → 分裂或路由   
1. 比较 "asanaus" vs "ana" → 匹配1个字符
2. 判断：1 < 3 → 部分匹配
3. 分裂：把 [ana] 拆成 [a] + [na]  
4. 路由：在新区结构中继续处理   
🔥🔥🔥 💥内部节点数据结构设计问题：
1.内部节点边标签不准确：内部节点 [ana] 实际上应该代表从根节点到该节点的路径标签
2.子节点键设计问题：子节点键应该是下一个字符，但你的比较逻辑没有正确执行
3.缺少字符比较：内部节点路由时直接看首字符，没有进行必要的字符比较来确定是否匹配
💥问题不是代码顺序，而是执行路径。内部节点路由分支可能有一个 return 语句，导致代码提前退出，没有执行后面的比较逻辑
❌_walkDown: 后缀5="asanaus", 边="ananasanaus" debugger eval code:252:13
   _walkDown 开始: 节点类型=叶子节点 
比较结果: matchLength=undefined, current=undefined 
插入后: debugger eval code:159:21
根 debugger eval code:167:17
  [ananasanaus] (叶, start=1, end=11) → 后缀1:"ananasanaus" 
  [bananasanaus] (叶, start=0, end=11) → 后缀0:"bananasanaus" 
  [nanasanaus] (叶, start=2, end=11) → 后缀2:"nanasanaus"
🔧比较方法返回 undefined，导致：matchLength和current都是undefined，所有决策逻辑都无法正常工作，算法退回到最简单的添加叶子节点模式
🔧比较方法返回 undefined：关键：在同一个作用域内不要用 let 重复声明同一个变量！
🔧如果类定义有问题，改用函数构造函数
/*function SuffixTreeNode() {
    this.children = {};
    this.start = -1;
    this.end = -1;
    this.edgeStart = -1;
    this.edgeEnd = -1;
    this.suffixLink = null;
    this.uniqueId = Math.random();
}
function SuffixTree {
    constructor(text) {
        this.text = text;
        this.root = new SuffixTreeNode();
        console.log("🚨 构造函数完成时根节点children:", Object.keys(this.root.children));
    }
🔧💥Uncaught TypeError: can't access property "start", this.root is undefined:可能原因1：构造函数没有执行,可能原因2：构造函数中的错误,可能原因3：代码执行顺序问题        
🔧SuffixTree 类: function debugger代码在准备创建实例...之后卡住了，说明实例创建过程中出现了错误！
🔧准备创建实例Uncaught InternalError: too much recursion :无限递归
💥💥💥多个 us 节点有相同的 start=10, end=11 是： 它们都指向文本中的相同位置 "us"，但在树结构中，它们应该有不同的路径身份
显示完整路径：修改你的显示逻辑，不只看节点的 start/end，而是显示从根节点到该节点的完整路径：

    */

class SuffixTree {
    constructor(text) {
        console.log("🔍 构造函数开始，text:", text);
        this.text = text;//🚨可能这里抛出了错误，导致 this.root 没有初始化,//🚨在类完全定义前就使用
        console.log("✅ text 设置完成");
        this.root = new SuffixTreeNode();//🚨 错误：忘记用 new 关键字:此时 this.root 是 undefined
        console.log("✅ 根节点创建完成:", this.root);
        console.log("🚨 构造函数完成时根节点children:", Object.keys(this.root.children));
    }
build() {
    const n = this.text.length;
    for (let i = 0; i < n; i++) {
        console.log(` 插入后缀 ${i}: "${this.text.substring(i)}"`);
        this._addSuffix(i);
    }
}
/*
🎯build()方法：
分离「构造」与「查询」： 没有build()的糟糕设计：每次查询都要重新建树！
有 build() 的良好设计：一次性构建，直接查询，无需重新构建
🔗预处理思想：后缀树的核心价值就是：一次构建（可能较慢）多次查询（非常快速）
🔗清晰的生命周期：初始化 →  构建   → 查询/使用
                ↓        ↓         ↓
              new()    build()   search()
🔗设计模式的体现：典型的Builder模式：构造过程复杂 → 封装在build()中，使用接口简单 → 暴露简单的 search()
*/
    debugStepByStep() {
        const n = this.text.length;
        console.log(`=== 构建后缀树: "${this.text}" ===`);
        for (let i = 0; i < n; i++) {
            console.log(`\n 步骤 ${i}: 插入后缀 "${this.text.substring(i)}"`);
            console.log("插入前:");
            this._printSimple();
            this._addSuffix(i);
            console.log("插入后:");
            this._printSimple();
            console.log("-------------------");
        }
    }
 /*   _printSimple(node = this.root, indent = 0) {
    let space = "  ".repeat(indent);
    if (node === this.root) {
        console.log(space + "根");
    } else {
        let edgeStart = node.start === -1 ? node.edgeStart : node.start;
        let edgeEnd = node.start === -1 ? node.edgeEnd : node.end;
        let edgeText = this.text.substring(edgeStart, edgeEnd + 1);
        let type = Object.keys(node.children).length === 0 ? "叶" : "内";
        
        let suffixInfo = "";
        if (type === "叶") {
            let actualSuffix = this.text.substring(node.start);
            suffixInfo = ` → 后缀${node.start}:"${actualSuffix}"`;
        }
        console.log(space + `[${edgeText}] (${type}, start=${node.start}, end=${node.end})${suffixInfo}`);
    }
    // 按字符排序子节点以便阅读
    let sortedChildren = Object.entries(node.children)
        .sort(([a], [b]) => a.localeCompare(b));
    for (let [char, child] of sortedChildren) {
        this._printSimple(child, indent + 1);
    }
}*/
_printSimple(node = this.root, indent = 0) {
    // 基础显示逻辑
    let space = "  ".repeat(indent);
    
    if (node === this.root) {
        console.log(space + "根");
    } else {
        // 确定显示的文本和类型
        let displayStart = node.start === -1 ? node.edgeStart : node.start;
        let displayEnd = node.start === -1 ? node.edgeEnd : node.end;
        let displayText = this.text.substring(displayStart, displayEnd + 1);
        
        // 判断节点类型：内部节点有children，叶子节点没有
        let isLeaf = Object.keys(node.children).length === 0;
        let type = isLeaf ? "叶" : "内";
        
        // 构建显示信息
        let line = `[${displayText}] (${type}, start=${node.start}, end=${node.end})`;
        
        // 如果是叶子节点，添加后缀信息
        if (isLeaf) {
            let suffixText = this.text.substring(node.start);
            line += ` → 后缀${node.start}:"${suffixText}"`;
        }
        
        console.log(space + line);
        
        // 🎯 特殊显示：如果是 "us" 叶子节点，显示完整路径
        if (displayText === "us" && isLeaf) {
            let path = this._getNodePath(node);
            console.log(space + `   路径: ${path}`);
        }
    }
    
    // 递归显示子节点（按字符排序）
    let childEntries = Object.entries(node.children);
    childEntries.sort(([a], [b]) => a.localeCompare(b));
    
    for (let [char, childNode] of childEntries) {
        this._printSimple(childNode, indent + 1);
    }
}

    

_addSuffix(suffixIndex) {
    //🔥朴素后缀树构建算法的核心：将文本中从位置suffixIndex开始的后缀插入到后缀树中//后缀树的构建引擎，它负责把每个后缀正确地加入到树结构中，并在需要时进行节点分裂来共享公共前缀
    //对于文本 "bananasanaus"：_addSuffix(0) → 插入后缀 "bananasanaus"，_addSuffix(1) → 插入后缀 "ananasanaus"
    //🎯每个后缀独立插入：这是朴素算法的特点；🎯从根节点开始：每次插入都从根节点重新开始；
    //🎯按首字符分组：相同首字符的后缀会在同一个分支下可能触发分裂🎯当新后缀与现有边部分匹配时，会调用 _walkDown 和 _splitNode
    console.log(`\n🔹 插入后缀 ${suffixIndex}: "${this.text.substring(suffixIndex)}"`);
    // 1. 从根节点开始
    let currentNode = this.root;
    // 2. 获取后缀的首字符
    let currentChar = this.text[suffixIndex]; 
    console.log(`   根节点的children:`, Object.keys(currentNode.children)); 
    // 3. 检查根节点是否有以这个字符开头的子节点
    if (!currentNode.children[currentChar]) {
        console.log(`   创建新叶子，字符: ${currentChar}`);
        // 3.1 如果没有：直接创建新叶子
        let leaf = new SuffixTreeNode();
        leaf.start = suffixIndex;
        leaf.end = this.text.length - 1;  //🚨必须设置！
        leaf.uniqueId = Math.random();  // 🎯 添加唯一标识
        console.log(`   创建新节点:`, leaf);
        console.log(`    节点内存地址:`, leaf.uniqueId);
        leaf.edgeStart = suffixIndex;
        leaf.edgeEnd = this.text.length - 1;
        currentNode.children[currentChar] = leaf;
        console.log(`    新节点内存地址:`, leaf.uniqueId);
    } else {// 3.2 如果有：沿着匹配的边继续深入
        
        let targetNode = currentNode.children[currentChar];
        console.log(`    找到现有节点:`, targetNode);
        console.log(`    现有节点内存地址:`, targetNode.uniqueId);
        console.log(`    现有节点数据:`, targetNode);
        this._walkDown(suffixIndex, currentNode.children[currentChar]);
    }
}
_compareSuffixWithEdge(suffixIndex, node) {
    console.log('🎯 _compareSuffixWithEdge 方法开始执行!');
    console.log('参数:', { suffixIndex, node });

    let current = suffixIndex;
    let edgePos = node.edgeStart;
    let matchLength = 0;

    console.log('变量初始化完成:', { current, edgePos, matchLength });
    
    // 🎯 情况1: 完全匹配整个边
    // 🎯 情况2: 部分匹配（匹配了前N个字符）  
    // 🎯 情况3: 完全不匹配（首字符就不匹配）
    console.log(` 比较: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
    while (current < this.text.length && edgePos <= node.edgeEnd) {
        console.log(`   位置${current}("${this.text[current]}") vs 位置${edgePos}("${this.text[edgePos]}")`);
        if (this.text[current] !== this.text[edgePos]) break;
        current++;
        edgePos++;
        matchLength++;
    }
    //第2步：计算匹配结果
    //决策的关键！它计算了两个重要长度，用来决定接下来该做什么
    //let matchLength = current - suffixIndex;//matchLength - 已匹配的长度
    let edgeLength = node.edgeEnd - node.edgeStart + 1;//✅使用edgeStart/edgeEnd//edgeLength-当前边的总长度
    console.log(`  匹配结果: matchLength=${matchLength}, edgeLength=${edgeLength}`);
    //第三步：现在添加三种情况的判断
    if (matchLength === edgeLength) {
        console.log(` 情况1: 完全匹配整个边`);
        if (current < this.text.length) {
            let nextChar = this.text[current];
            if (node.children[nextChar]) {
                this._walkDown(current, node.children[nextChar]);//////
            } else {
                console.log(` 添加新叶子，字符: ${nextChar}`);
                this._addLeaf(node, current);
            }}
    } else if (matchLength > 0) {
        console.log(` 情况2: 部分匹配 ${matchLength} 个字符`);
        this._splitNode(node, suffixIndex, matchLength);
    } else {
        console.log(` 情况3: 完全不匹配`);
        // 🎯 情况3: 完全不匹配 → 创建新分支（正常情况！）
        console.log(`创建新分支: ${this.text.substring(suffixIndex)}`);
        this._addNewBranch(node, suffixIndex);
    }
    console.log(`   比较完成: matchLength=${matchLength}, current=${current}`);
    return { current, matchLength, matchType: matchLength === edgeLength ? 'full' : matchLength > 0 ? 'partial' : 'none' };
    
    // 🎯 确保有这行！
    //return { current, matchLength };
    

}


_walkDown(suffixIndex, node) {//suffixIndex: 正在插入的后缀的起始位置，node: 当前要匹配的节点（边） 
     // 🎯 添加递归保护
    if (!this.recursionDepth) this.recursionDepth = 0;
    this.recursionDepth++;
    
    if (this.recursionDepth > 100) {
        console.error("❌ 递归过深！可能陷入无限循环");
        console.log("当前参数:", { suffixIndex, node });
        console.trace();
        this.recursionDepth = 0;
        return;
    }
    
    console.log(`递归深度: ${this.recursionDepth}, 后缀: ${suffixIndex}`);
   
    
    
    // 先声明变量
    //let current, matchLength, edgeLength;
    //🔥声明并初始化默认值
    let current = suffixIndex;
    let matchLength = 0;
    let edgeLength = 0;
    console.log('=== _walkDown 开始 ===');
    console.log('参数:', { suffixIndex, node });
    console.log('node.start:', node.start);

    //1.🚨先检查节点数据是否有效
    if (node.start > node.end) {
        console.error(`❌ 节点数据损坏: start=${node.start}, end=${node.end}`);
        return;
    } 
    console.log(`   _walkDown: 后缀${suffixIndex}="${this.text.substring(suffixIndex)}", 边="${this.text.substring(node.start, node.end + 1)}"`);
    console.log(`   _walkDown 开始: 节点类型=${node.start === -1 ? '内部节点' : '叶子节点'}`);
    /*2.🎯变量声明：
    let current = suffixIndex;//🎯新后缀的光标
    let edgePos = node.edgeStart;//✅使用 edgeStart//🎯当前边的光标
/*
🔥current跟踪新后缀当前比较到了哪个位置：current 就是新后缀的进度指示器，告诉我们已经匹配了多少，还剩下多少要处理
🎯current的完整生命周期：初始：current = suffixIndex（新后缀开始位置）比较中：current+（逐个字符前进）结束后：current 指向新后缀剩余部分的开始位置
新后缀: a n a s a n a u s
         ↑
       current=3 (开始)
        比较过程:
        a n a s a n a u s
      ✅✅✅ ❌
        ↑ ↑ ↑ ↑
        3 4 5 6 ← current 的位置变化
结束:
a n a s a n a u s
        ↑
      current=6 (剩余部分"sanaus"的开始)
🔥edgePos的作用：这个变量是当前边的"光标"，它与current配对工作
//在分裂时的关键作用：分裂时需要知道在边的哪个位置分裂，edgePos最终值告诉我们在边的哪个位置分裂：重复计算：node.start + matchLength重新计算了edgePos 的值，精度损失：如果计算有舍入误差，可能不一致，语义不清晰：edgePos 直接表示"边的匹配结束位置"，更直观
文本: "bananasanaus"
新后缀: "anasanaus" (从位置3开始)
当前边: "ananasanaus" (从位置1开始)
_walkDown(3, node) {
    let current = 3; 🎯新后缀光标：从位置3开始
    let edgePos = 1; 🎯当前边光标：从位置1开始//如果没有edgePos，我们无法知道当前边比较到了哪里，特别是在边很长的情况下：
    第1轮比较:
    text[current=3]='a' vs text[edgePos=1]='a'✅
    current = 4, edgePos = 2  // 两个光标都前进
    第2轮比较:  
    text[current=4]='n' vs text[edgePos=2]='n'✅
    current = 5, edgePos = 3  // 两个光标都前进
    第3轮比较:
    text[current=5]='a' vs text[edgePos=3]='a'✅  
    current = 6, edgePos = 4  // 两个光标都前进
    第4轮比较:
    text[current=6]='s' vs text[edgePos=4]='n' ❌
    跳出循环
}
*/
//3.🔁⚠️内部节点的路由逻辑
/*内部节点路由的三种情况：
正确的逻辑应该是:先检查新后缀与内部节点边标签的匹配情况,✅如果部分匹配 → 分裂内部节点,✅如果完全匹配 → 路由到子节点,✅如果完全不匹配 → 添加新叶子
应该把"字符匹配情况"作为判断条件*/
    if (node.start === -1) {//💥💥💥💥💥 处理内部节点的子节点查找和路由
        //🔥内部节点：重新赋值
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        console.log(`   内部节点: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
        
        console.log(' 准备调用 _compareSuffixWithEdge');
        
        // 先检查方法是否存在
        console.log('_compareSuffixWithEdge 方法类型:', typeof this._compareSuffixWithEdge);
        console.log('🎯 _compareSuffixWithEdge 返回结果:', result);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        
        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);


        //let matchLength = this._compareSuffixWithEdge(suffixIndex, node);
        //显示当前内部节点的边标签
        console.log(`   内部节点: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`); 
        console.log(`   内部节点路由: 边="${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
        let nextChar = this.text[suffixIndex];// 使用原始位置的首字符
/*
💥nextChar 是下一个要用于路由的字符，它取决于当前匹配后的位置；在完全匹配当前边后，下一个用于选择子节点的字符，基于比较后的当前位置 current
文本: "bananasanaus"//nextChar 必须在字符比较之后，基于新的current位置计算
后缀5: "asanaus"
当前边: "ana" (内部节点边标签)
比较过程:
"asanaus" vs "ana"
   "a" = "a" → current=6
   "s" ≠ "n" → 停止比较
结果: 
matchLength=1, current=6
nextChar = this.text[6] = "s"
*/
        console.log(`   查找子节点: ${nextChar}`);
        console.log(`   可用子节点:`, Object.keys(node.children));
        // 🎯 调用封装的比较方法
        // 🎯 先比较字符！
        //let { current, matchLength } = this._compareSuffixWithEdge(suffixIndex, node);// 🚨 错误：重复声明
         /* ✅ 正确：赋值给已声明的变量
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);*/
        ({ current, matchLength } = this._compareSuffixWithEdge(suffixIndex, node));
        /*✅1.正确：解构但不声明（去掉 let）
💥关键：({ current, matchLength } = result) 这种语法表示"赋值给已存在的变量"，而不是声明新变量。这样既能在开头声明变量供后面使用，又能在内部节点中正确赋值！
        edgeLength = node.edgeEnd - node.edgeStart + 1;
        let edgeLength = node.edgeEnd - node.edgeStart + 1;
        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);*/
        /*
        ES6的解构赋值语法：相当于：一个方法调用同时返回两个相关的计算结果：代码更清晰简洁
        // 先调用方法获取结果对象
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        // 然后从对象中提取属性
        let current = result.current;
        let matchLength = result.matchLength;
        */
        if (matchLength > 0 && matchLength < edgeLength) {
                    //部分匹配 → 分裂//分裂：用于"共享前缀但后续分叉"的情况
                    //分裂操作内部处理了新叶子的创建，但需要为其他两种情况定义对应的添加方法！
                    this._splitNode(node, suffixIndex, matchLength);
        } else if (matchLength === edgeLength) {
                    // 完全匹配 → 继续路由
                    let nextChar = this.text[current];// 获取匹配后的下一个字符
                    if (node.children[nextChar]) {
                        // 🎯 情况A：有对应的子节点 → 继续递归
                        this._walkDown(current, node.children[nextChar]);///////
                    } else {
                        // 🎯 这里才是真正添加叶子的地方！
                        //完全匹配但无子节点 → 直接添加叶子 (_addLeaf)，不需要走分裂流程就不会有叶子
                        this._addLeaf(node, current);
                    }
                } 
        else {
               //🎯理论上不会发生，但作为错误检查：可以去掉，因为正常的算法流程不会进入这个分支，作为调试工具，发现算法错误，提高代码的健壮性
                console.error(`❌ 内部节点完全不匹配: 后缀"${this.text.substring(suffixIndex)}" vs 边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
                this._addNewBranch(node, suffixIndex);
            }
                return;
            }
         else {
        // 💥💥💥💥💥 叶子节点逻辑
        //🔥叶子节点：重新赋值
        let result = this._compareSuffixWithEdge(suffixIndex, node);
        current = result.current;
        matchLength = result.matchLength;
        edgeLength = node.end - node.start + 1;
        
        console.log(`叶子节点比较结果: matchLength=${matchLength}, current=${current}`);
        
        // 叶子节点决策逻辑...
        // 🎯 直接调用，不需要额外决策
        this._compareSuffixWithEdge(suffixIndex, node);
        // 比较方法内部会处理分裂或创建新分支
    }
/*edgeLength 是当前边的文本标签的长度：
情况1：完全匹配：完全匹配应该发生在后缀与边标签完全一致且没有剩余字符时
后缀11: "s"
遇到内部节点 [s] (边标签="s")
比较:
"s" vs "s"
完全匹配1个字符
matchLength = 1
edgeLength = 1  
current = 12 (text.length)→没有剩余字符
matchLength = edgeLength → 完全匹配
情况2：部分匹配
新后缀: "asanaus" (从位置5开始) 
边标签: "ana" (位置1-3)
比较:
"a"sanaus vs "a"na
只匹配1个字符
matchLength = 1  
edgeLength = 3（ana的长度）
matchLength < edgeLength → 部分匹配
内部节点的路由机制：根节点根据首字符路由到不同分支，如果首字符不匹配，根本不会进入这个内部节点；完全不匹配"更多发生在：根节点级别或者算法错误时
*/

        console.log(`比较结果: matchLength=${matchLength}, current=${current}`);
    /*    if (node.children[nextChar]) {
            console.log(` 路由到子节点: ${nextChar}`);
            let childNode = node.children[nextChar];
            // 🚨 关键：继续在子节点中进行字符比较，可能触发进一步分裂
            this._walkDown(current, childNode);//suffixIndex（原始后缀起始位置）*/
/*
💥注意参数的正确传递，如果递归调用比较方法，传入current而不是index
如果传入原始其实后缀位置会发生：                                            
处理后缀5: "asanaus"                                                    
遇到内部节点 [ana] (边标签="ana")                                        
当前逻辑：                                             正确逻辑：                 
1. 看到首字符'a'                                     //先比较 "asanaus" vs "ana"                 
2. 找到子节点键'a'存在                                //发现匹配1个字符 ("a")                 
3. 递归调用_walkDown(5,childNode) ←还是从位置5开始！   //当前指针走到位置6 (剩余 "sanaus")         
4. 在子节点中重新比较asanausvs子节点的边标签            //递归调用 _walkDown(6, childNode) ← 从已匹配位置继续！
关键原则：在 JavaScript 中，let 和 const 声明的变量有"暂时性死区"，在声明之前不能使用。把所有声明放在函数开头可以避免这个问题
_walkDown(suffixIndex, node) {
    if (某个条件) {
        this._walkDown(current, childNode) //🚨在声明之前使用//🚨问题：这里直接使用 current，但 current 还没有计算！
    } 
    let current = suffixIndex;
💥缺少了字符比较来计算current,要把current算出来就必须把比较的方法放在路由之前,如果比较放在路由之前就会爆红，所以需要用一个新的变量来点出比较方法，把比较方法封装到内部方法里面
[a] (内部节点)
  ├── [na] (内部节点) 
  │     ├── [nasanaus] (叶子)  // 后缀1: "ananasanaus" 的部分
  │     └── [sanaus] (叶子)  // 后缀3: "anasanaus" 的部分
  └── [s] anaus (叶子)        // 后缀5: "asanaus"
}
*/
       //🔁与内部节点边标签比较
        //let matchLength = this._compareWithEdge(suffixIndex, node);
        //🎯避免重复代码：比较逻辑只写一次;解决死循环：方法调用不会造成循环依赖,调试清晰：比较过程有详细的日志,可复用：其他地方也可以使用这个比较方法
     /*   if (matchLength > 0 && matchLength < (node.edgeEnd - node.edgeStart + 1)) {
            //matchLength > 0，说明至少匹配了1个字符；node.edgeEnd - node.edgeStart + 1计算当前边的总长度；matchLength < 边长度：匹配的字符数 < 边的总长度，说明没有完全匹配整条边
            //如果匹配了至少1个字符，但没有匹配整条边
            //🔁情况一：如果部分匹配 → 分裂内部节点
            console.log(`   部分匹配 ${matchLength} 个字符，分裂内部节点`);
            this._splitNode(node, suffixIndex, matchLength);
            //分裂后不需要重新写指针关系：分裂逻辑 _splitNode 内部已经处理了指针关系
            return;
        } else if (matchLength === (node.edgeEnd - node.edgeStart + 1)) {
            //情况二：如果完全匹配 → 路由到子节点
            console.log(`   完全匹配，路由到子节点`);
            let nextChar = this.text[suffixIndex + matchLength];
            if (node.children[nextChar]) {
                this._walkDown(suffixIndex + matchLength, node.children[nextChar]);
            } */
           //=======================
        /*  if (node.children[nextChar]) {
             //直接路由
            }else {
                /*
                它假设：在内部节点中，如果根据首字符找不到子节点，就直接添加新叶子
                let nextChar = this.text[suffixIndex]; // 使用原始位置的首字符
                    if (node.children[nextChar]) {   
                        // 路由到子节点
                    } else {
                        // 🚨错误：直接添加新叶子
                        // 这跳过了必要的字符比较！
                    }
                        1. 取首字符 'a'
                        2. 查找 node.children['a'] 
                        3. 没找到 → 直接添加叶子 [asanaus]
                        4. 🚨 跳过了比较和分裂！
                */
          /*  console.log(`   叶子节点处理...`);
               //情况三：如果完全不匹配 → 添加新叶子
               console.log(`    添加新叶子到内部节点: ${nextChar}`);
                // 创建新叶子节点
                    let leaf = new SuffixTreeNode();
                    leaf.start = suffixIndex;
                    leaf.end = this.text.length - 1;
                    leaf.edgeStart = suffixIndex;
                    leaf.edgeEnd = this.text.length - 1;
                    // 添加到内部节点的子节点中
                    node.children[nextChar] = leaf;
                }
                return;
            }
            */
/*
💥叶子节点没有进入这个路由分支！叶子节点直接执行后面的通用比较逻辑，所以能正常分裂  
💥架构设计：
内部节点：走路由逻辑（快速查找）
合理的性能优化！内部节点通过路由快速定位到可能匹配的分支，叶子节点再进行详细的字符比较和分裂。叶子节点：走比较分裂逻辑（精细处理）
问题不在于架构设计，而在于内部节点路由逻辑中的索引计算错误
💥后缀树需要更精细的字符比较模型
💥内部节点应该先比较，再决策，而不是基于首字符直接路由

*/
//===========比较逻辑==========//
// 在通用比较逻辑开始前添加：
/*console.log(`🔍 通用比较调试:`);
console.log(`   节点类型: ${node.start === -1 ? '内部节点' : '叶子节点'}`);
console.log(`   节点edgeStart: ${node.edgeStart}, edgeEnd: ${node.edgeEnd}`);
console.log(`   边标签: "${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
console.log(`   后缀: "${this.text.substring(suffixIndex)}"`);
console.log(`   比较范围: 后缀位置${suffixIndex} vs 边位置${node.edgeStart}到${node.edgeEnd}`);
//🔥沿着树的边逐字符比较，找到新后缀的插入位置：后缀树匹配和分裂的核心逻辑
//1.字符比较
while (current < this.text.length && edgePos <= node.end) {
        if (this.text[current] !== this.text[edgePos]) {
            console.log(`    不匹配: 位置${current}('${this.text[current]}') ≠ 位置${edgePos}('${this.text[edgePos]}')`);
            break;
        }
        console.log(`    匹配: 位置${current}('${this.text[current]}') = 位置${edgePos}('${this.text[edgePos]}')`);
        current++;
        edgePos++;
    }
//第2步：计算匹配结果
//决策的关键！它计算了两个重要长度，用来决定接下来该做什么
let matchLength = current - suffixIndex;//matchLength - 已匹配的长度
let edgeLength = node.edgeEnd - node.edgeStart + 1;//✅使用edgeStart/edgeEnd//edgeLength-当前边的总长度
console.log(`  匹配结果: matchLength=${matchLength}, edgeLength=${edgeLength}`);
/*
🔥当前边 = 从父节点到当前节点的路径上的文本标签
插入后缀3: "anasanaus"
假设当前有边: "ananasanaus" (start=1, end=11)
_walkDown(3, node) {
    node.start=1, node.end=11
    当前边 = text[1..11] = "ananasanaus"
    比较:
    新后缀: a n a s a n a u s  (从位置3开始)
    当前边: a n a n a s a n a u s  (从位置1开始)//当前边就是从父节点到当前节点的路径上显示的那个文本标签
         ✅✅✅ ❌
        current = 6   匹配结束位置（不匹配发生在位置6）
        suffixIndex = 3
        matchLength = 6 - 3 = 3  匹配了3个字符"ana"
        node.start=1, node.end=11  
        edgeLength = 11 - 1 + 1 = 11当前边总长度11个字符
        决策: 3 < 11 → 部分匹配，需要分裂
}
🔥当前节点：node（树中已存在的节点，我们正在与它比较），比较过程：把新后缀与当前节点的边标签逐个字符比较，新的后缀：text[suffixIndex..]（我们正在尝试插入的内容）
*/
//第3步：三种情况处理
/*if (matchLength === edgeLength) {
        // 情况1: 完全匹配当前边，继续向下
/*
🔥完全匹配 = 新后缀与当前边的标签完全匹配，但新后缀还有剩余字符：
在 "anana" 匹配 "ana" 的情况下：current =3开始：比较结束后:current = 6，this.text.length = 6，if (current < this.text.length) → 6 < 6 → false，所以不会进入 if 分支，直接结束
文本：banana：当前边: "ana" (node.start=3, end=5)  新后缀: "ana" (suffixIndex=3)//部分匹配，不是完全匹配
🔥"完全匹配"有两种情况：
情况1：真正完全匹配（结束）：
当前边: "ana"
新后缀: "ana"
结果: 完全匹配，没有剩余，结束
情况2：前缀匹配（继续向下）：
当前边: "ana" (内部节点)
新后缀: "anana" 
结果: 完全匹配当前边，但还有剩余"na"，继续向下
🎯"完全匹配+继续向下"只发生在：🎯当前节点是内部节点（有子节点），🎯新后缀比当前边长（有剩余字符）
叶子节点的情况（无法继续向下）：
[anana] (叶子)
↑
完全匹配，结束！
内部节点的情况（可以继续向下）：结构要求：只有内部节点才有子节点可以"继续向下"，逻辑要求：如果当前节点是叶子，完全匹配就意味着后缀已存在，应该结束
[ana] (内部节点)//算法要求：后缀树的压缩特性要求共享前缀必须是内部节点//天然地要求当前节点必须是内部节点
├── [na] (叶子)
└── [s]  (叶子)
↑
完全匹配"ana"，继续在子节点中匹配剩余"na"
 */
/*      console.log(`完全匹配，继续向下`);
        if (current < this.text.length) {
            let nextChar = this.text[current];
            if (node.children[nextChar]) {
                this._walkDown(current, node.children[nextChar]);
            } else {
                console.log(` 添加新叶子，字符: ${nextChar}`);
                let leaf = new SuffixTreeNode();
                leaf.start = current;
                leaf.end = this.text.length - 1;
                node.children[nextChar] = leaf;
            }
        }
    } 
else if (matchLength > 0) {
        // 情况2: 部分匹配，需要分裂
        console.log(`部分匹配，需要分裂`);
        this._splitNode(node, suffixIndex, matchLength);
} else {
        // 情况3: 首字符匹配但matchLength=0（不应该发生）
        console.error(`    错误: 首字符匹配但matchLength=0`);
        console.error(`     后缀: "${this.text.substring(suffixIndex)}"`);
        console.error(`     边: "${this.text.substring(node.start, node.end + 1)}"`);
    }
    //🎯只有叶子节点才进行字符比较和分裂
    console.log(`   _walkDown: 后缀${suffixIndex}="${this.text.substring(suffixIndex)}", 边="${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
*/
// 在方法结束时减少深度
this.recursionDepth--;



}
// 需要添加这个方法，在已有路径完全匹配后添加叶子
_addLeaf(parentNode, startPos) {
    let leaf = new SuffixTreeNode();
    leaf.start = startPos;// 叶子节点在文本中的起始位置
    leaf.end = this.text.length - 1;// 叶子节点在文本中的结束位置
    leaf.edgeStart = startPos; // 边的起始位置（与start相同）//🎯
    leaf.edgeEnd = this.text.length - 1;// 边的结束位置//🎯
    leaf.parent = parentNode;  // 🎯 设置父指针：第二步：在所有创建节点的地方设置父指针
    let nextChar = this.text[startPos]; // 获取用于路由的字符
    if (!parentNode.children) parentNode.children = {};// 确保children对象存在
    parentNode.children[nextChar] = leaf; // 将叶子挂载到父节点
    
    console.log(` 添加新叶子: ${this.text.substring(startPos)}`);
}
_addNewBranch(parentNode, suffixIndex) {//在完全不匹配时创建全新分支
    console.log(` 创建新分支: ${this.text.substring(suffixIndex)}`);
    let leaf = new SuffixTreeNode();
    leaf.start = suffixIndex;
    leaf.end = this.text.length - 1;//🎯
    leaf.edgeStart = suffixIndex;//🎯
    leaf.edgeEnd = this.text.length - 1;
    leaf.parent = parentNode;  // 🎯 设置父指针：第二步：在所有创建节点的地方设置父指针
    let nextChar = this.text[suffixIndex];
    if (!parentNode.children) parentNode.children = {};
    parentNode.children[nextChar] = leaf;
    
    console.log(` 新分支创建完成: ${nextChar} -> ${this.text.substring(suffixIndex)}`);
}

debugSplit(node, suffixIndex, matchLength) {
    console.log(`🔧 分裂调试:`);
    console.log(`   插入后缀: "${this.text.substring(suffixIndex)}" (start=${suffixIndex})`);
    console.log(`   匹配节点: "${this.text.substring(node.start, node.end + 1)}" (start=${node.start}, end=${node.end})`);
    console.log(`   匹配长度: ${matchLength}`);
    console.log(`   分裂位置: ${node.start + matchLength}`);
    
    // 检查分裂前的父节点
    let parentBefore = this._findParent(node);
    console.log(`   分裂前父节点:`, parentBefore ? this.text.substring(parentBefore.start, parentBefore.end + 1) : '无');
        
     //3.🎯完整的字符比较逻辑
    //第1步：字符比较：逐个字符比较新后缀和当前边的标签
    //字符比较是后缀树的核心精髓！它解决了后缀树最关键的问题：如何发现和利用重复模式。1. 发现共享前缀2. 支持高效搜索3. 构建压缩树结构：字符比较让后缀树从朴素Trie变成压缩Trie
    //空间效率：共享前缀只存储一次，时间效率：搜索时快速定位，结构清晰：自然形成层次结构
    //字符比较不是可选的，而是后缀树存在的理由！它让后缀树从O(n²)的朴素结构变成了O(n)的压缩结构🎯
    
}
//比较逻辑：
/*_compareSuffixWithEdge(suffixIndex, node){
    
    // 🎯 确定比较的起始位置
    let current = suffixIndex;
    let edgePos;
    if (node.start === -1) {
        // 内部节点：用 edgeStart
        edgePos = node.edgeStart;
        console.log(`   比较: 后缀"${this.text.substring(suffixIndex)}" vs 内部节点边"${this.text.substring(node.edgeStart, node.edgeEnd + 1)}"`);
    } else {
        // 叶子节点：用 start  
        edgePos = node.start;
        console.log(`   比较: 后缀"${this.text.substring(suffixIndex)}" vs 叶子节点边"${this.text.substring(node.start, node.end + 1)}"`);
    }
    
    let matchLength = 0;
    
    // 🎯 确定比较的边界
    let edgeEnd;
    if (node.start === -1) {
        edgeEnd = node.edgeEnd;
    } else {
        edgeEnd = node.end;
    }
    
    // 字符比较
    while (current < this.text.length && edgePos <= edgeEnd) {
        if (this.text[current] !== this.text[edgePos]) {
            console.log(`    不匹配: 位置${current}('${this.text[current]}') ≠ 位置${edgePos}('${this.text[edgePos]}')`);
            break;
        }
        console.log(`    匹配: 位置${current}('${this.text[current]}') = 位置${edgePos}('${this.text[edgePos]}')`);
        current++;
        edgePos++;
        matchLength++;
    }
    
    console.log(`   匹配长度: ${matchLength}`);
    return matchLength;
}*/
//==============分裂逻辑============//
//分裂逻辑 _splitNode 只能处理叶子节点 → 内部节点的分裂，但不能处理内部节点 → 更深内部节点的分裂！
/*
当前的 _splitNode 假设：叶子节点 → 内部节点 + 叶子节点
但我们需要支持：内部节点 → 更深内部节点 + 叶子节点
*/
_splitInternalNode(node, suffixIndex, matchLength) {
    console.log('🎯 开始内部节点分裂');
    
    // 1. 保存原内部节点的信息
    let originalEdgeStart = node.edgeStart;
    let originalEdgeEnd = node.edgeEnd;
    let originalChildren = {...node.children};
    
    console.log('原内部节点:', this.text.substring(originalEdgeStart, originalEdgeEnd + 1));
    console.log('原子节点:', Object.keys(originalChildren));

    // 2. 创建 [na] 内部节点（继承原子节点）
    let naNode = new SuffixTreeNode();
    naNode.start = -1;
    naNode.end = -1;
    naNode.edgeStart = originalEdgeStart + matchLength;  // "na" 开始位置
    naNode.edgeEnd = originalEdgeEnd;                    // "na" 结束位置  
    naNode.children = originalChildren;                  // 继承所有子节点

    console.log('[na] 节点:', this.text.substring(naNode.edgeStart, naNode.edgeEnd + 1));

    // 3. 创建新叶子节点 [s]anaus (后缀5)
    let newLeaf = new SuffixTreeNode();
    newLeaf.start = suffixIndex + matchLength;           // "sanaus" 开始位置
    newLeaf.end = this.text.length - 1;
    newLeaf.edgeStart = suffixIndex + matchLength;
    newLeaf.edgeEnd = this.text.length - 1;

    console.log('新叶子:', this.text.substring(newLeaf.start, newLeaf.end + 1));

    // 4. 调整原节点为 [a]
    node.edgeEnd = originalEdgeStart + matchLength - 1;  // 只保留 "a"

    // 5. 设置子节点
    let naChar = this.text[naNode.edgeStart];            // "n"
    let newLeafChar = this.text[newLeaf.edgeStart];      // "s"

    node.children = {
        [naChar]: naNode,
        [newLeafChar]: newLeaf
    };

    console.log('✅ 内部节点分裂完成');
    console.log('新结构:');
    console.log('  [', this.text.substring(node.edgeStart, node.edgeEnd + 1), ']');
    console.log('    ├── [', this.text.substring(naNode.edgeStart, naNode.edgeEnd + 1), ']');
    console.log('    └── [', this.text.substring(newLeaf.start, newLeaf.end + 1), ']');
}
_splitNode(node, suffixIndex, matchLength) {
    /*console.log('🔍 === 分裂调用分析 ===');
    console.log('调用来源:', new Error().stack.split('\n')[2]);
    console.log('节点类型:', node.start === -1 ? '内部节点' : '叶子节点');
    console.log('节点边:', this.text.substring(node.edgeStart, node.edgeEnd + 1));
    console.log('匹配长度:', matchLength);*/
     //🚨严格检查：如果原节点身份已经是 -1，说明之前就有问题
     //💥💥💥💥💥💥删除这个报错检查！改为：根据节点类型选择分裂策略💡设计理念：后缀树应该支持无限深度的内部节点分裂：
    /*if (node.start === -1) {
        console.error(`❌ 严重错误: 分裂的节点身份已经是 -1!`);
        console.error(`   节点: ${this.text.substring(node.edgeStart, node.edgeEnd + 1)}`);
        console.error(`   正在插入: ${suffixIndex}`);
        console.trace();
        return; // 或者尝试修复
        }*/
//💥支持更深的内部节点分裂
    if (node.start === -1) {
        console.log('🔁处理内部节点的进一步分裂');
    //💥💥💥💥💥💥内部节点分裂的特殊逻辑：我们需要让分裂逻辑支持内部节点的递归分裂！
        return this._splitInternalNode(node, suffixIndex, matchLength);
    } else {
        console.log('🍃处理叶子节点分裂');
    // 🎯 确保这里有这行：
    let originalIdentity = node.start;  // 🚨 这行必须存在！
    // 🎯 删除这个干扰性检查！
    // 🎯 特别监控对根节点下 'a' 节点的修改
    if (node === this.root.children['a']) {
        console.error(`🚨 警告: 正在修改根节点的 'a' 节点!`);
        console.error(`   当前: start=${node.start}, 正在改为: -1`);
        console.trace();  // 打印调用栈
        }
  /*  this.debugSplit(node, suffixIndex, matchLength);
    //node - 当前需要分裂的节点（匹配发生在这个节点上）/matchLength 就是共同前缀的长度，它决定了在哪里分裂节点
    //🔥suffixIndex -后缀的原始身份标识，正在插入的后缀的起始位置：这个值在整个插入过程中保持不变//suffixIndex就是后缀的身份证号码，永远不变
    console.log(` _splitNode: 分裂节点[${this.text.substring(node.start, node.end + 1)}], suffixIndex=${suffixIndex}, matchLength=${matchLength}`);
    /*node定义：
    // - 这是一个现有的节点，我们正在尝试将新后缀插入到它的路径下
    // - 它可能是叶子节点或内部节点
    // - 它的 start/end 定义了这条边的文本范围
    // - 新后缀与这个节点的边部分匹配（匹配了matchLength个字符）：
    比如文本: "bananasanaus"
    正在插入: "anasanaus" (suffixIndex=3)
    node: 代表 "ananasanaus" (start=1, end=11)
    matchLength: 3 (匹配了 "ana")*/


    /*1.创建内部节点
    let internalNode = new SuffixTreeNode();
    internalNode.start = -1;
    🚨内部节点无身份：内部节点不应该有具体的后缀身份，内部节点代表共享前缀，不属于任何一个具体的后缀，如果内部节点有身份，会造成语义混乱
    internalNode.edgeStart = node.edgeStart;     
    internalNode.edgeEnd = node.edgeStart + matchLength - 1;
    */
    //🎯matchLength当前插入的后缀与现有边已经匹配的字符数量的作用：确定内部节点的范围，确定原节点的调整，🟢确定新叶子的位置：新叶子代表我们正在插入的后缀的剩余部分
    //🎯但注意：新叶子的 start 是原始后缀位置，不是匹配后的位置！
    /* 
    🚨原节点保持原来的 start！但边的标签应该同时被改变!
    ⏹️node.start 保持不变！仍然是start=1:原节点如果不改变直接作为字节点的话，它的start确实保持了初始值，但是它的内容还是start标志的位置开始，内容没有变！
    原节点现在在内部节点下面，应该代表的是后缀的剩余部分
    ⏹️调整原节点的位置，但保持其标识
    ana (内, start=1, end=3)        ← 新建的内部节点
        └── [ananasanaus] (start=1, end=11)←🚨原节点保持不变！但这样边标签还是 "ananasanaus"，不对！
    原节点保持 start=1（身份不变），但显示为 "nasanaus"（内容改变）：这实际上是不可能的，因为在一个节点中，start 既表示身份又决定边标签
    🔧1.需要创建新节点，而不是修改原节点：⚠️根本矛盾：一个节点无法同时满足：start 值作为永恒的身份标识，start/end 准确描述边的文本内容
    🔧2.此时引入新的变量用来记录原始文本的start值，内容依旧加上长度计算防止矛盾，记录原始的start和内容改变分开⚠️但这样start可读性非常差   
    🔥3.完全放弃用start作为边标签，让start永远代表身份：让打印出来的 start 值就是初始的 start，让人能直观理解。用新的变量来表示内容的起始位置。
    🔧4.创建新的内部节点，创建新的叶子节点，创建新的剩余节点，直接丢弃原节点：⚠️原节点还存在于树中，如果丢弃会造成内存泄漏和结构混乱
    🔥5.重用原节点（实际做法）：我们不创建新的内部节点，而是直接把原节点改造成内部节点。
    */
   
    console.log(`🔧 分裂调试:`);
    console.log(`   插入后缀: "${this.text.substring(suffixIndex)}" (身份=${suffixIndex})`);
    console.log(`   匹配节点: "${this.text.substring(node.edgeStart, node.edgeEnd + 1)}" (身份=${node.start})`);
    console.log(`   匹配长度: ${matchLength}`);
    console.log('=== 分裂节点 ===');
    console.log('原节点:', {
        start: node.start, 
        end: node.end,
        edgeStart: node.edgeStart, 
        edgeEnd: node.edgeEnd,
        edgeLabel: this.text.substring(node.edgeStart, node.edgeEnd + 1)
    });
    console.log('🔥 === 分裂终极调试 ===');
    console.log('🔥 节点身份:', node.start, node.end, node.edgeStart, node.edgeEnd);
    console.log('🔥 节点类型:', node.start === -1 ? '内部节点' : '叶子节点');
    console.log('🔥 边标签:', this.text.substring(node.edgeStart, node.edgeEnd + 1));
    console.log('🔥 匹配长度:', matchLength);
    console.log('🔥 正在插入的后缀:', this.text.substring(suffixIndex));
    //1.🔥第一步：直接改造原节点为内部节点：保存原节点的信息（在修改前）
    //💥💥💥💥💥你把叶子节点改造成了内部节点，但忘记调整它的边标签边界！
    let originalStart = node.start;// 保存原身份（后面要用）
    let originalEnd = node.end;// 保存原边标签结束
    let originalEdgeStart = node.edgeStart;  //保存原边标签起始
    

    let originalChildren = {...node.children};// 保存原子节点
    console.log(`   end值跟踪: 原节点end=${originalEnd}`);
    // 🚨不创建新的内部节点！直接改造原节点
    // 原节点现在变成共享前缀的内部节点
    /*🔥立即改造原节点：在分裂时过早地把节点标记为内部节点（设置 start=-1），
    /但这时候原节点可能还不是内部节点（可能还是叶子）设置start=-1 后，就丢失了原始身份信息；后续操作都基于这个错误的-1值
    解决方案：推迟身份清除：不要在分裂开始时就把 start 设为 -1，而是最后一步才设置 -1
    */
    // 🎯 第二步：创建两个新节点
    //2.1🔥创建代表原节点剩余部分的新节点（代表原节点的剩余部分）使用保存的原始值计算：总是使用保存的原始值来计算，避免依赖可能被修改的节点属性
    
    let remainingNode = new SuffixTreeNode();
    remainingNode.start = node.start;//1.🚨继承原身份
    remainingNode.end = originalEnd;// 🚨 必须设置
    //remainingNode.edgeStart = node.edgeStart + matchLength;//剩余节点内容的起始值 
    remainingNode.edgeStart = originalStart + matchLength;//2.需要原结束位置，originalStart时机安全：使用保存的原始值，不受后续修改影响，语义清晰：明确表示"基于原始起始位置计算"，避免混淆：不依赖可能被修改的 node.edgeStart
    remainingNode.edgeEnd = originalEnd;//3.直接使用保存的值 
    remainingNode.children = originalChildren;//🎯4.如果原内部节点有子节点，分裂后，这些子节点应该转移到剩余节点下面//继承原子节点
    
    remainingNode.parent = node;  // 🎯 设置父指针
    console.log(`  end值跟踪: 剩余节点end=${remainingNode.end}`);

    //2.2🔥新叶子必须记录原始后缀位置，创建新叶子（代表正在插入的后缀）
    let newLeaf = new SuffixTreeNode();
    newLeaf.start = suffixIndex;//很重要🎯
    newLeaf.end = this.text.length - 1;  // 🚨 必须设置！
    console.log(`   创建新叶子前: start=${newLeaf.start}`);
    newLeaf.edgeStart = suffixIndex + matchLength;
    newLeaf.edgeEnd = this.text.length - 1;

    newLeaf.parent = node;  // 🎯 设置父指针
    console.log(`   创建新叶子后: start=${newLeaf.start}`);
    console.log(`    end值跟踪: 新叶子end=${newLeaf.end}`);
    //newLeaf.end = this.text.length - 1;//叶子节点总是延伸到文本末尾文本："bananasanaus" (长度=12)

                                 
    
    //🎯先完全初始化节点，再使用它们🚀在对象字面量中使用变量前，确保该变量已经完全初始化！
    let remainingChar = this.text[remainingNode.edgeStart];  // ✅ 安全
    let newLeafChar = this.text[newLeaf.edgeStart];         // ✅ 安全
    //🎯添加身份传递检查
    console.log(`   🎯 身份传递: 原节点身份=${originalIdentity} → 剩余节点身份=${remainingNode.start}`);  
    //🎯第三步：最后才设置原节点为内部节点
    node.start = -1;//内部节点无身份🚨最后一步！//
    node.edgeStart = originalEdgeStart;                   // 边标签起始：1
    node.edgeEnd = originalEdgeStart + matchLength - 1;       // 边标签结束：3  
    //💥originalEdgeStart：🎯 虽然结果相同，但逻辑意义不同！originalEdgeStart：明确表示边的起始位置，originalStart：节点的身份标识，可能在其他情况下不同
    //node.children = {};// 先清空，稍后添加子节点 
    node.children = {
        [remainingChar]: remainingNode,
        [newLeafChar]: newLeaf
    }; 


    //🎯修正后的调试输出
    console.log(`   改造结果:`);
    console.log(`     - 原节点 → [${this.text.substring(node.edgeStart, node.edgeEnd + 1)}] (内部节点, start=${node.start})`);
    console.log(`     - 剩余节点 → [${this.text.substring(remainingNode.edgeStart, remainingNode.edgeEnd + 1)}] (身份=${remainingNode.start})`);
    console.log(`     - 新叶子 → [${this.text.substring(newLeaf.edgeStart, newLeaf.edgeEnd + 1)}] (身份=${newLeaf.start})`);
    console.log(`   子节点键: '${this.text[remainingNode.edgeStart]}' → 剩余节点, '${this.text[newLeaf.edgeStart]}' → 新叶子`);

    // 在 _splitNode 最后添加
    console.log(`    分裂后验证:`);
    console.log(`      原节点: [${this.text.substring(node.edgeStart, node.edgeEnd + 1)}] (start=${node.start}, end=${node.end})`);
    console.log(`      剩余节点: [${this.text.substring(remainingNode.edgeStart, remainingNode.edgeEnd + 1)}] (start=${remainingNode.start}, end=${remainingNode.end})`);
    console.log(`      新叶子: [${this.text.substring(newLeaf.edgeStart, newLeaf.edgeEnd + 1)}] (start=${newLeaf.start}, end=${newLeaf.end})`);

    /*console.log(`   内部节点: [${this.text.substring(internalNode.start, internalNode.end + 1)}]`);
    console.log(`   原节点调整: [${this.text.substring(node.start, node.end + 1)}]`);
    console.log(`   新叶子: start=${newLeaf.start}, 代表 "${this.text.substring(newLeaf.start)}"`);*/
    //3.更新节点间的父子关系/重新连接节点关系
        /*
        之前：父节点
        └── node (原节点)
        之后：父节点
        └── internalNode (新建的内部节点)
            ├── node (调整后的原节点)
            └── newLeaf (新叶子)
        
    🔥：重用原节点的最大优势：不需要更新任何父节点引用
    如果直接改变原节点为内部节点就不需要重新维护指针关系，我们只是改变了原节点里面的状态：
    原节点对象没变：还是同一个内存对象//父节点的引用没变：父节点仍然指向同一个对象
           */
    /* 1. 找到原节点的父节点
    let parent = this._findParent(node);//可能 _findParent没有找到正确的父节点，导致节点关系混乱！
    // 2. 获取内部节点的首字符（用于在父节点的children中定位）
    let firstChar = this.text[internalNode.start];
    // 3. 将父节点指向原节点的链接改为指向新内部节点// 现在：parent → internalNode（而不是原来的 node）
    if (parent) {
        parent.children[firstChar] = internalNode;
    }
    // 4. 将原节点和新叶子作为内部节点的子节点
    internalNode.children[this.text[node.start]] = node;
    internalNode.children[this.text[newLeaf.start]] = newLeaf;*/
    console.log(`   分裂位置分析:`);
    console.log(`     匹配长度: ${matchLength}`);
    console.log(`     应该分裂在: 共享前缀 "${this.text.substring(node.edgeStart, node.edgeStart + matchLength)}"`);
    console.log(`   重组完成`);}


}
_findParent(node){
    //使用广度优先搜索 (BFS) 来寻找父节点
    console.log(`  寻找节点 [${this.text.substring(node.start, node.end + 1)}] 的父节点`);
    let queue = [this.root];//1.从根节点开始
    //🚨这里不是"根节点是队列"，而是创建一个队列，初始时包含根节点
    /*广度优先BFS 确保：先检查高层级节点（更可能是父节点），不会错过任何节点，找到的父节点是最近的：根 → 子节点A → 子节点B → 子节点C → 孙节点A1...
    深度优先 (DFS)：根 → 子节点A → 孙节点A1 → 曾孙节点A1a...
    */
    while (queue.length > 0) {
        let current = queue.shift();// 取出队列第一个节点//从队列的头部取出第一个元素，确保我们按"层级顺序"遍历树
        // 检查current的所有子节点
        for (let [char, child] of Object.entries(current.children)) {
            //Object.entries() 的作用：将对象转换为键值对数组；
            /*{'a': { start:1, end:3,children: {...} 
               'char':{child}
            },  子节点A*/
            console.log(`    检查: ${char} -> [${this.text.substring(child.start, child.end + 1)}]`);
            if (child === node) {// 找到目标节点的父节点
                console.log(` 找到父节点`);
                return current;
            }
            queue.push(child);// 将子节点加入队列继续搜索
        }
    }
    console.log(`  未找到父节点`);
    return null;
}
//第三步：添加路径显示方法
_getNodePath(node) {
    if (!node || node === this.root) return "根";
    
    let path = [];
    let current = node;
    
    while (current && current !== this.root) {
        if (current.start !== -1) {
            // 🎯 叶子节点：显示实际后缀
            path.unshift(`[${this.text.substring(current.start, current.end + 1)}]`);
        } else {
            // 🎯 内部节点：显示边标签
            path.unshift(`[${this.text.substring(current.edgeStart, current.edgeEnd + 1)}]`);
        }
        
        if (current.parent) {
            current = current.parent;
        } else {
            break;
        }
    }
    
    return "根 → " + path.join(' → ');
}
search(pattern) {
    //✅后缀树搜索:是否存在，所有出现位置，精确匹配（不是模糊匹配）
    //✅关键特性：找所有位置：不只是第一个出现的位置；精确子串：必须是连续字符序列；O(m)速度：搜索时间只与模式串长度有关，与文本大小无关
    //✅在后缀树中搜索模式串，会返回该模式串在文本中所有出现的起始位置列表"；不仅仅是"显示内容"，而是精确定位所有出现位置！
    let currentNode = this.root;
    let patternIndex = 0;
    //1.外层循环 - 控制模式串进度
    while (patternIndex < pattern.length) {//只要模式串还有字符没匹配完，就继续
        //2. 选择分支
        let currentChar = pattern[patternIndex];
        if (!currentNode.children[currentChar]) return [];//根据当前要匹配的字符，选择树上的对应分支。如果没有这个分支，说明模式串不存在"
        //3. 获取边上文本
        let child = currentNode.children[currentChar];
        let edgeText = this.text.substring(child.start, child.end + 1);
        //4. 内层循环 - 匹配边上字符
        for (let i = 0; i < edgeText.length && patternIndex < pattern.length; i++) {
            if (edgeText[i] !== pattern[patternIndex]) return [];//逐个字符比较边上文本与模式串的剩余部分。如果发现不匹配，立即返回失败
            patternIndex++;
        }
        currentNode = child;//5.移动到下一节点
    }
    
    return this._collectLeafIndices(currentNode);

/*-------⚠️注意--------
🔧在文本 "bananasanaus" 中："ana" 应该出现在位置1,3但结果出现了位置8，这说明在分裂操作或叶子节点收集时：某些叶子节点的start值设置错误，或者搜索时匹配过度，包含了不应该匹配的路径
🔧叶子节点标识错误 - start 值设置逻辑有系统性偏差🔧导致重复和缺失 - 但不影响树的结构正确性
🔗 新叶子节点应该代表"正在插入的完整后缀"：插入后缀8 "naus"
理解1：代表"匹配后的剩余部分"：后缀8:n a u s：❌错误方式：后缀8和后缀10都创建 start=10 的叶子
                                | | | |
                                匹配 剩余
                               "na" "us"
                        新叶子代表："us" → start=10
理解2：代表"正在插入的完整后缀"：✅正确方式：后缀8创建 start=8，后缀10创建 start=10
后缀8: "n a u s"
        ↑
        完整后缀开始位置
新叶子代表："naus" → start=8
🔗新叶子节点永远代表：当前正在插入的完整后缀；不是剩余部分，不是片段，而是完整的原始后缀！
🔗搜索"ana":
1. 根节点 → 找键'a' → 找到内部节点
2. 内部节点边标签="ana" → 匹配成功!
3. 继续在内部节点下处理剩余部分
搜索"an":
1. 根节点 → 找键'a' → 找到内部节点  
2. 内部节点边标签="ana" → 匹配前2个字符"an"
3. 部分匹配，需要分裂 
共享前缀 "ana" 的完整边标签就是 "ana"，在父节点的children中只用首字符 'a' 作为查找键，这是为了搜索效率，不是边被截断了 
*/
}
_collectLeafIndices(node) {//递归收集所有叶子节点的起始位置：找到某个节点下的所有叶子节点，并收集它们的start值
    let results = [];
    if (Object.keys(node.children).length === 0) {//1. 基本情况 - 叶子节点
        results.push(node.start);
    } else {//2. 递归情况 - 内部节点：如果这个节点有子节点，就递归处理每个子节点，把结果合并
        for (let child of Object.values(node.children)) {
            results = results.concat(this._collectLeafIndices(child));
        }
    }
    return results;
}
// 添加调试方法
debugLeafStarts() {
    console.log("=== 检查所有叶子节点的start值 ===");
    this._debugLeafStarts(this.root);
}

_debugLeafStarts(node, path = "") {
    if (Object.keys(node.children).length === 0) {
        let suffix = this.text.substring(node.start);
        console.log(`叶子: 路径=${path}, start=${node.start}, 后缀="${suffix}"`);
    } else {
        for (let [char, child] of Object.entries(node.children)) {
            let edgeText = this.text.substring(child.start, child.end + 1);
            this._debugLeafStarts(child, path + " → [" + edgeText + "]");
        }
    }
}
// 检查是否所有后缀都有对应的叶子节点
checkAllSuffixes() {
    console.log("=== 检查所有后缀是否都有叶子节点 ===");
    const n = this.text.length;
    let missing = [];
    
    for (let i = 0; i < n; i++) {
        let found = false;
        // 遍历所有叶子节点，检查是否有start=i的
        let queue = [this.root];
        while (queue.length > 0) {
            let node = queue.shift();
            if (Object.keys(node.children).length === 0) {
                if (node.start === i) {
                    found = true;
                    break;
                }
            } else {
                for (let child of Object.values(node.children)) {
                    queue.push(child);
                }
            }
        }
        
        if (!found) {
            missing.push(i);
            console.log(`缺失: start=${i}, 后缀="${this.text.substring(i)}"`);
        }
    }
    
    if (missing.length === 0) {
        console.log(" 所有后缀都有对应的叶子节点");
    } else {
        console.log(`总计缺失 ${missing.length} 个后缀`);
    }
}
}




/*测试
console.log("=== 测试 ===");
let tree = new SuffixTree("bananasanaus");
tree.debugStepByStep();*/

/* 测试搜索功能
function testSearch() {
    let tree = new SuffixTree("bananasanaus");
    
    // 构建树
    for (let i = 0; i < tree.text.length; i++) {
        tree._addSuffix(i);
    }
    console.log("=== 搜索测试 ===");
    // 基本测试
    console.log("'ana' 位置:", tree.search("ana"));    // 应该返回 [1, 3]
    console.log("'na' 位置:", tree.search("na"));      // 应该返回 [2, 4]  
    console.log("'us' 位置:", tree.search("us"));      // 应该返回 [10]
    console.log("'ban' 位置:", tree.search("ban"));    // 应该返回 [0]
    // 边界测试
    console.log("'xyz' 位置:", tree.search("xyz"));    // 应该返回 []
    console.log("'' 位置:", tree.search(""));          // 应该返回所有位置
    // 单个字符
    console.log("'a' 位置:", tree.search("a"));        // 应该返回 [1, 3, 7, 9]
    console.log("'n' 位置:", tree.search("n"));        // 应该返回 [2, 4, 8]
}

testSearch();

let tree = new SuffixTree("bananasanaus");
for (let i = 0; i < tree.text.length; i++) {
    tree._addSuffix(i);
}

tree.debugLeafStarts();
*/
console.log("=== 详细构建过程 ===");
console.log('=== 启动调试 ===');
console.log('SuffixTree 类:', typeof SuffixTree);
console.log('准备创建实例...');
let tree = new SuffixTree("bananasanaus");
console.log('实例:', tree);
console.log('根节点:', tree.root);
console.log('根节点start:', tree.root.start);
for (let i = 0; i < tree.text.length; i++) {
    console.log(`\n 步骤 ${i}: 插入后缀 "${tree.text.substring(i)}"`);
    tree._addSuffix(i);
    // 每步后检查叶子节点
    if (i < 5) { // 只看前几步，避免输出太多
        console.log("当前叶子节点:");
        tree._debugLeafStarts(tree.root);
    }
}
let tree1 = new SuffixTree("bananasanaus");
console.log('实例:', tree1);
console.log('根节点:', tree1.root);
console.log('根节点start:', tree1.root.start);
for (let i = 0; i < tree1.text.length; i++) {
    tree1._addSuffix(i);
}
tree1.checkAllSuffixes();
tree1.debugLeafStarts();

// 测试代码
let tree2 = new SuffixTree("bananasanaus");
console.log("创建树后根节点children:", Object.keys(tree2.root.children));  //🎯这里检查
/*
Uncaught ReferenceError: can't access lexical declaration 'tree2' before initialization:在 tree2 变量初始化之前就访问了它
*/
// 如果这里就已经有节点，说明构造函数有问题
// 如果这里是空的，但 debugStepByStep 开始时就有节点，说明 debugStepByStep 内部有问题
tree2.debugStepByStep();
```