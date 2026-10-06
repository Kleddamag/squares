     Contact dynamics as a nonsmooth discrete element method
                                     Farhang Radjai, Richefeu Vincent



      To cite this version:
     Farhang Radjai, Richefeu Vincent. Contact dynamics as a nonsmooth discrete element method. Mechanics of
     Materials, 2009, 41, pp.715–728. ⟨10.1016/j.mechmat.2009.01.028⟩. ⟨hal-00689866⟩




                                        HAL Id: hal-00689866
                              https://hal.science/hal-00689866v1
                                           Submitted on 20 Apr 2012




    HAL is a multi-disciplinary open access archive             L’archive ouverte pluridisciplinaire HAL, est des-
for the deposit and dissemination of scientific re-        tinée au dépôt et à la diffusion de documents scien-
search documents, whether they are published or not.       tifiques de niveau recherche, publiés ou non, émanant
The documents may come from teaching and research          des établissements d’enseignement et de recherche
institutions in France or abroad, or from public or pri-   français ou étrangers, des laboratoires publics ou
vate research centers.                                     privés.


                                              HAL Authorization
    Contact dynamics as a nonsmooth discrete
                element method


                 Farhang Radjai and Vincent Richefeu
Laboratoire de Mécanique et Génie Civil, CNRS - Université Montpellier 2, Place
                 Eugène Bataillon, 34095 Montpellier cedex 05



Abstract

The contact dynamics (CD) method is presented as a discrete element method
for the simulation of nonsmooth granular dynamics at the scale of particle rear-
rangements where small elastic response times and displacements are neglected.
Two central ingredients of the method are detailed: 1) The contact laws expressed
as complementarity relations between the contact forces and velocities and 2) The
nonsmooth motion involving velocity jumps with impulsive unresolved forces as well
as smooth motion with resolved static forces. We show that a consistent descrip-
tion of the dynamics at the velocity level leads to an implicit time-stepping scheme
together with an explicit treatment of the evolution of the particle configuration.
We also discuss the intuitive features of the CD method with regard to collective
phenomena involved in the multicontact dynamics of granular media: the role of the
coarse-graining time δt, the precision issues and the interpretation of the restitution
coefficients.

Key words: contact dynamics method, discrete element method, nonsmooth
dynamics, Signorini’s conditions, Coulomb’s friction law, unilateral constraints.
PACS: 61.43.Bn, 81.05.Rm, 83.80.Fg, 45.70.Cc




1   Introduction


The contact dynamics (CD) method, also called nonsmooth contact dynamics
(NSCD), is a discrete element method (DEM) for the simulation of granular
materials. It emerged from a mathematical formulation of nonsmooth dynam-
ics and the subsequent algorithmic developments by J. J. Moreau and M. Jean

  Email address: radjai@lmgc.univ-montp2.fr,
richefeu@lmgc.univ-montp2.fr (Farhang Radjai and Vincent Richefeu).


Preprint submitted to Mechanics of Materials                            20 April 2012
(Moreau [1977, 1983, 1988a,b, 1993, 1994], Jean and Pratt [1985], Jean [1988],
Jean and Moreau [1992], Jean et al. [1994], Jean [1995, 1999]). The funda-
mental difference between this method and the common DEM or molecular
dynamics (MD) approach lies in the treatment of small length and time scales
involved in the dynamics of granular media. In MD-type DEM, pioneered by
P. Cundall, the particles are treated as rigid bodies but the contacts between
particles are assumed to be compliant and obeying a viscoelastic behavior in
which the local strain variables are the relative particle positions and displace-
ments (Cundall [1971], Cundall and Strack [1979], Thornton and Yin [1991],
Herrmann [1993], Thornton [1993], Pöschel and Buchholtz [1995], Thornton
[1997], Luding [1998], Matuttis et al. [1999], McNamara and Herrmann [2004],
Garca and Medina [2007], Gilabert et al. [2007], Richefeu et al. [2007]). The
time-stepping schemes used for the numerical integration of the equations of
motion imply thus a fine resolution of the small time and length scales involved
in contact interactions. In the CD method, these small scales are neglected
and their effects absorbed into contact laws together with a nonsmooth for-
mulation of particle dynamics described at a larger scale than small elastic
response times and displacements.

The CD method has been applied to investigate granular materials (Moreau
[1997], Radjai et al. [1996b, 1998], Bratberg et al. [2002], Radjai and Roux
[2002], Staron et al. [2002], Nouguier-Lehon et al. [2003], Renouf et al. [2004],
McNamara and Herrmann [2004], Taboada et al. [2005], Saussine et al. [2006],
Azéma et al. [2007], Ries et al. [2007]), as well as other mechanical systems
composed of rigid bodies with frictional contact interactions such as masonry
and tensegrity structures (Acary and Jean [1998], Nineb et al. [2006]). The
results prove often to be in good agreement with experimental observation,
and for static and plastic shear properties with MD simulations (Radjai et al.
[1995], Moreau [1997], Radjai et al. [1997a, 1999], Lanier and Jean [2000], Rad-
jai and Roux [2004]). The differences between the two methods arise mainly
from the scales of description and the presence of elastic parameters in the
MD method (Radjai et al. [1997a], McNamara and Herrmann [2004, 2006]).

In this paper, we present the CD method as a consistent model of nonsmooth
and multicontact granular dynamics expressed in contact coordinates. Nons-
moothness refers to various degrees of discontinuity in local or global charac-
teristics of a dynamical system. The mathematical concepts and tools for the
treatment of nonsmooth dynamics were developed in relation with mechanical
problems involving unilateral constraints and in the context of convex analysis;
see Brogliato [1999] for a detailed history. The multicontact feature is present
in static states and in dense flows of granular materials where spatial correla-
tions occur at large length scales and impulse dynamics is mixed with smooth
particle motions at different time scales (Bershadskii [1994], Lvoll et al. [1999],
Puglisi et al. [2002], Radjai and Roux [2002], Silbert et al. [2002], Staron et al.
[2002], Pouliquen [2004], Majmudar and Behringer [2005], Agnolin and Roux


                                        2
[2007], Behringer et al. [2007], Olsson and Teitel [2007]).

While explicit integration schemes used in the MD approach are rather straight-
forward to implement in a numerical code, the underlying model of the CD
method seems to be more complex and thus less accessible to computer im-
plementation. This paper is meant to highlight the intuitive aspects of the CD
method and to illustrate its simple but powerful logics in treating multiple
contacts.



2   Particle-scale model of granular dynamics


The dynamics of a homogeneous granular flow involves at least three different
scales: 1) small time and length scales characterizing contact interactions, 2)
intermediate scales associated with particle rearrangements and shear rate,
and 3) large length scales related to geometrical correlations at even larger
scales. The elastic response time τe of the particles and their contacts is far
below the rearrangement time characterized by the mean time interval τc be-
tween successive events (collisions, . . . ). In the same way, the relative stiffness
E/p, where E is the Young modulus of the particles and p the mean confin-
ing stress, is normally high, and hence the elastic displacements λe are tiny
compared to the mean particle size d.

Various DEM algorithms differ in the treatment of small scales. The common
denominator is that the particles are considered as rigid bodies and thus the
material behavior is attributed to the contact zones, with local strain variables
derived from rigid-body degrees of freedom (translations and rotations) of the
particles. When the small scales are numerically resolved, as in MD-like or
smooth DEM, the particle motions are smooth (twice differentiable) and the
equations of dynamics are integrated with the help of force laws governing
                                                                      ˙
particle interactions. The latter expresses the contact force f~(~δ, ~δ) between
a pair of touching particles as a (mono-valued) function of their contact dis-
placement ~δ (a displacement vector with respect to a reference state or defined
                                        ˙
geometrically) and its time derivative ~δ. With an explicit integration scheme,
the time step δt must be small compared to τe for the sake of numerical sta-
bility. Numerical efficiency often imposes the use of simple force laws (linear
elastic with viscous damping and a Coulomb friction law).

An interesting issue is whether one can or should neglect the small sub-particle
scales and turn to a model of granular dynamics at the scale of particle rear-
rangements. In other words, when only plastic granular flow is of interest, the
contact elastic strains may become irrelevant. Numerically, this also means
that large time steps can then be used and materials with very stiff particles


                                         3
simulated. Another motivation is that, when deformable particles are consid-
ered and modeled, e.g. within a finite-element approach, it is more plausible
to consider their mutual contacts as rigid, i.e. as purely unilateral constraints.
This is conform to the requirement of non-interpenetration between solid bod-
ies.

Such a particle-scale model of granular dynamics implies, however, velocity
jumps. Let δt be the time resolution (a time step in numerical simulations).
Since δt  τe , the net effect of fast collisional dynamics in a multicontact
system over the time interval δt is a finite change of particle velocities and
impulsive forces through the contact network as well as a net dissipation due to
contact plasticity or viscosity. This is similar to shock dynamics in a dilute gas
governed by binary collisions except that in the latter the impulse is confined
to a single contact at a time whereas in a multicontact system the whole
system is affected. This nonsmooth dynamics can not be described by second
order equations of motion since the accelerations are no more defined. The
model should thus necessarily be formulated at the velocity level with built-in
discontinuities.

