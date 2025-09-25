# 栈 stack
## 基本特性
- 栈是一种抽象数据类型，它可以用不同的底层数据结构实现
- LIFO（后进先出）Last In, First Out：最后进去的元素最先出来
- 栈的简洁性是其优势：只关注"当前顶部"，不关心历史
- 栈的基本操作-只能操作最顶部的元素
```
 1. push(元素) - 把元素压入栈顶
 2. pop() - 弹出栈顶元素（移除并返回）
 3. peek() - 查看栈顶元素（不移除）
 4. isEmpty() - 判断栈是否为空
```
- 栈 vs 其他数据结构的对比

|操作	|栈(链表实现)|	数组	|队列|
---|---|---|---
|插入元素|	O(1)	|O(1)或O(n)|O(1)|	
|删除元素|	O(1)	|O(n)	|O(1)|
|随机访问|	o(n)	|O(1)	|O(n)|
|查看顶部/头部|	o(1)|o(1)	|O(1)|

## 注意事项
1. 混淆点
```
栈的结构：
- 栈顶（top） → [C] ⇄ [B] ⇄ [A] → null
   ↑               ↑               ↑
pop/push都在这里 中间元素         栈底
```
- top 是栈类自己的属性；永远指向最上面的栈顶元素,同时可以调用next属性,this.top 永远指向当前的栈顶
- 每个元素都有next指针
- this.top：栈类的属性，是一个"指针变量"
- this.top.next：当前栈顶节点的next属性，是另一个"指针"
- 算法复杂度（大O表示法）
```
O(1)时间（常数时间）:数据量从10→1000，操作次数都是1次
O(n)时间（线性时间）:数据量从10→1000，操作次数从10次→1000次
O(n²)：平方时间，较差（如嵌套循环）
O(log n)：对数时间，很好（如二分查找）
```
- 栈的底层内存模型:栈永远只关心"顶部"元素
```
初始状态：stack.top → [A] → null
执行 push("B")：
const newNode = { data: "B", next: this.top }; 
newNode.next = this.top = 节点A
所以新节点B指向A：B → A
this.top = newNode;  // stack.top 现在指向新节点B
结果：stack.top → [B] → [A] → null
如果stack.top一直指向A，那么每次push都需要遍历到末尾，效率是O(n)
```
- pop()执行后会先断开栈顶连接的元素留下下一个元素；
```
pop()之前：stack.top → [B] → [A] → null
执行pop()：this.top = this.top.next;  // this.top从B移动到A
pop()之后：stack.top → [A] → null
然后push("C"):
const newNode = { data: "C", next: this.top };  // this.top是A，所以C指向A
this.top = newNode;  // stack.top指向C
最终：stack.top → [C] → [A] → null
```
- 对空栈执行pop()
```
tack.top.next 在空栈时=undefined，this.top=null。
```
- - 栈是一个临时存储结构，它的核心价值在于：
```
记录当前状态（比如函数调用栈）
提供撤销操作（比如编辑器的undo）
管理临时数据（比如表达式求值）
在这些场景中，被pop的元素通常不需要长期保存。
```

- 使用栈而不是数组的情况
```
当需要频繁的"后进先出"操作时：
    函数调用栈
    撤销/重做功能
    括号/语法匹配
    深度优先搜索
```
- 用链表实现栈的两种方式：
```
1. 在链表头部操作（推荐，因为O(1)时间）
栈顶 ← 链表头部
push: 在头部插入新节点
pop:  从头部删除节点
2.在链表尾部操作（需要遍历，O(n)时间

```
- 用双向链表实现栈
我们将利用双向链表在头部操作O(1)的优势：

