## Algorithm

 - Algorithm is the well-defined,finited sequence of unambigugous instructions for sloving a specific problem or performing a specific  computation.
 - Linear Search :Finding a target value by comapring it with each element in a list sequentially.
    ```
    procedure:linear search:(Target Integer x,a₀ a₁ a₂ a₃ aᵢ:distinct integers)
    i :=1;
    while (i<=n,and x ≠ aᵢ)
        i =i + 1
    if i <= n then location: =i ;
        else location =0
    return location
    ```
- Binary Search:A method of finding a target element x by repeatedly comparing it with  the middle element of a sorted list ;Binary Search = Sorted List + Middle Element + Repeated Halving.
   ```
   procedure binary search(Integer x,a₁ a₂ a₃ aₙIncreasing integers)
   i :=1;(i is the left endpoint of the search interval)
   j :=n;(i is the right endpoint of the search interval)
   while i<j:
      m= ⌊(i+j)/2⌋ 
      if x > aₘ then i :=m+1
      else j = m
   if x = aᵢ then location:=i
   else location = 0
   return location
   ```
- Sorting :The process of arranging unsorted elements into a specific order.
- Bubble sort: