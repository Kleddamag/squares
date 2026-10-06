        Force Distributions in Dense Two-Dimensional Granular
                                Systems
              Farhang Radjai, Michel Jean, Jean Jacques Moreau, Stéphane Roux



      To cite this version:
     Farhang Radjai, Michel Jean, Jean Jacques Moreau, Stéphane Roux. Force Distributions in Dense Two-
     Dimensional Granular Systems. Physical Review Letters, 1996, 77, pp.274 - 277. ⟨10.1103/PhysRevLett.77.274⟩.
     ⟨hal-00759668v2⟩




                                        HAL Id: hal-00759668
                              https://hal.science/hal-00759668v2
                                            Submitted on 2 Dec 2016




    HAL is a multi-disciplinary open access archive             L’archive ouverte pluridisciplinaire HAL, est des-
for the deposit and dissemination of scientific re-        tinée au dépôt et à la diffusion de documents scien-
search documents, whether they are published or not.       tifiques de niveau recherche, publiés ou non, émanant
The documents may come from teaching and research          des établissements d’enseignement et de recherche
institutions in France or abroad, or from public or pri-   français ou étrangers, des laboratoires publics ou
vate research centers.                                     privés.


           Distributed under a Creative Commons CC BY 4.0 - Attribution - International License
                    Force Distributions in Dense Two-Dimensional Granular Systems

                       Farhang Radjai,1 Michel Jean,2 Jean-Jacques Moreau,2 and Stéphane Roux3
                                      1
                                     HLRZ, Forschungszentrum, 52425 Jülich, Germany
               2
                LMGC, Université de Montpellier II, Place Eugène Bataillon, 34095 Montpellier Cedex 05, France
                            3
                              LPMMH-ESPCI, 10 rue Vauquelin, 75231 Paris Cedex 05, France

                Relying on contact dynamics simulations, we study the statistical distribution of contact forces inside
             a confined packing of circular rigid disks with solid friction. We find the following: (1) The number
             of normal and tangential forces lower than their respective mean value decays as a power law. (2) The
             number of normal and tangential forces higher than their respective mean value decays exponentially.
             (3) The ratio of friction to normal force is uniformly distributed and is uncorrelated with normal force.
             (4) When normalized with respect to their mean values, these distributions are independent of sample
             size and particle size distribution.



   Despite the highly uniform density of a random pack-              system, characterized by a set of inequalities, define
ing of noncohesive particles, photoelastic visualizations            a region in the configuration space presenting a large
provide a striking evidence of the heterogeneous distribu-           number of edges and corners. Moreover, the basic
tion of contact forces on a scale definitely larger than the         Coulomb’s law of friction, relevant to most of the granular
typical particle size [1–3]. A quantitative characteriza-            media of interest, is a nonsmooth law in the sense that
tion of these distributions is relevant both to mechanical           friction force and sliding velocity at a contact are not
processing (compression, compaction, flow, grinding) and             related together as a function. Finally, in the case of
fundamental understanding (mesoscopic scales, instability            collisions velocity jumps occur, so that the evolution is
thresholds) of granular media [4–7].                                 not globally governed by differential equations in the
   This Letter is concerned with a numerical study of                classical sense.
this problem in confined two-dimensional packings at                    The most commonly used algorithms are based on reg-
static equilibrium. We are interested in the statistical             ularization schemes. In this way, impenetrability is ap-
distributions PN and PT of normal forces and (absolute               proximated by a steep repulsive potential and Coulomb’s
values of) friction forces N and T, independently of                 law by a viscous friction law, to which smooth compu-
contact orientations. We also study the distribution Ph              tational methods can be applied. The dominant feature
of the dimensionless variable h ­ T yN, which is a                   of the CD method is that the conditions of perfect rigid-
measure of friction “mobilization” within the Coulomb                ity and exact Coulombian friction are implemented, with
range f0, mg, where m is the coefficient of friction between         no resort to any regularization. At a given step of evo-
disks. Scaling with sample size and relation among the               lution, all kinematic constraints implied by lasting in-
three distributions will be considered too.                          terparticular contacts and the possible rolling of some
   Numerical results will be presented here for four                 particles over others are simultaneously taken into ac-