2. 代码实现
```
class StackNode {
    constructor(data) {
        this.data = data;  // 存储的数据，基于链表
        this.next = null;  // 指向下一个节点的指针 ← 每个节点都有！
    }
}
class Stack {
    constructor() {
        this.top = null;  // 这是栈类的属性，用来记录"栈顶在哪里"
        this.size = 0;
    }


    // 入栈方法
    push(item) {
        const newNode = {
            data: item,
            next: null
        };
        
        if (this.top === null) {
            // 栈为空的情况
            this.top = newNode;
        } else {
            // 栈不为空：新节点指向原栈顶，然后更新栈顶指针
            newNode.next = this.top;
            this.top = newNode;
        }
        this.size++;
    }
    
    // 出栈方法
    pop() {
        if (this.top === null) {
            return null;  // 栈为空，不能出栈
        }
        
        const item = this.top.data;  // 保存栈顶数据
        this.top = this.top.next;    // 栈顶指针下移
        this.size--;
        return item;
    }
    
    // 查看栈顶
    peek() {
        if (this.top === null) {
            return null;
        }
        return this.top.data;
    }
    
    // 判断是否为空
    isEmpty() {
        return this.top === null;
    }
    //获取栈大小
     getSize() {
        return this.size;
    }
    
    // 清空栈
    clear() {
        this.top = null;
        this.size = 0;
    }
    
    //打印栈内容（调试用）
    print() {
        let current = this.top;
        const elements = [];
        while (current) {
            elements.push(current.data);
            current = current.next;
        }
        console.log("Stack:", elements.join(" → "));
}


```
```
双向链表实现栈的两种方式
委托链表
class Stack {
    constructor() {
        this.list = new DoublyLinkedList();
    }
    
    push(item) {
        this.list.addTask(item); 
    }
    
    pop() {
        if (this.isEmpty()) {    
            return null;
        }
        const item = this.list.head.data;
        this.list.deleteFromHead();  
        return item;
    }
    
    peek() {
        if (this.isEmpty()) {    
            return null;
        }
        return this.list.head.data;
    }
    
    isEmpty() {
        return this.list.size === 0; 
    }
    
    size() {
        return this.list.size;
    }
}
```
```
括号匹配：
栈的LIFO特性正好匹配括号的嵌套结构
遇到左括号push，遇到右括号pop，最后检查栈是否为空
天然的"最近匹配"原则
function isParenthesesBalanced(str) {
    const stack = new Stack();
    
    for (let i = 0; i < str.length; i++) {
        const char = str[i];
        
        if (char === '(') {
            // 遇到左括号，入栈
            stack.push(char);  // 或者 stack.push('(') 都可以
        } else if (char === ')') {
            // 遇到右括号，检查栈是否为空
            if (stack.isEmpty()) {  // 检查栈是否为空的方法
                return false;  // 栈为空，但有右括号，不匹配
            }
            // 出栈（匹配一个左括号）
            stack.pop();  // 调用pop方法，移除一个左括号
        }
    }
    
    // 最后栈应该为空才匹配
    return stack.isEmpty();  // 如果栈为空，说明所有括号都匹配了
}

function isAllParenthesesBalanced(str) {
    const stack = new Stack();
    
    for (let i = 0; i < str.length; i++) {
        const char = str[i];
        
        if (char === '(' || char === '[' || char === '{') {
            // 左括号入栈
            stack.push(char);
        } else if (char === ')' || char === ']' || char === '}') {
            // 右括号检查
            if (stack.isEmpty()) {
                return false;
            }
            
            const top = stack.pop();
            // 检查括号类型是否匹配
            if ((char === ')' && top !== '(') ||
                (char === ']' && top !== '[') ||
                (char === '}' && top !== '{')) {
                return false;
            }
        }
    }
    
    return stack.isEmpty();
}

字符串反转
//变量使用：不需要中间变量，直接操作栈即可//逻辑顺序：应该在循环完成后统一出栈，而不是边入栈边出栈
//代码重构："哪些变量是多余的？""哪些步骤可以合并？""有没有更简洁的表达方式
function reverseString(str) {
    const stack = new Stack();
    let result = '';
    
    // 第一步：把所有字符入栈
    for (let i = 0; i < str.length; i++) {
        stack.push(str[i]);
    }
    
    // 第二步：把所有字符出栈（由于栈的LIFO特性，顺序会反转）
    while (!stack.isEmpty()) {
        result += stack.pop();//result = result + stack.pop();
    }
    
    return result;
}
撤销栈：记录所有操作
const undoStack = new Stack();
const redoStack = new Stack();

// 执行操作时
function doAction(action) {
    undoStack.push(action);
    // 清空重做栈
    redoStack.clear();
}

// 撤销时
function undo() {
    if (!undoStack.isEmpty()) {
        const action = undoStack.pop();
        redoStack.push(action);
        // 执行撤销逻辑
    }
}

// 重做时  
function redo() {
    if (!redoStack.isEmpty()) {
        const action = redoStack.pop();
        undoStack.push(action);
        // 执行重做逻辑
    }
}
```
# 双向链表
## 基本特性
- 每个节点都有两个指针prev,next
- 每个链表类都有头指针和尾指针


