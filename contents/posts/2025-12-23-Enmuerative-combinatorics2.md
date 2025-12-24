## Permutations and Combinations with repetition

- permutations with repetition:permutation with repetition of n distinct objects taken r at a time is given by fomula `n^r`.
- combinations with repetition:combination with repetition of n distinct types taken r at a time ,is `𝐂(n+r-1,r)=𝐂(n+r-1,n-1)=(n+r-1)!/r!(n-1)!`.
- permutations of a multiset:for a multiset containing nᵢ indistinguishable objects of type i (for i=1,2...k),the number of distinct permutaions of all n= ∑nᵢ objects is `n!/n1!n2! ...nₖ!`
- Distribution problems:
  - Distinguishable objects and distinguishable boxes:distribute n distinct objects into k distinct boxes ,formally, `n!/n1!n2! ...nₖ!`
  - Indistinguishable objects and distinguishable boxes:for putting r Indistinguishable objects into r distinguishable boxs, fomula is `𝐂(n+r-1,n-1)`.
  - Distinguishable objects and InDistinguishable boxes:Stirling numbers of the second kind:`S(n, k) = (1/k!) * Σ_{i=0}^{k-1} [(-1)^i * C(k, i) * (k-i)^n]`
  - Indistinguishable objects and  InDistinguishable boxes:Integer Partition

## Generating permutations and combinations
- Generating permutation
  ```
  procedure next permutaion{the permutation a₁ a₂...aₙ}
  j:= n-1
  while aⱼ>aⱼ+₁:# find j 
  k:=n
  while aⱼ>aₖ :# find k
  k=k-1
  change aⱼand aₖ: {aₖ is the smallest number greater than aⱼ among the elements to its right}
  r:=n
  s:=j+1
  while r>s
  change aᵣ and aₛ:#reverse
  r=r-1 #move the pointers
  s=s+1
  {Arrange the suffix after postion j in incresing order.The resulting sequence a₁ a₂...aₙ is the next permutation}
  ```
- Generating combination
  ```
  procedure next bit string{bₙ₋₁bₙ₋₂...b₁b₀} #Essentially,it implements binary addition by one;carry propagation.
  i=0
  while bᵢ=1
    bᵢ=0
    i=i+1
  bᵢ=1
  ```
  ```
  procedure next r-combination{a₁,a₂...aᵣ}:
  i:=r #We select r numbers a₁ < … < aᵣ ≤ n. For the i-th position, there remain r−i numbers after it: aᵢ₊₁, …, aᵣ.
  while aᵢ=n-r+i# To make aᵢ as large as possible ,pick the following numbers consecutively,making the last one aᵣ=aᵢ + (r−i)
    i=i-1
  aᵢ=aᵢ+1
  for j=i+1 to r
    aⱼ= aᵢ+j-i
  //Input: an r-combination a₁ < a₂ < … < aᵣ from {1,2,…,n}
       //not equal to {n−r+1, …, n} (not the last combination)
  //Output: next combination in lexicographic order
  ```