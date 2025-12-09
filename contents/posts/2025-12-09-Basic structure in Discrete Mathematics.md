## Set
- **Concept**
  - A set is an unordered collection of objects.The objects are also called the elements of the set. The expression a∈A indicates that the set A contains the element a .
  - Empty set: it is a special set  with no elements.
  - Singleton set: it's a set that contains exactly one element.
  - Subset: A set A is the subset of set B if and only if every elements of A is also an element of B.A⊆B means that the all elements of A are in B.Conversely,A∉B .
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
    |`A ∪ B = B ∪ A` <br>` A ∩ B = B ∩ A`|Commutative Laws|
    |`A ∪ (B ∪ C) = (A ∪ B)∪ C`<br> `A ∩ (B ∩ C) = (A ∩ B) ∩ C`|Associative Laws|
    |`A ∪ (B ∩ C ) = (A ∪ B) ∩ (A ∪ C)`<br> `A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)`|Distributive Laws|
    |`(A ∩ B)ᶜ = Aᶜ ∪ Bᶜ`<br>`(A ∪ B)ᶜ= Aᶜ ∩ Bᶜ`|De Morgan‘s Laws|
    |`A ∪ (A ∩ B) = A`<br>`A ∩ (A ∪ B) = A`|Absportion Laws|
    |`A ∪ Ā = U` <br> `A ∩ Ā = ∅`|Complement Laws|