## 注意事项
1. 混淆点
- 节点实现
```
head → [A] <--> [B] ← tail
       ↑        ↑
    prev=null  prev=A
    next=B     next=null
```
- 双向链表通常维护tail（尾指针），从尾部操作也很方便;双向链表通过维护tail指针，用少量额外空间换来了尾部操作的O(1)时间复杂度
- 在尾部添加节点：双向链表（直接操作tail，无需遍历）;单向链表（需要遍历到最后）;
- 反向遍历：可以从tail开始，用prev指针倒着走
- 删除节点更方便：要删除某个节点，直接修改它前后节点的指针就行
- 尾部操作高效：因为有tail指针，在尾部添加节点是O(1)时间
- 建立双向连接的逻辑：每个新节点都要同时设置好向前和向后的指针
- 赋值顺序从右向左,逻辑理解从左向右
- tail是动态的，每次可能指向不同的节点
- this.tail 是一个"标签"，告诉我们当前哪个节点是尾部
```
基本逻辑：
1.先把新节点挂到当前尾节点的后面
2.然后更新tail标签，让新节点C成为新的尾部
- this.tail.next的存在是临时状态：在添加过程中，原来的尾节点暂时有next指向新节点，等添加完成后，新节点成为新的尾节点（next为null）
- 优势：其他线程中tail被修改，B→C的连接已经建立，不会出现孤岛节点。
```
- **先获取引用，再修改指针，操作顺序会影响中间状态**-"防御性编程"思想：尽量减少系统处于不一致状态的时间。