The CD method is based on a particle-scale model of granular dynamics with
two major ingredients. First, the interactions between particles are described
by contact laws instead of force laws. In this framework, a contact is a dynamic
and unilateral element with a coarse-grained behavior over the considered time
interval δt. Secondly, the equations of dynamics are adapted to account con-
sistently for both smooth and nonsmooth motion in a time-stepping scheme.
Below, we discuss in detail these features of the CD method.



3     Nonsmooth contact laws


3.1    A dynamic contact condition


Let us consider two particles i and j and a potential contact point α between
them. We assume that a unique contact plane (line in 2D) tangent to the
two particles at α can be geometrically defined so that the contact can be
endowed with a local reference frame defined by a normal unit vector ~n and
a tangential unit vector ~t lying on the tangent plane. The orientation of the
axes is a matter of convenience. In the following, the subscripts n and t refer
to normal and tangential components, respectively, with regard to the contact
frame.

A potential contact point between two particles has the following dynamic
content. As long as the distance δn between the two particles remains positive


                                       4
(corresponding to a gap), no force is activated and the normal force fn is
identically zero. But when δn = 0, a nonnegative (repulsive) normal force
fn is mobilized at the contact point and it can take indefinitely large values
depending on the forces acting on the two particles; see Fig. 1. These conditions
define a complementary relation, called Signorini’s conditions, between δn and
fn :
    
     δn > 0 ⇒ f n = 0
    
                                                                             (1)
         n = 0 ⇒ fn ≥ 0.
    δ
    



Only one of the two alternatives is true. This mutual disjunction between the
two statements is fundamental as it implies that none of the two variables can
be reduced to a mono-valued function of the other. In other words, Signorini’s
conditions define a degenerate, i.e. multi-valued, interaction law. It can be
represented as a graph displayed in Fig. 2. Symbolically, we represent this
complementarity relation as follows:
          S
    δn ←→ fn .                                                               (2)


A contact is persistent if both δn = 0 and un = δ̇n = 0. The normal force
vanishes at a breaking contact, i.e. when δn = 0 and un > 0. Hence, Signorini’s
complementarity relation can be developed as follows:
    
      δn > 0 ⇒ f n = 0
    
    
    
    
    
               
                 un > 0 ⇒ fn = 0
                                                                            (3)
    
    
     δ n = 0 ∧
    
               u = 0 ⇒ f ≥ 0
                
                    n          n



In this form, Signorini’s conditions contain a kinematic constraint: For a con-
tact, i.e. for δn = 0, we have
          S
    un ←→ fn .                                                               (4)


The full dynamic content of Signorini’s conditions appears for the second
derivative δ̈n = u̇n with respect to time where the relative acceleration δ̈n and
fn will obey Signorini’s complementarity relation. However, in a nonsmooth
formulation where velocity jumps are expected, we have to stay at the velocity
level and the relation (3) should further be reinterpreted according to the
coarse-graining time, as we shall see below.

The three alternatives in (3) lead to the condition of a complete contact law


                                       5
                              i

                                                  j
                                fn
                                     δn




                Fig. 1. A potential contact between two particles.

                                           fn



                                                      δn




         Fig. 2. Characteristics of Signorini’s complementarity relation.

formulated by Moreau as follows (Moreau [1994]):
    
     δn > 0 ⇒ f n = 0
    
    
    
    
    
      δn ≤ 0 ⇒ un ≥ 0                                                        (5)
    
    
    
       un > 0 ⇒ fn = 0
    
    
    



In this writing, δn ≤ 0 corresponds to the condition of a geometrical contact
which was expressed in (3) and (1) by an equality. The first and third con-
ditions are the same as in (3). The second condition is necessary to ensure
that the particle motions will respect the unilateral nature of a contact. Up to
numerical precision, this condition in CD simulations prevents the violation
of unilateral constraints in the absence of a repulsive force law.

In the context of nonsmooth motion, the time derivative δ̇n (t) is not unique.
Assuming bounded variation, we thus distinguish between the left-limit veloc-
ity u−                                 +
      n and the right-limit velocity un which in a time-stepping formulation
should be considered as the contact velocities at times t and t + δt, respec-
tively. With a finite time resolution δt, the actual velocity is immaterial since
only left and right velocities (and the velocity jumps) enter the dynamics;


                                       6
see section 4. In analogy with a binary collision, the main unknown of the
                                                                              −
problem is u+n that we would like to calculate given the approach velocity un
attributed to the beginning of the time step in a time-stepping scheme. The
contact model depends on the choice of the velocity un and the nature of the
force fn involved in the complementarity relation (3) or the relations (5) of a
complete contact law in the context of nonsmooth evolution.

In a granular flow, the normal velocity un at a contact evolves during a time
interval δt either as a result of smooth motion or due to impulses generated
by collisions. These impulses propagate through the contact network so that a
contact may experience several successive impulses during δt. Such events can
be resolved for a sufficiently small time increment δt or they may be tracked
according to an event-driven scheme. The event-tracking strategy is, however,
numerically inefficient, of limited applicability and in contradiction with the
scope of the CD method based on coarse-grained dynamics.

Moreau recognized that the approximation of the contact force fn during δt is
a measure problem in the mathematical sense (Moreau [1994, 2004]). A static
or regular force f s is the density of the measure f s dt with respect to dt. In
contrast, an impulse p generated by a collision has no density with respect to
dt. In other words, the forces at the origin of the impulse are not resolved at
the scale δt. In practice, however, we can not differentiate these contributions
in a coarse-grained dynamics, and the two contributions should be summed
up to a single measure dfn0 . Then, the contact force is defined as an average of
this measure over δt:
            t+δt
         1 Z
    fn =        dfn0                                                          (6)
         δt
               t



With this definition, the equations of dynamics can be formulated as measure
differential equations, as we shall see in section 4. Except in static equilibrium
where the forces are of static origin, fn generally depends on time resolution.
For large time steps, the fast dynamics, e.g. successive collisions or rearrange-
ment events, is partially filtered out and the remaining effect appears as an
average force p/δt, in addition to the static part fns . For small enough time
steps, the fast dynamics prevails and the corresponding contribution p/δt in-
creases.

As to the velocity un involved in Signorini’s condition (3), a simple and phys-
ically motivated choice is to assume that un is a weighted mean between u−       n
                    −
and u+n : u n = η u n + (1 − η)u+
                                n , where η is a material parameter characterizing
the contact. The value η = 0 seems plausible as it corresponds to a comple-
mentarity Signorini relation between the mean force fn and the right-limit
velocity u+ n which is the main unknown of the problem. However, for un = 0



                                       7
this choice leads to u+
                      n = 0. But, according to (3) nonzero forces occur only for
un = 0. Hence, this choice implies that, independently of the dynamics of the
system, nonzero forces will occur only at persistent (u+ n = 0) contacts. This
choice eludes thus the treatment of collisions with nonzero normal restitution
coefficient en for which the contact is not persistent (u+ n > 0) although the
corresponding force or impulsion is nonzero. For η 6= 0, a binary shock implies
        −
−u+n /un = η/(1 − η). Identifying this ratio with en , one gets η = en /(1 + en ).
Hence, we set
                    −
           u+
            n + en un
      un =            .                                                         (7)
             1 + en


Notice that, in contrast to the common definition of restitution coefficient for
binary collisions, Eq. (7) is not a kinematic relation between u−          +
                                                                 n and un ; It
is simply the expression of a weighted mean velocity that is assumed to obey
                            S
Signorini’s conditions un ←→ fn . Its exact role in the CD model will become
clear in combination with the equations of dynamics.


3.2   Coulomb’s friction law


The Coulomb law of dry friction is, by definition, a complementarity relation
between the friction force ft and the sliding velocity ut at a contact point
between two particles:
      
        ut > 0 ⇒ ft = −µfn
      
      
      
      
      
      
       ut = 0 ⇒ −µfn ≤ ft ≤ µfn                                                (8)
      
      
        ut < 0 ⇒ ft = µfn
      
      
      



where µ is the coefficient of friction and it is assumed that the unit tangential
vector t points in the direction of the sliding velocity so that ~ut · ~t = ut . The
graph of this complementarity relation is displayed in Fig. 3. Like Signorini’s
conditions, this is a degenerate law that can not be reduced to a mono-valued
function between ut and ft . For a concise expression of Coulomb’s law, we will
use the following notation:
          C
      ut ←→ ft .                                                                (9)


As in the case of Signorini’s conditions, it is useless to consider higher order
developments (for ut = 0 and u̇t = 0) in the context of nonsmooth motion.
This can be useful only in a system or for system parameters for which the


                                        8
                                                ft

                                                µfn

                                                           ut


                                     −µfn



                             Fig. 3. Coulomb’s friction law.


contact network does not evolve and the contact status (sliding/nonsliding,
force-transmitting/nontransmitting) fully characterizes the mechanical state.
In the MD method, the second condition (the vertical branch) of Coulomb’s
friction law (8) is replaced either by a tangential elastic relation or by a viscous
law. This regularization transforms the complementarity relation into a mono-
valued function at the price of introducing small local strain or strain-rate
parameters into the problem.

