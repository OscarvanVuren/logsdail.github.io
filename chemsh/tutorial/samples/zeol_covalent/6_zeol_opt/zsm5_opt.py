from chemsh       import *
from chemsh.cluster.getFrozen import getNotQM

# Creation of mfi cluster fragment
zsm5 = Fragment(coords='zsm5.pun', connmode='covalent')

ff = 'zeolite_gulp.ff'

# Parameters of the qmmm object
qm_theory = NWChem(method='scf', basis='3-21g', maxiter=100)

mm_theory = GULP(ff=ff)

qm_region = zsm5.getRegion(1)

# Parameters of boundary_charge_adjust function in qmmm.py file
silicate_modifiers = {("si","o1"):0.3} # ("si1","o1"):0.3
reverse_silicate_modifiers = {("si","o1"):-0.3}

# Creation of qmmm object
qmmm = QMMM(qm=qm_theory,
            mm=mm_theory,
            frag=zsm5,
            coupling='covalent',
            qm_region=qm_region,
            bond_modifiers=silicate_modifiers,
            embedding='electrostatic',
            dipole_adjust=True)

# Defining of atoms not involved in optimization calculation
frozen = getNotQM(zsm5.natoms, qm_region)

# Using a looser than usual tolerance to ensure quick convergence
opt = Opt(theory=qmmm, 
          algorithm="lbfgs", tolerance=0.0045, trustradius="energy",
          maxcycle=500, maxene=500, frozen=frozen)

opt.run()

# Reversal of dipole-adjust so it isn't applied twice during succeeded calculations which use optimized file
qmmm.boundary_charge_adjust(reverse_silicate_modifiers)

# Saving of optimized zsm5 cluster
zsm5.save('optimized_zsm5.pun', 'pun')
