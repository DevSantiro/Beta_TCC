from modeller import *
from modeller.automodel import *
log.verbose()
env = environ()

env.io.atom_files_directory = ['\modelos']

env.io.hetatm = True
env.io.water = True

a = automodel(env, alnfile = 'new_alinha.pir', knowns = '4hpg.pdb', sequence = 'beta_glucosidase.fasta')
a.starting_model = 1
a.ending_model = 3
a.make() 