In the framework of the CD model, Coulomb’s law needs to be reformulated
to incorporate velocity discontinuities and impulsions for a large integration
time δt. The points discussed with regard to Signorini’s conditions in section
3.1 apply also to Coulomb’s conditions. The force ft at a contact represents
the average effect of static and impulsive forces experienced by the contact
during the time lag δt. The sliding velocity ut entering Coulomb’s law (8) is
thus a mean velocity. Along the same lines as for normal contact reactions, a
simple model consistent with tangential restitution is to set

                       −
           u+
            t + et ut
    ut =                 .                                                     (10)
             1 + |et |


where et ∈ [−1, 1] is the tangential restitution coefficient. This expression of
                                            C
ut is assumed to obey Coulomb’s law ut ←→ ft .

The complementarity relations (3) and (8) together with the expressions (7)
and (10) of the mean velocity define a coarse-grained model of frictional con-
tact with three material parameters µ, en and et . This model can be used to
treat frictional contact problems for deformable or undeformable bodies. It
has the unique feature of combining static and impulsive forces in the same
framework. The rich content of this model can be appreciated only in inter-
play with the equations of dynamics, as we shall see below for granular media
composed of rigid particles.


                                            9
4     Nonsmooth dynamics in contact frame


4.1    Equations of dynamics


The rigid-body motion of the particles in a granular assembly is governed by
Newton’s equations under the action of imposed external bulk or boundary
forces F~ext , and the contact reaction forces f~α exerted by neighboring particles
at the contact points α. The contact reactions may involve contact torques
but torque transmission will not be considered here. We also consider mainly
a 2D system since our focus here is on the method rather than its applications
to various geometries. An absolute reference frame with unit vectors (x̂, ŷ)
is assumed, and we set ẑ = x̂ × ŷ. Each particle is characterized by its mass
m, moment of inertia I, mass center coordinates ~r, mass center velocity U       ~,
angular coordinates θ, and angular velocity ωẑ. For a smooth motion (twice
differentiable), the equations of motion of a particle are

       ~˙ = F~ + F~ext
      mU
                                                                              (11)
      I ω̇ = M + Mext


where F~ = α f~α and M = ẑ · α ~cα × f~α where ~cα is the contact vector
             P                     P

joining the center of mass to the contact α and Mext represents the moment
of external forces.

For a nonsmooth motion with time resolution δt involving impulses and ve-
locity discontinuities, an integrated form of the equations of dynamics should
be used. As discussed in section 3, every force sums up static and impulsive
actions so that it should naturally be represented as a measure dF~ 0 rather
than a density with respect to time. It has a density F~ with respect to dt only
for a smooth motion. Hence, the equations of dynamics should be written as
an equality of measures:

         ~ = dF~ 0 + F~ext dt
      m dU
                                                                              (12)
      I dω = dM0 + Mext dt


where dF~ 0 = α df~0α and dM0 = ẑ · α ~cα × df~0α . These measure differential
              P                      P

equations can be integrated over δt with the definition of F~ as an approxima-
tion of the integral over dF~ 0 :
      t+δt
      Z
           dF~ 0 = F~ δt                                                      (13)
       t



                                       10
In the same way, we set tt+δt dM0 = M δt. With these definitions, the inte-
                            R

gration of Eq. (12) over δt yields


         ~+ −U
      m (U   ~ − ) = δt F~ + δt F~ext
                                                                                    (14)
      I (ω + − ω − ) = δt M + δt Mext



where (U~ − , ω − ) and (U
                         ~ + , ω + ) are the left-limit and right-limit velocities of the
particle, respectively. In this form, the accelerations are replaced by velocity
jumps U ~+ − U  ~ − and ω + − ω − , and Newton’s equations take the form of an
equality between the change of momenta and the average impulse during δt.

Although Eqs. (14) may be considered as resulting from a direct integration
of smooth equations (11) over a short time lag, the formulation of dynamics in
terms of measures is a necessary step in a rigorous mathematical formulation
undertaken by Moreau and other precursors of nonsmooth mechanics. For
example, from this formulation, it becomes clear that, according to (13), F~
is a coarse-grained force. This means that, its dynamic content depends on
the time resolution δt. Clearly, in a quasi-static granular flow, the contact
forces F~ reflect basically the confining stresses which are regular static forces
applied on the system, so that the value of the time step in CD simulations will
have negligibly small effect on the calculated forces. In contrast, for a faster
flow and in dynamic transients during quasi-static flow, the value of time
step matters. This should not, however, be considered as a numerical artifact
but rather as a physical effect reflecting the nonsmooth character of granular
flow. Such effects of the integration time are also observed in MD simulations.
For example, it was shown that the velocity distributions and their spatial
correlations obtained from the integration of particle displacements crucially
depend on the integration time (Radjai and Roux [2002]).

The equations of dynamics can be written in a compact form for a set of
Np particles by using matrix representation. The particles are labelled with
integers i ∈ [1, Np ]. The forces and force moments Fxi , Fyi , Mi acting on the
particles i are arranged in a single high-dimensional column vector represented
by a boldface letter F belonging to R3Np . In the same way, the external bulk
forces Fext,x , Fext,y , Mext applied on the particles and the particle velocity com-
ponents Uxi , Uyi , ω i are represented by column vectors Fext and U , respectively.
The particle masses and moments of inertia define a diagonal 3Np × 3Np ma-
trix denoted by M . With these notations, the equations of dynamics (14) are
cast into a single matrix equation:

     M (U + − U − ) = δt(F + Fext )                                                 (15)


                                          11
4.2   Transfer equations


In the MD method, the equations of motion of the particles are integrated
with the help of force laws which express the contact forces as a function of
the actual mechanical state (particle positions and velocities) of the system.
In the CD method, the contact forces are not explicit functions of the state.
Hence, the forces and velocities should be determined at the same time. To
this end, as the contact laws are expressed in contact variables, we need to
express the equations of dynamics in the same variables.

The contacts are labelled with integers α ∈ [1, Nc ], where Nc is the total
number of contacts. Like particle velocities, the contact velocities uαn and uαt
can be collected in a column vector u ∈ R2Nc . In the same way, the contact
forces fnα and ftα are represented by a vector f ∈ R2Nc . We would like to
transform the equations of dynamics from F and U to f and u.

The formal transformation of matrix equations (15) is straightforward. Since
the contact velocities u are linear in particle velocities U , the transformation
of the velocities is an affine application:

      u=GU                                                                  (16)



where G is a 2Nc × 3Np matrix containing basically information about the
geometry of the contact network. A similar linear application relates f to F :

      F =H f                                                                (17)



where H is a 3Np × 2Nc matrix. We will refer to H as contact matrix. It
contains the same information as G in a dual or symmetric manner. It can
easily be shown that

      H = GT                                                                (18)



where GT is the transpose of G. This property can be inferred from the
equivalence between the power F · U developed by ’generalized’ forces F and
the power f · u developed by the bond forces f . In general, the matrix H
is singular and, by definition, its null space has a dimension at least equal to
2Nc −3Np . A schema of this transformation from particle dynamics to transfer
equations is displayed in Fig. 4.


                                      12
                                                       dynamics
                                               i
                                           U                        Fi

                                     H T,αi                             H iα


                                          uα                        fα
                                                     contact laws
                                                   transfer equations

      Fig. 4. Matrix transformation between particle and contact coordinates.
The matrix H iα can be decomposed into two matrices Hniα and Htiα such that

      uαn =       HnT,αi U i
              P
              i                                                                         (19)
      uαt =       HtT,αi U i
              P
              i



and

      Fi =        (Hniα fnα + Htiα ftα )
             X
                                                                                        (20)
              α



Using these relations, Eqs. (15) can be transformed into two equations for
each contact α:

      unα+ − uα−                     HnT,αi M −1,ij { (Hnjβ fnβ + Htjβ ftβ ) + Fext
                                                                                j
                                                                                    }
                               P                          P
              n = δt
                               i,j                         β
                                                                                        (21)
      uα+ − uα− = δt HtT,αi M −1,ij { (Hnjβ fnβ + Htjβ ftβ ) + Fext
                                                                j
                                                                    }
                    P                P
       t     t
                    i,j              β



We now can make appear explicitly linear relations between the contact vari-
ables from Eqs. (21) and definitions (7) and (10). We set

      Wkαβ               HkT,αi M −1,ij Hkjβ2 ,
                  X
         1 k2
              =             1
                                                                                        (22)
                   i,j



where k1 and k2 stand for n or t. With this notation, Eqs. (21) can be rewritten
as

      1 + en α
            (un − uα−     αα α      αα α
                   n ) = Wnn fn + Wnt ft
        δt
                                         αβ β                       j
                                αβ β
                                                    HnT,αi M −1,ij Fext
                         X                        X
                       +     {Wnn fn + Wnt ft } +                       (23)
                                      β(6=α)                               i,j



                                                        13
                                                             2α
                                            !cα
                                              2
                               1α
                                            α
                                      !cα
                                        1        !nα
                                                       !tα



Fig. 5. The geometry of a contact α between two particles 1α and 2α with contact
vectors ~cα and contact frame (~nα , ~tα ).
      1 + et α
            (ut − uα−     αα α      αα α
                   t ) = Wtn fn + Wtt ft
        δt
                                αβ β     αβ β
                                                  X T,αi       j
                                                   Ht M −1,ij Fext
                         X
                       +     {Wtn fn + Wnt ft } +                  (24)
                             β(6=α)                               i,j



The coefficients Wkαα1 k2
                          for each contact α can be calculated as a function of
