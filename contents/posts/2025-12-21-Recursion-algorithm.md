## Recursion Algorithm
- recursion algorithm:It's one where a problem is solved by into smaller,similar sub-problems.
   ```
   The recursion algorithm of factorial n
   procedure factorial (n:non negetive integer)
   if n=0 then return 1
   else return n · factorial(n-1)
   the output is n factorial
   ```
   ```
   The recursion algorithm of aⁿ
   procedure power (a:non-zero real number,n:non negetive integer)
   if n=0 then return 1
   else return a · power(a,n-1)#aⁿ = a × aⁿ⁻¹
   the output is aⁿ
   ```
   ```
   The recursion algorithm of gcd(a,b)
   procedure gcd(a,b: non negetive integer,a<b)
   if a=0 then return b
   else return gcd(b mod a ,a)
   the output is gcd(a,b)
   ```
   ```
   Recursive modular exponentiation
   procedure mpower (b,n,m integer and b>0,m>=2,n>=0)
   if n=0 then return 1
   else if n is even number #Exponentiation by Squaring
      return mpower(b,n/2,m)² mod m   
      #b²ᵏ = (bᵏ)²:when we want to caculate a number raised to the power of 2k ,we can frist caculate it raised to the power of k,then square the result.
   else 
   return((mpower (b,⌊n/2⌋,m))² mod m · b mod m)mod m #b²ᵏ⁺¹ = (bᵏ)² * b
   the output is bⁿ mod m
   ```
   ```
   Recursive linear search algorithm
   procedure search(i,j,x:integer 1 <= i <= j <= n)
   if aᵢ = x return i
   else if i=j then return 0
   else return search(i+1,j,x)
   the output is the index of target elements within array a[1...n] ,or 0 it's not present.
   ```
   ```
   Recursive binary search algorithm
   procedure binary search(i,j,x:integer 1 <= i <= n,1 <= j <= n)The array must be sorted in ascending order.
   m= ⌊(i+j)/2⌋
   if x=aₘ then return m
   else if (x<aₘ and i<m) then 
       return binary search(i,m-1,x)
   else if (x>aₘ and j>m) then
       return binary search (m+1,j,x)
   else return 0
   the output is the index of target elements within array a[1...n] ,or 0 it's not present.
   ```

