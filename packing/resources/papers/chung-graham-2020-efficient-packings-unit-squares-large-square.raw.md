    Efficient packings of unit squares in a large
                       square
                         Fan Chung∗              Ron Graham†


                                       Abstract
           How efficiently can a large square of side length x be packed with
        non-overlapping unit squares? In this note, we show that the uncov-
        ered area W (x) can be made as small as O(x3/5 ).√ This improves an
                                                           3+ 2
        earlier estimate which showed that W (x) = O(x       7    log x).


1       Introduction
Given a large square S(x) of side length x, let W (x) denoted the mini-
mum possible amount of uncovered area in any packing of S(x) with non-
overlapping unit squares. When x = N is an integer, then of course W (N ) =
0. However, when x is not an integer, then some waste (= uncovered area)
is inevitable. In we naively pack the square in the “obvious” way, (see Fig.
1), then the wasted area will be proportional to x(x − bxc), which is lin-
ear in x when (x − bxc) is bounded away from 0. . During the past 40
years, better upper bounds for W (x) have been obtained. Beginning with
                                7
                                    0.63636...
the estimate W (x) = O(x 11 ) = O(x
                                 √
                                               ) from [3], this was improved by
                                     3− 3
Montgomery [7] to√ W (x) = O(x         2    ) = O(x0.63397... ) and then most recently
                  3+ 2
                                                              √
to W (x) = O(x      7    log x) by the authors [2] where 3+7 2 = 0.63060 . . ..
    ∗
   Dept. of Mathematics, University of California, San Diego, fan@ucsd.edu
    †
   Dept. of Computer Science and Engineering, University of California, San Diego,
graham@ucsd.edu.


                                             1
    In the other direction, a seminal result of Roth and Vaughan [8] shows
that if x(x − bxc) > 16 then
                                             p
                            W (x) > 10−100    x kxk                          (1)

where kxk denote the distance from x to the nearest integer. In particular,
this shows that W (x) > cx1/2 for some absolute constant c provided x is
bounded away from an integer.
    In this note, we improve the upper bound for W (x).

Theorem 1.
                                              3
                                W (x) = O(x 5 ).

    To prove Theorem 1, we will describe the packing procedure in three
stages. In the first stage, we partition the square S(x) into a perfect square
(of integral side) and two rectangles. In second stage, the rectangles are
packed by stacks of unit squares but some trapezoids are still left uncovered
as well as some tiny triangles along the edges. At the last stage, we pack
the trapezoids in a careful way. We note that in the first and second stages,
the strategy for packing S(x) will be similar to that used in [2], although the
parameters are chosen differently.
    In each stage, there are a number of steps to pack unit squares into the
regions. During this process, we will keep track of the waste in each step of
the way. All together, we will consider nine types of waste, denoted by Wi (x)
for i = 1, . . . , 9. We will show that for each i, Wi (x) = O(x3/5 ). Summing
the Wi (x) for i = 1, . . . , 9, then yields the claimed upper bound for W (x).


2     Packing rectangles with unit squares.
Since we are only proving asymptotic bounds on W (x), we will omit floor
and ceiling functions when they are not essential. In order to simplify the
notation, we are first going to assume that x = N + 1/2 for some integer N .
The modifications needed for general x should be clear.

                                       2
   For the first stage of the construction, we will pack most of S(x) in the
naive way but leaving two unpacked rectangles with short side lengths equal
to x4/5 (see Fig. 1), In particular, we can take this length to be of the form
M + 1/2 for some integer M which makes M + 1/2 closest to x4/5 . Note that
the figures are not drawn to scale.

                                      S(x)
                        4
                       x5



                  x
                                 ........




                                            x

 Figure 1: Packing most of S(x) with axis-aligned stacks of unit squares .

   Next we are going to take stacks of M + 1 unit squares, tilt them slightly