samples of 500, 1200, 4025, and 1024 particles, referred             count, together with the equations of dynamics, in order
to as samples A, B, C, and D, respectively. Particle                 to determine all contact forces in the system. The method
radii are uniformly distributed between 3.8 and 7.5 mm in            is thus able to deal properly with the nonlocal character
samples A and B, and between 1.5 and 7.5 mm in sample                of the momentum transfers— resulting from the perfect
C. Sample D contains 192 particles of radius 1.6 mm, 320             rigidity of particles in contact.
particles of radius 1.05 mm, and 512 particles of radius                Detailed descriptions of the CD method can be found
0.65 mm. Particles are contained in a rectangular frame              in the literature [8–10]. In relation with the present in-
composed of one planar base, two immobile walls, and                 vestigation, we would just like to underline the point that
one horizontal plane (the lid) free to move vertically and           dynamics is an essential ingredient of this approach. It is
on which a downward force of 6600 N is applied. The                  well known that a granular system at static equilibrium is
acceleration of gravity is set to zero in order to avoid force       hyperstatic; i.e., for given boundary conditions there is a
gradients in the sample. Particle-particle and particle-base         continuous set of possible contact forces. This is due both
coefficients of friction are 0.2 and 0.5, respectively. All          to the absence of an internal displacement field (because
other coefficients of friction are zero.                             of perfect rigidity) and to the nonsmooth character of the
   For this investigation, we have relied on the contact             friction law [11]. In the CD method, the force network at
dynamics (CD) approach to the dynamics of perfectly                  static equilibrium is determined through the dynamic pro-
rigid particles with unilateral contacts. Since particles            cesses from which it relaxed. In other words, as in real
cannot interpenetrate, the allowed configurations of the             granular systems, the static values of forces are reached



                                                                 1
asymptotically as the kinematic energy of the system is             the mean are well fitted by an exponential decay. In order
dissipated in friction and collisions.                              to see the behavior at low forces, we have shown in Fig. 3
   Of course, this does not mean that the statistical dis-          the normalized log-log plots of the distribution of the
tribution of forces is necessarily dependent on the prepa-          logarithm of the forces. The data for forces lower than
ration process. The most probable force distribution may            the mean have a power-law distribution. We conclude
well result from the generic disorder of granular systems           that the normalized distribution of normal forces is inde-
[3]. However, density is a major control parameter of the           pendent of our sample sizes and can be approximated by
mechanical properties of granular materials, and only in            a power-law decay with a crossover to an exponential cut-
the steady state, reached after enough shear-induced vol-           off,
ume change, it acquires a rather well-defined value for a                               Ω
                                                                                          sNykNlda ,    N , kNl,
given confining pressure [12]. That is why we applied the                        PN ~ bs12NykNld                           (1)
                                                                                          e          , N . kNl.
same procedure to prepare all samples in the same state:
Filling the box with particles under gravity, shearing by           We find a ­ 20.3 and b ­ 1.4. It is important to notice
moving the base horizontally (dilation occurs then), stop-          the collapse of normalized data on the same distribution
ping shear and applying the confining load on top of the            in spite of the fact that the size dispersity of particles
sample, and, finally, setting the gravity to zero and allow-        is not the same in all samples. The mean values seem,
ing the system to relax to equilibrium under the load. Al-          however, to depend on size dispersity since they do not
though the algorithm is quite efficient compared to other           scale with system size as shown in Table I. On the other
available techniques, the whole procedure requires hun-             hand, the lack of statistics at low normal forces in sample
dreds of CPU hours on a fast Unix workstation (Sparc 20)            D as compared to sample B, giving rise to the fluctuations
for each sample.                                                    observed in Fig. 3, suggests that the “branching process”
   Figure 1 shows the network of normal forces in sample            generating low forces from the high applied force on the
D. One can observe both large contact-to-contact fluctu-            system is more efficient in systems with a continuous
ations and a subnetwork of “force chains” that seem to              distribution of particle sizes.
carry a significant portion of the applied external stress.            The semilogarithmic and log-log plots of the probabil-
Forces range from 0.003 to 1127 N, i.e., a range of 6 or-           ity distributions of the T are displayed in Figs. 4 and 5.
ders of magnitude, which clearly requires a scaling analy-          The data are normalized with respect to the mean kT l in
sis. The mean normal force is kNl ­ 249 N and more                  each sample, and, as we see, they nicely collapse on the
than 60% of contacts carry a force lower than the mean.             same distribution. This is again essentially a power-law
   Figure 2 displays semilogarithmic plots of probability           decay with a crossover to an exponential cutoff,
