1. 基本查询语法
- TABLE 类别 sum(金额) AS 总花费  == 想要显示的列1，想要显示的列2 ///文件概览的作用
- FROM 需要查找的问价路径名称 ===哪个文件夹
- WHERE contains(tags,"#finance")AND 类型 = "支出"====条件1 AND 条件2
- GROUP BY 分类===按照什么分组
- SORT sum(金额) DESC(descending)按照金额从高到低排序 //ASC(从小到大)  ===按照什么排序
- LIMIT 5 ==查看五条信息

2. #注意Frontmatter格式问题
- 必须有开头和结尾的---
- tags写法要正确，不要加引号或者用数组格式
```
tags:
  - research-question
```
- 确保正确的缩进(2个空格)
- 注意属性会自动话格式为正确的yaml
- 注意查询文件的正确且确认的路径
```
```dataview//查询带有标签的所有文件并且找出它的路径
TABLE file.name,file.folder
FROM #research-question 
```
```
```dataview//查询具体文件在哪个路径
TABLE file.name,file.folder
WHERE file.name="text1"
```

```
```dataview//精确找出文件路径
TABLE file.path
WHERE file.name= "text1"
```


- 查找相应的文件下某个文件名里的文件并且列举10条相关信息
```
```dataview
TABLE file.name
FROM "5-Knowledge-Garden(知识花园)"
LIMIT 10

```

```
```dataview//#列举某个文件夹和文件的名字并且限制查询多少条
TABLE file.name , file.folder
LIMIT 10

```

```
```dataview//#查找某个项目里所有的标签列举出来
LIST tags
WHERE tags
LIMIT 20
```

- 理解TASK关键字
查找某个任务项并且有任务列表- [  ]

```dataview//查询所有状态为调研的的任务项
```dataview
TASK 
WHERE 状态 = "调研中"
LIMIT 5
```
```
```dataview//查询所有该标签的的任务项并且列举出来
TASK 
FROM #research-question 
SORT file.name
LIMIT 10
```

- **理解tags**

[**注意Properties的语法**]：这是一种新的元数据格式用key::value来表示；查询tags时必须用DTV的JS函数来读取这种内联属性

```
```dataview//查询所有状态为调研中的文件
TABLE file.ctime,优先级,tags
FROM "file-path-name"
WHERE 状态="调研中"
```
```
```dataview//查询所有优先级为high的文件
TABLE 状态,下一步行动,tags
FROM "file-path-name"
WHERE 优先级 = "High"
```
```
```dataview//状态，优先级，标签同步筛选方案
TABLE WITHOUT ID
    file.link AS "文件夹",
    优先级 AS "优先级",
    状态 AS "状态",
    下一步行动 AS "下一步行动",
    tags AS "标签"
    
FROM "5-Knowledge-Garden(知识花园)/PX-01-Research"
WHERE 优先级
SORT 优先级 DESC,file.ctime DESC
```
```
```dataview//显示所有未完成的任务及其所在的文件
TASK
FROM "filename-path"
WHERE !completed #只显示未完成的任务
GROUP BY file.link #将任务按照他们所属的文件进行分组展示

```

```
```dataview//只显示有任务的文件名列表不显示具体任务内容
TABLE WITHOUT ID file.link AS "包含任务的文件"
FROM "filename-path"
WHERE length(file.tasks) > 0#包含任何任务的不论完成与否的所有文件
```

- 在字段中添加table时间的注意调用dateformat函数

```
TABLE 优先级, 状态, dateformat(file.cday, "yyyy年MM月dd日") AS "创建日期",投入时间
```

3. 注意事项
- 注意语法格式中的逗号或者冒号必须是英文
- 不允许在一个查询块中连续使用两个TABLE语句，可以替换为UNION合并两个查询
```
TBALE 类别,金额
FROM (
    SELECT "->总收入" AS 类别，sum(金额) AS (金额)
    FROM "file-path"
    WHERE contains(tags,"#finance")
    
    UNION ALL
    SELECT "->总支出 AS 类别，sum(金额) AS 金额"
    FROM "file-path"
    WHERE contains(tags,"#finance")
)
```
- 不能同时使用FROM（*在哪里找*） #research-question 和 WHERE（*指定找什么*） file.path= "..."//条件矛盾；只用from指定路径或者公用where过滤；不能同时用这两个词语来限定位置
