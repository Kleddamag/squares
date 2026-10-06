         Packing equal squares into a large square
                        Fan Chung ∗†               Ron Graham∗


                                            Abstract
          Let s(x) denote the maximum number of non-overlapping unit squares
       which can be packed into a large square of side length x. Let W (x) =
       x2 − s(x) denote the “wasted” area, i.e., the area not covered by the unit
       squares. In this note we prove that
                                               √
                                 W (x) = O x(3+ 2)/7 log x .
                                                          

       This improves earlier results of Erdős-Graham and Montgomery√
                                                                       in which
       the upper bounds of W (x) = O(x7/11 ) and W (x) = O(x(3− 3)/2 log x),
       respectively, were obtained. A complementary problem is to determine
       s0 (x) the minimum number of unit squares needed to cover a large square
       of side length x. We show that
                                                  √
                              s0 (x) = x2 + O x(3+ 2)/7 log x ,
                                                             


       improving an earlier bound of x2 + O(x7/11 ).


1      Introduction
The problem of finding dense packings of equal squares into a square has devel-
oped a fairly substantial literature since it was first introduced some 35 years
ago in a paper of Erdős and the second author [1]. Most of the research has cen-
tered on the case when the number of squares to be packed is relatively small,
e.g., less than 100. (The reader can consult Freedman [3] for an excellent survey
of the current state of knowledge.)
     In this note we show that a square of side length x can be packed with unit
squares so that the uncovered (or waste) area W (x) satisfies
                                             √
                               W (x) = O x(3+ 2)/7 log x .
                                                        

    ∗ University of California, San Diego
    † Research supported in part by NSF Grants DMS 0457215 and ITR 0426858




                                               1
                                              √
The best previous bound W (x) = O(x(3− 3)/2 ) was due to Montgomery [8] (see
also [9]), which improved on the earlier result in Erdős and Graham [1] that
W (x) = O(x7/11 ). Note that

                              7/11    =     0.636363 . . . ,
                               √
                            3− 3
                                      =     0.633974 . . . ,
                              2√
                            3+ 2
                                      =     0.630601 . . . .
                              7

By results of Roth and Vaughan [9], it is known that W (x)  x1/2− for any
 > 0 when x is bounded away from an integer. More precisely they show that
if x(x − bxc) > 1/6, then
                                        p
                       W (x) > 10−100       x |x − bx + 1/2c|.

Needless to say, their proof is non-trivial.
     The method of proving our new bound on W (x) can also be used to improve
the bounds for the dual problem of covering a square of side length x by a
minimum number of unit squares. Previously, Karabash and Soifer [5] showed
that the total number s0 (x) of squares needed satisfies s0 (x) = x2 + O(x2/3 ).
Recently they improved the bound to s0 (x) = x2 + O(x7/11 ) (see [6, 10]), based
on the earlier estimate of W (x) = O(x7/11 ). We will further improve this bound
to
                                            √
                        s0 (x) = x2 + O x(3+ 2)/7 log x .
                                                       



2      Preliminaries
During this and subsequent sections we will frequently suppress lower order
terms in our estimates for ease of exposition. Suppose we have a strip of width
m. (Here m is a function of x that goes to infinity as x approaches infinity.) We
wish to pack a stack of unit squares of height dme as close to being orthogonal
as possible. As seen in Figure 1, the stack will form an angle θ which is no more
     p
