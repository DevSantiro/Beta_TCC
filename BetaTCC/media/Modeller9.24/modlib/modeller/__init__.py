"""MODELLER, a package for protein structure modeling

   See U{http://salilab.org/modeller/} for further details.

   @author: Andrej Sali
   @copyright: 1989-2020 Andrej Sali
"""

__all__ = ['energy_data', 'io_data', 'environ', 'group_restraints',
           'ModellerError', 'FileFormatError', 'StatisticsError',
           'SequenceMismatchError', 'model', 'alignment',
           'sequence_db', 'profile', 'saxsdata', 'density', 'pssmdb',
           'excluded_pair', 'rigid_body', 'symmetry', 'selection', 'log',
           'info', 'pseudo_atom', 'virtual_atom', 'modfile', 'features',
           'forms', 'secondary_structure', 'terms', 'physical']

__docformat__ = "epytext en"

# Version check
import sys
if sys.version_info[0] < 2 \
   or (sys.version_info[0] == 2 and sys.version_info[1] < 3):
    raise ImportError("This module requires Python 2.3 or later")

try:
    from modeller import config
except ImportError:
    config = None

def __get_python_api_ver():
    """Get the Python version at which the C API last changed."""
    ver = sys.version_info[0:2]
    if ver[0] == 3:
        if ver[1] < 2:
            return (3,0)
        elif ver[1] == 2:
            return (3,2)
        else:
            return (3,3)
    elif ver[0] == 2 and ver[1] >= 5:
        return (2,5)
    return None

def __is_64_bit_windows():
    """Return True iff we are running on 64-bit Windows."""
    # This only works on Python 2.5 or later
    if hasattr(sys, 'maxsize'):
        return sys.maxsize > 2**32
    # This works on older Pythons, but not in Python 3
    else:
        return type(sys.dllhandle) == long

# Special processing on Windows to find _modeller.pyd and Modeller DLLs:
if hasattr(config, 'install_dir') and hasattr(sys, 'dllhandle'):
    if __is_64_bit_windows():
        exetype = 'x86_64-w64'
    else:
        exetype = 'i386-w32'
    dpath = config.install_dir + '\\lib\\%s\\python%d.%d' \
                                 % ((exetype,) + sys.version_info[:2])
    if dpath not in sys.path:
        # Insert *after* first entry, so as not to break parallel module's
        # propagation of the first entry (that containing the running script's
        # directory) to slaves
        sys.path.insert(1, dpath)
    try:
        import os
        dpath = config.install_dir + '\\lib\\%s' % exetype
        if dpath not in os.environ['PATH']:
            os.environ['PATH'] = dpath + ';' + os.environ['PATH']
        # Python 3.8 or later don't look in PATH for DLLs
        if hasattr(os, 'add_dll_directory'):
            __dll_directory = os.add_dll_directory(dpath)
        del os
    except ImportError:
        pass
    del dpath
# Add Python version-specific directory to search path:
elif hasattr(config, 'install_dir'):
    api_ver = __get_python_api_ver()
    if api_ver is not None:
        try:
            import os.path, re, sys
            srch = re.compile("%s/*lib/[^/]+/?" % config.install_dir)
            for (n, pathcomp) in enumerate(sys.path):
                if srch.match(pathcomp):
                    modpath = os.path.join(pathcomp, 'python%d.%d' % api_ver)
                    if modpath not in sys.path:
                        sys.path.insert(n, modpath)
                    break
            del re, n, pathcomp, os, srch
        except ImportError:
            pass

# Set Modeller install location and license
import _modeller
if hasattr(config, 'license'):
    _modeller.mod_license_key_set(config.license)
if hasattr(config, 'install_dir'):
    _modeller.mod_install_dir_set(config.install_dir)

_modeller.mod_start()
__version__ = _modeller.mod_short_version_get()

from modeller.energy_data import energy_data
from modeller.io_data import io_data
from modeller.environ import environ
from modeller.group_restraints import group_restraints
from modeller.error import *
from modeller.model import model
from modeller.alignment import alignment
from modeller.sequence_db import sequence_db
from modeller.profile import profile
from modeller.saxsdata import saxsdata
from modeller.density import density
from modeller.pssmdb import pssmdb
from modeller.excluded_pair import excluded_pair
from modeller.rigid_body import rigid_body
from modeller.symmetry import symmetry
from modeller.selection import selection
from modeller.util.logger import log
from modeller.information import info
from modeller import pseudo_atom
from modeller import virtual_atom
from modeller import modfile
from modeller import features
from modeller import forms
from modeller import secondary_structure
from modeller import terms
from modeller import physical

# Load in readline, if available, to make interactive use easier
try:
    if len(sys.argv) > 0 and sys.argv[0] == '-' and sys.stdin.isatty():
        import readline
except (ImportError, AttributeError):
    pass

# Set job name
if len(sys.argv) > 0 and sys.argv[0] != '-':
    nam = sys.argv[0]
    if nam.endswith('.py'):
        nam = nam[:-3]
    info.jobname = nam
    del nam

del sys, _modeller, config
