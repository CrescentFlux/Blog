## Number Theory

- Prime number:it's divisable only by itself and 1 .Any other natural number greater than 1 is a composite number.

 - The Foundamental Theorem of Arithmetic:For every integer greater than 1 can be represented uniquely as a product of prime numbers,up to the order of the factors.

 - Trial Division: If n is a composite number,it must have at least one prime factor less than the square root of n.

 - Sieve of Eratosthenes :it's an ancient algorithm for finding all prime numbers up to any given limit n.
 - The infinitude of prime:it's the theorem stating that the set of prime numbers is unboaded and infinite,there is no largest prime.
- Greatest common divisor:For two integers a and b,no both zero,their gcd is the largest postive integer d that divides both a and b.Formally, gcd(a,b).
   - If the greatest common divisor of two numbers  is 1,we say they are coprime.formally,1<=i<=j<=n,gcd (aᵢ,aⱼ)=1.
- Least common multiple:it's the smallest postive integer that is divisable by a and b.formally ,lcm(a,b).
- Euclidean Algorithm:A method for finding the greatest common divsor of two integers.formally,it's based on the proprety that for integers a ,b with b ≠0, given `a=bq+r`,then `gcd(a,b)=gcd(b,r)`,the algorithm repeated this process until find the gcd.
  ```
  procedure gcd (a,b is postive integer)
  x :=a
  y :=b
  while y≠0,
    r := x mod y
    x := y
    y := r
  return x(x=gcd(a,b))
  ```
  - The Linear Combination of GCD:formally ,the linear combination of gcd is the sa+tb for integer a,b.
  - Bézout's Identity:For any postive integer a,b:gcd(a,b) = sa + tb
  - Euclid's Lemma:For postive integer a,b,c:if gcd(a,b) = 1, a|bc,a|c.
  - For postive integer m,integer a,b,c ;if ac ≡ bc(mod m) and gcd(c,m)=1,then a ≡ b(mod m)

- Slove a congruence Equation:
   - Linear congruence equation:An equation of the form` ax ≡ b(mod m)`,where a,b,m are integers with m>0(m is modulus),and we seek the integer solutions for x.
   - The congruence has a solution if and only if `gcd(a,m)|b`.
   - Modular inverse:the modular inverse a of a modulo m is an integer x such that `ax≡1(mod m)`,and it extists if and only if `gcd(a,m)=1`.Formally ,a⁻¹(mod m).
   - Logical chain for Solving ax≡b(mod m):
     - Find modular inverse
     - multiply modular inverse both sides 
     - simplify:in modular arthmetic it can be replaced by its reminder.
     - Solution:x ≡ j (mod n) means that:x = j + nk, where k is any integer.

- Chinese Reminder Theorem: if moduli m₁,m₂​,…,mₖ​  are pairwise coprime,then the system of congruence `x≡aᵢ​(mod mᵢ​)` have a unique solusion modulo M=m₁,m₂​,…,mₖ.Logical chain:
    - Compute the product M of all moduli.：`M=m₁​×m₂​×⋯×mₖ`
    - For each i, compute：`Mᵢ​=M/mᵢ`
    - Find the modular inverse of Mᵢ modulo mᵢ：find tᵢ such that：`Mᵢ​⋅tᵢ​≡1(mod mᵢ​) `(gcd⁡(Mᵢ,mᵢ)=1gcd(Mᵢ​,mᵢ​)=1，there extists modular inverse)
    - Combine the partial solutions：`x= a₁​M₁​t₁​+a₂​M₂​t₂​+⋯+aₖ​Mₖ​tₖ(mod M)`
- Fermat's Little Theorem: formally,if k is prime,a is a integer for can not be divisable by k,then `aᴷ⁻¹≡1(mod p)`,and for every integer a,`aᴷ≡a(mod p) `.
- Pseudoprime:let b be a postive integer,n is called pseduprime to base b if gcd(b, k) = 1 and b ᴷ⁻¹=1(mod n).[Passing the fermat test does not guarantee primality]