than 2/m.



                                          2
                                                 m' = ⎡⎢ m ⎤⎥ + tan θ
                              m'       m
                                   θ              f = m' - m




                             (m')2 − m 2          2mf + f 2             2
             θ = arctan                  ≤ arctan           ≈
                                 m                  m                   m

                       Figure 1: Packing a stack of squares.



    Suppose now we wish to cover a strip of width m by using stacks of unit
squares of height dme + 1 as in Figure 2. Again the stacks form an angle ϕ
                         √
which is no more than 2/ m (plus lower order terms). Note that ϕ is larger
than θ but is of the same order.



              m''                                            2
                                               m'' = ⎡⎢ m ⎤⎥ + 1
             φ
         m
                                               f ' = ⎡⎢ m ⎤⎥ - m



               (m'')2 − m 2          2m(f ' + 1) + (f ' + 1)2   2
    φ = arctan              ≤ arctan                          ≈
                   m                          m                 m

                    Figure 2: Covering with a stack of squares.




3     The construction
The proof will be an induction based on efficient packings of three basic shapes:




                                           3
                               x'


               x                                  2x 2-2α ≤ x' ≤ 2x




                          Type 1

                          Figure 3: Type 1 rectangle.



A Type 1 shape is a rectangle with a vertical side length x and base x0 with
                                √
2x2−2α ≤ x0 ≤ 2x where α = (3 + 2)/7 (see Figure 3).
A Type 2 shape is a trapezoid with a vertical left side length of x, a top edge of
                     √
length x0 satisfying x ≤ x0 ≤ 2x and the angle θ between the right-hand side
                                  p
and a vertical line satisfying θ ≤ 2/x (see Figure 4).
A Type 3 shape is also a trapezoid similar to Type 2, except that in this case
                                                             √
the top edge length x0 satisfies 2x2−2γ ≤ x0 ≤ 2x with γ = 1/ 2, and the angle
θ satisfies θ ≤ 1/x (see Figure 5).   Let Wi , 1 ≤ i ≤ 3, denote the minimum

                               x'

                                                  x ≤ x' ≤ 2x
                   x
                                             θ            2
                                                   θ≤
                                                          x

                            Type 2

                          Figure 4: Type 2 trapezoid.


possible waste when a Type i shape is packed with unit squares.

Theorem 1 For a suitable absolute constant c > 0,


                                        4
                                x'

                                                      2x 2-2γ ≤ x' ≤ 2x
                   x
                                                  θ        θ ≤ 1x


                                x''
                              Type 3

                            Figure 5: Type 3 trapezoid.



(1)                                                    √
                                      α             3+ 2
                       W1 (x) ≤ 4cx log x where α =      ;
                                                      7
(2)                                                         √
                                     β                   2+ 2
                       W2 (x) ≤ cx log x       where β =      ;
                                                           4
(3)
                                                       1
                        W3 (x) ≤ 2cxγ log x where γ = √ .
                                                        2
Note that W (x) ≤ W1 (x) = O(xα log x).
Proof of (1):
      We will tile our x by x0 Type 1 rectangle R as follows. We first pack an
integer-sided rectangle R0 ⊆ R perfectly with unit squares (i.e., with no waste),
leaving unfilled two strips: S1 of width m and length x, and S2 of width m0
and length x0 − m, where m, m0 ≈ x2−2α (see Figure 6). The strips in S and
S 0 consists of stacks of unit squares of lengths dme and dm0 e, respectively. The
four unfilled regions at each of the ends of S and S 0 are (essentially) Type 2
                      p
trapezoids, with θ ≤ 2/m. The wasted (i.e., uncovered) area along the border
                             √    √
of S and S 0 is bounded by 4 2x/ m. Hence, the waste in this packing of R is




                                           5
                m'                      S'
                                      …….




                                                         …………
                                       …………                     S
                                        R'




                                                                m
                                         R

                          Figure 6: Packing of Type 1.



(by induction) bounded above by
             √ x
            4 2 √ + 4W2 (m) ≤ 6xα + 4cmβ log m
                 m
                                     ≤ 6xα + 4cx(2−2α)β (log x2−2α )

                                     ≤ 4cxα log x

since 6 + 4c(2 − 2α) log x ≤ 4c log x for x ≥ 2 and c ≥ 10.
Proof of (2):
    Our plan is to partition the Type 2 trapezoid T2 into a perfectly packed
                     √                                                p
region A, and about 2x of the Type 3 shapes of side length about x/2,
together with a strip S at the bottom of (approximate) dimensions x2−2α by x0
                                                                      p
(see Figure 7). (Thus, S is a Type 1 shape.) Also note that with y = x/2,
                                                                   √
each Bi is a Type 3 shape (since the corresponding angle θ ≤ 1/ x = 1/y
                             √
and Bi has side length y = x). Hence, by induction, the total waste for this
packing is bounded above by
                          √       p         p
                (2x)α +       2xc( x/2)γ log x/2 ≤ cxβ log x

since (1 + γ)/2 ≤ β and c is large enough.
Proof of (3):


                                         6
                                      x'         m≈     x 2
                                                      B1          x 2

                                                      B2          x 2


              T2                     A




                                                      ………
                                                                        2
                                                                  θ≤
                                                                        x


                                                       Br
                   x 2-2α             S
                                      x'

                             Figure 7: Packing of Type 2.



   We will have to work a little harder for this case. In Figure 8 we show a
Type 3 shape T3 . We are going to partition T3 into various regions (similar to
what was done for Type 2). As before, the bulk of T3 consists of an integer-sided
rectangle A0 which will be packed perfectly. Note that the top and bottom edge
lengths x0 and x00 differ by at most 1 since θ ≤ 1/x.
   For each Ci , we are going to pack most of it with tilted stacks of unit squares
of height z = 1 + dwe (which is one more than what we could use, but which
will be useful for our purpose). In particular, such a stack can be used for all
the Ci (i.e., it is longer than the bottom edge of the last Ci ).
   Now, for each Ci we partition it into a triangular region ei and a rectangular
region Ri (see Figure 9). The sum of the areas of ei (which will all be wasted)
is at most
                            x k2                            1
                             ·   = k ≤ xγ       since θ ≤     .
                            k x                             x
The rectangular region Ri will be packed with tilted stacks of z unit squares,
but leaving spaces at the end (to be specified later). The total wasted space




                                            7
                                   x'              w ∼ x 2-2γ
                                                  C1     k ∼ xγ

                                                  C2     k




                               ………
         T3     x            A'




                                                  ………
                                                             θ ≤ 1x



                                                    Cs
                k'                S'
                                        x''


                          Figure 8: Packing of Type 3.



along the borders of the Ci is bounded by
                              √         √
                           2k 2 x      2 2k
                            √ · = √         ≤ 3xγ .
                              w k         w

Now comes a more subtle step. We are going to examine the transition between
Ci and Ci+1 (see Figure 10). The plan is that at each such transition we will
stop short of the dividing line between Ci and Ci+1 by about w2−2γ /2 and
form a new trapezoidal shape with the union of the two ends (see Figure 11)
by trimming off small triangular pieces. It will turn out to be a Type 3 shape
because the difference of the angles σ 0 and σ 00 is sufficiently small (as we will
soon compute). At the top of C1 and the bottom of Cs we leave a gap of length
w2−2γ , so that Type 2 shapes are formed. By induction, the waste here is at
most
                               2 · 4cwβ log w ≤ xγ .




                                              8
                               w

                              …z
                              … …                    z = 1+ ⎡⎢ w⎤⎥
                              …
                              ………
                                …




                               ………
                   k          Ri
                                                ei
                              ……
                              …
                              …
                              ………
                                …




                                   w'
                                   Ci
                           Figure 9: Packing of Ci .



   In particular, the difference of the angles σi and σi+1 is bounded by
                       r         r
                           δi       δi+1
      σi − σi+1 = 2           −2                where δi = z − wi
                            z         z
                       r         r
                           δi       δi − x−1+γ
                  ≤ 2         −2                  since wi+1 ≤ wi + x−1+γ
                            z            z
                       r         s
                           δi             x−1+γ 
                  = 2          1− 1−
                            z               δi
                       r
                                    −1+γ
                           δi 1 x
                  ≤ 2         · ·
                            z 2      δi
                         1
                  ≤ √
                         δi z
                      1
                  ≤
                      z
since z ≈ w ≈ x2−2γ . This shows that the “trimmed” shape between Ci and
Ci+1 is a Type 3 trapezoid and so by the induction hypothesis, the total waste
for those pieces is bounded above by

                    x1−γ wγ    ≤        x1−γ+(2−2γ)γ c log x2−2γ
                                        3 γ
                               ≤          cx log x.
                                        5

                                            9
                                        Ci
                                        σi
                                        Xi
                  w2-2γ                 wi
                                             wi+1

                                        X i+1

                                                σ i+1
                                       Ci+1

                 Figure 10: Transition between Ci and Ci+1 .



We must also bound the waste due to the trimming used in creating these
transition Type 3 shapes. However it is easy to see that this waste is bounded
above by

                          2x 2−2γ                       2
                             w       ≤ 2x1−γ+(2−2γ)
                           k
                                     ≤ xγ .

Finally, we must bound the waste due the strip S 0 at the bottom. Here it is
immediate that this waste is at most

                              cxα log x + wγ ≤ xγ

since S 0 is essentially the union of a rectangle and a Type 3 trapezoid. Putting
this altogether, we see that the total waste is no more than

                               3
                          8xγ + cxγ log x < cxγ log x.
                               5

This completes the induction step. We will choose c sufficiently large so that


                                       10
                                         Ci


                  w'''
                                         Xi


                      w''''              X i+1



                                        Ci+1


                      Figure 11: Packing between Ci and Ci+1 .



for small x, say x ≤ 100, the theorem holds. This establishes the initial step of
the induction and the proof is complete.                                       


4      Some variations
Instead of packing unit squares into a large square, we consider covering a large
square with unit squares. We can prove the following:

Theorem 2 We can cover a square of side length x using s0 (x) unit squares
with                                                √
                  0           2     α            3+ 2
                s (x) = x + O(x log x) where α =      .
                                                   7
The proof proceeds along the same lines as described in the preceding section
using simultaneous induction on Types 1, 2 and 3 shapes. The only difference
is that the angle ϕ in the Type 2 trapezoids is a constant factor larger than
the associated angle θ computed in Section 2. The inductive proofs are almost
identical to those of Theorem 1. (We omit the proof.)


                                         11
   Let Wθ denote the waste for packing unit squares in trapezoid with a general
                                                    p
angle θ. A Type 2 shape is the special case with θ = 2/x and a Type 3 shape
is the case that θ = 1/x. It is not difficult to use the same proof to show:

Theorem 3 We can pack unit squares into a trapezoid of side length x and
angle θ so that the waste Wθ (x) satisfies
                                √
                     O(x1−δ/(2+ 2) ) if θ = 1/xδ and 0 < δ ≤ 2α,
      Wθ (x) =
                     O(xα )             if θ ≤ 1/x2α .
This proof is very similar to the proof of Theorem 1 and we will not include the
proof here.


5     Concluding remarks
A natural question to ask at this point is to what extent the exponent bound
       √
of (3 + 2)/7 can be improved.
                                              √            √
Challenge ($100). Improve the bound (3 + 2)/7 to (3 + 2)/7 − c for some
c > 0.
    While it might be natural to think that the “truth” is W (x) = O(x1/2+ )
for any  > 0 (as was suggested in [1]), the authors are skeptical. In fact, we
offer the opposite:
Conjecture: ($1000). Prove that for some c > 0, W (x)  x1/2+c .
    (Of course, this reward will be paid for a disproof of the conjecture.) As
usual, such prizes are only given to the first valid claimant!
    The upper bound on W (x) can be used to improve a related bound on t(N ),
defined to be the edge length of the smallest square into which n non-overlapping
unit squares can be packed (cf [7]). For this problem, we obtain
                                                log N
                        t(N ) ≤ N 1/2 + O(        √      ),
                                             N (4− 2)/14
improving earlier estimates of the big-O term based on weaker estimates of
W (x).
    Many questions remain. For example, if we have a trapezoid shape similar
to Type 2 but with an angle θ > c > 0 for some positive c, then is it true that
the waste area is greater than c0 x for some constant c0 = c0 (θ) > 0?


                                        12
   In the other direction, if the angle of a trapezoid is small, say θ < 1/x2α , it
can be shown that the wasted area is O(xα ) as stated in Theorem 3. It would
be of interest to find the maximum θ such that the trapezoid has waste area of
the same order as a square.
   In this paper, we deal with both the wasted area of packing and covering a
large square by unit squares. Are the two quantities W (x) and C(x) = s0 (x)−x2
of the same order (as suggested in [6])?
   Suppose that, for an integer n, we wish to pack n2 + 1 unit squares into
a large square with side length, say n + δn , as small as possible. What is the
                                                             √
values of δn ? The only known values are δ1 = 1 and δ2 = 1/ 2 (see [3]). In [7]
it was shown that δ43 ≤ 1/2. An immediate consequence of Theorem 1 is
                                              √
                                 δn  n(−5+ 2)/7 ,

improving an earlier estimate [7] using [1]. On the other hand, it seems likely
to us that the smallest square into which n2 − 1 unit squares can be packed has
side length n. The same result should hold for packing n2 − k unit squares when
k is fixed and n is sufficiently large (as conjectured in [3]).
   By way of contrast, the problem of packing equal discs into a large equi-
lateral triangle seems to exhibit a somewhat different behavior. Let T (m) de-
note the smallest possible side length of an equilateral triangle into which m
                                                                          
non-overlapping unit discs can be packed. It is known [2] that T n+1    2      =
         √
n − 1 + 2 3. Two currently unproved conjectures [4] are:
                                                                
Conjecture: For some constant c > 0, T n+1        + 1 > T n+1
                                                
                                              2                 2     + c for all
n. In fact, computation suggests that c > 0.3.
                                    
Conjecture: T n+1       − 1 = T n+1
                      
                   2                2     for all n.
   In other words, the optimal (obvious) packing of a triangular number of
equal discs into an equilateral triangle is so good that no smaller triangle can
hold one fewer disc, and further, if we try to pack one more, then the triangle
side length must increase by some non-trivial positive amount. However, it is
easy to see that a smaller triangle can be used if we are packing two fewer discs.



                                         13
References
 [1] P. Erdős and R. L. Graham, On packing squares with equal squares, J.
    Combin. Th. 19 (1975), 119–123.

 [2] L. Fejes Tóth, Lagerungen in der Ebene, auf der Kugel und im Raum, 2nd
    ed., Die Grundlehren der mathematische Wissenschaften, Band 5, Springer-
    Verlag, Berlin-New York, 1972, xi + 238pp.

 [3] E. Freedman, Packing unit squares in squares: A survey and new re-
    sults, The Electronic J. of Combinatorics, Dynamic surveys (#DS7),
    http://www.combinatorics.org/Surveys/ds7.html (2000), 25pp.

 [4] R. L. Graham and B. D. Lubachevsky, Dense packings of equal disks in
    an equilateral triangle: from 22 to 34 and beyond. Electron. J. Combin. 2
    (1995), # 1, 39 pp.

 [5] D. Karabash and A. Soifer, A sharp upper bound for cover-up squares,
    Geombinatorics 16 (2006), 219–226.

 [6] D. Karabash and A. Soifer, Note on covering a square with equal squares,
    Geombinatorics 18 (2008), 13–17.

 [7] M. Kearney and P. Shiu, Efficient packing of unit squares in a square, The
    Electronic J. of Combinatorics 9 (2002), #R14, 14pp.

 [8] H. Montgomery, personal communication.

 [9] K. F. Roth and R. C. Vaughan, Inefficiency in packing squares with unit
    squares, J. Combin. Th. (A) 24 (1978), 170–186.

[10] A. Soifer, Covering a square of side n +  with unit squares, J. Combin.
    Th. (A) 113 (2006), 380–388.




                                      14
