# Trie
## 基础知识
- **定义**
```
Trie树：又称字典树、前缀树或单词查找树，是一种专门用于处理字符串集合的树形数据结构。其核心思想是通过字符串的公共前缀来组织和存储数据，从而实现对字符串的高效检索。名称"Trie"来源于单词"retrieval"（检索）。
```
- **核心特性**
    - 结构特性
        - 树形结构：每个节点代表一个字符
        - 路径表示：从根节点到任意节点的路径构成一个字符串前缀
        - 共享存储：具有公共前缀的字符串共享存储路径
        - 多叉树：每个节点的子节点数量由字符集大小决定
- **Trie vs 哈希表**

|特性|	Trie	|哈希表|
---|---|---
|前缀搜索|	原生支持	|不支持|
|内存使用	|可能较高	|相对较低|
|冲突处理|	无冲突|	需要处理哈希冲突|
|有序性|	字典序|	无序|


## 注意事项
1. **混淆点**

|注意点	|正确做法| 	具体分析|
---|---|---
|节点设计|	class TrieNode { children = new Map(); isEnd = false; }	|Trie是多叉树，需要动态子节点映射，isEnd标记单词边界|
|字符处理	|使用Unicode安全的字符处理，考虑大小写一致性	|避免因字符编码或大小写导致搜索失败|
|内存优化|	对稀疏分支使用Map，对密集分支使用数组|	平衡查询速度和内存使用|
|前缀搜索实现|	先导航到前缀节点，再深度优先收集所有子节点	|确保找到所有匹配前缀的完整单词|
|空字符串处理|	根节点的isEnd=true表示空字符串是有效单词|	正确处理边界情况|
|删除操作|	懒惰删除标记，必要时才清理节点链	|避免频繁内存分配，提高性能|
|序列化|	使用层级结构或前缀表示法|	便于存储和网络传输|
|并发访问	|使用读写锁或不可变Trie结构|	保证多线程环境下的数据一致性|
|路径压缩|	对单链路径进行节点合并|	减少内存使用，提高查询效率|
|批量插入|	预先排序单词，利用前缀共享优化插入顺序	|最大化前缀复用，减少节点创建|
2. 代码实现
```
class TrieNode {//==========🔄节点类=========//
    constructor() {
        this.children  = new Map(); // 子节点映射//创建一个空的Map对象,Map是JS中的键值对集合//去下一个字符怎么走
        //每个节点不存储完整的路径，只存储从父节点到自己的字符,整个路径是通过节点连接关系隐含表达的
        this.isEnd = false;//一个布尔值标记// 是否为单词结尾//标记终点站
        this.frequency = 0;//🟢频率统计
    }
    }//清晰：每个属性职责单一，容易理解;易维护：修改指路逻辑不影响标记逻辑;可扩展：未来添加功能不会破坏现有结构
class Trie {//========🔄Trie类=========//
    constructor() {
        this.root= new TrieNode();//根节点//创建一个全新的空节点//创建一个空的根节点//root 在计算机科学中特指树形结构的顶级节点
    }
    insert(word,freq = 1) {//插入方法//🟢支持传入频率
    console.log(` 开始插入: "${word}", 频率: ${freq}`);
    let node = this.root;
    for (let char of word) {//检查当前路口有没有通往下一个字符的路
        console.log(`  处理字符: "${char}"`);
        if (!node.children.has(char)) {
            console.log(` 创建新节点 for "${char}"`);
            node.children.set(char, new TrieNode());//如果没有就创建一条新的路，指向一个新的空节点
        }else {
            console.log(` 使用现有节点 for "${char}"`);
        }
        //🟢Trie在内存中既是链式存储，又是树结构；普通二叉树固定两个分支左和右；Trie树动态多个分支；Trie是多叉树（每个节点可能有多个子节点）
        //🟢Trie是特殊的树：节点可以有0到多个子节点，子节点通过字符而不是位置来索引，深度由单词长度决定//用链式的实现表达了树形的逻辑
        //🟢Trie在内存中：存储方式：链式引用（指针/地址）；逻辑结构：多叉树；访问方式：通过字符映射而不是固定位置；//确实有链式特点（线性访问路径），整体是树结构，只是不是二叉树
        node = node.children.get(char);//沿着指示牌走向下一个节点//Map 不是普通对象，必须用 .get() 方法
        //get的作用：查找：在Map中找到对应键的值；返回：返回该值（这里是子节点的引用）；不修改：不会改变原来的Map，只是读取//从当前节点的指路牌（children Map）中，找到标着某个字符的地址，然后跳到那个地址指向的新节点
        console.log(` 移动到节点, 当前频率: ${node.frequency}`);
    }
    console.log(`到达单词结尾, 之前频率: ${node.frequency}, 新增: ${freq}`);
    node.isEnd = true;//直到单词结束
    node.frequency += freq;//🟢更新频率
    console.log(`最终频率: ${node.frequency}`);
}
    search(word) {//搜索完整单词//确认到达最后一个字符
    let node = this.root;
    for (let char of word) {
        if (!node.children.has(char)) {
            return false;
        }
        node = node.children.get(char);
    }
    return node.isEnd; //关键区别：还要检查结束标记//这里是不是单词终点
}
   startsWith(prefix) {//搜索前缀
    let node = this.root;
    for (let char of prefix) {
        if (!node.children.has(char)) {
            return false;
        }
        node = node.children.get(char);
    }
    return true;//关键区别：只要路径存在就返回true//前缀路径是否存在
}   
    getAllWordsWithPrefix(prefix) {//收集所有以指定前缀开头的完整单词
    let node = this.root;
    for (let char of prefix) {
        if (!node.children.has(char)) {
            return [];// 如果路径不存在，直接返回空数组
        }
        node = node.children.get(char);
    }
    const results = [];//收集所有后代单词
    this._collectWordsWithFrequency(node, prefix, results);
    return results;
}
 //🟢添加这个方法
    getAllWordsWithFrequency(prefix) {
        let node = this.root;
        for (let char of prefix) {
            if (!node.children.has(char)) {
                return [];
            }
            node = node.children.get(char);
        }
        const results = [];
        this._collectWordsWithFrequency(node, prefix, results);
        return results;
    }
_collectWordsWithFrequency(node, currentWord, results) {//返回带频率的对象
        if (node.isEnd) {
            results.push({
                word: currentWord,
                frequency: node.frequency//🟢包含频率信息
            });
        }
        for (let [char, childNode] of node.children) {
            this._collectWordsWithFrequency(childNode, currentWord + char, results);
        }}
    
_collectWords(node, currentWord, results) {//获取所有前缀匹配的单词//辅助函数//只返回字符串
    if (node.isEnd) {//如果当前节点是单词结尾
        results.push(currentWord); //把单词加入结果
    }
    for (let [char, childNode] of node.children) {//遍历所有子节点（继续探索所有分支）
        this._collectWords(childNode, currentWord + char, results);
    }
}}

/*=======💡注意======//
    Trie是一种特殊的树结构，专门用于高效处理前缀查询。
    在Trie中，每个节点代表一个字符，从根节点到叶子节点的路径表示一个完整字符串
节点结构
    每个Trie节点包含：
        子节点字典/映射：存储字符到子节点的映射
        结束标志：标记当前节点是否构成完整单词
查询操作
    搜索前缀"app"时：
        沿着路径a、p、p、导航
        然后收集该节点的所有子树中的所有单词
    搜索完整单词"apple"时：
        沿着路径导航到'e'节点
        检查该节点的结束标志是否为True
性能优势
    在包含50万单词的词典中搜索"app"开头的单词：
        传统方法需要约500万次比较
        Trie只需要3步导航
    Trie的性能优势来自于避免了重复的前缀比较
Trie常用于实现：搜索自动补全、IP路由表
    */
//测试代码//
const trie = new Trie();
trie.insert("apple");
trie.insert("application");
trie.insert("appliance");

console.log(trie.search("apple"));     // true
console.log(trie.search("app"));       // false  
console.log(trie.startsWith("app"));   //  true
const words = trie.getAllWordsWithPrefix("app");
console.log(words); 
//=========================🔄自动补全系统========================//
class AutoComplete {
    constructor() {
        this.trie = new Trie();
    }
    addSearchHistory(word, freq = 1) {//🚨正确传入频率参数
        // 记录搜索频率，用于排序
        this.trie.insert(word, freq);//🟢每次搜索频率+1
        this.trie.insert(word);
        // 实际中这里还会更新频率
    }
    getSuggestions(prefix) {//普通建议
        const wordsWithFreq = this.trie.getAllWordsWithPrefix(prefix);
        console.log(" 排序前数据:", wordsWithFreq);
         // 调试排序
            wordsWithFreq.sort((a, b) => {
                const result = b.frequency - a.frequency;
                console.log(`比较: ${a.word}(${a.frequency}) vs ${b.word}(${b.frequency}) = ${result}`);
                return result;
            });
            
            console.log("排序后数据:", wordsWithFreq);
        //🟢实际中这里会按频率排序
        //wordsWithFreq.sort((a, b) => b.frequency - a.frequency)// 按频率降序排序
        // 只返回单词列表（不包含频率信息）
        const result=wordsWithFreq.map(item => item.word).slice(0, 10);
        //✅wordsWithFreq 是对象数组，需要提取word属性：return wordsWithFreq.slice(0, 10); 这样返回的是对象数组，显示为 undefined
        //✅wordsWithFreq: 是一个对象数组， {word: "appliance", frequency: 200},.map(item => item.word): 把对象数组转换成字符串数组// 转换后：["appliance", "apple", "apply"]
        //return words.slice(0,10); // 返回前10个建议//0：从第0个元素开始；10：到第10个元素之前结束（不包含第10个）
        console.log("最终结果:", result);
        return result;
    }
    getSuggestionsdebug(prefix) {
        console.log("=== 开始调试 getSuggestions ===");
        const wordsWithFreq = this.trie.getAllWordsWithPrefix(prefix);
        console.log("1. 从Trie获取的数据:", wordsWithFreq);
        // 检查是否是数组
        console.log("2. 数据类型:", Array.isArray(wordsWithFreq) ? "数组" : "不是数组");
        if (wordsWithFreq.length === 0) {
            console.log("3. 数据为空数组");
            return [];
        }
        // 检查第一个元素的结构
        console.log("4. 第一个元素:", wordsWithFreq[0]);
        console.log("5. 第一个元素的word属性:", wordsWithFreq[0].word);
        console.log("6. 第一个元素的frequency属性:", wordsWithFreq[0].frequency);
        // 排序前
        console.log("7. 排序前的数据:", wordsWithFreq.map(item => `${item.word}:${item.frequency}`));
        wordsWithFreq.sort((a, b) => b.frequency - a.frequency);
        // 排序后
        console.log("8. 排序后的数据:", wordsWithFreq.map(item => `${item.word}:${item.frequency}`));
        const result = wordsWithFreq.map(item => {
            console.log(`9. 映射处理: ${item.word} -> ${item.word}`);
            return item.word;
        }).slice(0, 10);
        console.log("10. 最终结果:", result);
        console.log("=== 调试结束 ===\n");
        return result;
    }
    // 新增：获取带频率的详细建议（用于调试）//如果要按搜索频率排序，修改Trie的部分
    getDetailedSuggestions(prefix) {//详细建议
        //🟢修复：正确定义wordsWithFreq变量
        const wordsWithFreq = this.trie.getAllWordsWithPrefix(prefix);
        wordsWithFreq.sort((a, b) => b.frequency - a.frequency);
        return wordsWithFreq.slice(0, 10);
    }
    //------❌注意------//
    //🔧Uncaught ReferenceError: wordsWithFreq is not defined：wordsWithFreq变量在使用之前没有被定义
    //🔧getSuggestionsdebug 结果: Array [ undefined ]：//Trie类中有两个同名但功能不同的方法，这导致了冲突：
    //getAllWordsWithPrefix 调用的是 _collectWords，而不是 _collectWordsWithFrequency
    //getDetailedSuggestions 结果: Array [ {…} ]：说明 getDetailedSuggestions 现在返回的是带频率的对象，而不是纯字符串了！这是正确的行为  
    //getSuggestions - 返回纯字符串数组 ["appliance", "apple", ...]；getDetailedSuggestions - 返回对象数组 [{word: "appliance", frequency: 200}, ...]
    //🔧所有单词的频率都是2，这说明频率没有正确存储:
    //调用：autoComplete.addSearchHistory("apple", 150);// 但 AutoComplete 的 addSearchHistory 方法：addSearchHistory(word, freq = 1) {//🚨这里freq = 1覆盖150}
    //addSearchHistory(word, freq = 1)正确传入频率参数
}
/* 使用示例
const autoComplete = new AutoComplete();
autoComplete.addSearchHistory("javascript");
autoComplete.addSearchHistory("java");
autoComplete.addSearchHistory("python");
console.log(autoComplete.getSuggestions("jav"));
autoComplete.addSearchHistory("apple");
autoComplete.addSearchHistory("application");
autoComplete.addSearchHistory("appliance");
console.log("自动补全结果:", autoComplete.getSuggestions("app"));*/
console.log("=== 最小化测试 ===");
const autoComplete = new AutoComplete();
// 只插入一个单词测试
autoComplete.addSearchHistory("test", 100);
// 分别测试两个方法
console.log("getSuggestions 结果:", autoComplete.getSuggestions("t"));
console.log("getSuggestionsdebug 结果:", autoComplete.getSuggestions("t"));
console.log("getDetailedSuggestions 结果:", autoComplete.getDetailedSuggestions("t"));

console.log("=== 深度调试频率问题 ===");
const autoComplete2 = new AutoComplete();
// 逐步添加并检查
console.log("1. 添加 apple(150)");
autoComplete2.addSearchHistory("apple", 150);
console.log("2. 添加 application(80)");
autoComplete2.addSearchHistory("application", 80);
console.log("3. 添加 appliance(200)");
autoComplete2.addSearchHistory("appliance", 200);
// 立即测试
console.log("立即测试排序:");
const suggestions = autoComplete2.getSuggestions("app");
console.log("当前结果:", suggestions);
// 检查 Trie 内部状态
console.log("检查Trie根节点:", autoComplete2.trie.root);

console.log("=== 深度调试插入过程 ===");
const debugTrie = new Trie();
console.log("1. 插入 apple(150)");
debugTrie.insert("apple", 150);
console.log("\n2. 插入 application(80)");
debugTrie.insert("application", 80);
console.log("\n3. 插入 appliance(200)");
debugTrie.insert("appliance", 200);
// 检查最终状态
console.log("\n=== 检查最终状态 ===");
const finalData = debugTrie.getAllWordsWithFrequency("app");
console.log("最终数据:", finalData);
finalData.forEach(item => {
    console.log(`单词: ${item.word}, 频率: ${item.frequency}`);
});

console.log("=== 测试排序功能 ===");
const results = [
    {word: "apple", frequency: 150},
    {word: "application", frequency: 80}, 
    {word: "appliance", frequency: 200}
];
// 排序测试
console.log("排序前:", results.map(item => `${item.word}(${item.frequency})`));
results.sort((a, b) => b.frequency - a.frequency);
console.log("排序后:", results.map(item => `${item.word}(${item.frequency})`));
// 应该输出: ["appliance(200)", "apple(150)", "application(80)"]

console.log(" === 最终测试 === ");
const finalAC = new AutoComplete();
// 模拟真实用户行为
finalAC.addSearchHistory("javascript", 300);
finalAC.addSearchHistory("java", 250);
finalAC.addSearchHistory("python", 280);
finalAC.addSearchHistory("php", 50);
finalAC.addSearchHistory("ruby", 30);
console.log("语言:", finalAC.getSuggestions("j"));
// 应该看到: ["javascript", "java"] 
console.log("成功");

//========================🔄拼写检查器=========================//
class SpellChecker {
    //实现拼写检查和建议：单字符替换策略
    constructor(dictionary) {
        this.trie = new Trie();
        for (let word of dictionary) {
            this.trie.insert(word);//将字典单词插入Trie
        }
    }
    check(word) {
        return this.trie.search(word);//检查单词是否在字典中
    }
    getSuggestions(misspelledWord) {
        const suggestions = new Set();
        // 策略1: 单字符替换（现有策略）检查是否有仅差一个字符的单词//只替换字符，不改变长度
        this._singleCharReplace(misspelledWord, suggestions);
        // 策略2: 字符插入
        this._charInsert(misspelledWord, suggestions);
        // 策略3: 字符删除  
        this._charDelete(misspelledWord, suggestions);
        return Array.from(suggestions);
    }
    _singleCharReplace(misspelledWord, suggestions) {
        console.log("单字符替换策略:");// 替换错误（单字符替换）
        for (let i = 0; i < misspelledWord.length; i++) {
            for (let char of 'abcdefghijklmnopqrstuvwxyz') {
                if (char === misspelledWord[i]) continue;// 跳过相同的字符
                // 生成候选单词：替换第i个字符
                const candidate = misspelledWord.slice(0, i) + char + misspelledWord.slice(i + 1);
                //misspelledWord.slice(0, i)-切下前i个字符；+char-插入新字符；+ misspelledWord.slice(i + 1)-加上剩下的字符
                if (this.check(candidate)) {//检查候选单词是否存在
                    console.log(` ${misspelledWord} → ${candidate} (位置${i}: ${misspelledWord[i]}→${char})`);
                    suggestions.add(candidate);
                }
            }
        }
    }
    _charInsert(misspelledWord, suggestions) {
        console.log(" 字符插入策略:");//在第i个位置插入字符//. 缺失错误（字符插入）
        for (let i = 0; i <= misspelledWord.length; i++) {
            for (let char of 'abcdefghijklmnopqrstuvwxyz') {
                const candidate = misspelledWord.slice(0, i) + char + misspelledWord.slice(i);
                
                if (this.check(candidate)) {
                    console.log(` ${misspelledWord} → ${candidate} (在位置${i}插入${char})`);
                    suggestions.add(candidate);
                }
            }
        }
    }
    _charDelete(misspelledWord, suggestions) {
        console.log("字符删除策略:");//删除第i个字符//多余错误（字符删除）
        for (let i = 0; i < misspelledWord.length; i++) {
            const candidate = misspelledWord.slice(0, i) + misspelledWord.slice(i + 1);
            
            if (this.check(candidate)) {
                console.log(`  ${misspelledWord} → ${candidate} (删除位置${i}的${misspelledWord[i]})`);
                suggestions.add(candidate);
    }
}}}
console.log("=== 拼写检查器测试 ===");
// 词典数据
const dictionary = [
    "apple", "application", "appliance", "apply", "app",
    "banana", "band", "bank", "bat", "batman",
    "cat", "car", "card", "care", "case"
];
// 创建拼写检查器
const spellChecker = new SpellChecker(dictionary);
// 测试用例
console.log("1. 检查正确拼写:");
console.log("   'apple':", spellChecker.check("apple")); // true
console.log("   'banana':", spellChecker.check("banana")); // true
console.log("\n2. 检查错误拼写:");
console.log("   'appl':", spellChecker.check("appl")); // false
console.log("   'bannaa':", spellChecker.check("bannaa")); // false
console.log("\n3. 获取拼写建议:");
console.log("   'appl' 的建议:", spellChecker.getSuggestions("appl"));
// 可能输出: ["apple", "apply"]
console.log("   'bannaa' 的建议:", spellChecker.getSuggestions("bannaa"));
// 可能输出: ["banana"]
console.log("   'cat' 的建议:", spellChecker.getSuggestions("cat"));
// 可能输出: ["bat", "car"] 等只有一个字符不同的单词
console.log("   'batman' 的建议:", spellChecker.getSuggestions("batman"));
// 可能输出: [] 因为没有只差一个字符的单词

console.log("=== 三种错误类型测试 ===");
const spellChecker1 = new SpellChecker([
    "apple", "banana", "cat", "dog", "application"
]);
// 测试用例
const testCases = [
    { wrong: "bapple", right: "apple", type: "替换错误" },      // b→a
    { wrong: "applee", right: "apple", type: "多余错误" },      // 删除e
    { wrong: "aple", right: "apple", type: "缺失错误" },        // 插入p
    { wrong: "application", right: "application", type: "替换错误" } // i→a
];
testCases.forEach(test => {
    console.log(`\n${test.type}: "${test.wrong}" → "${test.right}"`);
    const suggestions = spellChecker1.getSuggestions(test.wrong);
    console.log(`建议: ${suggestions}`);
});
//====================🔄IP路由表==================//
//实现最长前缀匹配
class Router {//决定数据包应该往哪里送；路由表使用CIDR表示法：前24位固定，后8位任意
    constructor() {
        this.trie = new Trie();
    } 
    //1.添加路由规则
    addRoute(cidr, target) {
        //cidr - 路由规则:Classless Inter-Domain Routing（无类别域间路由）格式："IP地址/前缀长度""10.0.0.0/8"//大型网络"0.0.0.0/0"// 默认路由:前缀长度数字越大网络越小
        //把人类友好的CIDR表示法转换成了计算机高效的Trie存储结构
        const [ip, prefixLength] = cidr.split('/');//1.解析CIDR表示法
        //ip - IP地址部分:从cidr中提取的IP地址：//prefixLength - 前缀长度:网络部分的位数:/24 = 前24位是网络地址;/8  = 前8位是网络地址;/0=没有网络地址（匹配所有）
        const binaryIP = this._ipToBinary(ip).substring(0, prefixLength);
        //2.IP转二进制 + 截取前缀//计算机看IP地址:32位二进制，计算机的真正语言;前24位相同就在同一网络;：存储网络地址//用很少的规则管理大量的IP地址
        //互联网就可以分层管理:"10.0.0.0/8":前24位：网络标识;后8位：主机标识;数字越小：网络越大;数字越大：网络越小
        this.trie.insert(binaryIP, target);//3.插入Trie
        //target - 目标位置:数据包应该发送到哪里//binaryIP - 二进制IP的前缀
    }
    //2.查找路由
    findRoute(ip) {////最长前缀匹配算法//数据包总是被发送到最具体的网络
        //🟢直接匹配会让本地流量绕远路;通用规则会覆盖特殊规则;无法实现精细的网络管理;最长匹配就是找"最具体的那个规则"
        //🟢路由表不是一个单独的数组或对象，而是存储在Trie树的节点中;
        const binaryIP = this._ipToBinary(ip);// IP转二进制
        let node = this.trie.root;// 从根节点开始
        let longestMatch = null;// 记录最长匹配
        let currentPath = ""; // 记录当前路径
        
        for (let bit of binaryIP) {// 遍历每个比特位
            if (!node.children.has(bit)) break;//如果没有路径，停止
            node = node.children.get(bit);//沿着路径前进
            currentPath += bit;// 记录走过的路径
            if (node.isEnd && node.value) {//如果当前是路由规则终点
                longestMatch = node.value;// 更新最长匹配
            }
        }
        return longestMatch;// 返回找到的最长匹配
    }
    _ipToBinary(ip) {//IP地址转二进制的方法
        return ip.split('.').map(segment => 
            parseInt(segment).toString(2).padStart(8, '0')//padStart(8, '0'):确保每个段都是8位
        ).join('');
        //1.ip.split('.')2.map(segment => ...) 处理每个数字3..join('') 连接所有二进制
    }
}

// 1. 先定义IP匹配函数
function ipMatchesCIDR(ip, cidr) {
    const [network, prefixLength] = cidr.split('/');
    const binaryIP = ipToBinary(ip);
    const binaryNetwork = ipToBinary(network);
    // 比较前 prefixLength 位是否相同
    return binaryIP.substring(0, prefixLength) === binaryNetwork.substring(0, prefixLength);
}
// 2.IP转二进制函数
function ipToBinary(ip) {
    return ip.split('.').map(segment => 
        parseInt(segment).toString(2).padStart(8, '0')
    ).join('');
}
// 3. 电脑路由表模拟
const myRouteTable = [
    { target: "0.0.0.0/0", gateway: "123.123.123.123" },// 默认路由//这是路由器网关！
    { target: "127.0.0.0/8", gateway: "127.0.0.1" },// 本地回环
    { target: "200.200.200.200", gateway: "200.200.200.200" }//本地网络//本机服务
];
// 4. 路由决策函数
function whereToSend(destIP) {
    console.log(` 数据包要去: ${destIP}`);
    // 最长前缀匹配
    let bestMatch = null;
    let bestLength = -1;
    for (let route of myRouteTable) {
        if (ipMatchesCIDR(destIP, route.target)) {
            const prefixLength = parseInt(route.target.split('/')[1]);
            console.log(`    匹配: ${route.target} (${prefixLength}位) → ${route.gateway}`);
            //选择前缀最长的匹配
            if (prefixLength > bestLength) {
                bestLength = prefixLength;
                bestMatch = route;
            }
        }
    }
    if (bestMatch) {
        console.log(`   最终发送到: ${bestMatch.gateway}`);
        return bestMatch.gateway;
    } else {
        console.log(`    没有匹配的路由！`);
        return null;
    }
}
//电脑路由表
const myRouteTable2 = [
    { target: "0.0.0.0/0", gateway: "123.123.123.123" },
    //默认路由:数据包的问路策略,承认自己不知道，但知道该问谁//路由表就在操作系统内核里//🌐路由表不是一个看得见的文件，而是存储在操作系统网络栈的内存中;//所有不认识的目的地，都通过网卡发给网关
    { target: "127.0.0.0/8", gateway: "127.0.0.1" },//本地回环
    { target: "200.200.200.200", gateway: "200.200.200.200" }//本地网络//地址直接通过网卡发送
    //路由表三要素：回环 + 本地网络 + 默认网关✅主要通路：通过网关访问互联网✅次要通路：本地网络直接通信✅ 特殊通路：回环自我访问
];
function whereToSend(destIP) {
    console.log(`数据包要去: ${destIP}`);
    // 最长前缀匹配
    let bestMatch = null; 
    for (let route of myRouteTable) {
        if (ipMatchesCIDR(destIP, route.target)) {
            console.log(` 匹配: ${route.target} → ${route.gateway}`);
            bestMatch = route;
        }
    }
    console.log(`最终发送到: ${bestMatch.gateway}`);
    return bestMatch.gateway;
}
// 测试路由
console.log("=== 电脑路由决策 ===");
whereToSend("8.8.8.8");        // 去Google DNS
whereToSend("123.123.123.123");// 本地网关
whereToSend("127.0.0.1");      // 访问自己
// 使用示例
const router = new Router();
router.addRoute("123.123.123.123", "内网服务器");
console.log(router.findRoute("200.200.200.200"));

/*Trie的空间时间权衡：
在包含10万英语单词的词典中：数组存储需要：400万字符存储；Trie存储需要：约150万节点；前缀搜索"app"：数组：50万次比较；Trie：3步导航 + 结果收集
Trie用空间换来了时间优势: 插入时间：从 O(1) HashMap → O(k)Trie;Trie前缀搜索：从 O(n) → O(k + m);内存占用：从 O(n×m) → O(n×m)但实际更复杂
适合使用Trie：需要频繁的前缀查询;内存极度受限;字符串集合有很多公共前缀;只需要精确匹配*/
```