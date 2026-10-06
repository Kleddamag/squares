   Some numerical methods in multibody dynamics: application
                     to granular materials
                                              Jean Jacques Moreau



      To cite this version:
     Jean Jacques Moreau. Some numerical methods in multibody dynamics: application to granular materials.
     European Journal of Mechanics - A/Solids, 1994, 13 (4 - suppl), pp.93-114. ⟨hal-01789082⟩




                                        HAL Id: hal-01789082
                              https://hal.science/hal-01789082v1
                                           Submitted on 9 May 2018




    HAL is a multi-disciplinary open access archive             L’archive ouverte pluridisciplinaire HAL, est des-
for the deposit and dissemination of scientific re-        tinée au dépôt et à la diffusion de documents scien-
search documents, whether they are published or not.       tifiques de niveau recherche, publiés ou non, émanant
The documents may come from teaching and research          des établissements d’enseignement et de recherche
institutions in France or abroad, or from public or pri-   français ou étrangers, des laboratoires publics ou
vate research centers.                                     privés.


 Distributed under a Creative Commons CC BY-NC 4.0 - Attribution - Non-commercial use - International
                                             License
            Sorne numerical methods in multibody dynamics:
                    application to granular materials
                                                J.J.MOREAU


ABSTRACT. - The unilaterality of non-pene1ration cons1rain1s, ù1e vclocily jumps which occur in case of collisions,
ù1e irregularity of ilie law of dry friction are 'nonsmooù1' features of ù1e dynamical systems in vicw. Numcrical meiliods
are presented, wich face nonsmooùrness wiiliout resorLing to mollifying approximation proccdurcs. A careful
formulation of contact Iaws generates algoriilims which, at evcry step of ùie time-discretization, are ready to face
possible collisions on ilie same footing as permanent contacts. These algoriùuns prove efficient enough to treat on
microcomputers or small workstations ù1e dynamical motion of systems involving a few thousands of bodies.
    Granular materials are modelled as collections of spherical beads. The concemed numerical technique has recently
permitted to discover a mechanism underlying Ùle phenomenon of size-segregation in a granular material contained in a
vertically shaken vesse!. This mechanism, which connects segregation wiù1 the convection currents induced by
boundary friction, bas been exhibited independenùy by some experimenlalists. The numerical assessment of boundary
forces, presented here, ù1rows some light on Ùle generation of boundary cun-ents.



1. Introduction

   Severa! computational techniques are currently used in the dynamics of collections of bodies,
during the motion of which contacts; generally subject to friction, are susceptible to occur or to
break.
   The most popular ones, commonly called Distinct Element or Discrete Element Methods, derive
from the pioneering work of P. A. Cundall [Cundall, 197 l][Cundall & Strack, 1979] or are adapted
from the procedures applied in numerical Molecular Dynamics. They consist in approximating the
mechanical constraint of non inter-penetrability of each body. pair by some close-range steep
repulsion law. In addition, on every time interval where two bodies are close enough to be viewed as
contacting (numerically, they may appear to overlap a little), they are assumed to exert on each other
some dissipative forces, depending on velocities in a smooth way which mimicks friction. Thereby,
the evolution problem is approximately reduced to the integration of a system of second order
differential equations, to which classical methods are applied. The steeper the approximate laws of
interaction, the more realistic are the results, at the price of reducing the time-step length for the sake
of numerical stability.
   Alternatively, while approximating non inter-penetrability in the same way as above, one may
mode! the inelasticity of possible collisions by assigning different repulsion coefficients to loading



