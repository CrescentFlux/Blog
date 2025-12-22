## The basic principle of counting
- The multiplication principle:if an operation can be performed in m ways,and a second independent operation can be performed in n ways,then the two operations can be performed togerther in m×n ways.
- The addition principle:if two tasks are mutually exclusive ,and the frist can be done in m ways,the second in n ways,then there are m+n ways to choose one of these tasks.
- Inclusion-exclusion principle:For two sets of methods,if a task can be performed either by n1 methods from a frist set or by n2 methods from a second set,and there are c methods that belong to both sets,then the total number of distinct ways to perform the task is :`n1+n2-c`,formally,`|A ∪ B| = |A| + |B| - |A ∩ B|`
- Division principle:if an initial count yeilds N ways to perform a task,and every distinct ways is counted exactly d times in that initial count,then the number of truly distinct ways is `N/d`.
- Pigeonhole principle:if at least n+1 objects are placed into n boxes,then there must be a box with two or more objects.
  - Generalized pigeonhole principle:if we put N objects into k boxes,then at least one box contains at least `N/k` objects.
  - Every sequence of `n²+1` distinct real numbers contains a monotonic (either increasing or decreasing) subsequence of length `n+1`.

## Permutation and Combination

- The number of r-permutations of an n-element set:it's the number of ways to arrange r distinct elements chosen from the set in a sequence.formally,`𝐏(n,r)=n(n-1)(n-2)...(n-r+1)` ;`𝐏(n,r)`=`n!/(n-r)!`
- The number of r-combinations is an unordered selection of r distinct elements from the set,and is given by the formula:`𝐏(n,r)=n!/r!(n-r)!`
## Binomial coefficients and Identity
- Binomial Theorem:`(x + y)ⁿ =  Σ_{k=0}ⁿ (ⁿₖ) xⁿ⁻ᵏ yᵏ`,where` (ⁿₖ) = n!/(k!(n-k)!)` is the binomial coefficient.
  - If n is non-negative integer:` Σ_{k=0}ⁿ (ⁿₖ)=2ⁿ`
  - if n is postive integer:` Σ_{k=0}(-1)ᴷ(ⁿₖ)=0`
  - If n is non-negative integer:` Σ_{k=0}2ᴷ(ⁿₖ)=3ⁿ`
- Pascal's Identity:For postive integers k>=n:`(ⁿ⁺¹ₖ) = (ⁿₖ₋₁) + (ⁿₖ)`
  - Pascal's Triangle:Every other number is the sum of the two numbers diagonally above it,Each row starts and ends with 1.
  - C(n+1,k)：the entry in row n+1, column k ;C(n,k−1)：The number in the row n, column k-1 (its upper-left neighbor);C(n,k)： The number in the row n, column k (its upper-right neighbor).
- Vandermonde's Identity:`C(m + n, r) = Σ_{k=0}^{r} C(m, r-k) * C(n, k)`
  - If n is non-negative integer:`  (ⁿ₂ₙ)=Σ_{k=0}ⁿ(ⁿₖ)²`
  - If n,r,r<=n is non-negative integer:`C(n+1,r+1)=Σ_{k=r}ⁿC(j,r)`