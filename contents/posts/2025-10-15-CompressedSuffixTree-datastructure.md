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


- 边
```
不仅是结构连接的桥梁，更是智能文本载体： 通过索引存储实现空间优化；通过可变长度支持快速匹配；通过方向导航维护结构清晰
```

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






2. 代码实现
```
//----------调试版本-----------//
//节点定义与树结构
class SuffixTreeNode {//后缀树节点
    constructor() {
        //🟢节点不存储实际的字符串值，只存储 start 和 end 索引。实际的文本需要通过 T.substring(start, end+1) 计算得到。
        //🟢children 表建立了字符到子节点内存地址的映射；叶子节点的 children 通常为空对象 {}。
        //🟢节省了大量内存，所有节点都共享原始字符串 T，不需要重复存储字符串内容
        this.children = {};//子节点映射表；键：边的起始字符；值：子节点对象//节点不代表一个字符，而是代表一条边，这条边上可能存储着一个子串
        //children对象记录了从这个节点出发的所有出边。每条出边由一个起始字符（Key）和对应的子节点（Value）定义。
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
//--------优化版本----------//
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