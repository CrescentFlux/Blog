## Permutations and Combinations with repetition

- permutations with repetition:permutation with repetition of n distinct objects taken r at a time is given by fomula `n^r`.
- combinations with repetition:combination with repetition of n distinct types taken r at a time ,is `𝐂(n+r-1,r)=𝐂(n+r-1,n-1)=(n+r-1)!/r!(n-1)!`.
- permutations of a multiset:for a multiset containing nᵢ indistinguishable objects of type i (for i=1,2...k),the number of distinct permutaions of all n= ∑nᵢ objects is `n!/n1!n2! ...nᵢ!`
  - Distribution problems:
  - Distinguishable objects and distinguishable boxes:distribute n distinct objects into k distinct boxes such that box i receives exactly nᵢ objects,fomula  `n!/n1!n2! ...nᵢ!`
  - Indistinguishable objects and distinguishable boxes:for putting r Indistinguishable objects into r distinguishable boxs,it's fomula is `𝐂(n+r-1,n-1)`.
  - Distinguishable objects and InDistinguishable boxes:Stirling numbers of the second kind:`S(n, k) = (1/k!) * Σ_{i=0}^{k-1} [(-1)^i * C(k, i) * (k-i)^n]`
  - Indistinguishable objects and  InDistinguishable boxes:Integer Partition

## Generating permutations and combinations
