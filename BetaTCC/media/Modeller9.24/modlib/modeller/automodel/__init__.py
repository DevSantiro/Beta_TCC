"""Classes to cover most comparative modeling tasks.
     - Use the :class:`automodel` class to build one or more comparative models.
     - Use the :class:`allhmodel` class instead if you want to build
       all-atom models.
     - Use the :class:`loopmodel`, :class:`dope_loopmodel`, or
       :class:`dopehr_loopmodel` classes if you additionally want to
       refine loop regions.
"""

from modeller.automodel.automodel import automodel
from modeller.automodel.allhmodel import allhmodel
from modeller.automodel.loopmodel import loopmodel
from modeller.automodel.dope_loopmodel import dope_loopmodel
from modeller.automodel.dopehr_loopmodel import dopehr_loopmodel
from modeller.automodel import refine, generate, randomize
from modeller.automodel import assess, autosched
