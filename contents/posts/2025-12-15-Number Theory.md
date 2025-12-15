

## Number Theory

- Divisiblity:Divisiblity is checked by the modulo operator .if a % b == 0,then b divides a.The reminder concept is what makes modular arithmetic work.
- Division:For integer a,b with a≠0,we say a divise b if there extists an integer c such that b=ac;Commonly ,a is the   divisor or factor of b,b is the multiple of a.Formally ,a | b .conversly,we can say a ∤ b.
- Theorem :For integer a,b,c,with a≠0:
   - if a | b ,a | c,then a | (b+c)
   - if a | b ,for all integer c,has a | bc
   - if a | b ,b | c,then a | c.
   - if a | b ,a | c,for integer s,t,b = as,c=at,then b+c=as+at.
   - Corollary:if integer a,b,c,with a≠0,and a | b ,a | c,if m,n is integer ,then a |mb+nc
- Division algorithm: For any integer a and postive integer b,there exist unique integers q(quotient) and r(remainder) such that:a=bq+r ,with 0≤r<b.
- Congruence:Integers a and b has the same reminder in modulo m.Formally,a ≡ b is congruence,m is modulus;a ≡ b (mod m) ⇔ m | (a - b) ⇔ a % m == b % m
- Congruence class:it is the set of all integers that  have the same reminder module m.
  - Theorem:Given postive integer m,if a ≡ b(mod m),c ≡ d(mod m) → a+c ≡ b+d(mod m) and ac ≡ bd.
  - Corollary:postive integer m,integer a,b:(a+b) mod m = ((a mod m) +(b mod m))mod m,and ab(mod)m = (a mod m)(b mod m)(mod m)

- Module Arithmetic:Formally,a + ₘb=(a+b)mod m;a ⋅ ₘb=(a ⋅ b)mod m;
  - Colsure:If a ,b ∈ 𝐙ₘ ,a + ₘb and a ⋅ ₘb ∈ 𝐙ₘ;
  - Associalativity:If a,b,c ∈ 𝐙ₘ,(a + ₘb)+ₘc=a+ₘ(b+ₘc);(a ⋅ₘb)⋅ₘc=a ⋅ ₘ(b⋅ₘc)
  - Commutativity:a + ₘb = b + ₘa;a ⋅ₘb = b⋅ ₘa
  - Identity element:element 0 and element 1 is the identity element of the plus and multiply in module.if aₘ ∈ 𝐙,a + ₘ0=0+ₘa;a ⋅ₘ1=1 ⋅ₘa=a.
  - Addtive inverse:if a≠0,∈𝐙,m-a is the addtive inverse of module m in a.0 is the addtive inverse of itself.a + ₘ(m-a)=0,and 0 + ₘ0=0.
  - Distributivity:if a,b,c ∈ 𝐙ₘ,a ⋅ₘ(b+ₘc) =(a ⋅ₘb) + ₘ(a ⋅ₘc)