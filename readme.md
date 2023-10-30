# Completed work so far
- 4 Functional radix sort algorithms
- Successful integration of radix sort into PyPy exclusively for integer lists
- Data generation for testing, data is generated in multiple distributions
- Testing script that tests the 4 algorithms with 7 different bases.
- Production of some statistical analysis & graphs to illustrate comparisons between algorithms

# Current points of uncertainty

## Large integers
I Cannot use the radix sort on lists containing values over 9223372036854775807 because PyPy defines these values as longs, not ints. There does not exist a custom sorting strategy for longs and even if their were, I do not believe it would apply to lists containing ints and longs.

See here for example on how PyPy handles lists: https://www.pypy.org/posts/2011/10/more-compact-lists-with-list-strategies-8229304944653956829.html

## Using insertion sort
I found in my experimentation (and later online) that radix sort can be inefficient when performed on small lists. As MSD sorting creates lots of small lists, I have included insertion sort but I had immense difficulty finding exactly when to use insertion sort (i.e. how small a list needs to be before insertion sort becomes faster). This is especially difficult when performing tests with different bases.

As insertion sort has complexity of n^2 and radix sort has kn (where k is number of bits of integer), i would expect the point insertion sort becomes faster to be around k>n but this did not appear to be the case

## Contribution
I have not yet properly evaluated that my project fits in with the PyPy project's contribution guidelines or coding guide. I still need to create unit tests for my project.

This is something I was less focussed on before, as I have been uncertain about the performance of my algorithm compared to Timsort and due to time constraints but is something I want to complete as it is part of my project outline.

## Which base to use
I included the ability to sort using a different base/radix because I was unsure which would be fastest, I expected sorting in base 256 would be faster than sorting decimal numbers but i was unsure whether base 4096 might be even faster.

The results of my testing do not show that there is a clear best base to use, larger bases tend to be faster but base 16384 tended to be slower than base 4096. 

I believe there might be a method of quickly selecting the best base to use, for example selecting a smaller base if all the items of the list are small, but as to whether this would be cheap enough to compute for it to be useful is uncertain.

As of right now I'm completely unsure of how to select which base to use to sort, but I'll probably just go with whichever one is fastest on average in the testing.

## Performance
I'm somewhat concerned that my algorithm isn't actually faster than TimSort in a lot of situations, and when it is faster the benefits are marginal.
I believe that I may be able to save some time by streamlining the code by removing all but one of the sorting algorithms and statically assigning the base, but this would mean that I can't test different bases and algorithms without compiling PyPy 28 times.

I think maybe I should evaluate which of the 4 algorithms I designed is best, decide which base is best or allow the algorithm to determine it itself and then only compare that algorithm to timsort to cut down on the copmutational overhead currently being used to select the algorithm & base.



