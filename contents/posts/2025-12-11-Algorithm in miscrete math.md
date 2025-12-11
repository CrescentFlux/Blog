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
- Bubble sort:Repeatedly compare adjacent elements from left to right;if the left element is greater than the right element,swap them.Continue until the entire list is sorted.
   ```
   procedure bubble sort:(a₁, a₂, a₃, ..., aₙ,integer n >=2,Increasing sorting)
   for i := 1 to n-1 #Interation
       for j:=1 to n-i  #progress /position
          if aⱼ > aⱼ₊₁ then swap aⱼ and aⱼ₊₁
    ```

- Insert sort: Like sorting playing poker,you take an element and insert it into the correct position by comparing it with  already-sorted elementes from right to left.(By breaking down the existing arrangement,we can construct the target configeration)
   ```
   procedure insert sort:(a₁, a₂, a₃, ..., aₙ,integer n >=2)
     for j:=2 to n  
         i:=1
         while aⱼ> aᵢ #stage1:Find the insertion position
            i=i+1
         m:=aⱼ   #stage1：save the value
         for k:=0 to j-i-1 #stage2: Move/overwrite
           aⱼ₋ₖ := aⱼ₋ₖ₋₁ 
         aᵢ :=m  #Insertion
    ```
- Greedy algorithm :An aprroach that makes irrevocable locally optimal choices at each step,hoping for a globally optimal solution.
   ```
   Cion change problem
   procedure change(c₁ c₂ ... cᵣ ,Coin denomitations,c₁> c₂> ... cᵣ,Postive integer n)   
     for i := 1 to r  #Process coin denomitations in descending order.
         dᵢ := 0   #dᵢ records the count of coins with denomitation cᵢ.
         while n>=cᵢ: # Select the largest coin denomitation that does not exceed the remaining amount.
            dᵢ=dᵢ+1 #Increment a counter
            n = n-cᵢ
  ```

  