2. 代码实现
```
class DoublyNode {
    constructor(data) {
        this.data = data;
        this.next = null;   // 指向后一个节点
        this.prev = null;   // 指向前一个节点 
    }
}
class DoublyLinkedList {
    constructor() {
        this.head = null;    // 头指针
        this.tail = null;    // 尾指针 
        this.size = 0;
    }
}
addTask(taskText) {
    const newNode = new DoublyNode(taskText);
    
    if (this.head === null) {
        this.head = newNode;
        this.tail = newNode;  // 头尾都是新节点
    } else {
        // 直接操作tail，不需要遍历！，tail属于标签属性不是真正意义上的最后一个数字
        this.tail.next = newNode;  // 当前尾节点指向新节点
        newNode.prev = this.tail;  // 新节点指回当前尾节点///操作顺序：保证数据一致性，防止中间状态异常；双向连接：先建立单向连接，再补全反向连接；tail标签：用空间换时间，提升效率
        this.tail = newNode;       // 更新tail为新节点
    }}
    this.size++;
    
printAllTasks() {
        console.log("--- Doubly Linked List ---");
        let current = this.head;
        while (current !== null) {
            // 显示当前节点的数据，以及前后节点的数据（如果是null就显示'null'）
            const prevData = current.prev ? current.prev.data : 'null';
            const nextData = current.next ? current.next.data : 'null';
            console.log(`Data: ${current.data}, Prev: ${prevData}, Next: ${nextData}`);
            current = current.next;}

deleteFromTail() {
    //从尾部删除
    if (this.tail === null) {
        console.log("链表为空！");
        return false;
    }
    
    if (this.head === this.tail) {
        // 情况1：只有一个节点
        this.head = null;
        this.tail = null;
    } else {
        // 情况2：多个节点
        let newTail = this.tail.prev;  // 当前尾节点的前一个节点
        newTail.next = null;           // 新的尾节点next设为null
        this.tail = newTail;           // 更新tail指针
    }
    
    this.size--;
    return true;
}

deleteFromHead() {
    //从头部删除
        if (this.head === null) {
            return null; // 链表为空
        }
        
        const item = this.head.data;
        
        if (this.head === this.tail) {
            // 只有一个节点
            this.head = null;
            this.tail = null;
        } else {
            // 多个节点，基本逻辑：下一个节点直接覆盖前一个节点实现从头部删除
            this.head = this.head.next;
            this.head.prev = null;
        }
        
        this.size--;
        return item;
    }

//尾部添加：旧节点→新节点 先建立（因为新节点后面是null，没有其他节点受影响）
//中间插入：新节点→后节点 先建立（为了在修改前保存后节点的引用）
insertAtHead(taskText) {
    // 在头部插入新节点
    const newNode = new DoublyNode(taskText);
    
    if (this.head === null) {
        // 链表为空的情况
        this.head = newnode;
        this.tail = newnode;
    } else {
        // 链表不为空的情况
        newNode.next = this.head;    // 新节点指向原来的头节点
        this.head.prev = newnode;  // 原来的头节点指回新节点
        this.head = newnode;       // 更新头指针
    }
    this.size++;
    return true;
}

insertTaskAtIndex(index, taskText) {
    if (index < 0 || index > this.size) return false;
    
    if (index === 0) {
        // 在头部插入
        return this.insertAtHead(taskText);
    } else if (index === this.size) {
        // 在尾部插入
        this.addTask(taskText);
        return true;
    } else {
        // 在中间插入 - 这是最有趣的部分！
        const newNode = new DoublyNode(taskText);
        
        // 第一步：找到要插入位置的前一个节点
        let current = this.head;
        let count = 0;
        while (count < index-1) {
            current = current.next;//没有这行代码：current永远停留在A，无法找到正确的插入位置。
            count++;
        }
        
        // 现在current指向第(index-1)个节点
        // 第二步：建立新节点的连接
        newNode.next = current.next;        // 新节点指向current的下一个节点
        newNode.prev = current;        // 新节点指回current
        
        // 第三步：调整原有节点的连接
        current.next.prev = newNode;        // current的下一个节点的prev指向新节点
        current.next = newnode;        // current指向新节点
        
        this.size++;
        return true;
    }
}


}
```

### 反转链表
1. 混淆点
- 注意边界情况的处理prev的初始值是null;优秀的算法不是等遇到问题再修补，而是一开始就优雅地处理好所有情况;
- 每次只改变一个指针，但方向明确
- 循环过程中原本指向null的最后一个元素也指向null,循环的第一个元素可以单独一列指向null；
- prev 不是"循环后第一次指针的初始值"，而是"当前节点反转后应该指向的那个节点"；
- prev：永远指向已经反转好的部分链表的头节点
- current：当前要处理的节点
- nextTemp：还没有处理的剩余链表
- 每个节点在任一时刻都只有一个next指针
- 辅助变量(临时变量)来"保持状态"，让操作变得清晰可控
- 基本逻辑
```
1.让当前节点指向prev（连接到已反转部分）
2.把当前节点设为新的prev（更新已反转部分的头）
3.移动到下一个节点
```

2. 代码实现
```
reverse() {
    let prev = null;
    let current = this.head;
    while (current !== null) {
        let nextTemp = current.next;  // 保存下一个节点
        current.next = prev;          // 反转指针方向
        prev = current;               // prev前移
        current = nextTemp;           // current前移
    }
    this.head = prev;                 // 最后prev就是新的头节点
}
```

#  队列
## 基本概念
- 在尾部rear添加节点（入队enqueue）;在头部(front)删除节点（出队dequeue）
- FIFO  First In, First Out
- 队列是"包装器"而非"新数据结构",唯一属性就是包装的链表
- 栈和队列对比

|特性	|栈（Stack）	|队列（Queue）|
---|---|---
|原则	|LIFO（后进先出）|	FIFO（先进先出）|
|插入端	|顶部（同一端）	|尾部|
|删除端|	顶部（同一端）|	头部|
|应用	|函数调用、撤销|	消息处理、BFS|


