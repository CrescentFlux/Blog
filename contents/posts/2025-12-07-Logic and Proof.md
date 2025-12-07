## Logic Symbols Basic Rules

- **Truth Table**

|p |q| $ p \land q $| $ p \lor q$|$ p \oplus q$|$ p \to q$|$ p \leftrightarrow q $|
|---|---|---|---|---|---|---|
|T|F|F|T|T|F|F|
|F|T|F|T|T|T|F|
|T|T|T|T|F|T|T|
|F|F|F|F|F|T|T|
|$ p \to q $|$ \neg p\to\neg q$|$ \neg q \to \neg p$|
|T|F|T|
|运算优先级|$ \forall, \exist$|$ \neg $|$  \land  $|$  \lor $|$  \to $|$  \leftrightarrow  $|


- **Logically equivalent**

|p|$ \neg p$|$ p \lor \neg p$|$ p \land \neg p$|
---|---|---|---|
|T|F|T|F|
|F|T|T|F|
|contingency|contingency |tautology|controdiction|

- **logical equivalence(Augustus De Morgan )**


|$ \neg (p \land q) \equiv \neg p \lor \neg q $ <br> $ \neg(p \lor q) \equiv \neg p \land \neg q$|
---|

- **Predicate logic/Propositional Function and Quantifiers**

  - 谓词 = 带变量的命题模板; 谓词是命题的函数：输入个体，输出命题; 谓词 = 谓词符号 + 个体变元
  - 量词让谓词变成命题
  - Comparison

  |Proposition|T|F|
  |---|---|---|
  |$ \forall {_x}P_{(x)}$|For every x in the domain, P(x) holds for all x // For every x,P(x) is true.| There exists an x such that P(x) is false.|
  |$ \exists {_x}P_{(x)}$|There exists an x such that P(x)//There exists an x such that P(x) is true.| For every x,P(x) is false.|

    | Negation of quantified expressions|T|F|
    |---|---|---|
    |$ \neg \forall {_x}p{(x)} \equiv \exists{_x}{}_\neg p{(x)}$|There exists an x such that P(x) is false.|For every x,P(x) is true.|
    |$\neg \exists {_x}p{(x)} \equiv \forall{_x}{}_\neg p{(x)}$|For every x,P(x) is false.|There exists an x such that P(x) is true.|

    |Nested Quantifiers|Meaning|
    |---|---|
    |$ \forall x\exists y(x+y=0)$|For every x, there exists a y such that x + y = 0|
    |$ \neg \exists \mathcal w \forall a f(p (\mathcal w,f))\land \mathcal{q}(f,a)$|$\equiv \forall\mathcal{w}{}_\neg \forall a f(p (\mathcal w,f))\land \mathcal{q}(f,a) \equiv \forall \mathcal{w} \exists \mathcal{a} {}_\neg f(p (\mathcal w,f))\land \mathcal{q}(f,a) \equiv \forall \mathcal{w} \exists \mathcal{a} f {}_\neg (p (\mathcal w,f))\land \mathcal{q}(f,a) \equiv \forall \mathcal{w} \exists \mathcal{a} f ({}_\neg p (\mathcal w,f))\lor {}_\neg \mathcal{q}(f,a) $|