and pack most of the two rectangles with these stacks.

                   2                  W1
                 x5

            4
           x5      T                            ......




          Figure 2: Packing the rectangles with stacks of squares.

                                            3
    There are now two questions. How much of the rectangles do we pack
this way, and how must waste do we generate?




                                       θ



                                                 1
                        ( M + 1+ tan θ )2 − ( M + )2
             θ = arctan                          2 ≈ 1 ≈ 1 + O( 1 )
                                        1
                                                          2      4

                                  M+                 M x5      x5
                                        2

                        Figure 3: The angle of a stack.

    Referring to Fig. 3, a computation shows that the angle θ in the small
right triangle is asymptotic to √1M (since tan θ ∼ θ as M → ∞.) Hence, the
area of each of the shaded right triangle is (asymptotic to) √1M = O(x−2/5 ).
Since there are at most 4x such triangles, then this waste W1 (x) is bounded
by W1 (x) = O(x3/5 ).


3     Packing the trapezoids with unit squares.
We will fill the rectangles with the aforementioned stacks until we have empty
trapezoids with top edges of length x2/5 . Hence, the bottom sides have length
2x2/5 (see Fig. 4).
    We will focus on a single trapezoid T (we treat the other three in the
same way). We subdivide T into t + 1 trapezoids Bi , 0 ≤ i ≤ t, as follows.
Let b0 denote the length of the top edge of T . Then go down the left-hand
side of T by steps of size 1 until the horizontal line going to the right-hand
side of T has length b1 exceeding b0 + 1 but no more than b0 + 1 + O(x−2/5 ).

                                       4
                                     2
                                    x5




                               4
                             x5      T


                                                 θ


                                             2
                                         2x 5

                         Figure 4: The trapezoid T.

This will happen when the horizontal line has come down for a distance of
h0 ∼ x2/5 where h0 is an integer. We now draw this horizontal line which
will form the bottom edge of the first sub-trapezoid B0 . Now we repeat this
process starting from the bottom edge of B0 . Namely, we go down until we
find that the horizontal line to the right-hand side of T has length b2 which
exceeds b1 + 1 but is less than b1 + 1 + O(x−2/5 ). Again, this will happen
when the left-hand side has come down a distance h1 ∼ x2/5 . Drawing the
horizontal line at this point will form the bottom edge of the sub-trapezoid
B1 . We keep doing this until we reach the bottom of T . In general, Bi will
have a top edge of length bi between b0 + i and b0 + i + O(x−2/5 ), a left-hand
edge of integer length hi ∼ x2/5 and a bottom edge of length bi+1 between
b0 + i + 1 and b0 + i + 1 + O(x−2/5 ) (see Fig. 5). The exception occurs with
the last trapezoid Bt . For this sub-trapezoid, ht = O(x2/5 ) may not be an
integer. In this case, we just pack Bt “trivially” with axis-aligned stacks of
squares, leaving a waste altogether of W2 (x) = O(x2/5 ).
   In the next section, we describe how to pack squares into the Bi .




                                         5
                                                          2
                                                  b0 = x 5

                                                                     −2
                          h0    B0                   b1 = b0 + 1+ O(x 5 )


                           h1    B1

                      4
                    x5           ......

                                                      θ           W2 (x)

                          ht      Bt
                                          2
                                      2x 5
                Figure 5: Subividing T into sub-trapezoids Bi .

4     Packing the Bi.
The first step in packing Bi is to place i stacks of unit squares of height hi
along the left-hand edge of Bi (see Fig. 6).
    Since hi is an integer, no wasted space is created here. By construction,
the remaining portion of Bi is a subtrapzoid essentially isomorphic to B0 ,
                                              1
having a top edge length of bi − i = b0 + O( x2/5 ).
    The next step will be to remove x1/5 small right triangles from the right-
hand edge of Bi as shown in Fig. 7.
    Each triangle has height x1/5 . The area of such a triangle is O((x1/5 )2 θ) =
