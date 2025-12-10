##  Set
  - Cardinality : For sets A and B,|A| = |B| means A and B are equinumerous (have the same cardinality).|A| < |B| means the cardinality of A is strictly less than that of B.
  - Countable set : A set is countable if it is either finite or its elements can be put in one-to-one correspondence with natures of numbers N.Otherwise,it is uncountable.

## Sequence

  - sequence is a discrete structure consisting of an ordered list of elements.
  - Geometric sequence: it's the discrete counterpart of an exponential function f(x)= arⁿ; Formally,ar¹, ar², ar³, ... arⁿ(a,r is real-numbers) 
  - Arithmetic sequence: Arithmetic sequence is the discrete Analogue  of Linear function f(x)=dx+a,the domains are different. Formally,a,a+d,a+2d,...,a+nd...(a,d is real-numbers)
  - Recurrence relation: A recurrence relation for  a sequence  {aₙ} is a equation defines as aₙ using previous terms (e.g., aₙ = aₙ₋₁ - 8), along with initial values to start the sequence.
  - Fibonacci sequence:Formally,f₀ ,f₁, f₂,...,intial values f₀=0 ,f₁=1, recurrence sequence:fₙ =fₙ₋₁+fₙ₋2 , n=2,3,4...

## Summation

 - **Operation** 

    |Expresstion|Name|
    |---|---|  
    |`n`<br>`∑ aᵢ  = a₁ + a₂ + ... + aₙ`<br>`i=1`|`Summation notation`<br>`i=index variable`<br>`1:low limit`<br>`n:upperlimit`|
    |`Geometric sequence Non-closed：`<br>`a + ar + ar² + ... + arⁿ`<br>`Sₙ =：Closed Form`<br>` ⎧ a(rⁿ⁺¹ - 1)`<br>` ⎪ ―――――――――――    if r ≠ 1`<br>`  ⎨    r - 1`<br> ` ⎪`<br> ` ⎩ a(n+1)        if r = 1`|`Sum of Geometric sequence` |
    |`Non-closed：`<br>`Sₙ = 1 + 2 + 3 + ... + n`<br>`Closed Form：`<br>`Sₙ = n(n+1)/2`|`Sum of Arithmetic sequence` |
    | ` n`<br>`Σ   k² = 1² + 2² + 3² + ... + n²`<br>`k=1`<br>`Closed Form：n(n+1)(2n+1)/6`|`Sum of squares formula`|
    |`  n`<br>`Σ   k³ = 1³ + 2³ + 3³ + ... + n³`<br>`k=1`<br>`Closed Form：[n(n+1)/2]² = (1+2+...+n)²`|`Sum of cubes formula`|
    |`∀x real-value:absolute value<1`<br>`∞`<br>` Σ xⁿ = 1 + x + x² + x³ + ...=1/(1-x) `<br>` n=0`|`Geometric series sum formula`|
    |`∀x real-value:absolute value<1`<br>`  ∞`<br>`Σ   k·xᵏ⁻¹ = 1/(1-x)² `<br>` k=1 ` |`Derivative of a power series`|


## Matrix
  - A matrix is a rectangular array of numbers arranged in rows and columns.
  - square:if a matrix have the same number of rows and colums,it's called square.
  - Two matrix are equare if they have the same dimensions and all their corresponding entries are identical.
  - Transpose:The transpose of matrix is obtained by interchanging its rows and columns.
  - Matrix power: Matrix power refers to repeatedly multiplying a square matrix by itself.
  - 0‑1 matrix:Binary matrix is a matrix whose entries are all either 0 or 1
  - Boolean Power:it's the result obtained by repeatedly applying the boolean product operation to the same matrix.
  - Boolean Product:it's the operation of multiplying two 0-1 matrics using logical AND or OR.Formally,A ⊙ B is boolean product.
  - Matrix operations:


        For m×n  Matrix A=(aij​)n×n​ 和 n×p  Matrix B：
        C is m×p  Matrix，and
            ------------------------------------------       ------------------------------------------- 
                n                                            
            Cᵢⱼ = Σ Aᵢₖ · Bₖⱼ                                Bₖⱼ：k runs over all rows of B
                k=1                                          Aᵢₖ：the index k runs over all columns of A,
            Cᵢⱼ = Aᵢ₁B₁ⱼ + Aᵢ₂B₂ⱼ + Aᵢ₃B₃ⱼ + … + AᵢₖBₖⱼ      The number of columns of A = The number of rows of B.
            -------------------------------------------      ------------------------------------------- 
                                                             
            
                ─────────────────────────────                Cᵢⱼ = Aᵢⱼ + Bᵢⱼ
                        NameX  NameY                         A×B ≠ B×A
                Store1  [   1      2   ]                     ─────────────────────────────
                Store2  [   3      4   ]                     A, B is 0-1 matrix, C = A ⊙ B donoted： 
                ─────────────────────────────                C[i,j] = ⋁ₖ (A[i,k] ∧ B[k,j])
                        Price A Price B                      -----------------------------
                NameX   [   5      6   ]                     A = [1 0]     row：1, 2   B = [0 1]     row：1, 2
                NameY   [   7      8   ]                         [1 1]     column：1, 2    [1 0]  column：1, 2
                ─────────────────────────────                C = A ⊙ B → C[2,1]
                         Acost      Bcost                    C[2,1] = (A[2,1] ∧ B[1,1]) ∨ (A[2,2] ∧ B[2,1])
                Store1[    19        22    ]                             ↓
                Store2[    43        50    ]                           coordinate(2,1)
                                                                         ↓
                                                                       element1 
                                                            -------------------------------
                                                            Ais n×n Boolean matrix，The rth Boolean power of A is defined as:
                                                            A(1)=A;  A^(r)= A⊙A⊙⋯⊙A​​(r≥2)




       
       

      
      
        
    
