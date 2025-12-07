## Logic Symbols Basic Rules



- **Truth Table**

|p |q| p ∧ q |  p ∨ q| p ⊕ q| p → q| p ↔  q |
|---|---|---|---|---|---|---|
|T|F|F|T|T|F|F|
|F|T|F|T|T|T|F|
|T|T|T|T|F|T|T|
|F|F|F|F|F|T|T|
|p → q | ¬ p→ ¬ q|¬ q → ¬ p|
|T|F|T|
|运算优先级|∀ ∃|¬|∧|∨|→| ↔ |


- **Logically equivalent**

|p|¬ p| p ∨ ¬ p|p ∧ ¬ p|
---|---|---|---|
|T|F|T|F|
|F|T|T|F|
|contingency|contingency |tautology|controdiction|

- **logical equivalence(Augustus De Morgan )**


| ¬ (p ∧ q) ≡ ¬ p ∨ ¬ q  <br>  ¬(p ∨ q) ≡ ¬ p ∧ ¬ q|
---|

- **Predicate logic/Propositional Function and Quantifiers**

  - 谓词 = 带变量的命题模板; 谓词是命题的函数：输入个体，输出命题; 谓词 = 谓词符号 + 个体变元
  - 量词让谓词变成命题
  - Comparison

  |Proposition|T|F|
  |---|---|---|
  |∀ₓP₍ₓ₎|For every x in the domain, P(x) holds for all x // For every x,P(x) is true.| There exists an x such that P(x) is false.|
  |∃ₓP₍ₓ₎|There exists an x such that P(x)//There exists an x such that P(x) is true.| For every x,P(x) is false.|

    | Negation of quantified expressions|T|F|
    |---|---|---|
    | ¬ ∀ₓP₍ₓ₎ ≡ ∃ₓ¬P₍ₓ₎|There exists an x such that P(x) is false.|For every x,P(x) is true.|
    |¬∃ₓP₍ₓ₎≡∀ₓ¬ P₍ₓ₎|For every x,P(x) is false.|There exists an x such that P(x) is true.|

    |Nested Quantifiers|Meaning|
    |---|---|
    | ∀ x ∃ y(x+y=0)|For every x, there exists a y such that x + y = 0|
    |¬∃w∀a F {p(W,f)}∧q(f,a)|≡ ∀w¬∀a F {P(W,f)}∧q(f,a) ≡ ∀w∃a¬F{p(W,f)}∧q(f,a) ≡ ∀w∃a F¬{p(W,f)}∧q(f,a)≡ ∀w∃a F(¬{p(W,f)} ∨¬q(f,a))