the contact geometry and inertia parameters of the two partners 1α and 2α
of the contact α. Let ~cαi be the contact vector joining the center of mass of
particle i to the contact α. The following expressions are easily established:


              1      1    (cα )2 (cα )2
      αα
     Wnn =        +      + 1t + 2t ,
             m1α m2α       I1α       I2α
                            α 2
              1      1    (c )      (cα )2
     Wttαα =      +      + 1n + 2n ,                                                (25)
             m1α m2α       I1α        I2α
                     α α     α α
                    c c     c c
      αα
     Wnt       αα
           = Wtn  = 1n 1t + 2n 2t ,
                     I1α      I2α

where cαin = ~cαi · ~nα and cαit = ~cαi · ~tα are the components of the contact vectors
in the contact frame; see Fig. 5. Note that the coefficients Wkαα        1 k2
                                                                              are inverse
reduced inertia.

An alternative representation of Eqs. (23) and (24) is


      αα α     αα α                 1 α
     Wnn fn + Wnt ft = (1 + en )      u + aαn ,                                     (26)
                                   δt n
                                   1
     Wttαα ftα + Wtn
                  αα α
                     fn = (1 + et ) uαt + aαt .                                     (27)
                                   δt
The two offsets aαn and aαt can easily be expressed from the equations (23)


                                            14
and (24). We refer to Eqs. (26) and (27) or Eqs. (23) and (24) as transfer
equations since the contact α between the two particles 1α and 2α appears here
as a unilateral element (with regard to Signorini’s conditions and Coulomb’s
friction law) allowing for force transfer according to the values of aαn and aαt
which depend on the left-limit velocity and the other forces acting on the
particles 1α and 2α . To see this point, starting with the equations of dynamics
for each of the two particles, it is easy to show that

                                                        
                           1       F~ 2α F~ 1α
                                   ext − ext  · ~
      aαn = bαn − (1 + en ) uα− +                 nα .                         (28)
                           δt n    m2α   m1α
                                                       
                           1       F~ 2α F~ 1α
                                   ext − ext  · ~
      aαt = bαt − (1 + et ) uα− +                 tα .                         (29)
                           δt t    m2α   m1α

                                                                     α−
The effect of the approach velocity (left-limit velocity) (uα− n , ut ) appears as
an impulse depending on the reduced mass and the restitution coefficient. The
effect of contact forces f~iβ acting on the two touching particles i are represented
by bαn and bαt given by


               1                       1
                         f~2α · ~nα −            f~1α · ~nα ,
                   X β                     X β
      bαn =                                                                    (30)
              m2α β(6=α)              m1α β(6=α)
               1                       1 X ~β ~α
                         f~2α · ~tα −
                   X β
      bαt =                                     f ·t .                         (31)
              m2α β(6=α)              m1α β(6=α) 1α

The transfer equations (26) and (27) define a system of two linear equations
between the contact variables at each contact point. The solution, when the
values of an and at at a contact are assumed, should also verify the contact
complementarity relations (3) and (8). Graphically, this means that the solu-
tion is at the intersection between the straight line (26) and Signorini’s graph
on one hand, and between (27) and Coulomb’s graph, on the other hand. This
is a highly nonlinear procedure for a multicontact system as discussed below.



5     Iterative determination of contact forces and velocities


5.1    Single contact problem


In order to solve the system of 2Nc transfer equations (in 2D) with the corre-
sponding complementarity relations, we proceed by an iterative method which
converges to the solution simultaneously for all contact forces and velocities.
We first consider a single-contact situation to which we will refer as the local


                                               15
                        fn                                   ft

                                                              µfn
                                        un                                ut


                                                     −µfn



Fig. 6. Solution of the local Signorini-Coulomb problem at the intersection points
between transfer equations and complementarity relations.

SC problem (SC standing for Signorini-Coulomb). It consists of the determi-
nation of contact variables fnα , ftα , uαn and uαt at a single contact given the
values of the offsets aαn and aαt at the same contact. Formally, by combining
the transfer equations (26) and (27) with the complementarity relations (4)
and (9), it is easily shown that the local SC problem is equivalent to the
following relations:


      αα α                          S
     Wnn fn − (aαn − Wnt
                      αα α
                         ft ) ←→ fnα ,                                          (32)
                                    C
     Wttαα ftα − (aαt − Wnt
                         αα α
                            fn ) ←→ ftα .                                       (33)


The solution of this problem is given by intersecting the lines representing
transfer equations with Signorini’s and Coulomb’s graphs; see Fig. 6. The
intersection occurs at a unique point due to the positivity of the coefficients
Wkαα
   1 k2
        (positive slope). In other words, the dynamics removes the degeneracy
of the contact laws. Notice, however, that the two intersections can not be
                                   αα
established separately when Wnt       6= 0. To find the local solution, one may
consider the intersection of transfer equations with the force axis, i.e. by setting
un = ut = 0. This yields two values gnα and gtα of fnα and ftα , respectively:

                        αα α
           Wttαα aαn − Wnt at
     gnα =        αα       αα 2
                                ,                                               (34)
          Wnn Wtt − (Wnt )
           αα

           W αα aαn − Wtn
                        αα α
                           at
     gtα = ααnn αα         αα 2
                                .                                               (35)
          Wtt Wnn − (Wtn      )

It can be shown that the denominator is positive. If gnα < 0, then the solution is
fnα = ftα = 0. This corresponds to a breaking contact. Otherwise, i.e. if gnα ≥ 0,
we have fnα = gnα . With this value of fnα , we can determine the solution of the
Coulomb problem. If gtα > µfnα , the solution is ftα = µfnα and in the opposite
case, i.e. if gtα < −µfnα , the solution is ftα = −µfnα (sliding contact). Otherwise,
i.e. when −µfnα < gtα < µfnα , the solution is ftα = gtα (rolling contact).


                                         16
                                 F1              F2        x



              Fig. 7. Binary frontal collision between two particles.

In order to illustrate how this works, let us consider a simple contact problem
between two disks of masses m1 and m2 and radii R1 and R2 lying on the x-
axis and subjected to constant external forces F 1 x̂ and −F 2 x̂, respectively,
where F 1 ≥ F 2 ≥ 0; see Fig. 7. We also assume that the two particles come
in touch with a relative velocity u−          2     1
                                        n = Ux − Ux ≤ 0. The normal coefficient of
restitution is en and the inverse reduced mass is Wnn = (m1 + m2 )/(m1 m2 )
since for a disk ct = ~c · ~t = 0; see equation (25). From equations (28) and (29),
we have

                          F1   F2
                                            !
                   1
    an = −(1 + en ) u−n +    +                                                (36)
                   δt     m1 m2


The transfer equation is

                         1
    Wnn fn = (1 + en )      un + an                                           (37)
                         δt


The intersection of this line with Signorini’s graph occurs on the vertical
                                                                             −
branch if an > 0, and this is the case. Hence, un = 0, and we have u+
                                                                    n = −en un
and

                                           m2 F 1 + m1 F 2
                                                                !
                 1 m1 m2
    f n = an = −            (1 + en ) u−
                                       n +                                    (38)
                 δt m1 + m2                  m1 + m2


This is an interesting expression as it shows the two origins of the total normal
force experienced by the contact. The first term is an impulsive force induced
by the impact velocity u−    n and averaged over the time lag δt whereas the
second term is a static force induced by the applied external forces F 1 and
F 2 . The first term vanishes only if the impact velocity is zero, i.e. if the two
particles initially touch. In this case, we have u+
                                                  n = 0 so that the two particles
stay in contact. The particle velocities can be calculated from the equations
of motion of each particle and the value of fn : U 1+ = U 1− + δt(F 1 − fn )/m1
and U 2+ = U 2− + δt(−F 2 + fn )/m2 . In the case U 1− = U 2− = 0, we get
U 1+ = U 2+ = (F 1 − F 2 )/(m1 + m2 ) which corresponds to the velocity of the
center of mass of the two particles.


                                       17
5.2   Multicontact problem


In a multicontact system, the terms bαn and bαt in the offsets aαn and aαt depend
on the forces and velocities at contacts β 6= α; see equations (28), (28), (30)
and (31). Hence, the solution for each contact depends on all other contacts
of the system and it must be determined simultaneously for all contacts. We
will refer to this problem as the global SC problem.

An intuitive and robust method to solve the global SC problem is to search
the solution as the limit of a sequence {fnα (k), ftα (k), uαn (k), uαt (k)} with α ∈
[1, Nc ]. Let us assume that the transient set of contact forces {fnα (k), ftα (k)}
at the iteration step k is given. From this set, the offsets {aαn (k), aαt (k)} for all
contacts can be calculated through the relations (28) and (29). The local SC
problem can then be solved for each contact α for these values of the offsets,
yielding an updated set of contact forces {fnα (k+1), ftα (k+1)}. This correction
procedure is equivalent to the solution of the following local SC problem:


       αα α                                           S
      Wnn fn (k + 1) − {aαn (k) − Wnt
                                   αα α
                                      ft (k + 1)} ←→ fnα (k + 1),                 (39)
                                                      C
      Wttαα ftα (k + 1) − {aαt (k) − Wnt
                                      αα α
                                         fn (k + 1)} ←→ ftα (k + 1).              (40)