## 注意事项
1. 混淆点
- 结构
```
栈顶:队首（front） → [A] ⇄ [B] ⇄ [C] → 栈底:队尾（rear）
   ↑               ↑               ↑
dequeue从这里   中间元素         enqueue从这里
出队                          入队
```
- 使用双向链表实现的优势：
```
入队（尾部添加）：O(1)时间 ← 有tail指针
出队（头部删除）：O(1)时间 ← 有head指针
```
- 队列并不直接操作节点，而是通过双向链表来实现功能
```
enqueue() → 调用链表的addTask()（尾部添加）
dequeue() → 调用链表的deleteFromHead()（头部删除）
peek() → 直接访问list.head.data
```
- 指针顺序问题
```
1.入队顺序
front → [A] ← rear
enqueue("B") 后：
front → [A] ⇄ [B] ← rear
enqueue("C") 后:
front → [A] ⇄ [B] ⇄ [C] ← rear
2.出队顺序
dequeue() 后（A出队）：front → [B] ⇄ [C] ← rear
dequeue() 后（B出队）：front → [C] ← rear
```
- 队列和栈的指针区别
```
1.
因为队列是先进先出：委托给链表
需要快速访问最早进来的元素（front指针）
需要快速在末尾添加新元素（rear指针）
而栈是后进先出，所有操作都在同一端，所以只需要一个top指针。自己管理指针
2.
栈的操作都在同一端，逻辑简单，自己管理更直接
队列需要头尾两端操作，双向链表已经完美支持这种模式
代码复用的原则：不要重复造轮子

```
- 注意先定义类
```
lass Queue {
    // ...队列定义
}
// 然后才能使用
const myQueue = new Queue(); 
```
- 队列是一个"接口适配器":
```
1.重用双向链表的所有能力
2.提供新的操作语义（FIFO vs 通用链表）
3.隐藏复杂的指针操作，提供简单API
```
2. 代码实现
```
//---- 基础实现-----//
class Queue {
    constructor() {
        this.list = new DoublyLinkedList();  // 唯一属性就是包装的链表
        // 没有 this.top, this.front, this.rear 等新属性！
    }
}
class Queue {
    constructor() {
        this.list = new DoublyLinkedList();  // 委托给链表
    }
    enqueue(item) {
        this.list.addTask(item);  // 调用链表的方法
    }
}
//通过链表实现队列
class DoublyLinkedList {
    constructor() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }  
    addTask(item) {
        const newNode = new DoublyNode(item);
        if (this.head === null) {
            this.head = newNode;
            this.tail = newNode;
        } else {
            this.tail.next = newNode;
            newNode.prev = this.tail;
            this.tail = newNode;
        }
        this.size++;
    }
    
    deleteFromHead() {
        if (this.head === null) {
            return null;
        }
        
        const item = this.head.data;
        
        if (this.head === this.tail) {
            this.head = null;
            this.tail = null;
        } else {
            this.head = this.head.next;//指针指向改变直接覆盖上一个数据
            this.head.prev = null;
        }
        
        this.size--;
        return item;
    }
}
//队列定义方式通常直接委托链表类
class Queue {
    constructor() {
        this.list = new DoublyLinkedList();
    }
     // 入队 - 在链表尾部添加
    enqueue(item) {
        this.list.addTask(item);
    }
    // 出队 - 从链表头部删除并返回
    dequeue() {
        if (this.isEmpty()) {
            return null;
        }
        return this.list.deleteFromHead();//// 委托给链表处理所有逻辑
    }

    //出队方法二：
     dequeue() {
        if (this.isEmpty()) {
            return null;
        }
        const item = this.list.head.data;  // 获取头部数据
        this.list.deletefromhead();                    // 删除头部节点
        return item;
    }
//方法对比：1.避免重复检查：队列的isEmpty()和链表的空检查可能重复2.单一责任原则：删除逻辑应该由链表负责3.代码更简洁：一行 vs 四行

    peek() {
        if (this.isEmpty()) {
            return null;
        }
        return this.list.head.data;
    }
    
    isEmpty() {
        return this.list.size === 0;
    }
    
    size() {
        return this.list.size;
    }
}

//-----广度优先搜索----在树或图中按层次遍历//
queue.enqueue(根节点);
while (!queue.isEmpty()) {
    const node = queue.dequeue();
    // 处理当前节点
    // 将子节点入队
}

//-----处理用户请求--------//
queue.enqueue("用户A的请求");
queue.enqueue("用户B的请求");
queue.enqueue("用户C的请求");

// 按顺序处理
while (!queue.isEmpty()) {
    const request = queue.dequeue();
    processRequest(request);
}



//-------打印任务队列---------//
const myQueue = new Queue();
myQueue.enqueue("第一个顾客");
myQueue.enqueue("第二个顾客");
// 不要再次用 const 声明 myQueue
-redeclaration of const myQueue 错误：为重复声明同一个变量
 const myQueue = new Queue();
 myQueue.enqueue("第一个顾客");
-Uncaught SyntaxError: redeclaration of const myQueue
    <anonymous> debugger eval code:1
在浏览器控制台中，如果你多次运行const myQueue = new Queue()，就会报这个错误。
因为：const声明的变量不能重复定义，而控制台会保留之前执行的变量。
-》刷新页面（最简单）
-》使用let而不是const，let myQueue = new Queue();myQueue.enqueue("第一个顾客");
// 如果需要重新测试，可以先赋值为null：myQueue = null;
myQueue = new Queue();  // 现在可以重新创建了
-》使用不同的变量名const myQueue1 = new Queue();myQueue1.enqueue("第一个顾客");const myQueue2 = new Queue();
myQueue2.enqueue("新的顾客");

// 完整的可运行代码{打印队列+用双向链表的形式实现括号匹配}
// 1. 所有类定义
class DoublyNode {
    constructor(data) {
        this.data = data;
        this.next = null;
        this.prev = null;
    }
}

class DoublyLinkedList {
    constructor() {
        this.head = null;
        this.tail = null; 
        this.size = 0;
    }
    
    addTask(item) {
        const newNode = new DoublyNode(item);
        if (this.head === null) {
            this.head = newNode;
            this.tail = newNode;
        } else {
            this.tail.next = newNode;
            newNode.prev = this.tail;
            this.tail = newNode;
        }
        this.size++;
    }
    
    deleteFromHead() {
        if (this.head === null) return null;
        const item = this.head.data;
        if (this.head === this.tail) {
            this.head = null;
            this.tail = null;
        } else {
            this.head = this.head.next;
            this.head.prev = null;
        }
        this.size--;
        return item;
    }
}

class Stack {
    constructor() {委托给链表
        this.list = new DoublyLinkedList();
    }
    push(item) { this.list.addTask(item); }
    pop() { return this.list.deleteFromHead(); }
    peek() { return this.isEmpty() ? null : this.list.head.data; }
    isEmpty() { return this.list.size === 0; }
    size() { return this.list.size; }
}

class Queue {
    constructor() {
        this.list = new DoublyLinkedList();
    }
    enqueue(item) { this.list.addTask(item); }
    dequeue() { return this.list.deleteFromHead(); }
    peek() { return this.isEmpty() ? null : this.list.head.data; }
    isEmpty() { return this.list.size === 0; }
    size() { return this.list.size; }
}

// 2. 括号匹配函数
function isParenthesesBalanced(str) {
    const stack = new Stack();
    for (let i = 0; i < str.length; i++) {
        const char = str[i];
        if (char === '(') {
            stack.push(char);
        } else if (char === ')') {
            if (stack.isEmpty()) return false;
            stack.pop();
        }
    }
    return stack.isEmpty();
}

// 3. 测试代码
console.log("=== 测试开始 ===");

// 测试栈
console.log("测试括号匹配:");
console.log("(())", isParenthesesBalanced("(())"));  // true
console.log("())", isParenthesesBalanced("())"));    // false

// 测试队列
console.log("测试队列:");
const testQueue = new Queue();  // 用testQueue而不是myQueue
testQueue.enqueue("第一个顾客");
testQueue.enqueue("第二个顾客");
console.log("队首:", testQueue.peek());
console.log("出队:", testQueue.dequeue());
console.log("新队首:", testQueue.peek());
console.log("=== 测试结束 ===");

```