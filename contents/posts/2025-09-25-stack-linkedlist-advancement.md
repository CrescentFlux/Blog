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
|插入元素|	O(1)	|O(1)或O(n)|	
|删除元素|	O(1)	|O(n)	|
|随机访问|	o(n)	|O(1)	|
|查看顶部/头部|	o(1)|o(1)	|

## 注意事项
1. 混淆点
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
- 双向链表通常维护tail（尾指针），从尾部操作也很方便;双向链表通过维护tail指针，用少量额外空间换来了尾部操作的O(1)时间复杂度
- 在尾部添加节点：双向链表（直接操作tail，无需遍历）;单向链表（需要遍历到最后）;
- 反向遍历：可以从tail开始，用prev指针倒着走
- 删除节点更方便：要删除某个节点，直接修改它前后节点的指针就行
- 尾部操作高效：因为有tail指针，在尾部添加节点是O(1)时间
- 节点实现
```
head → [A] <--> [B] ← tail
       ↑        ↑
    prev=null  prev=A
    next=B     next=null
```
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
- **先获取引用，再修改指针，操作顺序会影响中间状态**-"防御性编程"的思想：尽量减少系统处于不一致状态的时间。

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