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