O(1). Hence, the total area of all these triangles is O(x3/5 ) since there are
x2/5 Bi ’s and each Bi has O(x1/5 ) such triangles. These triangles will be left
empty so the waste introduced here is W3 (x) = O(x3/5 ).
    Now define m to be the integer closest to db0 e + 1. All of the remaining
square packing of the Bi will be done with stacks of unit squares of height


                                              6
                                        2
                                   x5
                      h0           B0


                      h1           B1

                  4
                x5
                                    ......

                                                                   θ
                      ht−1        ...       Bt−1

                                                 2
                                            2x 5

Figure 6: Filling the ends of the Bi with stacks of squares.



                                                 1
                                                x5
                                                     1                     W3
                                                 x5
                                                         1
                                                     x5
                             Bi

                                                             ...

                                                                   1
                                                               x5
                                                                       1
                                                                   x5


            Figure 7: Creating “serrated” Bi ’s.


                                            7
m. In particular, all of the stacks will have their left-hand ends touching the
left-hand edges of the modified Bi (see Fig. 8).



               W4



                                              W4
                                       Bi


             Figure 8: Filling Bi with tilted stacks of height m.

   Also, these stacks will always be placed as close to the top as possible,
so that each stack will touch the stack above it. We continue placing stacks
of height m in the Bi , allowing stacks to cross from Bi to Bi+1 when neces-
sary. Doing this will create a certain amount of wasted space, which we now
estimate.
   First, the waste W4 (x) created by the small triangles at the ends of the
stack (see Fig. 8).
   The “tilt” of any stack is at most O(x−1/5 ) so that the area of such a
triangle is O(x−1/5 ). Since there are O(x4/5 ) such triangles, then we see that
W4 (x) = O(x3/5 ).
   Next, we examine what happens when consecutive stacks touch different
parts of the “serrated” Bi (see Fig. 9).
   A simple calculation shows that the difference in the tilts of the two stacks
                                                               c
can be estimated as follows. The tilt of the upper stack is ∼ x1/5 + O(x−2/5 )
                              √
for some constant c between 2 and 2 (which depends on the fractional part
of b0 ). The tilt of the lower stack is ∼ √ c        . Thus, by ignoring the
                                            x2/5 +x−1/5


                                       8
                                W5
                                     Bi

          Figure 9: A wasted triangle between two stacks within Bi .

lower-order terms, the difference of the two tilts is
                          c         c
                     ∼    −√                 =
                         x1/5 x 2/5 + x−1/5
                                            
                        c             1
                     = 1/5 1 − √               = O(x−4/5 )
                      x           1+x   −3/5


so that the area of the elongated triangle between the two stacks is
                                    2
                                x2/5 x−4/5 = O(1).

Since there are at most O(x3/5 ) such transitions inside the Bi ’s over all i,
then this waste W5 (x) is bounded by W5 (x) = O(x3/5 ).
   In addition, there is a small unpacked region above the lower of the two
stacks which has area O(x−(1/5) ) (see Fig. 10).
These altogether contribute a waste of at most W6 (x) = O(x2/5 ).
   Finally, we have to consider what happens when the stacks cross the
boundaries between consecutive Bi ’s (see Fig. 11).
   As we can see in Fig. 11, there is an elongated triangle between the last
stack (of length m) in Bi and the first stack (also of length m) in Bi+1 . We
note that the tilt of the first stack in Bi and the tilt of the first stack in Bi+1
are asymptotically the same since bi+1 − 1 = bi + O(x−2/5 ) ∼ x2/5 . We have

                                          9
                                               W6
                                     Bi

Figure 10: Additional wasted space between stacks with slightly different tilts.

shown previously that within Bi , there are x1/5 gaps each of which has an
angle of order O(x−4/5 ). Therefore the difference of the tilts of the first stack
and the last stack in Bi is at most O(x−4/5 ). This implies the difference in the
tilts between the the last stack in Bi and the first stack in Bi+1 is O(x−3/5 ).
Thus the area of the region between the two stacks is

                          O((x2/5 )2 x−3/5 ) = O(x1/5 ).

