## Discrete probability
- Finite probability:In finite probability,Event E is a subset of finite sample space S.when outcomes are all equally likely,the probability of E is given by classical fomula:`p(𝐄)=|𝐄|/|𝐒|`,consequently,`0<=p(𝐄)<=1`.
- Probability of the complement of an event:Let E be an event of finite sample space S,the probability of Complement of it's complement,donoted Ē is given by `p(Ē)=1-p(E)`.
- Probability of  the union of two events :Let E₁ and E₂ be two events in a finite sample space S,fomula is `p(E₁∪ E₂)=p(E₁)+p(E₂)-p(E₁∩E₂) `

## Probability theory
- Probability distribution:Let a finite sample space S have n elementary outcomes.Let x be an random variable that assigns a numberical valuexᵢ to each outcome. The probability distribution of x is given by the set of probabilities:`p(ᵢ)=P(x=xᵢ)`,for i=1,2...n,which must satisfy the following two axions:0<=p(ᵢ)<=1,∑(i=1...n)p(xᵢ)=1,the function p is called the probability distribution of X on S.
- The probability of an event is defined as the sum of probabilities of all elementary outcomes that constitute that event.this expressed formally as: `P(E) = Σ_{x∈E} P(x)`
- Additivity Axiom:Let A₁A₂A₃...be a finite sequence of pairwise disjiont events,then the probability of their union is the sum of their probabilities:` P(⋃ᵢAᵢ)=∑ᵢP(Aᵢ)`，provided that Aᵢ∩Aⱼ=∅（for all i≠j）
- Conditional probability:Let E and F be events with p(F)>0,the conditional probability of E given F ,donated by p(E|F),is defined as `p(E|F)=p(E∩F)/p(F)`.
- Independence of Events: Events E and F are independent ,if and only if `p(E∩F)=p(E)p(F)`.They can happen simultaneously.
- Pairwise independent:Let Events E₁E₂E₃...Eₙ are pairwise if and only if` p(Eᵢ∩Eⱼ)=p(Eᵢ)p(Eⱼ)`,for all i and j,1=<i<j<=n.
- Mutually independent:Events are mutually independent if and only if` p(Eᵢ₁∩Eᵢ₂∩...Eᵢₘ)=p(Eᵢ₁)p(Eᵢ₂)...p(Eᵢₘ)`,1<=i₁<i₂<iₘ<=n,m>=2.
- Binomial Experiment:In n independent bernoulli trails with sucesss probability is p,and failture probability is q,the probability of exactly k success is ` C(n,k) pᵏqⁿ⁻ᵏ`.so we donated this probability as b(k;n,p) and  the function `b(k;n,p)=C(n,k) pᵏqⁿ⁻ᵏ` is named probability mass function of the Binomial Distribution.
- Random variable:A random variable is a real-valued function defined on a sample space.
- Distribution of a discrete random variable: For a discrete random variable X, its distribution is given by its probability mass function `P(X=r)` ,specified for each value r in range of X.
- Hash collision Probability :`P_no-collision = 1 × [(N-1)/N] × [(N-2)/N] × … × [(N-(k-1))/N]= ∏_{i=1}^{k-1} [1 - (i/N)]`
`P_collision = 1-1 × [(N-1)/N] × [(N-2)/N] × … × [(N-(k-1))/N]`
- Probabilistic Method:if the probability that a randomly chosen element from S does not have property P is less than 1,then S must contain an element with property P.
- The Erdős lower bound on Ramsey numbers:if k is a integer,k>=2,`R(k,k) >= 2^(k/2)`,Erdős proved that Ramsey numbers grow at least exponentially.