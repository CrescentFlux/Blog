# Ukkonen's algorithm 
- 定义
```
Ukkonen's Algorithm 是一种用于在 O(n) 时间复杂度 和 O(n) 空间复杂度 下构建后缀树的 在线算法，由 Esko Ukkonen 于 1995 年提出。
关键创新：通过维护"活动点(active point)"和"后缀链接(suffix links)"，避免在每次添加新字符时重新构建整个树，从而将时间复杂度从 O(n²) 优化到 O(n)。
```
- 算法核心组件：活动点 (Active Point)，后缀链接 (Suffix Links)，全局结束位置 (Global End)
- Ukkonen算法基础实现
```
class SuffixTreeNode {//基础数据结构
    constructor() {
        this.children = {};      // 存储子节点 {char: node}//出边信息
        this.start = null;       // 边代表的子串起始索引//入边的起始
        this.end = null;         // 边代表的子串结束索引//入边的结束
        this.suffixLink = null;  // 后缀链接
    }
    //边的长度
    get length() {
        if (this.start === null || this.end === null) return 0;
        return this.end - this.start + 1;//边的长度 = 这个子串包含的字符数：判断活动点是否「超出」当前边
        /*
        🎯边的长度是连接抽象活动点与具体树结构的桥梁
        长度计算的更多用途： 分裂边时的精确定位，字符比较的范围控制，内存优化验证
        位置验证：确保活动点在边的物理范围内；状态校正：当活动点「飘移」时，能正确跳转到下一条边；分裂定位：精确定位在边上哪里需要分裂；算法正确性：保证整个状态机的一致性和正确性
        在后缀树的典型实现中，边通常不显式表示为对象，而是通过节点来隐含表示
        边本身不是对象，边的信息存储在子节点中
        🎯SuffixTreeNode类实际上表示的是边的终点节点，但包含了边的信息：每个节点存储了指向自己的边的信息
        🎯这种设计的优势：
        访问高效：直接通过节点访问边信息；内存紧凑：不需要额外的边对象，节点自然包含了必要的信息；算法简洁
        一种空间换时间的设计选择——通过让节点「多存储一点信息」，来避免维护复杂的边对象网络
        */
    }
}
class SuffixTree {
    constructor() {
        this.root = new SuffixTreeNode();
        this.text = '';
        
        //👉活动点三元组 (node, edge, length)//现在在哪，在做什么
        this.activeNode = this.root;//当前在哪个节点
        this.activeEdge = -1;
        /*当前在哪个边上（用字符索引表示）:activeEdge 是一个数字索引，指向原字符串中的位置
        activeEdge = 2  // 意思是：看字符串中第2个位置的字符,不是字符本身，而是字符在字符串中的位置
        用索引而不用字符:同一个字符可能出现在多个位置用索引能精确定位到具体是哪个'a',activeEdge告诉算法：从当前节点，找以这个字符开头的边
        活动点: (root, 2, 1)字符串: "aba$":表示在根节点 (root)找以 text[2] = 'a' 开头的边 ← 第2个字符是'a'！已经在这条边上走了1步
        */
        this.activeLength = 0;
        /*在当前边上走了多远,🎯activeLength = 1的真正含义:在当前边上，已经心理上走过了1个字符,activeLength 让算法能「预览」边的下一个字符，
        而不需要实际移动;
        activeLength 告诉算法在边的哪个位置分裂:
        边: "banana" [0,∞]
        活动点: (root, 0, 3)  // 走了3步,这意味着应该在 "ban" 后面分裂："ban" | "ana",activeLength = 3 → 在第3个字符后分裂
        */
        /*
        🔀分裂的时机:分裂发生在你要往一条边的中间插入新分支时,活动点告诉我们分裂位置，活动点是分裂的「导航系统」
        活动点 (node, edge, length) 精确回答了在哪分裂：node + text[edge] 找到要分裂的边，哪里分裂：length 告诉你在边上走多远后分裂
        */

        //👉全局变量
        this.remainingSuffixCount = 0;//任务计数器//待办清单，变量记录还有多少个后缀需要处理//本轮还需要扩展的后缀数量
        this.lastNewNode = null;//后缀链接的粘合剂// 记录上一个新创建的内部节点
        /*
        this.lastNewNode = null;这确保了后缀链接网络的连续性//作用：在创建新内部节点时，建立后缀链接：
        创建节点A时：lastNewNode = A
        创建节点B时：lastNewNode.suffixLink = B  // 建立链接！
        然后：lastNewNode = B
        */
        this.size = -1;}
/*包括特殊字符的字符串长度，全局结束指针，关键用途：与∞（无穷大）配合使用，动态计算到字符串末尾的长度，这样叶子节点的边可以自动延伸到字符串末尾
Ukkonen算法是一个复杂的状态机：需要记住当前位置（活动点），还有多少工作（剩余计数），网络关系（后缀链接），全局上下文（字符串大小）
*/
        /*
    Ukkonen算法的主循环，也是整个算法的驱动引擎
    */
    buildSuffixTree(text) {
        this.text = text + '$';//添加特殊字符,'$'结束符//添加特殊字符确保每个后缀有独立叶子
        this.size = this.text.length;
        console.log("开始构建，文本:", this.text, "长度:", this.size);
        //初始化活动点-算法的工作记忆
        this.activeNode = this.root;// 从根节点开始
        this.activeEdge = -1; //没有当前边
        this.activeLength = 0;//在当前边上走了0步
        this.remainingSuffixCount = 0;//没有待处理的后缀
        
        for (let i = 0; i < this.size; i++) {
            console.log(`\n=== 处理字符 ${i}: '${this.text[i]}' ===`);
            /* 主循环的作用:逐个字符处理整个字符串 
            驱动算法：按字符顺序推进处理
            增量构建：一个字符一个字符地完善后缀树
            状态维护：保持活动点和其他状态的连续性
            最终完成：处理完所有字符后得到完整后缀树
            */
           this.extendSuffixTree(i);  //✅在循环内调用，并传递i
        }
        //this.extendSuffixTree();  // 为位置i的字符扩展后缀树
         console.log("当前活动点:", {
            node: this.activeNode === this.root ? 'root' : 'other',
            edge: this.activeEdge,
            length: this.activeLength
        });
        return this.root;
}
    /*
    🎯在线增量
    1.在Ukkonen之前，后缀树算法（如McCreight算法）都是离线的:必须预先知道整个字符串,无法处理实时数据流,内存占用大（需要存储整个字符串）
    2.在线算法的需求场景:
    网络数据流(数据源源不断来，不能等全部到齐再处理,需要实时更新后缀树)
    大文件处理(文件太大，无法一次性加载到内存,需要增量处理每个数据块)
    实时搜索(用户边输入边搜索,需要在现有基础上扩展，不是重新构建)
    3.在线增量的核心优势:
    内存友好(离线算法：需要存储整个字符串 + 构建过程中的临时数据,在线算法：只需要维护当前状态)
    实时性(用户可以立即查询已处理部分,不用等到所有数据处理完)
    可中断性(可以随时停止，已有结果仍然有效,离线算法要么完成要么一无所有)
    McCreight算法：O(n)但离线 → 适用性有限;Ukkonen算法：O(n)且在线 → 真正实用！
    在线增量不仅是性能优化，更是思维范式的转变:从我有一个完整问题，如何解决它？变为：问题在不断变化，我如何持续解决它？这种思维在现代计算中至关重要:流数据处理,实时系统,交互式应用
    它让算法能够应对真实的、动态的、大规模的数据世界
    */
    // 扩展活动点
    walkDown(currentNode) {
        /*
        walkDown就是处理位置超出当前边范围的情况,确保我们在正确的起点开始工作
        walkDown函数是活动点的位置校正器:输入：可能「飘移」的活动点;处理：沿着树结构向下走，直到找到物理位置;输出：校正后的有效活动点
        没有这个校正，活动点就可能指向不存在的虚空位置，导致算法出错:它让算法能够在复杂的树结构中精确导航
        */
        const activeEdgeChar = this.text[this.activeEdge];//this.activeEdge 是一个数字索引，指向字符串中的某个位置，this.text[this.activeEdge] 得到那个位置的字符
        const child = currentNode.children[activeEdgeChar];//currentNode.children[activeEdgeChar] 在当前节点的子节点中找以这个字符开头的边
        
        if (!child) return false;//如果找不到对应的边，就返回失败
        /*
        walkDown操作的前提检查，确保后续的向下走操作是安全可行的
        索引转字符：把数字索引转换成对应的字符-查找子节点：在当前节点的子节点中找到对应的边-安全验证：确保活动点状态与树结构一致-错误预防：如果状态不一致，提前返回避免崩溃
        安全校验：
        验证活动点的有效性：确保activeEdge指向的边确实存在，
        防止空指针错误：如果边不存在，提前返回避免后续错误，
        状态一致性检查：发现活动点与树结构不一致时及时止损
        */
        
        // 如果活动长度大于当前边的长度，需要继续向下走
        if (this.activeLength >= child.length) {//处理「活动点跨越边界」的情况，校正活动点的位置，把它从虚空中拉回到真实的树结构上
            //需要向下移动一层
            this.activeNode = child;// 移动到子节点
            this.activeEdge += child.length;// 调整边索引
            this.activeLength -= child.length;// 调整剩余长度
            return true; 
/*return true表示我移动了活动点，可能需要继续walkDown，一次walkDown可能只能校正一层，如果新的活动点仍然超出范围，需要继续walkDown，
检测越界：活动长度是否超过当前边的物理长度，层级下移：移动到子节点，调整索引和长度，迭代校正：可能需多次下移直到位置正确，状态同步：让抽象的活动点与具体的树结构保持一致
*/
        }
        return false; // 表示活动点已在正确位置，不需要再移动
    }                                                                           
    // 添加后缀链接
    addSuffixLink(node) {
        console.log("🔗 尝试建立后缀链接:", {
            from: this.lastNewNode ? `节点[${this.lastNewNode.start},${this.lastNewNode.end}]` : 'null',
            to: `节点[${node.start},${node.end}]`
        });

        if (this.lastNewNode !== null) {
            this.lastNewNode.suffixLink = node;// 建立从上个节点到当前节点的链接
            console.log("建立后缀链接成功");
        }
        this.lastNewNode = node;// 记住当前节点，等待下一个节点来链接它
        /*后缀链接的记忆链：后缀链接建立了一个重要的关系：如果 节点A 代表字符串 "abc"，那么 节点A.suffixLink 指向代表 "bc" 的节点
        当我们创建节点A时，代表"bc"的节点可能还不存在：用 lastNewNode 建立了一个「延迟链接」机制，每个新节点都链接到下一个新创建的节点
        addSuffixLink 利用创建顺序自动建立正确的链接关系！后缀链接有这种时间顺序：先创建长字符串的节点（如 "abc"），后创建短字符串的节点（如 "bc"），长节点应该链接到短节点
        addSuffixLink 的智能：这个函数实际上在构建一个链式网络
        创建节点A → addSuffixLink(A)  // 记住A//这样就自动建立了：A → B → C 的链接链
        创建节点B → addSuffixLink(B)  // A.suffixLink = B，记住B  
        创建节点C → addSuffixLink(C)  // B.suffixLink = C，记住C
        */
    }
    
    //扩展阶段
/*扩展=把隐式后缀树从处理到位置i的状态，变成处理到位置i+1的状态;
    输入：S[1..i] 的隐式后缀树,输出：S[1..i+1] 的隐式后缀树,操作：为所有后缀添加字符 S[i+1]
    情况1：隐式扩展//现有路径：A -> B -> C,要加字符：'C'（已存在）,操作：什么都不做！路径自然包含
    情况2：简单扩展//现有路径：A -> B -> [叶子],要加字符：'C'（新字符）,操作：直接延长：A -> B -> C
    情况3：分裂扩展//现有路径：A -> B -> C -> D,要加字符：'X'（新分支）,：A -> B -> [新节点] -> C -> D
     -> X 
*/  
    extendSuffixTree(pos) {
/*
函数整体目标：为所有后缀添加新字符 this.text[pos]，输入：当前隐式后缀树（处理到pos-1），输出：新的隐式后缀树（处理到pos）//给现有的所有路径都延长一步
🎯pos参数是Ukkonen算法在线的、增量的核心体现,pos的具体作用:没有pos，算法就不知道我现在该做什么，就会退化成朴素算法
pos=0：处理字符 'a'知道我在处理第1个字符;pos=1：处理字符 'b'知道我在处理第2个字符;
确定要添加的字符const charToAdd = this.text[pos];  // 当前要处理的字符,确定新节点的起始位置
确定新节点的起始位置:leaf.start = pos;//新后缀从这个位置开始
指导扩展过程:// 检查字符是否匹配
if (this.text[next.start + this.activeLength] === this.text[pos]) {
    //这个字符已经存在了！
}
🎯进度标识：当前处理到哪个字符了🎯字符定位：要添加哪个新字符🎯节点定位：新后缀从哪里开始🎯状态推进：推动算法向前发展
*/       
    //添加参数检查
    if (pos === undefined) {
        console.error("❌ 错误: pos是undefined!");
        return;
    }
    console.log("🎬 extendSuffixTree开始:", {
        pos: pos,
        char: this.text[pos],
        activeNode: this.activeNode === this.root ? 'root' : 'other',
        activeEdge: this.activeEdge,
        activeLength: this.activeLength,
        remainingStart: this.remainingSuffixCount
    });
    // 先记录初始状态
    const initialState = {
        remainingStart: this.remainingSuffixCount,
        activePoint: `(${this.activeNode === this.root ? 'root' : 'node'}, ${this.activeEdge}, ${this.activeLength})`
    };
        //1.初始化阶段：
        this.lastNewNode = null;// 重置后缀链接记忆
        this.remainingSuffixCount++;// 新增一个待处理后缀，每个新字符都会产生一个新的后缀需要处理

    // 现在打印更新后的状态
    console.log("📊 更新后状态:", {
        ...initialState,
        remainingEnd: this.remainingSuffixCount,
        lastNewNode: this.lastNewNode ? `[${this.lastNewNode.start},${this.lastNewNode.end}]` : 'null'
    });
        //逐个处理后缀，直到全部完成
        while (this.remainingSuffixCount > 0) {
            if (this.activeLength === 0) {//活动长度为0的特殊处理，this.activeEdge = pos;//直接从新字符开始，如果活动点在节点上（不在边中间），就从当前新字符开始找路径
                this.activeEdge = pos
            }
            //情况判断——边是否存在，//从当前位置，有没有通往下一个字符的路
            const activeEdgeChar = this.text[this.activeEdge]; // 下一个字符是什么
            if (!this.activeNode.children[activeEdgeChar]) {
            // 情况2：需要创建新边 - 全新路径，直接创建叶子节点
            /*
            情况2在以下场景触发：全新后缀的第一个字符，全新分支的创建，叶子节点的扩展
            */
            const leaf = new SuffixTreeNode();//创建新叶子节点
            leaf.start = pos;           // 新后缀的开始位置
            leaf.end = Infinity;        // 使用∞表示延伸到字符串末尾
            console.log(`创建叶子节点: start=${pos}, end=Infinity, char=${this.text[pos]}`);
            //添加到树中：
            this.activeNode.children[activeEdgeChar] = leaf;//在活动节点下创建以activeEdgeChar开头的新边
            //更新状态：
            this.remainingSuffixCount--;//完成一个后缀的处理
            //维护后缀链接：
            // 如果上个循环创建了内部节点，建立后缀链接
            this.addSuffixLink(this.activeNode);

            } else {
                // 情况1或3
                console.log("🔀 进入情况1/3分支");
                const next = this.activeNode.children[activeEdgeChar];
                console.log("🔍 检查情况1:", {
                    checkPos: next.start + this.activeLength,
                    existingChar: this.text[next.start + this.activeLength],
                    newChar: this.text[pos],
                    isMatch: this.text[next.start + this.activeLength] === this.text[pos]
                });
                if (this.walkDown(next)) {
                    continue;
                }
                
                // 情况1：字符已存在
                if (this.text[next.start + this.activeLength] === this.text[pos]) {
                    console.log("🎯情况1触发！提前终止");
                    this.activeLength++; // 只是移动活动点
                    this.addSuffixLink(this.activeNode); // 更新后缀链接
                    this.remainingSuffixCount--;//✅修复减少剩余计数,remainingSuffixCount表示本轮还有多少个后缀需要处理。
/*✅每个字符处理完后，remaining都应该归零，表示这个字符的所有相关工作都完成了。如果不归零会发生什么:算法认为有工作要做，但实际上没有:
remainingSuffixCount必须归零:状态一致性：算法状态必须与实际工作匹配,确定性：每个字符的处理应该是自包含的,可预测性：下个字符应该从干净的状态开始
*/
                    break;// 关键优化：提前终止本轮！
                }
                // 情况3：需要分裂边
//🎯分裂是为了固定边的范围，为新增字符腾出空间;分裂必要：当要添加特殊字符时，需要固定边界,分裂的本质：从「自动延伸」模式切换到「精确边界」模式
                console.log("🔧 进入情况3：需要分裂");
                    console.log(" 分裂边:", {
                        nextStart: next.start,
                        activeLength: this.activeLength, 
                        splitEnd: next.start + this.activeLength - 1,
                        nextChar: this.text[next.start],
                        newChar: this.text[pos]
                    });

                    //第1步：计算分裂位置
                    const splitEnd = next.start + this.activeLength - 1;//计算分裂位置,next.start = 0（边的起始位置）,this.activeLength = 1（在边上走了1步）,splitEnd = 0 + 1 - 1 = 0,在位置0之后分裂（"a" | "ba"）
                    //第2步：创建中转站，这个节点将成为分叉点，十字路口让新旧路径共存！splitNode = 十字路口
                    const splitNode = new SuffixTreeNode();//创建新节点代表 "a"（从0到0）
                    //第3步：调整原有路径，🎯必须保持原有连接的同时建立新连接
                    /*定义中转站负责的路段告诉中转站：你负责从位置0到位置0这段路这个中转站，只覆盖字符串中的第0个字符，即 "a"，划定管辖范围，精确
                    分段，标签定义，责任分离
                    "a" 没有丢失：中转站 = 负责 "a"（位置0到0）原有节点 = 负责 "ba"（位置1到∞）"a" 还在，只是换了个管家！
                    */
                    splitNode.start = next.start;// 0
                    splitNode.end = splitEnd;//✅正确// 0
                    //调整原有节点，把原有节点的起点往后移动
                    next.start += this.activeLength;
                    //重新连接根节点，把根节点的指针从原有节点改指向中转站；改变根节点的指针，从：根 → 原有节点变成：根 → 中转站
                    this.activeNode.children[activeEdgeChar] = splitNode;
                    //连接中转站到原有节点，在中转站建立到原有节点的连接；建立中转站的新指针，中转站 → 分裂后剩下的一半，避免创建新节点对象
                    /*
                    我们可以选择：方案A：创建新节点代表"ba"，保持原节点不变，方案B：直接修改原节点，让它代表"ba"
                    Ukkonen选择了方案B：更节省内存，避免复杂的对象拷贝，保持引用的一致性，原节点被「重用」了，但内容更新了
                    */
                    splitNode.children[this.text[next.start]] = next;
                    console.log("💰 关键检查 - 中转站是否有'$'路径:", {
                        hasDollar: '$' in splitNode.children,
                        allChildren: Object.keys(splitNode.children)
                    });
                    // 添加详细的路径追踪
                    console.log("🔍 分裂后立即验证:");
                    console.log("   中转站的孩子:", Object.keys(splitNode.children));
                    console.log("   完整路径检查:");
                    
                    //第4步：创建新分支
                    console.log(" 创建新叶子前:", {
                            pos: pos,
                            char: this.text[pos],
                            splitNodeChildren: Object.keys(splitNode.children)
                        });
                    const leaf = new SuffixTreeNode();
                    leaf.start = pos;//创建新叶子代表 "$" ，每个后缀必须有自己结束的叶子节点
                    leaf.end = Infinity;
                    console.log("🍃 新叶子创建:", {
                        start: leaf.start,
                        end: leaf.end,
                        char: this.text[pos]
                    });
                    //把新叶子挂到中转站，连接新分支：让新后缀能被访问到
                    splitNode.children[this.text[pos]] = leaf;// 这行应该创建'$'路径
                    console.log("🔧 创建新叶子后:", {
                            splitNodeChildren: Object.keys(splitNode.children),
                            "是否有$": '$' in splitNode.children
                        });
                        console.log("🎯 基本信息验证:", {
                            pos: pos,
                            "this.text": this.text,
                            "this.text[pos]": this.text[pos],
                            "this.text[pos] === '$'": this.text[pos] === '$'
                        });
                    //建立后缀链接，维护状态网络：为后续智能跳转做准备
                    this.addSuffixLink(splitNode);
                    /*
                    创建新分支后建立后缀链接：
                    后缀链接的作用：后缀链接建立了「长后缀 → 短后缀」的关系"abc" → "bc" → "c"，当算法处理完"abc"后，通过后缀链接直接跳转到"bc"的位置，而不是从头开始找
                    新创建的中转站（splitNode）可能成为后续处理的起点，假设后续要处理后缀"ba$"没有后缀链接：从根开始 → 找'b'边 → 找到路径 → 处理...
                    有后缀链接：从"a"节点的后缀链接直接跳转到正确位置 → 处理...后缀链接是「快捷方式」！
                    🚀提供快捷方式：让后续处理能快速跳转，🕸️构建智能网络：自动连接相关节点，⚡ 优化性能：避免重复的路径查找，🔗 保持连续性：确保算法状态连贯
                    */
                    //减少剩余工作，标记一个后缀处理完成
                    //this.remainingSuffixCount--;
                    console.log("🔄 分裂后准备处理下一个后缀");
                    //第5步：更新活动点：一次分裂只能处理一个后缀，但还有更多后缀要处理，继续处理剩余的后缀，这三个策略共同确保了算法的完备性和高效性
                    //活动点更新 = 改变 (node, edge, length)活动点更新就是改变这三个值
                    if (this.activeNode.suffixLink !== null) {
                        console.log("🔗 通过后缀链接跳转");
                        this.activeNode = this.activeNode.suffixLink;//策略1：直接跳到下一个相关后缀的位置//🎯更新activeNode
                    } else if (this.activeNode === this.root) {//策略2：在根节点时，手动调整活动点
                        console.log("🔗 在根节点，调整活动点");
                        if (this.activeLength > 0) {
                            this.activeEdge = this.activeEdge + 1;//🎯更新activeEdge
                            this.activeLength = this.activeLength - 1;//🎯更新activeLength
                        }
                    } else {//策略3：回退到根节点
                        console.log("🔗 没有后缀链接，回到根节点");
                        this.activeNode = this.root;// 🎯 更新activeNode
                    }
                    //活动点决定下一个处理哪个后缀！如果活动点更新不正确：可能跳过了处理 "a$" 的位置，或者停在了错误的位置，导致 "a$" 没有被创建
                    console.log("🎯 活动点更新后:", {
                        新活动点: `(${this.activeNode === this.root ? 'root' : 'node'}, ${this.activeEdge}, ${this.activeLength})`,
                        剩余工作: this.remainingSuffixCount,
                        "当前字符": this.text[this.activeEdge]
                    });

                    // 特别检查是否应该创建 "a$"
                    if (this.activeNode === this.root && this.activeLength === 0) {
                        console.log("💡 可能应该创建直接路径的时刻");
}                   
                    console.log("🔄 准备继续循环前的最终检查:");
                    console.log("   中转站的孩子:", Object.keys(splitNode.children));
                    console.log("   是否有'$':", '$' in splitNode.children);

                    // 然后才执行活动点更新和continue
                    continue;  // 🎯 关键：继续处理下一个后缀


                    
                
/*-------注意-------/
🔧Ukkonen算法依赖后缀链接自动处理剩余后缀，但如果链接没建立好，就会提前结束，//修复核心：在情况3分裂后，必须通过后缀链接更新活动点并continue！
🔧分裂逻辑没有成功创建 '$' 路径：检查创建叶子前后的$ 是否真正的创建成功
🔧'$' 路径创建成功了，但最终树结构没有显示，说明问题在后续的处理过程中：后续代码修改了结构，活动点更新后，某些操作覆盖了 '$' 路径，printTree函数有bug
remaining 会变成0：每个新字符开始时this.remainingSuffixCount++;  // 从0变成1，分裂中this.remainingSuffixCount--;  // 从1变成0
但一个字符可能对应多个后缀！ 比如 '$' 对应："aba$"，"ba$"，"a$"，"$"不应该在每次分裂后都减少 remaining：
remainingSuffixCount 记录还有多少个后缀需要处理，每次成功处理后缀时才减少，但分裂只是重新组织结构，不一定是完成了一个后缀，只在真正完成后缀处理时才减少

*/
                            }
        }
        console.log("扩展后活动点:", {
            node: this.activeNode === this.root ? 'root' : 'other',
            edge: this.activeEdge,
            length: this.activeLength,
            remaining: this.remainingSuffixCount
        });
        
        }

printTree(node = this.root, prefix = '', isLast = true) {
        if (!node) return;
        
        const connector = isLast ? '└── ' : '├── ';
        
        if (node === this.root) {
            console.log(prefix + connector + '根节点');
        } else {
            const endIndex = node.end === Infinity ? this.text.length : node.end + 1;
            const edgeText = this.text.substring(node.start, endIndex);
            const nodeType = Object.keys(node.children).length === 0 ? '叶子' : '内部节点';
            console.log(prefix + connector + `${nodeType} [${node.start},${node.end}] "${edgeText}"`);
        }
        
        const children = Object.keys(node.children);
        children.forEach((char, index) => {
            const isLastChild = index === children.length - 1;
            const childPrefix = prefix + (isLast ? '    ' : '│   ');
            console.log(childPrefix + `通过字符 '${char}':`);
            this.printTree(node.children[char], childPrefix + '    ', isLastChild);
        });
    }
debugTree(node = this.root, depth = 0) {
    if (!node) return;
    
    const indent = '  '.repeat(depth);
    if (node === this.root) {
        console.log(indent + '根节点');
    } else {
        const endIndex = node.end === Infinity ? this.text.length : node.end + 1;
        const edgeText = this.text.substring(node.start, endIndex);
        console.log(indent + `[${node.start},${node.end}] "${edgeText}"`);
    }
    
    Object.keys(node.children).forEach(char => {
        console.log(indent + `  └─ 字符 '${char}':`);
        this.debugTree(node.children[char], depth + 2);
    });
}
    }
const st = new SuffixTree();
st.buildSuffixTree("banana");
st.printTree();
```