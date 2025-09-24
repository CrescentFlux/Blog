# 数组(Array)
## 基础概念
- [0,1,2, ...]每个元素都有固定的编号，比如 0号、1号、2号...
- 优点：元素连在一起，快速随机访问
- 缺点：想在中间（比如1号和2号之间）插入一个编号，会非常麻烦
## 注意事项
1. **混淆点**

|操作	|链表|	数组|	对比|
---|---|---|---
内存分配|	动态分配，不连续	|连续内存块	|数组更紧凑，链表更灵活
随机访问|	O(n) - 必须遍历|	O(1) - 瞬间完成	|数组直接访问元素，链表必须从头找
头部插入|	O(1) - 改变指针|	O(n) - 移动所有元素	|链表擅长插入元素会很快，数组插入元素会很慢
尾部添加|	O(n) - 需要遍历到最后	|O(1) - 直接放在末尾|链表在末尾添加很慢	数组在末尾添加很快
中间插入/删除|	O(1) - 改变指针|	O(n) - 移动元素	|链表只需改连接，数组需要所有元素全部移动

- 数组的随机访问快：数组获取第5000个元素：直接 tasks[5000]，瞬间完成；元素地址 = 数组起始地址 + 索引 × 元素大小
- 链表在头部插入更快：只需要改变head指针，不需要移动任何现有数据
- 需要频繁随机访问 → 数组；需要频繁在头部/中间插入删除 → 链表
- 链表的结构决定了只能从头开始一个个找所以需要for循环
- 必须从后往前移动！ 如果从前往后会覆盖数据
- 插入逻辑要从后往前挪出空位然后在index位置插入新的元素
- 删除逻辑如果从i=0开始，会移动所有元素，只想移动删除位置之后的元素需要i = index


2. **代码实现**
```
class todolistwitharray(){
    this.tasks=[];
    this.size=0;
    addtask(){
        this.tasks[this.size]=tasktext;
        this.size++;//在数组末尾直接添加文本
    }
    printalltask(){//遍历所有元素
        for(i=0,i<this.size,i++){
        console.log(`${i + 1}. ${this.tasks[i]}`)
        }
    }
    getTaskAtIndex(index) {
    if (index < 0 || index >= this.size) return null;
    return this.tasks[index];  // 直接返回第index个元素; //返回第index个任务
}
    insertTaskAtIndex(index, taskText) {
    if (index < 0 || index > this.size) {
        console.log("无效的位置！");
        return false;
    }
    // 关键步骤：从后往前，把每个元素向后移动一位
    for (let i = this.size; i > index; i--) {
        this.tasks[i] = this.tasks[i - 1];
    }
    // 在空出的位置插入新元素
    this.tasks[index] = taskText;
    this.size++;
    return true; 
}    
    deleteTaskAtIndex(index) {
    if (index < 0 || index >= this.size) {
        console.log("无效的位置！");
        return false;
    }
    // 从要删除的位置开始，把后面的元素都向前移动一位
    for (let i = index; i < this.size - 1; i++) {
        this.tasks[i] = this.tasks[i + 1];
    }
    this.size--;
    return true;
}}
```

# 链表 (Linked List)
## 基础概念
- 原始链表包括节点和链表类
- 每个节点会指出两件事：1. 这里有什么数据 2. 下一个节点的地址/指针
- 缺点：顺序访问，无法随机访问
- 优点：中间插入一个新的编号，非常容易
```
找到要插入位置的前一个编号
让新编号的“下一个线索”指向前一个编号原本指向的地方
让前一个编号的“下一个线索”指向这个新编号
```
## 注意事项
1. **混淆点**
- head是一个“入口点”或“起点标记”。没有它，链表现在内存里，但你丢失了它的地址，它就永远找不到了，相当于内存泄漏。
- 删除逻辑:找到节点B的前一个节点A，让A的next直接指向C跳过B
- current
```
真正的连接：是由每个节点自带的指针完成的，current只是帮我们找到该修改哪个节点的next指针。
current本身不进行连接，它只是告诉代码在哪里进行连接，它只具备标签属性
```
- 变量赋值 vs 属性赋值
```
const/let：只控制变量名本身能不能被重新赋值，不影响它指向的对象有什么属性。
```
- 两个花括号爆红的问题
```
括号不匹配：比如少了一个括号
在错误的地方写了代码：比如把方法写到了类的外面。
```
- 真正的执行操作
```
newNode = new Node(taskText)：创建节点
current.next = newNode：通过current连接节点
```
- 插入逻辑注意事项
```
1.注意插入位置的前一个节点是index-1
2.基本逻辑：
head -> [A] -> [B] -> [C] -> null
-找到索引0的节点[A]
-新节点[X]指向[B]
-[A]指向[X]
结果应该是：
head -> [A] -> [X] -> [B] -> [C] -> null
3.注意理解赋值的方向
- 赋值语句 a = b 的执行顺序是：
先计算右边的 b（得到一个值）
再把计算出的值赋给左边的 a
- 先连接新节点的后方；再连接新节点的前方；两个赋值操作是完全独立；
顺序绝对不能颠倒
```

2. **代码实现**
```
class Node{
    constructor(){
        this.data=data
        this.next=null
    }   
}
class todolist{
    constructor(){
        this.head=null
        this.size=0
    }   
    addTask(tasktext){
        const newNode = new Node(taskText)
        if this.head===null{
            this.head = newNode;
        }else{
           let  current = this.head;// 手写临时标签
           while(size!==0){
             current=curent.next//移动标签相当于遍历
           }
           current.next=newNode;
        }

    }
    this.size++;
    inserttaskIndex(inserttask){
        if (index < 0 || index > this.size) {
        console.log("无效的位置！");
        return false;
    }
    if (index === 0) {           //如果插入到头部索引为0
        newNode.next = this.head
        this.head = newnode
    } else {
        let current = this.head;
        let count = 0;
        while (count < index-1) {
            current = current.next;
            count++;
        }
        newNode.next = current.next;// 新节点指向current的下一个节点
        current.next = newnode ;// current指向新节点
    }
    this.size++;
    return true;
    }
    deleteTaskAtIndex(index) {
    if (index < 0 || index >= this.size) {
        console.log("无效的位置！");
        return false;
    }
    if (index === 0) {
        this.head = this.head.next;  
    } 
    else {
        let current = this.head;
        let count = 0;
        while (count < index - 1) {
            current = current.next;
            count++;
        }
        current.next = current.next.next;//下下个节点
    }
    this.size--;
    return true;
    }
    printAllTasks() {
        console.log("--- Todo List (LinkedList) ---");
        let current = this.head;
        let index = 1;
        while (current !== null) {
            console.log(`${index}. ${current.data}`);
            current = current.next;
            index++;
}}
}
```