distributions PN of normal forces in the four samples.                                   Ω           0

Forces are normalized with respect to their mean in each                                   sTykT lda     T , kT l ,
                                                                                  PT ~ b 0 s12TykTld                        (2)
sample. The normalized distributions coincide over al-                                     e           , T . kT l .
most the whole range, and the data for forces larger than           We find a 0 ­ 20.5 and b 0 ­ 1.
                                                                       We also studied the probability distribution Ph of h ­
                                                                    T yN. This is a uniform distribution except for a small
                                                                    peak at h ­ m. The uniformity of this distribution may




FIG. 1. Network of normal forces in sample D; see
Table I. Forces are encoded as the widths of intercenter con-       FIG. 2. Semilogarithmic plots of the probability distributions
necting segments.                                                   of normalized normal forces NykNl.



                                                                2
FIG. 3. Log-log plots of the probability distributions of          FIG. 4. Semilogarithmic plots of the probability distributions
normalized normal forces NykNl.                                    of normalized friction forces T ykTl.

                                                                   One may check that integration of the two members
be attributed to the random structure of the contact net-          of Eq. (3) with respect to N and T over f0, 1`g, with
work. On the other hand, it is likely that the rather weak         the substitution T ­ hN in the right-hand side together
singularity at h ­ m is a “signature” of the dynamics of           with the constraint h [ f0, mg, implies a normalized Ph
preparation. Indeed, only at sliding contacts is the fric-         over the Coulomb range f0, mg. Introducing the uniform
tion force fully mobilized. If a granular assembly relaxes         distribution Ph shd ­ 1sf0, mgd in Eq. (3) and integrating
asymptotically towards static equilibrium, then the set of         with respect to N over f0, 1`g with the substitution
the last sliding contacts at the equilibrium threshold might       N ­ Tyh in the right side, we get the following relation
remain fully mobilized. We checked that when the sys-              between PN and PT :
tem is sheared by the motion of the basal plane, the peak
                                                                                           1 Z 1`           dx
at h ­ m can rise to 50% of contacts, whereas the dis-                           PT sT d ­         PN sxT d    .          (4)
tribution remains uniform within f0, mf. Finally, we note                                  m 1ym             x
that the normal forces for which h ­ m are much smaller                This equation implies that the initial power law of the
than the average, so that the peak may well result also            two distributions PN and PT should be the same: a ­
from an imperfect relaxation.                                      a 0 . Moreover, an exponential upper cutoff of normal
   Another important result regarding friction mobilization        forces yields an exponential-integral cutoff for friction
is the statistical independence of h with respect to               forces, i.e., essentially an exponential decay times a
N. Whatever the value of N, friction is indifferently              slowly varying function. Going back to Figs. 2–5, we
mobilized within the Coulomb range f0, mNg (apart from             see that such refinements are out of reach within the
the above discussed small peak). Such an assumption
allows one to relate in a simple way PN to PT . Let
PsN, Td be the joint probability distribution of normal and
friction forces. Since h is statistically independent of N,
we may write PsN, Td as a product of PN and Ph times
the Jacobian of the transformation sN, T d ! sN, hd,
                            1
         PsN, T d dN dT ­     PN sNdPh shd dN dT .       (3)
                            N

TABLE I. Number of particles p, number of contacts c, width
L, mean normal force kNl, and mean friction force kTl in our
samples A, B, C, and D.
Sample       p       c       L (mm)     kNl sNd      kTl sNd
  A          500     806       260        592          51
  B         1200    1969       389        213          18
  C         4025    6293       620        219          21
  D         1024    1498        65        249          23          FIG. 5. Log-log plots of the probability distributions of
                                                                   normalized friction forces T ykT l.



                                                               3
statistical precision. On one hand, the cutoff may well              experiments [3]. Weaker forces are technically difficult
be an exponential-integral function. On the other hand,              to measure, and their distribution has not been observed.
the equality of exponents is consistent with the rough               The exponential tail has also been obtained through the
determination of these exponents.                                    usual simulation methods [15], and, what is more, a recent
   Equation (4) can, however, be directly checked from               theoretical model provides plausible statistical arguments
the data. In Fig. 6 we have plotted both PT and the                  in favor of it [3]. This statistical model is likely to
probability distribution obtained from PN via Eq. (4) for            apply only to the subnetwork of force chains, which
sample C. They are almost the same with a very good                  carries in effect most of the applied external load and
precision, although we assumed a uniform distribution of             in our simulations belongs to the exponential tail. The
h with no additional peak on the edge h ­ m. This                    characteristic force at this scale is essentially imposed by
validation of Eq. (4) is also an indirect check of the               the external load and the ratio of the system size to the
statistical independence of h with respect to N.                     largest particle size. On the other hand, the power-law
   Finally, integration of Eq. (4) with respect to T yields          decay of weak forces, if confirmed by other investigators,
the following relation between the mean values:                      indicates the self-similar nature of weak contacts that do
                               m                                     not belong to the subnetwork of large forces. Indeed,
                      kT l ­     kNl.                     (5)        such contacts do not feel the external load, and hence
                               2                                     their distribution can give rise to a power law through
This relation is approximately satisfied for our samples, as         a self-similar branching process with no intrinsic scale.
can be seen in Table I.                                              This observation also suggests that the exponents a and
   In view of these findings, we would like to underline             a 0 depend on the interparticular friction coefficient m.
some salient aspects of the problem. One important                      We gratefully acknowledge many fruitful conversations
point concerns the scale of statistical homogeneity of               with D. E. Wolf. This work has been supported by
granular systems. Despite local force fluctuations, the              the Groupement de Recherche “Physique des Milieux
present study shows that for a sample as small as                    Hétérogènes Complexes” of the CNRS.
1200 particles the force distributions are clearly defined
over several decades. An increase in sample size does
nothing but improve statistics. Hence, as far as stress
is concerned, the linear scale of statistical homogeneity
                                                                      [1] P. Dantu, in Proceedings of the 4th International Con-
in a 2D assembly is a few tens of particle diameters.
                                                                          ference on Soil Mechanics and Foundations Engineering
This is what comes out also from the study of anisotropy                  ( Butterworths Scientific Publications, London, 1957).
in angular distributions of contact forces [13,14]. This              [2] T. Travers, D. Bideau, A. Gervois, and J. C. Messager,
observation is crucial for a continuum approach to the                    J. Phys. A 19, L1033 – 1038 (1986).
mechanics of granular media, needed in most of the usual              [3] C. H. Liu, S. R. Nagel, D. A. Schecter, S. N. Coppersmith,
technological problems.                                                   S. Majumdar, O. Narayan, and T. A. Witten, Science 269,
   Another point is that only the exponential tail of the                 513 (1995).
distribution of normal forces, comprising nearly 40%                  [4] E. Guyon, S. Roux, A. Hansen, D. Bideau, J. P. Troadec,
of contacts in our simulations, has been observed in                      and H. Crapo, Rep. Prog. Phys. 53, 373–419 (1990).
                                                                      [5] H. M. Jaeger and S. R. Nagel, Science 255, 1523 (1992).
                                                                      [6] Disorder and Granular Media, edited by D. Bideau and
                                                                          A. Hansen ( Elsevier, North-Holland, Amsterdam, 1993).
                                                                      [7] D. E. Wolf, in Computational Physics: Selected Meth-
                                                                          ods —Simple Exercises—Serious Applications, edited by
                                                                          K. H. Hoffmann and M. Schreiber (Springer, Heidelberg,
                                                                          1996).
                                                                      [8] J. J. Moreau, Eur. J. Mech. A, Solids 13, 93 –114 (1994).
                                                                      [9] M. Jean, in Mechanics of Geometrical Interfaces, edited
                                                                          by A. P. S. Selvadurai and M. J. Boulon ( Elsevier Science
                                                                          B. V., Amsterdam, 1995), pp. 463– 486.
                                                                     [10] F. Radjai and S. Roux, Phys. Rev. E 51, 6177 (1995).
                                                                     [11] F. Radjai, L. Brendel, and S. Roux, Phys. Rev. E (to be
                                                                          published).
                                                                     [12] A. N. Schofield and C. P. Wroth, Critical State Soil
                                                                          Mechanics (McGraw-Hill, London, 1968).
                                                                     [13] L. Rothenburg and R. J. Bathurst, Géotechnique 39, 601 –
                                                                          614 (1989).
FIG. 6. Log-log plots of the distribution PT of normalized           [14] B. Cambou, in Powders and Grains 93, edited by
friction forces and the one obtained by applying Eq. (4) to PN            C. Thornton (Balkema, Rotterdam, 1993).
in sample C.                                                         [15] K. Bagi, in Powders and Grains 93 (Ref. [14]).



                                                                 4