Remark that this force update procedure does not require the contact velocities
uαn (k + 1), uαt (k + 1)} to be calculated as the offsets depend only on the contact
forces. The set {fnα (k), ftα (k)} evolves with k by successive corrections and it
converges to a solution satisfying the transfer equations and complementarity
relations at all potential contacts of the system. The iteration can be stopped
when the set {fnα (k), ftα (k)} is stable with regard to the force update procedure
within a prescribed precision criterion εf :

      | f α (k + 1) − f α (k) |
                                < εf   ∀α.                                        (41)
              f α (k + 1)


                                                                     ~ i } can be
Finally, from the converged contact forces, the particle velocities {U
computed by means of the equations of dynamics (14). The efficiency of this
iterative scheme depends on how the information (imposed boundary and bulk
forces or velocities) propagates through the system. Clearly, the information
propagates faster if the updated contact force (fnα (k + 1), ftα (k + 1)) at a
contact α is used to update also the values of the offsets (aβn (k), aβt (k)) at
the neighboring contacts β that will be treated next. This sweeping of the
contact network might be optimized to some extent depending on the expected
solution.

The iterative procedure depicted above provides a robust method which proves


                                             18
             (a)                             (b)




             (c)                             (d)


Fig. 8. Four snapshots of the normal force network during iterative resolution of the
global SC problem. Line thickness is proportional to the normal force.

efficient in the context of granular dynamics. Note that the information is
treated locally and no large matrices are manipulated during iterations. Fig.
8 shows several snapshots of the normal force network in a packing of disks
in the course of iterations. The left and bottom walls are immobile while the
top and right walls are free to move and subjected to the same confining
stress p. The sample is dense and its time evolution is not of interest here;
we rather calculate the forces and velocities by solving iteratively the global
SC problem for this system. In the time-stepping scheme this is equivalent to
the resolution of the problem over a single time step. The initial values of the
contact forces are set to zero, i.e. fnα (0) = 0 and ftα (0) = 0 for all α. We see
that the information (boundary forces) propagates from the walls smoothly
throughout the system with increasing number of iterations (130, 365, 1000
and 2000). If the iterations were stopped before the full propagation of the
information, the solution would involve strong force gradients.

The evolution of the probability distribution function of normal forces during
iterations is shown in Fig. 9. When normalized by the average normal force
hfn i at the converged state, the distribution appears to increase in width and
it becomes stable beyond 1000 iterations but carries the signature of the well-
known exponential shape of strong contact forces just after a few iterations.
The number Ni of necessary iterations to converge is strongly dependent on
the precision εf but not on δt. Fig. 10 shows Ni as a function of εf for a given
global SC problem in a packing of 2500 particles with initialization of the
forces to zero. We see that Ni diverges quite fast as εf is decreased. It should,


                                        19
                        0
                   10

                        -1
                   10                         k


               P
                    -2
                   10

                        -3
                   10 0       1      2         3      4      5       6
                                          fn / <fn>

Fig. 9. Probability distribution function of normal forces at the four iteration steps
shown in Fig. 8. The arrow points in the direction of the increasing number k of
iterations.
however, be noted that the number of iterations is substantially reduced when
the iteration is initialized with a globally correct guess of the forces. This is
the case in an evolution problem where the forces at each time step can be
initialized with the forces computed at the preceding step; see section 6.

The number of iterations is partially controlled by the special features of force
distribution in granular media. As a result of arching, the probability density
function P (fn ) of normal forces shows no or weak central tendency. A small
peak is observed when the system is isotropic. But in all cases the number
of forces tends either to a finite value P (0) as fn → 0 or diverges (Radjai
et al. [1997b], Mueth et al. [1998], Radjai et al. [1999], Antony [2001], Silbert
et al. [2002], Kruyt [2003], Metzger [2004], Majmudar and Behringer [2005],
Richefeu et al. [2006], Azéma et al. [2007], Kruyt and Antony [2007]). Hence, a
huge number of contacts (nearly 60% in a weakly polydisperse packing) carry
small forces whereas the strong forces are less in number but exponentially
distributed. It is important to remark that the weak forces cannot simply be
neglected as they play an organic role in the overall stability of the assem-
bly Radjai et al. [1998]. Due to the absence or weakness of central tendency,
an increasing number of weak contacts should be resolved as εf is decreased,
requiring thus an increasingly larger number of iterations. In sum, for a pre-
scribed precision εf , the forces below εf hfn i are not correctly calculated. This
provides a physical criterion which may be employed to calibrate the required
precision in dealing with a specific problem.

A high precision over forces might be required when the static equilibrium of
a packing is studied. During a quasistatic flow, a high precision is necessary
in the investigation of transition between successive states separated by small
time intervals δt. The trajectory is all the more determinist as the precision on
forces, and hence on velocities, is high. For longer evolutions, when some degree
of ergodicity may be assumed, it might be physically justified to consider lower
precision in each step at the level of the resolution of the global SC problem.
The choice of the precision can be combined with a more or less large time-step


                                         20
                 3000


                 2000

            Ni   1000


                    0
                        0      0.005          0.01      0.015        0.02
                                               εf

Fig. 10. The number of iterations Ni as a function of the precision criterion εf in
iterative resolution of the global SC problem when the forces are initialized to zero.

δt.

It should also be briefly mentioned that the uniqueness of solution of the global
SC problem in a multicontact system is not proved. We have 3Np equations
of dynamics and 2Nc complementarity relations. The unknowns of the prob-
lem are 3Np particle velocities and 2Nc contact forces. Since there are equal
numbers of unknowns and dynamic or contact relations, and since the solu-
tion of the local SC problem is unique, the global solution could have been
unique, too. The point is that the 2Nc contact complementarity relations are
not equations but inequations. Thus, the extent of indeterminacy of the so-
lution reflects all possible combinations of contact forces accommodating the
complementarity relations.

In fact, the CD method provides a suitable framework to study the indeter-
minacy of granular assemblies by searching self-equilibrated solutions with
external forces and particle velocities set to zero in the expressions of aαn and
aαt ; Eqs. (28) and (29). For a given configuration of particles, the standard SC
problem can thus be solved by setting external forces and particle velocities to
zero and for an ensemble {fnα (0), ftα (0)} varied according to a statistical distri-
bution. The ordering of the sequence of updated contacts during the iterative
procedure may also affect the solution. It happens that for a generically disor-
dered granular system, self-equilibrated solutions can not be found unless in
small partially or totally ordered systems. This implies that the CD treatment
of a granular assembly involves practically no indeterminacy. Thus, if slightly
different solutions are found according to the iteration method employed, they
should be attributed to the lack of precision below the convergence criterion
εf , affecting mainly the very weak contacts. The indeterminacy can be studied
also analytically by considering the null space of the contact matrix H (Rad-
jai et al. [1996a], McNamara et al. [2005]). The degree of indeterminacy may
be high, but it does not imply significant force variability since the solutions
are restrained by the complementarity relations. This is also consistent with a


                                         21
common observation in CD simulations that the force fluctuations, when they
occur, are basically of impulsive nature and not spurious effects that could be
attributed to the presence of scale-free self-stresses.



Finally, a few words about the role of the restitution coefficient en is useful. In
a binary collision, the contact opening is fully controlled by en as in the simple
example discussed in section 5.1. The situation is different in a multicontact
system where a contact can open even if u−        n = 0. In other words, contact
opening is governed by the multicontact dynamics and not only by the local
restitution. In contrast, contact closing, i.e. the creation of a persistent contact,
depends only on the local restitution coefficient. This is because, according to
                                                               −
equation (7), with en > 0 the conditions u+      n = 0 and un < 0 imply un < 0
which contradicts Signorini’s conditions. Hence, in the CD method a collision
between two particles leads to the creation of a persistent contact only if
en = 0.



The problem of multiple shocks is a complex issue that should be treated at
very small time scales of elastic waves, and this is out of the scope of the
contact dynamics model which was designed to find mechanically admissible
solutions of multicontact dynamics at much larger time scales. Experimental
observation, however, suggests that in a multicontact system multiple shocks
may occur and dissipate the whole kinetic energy at very short times so that
the effective restitution coefficient should indeed be set to zero (Luding et al.
[1994a,b], Dippel et al. [1996], da Cruz et al. [2005]). This effect is the remi-
niscence of inelastic collapse (McNamara and Young [1992]). When the time
increment δt is large enough compared to the characteristic time of successive
collisions, the choice en = 0 is relevant. In dense systems, this choice allows for
the opening and closing of contacts due to multicontact dynamics. In a loose
assembly, the time scales are different and the effective restitution coefficient
might be nonzero for coarse-grained dynamics.



It should also be mentioned that the restitution coefficients en and et in binary
collisions are not pure material parameters but depend on the surface geometry
and impact velocity (Lun and Savage [1986], Kuwabara and Kono [1987],
Smith and Liu [1992], Foerster et al. [1994], Labous et al. [1997], Luding [1998],
Brilliantov et al. [2004, 2007]). There is no fundamental difficulty in taking
such effects into account in a CD algorithm. This is also true for the coefficient
of friction µ which may depend on the sliding velocity. It should, however,
be remarked again that the manifestation of physical effects of this kind is
different under multicontact conditions with respect to binary interactions.


                                        22
6   Time-stepping scheme


The global SC problem may well occur as an event at particular instances
of a granular flow. The iterative resolution method presented above can then
be applied to calculate the contact forces and particle velocities at those in-
stances. Hence, the global SC problem may be embedded in an event-driven
algorithm which can be a useful approach in certain circumstances. The global
SC problem may also be considered for the estimation of the stability of a static
assembly of particles. In the CD method, the global SC problem is associated
with a time-stepping scheme.

In order to set up this scheme, we need to come back to the contact laws
and remark that the first condition of the Signorini relation in (3) is the
only condition referring to space coordinates. Actually, the SC problem was
formulated at the velocity level for both dynamics and contact laws, and the
first Signorini condition was accounted for by assuming that only the potential
contacts, where δn ≤ 0, were involved in the SC problem. In other words, the
contact network is defined explicitly from particle positions in a SC problem
and it will no more evolve during the coarse-graining time interval δt.

Another important feature of the global SC problem is the prospective charac-
ter of the treatment expressed by the second condition of a complete contact
law (5). This means that the right-limit velocities are calculated such that the
complementarity relations will not be violated by the subsequent motion of
the particles. This condition is achieved through an appropriate definition of
the mean velocities un and ut in Eqs. (7) and (10) entering the complementar-
ity relations. In other words, the treatment is fully implicit and the right-limit
            ~ i+ , ω i+ } may be used to increment particle positions.