Laboratoire de Mécanique et Génie Civil, URA CNRS 1214, Université Montpellier II,
34095 Montpellier Cedex 5, France.
   and to unloading [Walton & Braun, 1986]. Fliction, on the other hand, may be handled by applying
   directly the law of Coulomb [Wallon, I993a,b).
      Many significant simulations of motions have been obtained by some of these computation
   techniques, for systems of bodies which may either be fully deformable or treated as macroscopically
   rigid.
      A different approach is presented in this lecture, characterized by the absence of smoothing
   approximation.
      Precisely, the problems in view are nonsmooth in three respects:
   • The geometric effect of non inter-penetrability is expressed by a set of inequalities, instead of the
   equalities associated with traditional (bilateral) mechanical constraints. In other words, non inter­
  penetrability is a unilateral constraint, which makes that, in the space of the configuration variables,
   the feasible set is a region Iimited by a collection of surfaces. The boundary of such a region is hable
   to present a great number of multi-dimensional singulalities, a situation similar to what is commonly
   met in problems arising from Operation Research. This is nonsmoothness in space. Furthermore, the
  physical realization of non inter-penetrability, like that of any mechanical constraint, rests on the
   action of 'forces of constraint' or 'reactions'. These forces vanish as soon as the concerned bodies
   separate out, while during contact no fonction is available to express them completely : ail what is
   known is that reactions belong to some configuration-dependent sets. In regard to such irregular
  relationships between forces and configurations, one may say that non-smoothness in force-Law
  goes with non-smoothness in space.
  • In the event of a collision, the fonction of time which represents the system velocity is expected to
  be discontinuous. This is nonsmoothness in time.
  • If the friction considered at contact points is of the dry sort, for instance Coulomb's friction, it is
  governed by a relationship between the reaction force and the local relative velocity which makes
  another instance of nonsmoothness in force-law.
      Motivated, in particular, by the needs of Operation Research and Economies, formai and
  computational developments _have taken place in recent decades, giving birth to a mathematical
  domain called 'Nonsmooth Analysis' (see e.g. [Clarke, 1989][Hiriart-Um1ty & Lemarechal, 1993)).
  This includes 'Multivalued Analysis', i.e. the treatment of set-valued fonctions (see e.g. [Aubin &
. Frankowska, 1990)). The application of such tools to mechanical topics has been systematized under
  the title of 'Nonsmooth Mechanics' [Moreau et al., 1988)[Moreau & Panagiotopoulos, 1988). The
  approach presented in this lecture has been developed in this spirit.
      We propose to cal! this approach the Contact Dynamics method.
      Another numerical strategy, also avoiding the use of mollifying approximations in multibody
  dynamics, has recently been proposed [Hogue & Newland, 1993)).
      At the mathematical level, the study of nonsmooth dynamical problems (existence of solutions,
  possible cases of uniqueness, approximation procedures, etc.) is the subject of current research
  [Monteiro Marques, 1993)[Paoli & Schatzman, 1993).


 2. Outline and discussion

    Let be chosen a division of the time-interval I, with origin l(), into (usually equal) subintervals. At
 every of these time-steps, the proposed algorithms will be ready to face collisions on the same
  footing as lasting contacts. This is equivalent to treating the latter as successions of mini-collisions.
  Significantly in [Baraff, 1991], a paper with mechanical insight but aimcd at the produclion of artistic
  Computer Graphies animations, the same attitude is preconized on the basis of computational
  complexity assessements.
      This uniform treatment is made possible by imposing on the information available about the
  physical circumstances of contact to be stated under a standardized formalism ù1at we call a 'complete
  contact law' : see Sec. 5 below. This fonnalism takes care automatically of the non intcr-penctrability
  constraint and of the possibility of some contacts to break in the course of the motion, but leaves
  widely open the choice of phenomenological desc1iptions for f1iction and for collisions.
      In the sort of applications we are to present at the end of this lecture, namely the dynamics of dry
  granular materials, the law of Coulomb is generally acccpted as a fairly good representation of
  friction.
      More problematic is the modelling of collisional processes. By refening to rigid body collisions,
 one means that the involved bodies show sufficiently small deformation for being geometrically
 considered as rigid at the global observation scale [Stronge, 1990J[Brach, 1991J[Wang & Masan,
 1992]. In most of the literature devoted to this subject, authors tend to analyse such a collision as a
 microscopie phenomenon !ocalized in the vicinity of the impact locus : at this scale, material
 defonnability is taken into account (using models of elastic, visco-elastic or elasto-plastic behaviour),
 as well as the evolution of the small contact zone in which stick and slip regions may be distinguished
 [Maw et al., 1981]. Situations to which such an analysis is relevant certainly exist but, in general, the
 consequences of collisions are not localized. For instance, material dissipation in the vicinity of the
 impact is not the only cause of the energy Joss observable at the macroscopic level. Even if the bodies
 are assumed perfectly elastic, energy conse1vation cannot be expected. In fact, disturbances are likely
 to propagate from the collision locus to the whole system and also, if the latter is linked with some
 external support, to the outside world. After contact recedes, a state of vibration should persist. At
 the macroscopic observation level, this does not contradict the rigidity assertion, but the energy
involved in microscopie agitation may not be negligible. Also as a consequence of vibrations, a
collision may, at the microscopie time-scale, split into several separate contact episodes: an exarnple
 of such a double bounce is calculated in. closed form in [Timoshenko, 1948, Chap. 12]. Finite
 element computation of the collision of two èlas.tic bodies perfo1med in our laboratory has shown the
same. This makes the outcome of a collision strongly depend on the shape of the concerned bodies.
     Fortunately, the case of spherical objects, widely invoked in the simulation of granular materials,
proves more tractable. A collision law involving three parameters, identified as the friction
coefficient, the normal restitution coefficient and the tangential restitution coefficient has been
discussed [W, 1993a][Lun & Bent, 1993] and experimentally founct·acceptable [Foerster et al.,
1994].
     In view of this complexity, we choose to be content with a pragmatic description of collisions,
whose validity has to be investigated, in each class of applications, by comparing the results of
calculations with some calibrated expe1iments. It consists in assening that a complete contact law, of
the same form as that which applies to standing contact, holds between the contact percussion and a
certain formai local velocity. The latter is constructed by an averaging procedure involving the
(known) local velocity before collision and the (unknown) local velocity after (see Sec. 6 below). In
the case of spherical bodies, the resulting fo1mulas are found st1ictly equivalent to those produced by
 the above mentioned mode!, based on normal and tangential restitution coefficients, thus have the
 same domain of acceptability.
     The efficiency of CD methods in the dynamics of granular materials mainly stems from th"at, once
 a time-discretization has been chosen, ail the collisions which are detected as occurring on a given
 time-step are treated together. This of course entails some trade-offs which have to be assessed. It
 seems immaterial that the ordering of the collisions, which mechanically should be successive, is
 only internai to the algorithm (it depends on the objects numbering; randomizing it in the course of
 computation has not been judged useful). In fact, the problems in view are physically
 undeterministic, since a slight change in the initial conditions is enough to produce, after a short lime,
 a completely different sequence of positions and collisions. A more critical observation is that each
 collision is treated as occuring only once between the involved bodies in the considered time-step. An
 accumulation of bounces, such as those of a ping-pong ball coming to rest, is thus viewed as a single
 collision as soon as the successive bounces are ail comprised in the time-step. This could result in
 underestimating the global energy Joss aiising from inelastic collisions. This source of error may be
 checked by repeating computation with the lime step reduced to half: if no change is found in the
 energy vs time curve, one may conclude that no harm was done.
     Another delicate malter is that, in compact assemblies, the bodies involved in a collision may be
 parts of clusters of objects previously in contact. The propagation of impulses through such clusters
 raises questions of the same nature as sound in granulate materials.
    Anyway, the ultimate criterium of the usefulness of a computation method consists in comparison
 with calibrated physical experiments. In [Clément et al., 1992][Duran et al., 1993J[Rajchenbach et al.
 1993] a two-dimensional experimental set-up is described. A container is made of two parallel
 vertical glass plates and of lateral boundaries of various shapes (circular when spinning drum
experiments are devised, rectangular for shaken boxes). Metallic spherical beads with uniform
diameter, to which the space available between the glass plates bas been adjusted, are introduced.
 Also, when size-segregation is investigated, larger circular abjects with bead-inserts secming correct
 guiding by the glass plates are added. The high friction coefficients (say 0.8) needed in some
experiments is provided by using oxidized aluminium beads or chemically corroded steel beads.
Restitution is naturally higher with steel than with aluminium. The fairly large size of the beads
 (usually 1.5 mm in diameter) makes the effect of air negligible, as it has been tested by counter
experiments performed in a void.
    Visually, the concordance between these physical experiments and the animations displayed on the
computer screen seems almost perfect. Due to the majority of abjects having the same diameter,
cristal-like arrangements are generally formed whose dynamical behaviour involves some delicate
features : dislocations, propagation of defects, etc .. very well reproduced by CD computations. One
of these specific effects is the sporadic occurrence, in the upper corners of a vertically vibrated
rectangular pack of beads, of dislocation vortices. Figure 1 shows how this is rendered on the
computer.
    Heaps at the surface of vibrated packs of beads are also reproduced by computation [M, 1993].
    Such experiments involving the dynamics of very dense assemblies make severe tests for
numerical models. Quantitative compa1ison is currently in progress.
    Inertia of the concerned bodies plays an essential part in CD algorithms. This does not preclude
the use of the method in computing the quasi-static evolutions of granular materials familiar in many
situations of civil enginee1ing [Yemmas, 1993]. In that case, one is tempted to view the inertia terms
        Displacements over 60 periods of box vibration                   Vertically shaken two-dimensional cell
        (beads shown in their initial positions):                          Width: 7.5 cm
                                                                           Freq11ency : 15 hertz
                                                                           Peak ro peak ampli111de: 0.3 cm
                                                                             (Maximal acceleration: 1.332 g)
                                                                         Beads (oxidized a/11111ini11111):
                                                                           N11111ber: 1650 in tJ1c cell
                                                                           Diameter: 0.15 cm
                                                                           Friction benveen beads: 0.8
                                                                           Restitution: 0.7
                                                                         Laierai and bollom boundaries
                                                                           Friction: 0.8
                                                                           Restit11tion: 0.4
                                                                        The collisional and frictional cffccts of frontal
                                                                        glass boundaries arc neglcclcd.

                                Fig. 1. - Corner circulation in a vertically shaken box.
  (Numerical simulation   for comparison wiù1 cxperiments of E. Clément, J. Duran & J. Rajchcnbach [Clément 1992])
 as mere numerical mollifyers whose values might be adjusted for the sake of computation efficiency.
 Actually, it proves safer to keep these terms with their true physical values. In fact, the experiments
 commonly made with assemblies of cylinders (Schneebeli materials) show that, however slow the
 evolution of the control parameters may be, the deformation of the pack takes place through local
 crises which essentially are dynamical processes [Meftah & al., 1993]. An example of evolution of
 this sort is shortly presented in [Jean, I 994], where the results of a CD method are compared with
 those obtained by Cundall's TRUBAL software.
    The applications of CD methods have not been limited to round granules. Simulations of buildings
made of rectangular blocks assembled without mortar (the case of ancient Greek monuments)
supported by quaking ground have been performed. A se1ies of drawings may be found in [Jean &
Moreau, 1992] showing the progressive damage and the partial collapse of a wall due to ground
oscillation. In this case too, the validity of the_assumed contact Iaws has to be checked. Comparisons
with the experiments described in [Ageno & S_jnopoli, 1991] and [Raous, 1993] induce to make the
normal and tangential restitution coefficients equaLto zero for problems of this sort. More elaborate
contact laws remain to be designed, in order to describe masonry with mortar bonds. There is no
algo1ithmic difficulty in making such laws depend on the motion history.
    The use of CD methods in the numerical treatment, through finite elements, of dynamic or quasi­
static problems involving deformable bodies is out the scope of this lecture [Jean, 1993].
    The dominant features of al! CD algorithms is that they are time-discretization schemes of the
implicit type with regard to velocities.


3. Analytical setting

  Let the configurations of the system members be parameuized, at least locally, through generalized
coordinates, say q = (q 1, q2,... , q11). As usual such a reduction to finite freedom is assumed to result
 from (bilateral) ideal constraints, namely the strict rigidity of the system members and the possible
 action of internai or extemal frictionless linkages.
    After constructing this parametrization, one takes into account the constraints of non irtter­
 penetrability ; their geometric effect is assumed expressed by a finite set of inequalities

 (3.1)                  f (t, q) � 0, ae { 1, 2,..., K),
                         a
 where f1, f2, ...,f1C are given fonctions. Equality f a = 0corresponds to the occurrence of a contact.
 Through the presence of t in such an inequality, provision is made for the case where the inequality
 describes the confinement of a part of the system by some external boundaries with prescribed
 motion.
                                                                                          *
    In ail the sequel, it will be assumed that each of the fonctions fa is C 1 , with ofJoq 0at least in a
 neighbourhhood of the hypersurface f = 0of Rn+I _
                                         a
    For every imagined motion t�(t) and for t such that the derivative q(t)e Rn exists, the kinetic
 energy has an expression of degree 2 in q , say
                                 ·      1         ·i ·           ·i
 (3.2)                  'Eic(t, q, q) = 2 Ai/t,q) q qj + Bi(t,q) q + C(t, q),

 where A is a symmetric positive definite nxn-matrix, Be Rn and Ce R. In the usual case of
 scleronomic (i.e. time-independent) parametrization, A is constant in t, while B and C vanish.
    As far as s mooth, i.e. twice differentiable, motions are concerned, the system Dynamics is
 govemed by Lagrange's equations, here written as an equality in Rn

 (3.3)                  A(t,q) q = F(t, q,q) + L ra .

       The expression F comprises standard terms of Lagrange's equations and the covariant
  components, relative to the paramet1ization (q), of some applied forces supposed given as fonctions
  of time, position and velocity. The element ra of Rn is made of the covariant components of the
  contact forces experienced by the system in case the contact f = 0holds. Their construction rests on
                                                                  a
  the standard definition of the covariant components in Rn of forces located in physical space, so this
  construction is connected as follows wit_h the system kinematics.
       First suppose that inequality f � 0 expresses the mutual non inter-penetrability of some pair of
                                             a
  members of the system, say '13 and '13', so that equality f a = 0 corresponds to these two bodies
  touching each other at some point of space denoted by M . This we shall assume to be an isolated
                                                              a
  contact point, but other contacts, corresponding to different values of a, may also be in effect
  between the same bodies at the same instant. For every imagined motion t"""""?q(t) bringing the system
· through the considered contact position for some value of t, the velocities 'V a and 'Va' of the
  respective particles of '13 and '13' passing at point M let themselves be expressed as affine
                                                              a
  fonctions of the value u of the derivative q. The same is thus true for the relative velocity 'lla.='Va.­
  'V a.' of '13 with respect to '13' at this point, say

 (3.4)

 where Ga.:Rn"""""?R3 denotes a linear mapping, depending on t and q. No attention is paid al this stage
 to the imagined motion preserving contact or not. The Lerm 'Wa.e R3 , a known fonction of t and q,
 vanishes in the usual case of a scleronomic parametlization.
  Let 'l(a denote the contact force that body '13 experiences at point Ma from body '13'; then '13'
experiences from '13 the force -'l(a. Classically, the covariant componcnts of this pair of forces are
expressed by

(3.5)

with G�: R3 � Rn denoting the u·anspose of Ga (the convention of implicit summalion will never be
applied to Greek indices).
   Similar formulas hold if inequality fé O represents the confinement of a part '13 of the system by
some extemal boundary with prescribed motion. Assume that equality fa= 0 corresponds to contact
taking place at some point, here again denoted by Ma. The relative velocity, at this point, of '13 with
respect to the boundary has an expression of the form (3.4), where 'Wa now takes into account the
known velocity of the boundary, while ra in (3.5) equals the cova1iant components of the force 'l(a
alone, acting on '13. Its counterpart-'l(a, exerted by '13 upon the boundary, is no more in this case a
force experienced by ù1e system..
   In both cases; the following relationship is found [M, 1988b] to hold hetween af a/aq and the
n01mal unit vecteur na at point Ma to Ù1e two contacting bodies, directed toward '13

(3.6)                  :lÀ2:0 such that

    In ail the sequel, we shall assume that the mapping Ga is surjective of R 11 to R 3 ; equivalently, its
transpose G� is injective of R3 to R n. Only some special positions of certain linkages may give rise
to 'wedging' effects which break this assumption.


4. Nonsmooth formulation

     Due to the bodies beeing treated as perfectly rigid, possible collisions appear as instantaneous
processes. The velocity fonction t�u(t)=q(t) of the time interval I into R n is expected to be
discontinuous at the corresponding instants. Of course, this is only a formai way of condensing the
available information regarding a very b1jef episode, du1ing which u is differentiable and governed
by the differential equations of regular Dynamics, but with 'very large' contact forces.
     The natural mathematical seuing allowing for the fonction u to exhibit jumps consists in
assuming that this fonction has locally boun.ded variation. from I into Rn (notation : uE lbv(I, R11)),
i.e. it has bounded variation on every compact subinterval of I. Classically, with every such u, an
R11-valued measure on I is associated, called the differen.tial measure or Stieltjes measure of u and
denoted in ùüs paper by du. The reader may refer to [M, 1988a] as an expository text on this subject
(see also [Moreau & Valadier, !987][M, 1989) for some specific aspects).
    On every subinterval where u possesses a continuous derivative, say u; , one has du=u(dt i.e.
the measur� du admits u; as density fun.ction. relative to the Lebesgue measure dt of tl1is Lime interval
(tl1is is more generally true if u is a locally absolutely con.tinuous function so Ù1at u; is an element of
LL�/1, dt; R n)).
    Any uE lbv(l,R n ) possesses at every point· t of I a right-lim.it and a left-limit, respectively
denoted by u+(t) and u-(t) (by convention the left-limit at tl1e initial instant t is interpreted as u(tJ
                                                                                   0
and the symmetric convention applies to the possible final point of 1). Typically, for every compact
subinterval [a, b] of I, one has

(4.1)

This holds in particular for a= b , i.e. the integral of the measure du over the singleton { a} equals
the jump of u at point a. Thus the point a carries an atom of the measure du if and only if the
jump is nonzero.
   The traditional theory of percussions rests on the integration of both members of the differential
equation (3.3) over the 'very short' interval of a collision process. Since the term F remains
bounded on the interval, its integral is negligible, as well as the change of the configuration fonction
q. Ali what is left is this equality, valid at the instant t of the collision

(4.2)                          A(t,q) (u+(t)- u-(t)) =    L Pa..
                                                          a.

              a.
The terms p here equal the respective integrals, over the very short time interval, of the covariant
components of the 'very large' contact forces. By definition, these integrals constitute the covariant
components of the contact percussions.
   The velocity fonction u constitutes the central unknown of the evolution problem, to which the
configuration fonction t�q(t) is related through

(4.3)                         q(t) = q(t0) + f L u(s) ds
                                              LO
The differential equation (3.3), valid on any interval of smooth motion, may then be written as

(4.5)                          A(t, q) u; = F(t, q, u) + L ra. .
                                                         a.

Let us regard both members as the density functions, relative to the Lebesgue measure dt on the
considered time interval, of some Rn -valued measures. The equality of these measures

(4.6)                          A(t, q) du= F(t, q, u) dt+ L dRa.
                                                               a.

is equivalent to the differential equation (4.5) holding all over I. This may be called a measure
dijferential equation. The terms dRa.= ra.dt in this writing constitute the contact impulsion measures.
In such a smooth case they happen to admit density fonctions with regard to dt which properly
express reaction forces. In contrast, for the collisional situation described in the foregoing,
percussions contribute in the contact impulsion through vector measures which do not possess
densities relative to dt. Contact percussions actually are atoms of the contact impulsion measures and
the elements pa. of Rn equal the densities of these atoms relative to o , the Dirac measure at the point
                                                                       L
t of I.

   This is a general fact that, for a finite collection of R-valued or R11 -valued measures on the interval
I, such here are dt, du, dRa, there exists (non uniquely) a positive real measure, say dÂ., relative to
which they possess respective density fonctions t;i,e L1�/I, dÂ.; R), u;i_e L1�c(I, dÂ.; Rn ), and
R'fe L �(I, dÂ.; Rn). An alternative writing of the measure differential equation (4.6) therefore is
       1
(4.7)                  A(t, q) u;i_(t) = F(t, q, u) t;i,(t) + L R f(t),
                                                         a
holding for every t in I (with the possible exception of a dÀ.-negligible subset : equivalently one
may assign null values to the respective density functions on such a subset, so as to make (4.7)
actually hold everywhere in 1).
   The element R'{(t) of R11 consists of the covariant components of a 3-dimensional vector of
physical space, localized at the contact point Mo:, say �{(t), and the same correspondence as in
(3.5) holds, namely

(4.8)
REMARK 1. In (4.1) the function u appears only through its left- and right-limits : the value that it
may take at some discontinuity point is immaterial there. The same is true for (4.3), since classically
the set of Ùle discontinuity points of an lbv function is countable, hence negligible in the integration
with respect to dt. So the values that one may assign to the velocity function at the exact instants of
collisions bear at the present stage no dynamical significance. This latitude will be exploited in the
forthcoming Sections.

REMARK 2. One may i_isk why the lreatment of such nonsmooth effects as collisions should rest only
on measure differential equations, instead of more general evolution laws involving time­
dist1ibutions of higher order. Sorne justification of this peculiarity may be found in [M, 1989a] : the
unilaterality of the non inter-penetrability constraint imposes on contact impulsions a sign condition.
Now it is known that a signed dist1ibution is automatically of order zero, i.e. il equals a measure. Let
us stress Ùlat ilie present formulation owes noiliing Lo a so-called prin.ciple of constrain.t, according to
which "constraints shall be maintained by forces, so long as this is possible; otherwise, and only
otherwise, by impulses".


5. The general form of a contact law

    As already said, in CD methods, one starts with the choice of a subdivision of the investigated
lime interval. Over each subinterval, persistent contacts are to be treated on the same footing as
possible collisions. Also some previously effective contacts may get loose at some instant and, even
in the case of smooth motions, this is known to be a nontiivial matter. The traditional approach to
contact break consists in tentatively calcuiating the motion under the assumption that a.JI contacts
present at a considered instant remain effective. If the calculation of contact forces in the course of
such a motion yields, at a further instant, an unfeasible direction, one concludes that some contacts
should break at this instant, so the continued motion has to be calculated differently. But contacts
which break are not necessarily those for which unfeasible contact forces were just found (for the
frictionless case, see [Delassus, l 9 l 7][M, 1963]).
   In order Ùlat the algoiithms handle ail such circumstances correctly, one has to design carefully the
contact laws, i.e. the admitted relationships between Ùle local velocilies and the corresponding contact
forces - mare generally the densities of contact percussions with regard to a base measure dÀ.. For
each contact assumed to correspond to a �ertain constraint fonction f, such a law bas the form

(5.1)                                 law(t, q, 'li, 9() = true.
For legibility, the index a specifying the concemed contact has been dropped and one simply writes
'1( instead of 2(-f. Strictly speaking, the no1mal unit n and the mapping G:R11�R3 make sense
only if contact holds, i.e. if f(t,q)==O. For constructing nume1ical methods (as well as in the study of
existence of solutions [Monteiro Marques, 1993]), the definition of these two elements is assumed
extended, in a smooth arbitrary way, to values of t and q laying in a neighborhood of the
hypersurface f==O.
    One is looking for motions which, in addition to the dynamical equation (3.3), actually taken
under its nonsmooth form (4.6), satisfy the geometrical conditions of non inter-penetrability (3.1).
Contact laws will be formalized in such a way that they take care of that a/so.
   Here is the key concept.

DEFINITION. A relation of the form (5.1) is said to be a complete contact law if it involves the three
following implications

(5.2)                          f(t, q) < 0� '1(== 0,

(5.3)                          f(t,q)� O� n.'U�O.

(5.4)                          n.'U > 0 � 'R.:- O.

Let us comment on the importance of (5.3). Put
                         { 'U E R 3 : n. 'U �o) if f(t, q) � 0
(5.5)        �t, q) == {
                         R 3 if f ( t,q) < 0,
called the set of the right-admissible values for the relative velocity of the two concerned bodies at
the contact point M. The following is easily established [M, 1986b]

    Let I be a time-interval with origin t and let a motion q:I�R 11 be defined through a locally
                                           0
integrable velocity function u:I�R 11 by relation (4.3). If 'U(t) == G(t, q) u(t) + 'W(t, q) belongs to
'.K(t, q(t)) for almost every t and if inequality f(t, q(t)):c;O holds at the initial instant t , then this
                                                                                               0
inequality holds for every teI.

   In other words, provided the initial position is correct, the non inter-penetrability condition f::;O is
automatically taken care of by (5.3). Observe that this statement is sensitive Lo the ordering of time.
In the symmeu·ic assertion involving, instead of the initial instant t ,the possible final point of I, one
                                                                      0
should replace '.K by -'.K, which may be viewed as the set of the left-admissible values of 'U.
   The importance of (5.4) will only become apparent in the next Sections, devoted to the treatment
of collisions and to numerical algorithms.
   In order to demonstrate that ù1e concept of a complete contact law has more theoretical consistency
than a mere programming LJick, two usual examples are presented below.
    Let us first recall a standard definition of Convex Analysis.
    Let C denote a convex subset of R3 and let aeC. The subset

(5.6)                  Nc(a) == {xeR3 : VyeC x.(y-a):c;O)
is called the ( outward) normal cane to C at point a. In the context of Convcx Analysis. it proves
consistent to define Nc(a)=0 if aé C. For every aeC, Nc(a) con tains at lcast the zero of R3 and
reduces to ù1is single element whenever a is an interior point of C.
   The normal cone more generally makes sense when a pair of arbitrary linear spaccs is considered,
with a bilinear pairing playing the role of the dot product of R3. That is a common situation in
Mechanics, the two linear spaces then consisting of 'forces' and 'vclocitics'. paired through the
bilinear form 'power'.

EXAMPLE l : Frictionless contact.
    Let us denote by 9{{,'ll) the normal cone at point 'Ue R3 to the convex set '}(!t, q) defined in
(5.5). For f(t, q)�O. the latter is a closed half-space, so '.\!:( 'U)={0} if n. 'U>Ü and 9{{_ 'l1)=0 if
n. 'U<Ü. If 'U lies in the boundary of the half-space, 9{{,'U) consists of the half-line gcnerated by -n.
For f(t, q)<Ü the set '!((t, q) equals the whole of R3 , so '.\!:('ll)={O} for every 'U in this case.
Consequently, in the writing

(5.7)                   - 1{_E 9{{_ 'll)

a complete contact Iaw is fo1mulated.
   This relation implies in particular that, in case of proper contact, 1( helongs to the half-line
generated by n : iliis is ilie traditional no friction assumption.

EXAMPLE 2 : De Saxcé's formulation of Coulomb's Law.
   Wilh a contact exhibiting dry friction, one associates the cane of Coulomb C, a convex cone of
R3 (with vertex at the origin) containing the vector n in its interior. In the traditional case, C is
axissymmetric about n , but considering more general convex cones provides for the formulation of
anisotropie friction.
   Let T denote the orthogonal plane to n in R3. Every elements 'l1 and 1( of R3 may uniquely
be decomposed in the form

                                                    'llyET,

                        1(= 2q+ �n,                             �ER.

Let D1 = { 2qET: 2q +ne C} (the 'unit section' of C) and define in T ù1e real function

                        'TET-? cpj('I) = sup{'T.SE R: se-Di).

In the traditional case of isotropie friction wiili coefficient µ, one simply°has cp1 ('I) = µ ll'TII. Put the
convention C={O} if f<O. Using arguments of Convex Analysis, one establishes [De Saxcé, 1992]
that ù1e relation between 'U and 1( consisting of the system of conditions

(5.8)                   'UE '1(,           1{.eC,

with '!( defined as in (5.5), is a complete contact law which reduces to the law of Coulomb in the
standard case. Furthermore, one may prove iliat for every pair ('Il, S)

                        Vo/e '1(,          VseC
so that (5.8) expresses that the real function (o/,5) � '!l.s + cp1 ('vir-)SN, separately convex with regard
to o/ and S, attains at the point ('ll,?(J its minimal value relative to the product set 'JO(C and that this
minimal value is zero. This is a special case of what De Saxcé calls the method of 'bipotentials',
useful in the numerical treatment of va1ious dissipative laws.


6. Collisions

   Let us corne back to the setting of Sec. 4. At the instant te of a collision, the velocity function
t�u(t)E Rn is expected to present ajump between well defined limits u-(te) and u+(te)· Concerning
a contact of index a, active at this instant (this in particular may be the contact suddenly introduced
by the collision) ajump is expected for the local velocity, as expressed by (3.4). It has been observed
in Sec. 4 that the value that one might ascribe to u at the very instant te has no relevance to the
equations of Dynamics. If a contact law of the form (5.1) has then to be invoked, what value of 'l1
shall be used ? The choice of this value is part of the mode! adopted to describe the mechanical effect
of the collision. The complexity of this effect has been stressed in Sec. 2 and we choose here a
pragmatic approach, primarily aimed at making tJ1e algorithms work whatever are the circumstances
met. Fortunately as already said, in the case of spherical bodies the resulting collision mode!
coïncides with that which has been discussed by other authors and expe1imentally tested. The case of
bodies of other shapes is still an object of research.
   For every a a contact law of the form (5.1) is declared to hold between the contact impulsion sa
and the local average velocity 'lia defined through its normal and tangential components as follows
                          a      Prv
                              ---'---"'-      -         1   +
(6.1)                   'llCJ.N=          'llCJ.N + -- 'llaN E R
                               l +Pa                l +Pa
                          a � -                       l   +
(6.2)                  'llaT=            'llaT + -- 'll aT E T .
                               l+'ta               l+'ta
Here Pa and 'ta are chosen constants with values in the interval [0,1). The meaning of Pa is
made clear by iliis observation
   Suppose that the contact law accepted for the considered contact is complete in the sense of Sec. 5.
It readily results from condition (5.2) to (5.3) that, as far as S a does not vanish, one has
n.'llt= 0, i.e. in view of (6.1)

(6.3)

which mean that Pa is identical to Newton's restitution coefficient in this case.
   But for cases where several contacts are present in the system at time te , it is essential to observe
that (6.3) is not secured anymore if the mathematical treatment yields sa= O. This is precisely what
makes the above formulation able to handle in a logical way the problem, familiar in the earthquake
engineering literature, of the rocking of a slender rectangular block suppo11ed by a fixed horizontal
plane. For simplicity, assume the lower edge slightly concave, so that contact can only occur
through the two lower corners. Let the left corner remain in contact for an episode where the black
rotates to iliè right, until ilie Iight corner collides. If at this time Newton's assumption was applied to
both contact points, no rocking could be found.
  Similarly, if the admitted contact law involves a sufficient amount of dry friction for implying
V�T= 0 in a certain situation, one finds

(6.4)

   In view of (6.3) and (6.4), Pa and 'ta may respectively be called the normal and tangential
restitution coefficients.
   If the admitted contact law is the (complete) law of Coulomb, the friction coefficient µa has also
to be included in the data relative to the considered contact. There is no algorithmic difficulty in
making al! these coefficients depend on circumstances. In particular, they may be functions of 'lJô.
so that the restitution coefficients may depend on the strenght of the collision and that the collisional
friction coefficient may be different from the static or dynamic friction coeflïcicnts used for lasting
contacts.
    One may convince onest:lf of the importance of the coefficient 'ta by applying the above
formalism to the bounce of a ball against a plane and discussing the consequcnces of possible
backspin.
    An important issue is the energy balance of a collision. Authors [Stronge, 19901[Brach,
I991](Wang & Mason, 1992] stress that, in collisions involving bodies deprived from the customary
symmetry properties, a treatrnent based on Newton's restitution assumption may yield an increase in
the system energy, even though the system is scleronomic. In general, the prevention of such an
unphysical consequence when the above mode! is used, would require that the three coefficients
satisfy certain inequalities. Let us only observe that, when the trick of using an average local velocity
first appeared [M. 1988b], this was with Pa and 'ta assuming the single value PE l] for ailro.
contacts. The energy balance of a collision for a multicontact system may in this case be drawn from
(4.2) in the form

(6.5)          � -- � =    !   A (u1- u1)(uj- uj )o-f v�. sa .
                                ij

with 8 = 1--p/l +pE (0,1] called the dissipation index. The first term on the right-hand side is sure to
be nonnegative since the matrix A is positive definite. If the contact laws admitted to hold at the
various contacts points are ail dissipative (such is the law of Coulomb), this equality entails a
decrease of kinetic energy. Incidentally, equality (6.5) is only a special case of the expression of the
dif.ferential measure of the fonction t-nic in Nonsmooth Dynamics, obtained through the Dif.ferential
Calculus of functions with locally bounded variation [M, 1988a](see also [Moreau & Valadier,
1987]).

REMARK 1. As early as [Lecomu, 1905] it has been recognized that, in the dynamics of systems
involving dry friction, velocity jumps may occur even in the absence of collision. Such an event is
due to paroxysms in the contact forces, similar to the locking effect commonly observed in the statics
of the same systems. One may call them frictional catastrophes. They logically appear in the
framework of Nonsmooth Dynamic, as demonstrated in [M, 1988b] (on this subject, see also [Wang
& Mason, 1992] or for an account of early literature on unilateral constraints and frictional contact
[Pérès, 19531).
REMARK 2. If the contact law invoked in conjunction with the above averaging trick is the complete
law offrictionless contact (5.7), the coefficient 'ta becomes immaterial. If in addition Pa is made
equal to zero, one obtains the 'standard inelastic shocks' introduced by [M, 1985), a paper which
may be read as an introduction to the present treatment of collisions in multicontact systems.


7. A model algorithm

    Algorithms based on the foregoing may affect di verse forms (see e.g. [Jean, 1993, 1994)). Here
is a typical set-up, which has in fact been used in computing the examples of Sec. 8.
    Let [tl'tF ), tF = t 1+h, denote an interval of the time discretization. Starting with qI, ul' the
approximate values of q and u at time tl' the objective is to calculate qF' Up the approximate values
at the end of this interval.

IDENTIFICATION OF CONTACTS
   Introducing the middle time tM= t1 +! h and a test position qM = q1 +ih u1, the set of the contacts
                                        2
to be treated as active is estimated as



DISCRETIZATION OF TIŒ MEASURE DIFFERENllAL EQUATION (4.6)

            A(qM)(uF-uI) = h F(tM'q M, uI) + L o;(tM,qM)s�,
                                              �EJ
where S�e R3 denotes the impulsion at contact �- In sho1t



CONTACTLAWS
(7.2)                  Va.el:

where the average local velocity 'l.l� is defined according to Sec. 6

(7.3)                      a -
                       'l.laN     Pa · - --           1      +
                              =       - 'l.laN +        'l.laN
                                l +Pa              l+Pa
(7.4)                      a      'ta       -       1     +
                       'l.la T= -- 'l.laT + -- 'l.laT ·
                                1 +'ta           l +'ta
Possibly Pa and 'ta , the normal and tangential restitution coefficients assigned to the contact a, will
be made dependent of the impact velocity 'l1a.· Here 'lFa. and 'l.ftx are estimated through (3.5) , with uF
and u1 playing the roles of u+ and u- respectively, namely

(7.5)                  'l.la =Gau!+ 'Wa ,      � =Gau F + 'Wa.
If the contact a takes place between a body of the system and some external boundary with
prescribed motion, the term 'Wa equals the negative of the boundary velocity vector at the estimated
contact point at lime tM while, for a contact occuITing between two members of the system, this term
vanishes.
FINAL POSITION



ITERATIVE PROCEDURE
   The heaviest part of the computation consists of solving the system of conditions (7.1) to (7.5).
Contact laws considered in the foregoing Sections were positive/y homogeneous with regard to
velocities. This allows one to replace conditions (7.2) Lo (7.5) by

  VaEJ: lawa(paGaNu I + G             u +(l+p )'W ' 'C G u +GaTu F +(1+-ca)'WaT' f1') = true,
                                 aN    F     a   aN   a aT I

to be joined with (7.1). Here is a relaxation technique, amounting to treat a succession of single­
contact problems.
    Let an estimated solution ue}ti, Se�ti , � running through J, be obtained, wi th (7.1) satisfied. One
attempts to construct a corrected estimate, say uc�IT . s gIT, by altering only S a , i.e. scgIT = Sc�ti fo r
                                                            c
� ;t: a. The new estimate is astrained to satisfy (7. l), i.e. since the old cstimatc satislïes the same,

(7.6)          éoIT=uesti+A-IG*(s a -s a .)
                F     F       a COIT  esu '

and to satisfy the law·of contact a under the form written above. By applying Ga to bath members of
(7.6) one gives to this contact law the following form

(7.7)          law a('Zfon sL+G ue�Li+H (S a -s a .) S a )=true
                         a     a I·    a COIT esu ' COIT       '

where the expression 'Uc�st , an element of R 3, is defined through its normal and tangential
components


                  'lfonsl _
                    aT - 'taG aTUI + (l+'Ca)'WaT ·
and Ha = GaA-1G: is a symmetric positive definite 3x3 matrix.
   Solving (7.7) with regard to the unknown Sc�IT is, in usual cases, easy. The above computation
will then be iterated, with a ranging cyclically through J. The decision of stopping iterations may be
taken on observing the magnitude of Sc�IT-Se�ti and this turns out to be equivalent to checking the
precision at which each pair 'l{,s a satisfies the corresponding contact law. Observe that, provided
this precision check is made, the operator Ha in (7.7) may be replaced by any other mapping with
zero Iimit at the origin : Ùlis may be used in tricks for accelerating convergence.
   Clearly,'tl1is algoriÙlm tolerates a certain amount of violation of the impenetrability constraints. By
adjusting the step-length and the st9pping criterium, one may keep these errors arbitrarily small and
prevent Ùleir accumulation.
   The iterated calculation is very simple, but needs to be repeated many Limes in case of numerous
contacts. Since equation (7.1) is only preserved from one iteration to the next through the
conservation condition (7.6), one should think of the possible accumulation of arithmetic errors. For
safety, one ma� refresh ue}ti from time to time, by returning to (7.1) while keeping the constructed
approximate values of S�: Ùlis proves useful oiily for motions involving Ùlousands of contacts.
   Technically, let us also observe that in many usual applications, the nxn matrix A is constant and
diagonal. d a is a 3xn matrix, but only the elements corresponding to the two bodies involved in
contact a are nonzero. So the treatment of large collections of bodies does not require the handling of
large matrices.
   The convergence of this algorithm has not been proved and not even the existence of a solution to
the problem it addresses. Uniqueness certainly does not hold in general, since the mec·hanical
problem of determining the reactions in a closely packed collection of 1igid bodies (for instance a wall
made of rectangular blacks) is usually hyperstatic.

REMARK. At every time-step, the above algorithm is ready to face velocity jumps, would they result
from collisions or arise as frictional catastrophes (Sec. 6). lt also manages correctly the possible
breaking of contacts, automatically overcoming the difficulties recalled at the beginning of Sec. 5.


8. Size segregation in vertically shaken granular materials

    When a vesse! containing grains of different sizes is vertically shaken, one commonly observes a
progressive accumulation of larger grains at the top of the pack, even if they are denser than the rest.
Similar segregation may also occur in other situations of granular dynamics : flow on a slope,
rotating drum (deceptively intended to act as a mixer), etc. and is a nuisance in industrial processes
such as the preparation of pharmaceuticals. This is commonly called the 'Brazil nut effect' [Rosato et
al., 1987).
    The case of vertical shake, to which this lecture is restricted, has been the subject of a fairly large
number of studies tending to explain the segregative effect on the basis of statistical mechanics
[Mehta & Barker, 1991) or proposing explicit mechanisms at the scale of individual particles [Jullien
et al., 1992][Duran et al., 1993). The same authors have also made use of computer simulations, but
not of the properly dynamic sort. These simulations, based on geometry and random drawings (in
so-called 'Monte Carlo methods'), are rather meant to test the consequences of tentative conceptions;
they may be viewed as an aid to reasoning.
    In real situations, several different and possibly antagonistic effects are liable to intervene, so that
phenomena may depend qualitatively on the expe1imental parameters. Anyway, computer simulations
performed by the CD method [M, 1993) strongly suggests that past physical expe1iments, intended to
display size-segregation by shaking, produced no proof of any tendency of the larger abjects to
migrate upwards relatively to the rest of the material. The created animations of two- or three­
dimensional granular motions show that, if such a tendency exists, it was anyway masked by an
extremely apparent convection effect.
    Figure 2 is extracted from a series of two-dimensional computations. The upper-left drawing
shows the positions of grains at some reference instant. From the center of each, a line is drawn
representing the grain displacement after exactly 16 shakes of the containing vesse!. An overall
circulatory flow is very visible, in which the large abject takes part in the same way as its
surroundings. Animations show it reach the agitated top region (the long straight lines appea1ing in
this region are the net results of the ballistic flights that small abjects perform with only few
collisions) then d1ift to one corner where it remains indefinitely. ·A Jess vivid demonsu·ation is
                                               Vcrtically vibrated vcsscl:
                                              Freq11ency: 20 hertz
                                              Peak to peak a111pli111de: 2 . .5 mm(ma.r. acceleration : 2g)

                                               Two-dimcnsional circular objccts
                                             N11111/Jer: .500
                                             Larger o/Jjecr : 0 5 mm
                                             Smaller o/Jjects: 0 unifnrmly distributcd bctwccn 0.7.5
                                             and 1.5 mm

                                              Contact pmamctcrs :
                                             Friction coefjïcient : 0.8 el'erywhere
                                             Tangential restitution: 0 e1•eryivhere
                                             Normal restit11tio11: 0.9 bctwccn cin:ular objects
                                                                    0.6 with boundarics

                                                   1
                                              L& : stroboscopie displaccmcnts ovcr 16 vibration
                                              pcriods (initial positions shown in grey).

                                             BELOW : stroboscopic trajcctories of the large objcct
                                             and of an initially adjacent smallcr one ovcr 600
                                             vibration periods.


 The downward boun.dary currents appear too thin to recycle the large object.

                                                                                     595
                                                            period 600
                                                                                           \
                                                                                            \
                                                                                                ''
                     period 600




                                                                    /
                                                             period O
      period 0


Fig. 2. - Boundary-induced circulation and size-segregation (two-dimensional example).
provided by the bottom drawings of Fig. 2, where the 'stroboscopie' trajectory of the large abject
over 600 shakes may be compared with that of an initially adjacent smaller one.
   The motor of the circulatory flow appears to be a boundary effect producing strong downward
currents in thin boundary layers. Boundary currents are tao thin to recycle large abjects down, so
size-segregation may be viewed as the result of a sort of filtration.
    Repeated numerical experiments, with wider vesse! and the number of abject augmented
proportionally, show the same boundary layers but naturally slower general circulation. The two
upper corner vortices, already mentioned in Sec. 2, may be identified in ù1is set-up too and are able to
take rather large abjects into limited incursions downwards. When collections of abjects with
dispersed sizes are considered, the relative accumulation of the larger ones in the upper part of the
vesse! manifests itself statistically.
    Friction is essential in the generation of boundary currents. Computation performed in the same
conditions as above, except that the fliction coefficient between beads and boundaiies is made equal
to zero, yields no circulatory flow and the large abject does not move upwards.
    Three-dimensional computation, involving sphe1ical beads in a square-based vesse!, has produced
completely similar results.
    Only one month before the distribulion of ù1e book [M, 1993], there appeared the paper [Knight et
al., 1993] reaching the same conclusion on the basis of three-dimensional experiments : size
segregation was found the result of friction induced downward boundary currents, too thin to take
large abjects back down once these have been brought to the top by the central upward overall
motion. The difficulty of observing internai cutTents in the bead pack led these authors to consider,
instead of an oscillatory motion of ù1e container, a succession of cycles, each of them consisting of a
single vertical shake followed by a return of everyù1ing to rest. The simulation by CD computation of
such an alternance of shakes and return to rest is of great interest and will be the abject of a future
publication.
    In this lecture, a regime of sinusoïdal vertical oscillation is considered, as in the 2D case.
    Figure 3 has been created by computing the motion of 3630 spherical beads of uniform size
contained in a vertically .shaken cylind1ical vesse!. The geometrical data are the same as in [K. et al.],
namely a cylindrical vesse! with diameter 3.5 cm and beads with diameter 0.2 cm. The objective is
only to investigate the generation of circulatory flows, so no larger abject has been introduced.
    The upper-left drawing of Fig. 3 shows beads whose centers initially lie in a meridian slice of
thickness equal to one ball diameter. Their displacements over 10 periods of shaking reveal a
circulatory flow similar to that of Fig. 2.
    The bottom of Fig. 3 shows the graphs, over a time interval equal to one period of the sinusoidal
shake, say 0.04 s, of the two following quantities
• upper curve : the total pressure exerted by the lateral boundary of the cylindrical vesse! upon the
pack of beads, i.e. the sum of the normal components of the forces that this surface exerts on
contacting beads,
 • lower curve : the sum of the vertical components of the same forces, taken as positive in the
upward direction.
    More precisely, the considered lime interval has been divided into 50, each of these subintervals
 corresponding to 40 �teps of the algorithm. At each point o·f division is plotted the average value of
the concerned quantity over the 40 precedings steps. Of course, at every step of the algo1ithm, 'force'
 means the quotient of a computed impulse by the step duralion. At time 0, the vesse! is at its lowest
                                                                        Cylindrica/ vesse/ : 0 3.5 cm
                                                                        Vertical vibration : frcquency 25 hertz,
                                                                                             pcak to peak amplitude 0.2 cm
                                                                                             (maximal accclcration 2.51 g)
                                                                        Beads : 0 0.2 cm, total numher 3630
                                                                        Conract parameters : friction 0.8,
                                                                                             normal restitution 0.95,
                                                                                             tangcntial restitution 0.4


                                                                        LEI'T: Beads with centers initial/y located in a
                                                                               meridicm slice ofthickness 0.2 cm:
                                                                               stroboscopie disp/acements over 10 periods
                                                                               of vesse/ vibration




    BELOW :   Total reaction exerted by the /ateral cyli11drical bo11ndary 11pon the pack of beads
              (normal and vertical components, rime inte1w1/: 1 pcriod)




0
                                         ,·u,n�n�u,.,-.,, .............. , ..........
                                                                                   ,,. ....�-..
                                                                                              ...
                                                                                                •n•• ...•·••••••·'""'"'+' . .-....-�..




                                                                        Vertical component




                         Fig. 3. - Bcads in vertically shaken cylindrical vesse!.
position and beads, in the positions shown on the upper left drawing, are freely falling down with
little interna! agitation so the peripheral forces are practically zero. As the vesse! moves up, its bottom
 hits the lowest beads, generating a collision wave which considerably increases the mean internai
 pressure of the pack. It was found that the variations of the total normal reaction of the lateral
boundary, plotted here, nearly reproduce those of this mean internai pressure. As the pack performs
its flight loose from the vesse! bottom, its internai agitation is progressively damped by collisions so
the mean internal pressure decreases.
    The time variation of the vertical component of the total force exerted by the lateral boundary
shows a negative average. The significant effect takes place between t=O.O15 and t=0.030,
approximately. During this episode, the granular material is very fluid and its contact with the lateral
boundary displays an overall upward sliding. Peripheral beads therefore have their upward motion
damped : their maximal altitude is found notably lower than that of the others and the latter corne to
occupy the corresponding vacant space at the top. On the contrary, the downward motion undergoes
no boundary damping, because the pack pressure has become nearly zero at this time. This repeated
over many periods clearly results in an average downward boundary current.
    The contrasty evolution of the vertical component which takes place between t=O and t= 0.01
should be ascribed to brutal events occurring when the descending beads hit the vesse! bottom. The
peripheral beads, which return from a slightly lower flight than the others are found to hit the bottom
first and form a relatively dense boundary layer, before the central ones hit the bottom in their turn.
When initiating their compaction process, the latter appear to exert on the boundary beads some
forces provoking the observed boundary reactions. Presumably, these events occurring in a
compacted state of the pack do not influence the circulatory currents.
    Circulatory currents in shaken granular materials have been, independently of segregation,
intensively studied. The experiments of [Laroche et al. 1989] should be quoted, as well as the
Molecular Dynamic simulations of [Gallas et al. 1992, 1993] or the Distinct Element simulations of
[Tamura et al., 1993]. Frequently, the mode of shaking leaves the vertical boundaries fixed, while
the bottom of the container performs vertical vibrations with space-modulated amplitude. Such is the
case in [Savage, 1988], a paper stressing the prudence needed when, starting from physical
observations, one tries to infer the underlying mechanisms.
    As a conclusion to the present lecture, let us say that the enormous advantage, offered by
numerical simulations, of giving access to ail variables inside the system, also calls for extreme
prudence. In fact there always remains the possiblity of failure or inaccuracy for some of the
assumptions on which calculation is based. So ail occasions of checking the results of computation
against well calibrated experiments should be seized.


                                                    REFERENCES.

      AGENO, A. & SINOPOLI, A., 1991, Indagine teorica e sperimentale sui problema dell'urto fra blocchi rigidi, x
Congresso Nazionale Ingegnieria Sismica in Italia, Palermo.
   AUBIN, J. P. & FRANKOWSKA, H., 1990, Set-va/ued Analysis, Birkhlluser, Base!. Boston, Berlin.
   BARAFF, D., 1991, Coping with friction for non-penetrating rigid body simulations, Computer Graphies, 25, 31-
40.
      BRACH, R. M., 1991, Mechanica/ Impact Dynamics (Rigid Body .Collisions), John Wiley & Sons, 1991.
      CLARKE, F. H., 1989, Optimization and Nonsnwoth Analysis, CRM. Montréal.
   CLEMENT, E., J. DURAN & J. RAJCIŒNllACII. 1992, Experimcntal study of hcaping in a two-dimcnsional
'sanèlpile' , Phys. Rev. Lerr., 69, 1189-1192.
   CUNDALL, P. A., 1971, A computer mode! for simulating progressive l;u·gc scale movcmcnts of blocky rock
systems, In: Proceedings of the Symposium of rhe /111ernatio11al Sociery c;( Rock Mechanics. (Nancy, France.
1971),Vol.l, 132-150.
   CUNDALL, P.A. & STRACK, O. D. L.. 1979, A discrcte numcrical modcl for gnmular asscmblics. Géotechnique.
29, 47-65.
    DELASSUS. E.,1917, Mémoire sur la ù1éorie des liaisons tinies unilatérales. Ann. Sei. Ecole Nom1. Sup.. 34, 95-
179.
    DE SAXCE, G., 1992, Une généralisation de l'inégalité de Fenchel et ses applications aux lois constitutives,
Comptes Rendus Acad. Sei. Paris, Sér./1, 314, 125-129.
    DURAN. J., RAJCHENllACll,J. & CLEMENT, E.. 1993. Arching effect modcl for p;u·ticlc size scgregation, Phys.
Rev. Lei/, 70, 2431-2434.
    FOERSTER, S., LOUGE, M.,CHANG, H. & ALLIA, K., 1994, Measurements of ù1c collision prnperties of small
spheres, Phys. Fluids, 6, 1108-1115.
    GALLAS, J.A.C., HERRMANN, H. J. & SOKOLOWSK.1, S.. 1992. Convection cells in vibrating granular media,
Phys. Rev. Lei/., 69,1371-1374.
    GALLAS, J.A.C., HERRMANN, H. J. & SOKOLOWSK!, S.. 1993, Granuhu· media on a vihrating plate : a
molecular dynamics simulation, International J. of Modem Physics B. 7, 1779-1788.
   HERRMAN, H. J.: 1993,Computer simulations of granular media, ln : Disorder and gran11lar media, BIDEAU, D. &
HANSEN,A., Eds., Norm-Holland,Amsterdam, 305-320.
    HIRIART-URRUTY, J. B. & LEMARECIIAL. C.. 1993, Convex analysis and minimizarion algorithms, vol. I , li,
Springer-Verlag.
    HOGUE,C. & NEWLAND, D.E., 1993, Efficient computer mudclling of ù1e motion of arbitrary grains, ln : Powders
and grains 93, Ti-IORNTON,C., Ed., Balkema, Rotterdam, 413-419.
    JAEGER, H. M. & NAGEL, S. R., 1992, Physics of ù1e Granular State, Science, 255, 1523-1531.
   JEAN, M. & MOREAU, J. J., 1992, Unilaterality and dry friction in ù1c dynamics of rigid body collections, In :
Contact mechanics international symposium,CURNIER, A., Ed., Presses Polytechniques et Universitaires Romandes,
Lausanne, 31-48.
   JEAN, M., 1993, Numerical methods for three-dimensional dynamical problcms, In : Proc. conference Contact
Mechanics 93, Southampton,ALIAllADI, M. H. & BRElllllA, C. A., Eds., Computalional Mechanics Publications,
Southampton, Boston.
    JEAN, M., 1994, Frictional contact in collections of rigid or deformable bodies : numerical simulation of
geomaterial motions, In : Mechanics of geomaterial interfaces, SALV ADURA!, A. P. S .. Ed., Elsevier Science
Publisher, to appear.
    JULLIEN, R., MEAKJN, P. & PAYLOVITCil, ;_,..• 1992, 111ree-dimensional mode! for particle-size segrcgation by
shaking, Phys. Rev. Lett., 69, 640-643.
    KNIGHT, J. B., JAEGER, H. M. & NAGEL, S. R., 1993, Vibration-induced sizc scparation in granular media : the
convection connection, Phys. Rev. Leu., 70, 3728-3731.
    LAROCHE,C., OOUADY, S. & FAUVE S., 1989,Convective flow of granular masses under vertical vibrations , J.
Phys. France, 50, 699-706.
    LECORNU, L., 1905, Sur la loi deCoulomb, Comptes Rendus Acad. Sei. Paris,140, 847-848.
    LUN,C. K. K. & BENT,A. A., 1993,Computer simulation of simple shear llow of inclastic frictional spheres, In:
Powders and grains 93, TI-IORNTON,C., Ed., Balkema, Rotterdam, 301-306.
    MAW, N., BARllER, J. R. & FAWCETI, J. N., 1981, The rote of elastic tangential compliance in oblique impact,
ASME J. of Lubrification Techn., 103, 74-80.
    MEFTAH, W., EVESQUE, P., BIAREZ, J., SORNETfE, D. & ADRIAK, N. E., 1993, Evidence of local 'seisms' of
microscopie and macroscopic stress fluctuations during ù1e defonnation of packings of grains, In : Powders and grains
93, THORNTON, c.. Ed., Balkema, Rotterdam, 173-178..
    MEHTA, A. & BARKER, G. C., 1991, Vibrated powders : a microscopie approach, Phys. Rev. Lei/., 67, 394-397.
      MONTEIRO MARQUES, M. D. P., 1993, Differenrial Inclusions in Nons111001h Mechanical Problems: Shocks and
  Dry Friction, BirkhHuser, I3asel, Boston. Berlin.
      MOREAU, J. J., 1963, Les liaisons unilatérales el le principe de Gauss, Compres Rend11s Acad. Sei. Paris, 256,
  871-874.
      MOREAU, J. J., 1985, Standard inelastic shocks and U1e dynamics of unilatcraJ constraints, ln: Unilareral Problems
  in Structural Analysis, DEL PIERO, G. & M/\CERI, F., Eds., CISM Courses and Lectures No. 288, Springcr-Verlag,
  Wien, New York, 173-221.
      MOREAU, J. J. & VALADIER, M., 1987, A chain rule involving vector functions of bounded variation, J.
  Functional Analysis, 74 , 333-345.
      MOREAU, J. J., PANAGIOTOPOULOS, P. D. & STRANG, G., Edilors, 1988,Topics in Nonsmoorh Mechanics,
  Birk.hauser, Base!, Boston, Berlin.
      MOREAU, J. J., 1988a, Bounded variation in lime, above book 1-74.
       MOREAU, J. J. & PAN/\GIOTOPOULOS, P. D, Editors, 1988, Nonsmoorh Mechanics and Applicarions, CISM
  Courses and Lectures, n ° 302, Springer-Verlag, Wicn, New York.
      MOREAU, J. J., 1988b, Unilateral Contact and Dry Friction in Fini1e f-reedom Dynamics, above book 1-82.
      MOREAU, J. J., 1989a, An expression of classical dynamics. Ann. ln.1·1. H. Poincaré Anal. Non Linéaire, 6
  (suppl.), 1-48. Volume aJso available as: Analyse Non Linéaire , /\TTOUCII, li., AUOIN, J.-P., CLARKE, F. &
  EKEL/\ND, 1., Eds., GauUlier-Villars, Paris.
      MOREAU, J. J., 1989b, Jump functions of a reaJ inlerval to a Banach space. Annales de la Faculré de.1· Sciences de
  Toulouse, n° spécial du Centenaire, pp. 77-91.
      MOREAU, J. J., 1993, New computation metJ1ods in granular dynamics, ln : Powder.1· and grains 93, THORNTON,
· C., Ed., Balkema, Rotterdam, 227-232.
      PAOLI, L. & SCII/\TZMAN, M., 1993, Mouvements à un nombre lïni de degrés de liberLé avec contraintes
  unilatérales: cas avec perle d'énergie, Mar/1. Modelling and Nu111. Anal., 27, 673-717.
      PERES, J., Mécanique générale, Masson, Paris, 1953, Chap. 10.
      RAJCHENB/\CH, J., CLEMENT, E. & DURAN, J., 1993, Experimental study of bidimcnsional models of sand,
  Inrernarional J. ofModern Physics B, 7, 1789-1798.
      R/\OUS, M., 1993, Experimenral analysis ofrhe rocking ofa rigid /Jlock, 3rd Pan Amcrican Congrcss of Applied
  Mechanics (PACAM Ill), Sao Paolo, Brazil.
      ROSATO, A., STRANDBURG, K. J., PRINZ, F. & SWENDSEN, R. !-!., 1987, Why U1c Brazil nuts are on top: size
  scgrcgation of particulatc malter by shaking, Phys. Rev. Lerr., 58, 1038-1040.
      SI\YAGE, S. !3., 1988, Streaming motions in a bcd of vibraûonally nuidizcd dry granular material, J. Fluid Mech.,
  194, 457-478.
      STRONGE, W. J., 1990, Rigid body collisions wiU1 friction , Proc. Roy. Soc. London A, 431, 169-181.
      T/\MURA, S., i\JZAw/\, T. & K1I 11\RA, J., 1993, MechanicaJ behaviour of powdcr particlc on U1e applicd vibration,
  !nt. J. ofModern Phys.B, 7, 1829-1838.
      'OMOSIIENKO, S., 1948, Théorie de /'éla.1·riciré, Béranger, Paris, Liège.
      W/\LTON, O. R., 1984, Application of molecular dynamics 10 macroscopic particlcs. /111. .1. Engng. Sei., 22, 1097-
  1107.
      WAL TON, O. R., 1993a, NumericaJ simulation of inclastic, frictional panicle-particle in1erac1ions, ln : Parriculate
  two-phase jlow, ROCCO, M. C., Ed., Buttcrworlh-l-leinemann, Boston, 884-910.
      W /\LTON, O. R., 1993b, Numcrical simulation of inclined chute flows of monouispcrse. inelastic, frictional
  sphercs, Mechanics ofmaterials, 16, 239-247.
      W/\LTON, O. R. & BRAUN, R. L., 1986, Stress calculations for assemblics of inclastic sphcrcs in uniform shear,
  Acta Mech., 63, 73-86.
      W /\NG, Y. & M/\SON, M. T., 1992, Two-dimensional rigiu-body collisions wiU1 friction, J. Appt. Mech., 59,
  635-642.
      YEMMAS, R., 1993, Simulation.1· numériques des 111aréria11x granulaires. Thesis, Univcrsilé Montpellier Il.
