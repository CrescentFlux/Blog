## Set
- **Concept**
  - A set is an unordered collection of objects.The objects are also called the elements of the set. The expression a∈A indicates that the set A contains the element a .
  - Empty set: it is a special set  with no elements.
  - Singleton set: it's a set that contains exactly one element.
  - Subset: A set A is the subset of set B if and only if every elements of A is also an element of B.A⊆B means that the all elements of A are in B.Conversely,A⊇B .
  - Power set :The power set of a set S is a set of all subset of S. The expression is 𝒫(S).
  - Cartesian product:The Caretsian product of two set A and B denoted by A×B.mathematical expression :A×B ={a,b |a∈A ∧ b∈B}
  - Note:A₁× A₂× A₃,⋯,× Aₙ ={(a₁, a₂, a₃, ⋯, aₙ) | aᵢ∈ Aᵢ,i=1,2,3,...,n} 
  - set-builder notation with quantifiers: 
     - The Universal quantification of P(x) is taken over all elements of the set S . ∀x∈S(P(x)) means that ∀x(x∈S → P(x)) 
     - Conversely,Existential quantification : ∃x∈S(P(x)) / ∃x(x∈S → P(x)) 
  - Truth set:The truth set of predicate P(x) over a domain D is the set of all elements in D for which P(x) is true.Mathematical Notation:{x∈D|P(x)}
- **Operation**
  - Union: The union is a set that contains all elements which are in A or B(or both).Mathematical notation: A∪B ={x∈A ∨ x∈B}
  - Intersetion: The intersetion of two set A and B is the set containing all elements that are common to both A and B.Notation:A∩B = {x∈A ∧ x∈B}
  - Principle of inclusion-exclusion:|A ∪ B| = |A| + |B| - |A ∩ B|
  - Set difference: the set diffrence of  A and B,donated by  A \ B or A − B, is the set of all elements that are in A but not in B. Formally: A \ B = { x | x ∈ A and x ∉ B }.
  - Complement: Given universal set 𝕌,the complement of a set A means is the set of all elements in 𝕌 but not in A.notation:
  Ā = { x∈𝕌 | x∉A }
  - Set identity

    |Identity|Name|
    ---|---
    |`A ∩ U = A` <br> `A ∪ ∅ = A`|Identity Laws|
    |`A ∪ U = U` <br> `A ∩ ∅ = ∅`|Domination Laws|
    |`A ∪ A = A` <br> `A ∩ A = A`|Idempotent Laws|
    |`(A̿)= A`|Double Complement Laws|
    |`A ∪ B = B ∪ A` <br>`A ∩ B = B ∩ A`|Commutative Laws|
    |`A ∪ (B ∪ C) = (A ∪ B)∪ C`<br> `A ∩ (B ∩ C) = (A ∩ B) ∩ C`|Associative Laws|
    |`A ∪ (B ∩ C ) = (A ∪ B) ∩ (A ∪ C)`<br> `A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)`|Distributive Laws|
    |`(A ∩ B)ᶜ = Aᶜ ∪ Bᶜ`<br>`(A ∪ B)ᶜ= Aᶜ ∩ Bᶜ`|De Morgan‘s Laws|
    |`A ∪ (A ∩ B) = A`<br>`A ∩ (A ∪ B) = A`|Absportion Laws|
    |`A ∪ Ā = U` <br> `A ∩ Ā = ∅`|Complement Laws|

## Function 
- **Concept**
    - Function: Function  is also called mapping or transformation,The notation f(a)=b denotes f is the function from a to b,formally,we say ‘f maps a to b’.
    - Domain| Codomain: The set of all possible values is called the domain of f,The set into which all outputs fall is called the codomain of f; 
    - Image| Preimage| Range: if f(a)=b,we can say that b is the image of a under f,a is the preimage of b.the range of f is the collection of image that all elements in the domain.
    




    - Real-valued function |Integer-values function: A function is called real-valued whose a subset of the real numbers ℝ;Integer-values function is one whose codomain is a subset of the integer ℤ.Two real-value funcion or integer value funciton with the same domain can be added or multiplied.Formally,(f₁+f₂)(x) = f₁(x) + f₂(x); (f₁f₂)x = f₁(x)f₂(x)
    - Injection function:one-to-one funciton for which distinct elements in the domain have distinct images,That is, if f(a) = f(b),then necessarily a = b.Therefore,A strictly monotonic function (strictly increasing or decreasing )is injective,formally,∀x∀y(x<y→f(x)<f(y)) or ∀x∀y(x<y→f(x)>f(y)) 
    - Surjective function:∀y∃x( f(x)=y ),x ranges over the domain of f,the domain of y is the codomain of f.
    - Bijective function: Bijective = Injective + Surjective (Both one-to-one and onto)
    - Inverse function:if f: A → B is bijective,it's inverse function is f⁻¹: B → A;for every a∈A,b∈B, if f(a) = b， f⁻¹(b) = a。
    - Composition function:g is a function from setA to setB;f is function from setB to setC;for every a∈A, f ∘ g(a)=f( g(a)).
    - Graph of a function:it's a collection of ordered pairs(x, f(x))
    - Floor | ceiling: The floor of a real number x, denoted ⌊x⌋, is the greatest integer less than or equal to x.The ceiling of a real number x, denoted ⌈x⌉, is the smallest integer greater than or equal to x.
    - Factorial function:f(n)=n!;n! = n × (n−1)!
    - Partial function| Total function:partial function that maybe undefined for some elements in its source set(domain ⊆ source set).Total function that function is defined for every elements in its domain.

 - *Note :codomain and range*:

    |Concept|Core|Examples|
    |---|---|---|
    |Codomain|Possible|`Function Definition:`<br>`g: {Xiaoming, Xiaohong} → {Excellent, Good, Pass, Fail}`<br>`Mapping Rule:`<br>`g(Xiaoming) = Excellent; g(Xiaohong) = Good`<br>`Codomain: {Excellent, Good, Pass, Fail}`|
    |Range|Actucl|`Range: {Excellent, Good}`|