velocities {U

The above two remarks devise the following time-stepping scheme. Let t and
t + δt be the considered time interval. The configuration {~ri (t)} and particle
velocities {U   ~ i (t), ω i (t)} are given at time t. The latter play the role of left-
limit velocities {U      ~ i− , ω i− } in the global SC problem. The contact network
{α, ~nα , ~tα } is set up from the configuration at time t or from an intermediate
                       i
configuration {~rm       } defined by

       i               δt ~ i
     ~rm ≡ ~ri (t) +      U (t).                                                   (42)
                       2


When this configuration is used for contact detection, other space-dependent
quantities such as the inverse mass parameters Wkαα                          ~ ext
                                                         and external forces U i
                                                    1 k2
should consistently be defined for the same configuration and at the same time
t + δt/2.


                                          23
                      3
                 10


                   2
                 10

            Ni
                      1
                 10


                   0
                 10 0                     200                       400
                                          Step

Fig. 11. The number of iterations Ni as a function of time step during a shear flow.
The imposed minimum and maximum numbers of iterations are marked by dashed
lines.
Then, the global SC problem is solved iteratively over the contact network
                                         ~ i+ , ω i+ } are calculated. The latter
and the right-limit particle velocities {U
correspond to the velocities at the end of the time step t + δt:

    ~ i (t + δt) = U
    U              ~ i+ ,                                                      (43)
    ω i (t + δt) = ω i+ .                                                      (44)

Finally, the positions are updated by integrating the updated velocities:

                       δt ~ i
    ~ri (t + δt) = ~rm
                     i
                       +  U (t + δt),                                          (45)
                       2
                       δt i
    θi (t + δt) = θm
                   i
                     +    ω (t + δt).                                          (46)
                       2

This scheme is unconditionally stable due to the implicit discretization. Hence,
no damping parameters at any level are needed. For this reason, the time step
δt can be large. The real limit imposed on the time step is the occurrence
of cumulative numerical errors leading to undesired excess overlaps between
the particles. Of course, such overlaps have no dynamic significance in the CD
method, but they falsify the geometry and thus the evolution of the system. By
construction, if there are initially no overlaps between the particles, the contact
dynamics ensures that no overlaps will occur in the course of evolution. But the
particle positions are secondary in the CD method and they are updated from
the integration of the velocities. Even for a high precision εf , the calculated
velocities and contact forces by solving the SC problem involve some numerical
imprecision that may lead to excessive overlaps at a number of contacts in the
long run. Hence, to avoid such effects, one requires both a sufficiently high
precision and rather small time steps. In high-quality simulations of shear


                                        24
flow with ≃ 104 particles, the typical value of the time step is ≃ 10−4 s. This
value is by several orders of magnitude larger than the usual values of the time
step in MD simulations. It should also be borne in mind that the time step δt
is not a precision criterion for the evolution problem in the CD method. The
precision is mainly controlled by εf . The time step should rather be considered
as a coarse-graining parameter for nonsmooth dynamics. It should be reduced
if the impulse dynamics at small time scales is of interest.

An important feature of granular dynamics is the occurrence of highly nonlin-
ear and subtle transitions at small time scales. These short-time phenomena
include sharp impulsive transitions, collective rearrangements and frictional in-
terlocking. As a result, the dynamics over successive time steps needs variable
treatment. For a rather smooth evolution less effort should be consumed than
when a major rearrangement event takes place. In the CD simulations, the
number of iterations represents the required effort at each step. For the same
level of precision, the number of iterations varies considerably in the course of
time stepping. One example is shown in Fig. 11. It can be checked that, if the
initializing forces at each step are retrieved from the last step, the number of
iterations is correlated with dynamic events. Hence, in the CD method subtle
rearrangement events are always calculated with the required high precision.
In some cases, a maximum number of iterations may be imposed in order to
increase efficiency, but this is equivalent to reducing precision when a larger
number of iterations are necessary. Moreover, incomplete relaxation leads to
wave-like perturbations in time evolution (Unger et al. [2002]).



7   Concluding remarks


In this paper, the basics of the CD (contact dynamics) method for discrete
element simulation of granular materials were presented. This method can be
viewed as the algorithmic formulation of nonsmooth granular dynamics at the
scale of particle rearrangements where small elastic response times and dis-
placements are neglected. Two major issues arising in this context are treated
in the framework of the CD method: 1) The contact laws expressed as com-
plementarity relations between the contact forces and velocities and 2) The
nonsmooth motion involving velocity jumps with impulsive unresolved forces
as well as smooth motion with well-resolved static forces. A consistent de-
scription of the dynamics at the velocity level leads naturally to an implicit
time-stepping scheme together with an explicit treatment of the evolution of
the contact network. Most concepts developed in this formulation are rather
intuitive although they rely on a sound mathematical background of nons-
mooth dynamics and convex analysis.

The focus of this paper was on the intuitive features of the CD method with


                                      25
respect to subtle collective phenomena involved in the multicontact dynamics
of granular media. In particular, we discussed the role of the coarse-graining
time δt, the precision issue in the iterative procedure for the resolution of the
global SC (Signorini-Coulomb) problem with respect to force distributions,
and the relevance of the coefficients of restitution en and et and their inter-
pretation in a multicontact system. The CD method is characterized by its
unique feature of bringing together in the same formalism two limit regimes of
granular dynamics: 1) collisional regime governed by binary shocks and incom-
plete energy restitution and 2) static regime governed by multiple contacts,
geometrical disorder, force balance and dynamic rearrangements. Hence, this
method provides a suitable framework for the investigation of dense granular
flows where smooth evolutions are intermingled with sharp transitions.

The CD method can also be considered as an adequate framework for the
numerical treatment of frictional contact problems. Indeed, the Coulomb fric-
tion and perfectly rigid contact condition are implemented in an exact form,
i.e. without introducing artificial penalization parameters or damping. Given
a contact network, all kinematic constraints implied by contact laws are si-
multaneously taken into account together with the equations of dynamics in
order to determine the velocities and contact forces in the system. This global
SC problem is solved by an iterative process pertaining to the Gauss-Seidel
iterative method that consists of solving a single SC problem at each contact,
and successively and iteratively updating the forces until a convergence crite-
rion is fulfilled (Jeffreys and Jeffreys [1988]). The method is thus capable of
dealing properly with the nonlocal character of the momentum transfers re-
sulting from the impenetrability of the particles. It can be employed to study
stiff systems for which smooth MD-like methods require small time steps for
numerical stability and the stiffness matrix may become ill-conditionned as
the contact network evolves.

The CD method is unconditionally stable due to its inherent implicit time
integration scheme. The uniqueness of the solution at each time step is not
guaranteed for perfectly rigid particles. However, the variability of admissi-
ble solutions is generally below numerical precision. The variability resulting
from numerical precision can be reduced and the calculations significantly ac-
celerated by initializing the iterative procedure at each step with the forces
computed in the preceding step.

The basic algorithm presented in this paper can be (and has been) extended
to deal with richer contact laws, various particle shapes and more efficient res-
olution of the global SC problem in 2D and 3D. Several variants of the time-
stepping scheme can be found in (Jean [2001]) and a parallelization strategy
in (Renouf et al. [2004]). The contact laws can be supplemented with a com-
plementarity relation between a torque and a contact spin variable (Bratberg
et al. [2002]). Using such a complementarity relation, the rolling friction is


                                      26
easily implemented in this framework. Adhesion forces can be introduced by
a simple shift of the complementarity relations:


         S
    un ←→ fn − fna ,                                                        (47)
         C
     ut ←→ ft ,                                                             (48)

