# -*- python -*-
#
#       Copyright CIRAD - INRAE
#
#       File author(s):
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
# ==============================================================================
"""
"""
# ==============================================================================
from setuptools import setup, find_packages
# ==============================================================================

setup(
    name="openalea.epymix",
    version="1.1.0",
    description="Epidemic dilution and barrier factors in Mixture crops ",
    long_description="A Python Model to study Epidemic dilution and barrier factors in Mixture crops ",

    author="* Sebastien Levionnois\n"
           "* Christian Fournier\n"
           "* Marc Labadie\n"
           "* Christophe Pradal\n"
           "* Corinne Robert\n",

    author_email="* christian.fournier@inrae.fr\n"
                 "* marc.labadie@inrae.fr\n"
                 "* christophe.pradal@cirad.fr\n",
    maintainer="",
    maintainer_email="",

    url="https://github.com/openalea/epymix",
    license="Cecill-C",
    keywords='openalea, wheat, epidemiology, desease, septoria, rust, crop-mixture',

    # package installation
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["*.txt"]},
    zip_safe=False,
    setup_requires = ['openalea.deploy'],
    entry_points = {
       "wralea": ["epymix = epymix.wralea",
                  "demo = epymix.wralea.demo"]},    
    )