Since there are just O(x2/5 ) such transitions between the Bi ’s, then the waste
W7 (x) here is just W7 (x) = O(x3/5 ).
   There is still a small uncovered area of area at most 1 to the left of the first
stack of Bi+1 which we call waste W8 (as seen in Fig. 12). Altogether, there
are x2/5 such transitions, so W8 (x) = O(x2/5 ). There is also an uncovered area
above the first stack in B0 as well as an uncovered area below the last stack
in Bt−1 . Both can be packed trivially with a waste at most W9 (x) = O(x2/5 ).
   Adding up all the Wi (x), for i = 1, . . . , 9, we see that the wasted space in
our packing is O(x3/5 ) as claimed. This completes the proof of Theorem 1.




                                         10
                                 Bi




                                      Bi+1   W7


  Figure 11: Space wasted when the stacks end up in different Bi ’s.




                                Bi
                          W8




                                      Bi+1

Figure 12: Small uncovered area to the left of the first stack of Bi+1 ..




                                     11
5     Concluding remarks.
Of course, the basic problem is to determine the correct order of growth of
W (x). On one hand, because of the result of Roth and Vaughan [8], one
might be tempted to guess that W (x) = O(x1/2 ). (The authors don’t be-
lieve this.) On the other hand, the best upper bound currently available is
W (x) = O(x3/5 ).


    Challenge 1. ($ 100), Show that W (x) = o(x3/5 ).
    Challenge 2. ($ 250). Show that W (x) = O(x3/5−c ) for some fixed
c > 0.
    Challenge 3. ($ 500). Show that W (N + 1/2)  N 1/2+c for some fixed
c > 0.
    Of course, the rewards are also given for disproving the above assertions
(but only to the first claimants).
    We observe that the techniques used in the preceding results can be ap-
plied with minor changes to the question of covering a square of side x with
a minimum number of unit squares (as was done on [2]). This results in the
following.

Theorem 2. It is possible to cover a square of side x with x2 + C(x) non-
overlapping unit squares where C(x) = O(x3/5 ).

Earlier results on this variation also appear in [5, 6, 9].
    We point out that there has been a fair amount of work on optimally
packing a small number (e.g., less than 100) of unit squares into the smallest
possible square. A good survey of these results in can be found in [1] and [4].


6     Acknowledgement
We would like to express our appreciation for the energetic enthusiasm we
found at the 33rd Bellairs Winter Workshop on Computational Geometry in

                                       12
Barbados where some of this research was carried out.


References
 [1] P. Brass, W. Moser and J. Pach, Research Problems in Discrete Geom-
    etry, Springer, New York (2005), 499 pp. + xii.

 [2] Fan Chung and Ron Graham, Packing equal squares into a large square,
    J. Combin. Th.(A) 116 (2009), 1167–1175.

 [3] P. Erdős and R. L. Graham, On packing squares with equal squares, J.
    Combin. Th. 19 (1975), 119–123.

 [4] E. Friedman, Packing unit squares in squares:           A survey and
    new results, Electronic J. Combinatorics, Dynamic Surveys (#DS7)
    http://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7.html.

 [5] D. Karabash and A. Soifer, A sharp upper bound for cover-up squares,
    Geombinatorics 16, (2006), 219–226.

 [6] D. Karabash and A. Soifer, Note on covering a square with equal squares,
    Geombinatorics 18 (2008), 13–17.

 [7] H. Montgomery, personal communication.

 [8] K. F. Roth and R. C. Vaughan, Inefficiency in packing squares with unit
    squares, J. Combin. Th. (A) 24 (1978), 170–186.

 [9] A. Soifer, Covering a square of side n +  with unit squares, J. Combin.
    Th. (A), 113 (2006), 380–388.




                                     13