where fna is the adhesion threshold. Particle deformability can also be treated
in the CD method by associating strain variables to the particles rather than
to the contacts. The strains can be defined either from rigid-body degrees of
freedom, as in the MD method, or associated with new internal degrees of
freedom. Concerning particle shapes, it is a generic feature of the CD method
that, in contrast to force laws, the nature of the contact complementarity
relations does not depend on the particle shape. Hence, the solver which takes
in charge the resolution of the global SC problem is independent of the particle
shape. The potential face-face or face-edge contacts are represented by three
or two points which are treated as independent point contacts by the solver
(Saussine et al. [2006], Azéma et al. [2008]). The basics of the method are the
same in 2D and 3D. The only difference lies in the treatment of the tangential
force whose direction is an unknown of the SC problem and is determined in
the course of the iterative procedure.

A particular attention should be paid to the origin of the contact forces in
the CD method. An example is the uniaxial compression of a dense granular
material by imposing a constant velocity on a wall. In the MD simulation of
this problem, the displacement of the wall causes mainly the elastic deforma-
tion of the particles and the contact forces increase accordingly. In the CD
simulation of the same problem, since the contact laws involve no force scale
and no static boundary or bulk force are applied, the force scale is fixed by the
imposed velocity through the impulsive terms in Eqs. (28) and (29). Since no
rearrangements can occur due to a too high density, the corresponding kinetic
energy is not dissipated. This energy increases adiabatically, the contact forces
increase proportionally to the displacement and the particles interpenetrate.
In contrast, if the uniaxial compression is controlled by an increasing bound-
ary force, the contact forces increase in proportion to the applied force as in
MD simulations, and, in the absence of particle rearrangements, the contact
reaction forces balance exactly the driving force so that the packing stays in-
definitely in static equilibrium. In the MD approach, the static forces are fully
encoded in the particle positions with a scale given by the stiffness. In the CD
approach, there is no such force scale and thus the static force scale should be
defined externally.

Finally, a future work on the coarse-grained granular dynamics might help
to get more insight into the dissipative and impulsive phenomena that are
modeled by their average effects in the CD method. The suggestion is to apply


                                      27
the same methodology as in (Radjai and Roux [2002]) in order to evaluate the
influence of time resolution. One can first perform a standard MD simulation
of a shear flow, then take averages over the dynamics for a given integration
time δt and finally compare this coarse-grained dynamics with CD simulations
of the same flow with a time step δt. Repeating this procedure for several
values of δt, will allow us to appreciate the CD method and compare it in a
meaningful way with the MD method.

The authors acknowledge very motivating and interesting discussions with F.
Dubois, M. Jean, J. J. Moreau and S. Roux.



References

V Acary and M Jean. Numerical simulation of monuments by the contact dy-
   namics method. In DGEMN-LNEC-JRC, editor, Monument-98, Workshop
   on Seismic Performance of Monuments, pages 12–14. LNEC, 1998.
Ivana Agnolin and Jean-Noël Roux. Internal states of model isotropic granular
   packings. i. assembling process, geometry, and contact networks. Phys Rev
   E Stat Nonlin Soft Matter Phys, 76(6-1):061302, Dec 2007.
S. J. Antony. Evolution of force distribution in three-dimensional granular
   media. Phys Rev E, 63(1 Pt 1):011302, Jan 2001.
E. Azéma, F. Radjai, and G. Saussine. Quasistatic rheology and force trans-
   mission in a packing of polyhedral particles. Submitted., 2008.
Emilien Azéma, Farhang Radjai, Robert Peyroux, and Gilles Saussine. Force
   transmission in a packing of pentagonal particles. Phys. Rev. E, 76(1 Pt 1):
   011301, Jul 2007.
R. P. Behringer, Karen E Daniels, Trushant S Majmudar, and Matthias Sperl.
   Fluctuations, correlations and transitions in granular materials: statistical
   mechanics for a non-conventional system. Philos Transact A Math Phys
   Eng Sci, Aug 2007.
A. Bershadskii. Stochastic density waves of granular flows: strong-intermittent
   dissipation fields with self-organization. Physica A, 210:386–390, 1994.
I. Bratberg, F. Radjai, and A. Hansen. Dynamic rearrangements and packing
   regimes in randomly deposited two-dimensional granular beds. Phys. Rev.
   E, 66:031303–1, 2002.
Nikolai Brilliantov, Clara Saluea, Thomas Schwager, and Thorsten Pschel.
   Transient structures in a granular gas. Phys Rev Lett, 93(13):134301, Sep
   2004.
Nikolai V Brilliantov, Nicole Albers, Frank Spahn, and Thorsten Pschel. Col-
   lision dynamics of granular particles with adhesion. Phys Rev E Stat Nonlin
   Soft Matter Phys, 76(5 Pt 1):051302, Nov 2007.
B Brogliato. Nonsmooth mechanics. Springer, London, 1999.
P. Cundall. A computer model for simulating progressive large scale move-


                                      28
  ments of blocky rock systems. In Proceedings of the Symposium of the
  International Society of Rock Mechanics, Vol. 1, 132-150, 1971.
P. A. Cundall and O. D. L. Strack. A discrete numerical model for granular
  assemblies. Géotechnique, 29(1):47–65, 1979.
Frdric da Cruz, Sacha Emam, Michal Prochnow, Jean-Nol Roux, and Franois
  Chevoir. Rheophysics of dense granular materials: discrete simulation of
  plane shear flows. Phys Rev E Stat Nonlin Soft Matter Phys, 72(2 Pt 1):
  021309, Aug 2005.
S. Dippel, G. G. Batrouni, and D. E. Wolf. Collision-induced friction in the
  motion of a single particle on a bumpy inclined line. Phys.Rev. E, 54:6845,
  1996.
S. F. Foerster, M. Y. Louge, H. Chang, and K. Allia. Measurements of the
  collision properties of small spheres. Phys. Fluids, 6(3):1108–1115, 1994.
Xavier Garca and Ernesto Medina. Acoustic response of cemented granular
  sedimentary rocks: molecular dynamics modeling. Phys Rev E Stat Nonlin
  Soft Matter Phys, 75(6 Pt 1):061308, Jun 2007.
F. A. Gilabert, J-N. Roux, and A. Castellanos. Computer simulation of model
  cohesive powders: influence of assembling procedure and contact laws on low
  consolidation states. Phys Rev E Stat Nonlin Soft Matter Phys, 75(1 Pt 1):
  011303, Jan 2007.
H. J. Herrmann. Molecular dynamics simulations of dry granular media. In
  The first Nisshin Engineering Particle Technology International Seminar:
  Discrete Particle Simulations in Powder Technology, page 8, Osaka, Japan,
  1993.
M. Jean. Unilateral contact and dry friction: time and space variables dis-
  cretization. Arch. of Mech., Warszawa, 40(1):677–691, 1988.
M. Jean. Frictional contact in rigid or deformable bodies: numerical simulation
  of geomaterials, pages 463–486. Elsevier Science Publisher, Amsterdam,
  1995.
M. Jean. The non smooth contact dynamics method. In Special issue on
  modeling contact and friction. 1999.
M Jean. Micromécanique des matériaux granulaires, chapter Simulation
  numérique discrt̀e, pages 199–324. Hermes, Paris, 2001.
M. Jean and J. J. Moreau. Unilaterality and dry friction in the dynamics of
  rigid body collections. In Proceedings of Contact Mechanics International
  Symposium, pages 31–48, Lausanne, Switzerland, 1992. Presses Polytech-
  niques et Universitaires Romandes.
M. Jean and E. Pratt. A system of rigid bodies with dry friction. International
  Journal Eng. Sci., pages 497–513, 1985.
M. Jean, F. Jourdan, and B. Tathi. Numerical dynamics for the simulation
  of deep drawing. In Proc. of IDDRG 1994, Handbooks on Theory and
  Engineering Applications of Computational Methods, May 16-17 1994.
H. Jeffreys and B. S. Jeffreys. Methods of Mathematical Physics. Cambridge,
  England, 1988.
N. P. Kruyt. Contact forces in anisotropic frictional granular materials. In-


                                     29
   ternational Journal of Solids and Structures, 40(13-14):3537–3556, 2003.
N. P. Kruyt and S. J. Antony. Force, relative-displacement, and work networks
   in granular materials subjected to quasistatic deformation. Phys. Rev. E,
   75(5):051308–8, May 2007.
G. Kuwabara and K. Kono. Restitution coefficient in a collision between two
   spheres. Japanese Journal of Applied Physics, 26(8):1230–1233, 1987.
L. Labous, A. D. Rosato, and R. Dave. Measurements of collision properties
   of spheres using high-speed video analysis. Phys. Rev. E, 56:5715, 1997.
J. Lanier and M. Jean. Experiments and numerical simulations with 2d disks
   assembly. Powder Technology, 109:206–221, 2000.
S. Luding. Collisions and contacts between two particles. In H. J. Herrmann,
   J.-P. Hovi, and S. Luding, editors, Physics of dry granular media - NATO
   ASI Series E350, page 285, Dordrecht, 1998. Kluwer Academic Publishers.
S. Luding, E. Clément, A. Blumen, J. Rajchenbach, and J. Duran. Anoma-
   lous energy dissipation in molecular dynamics simulations of grains: The
   “detachment effect”. Phys. Rev. E, 50:4113, 1994a.
S. Luding, E. Clément, A. Blumen, J. Rajchenbach, and J. Duran. Studies
   of columns of beads under external vibrations. Phys. Rev. E, 49(2):1634,
   1994b.
C. K. K. Lun and S. B. Savage. The effects of an impact velocity dependent
   coefficient of restitution on stresses developed by sheared granular materials.
   Acta Mechanica, 63:15–44, 1986.
