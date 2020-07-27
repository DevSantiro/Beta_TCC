# Example for: model.read(), model.write()

# This will read a PDB file and write both CHARMM and mmCIF atom files without
# atomic charges or radii. For assigning charges and radii, see the
# all_hydrogen.py script.

from modeller import *

env = environ()
env.io.atom_files_directory = ['../atom_files']

mdl = model(env)
mdl.read(file='1fas')
mdl.write(file='1fas.crd', model_format='CHARMM')
mdl.write(file='1fas.cif', model_format='MMCIF')
