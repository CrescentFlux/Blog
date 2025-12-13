## Alogrithm 

- Polynomial Dominance Lemma:
     ```
     |f(n)| = | aₖnᵏ+aₖ₋₁nᵏ⁻¹+ ... +a₁n+a₀|<= |aₖ|nᵏ+|aₖ₋₁|nᵏ⁻¹+ ... +|a₁|n+|a₀|
                                            = nᵏ(|aₖ|+|aₖ₋₁|/n+ ... +|a₁|/nᵏ⁻¹+|a₀|)
                                           <= nᵏ(|aₖ|+|aₖ₋₁|+ ... +|a₁|+|a₀|)
                                           <= nᵏ(|aₖ|+|aₖ₋₁|+ ... +|a₁|+|a₀|)
     x>1, |f(n)|<= 𝐂nᵏ,𝐂 is scaling factor
    ```
- For any polynocmical function, there extists an exponential function that asymptotically dominates it.The converse does not hold,bₙ is grower faster than any constant multiple of nᵏ.∀ k>0 ,b>1,nᵏ=O(bₙ) ;There exstists constants C,for all n,n≥n₀​：nᵏ≤C⋅(bₙ).  Polynomical growth: fixed exponent,variable base; Exponential growth:fixed base,variable exponent;

- For every c>0,log n = 𝐎(nᶜ);For any postive constant c,the logarithmic funcition is log n is in 𝐎(nᶜ).This establishes that logarithmic growth is strictly asysmptotically dominated by polynomical growth of any postive degree.

- lognᵏ=Θ(logbᵏ),Logarithms with different bases differ only by a constant factor.

- Ω notation:f(n)=Ω(g(n)),There extists if and only if postive constants C 和 n₀​，for all n≥n₀​：|f(n)|≥C⋅|g(n)| ,C is lower bound scaling factor.

- Θ notation:f(n)=Θ(g(n)) means the function grows proportionally to g(n) asymptotically.Formally, C1​|g(x)|≤|f(x)|≤C2​|g(x)|,C is two-side scaling factor.

- Computational complexity :It encompasses both time complexity and space complexity.
  - Constant complexity ; Linear complexity;Logarithmic complexity;Linearithmic logarithmic complexity;Polylomial complexity.

- Np complete problem:NP problem are the hardest problems in NP.NP = Nondeterministic Polynomial time