G. Lvoll, K. J. Mly, and E. G. Flekky. Force measurements on static granular
   materials. Phys Rev E Stat Phys Plasmas Fluids Relat Interdiscip Topics,
   60(5 Pt B):5872–5878, Nov 1999.
T. S. Majmudar and R. P. Behringer. Contact force measurements and stress-
   induced anisotropy in granular materials. Nature, 435(7045):1079–1082, Jun
   2005.
H.-G. Matuttis, S. Luding, and H. J. Herrmann. Discrete element methods
   for the simulation of dense packings and heaps made of spherical and non-
   spherical particles. Powder Technology, 1999. in press.
S. McNamara and W. R. Young. Inelastic collapse and clumping in a one-
   dimensional granular medium. Phys. Fluids A, 4(3):496, 1992.
Sean McNamara and Hans Herrmann. Measurement of indeterminacy in pack-
   ings of perfectly rigid disks. Phys. Rev. E, 70(6 Pt 1):061303, Dec 2004.
Sean McNamara, Ramn Garca-Rojo, and Hans Herrmann. Indeterminacy and
   the onset of motion in a simple granular packing. Phys. Rev. E, 72(2 Pt 1):
   021304, Aug 2005.
Sean C McNamara and Hans J Herrmann. Quasirigidity: some uniqueness
   issues. Phys. Rev. E, 74(6 Pt 1):061303, Dec 2006.
Philip T Metzger. Granular contact force density of states and entropy in a
   modified edwards ensemble. Phys Rev E Stat Nonlin Soft Matter Phys, 70
   (5 Pt 1):051303, Nov 2004.
J. J. Moreau. Evolution problem associated with a moving convex set in a
   hilbert space. Journal of differential equations, 26:347–374, 1977.


                                       30
J. J. Moreau. Liasons unilatérales sans frottement et chocs inélastiques.
   Comptes Rendus de l’Académie des Sciences, 296:1473–1476, 1983.
J. J. Moreau. Bounded variation in time. In P.D. Panagiotopoulos and
   G Strang, editors, Topics in Nonsmooth Mechanics, pages 1–74. Bikhäuser,
   Basel, 1988a.
J. J. Moreau. New computation methods in granular dynamics. In Powders
   & Grains 93, page 227, Rotterdam, 1993. A. A. Balkema.
J. J. Moreau. Numerical investigation of shear zones in granular materials. In
   D. E. Wolf and P. Grassberger, editors, Friction, Arching, Contact Dynam-
   ics, pages 233–247, Singapore, 1997. World Scientific.
J.J. Moreau. Unilateral contact and dry friction in finite freedom dynamics,
   volume 302 of International Centre for Mechanical Sciences, Courses and
   Lectures. Springer, Vienna, 1988b.
J.J. Moreau. Some numerical methods in multibody dynamics: Application
   to granular materials. European Journal of Mechanics A/Solids, supp.(4):
   93–114, 1994. Formulation mathematiques tire du livre Contacts mechanics.
J.J. Moreau. An introduction to unilateral dynamics. In M. Frémond and
   F. Maceri, editors, Novel approaches in civil engineering, number 14 in Lec-
   ture Notes in Applied and Computational Mechanics, pages 1–46. Springer-
   Verlag, 2004.
D. M. Mueth, H. M. Jaeger, and S. R. Nagel. Force distribution in a granular
   medium. Phys. Rev. E, 57:3164, 1998.
S. Nineb, P. Alart, and D. Dureisseix. Approche multi-échelle des systèmes de
   tenségrité. Revue Européenne de Mécanique Numérique, 15:319–328, 2006.
C. Nouguier-Lehon, B. Cambou, and E. Vincens. Influence of particle shape
   and angularity on the behavior of granular materials: a numerical analysis.
   Int. J. Numer. Anal. Meth. Geomech, 27:1207–1226, 2003.
Peter Olsson and S. Teitel. Critical scaling of shear viscosity at the jamming
   transition. Phys Rev Lett, 99(17):178001, Oct 2007.
T. Pöschel and V. Buchholtz. Molecular dynamics of arbitrarily shaped gran-
   ular particles. J. Phys. I France, 5(11):1431–1455, 1995.
O. Pouliquen. Velocity correlations in dense granular flows. Phys. Rev. Lett.,
   93(24):248001–4, December 2004.
A. Puglisi, A. Baldassarri, and V. Loreto. Fluctuation-dissipation relations in
   driven granular gases. Phys Rev E Stat Nonlin Soft Matter Phys, 66(6 Pt
   1):061305, Dec 2002.
Radjai, Evesque, Bideau, and Roux. Stick-slip dynamics of a one-dimensional
   array of particles. Phys. Rev. E, 52(5):5555–5564, Nov 1995.
F. Radjai and S. Roux. Contact dynamics study of 2d granular media : Critical
   states and relevant internal variables. In H. Hinrichsen and D. E. Wolf,
   editors, The Physics of Granular Media, pages 165–186, Weinheim, 2004.
   Wiley-VCH.
F. Radjai, L. Brendel, and S. Roux. Nonsmoothness, indeterminacy, and fric-
   tion in two- dimensional arrays of rigid particle. Phys. Rev. E, 54(1):861,
   1996a.


                                     31
F. Radjai, J. Schäfer, S. Dippel, and D. Wolf. Collective friction of an array
  of particles: A crucial test for numerical algorithms. J. Phys. I France, 7:
  1053, 1997a.
F. Radjai, D. E. Wolf, S. Roux, M. Jean, and J. J. Moreau. Force networks
  in dense granular media. In R. P. Behringer and J. T. Jenkins, editors,
  Powders & Grains 97, pages 211–214. Balkema, Rotterdam, 1997b.
F. Radjai, D. E. Wolf, M. Jean, and J.J. Moreau. Bimodal character of stress
  transmission in granular packings. Phys. Rev. Letter, 80:61–64, 1998.
Farhang Radjai and Stphane Roux. Turbulentlike fluctuations in quasistatic
  flow of granular media. Phys Rev Lett, 89(6):064302, Aug 2002.
Farhang Radjai, Michel Jean, Jean-Jacques Moreau, and Stphane Roux. Force
  distributions in dense two-dimensional granular systems. Phys. Rev. Lett.,
  77(2):274–, July 1996b.
Farhang Radjai, Stephane Roux, and Jean Jacques Moreau. Contact forces in
  a granular packing. Chaos, 9(3):544–550, Sep 1999.
Mathieu Renouf, Frederic Dubois, and Pierre Alart. A parallel version of
  the non smooth contact dynamics algorithm applied to the simulation of
  granular media. Journal of Computational and Applied Mathematics, 168
  (1-2):375–382, July 2004.
V. Richefeu, F. Radjai, and M. S. El Youssoufi. Stress transmission in wet
  granular materials. Eur. Phys. J. E, Feb 2007.
Vincent Richefeu, Moulay Saı̈d El Youssoufi, and Farhang Radjai. Shear
  strength properties of wet granular materials. Phys. Rev. E, 73(5 Pt 1):
  051304, May 2006.
Alexander Ries, Dietrich E Wolf, and Tams Unger. Shear zones in granular
  media: three-dimensional contact dynamics simulation. Phys Rev E Stat
  Nonlin Soft Matter Phys, 76(5 Pt 1):051301, Nov 2007.
G. Saussine, C. Cholet, P.E. Gautier, F. Dubois, C. Bohatier, and J.J. Moreau.
  Modelling ballast behaviour under dynamic loading. part 1: A 2d polygonal
  discrete element method approach. Computer Methods in Applied Mechan-
  ics and Engineering, 195(19-22):2841–2859, April 2006.
Leonardo E Silbert, Gary S Grest, and James W Landry. Statistics of the
  contact network in frictional and frictionless granular packings. Phys Rev
  E Stat Nonlin Soft Matter Phys, 66(6 Pt 1):061303, Dec 2002.
C. E. Smith and P.-P. Liu. Coefficients of restitution. J. Appl. Mech., 59:963,
  1992.
L. Staron, J.-P. Vilotte, and F. Radjai. Preavalanche instabilities in a granular
  pile. Phys. Rev. Lett., 89:204302, 2002.
A. Taboada, K. J. Chang, F. Radjai, and F. Bouchette. Rheology, force trans-
  mission, and shear instabilities in frictional granular media from biaxial
  numerical test using the contact dynamics method. Journal Of Geophysical
  Research, 110:1–24, 2005.
C. Thornton. Computer simulation of impact fracture/fragmentation. In
  The first Nisshin Engineering Particle Technology International Seminar:
  Discrete Particle Simulations in Powder Technology, page 17, Osaka, Japan,


                                      32
  1993.
C. Thornton. Coefficient of restitution for collinear collisions of elastic-
  perfectly plastic spheres. Journal of Applied Mechanics, 64:383–386, 1997.
C. Thornton and K. K. Yin. Impact of elastic spheres with and without
  adhesion. Powder Technol., 65:153, 1991.
T. Unger, L. Brendel, D. E. Wolf, and J. Kertsz. Elastic behavior in contact
  dynamics of rigid particles. Phys Rev E Stat Nonlin Soft Matter Phys, 65
  (6 Pt 1):061305, Jun 2002.




                                    33
